# LPT_TEMPLATE.py
# template for lpi file creation, used by AT_To_FP_FORM.py
#
# TEMPLATE.lpi  Substitution list example: for Customer Maintenance Program (CM)
# %TITLE%  = CM
# %LPR_FILENAME% = cm.lpr
# %UNIT_FILENAME% = unitCM.pas
# %COMPONET_NAME% = frmCM
# %UNIT_NAME% = UnitCM
# %TARGET_FILENAME% = CM
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

LPI_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<CONFIG>
  <ProjectOptions>
    <Version Value="12"/>
    <PathDelim Value="\"/>
    <General>
      <SessionStorage Value="InProjectDir"/>
      <Title Value="%TITLE%"/>
      <Scaled Value="True"/>
      <ResourceType Value="res"/>
      <UseXPManifest Value="True"/>
      <XPManifest>
        <DpiAware Value="True"/>
      </XPManifest>
    </General>
    <BuildModes>
      <Item Name="Default" Default="True"/>
    </BuildModes>
    <PublishOptions>
      <Version Value="2"/>
      <UseFileFilters Value="True"/>
    </PublishOptions>
    <RunParams>
      <FormatVersion Value="2"/>
    </RunParams>
    <RequiredPackages>
      <Item>
        <PackageName Value="LCL"/>
      </Item>
    </RequiredPackages>
    <Units>
      <Unit>
        <Filename Value="%LPR_FILENAME%"/>
        <IsPartOfProject Value="True"/>
      </Unit>
      <Unit>
        <Filename Value="%UNIT_FILENAME%"/>
        <IsPartOfProject Value="True"/>
        <ComponentName Value="%COMPONET_NAME%"/>
        <HasResources Value="True"/>
        <ResourceBaseClass Value="Form"/>
        <UnitName Value="%UNIT_NAME%"/>
      </Unit>
    </Units>
  </ProjectOptions>
  <CompilerOptions>
    <Version Value="11"/>
    <PathDelim Value="\"/>
    <Target>
      <Filename Value="%TARGET_FILENAME%"/>
    </Target>
    <SearchPaths>
      <IncludeFiles Value="$(ProjOutDir)"/>
      <UnitOutputDirectory Value="lib\$(TargetCPU)-$(TargetOS)"/>
    </SearchPaths>
    <Linking>
      <Options>
        <Win32>
          <GraphicApplication Value="True"/>
        </Win32>
      </Options>
    </Linking>
  </CompilerOptions>
  <Debugging>
    <Exceptions>
      <Item>
        <Name Value="EAbort"/>
      </Item>
      <Item>
        <Name Value="ECodetoolError"/>
      </Item>
      <Item>
        <Name Value="EFOpenError"/>
      </Item>
    </Exceptions>
  </Debugging>
</CONFIG>"""
