# AT_TO_FP_Form.py
# Script parses AT form def file and creates Free Pascal (Lazarus) .lpr .lpi .pas and .lfm file template for application 
#
# TO DO:
# some documention would be nice
# add missing controls
# add auto generate of button click events
# 
# Process basics:
# NOTE!! Assumes AT Form sizing  (Scale) is pixels !!!
# User Selects AT form file to process (Open) 
# User Loads form into table (Load)
# User Processes from into Free Pascal skeleton  (Genereate)
#
# All files are created in the same directory as the AT form definition file, suggest creating  unique directory for each generated application skeleton.
#
# This is a work in progress !!
# 
"""This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>"""

#
import PySimpleGUI as sg
import pathlib
from LPI_TEMPLATE import LPI_TEMPLATE

# all important scaling value - scales AT form controls by set amount
PSCALE = 1.10    # 110%

# all important default values for controls. I know this is a hack, fix it!
DFLT_ITEM_HEIGHT = 'ItemHeight = 16'    # used for listbox and combobox
DFLT_LABEL_BACK = 'clInactiveCaption'   # AT can draw labels with border style, not so for FP, just change background

#from tkinter import Tk
#from tkinter.font import Font

# debug flag dbg (results in printing debug info to terminal / output window)
dbg = 'none'
#dbg = 'yes'
#dbg = 'all'

dbg_process_form = False
dbg_output_controls = False

if dbg == 'all':
    dbg_output_controls = True
    dbg_process_form = True


#sg.theme('BrownBlue')
sg.theme('SystemDefault')
# --
# some constants
#

FORMVALUE_EMPTYCELL = '-       -'
EMPTYCELL = '~'
FORM_TABLE_COLOR = 'light steel blue'
GRID_COLOR = '"light steel blue"'

TAB_ORDER_SKIP = ['Label','Frame']




FM  = chr(254)  # hx fe field marker (also refered to as attribute marker)
VM  = chr(253)  # hx fd value marker     y
SVM = chr(252)  # hx fc sub value marker u
TYPE_IDX_SEP = '^'

# define ACCUTERM form def layout
FMCMD = 0
FMID = 1
FMPARENT = 2
FMTYPE = 3
FMLEFT = 4
FMTOP = 5
FMWIDTH = 6
FMHEIGHT = 7 
FMEVENTMASK = 8

# define form table columns / list indexes (formvalues)
TCMD = 0
TID =  1
TPARENT = 2
TTYPE = 3
TIDX  = 4
TLEFT = 5
TTOP = 6
TWIDTH = 7
THEIGHT = 8 
TEVENTMASK = 9
TTAB = 10

# define property table columns / list indexes
PCMD = 0
PID = 1
PPROP = 2
PCOL= 3
PROW= 4
PVALUE = 5

# from ATGUIEQUATES
# commands
GCCREATE = '2'
GCSETPROP = '4'

# at widget types
wdgt_FORMSIZABLE = '5'
wdgt_FORMFIXED = '6'
wdgt_DIALOG = '7'
wdgt_SDISIZABLE = '8'
wdgt_SDIFIXED = '9'
wdgt_LABEL = '15'
wdgt_EDIT = '16'      # Input
wdgt_EDITMULTILINE = '17'
wdgt_COMMAND = '18'   # Button
wdgt_OPTION = '19'
wdgt_CHECK = '20'
wdgt_LIST = '21'
wdgt_LISTMULTISEL = '22'
wdgt_DRPDWNCBO = '23'
wdgt_DRPDWNLST = '24'
wdgt_PICTURE = '25'
wdgt_FRAME = '26'
wdgt_GRID = '27'
wdgt_GRIDEDITABLE = '28'
wdgt_EDITPASSWORD = '29'
wdgt_TABGRP = '30'
wdgt_TAB = '31'
wdgt_GAUGE = '32'
wdgt_GUAGE = '32'
wdgt_TREE = '33'
wdgt_CHECKEDLIST = '34'
wdgt_TIMER = '35'
wdgt_BROWSER = '36'
wdgt_MENU = '75'
wdgt_POPUP = '76'
wdgt_TOOLBAR = '77'
wdgt_STATUSBAR = '78'

# Grid ColTypes
grd_LABEL = '0'
grd_TEXTBOX = '1'
grd_CHECKBOX = '2'
grd_DROPDOWN = '3'
grd_COMBO = '4'
grd_BUTTON = '7'

grd_cell_types = ["cbsNone","cbsAuto","cbsCheckboxColumn","cbsPickList","cbsNone","cbsNone","cbsNone","cbsButtonColumn"]

# at widget properties
prop_DEFVAL = '0'
prop_VALUE = '1'
prop_LEFT = '2'
prop_TOP = '3'
prop_WIDTH = '4'
prop_HEIGHT = '5'
prop_CHANGED = '6' # form only
prop_SCALE = '7' # App only
prop_ENABLED = '8'
prop_VISIBLE = '9'
prop_STYLE = '10'
prop_BORDER = '11'
prop_READONLY = '12'
prop_TABSTOP = '13'
prop_BACKCOLOR = '14'
prop_FORECOLOR = '15'
prop_FONTNAME = '16'
prop_FONTSIZE = '17'
prop_FONTBOLD = '18'
prop_FONTITALIC = '19'
prop_HELPFILE = '20' # App only
prop_HELPID = '21'
prop_CAPTION = '22' # may be same as value
prop_PICTURE = '23' # picture or form
prop_RTNEQTAB = '24' # App only
prop_ALIGN = '25'
prop_ITEMS = '26'
prop_COLUMNS = '27'
prop_ROWS = '28'
prop_DATATYPE = '29'
prop_COLUMN = '30'
prop_ROW = '31'
prop_COLHEADING = '32'
prop_GRIDLINES = '33'
prop_COLFIELDTYPE = '34'
prop_COLDATATYPE = '35'
prop_COLITEMS = '36'
prop_COLWIDTH = '37'
prop_COLALIGN = '38'
prop_DATACOL = '39'
prop_ARRANGE = '40'
prop_DESCRIPTION = '41'
prop_AUTHOR = '42'
prop_COPYRIGHT = '43'
prop_VERSION = '44'
prop_LOGO = '45'
prop_AUTOSEL = '46' # App only
prop_STATUS = '47' # App only / read only
prop_WINDOWSTATE = '48'
prop_HINT = '49'
prop_EXTENSION = '50'
prop_MAXLEN = '51'
prop_MAXLINES = '52'
prop_MAXDROP = '53'
prop_REQUIRED = '54'
prop_FIXEDCOLS = '55'
prop_ICON = '56'
prop_SELSTART = '57'
prop_SELLENGTH = '58'
prop_HELPTYPE = '59'
prop_TIMEOUT = '60'
prop_MSGTEXT = '61'
prop_STATE = '62'
prop_COLSIZABLE = '63'
prop_COLHINT = '64'
prop_ALTCOLOR = '65'
prop_NOAUTOTIPS = '66'
prop_TRANSPARENT = '67'
prop_FONTUNDERLINE = '68'
prop_ICONALIGN = '69'
prop_ICONSIZE = '70'
prop_WORDWRAP = '71'
prop_CONTENT = '72'
prop_DRAGID = '73'
prop_DROPIDS = '74'
prop_DRAGMODE = '75'
prop_SELRANGE = '76'
prop_COLTABSTOP = '77'
prop_FOCUSSTYLE = '78'
prop_PASTEMODE = '79'
prop_WINDOWHANDLE = '98'
prop_EVENTMASK = '99'
prop_CUSTOM = '100'


form_col_count = 12
form_row_count = 30

# init window width and height, we actually set these values in get_form
window_width = 950
window_height = 600

# AT forms file we select to process
file_to_open = None

# have we loaded the form?
form_loaded = False
# have we processed the form?
form_processed = False

# formvalues will be a list of lists containing each widgets GCCREATE dataln from the form definition file
formvalues = [[FORMVALUE_EMPTYCELL for col in range(form_col_count)] for count in range(form_row_count)]

# propvalues will be a dictionary of lists of properties for each widget
# key = widget/control name
# values = list of widgets property items
propvalues = {}

# create a dictionary of containers and list of controls contained in the container (just row # in formvalues)
# populated in process_form
# used by output_control
containers = {'mainform':[]}

#
# mainmenu = we need the object name of main menu on form object creation
mainmenu = ''
app_name = ''
indent_cnt = 0
INDENT_AMOUNT = 2

form_heading = ["Cmd","Id","Parent Id","Cntl Type","Cntl idx","Left","Top","Width","Height","EventMask","TabIdx"]
prop_heading = ["Cmd","Id","Property","ColPos","RowPos","Value"]

# widget cross reference  dictionary
#key = acuterm widget id
# value list of ["acuterm widget",
#                "Free Pascal Component",
#                 container t/f,
wid_xref_dict = {
wdgt_FORMSIZABLE:  ['FormSizable', 'TForm',True,True],
wdgt_FORMFIXED  :  ['FormFixed', 'TForm',True,True],
wdgt_DIALOG     :  ['Dialog', 'TForm',True,True],
wdgt_SDISIZABLE :  ['DialogSzbl', 'TForm',True,True],
wdgt_SDIFIXED   :  ['DialogFixed', 'TForm',True,True],
wdgt_LABEL      :  ['Label', 'TLabel',False,True],
wdgt_EDIT       :  ['Edit', 'TEdit',False,True], 
wdgt_EDITMULTILINE :  ['EditMulti', 'TMemo',False,False],
wdgt_COMMAND    :  ['Cmd Button', 'TButton',False,True],
wdgt_OPTION     :  ['Option', 'TRADIOBUTTON',False,True],
wdgt_CHECK      :  ['Checkbox', 'TCheckBox',False,True], 
wdgt_LIST       :  ['Listbox', 'TListBox'  ,False,False],
wdgt_LISTMULTISEL  :  ['Listbox(MutiSel)', 'ListBox',False,False], 
wdgt_DRPDWNCBO  :  ['DropDownCombo', 'TComboBox',False,True],
wdgt_DRPDWNLST  :  ['DropDownList', 'TListBox', False,False],     # List Box with drop-down list selected
wdgt_PICTURE    :  ['Picture', 'TImage',False,True],
wdgt_FRAME      :  ['Frame', 'TPanel',True,True],
wdgt_GRID       :  ['Grid', 'TStringGrid',False,False],
wdgt_GRIDEDITABLE  : ['GridEdit', 'TStringGrid',False,False],
wdgt_EDITPASSWORD  : ['EDITPWD' , 'UNKNOWN',False,True],
wdgt_TABGRP     : ['TabGrp' , 'TPageControl',True,True],
wdgt_TAB        : ['Tab'    , 'TTabSheet'     ,True,True],
wdgt_GUAGE      : ['GUAGE' , 'TProgressBar',False,False],
wdgt_TREE       : ['TREE' , 'UNKNOWN',False,True],
wdgt_CHECKEDLIST: ['CHECKEDLIST' , 'UNKNOWN',False,True],
wdgt_TIMER      : ['TIMER' , 'UNKNOWN',False,True],
wdgt_BROWSER    : ['BROWSER' , 'UNKNOWN',False,True],
wdgt_MENU       : ['MENU' , 'TMenu',False,False],   
wdgt_POPUP      : ['POPUP' , 'Popup',False,True],
wdgt_TOOLBAR    : ['TOOLBAR' , 'UNKNOWN',False,True],
wdgt_STATUSBAR  : ['StatusBar' , 'TProgressBar',False,False]
}

# widget property dictionary
# key = property id
# value list of [atpropert name, free pascal component  property name or 'n/a' if not applicable]
# design change - only used as at property idx to property text for display purpose
# the conversion is defined in the widget cross ref table for each widget type
UNKNOWN  = 'UNKNOWN'    # unknown / no match to property in pysimple gui                      
wid_props = {
prop_DEFVAL: ['prop_DEFVAL',UNKNOWN],
prop_VALUE: ['prop_VALUE',UNKNOWN],
prop_LEFT: ['LEFT',UNKNOWN],
prop_TOP : ['TOP',UNKNOWN], 
prop_WIDTH: ['WIDTH',UNKNOWN],
prop_HEIGHT: ['HEIGHT',UNKNOWN],   
prop_CHANGED: ['prop_CHANGED',UNKNOWN],
prop_SCALE: ['prop_SCALE',UNKNOWN],
prop_ENABLED : ['ENABLED',UNKNOWN], 
prop_VISIBLE : ['prop_VISIBLE',UNKNOWN], 
prop_STYLE : ['prop_STYLE',UNKNOWN], 
prop_BORDER  : ['prop_BORDER',UNKNOWN],  
prop_READONLY: ['prop_READONLY',UNKNOWN],
prop_TABSTOP : ['prop_TABSTOP',UNKNOWN], 
prop_BACKCOLOR : ['prop_BACKCOLOR',UNKNOWN], 
prop_FORECOLOR : ['prop_FORECOLOR',UNKNOWN], 
prop_FONTNAME: ['prop_FONTNAME',UNKNOWN],
prop_FONTSIZE: ['prop_FONTSIZE',UNKNOWN],
prop_FONTBOLD: ['prop_FONTBOLD',UNKNOWN],
prop_FONTITALIC: ['prop_FONTITALIC',UNKNOWN],
prop_HELPFILE: ['prop_HELPFILE',UNKNOWN],
prop_HELPID  : ['prop_HELPID',UNKNOWN],  
prop_CAPTION: ['prop_CAPTION',UNKNOWN],
prop_PICTURE : ['prop_PICTURE',UNKNOWN], 
prop_RTNEQTAB: ['prop_RTNEQTAB',UNKNOWN],
prop_ALIGN: ['prop_ALIGN',UNKNOWN],
prop_ITEMS: ['prop_ITEMS',UNKNOWN],
prop_COLUMNS : ['prop_COLUMNS',UNKNOWN], 
prop_ROWS: ['prop_ROWS',UNKNOWN],
prop_DATATYPE: ['prop_DATATYPE',UNKNOWN],
prop_COLUMN  : ['prop_COLUMN',UNKNOWN],  
prop_ROW : ['prop_ROW',UNKNOWN], 
prop_COLHEADING: ['prop_COLHEADING',UNKNOWN],
prop_GRIDLINES : ['prop_GRIDLINES',UNKNOWN], 
prop_COLFIELDTYPE: ['prop_COLFIELDTYPE',UNKNOWN],
prop_COLDATATYPE : ['prop_COLDATATYPE',UNKNOWN],
prop_COLITEMS: ['prop_COLITEMS',UNKNOWN],
prop_COLWIDTH: ['prop_COLWIDTH',UNKNOWN],
prop_COLALIGN: ['prop_COLALIGN',UNKNOWN],
prop_DATACOL : ['prop_DATACOL',UNKNOWN], 
prop_ARRANGE : ['prop_ARRANGE',UNKNOWN], 
prop_DESCRIPTION: ['prop_DESCRIPTION',UNKNOWN],
prop_AUTHOR  : ['prop_AUTHOR',UNKNOWN],  
prop_COPYRIGHT : ['prop_COPYRIGHT',UNKNOWN], 
prop_VERSION : ['prop_VERSION',UNKNOWN], 
prop_LOGO: ['prop_LOGO',UNKNOWN],
prop_AUTOSEL : ['prop_AUTOSEL',UNKNOWN], 
prop_STATUS  : ['prop_STATUS',UNKNOWN],  
prop_WINDOWSTATE: ['prop_WINDOWSTATE',UNKNOWN],
prop_HINT: ['prop_HINT',UNKNOWN],
prop_EXTENSION : ['prop_EXTENSION',UNKNOWN], 
prop_MAXLEN  : ['prop_MAXLEN',UNKNOWN],  
prop_MAXLINES: ['prop_MAXLINES',UNKNOWN],
prop_MAXDROP : ['prop_MAXDROP',UNKNOWN], 
prop_REQUIRED: ['prop_REQUIRED',UNKNOWN],
prop_FIXEDCOLS : ['prop_FIXEDCOLS',UNKNOWN], 
prop_ICON: ['prop_ICON',UNKNOWN],
prop_SELSTART: ['prop_SELSTART',UNKNOWN],
prop_SELLENGTH : ['prop_SELLENGTH',UNKNOWN], 
prop_HELPTYPE: ['prop_HELPTYPE',UNKNOWN],
prop_TIMEOUT : ['prop_TIMEOUT',UNKNOWN], 
prop_MSGTEXT : ['prop_MSGTEXT',UNKNOWN], 
prop_STATE: ['prop_STATE',UNKNOWN],
prop_COLSIZABLE: ['prop_COLSIZABLE',UNKNOWN],
prop_COLHINT : ['prop_COLHINT',UNKNOWN], 
prop_ALTCOLOR: ['prop_ALTCOLOR',UNKNOWN],
prop_NOAUTOTIPS: ['prop_NOAUTOTIPS',UNKNOWN],
prop_TRANSPARENT: ['prop_TRANSPARENT',UNKNOWN],
prop_FONTUNDERLINE : ['prop_FONTUNDERLINE',UNKNOWN],
prop_ICONALIGN: ['prop_ICONALIGN',UNKNOWN],
prop_ICONSIZE: ['prop_ICONSIZE',UNKNOWN],
prop_WORDWRAP: ['prop_WORDWRAP',UNKNOWN],
prop_CONTENT: ['prop_CONTENT',UNKNOWN],
prop_DRAGID: ['prop_DRAGID',UNKNOWN],
prop_DROPIDS: ['prop_DROPIDS',UNKNOWN],
prop_DRAGMODE: ['prop_DRAGMODE',UNKNOWN],
prop_SELRANGE: ['prop_SELRANGE',UNKNOWN],
prop_COLTABSTOP: ['prop_COLTABSTOP',UNKNOWN],
prop_FOCUSSTYLE: ['prop_FOCUSSTYLE',UNKNOWN],
prop_PASTEMODE: ['prop_PASTEMODE',UNKNOWN],
prop_WINDOWHANDLE: ['prop_WINDOWHANDLE',UNKNOWN],
prop_EVENTMASK: ['prop_EVENTMASK',UNKNOWN],
prop_CUSTOM: ['prop_CUSTOM',UNKNOWN],
}

def scale(px):
    """return string representation of scaled pixel value px"""
    mypix = '0'
    try:
        mypix = float(px)
        mypix = str(round(mypix*PSCALE))
    except:
        try:
            mypix = int(px)
            mypix = str(round(mypix*PSCALE))
        except:
             sg.popup('Warning string invalid pixel representation, cannot scale' + px)

    return mypix

def get_indent():
    str = " "*(indent_cnt * INDENT_AMOUNT)
    return str

def cd_indent():
    str = " "*(INDENT_AMOUNT)
    return str

def get_FP_cmpnt(cv):
    if cv[TIDX] in wid_xref_dict:
        return wid_xref_dict[cv[TIDX]][1]
    else:
        return "unknown"
    
################## functions to output Free Pascal stuff  ######################################################    

def wrt_cmpnt_hdr(cv):
    """ output form text form component object header and code type def"""
    insert_form_text(get_indent() + 'object '+cv[TID]+': ' + get_FP_cmpnt(cv))
    insert_code_text(cd_indent() + cd_indent() + cv[TID]+': ' + get_FP_cmpnt(cv) +';')
    #window['-FORM_TEXT-'].Update(get_indent() + 'object '+cv[TID]+': ' + get_FP_cmpnt(cv))              # force to top of multiline
    #window['-CODE_TEXT-'].Update(cd_indent() + cd_indent() + cv[TID]+': ' + get_FP_cmpnt(cv) +';')


def wrt_menu(cv):
    def m_indent(lv):
        """get indent for menu level lv"""
        return get_indent() + (lv)*( " "*INDENT_AMOUNT)
    
    def nxt_mnu_level(idx,menus):
        """get next menu item level, return 0 if at the end"""
        if idx+1 < len(menus):
            nxt_level = int(menus[idx+1][1])
        else:
            nxt_level = 0
        return nxt_level

    insert_form_text(get_indent() + "object MainMenu: TMainMenu")        # note Menu is a reserved word, so we are just overwriting the AT Menu control "MainMenu"
    insert_code_text(cd_indent() + cd_indent() + "MainMenu: TMainMenu;")
    
    widget_id = cv[TID]
    if widget_id in propvalues:
        prop_list = propvalues[widget_id]  # get the menu list
        menus = get_prop('prop_ITEMS',prop_list)
        indent = get_indent() + " "*INDENT_AMOUNT
        insert_form_text(indent + 'Left = 192') # this needs to be figured out!
        insert_form_text(indent + 'Top = 144')
        
        last_mnu_level = 999
        for m_idx in range(len(menus)):
            menu_item = menus[m_idx]
            # rem menu_item is a list of the full menu def 
            # ie:
            #['Maint', '1', 'Item ', '', '0', '1', '', '0', '']
            #['CanShip', '2', 'Cancel Last Shipment', '', '0', '1', '', '1', '']
            #
            mnu_level = int(menu_item[1]) 
            nxt_level =nxt_mnu_level(m_idx,menus) 

            indent = m_indent(mnu_level)
            nxt_indent = indent + " "*INDENT_AMOUNT

            mnu_name = str(menu_item[0]).replace('*','')  # get rid of the special key designation
            insert_form_text(indent + "object mnu"+ mnu_name + ": TMenuItem")
            insert_form_text(nxt_indent + "Caption = '"+str(menu_item[2]) + "'")

            if (nxt_level == 0):   # done with menu items, need the end
                insert_form_text(m_indent(mnu_level) + "end")   # add for first skipped menuitem

            elif (mnu_level < nxt_level):    # will we go up a level at the next menu?
                pass                         # yes, skip end

            else:                            #  this menu  at same level or lower then next?
                insert_form_text(indent + "end")   # yes, add the end 

            if (mnu_level > nxt_level) and (nxt_level != 0):    # we drop down a lever, add end unless last menu item
                insert_form_text(m_indent(nxt_level) + "end")   

            # code for menu item
            insert_code_text(cd_indent() + cd_indent() + "mnu"+ mnu_name + ": TMenuItem;")
            last_mnu_level = mnu_level

       # insert_form_text(m_indent(mnu_level) + "end")   # add for first skipped menuitem

def wrt_label(cv):
    """write form object for label"""
    wrt_cmpnt(cv)
        # add in caption (if found)
    widget_id = cv[TID]
    if widget_id in propvalues:
        prop_list = propvalues[widget_id]
        caption = get_prop('prop_DEFVAL',prop_list)  # for label controls, caption is prop_DEFVAL
        if caption != "":
            indent = get_indent() + " "*INDENT_AMOUNT
            insert_form_text(indent + "Caption  = '" + caption + "'")
        lblborder = get_prop('prop_BORDER',prop_list)  # do we have a border?
        if lblborder == "2":                           # yes, only thing we can do to highlite is change the color
            indent = get_indent() + " "*INDENT_AMOUNT
            insert_form_text(indent + "Color = " + DFLT_LABEL_BACK )

def wrt_panel(cv):
    """write form object for panel"""
    wrt_cmpnt(cv)
    indent = get_indent() + " "*INDENT_AMOUNT
    insert_form_text(indent + "BorderStyle = bsSingle") 

def wrt_listbox(cv):
    """write form object for ListBox"""
    wrt_cmpnt(cv)
    indent = get_indent() + " "*INDENT_AMOUNT
    insert_form_text(indent + DFLT_ITEM_HEIGHT) 

def wrt_combobox(cv):
    """write form object for ComboBox"""
    wrt_cmpnt(cv)
    indent = get_indent() + " "*INDENT_AMOUNT
    insert_form_text(indent + DFLT_ITEM_HEIGHT)                  

def wrt_stringGrid(cv):
    """write form object for TStringGrid"""
    wrt_cmpnt(cv)
    # get propertis for this widget
    widget_id = cv[TID]
    if widget_id in propvalues:
        prop_list = propvalues[widget_id]
        # col count?
        ccnt_val = get_prop('prop_COLUMNS',prop_list)  # column count
        headings_val = get_prop('prop_COLHEADING',prop_list)  # column headings
        cwdth_val = get_prop('prop_COLWIDTH',prop_list)  # column width
        ctype_val = get_prop('prop_COLFIELDTYPE',prop_list)  # column types
        citems_val = get_prop('prop_COLITEMS',prop_list)  # column items (for dropdown / combo)
        if ccnt_val != "":
            indent = get_indent() + " "*INDENT_AMOUNT
            indent2 = indent + " "*INDENT_AMOUNT
            indent3 = indent2 + " "*INDENT_AMOUNT
            insert_form_text(indent + "ColCount = " + ccnt_val )
            # now for each col add in the provided info
            col_cnt = int(ccnt_val)
            insert_form_text(indent + "Columns = <" )
            #
            # output col detail info
            for idx in range(col_cnt):
               insert_form_text(indent2 + "item" ) 
               caption = headings_val[idx]   
               insert_form_text(indent3 + "Title.Caption = '" + caption + "'" ) 
               wdth = scale(cwdth_val[idx])
               insert_form_text(indent3 + "Width =" + wdth )
               col_type = int(ctype_val[idx])
               if col_type in range(len(grd_cell_types)):
                 insert_form_text(indent3 + "ButtonStyle = " + grd_cell_types[col_type]) 
               if (idx + 1) < col_cnt: 
                 insert_form_text(indent2 + "end" )
               else:
                insert_form_text(indent2 + "end>" )   
            #  
            # add in some needed object properties in a vary inefficient way 
            #
            p_str = "DefaultColWidth = 125"
            insert_form_text(indent + p_str )
            #
            p_str = "DefaultRowHeight = 20"
            insert_form_text(indent + p_str )
            #
            p_str = "FixedCols = 0"
            insert_form_text(indent + p_str )
            # 
            p_str = "Options = [goFixedVertLine, goFixedHorzLine, goVertLine, goHorzLine, goRangeSelect, goColSizing, goEditing, goAutoAddRows, goSmoothScroll]"
            insert_form_text(indent + p_str)



def wrt_cmpnt(cv):
    """output code and form text for generic component"""
    wrt_cmpnt_hdr(cv)      #insert_form_text(get_indent + 'object '+cv[TID]+': ' + get_FP_obj(cv))
    add_cntl_pos(cv)


def add_cntl_pos(cv):
    '''adds left height top width properties from formvalues for row_idx to form_editor '''
    indent = get_indent() + " "*INDENT_AMOUNT
    if cv[TLEFT] != 'auto':  # shameless hack to remove "auto" for formvalues for form definition line
        insert_form_text(indent + 'Left = ' + scale(cv[TLEFT])) 
        insert_form_text(indent + 'Top = ' + scale(cv[TTOP]))
    else:
        insert_form_text(indent + 'Left = 350') 
        insert_form_text(indent + 'Top = 350')

    insert_form_text(indent + 'Height = ' + scale(cv[THEIGHT]))
    insert_form_text(indent + 'Width = ' + scale(cv[TWIDTH]))
    if wid_xref_dict[cv[TIDX]][3] == True: # if control has AutoSizing property
        # turn off autosizing
        insert_form_text(indent + 'AutoSize = False')
    # add in caption (if found)
    widget_id = cv[TID]
    if widget_id in propvalues:
        prop_list = propvalues[widget_id]
        caption = get_prop('prop_CAPTION',prop_list)
        if caption != "":
            insert_form_text(indent + "Caption  = '" + caption + "'")
        
    if TTAB in cv:
        tab_ord = cv[TTAB]
        if tab_ord.isnumeric():
            insert_form_text(indent + 'TabOrder = ' + tab_ord) 


def form_object(cv):
    global indent_cnt
    indent_cnt = 0   # set beginning indent when we output the form object
    ft = """  ClientHeight = 500
  ClientWidth = 500
  Font.CharSet = ANSI_CHARSET
  Font.Height = -13
  Font.Name = 'Arial Narrow'
  Font.Pitch = fpVariable
  Font.Quality = fqDraft
  SessionProperties = 'Left;Top;Width;Height'
  LCLVersion = '2.2.6.0'
  Visible = True""" 
    sp_obj = """  object XMLPropStorage1: TXMLPropStorage
    StoredValues = <>
    FileName = 'session_props.xml'
    Left = 88
    Top = 144
  end"""
    form = cv[TID]
    insert_form_text('object frm'+form+': Tfrm'+form) 
    add_cntl_pos(cv)    # we assume the form control is the first line in formvalues
    insert_form_text('  AutoScroll = True')  # we want scroll bars
    insert_form_text(ft)   
    insert_form_text('  Menu = MainMenu')   # Note we hard code this, probably will be a problem!
    insert_form_text(sp_obj)  # add the session properties storage object
    indent_cnt = 1
   

def code_hrdr(form):
    ct = """
{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, ExtCtrls,
  Grids, Menus, XMLPropStorage, ComCtrls;

type

"""
    insert_code_text('unit Unit'+form+';')
    insert_code_text(ct)
    insert_code_text(cd_indent()+'{ Tfrm'+form+'  }')
    insert_code_text(' ')
    insert_code_text(cd_indent()+'Tfrm' +form+' = class(TForm)')
    insert_code_text(cd_indent()+cd_indent()+'XMLPropStorage1: TXMLPropStorage;')

def output_controls(container_list):
    """ main contol function for output of form / code for controls listed in contaier_list"""
    global indent_cnt

    if dbg_output_controls:
        print('at output_controls, container list is:')
        print(container_list)
    for row_idx in container_list:
      control = formvalues[row_idx]               # get the controls values list
      if wid_xref_dict[control[TIDX]][2] != True: # if not another container control
            if call_control_output(control,row_idx):                     # output the syntax for the control
                if dbg_output_controls:
                    insert_form_text(get_indent()+'end'  + str(row_idx))  # end of control, add "end"
                else:
                    insert_form_text(get_indent()+'end')  # end of control, add "end"
      else:
          if call_control_output(control,row_idx):                     # output the syntax for the control
            next_container = control[TID]   # is itself a container control, so output its contained controls here
            next_container_list = containers[next_container] 
            output_controls(next_container_list)
            indent_cnt -= 1 
            if dbg_output_controls:
                insert_form_text(get_indent()+'end'  + str(row_idx))  # end of control, add "end"
            else:
                insert_form_text(get_indent()+'end')  # end of control, add "end"
          

def call_control_output(control_values,ridx):
    """call function to output control defined in control_values"""
    global indent_cnt, last_control_a_con
    control_type = control_values[TTYPE]
    found = True
    if dbg_output_controls:
        print ('call_control: ' + control_type)

    if  control_type == "Checkbox":
        wrt_cmpnt(control_values)
    elif control_type == "Cmd Button":
        wrt_cmpnt(control_values)
    elif control_type == "DropDownList":  
        wrt_listbox(control_values)    
    elif control_type == "Edit":
        wrt_cmpnt(control_values)
    elif control_type == "Frame":
        wrt_panel(control_values)    
    elif control_type == "Label":
        wrt_label(control_values)
    elif control_type == "Listbox":
        wrt_cmpnt(control_values) 
    elif control_type == "DropDownList":   # listbox with dropdown checked
        wrt_listbox(control_values)     
    elif control_type == "DropDownCombo":
        wrt_combobox(control_values)        
    elif control_type == "EditMulti":
        wrt_cmpnt(control_values)       
    elif control_type == "MENU":
        wrt_menu(control_values)    
    elif control_type == "Tab":
        wrt_cmpnt(control_values) 
    elif control_type == "TabGrp":
       wrt_cmpnt(control_values) 
    elif (control_type == "Grid") or (control_type == "GridEdit"):
       wrt_stringGrid(control_values)    
    else:
        #insert_form_text('Uncoded control type: ' + control_type) 
        sg.popup('Waring Uncoded control type: ' + control_type + ' at row: '+ str(ridx))
        found = False

    if wid_xref_dict[control_values[TIDX]][2] == True: # if we just started a new container control
        indent_cnt += 1                                # add to indent spacing
    return found

######################################## functions to parse AT definition file and create strutures for conversion ######################################

def get_widget_id(widget):
    '''returns widget id from widget string (ie counts "*" and returns last value)'''
    ids = widget.split('*')
    match len(ids):
        case 0:
            sg.popup('error, did not find an id in ' + widget)
            id = ''
        case default:
            id = ids[len(ids)-1]
    if '.' in id:
        sg.popup('Waring "." found in widget name: ' + id +', this may cause issues!')
    return id

def get_widget_type(row):
    ''' return the widget type index value at formvalues row'''
    return formvalues[row][TTYPE].split('^')[1]
 

def decode_widget(dataln):
    '''routine 1) decodes widget type number to text, 2) filters widget id string (fld*fld*Fld, to fld), returns AT definition text as list'''
    global mainmenu

    decodeln = dataln.strip().split(VM)  # rem we start with the full AT definition text line and convert to a list
    
    AT_CNTL_IDX = decodeln[TTYPE]
    decodeln.insert(TIDX,AT_CNTL_IDX)  # insert a list item for AT control id number
    if AT_CNTL_IDX in wid_xref_dict:   # performs cross reference from AT style widge / control to FP control
        decodeln[TTYPE] = wid_xref_dict[AT_CNTL_IDX][0]
        if decodeln[TTYPE] == 'MENU':
            mainmenu = get_widget_id(decodeln[TID]) 
    else:
        decodeln[TTYPE] = 'unknown'
    # look for widget id 
    decodeln[FMID] = get_widget_id(decodeln[FMID])
    
    return decodeln

def decode_property(dataln,widget_type):
    '''routine decodes property type to text '''
    decodeln = dataln.strip().split(VM)
    property_key = decodeln[PPROP]
    # if this is a grid, values are multivalue
    if widget_type in [wdgt_GRID,wdgt_GRIDEDITABLE]:
        #
        newcodeln = list(decodeln[:PVALUE])
        if property_key in [prop_COLHEADING,prop_COLFIELDTYPE,prop_COLWIDTH,prop_COLALIGN,prop_COLITEMS]:
            # for grids, there will be 1 item for each column of the grid
            property_value = []
            for idx in range(PVALUE, len(decodeln)):
                property_value.append(decodeln[idx])
            # remove items we have not combined into one list element (as a list)
            newcodeln.append(property_value)
            decodeln = newcodeln
        elif property_key == prop_DEFVAL:
            # for grids, the default values have 1 item for each row of grid (as created), separated by SVM
                        # for grids, there will be 1 item for each column of the grid
            property_value = []
            for idx in range(PVALUE, len(decodeln)):
                property_value.append(decodeln[idx].split(SVM))
            # remove items we have not combined into one list element (as a list)
            newcodeln.append(property_value)
            decodeln = newcodeln
    elif widget_type == wdgt_MENU:
        # special processing for menu properties
        if property_key == prop_ITEMS:
            # for menu widgets, property items is a subvalued list for each menu item (see ATGUICREATEMENU in manual)
            property_value = []
            newcodeln = list(decodeln[:PVALUE])
            for idx in range(PVALUE, len(decodeln)):
                menu_values = decodeln[idx].split(SVM)
                #property_value.append(menu_values[2]) # for now just grab the menu name, figure more out later
                property_value.append(menu_values) # for now just grab all the menu def, figure more out later
            newcodeln.append(property_value)
            decodeln = newcodeln
    if property_key in wid_props:
        decodeln[PPROP] = wid_props[property_key][0] +TYPE_IDX_SEP + property_key
    else:
        decodeln[PPROP] = 'unknown' + TYPE_IDX_SEP + property_key
    return decodeln    

def get_form():
    '''reads file_to_open and returns values (which is a list of lists of widgets) 
        and props ()'''
    global form_loaded, app_name, window_width, window_height
    values = []
    props = {}
    start_of_form_def_found = False
    start_of_app_def_found = False
    app_name = ''
    last_widget = ''
    last_widget_type = ''
    tabidx =0    # used to keep track of tab order

    if file_to_open == None:
        return
    with open(file_to_open) as f:
        for line in f:
            data_ln = line.strip().split(VM)
            cmd = data_ln[FMCMD]
            if start_of_form_def_found:
                # processed all form definitions?
                if cmd == '0':
                    break    
                if cmd == GCCREATE:
                    # command is to create an AT widget (control) add to our list of widgets
                    decodelist = decode_widget(line)
                    control = decodelist[TTYPE]
                    if control in TAB_ORDER_SKIP:
                        decodelist.append("")
                    else:
                        tabidx +=1
                        decodelist.append(str(tabidx))
                    values.append(decodelist)
                    # create an empty dictionary entry of properties from this widget
                    last_widget = get_widget_id(data_ln[FMID]) 
                    last_widget_type = data_ln[FMTYPE]
                    cmd_prop = {last_widget :[]}
                    props.update(cmd_prop)
                else:
                    # was not create command, assume its a property for the previously created widget 
                    # add property to list of properties for this widget
                    cmd_props = props[last_widget]
                    # decode property type and append
                    cmd_props.append(decode_property(line,last_widget_type))
                    up_props = {last_widget : cmd_props}
                    props.update(up_props)

            elif cmd == 'TEMPLATE':
                app_name =data_ln[2]
                app_name = app_name.replace(" ", "_")
                app_name = app_name.upper()

            elif cmd == GCCREATE: 
            # what we should be doing here is skipping over the app definition data in the form definition file
            # (we are assuming the actual form definition starts at the second create, this maybe an error 
            #  other option would be to look at the count of "*" or fields in the ID 0 = App create, 1 = form create, 2 = widget create)
                if start_of_app_def_found:
                    start_of_form_def_found  = True
                    values.append(decode_widget(line))
                    # save the form's window size
                    window_width = int(float(values[0][TWIDTH]))
                    window_height = int(float(values[0][THEIGHT]))
                    # create dictionary entry of properties from this widget
                    last_widget = get_widget_id(data_ln[FMID]) 
                    last_widget_type = data_ln[FMTYPE]
                    cmd_prop = {last_widget :[]}
                    props.update(cmd_prop)
                else:
                    start_of_app_def_found = True


        f.close()
        form_loaded = True
    return values, props

def  get_prop_list(row):
    '''returns widget selected and a property list of lists for widget selected from form table at row row'''
    prop_list = []
    widget_id = formvalues[row][TID]
    if widget_id in propvalues:
        prop_list = propvalues[widget_id]
    else:
        sg.popup(widget_id + ' not found', keep_on_top=True)
    return widget_id, prop_list

def get_prop(prop,prop_list):
    '''return the propert value for property prop'''
    rvalue = ""
    for list in prop_list:
        if list[PPROP].split(TYPE_IDX_SEP)[0] == prop:
            rvalue = list[PVALUE]
            break
    return rvalue


def process_form():
    '''routine creates the Free Pascal files for the AT form'''
    global containers
    #
    # Notes The AT definition file can have controls defined before the contianer control, therefore we need to come up with a 
    # process that ensures containers and their contained controls are output in the proper order.
    #
    starting_formvalues_row = 0

    for row_idx  in range(1, len(formvalues)):  # parse thru the form values list
       cparent = formvalues[row_idx][TPARENT]   # this controls parent container
       if cparent  == "":                        
         containers['mainform'].append(row_idx)  # no parent container, add control to mainform
       else:
         if cparent in containers:               # have we already added this container??
           containers[cparent].append(row_idx)   # yes, add this control to its list on controls
         else: 
#                                                 # not yet in dictionary,  
           containers.update({cparent : []})      # create new dictionary entry for this container
           containers[cparent].append(row_idx)    # we actually catch this on the first control in the newly added container, must add the control

# we now have a dictionary of containers,
# now how do we make sure we output them in the correct order?????
    if dbg_process_form:
        print('at process_form, completed containers population')
        print(containers)
    mainform_list = containers['mainform'] 
    # 
    # start out the form and code generation
    form_object(formvalues[0])
    code_hrdr(app_name)
    # 
    # now parse thru the main container list and genetate the balance
    output_controls(mainform_list) 
    #
    #  form and pas file generated close up
    #
    ct = """  private

  public

  end;

var"""
 
    insert_code_text(ct) 
    insert_code_text(cd_indent() + 'frm' +app_name +': Tfrm' + app_name + ';')


    ct = """
implementation

{$R *.lfm}"""
    insert_code_text(ct)
    insert_form_text('')
    insert_code_text('end.')
    # 
    #  
    insert_form_text('end') 
     
              

#
# functions that insert text into our editors
def insert_form_text(text):
    '''append text to editor'''
    tkwidget = window['-FORM_TEXT-']
    tkwidget.Widget.insert('end', text+'\n')

def insert_code_text(text):
    '''append code text to editor'''
    tkwidget = window['-CODE_TEXT-']
    tkwidget.Widget.insert('end', text+'\n') 

def save_code(pu):
    if form_processed == True:
        filepathobj = pathlib.PurePath(file_to_open)
        filepath = filepathobj.parent
        #oldfilename = filepathobj.name
        #newfilename = 'unit' + oldfilename.replace('.','_') + '.pas'
        newfilename = 'unit' + app_name + '.pas'
        file = pathlib.Path(filepath,newfilename)
    #file.write_text(values.get('-CODE_TEXT-'),encoding="utf-8") 
        file.write_text(window['-CODE_TEXT-'].get(),encoding="utf-8")
        if pu:
            sg.popup('Saved', str(file))   

def save_form(pu):
    if form_processed == True:
        filepathobj = pathlib.PurePath(file_to_open)
        filepath = filepathobj.parent
        #oldfilename = filepathobj.name
        #newfilename = 'unit' + oldfilename.replace('.','_') + '.lfm'
        newfilename = 'unit' + app_name + '.lfm'
        file = pathlib.Path(filepath,newfilename)
    #file.write_text(values.get('-FORM_TEXT-'),encoding="utf-8")
        file.write_text(window['-FORM_TEXT-'].get(),encoding="utf-8")
        if pu:
            sg.popup('Saved', str(file))

def wrt_lpi():
    my_lpi = LPI_TEMPLATE
    my_lpi = my_lpi.replace("%TITLE%",app_name)
    my_lpi = my_lpi.replace("%LPR_FILENAME%",app_name + '.lpr' )
    my_lpi = my_lpi.replace("%UNIT_FILENAME%",'unit'+app_name + '.pas' )
    my_lpi = my_lpi.replace("%UNIT_NAME%",'unit'+app_name)
    my_lpi = my_lpi.replace("%COMPONET_NAME%",'frm'+app_name)
    my_lpi = my_lpi.replace("%TARGET_FILENAME%",app_name)
    filepathobj = pathlib.PurePath(file_to_open)
    filepath = filepathobj.parent
    newfilename = app_name + '.lpi'
    file = pathlib.Path(filepath,newfilename)
    file.write_text(my_lpi,encoding="utf-8")


def wrt_lpr():
    my_lpr = """program %PROGRAM_NAME%;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}
  cthreads,
  {$ENDIF}
  {$IFDEF HASAMIGA}
  athreads,
  {$ENDIF}
  Interfaces, // this includes the LCL widgetset
  Forms, %UNIT_NAME%
  { you can add units after this };

{$R *.res}

begin
  RequireDerivedFormResource:=True;
  Application.Scaled:=True;
  Application.Initialize;
  Application.CreateForm(T%FORM_NAME%, %FORM_NAME%);
  Application.Run;
end."""
    my_lpr = my_lpr.replace("%PROGRAM_NAME%",app_name)
    my_lpr = my_lpr.replace("%UNIT_NAME%",'unit'+app_name)
    my_lpr = my_lpr.replace("%FORM_NAME%",'frm'+app_name)
    filepathobj = pathlib.PurePath(file_to_open)
    filepath = filepathobj.parent
    newfilename = app_name + '.lpr'
    file = pathlib.Path(filepath,newfilename)
    file.write_text(my_lpr,encoding="utf-8")


################################################################## start of processing code ############################################################################



props_tab =   [ 
     [sg.Table(propvalues, headings=prop_heading, max_col_width=25,pad = 0,
                        auto_size_columns=False,
                        font=('Consolas', 12),
                        col_widths = 25, 
                        # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                        display_row_numbers=True,
                        justification='center',
                        num_rows=5,
                        alternating_row_color= FORM_TABLE_COLOR,
                        key='-PROP_TABLE-',
    #                    selected_row_colors='red on yellow',
                        enable_events=True,
                        expand_x=True,
                        expand_y=True,
                        vertical_scroll_only=False,
                        hide_vertical_scroll = False,
                        enable_click_events=False           # Comment out to not enable header and other clicks
                        )]
]

form_editor_tab =  [
    [sg.Button("Save_Form")],
    [sg.Multiline(default_text='',font=('Consolas', 12), size=(875, 300), key='-FORM_TEXT-')]
    ]
code_editor_tab =  [
    [sg.Button("Save_Code")],
    [sg.Multiline(default_text='',font=('Consolas', 12), size=(875, 300), key='-CODE_TEXT-')]
    ]

layout = [
#    [sg.T("")], [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-FILENAME-")],
    [sg.Button("Open File"),sg.Button("Load"),sg.Text("", size=(0, 1), key='FILENAME'),sg.Button("Generate"),sg.Checkbox('Auto Save Generated Files', default=True,key='AUTO_SAVE'), sg.Text('PySimpleGUI version: '),sg.Text(sg.__version__)], 
    [sg.Table(formvalues, headings=form_heading, max_col_width=25,pad = 0,
                        auto_size_columns=True,
                        font=('Consolas', 12),
                        col_widths = 25, 
                        # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                        display_row_numbers=True,
                        justification='center',
                        num_rows=10,
                        alternating_row_color= FORM_TABLE_COLOR,
                        key='-FORM_TABLE-',
    #                    selected_row_colors='red on yellow',
                        enable_events=True,
                        expand_x=True,
                        expand_y=True,
                        vertical_scroll_only=False,
                        hide_vertical_scroll = False,
                        enable_click_events=True,           # Comment out to not enable header and other clicks
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE
                        )],

    [sg.Text("Widget Id: "),sg.Text("", size=(0, 1), key='WIDGET_ID')],
    [sg.TabGroup([[sg.Tab('Props',props_tab,key='-PROPS-'),sg.Tab('Form',form_editor_tab,key='-FORM_EDITOR-'),sg.Tab('Code',code_editor_tab,key='-CODE_EDITOR-')]])],
    ]

###Building Window
window = sg.Window('AT_Form_Parser', layout, size=(900,600), resizable=True,  finalize=True)
last_row_click = -1   
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":

        break
    # table event?
    elif isinstance(event, tuple):        
        if event[0] == '-FORM_TABLE-':
            if event[2][0] == None:    # column resize was attempted
                pass
            elif (event[2][0] == -1) or (event[2][1] == -1):
                    pass  # header or "row" column was clicked
            else:
                # row was clicked, get it
                last_row_click = event[2][0]
                # row on form table was clicked, display properties for associated form widget
                widget_id, prop_list = get_prop_list(last_row_click)
                window['WIDGET_ID'].update(value=widget_id)
                window['-PROP_TABLE-'].update(values=prop_list)
                if dbg =='yes':
                    for prop in prop_list:
                        print(prop)

    elif event == "Open File":
            file_to_open = sg.popup_get_file('Open',no_window=True, keep_on_top=True)
            if file_to_open != None:
                window['FILENAME'].update(value=file_to_open)

    elif event == "Save_Form" and file_to_open != None:
        save_form(True)
  

    elif event == "Save_Code" and file_to_open != None:
        save_code(True)

           
    elif event == "Load" and file_to_open != None:
        formvalues, propvalues  = get_form()
        window['-FORM_TABLE-'].update(values=formvalues)
  
    elif event == "Generate":
        if form_loaded:
            process_form()
            form_processed = True
            if values['AUTO_SAVE'] == True:  #  save 
                save_code(False)
                save_form(False)
                wrt_lpi()
                wrt_lpr()
                sg.popup('Auto Saved Generated Files (.pas, .lfm, .lpi, .lpr) to ' + str(pathlib.PurePath(file_to_open)))

