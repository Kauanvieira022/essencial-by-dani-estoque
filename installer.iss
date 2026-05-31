[Setup]
AppName=Controle de Estoque
AppVersion=1.0
DefaultDirName={pf}\ControleEstoque
DefaultGroupName=ControleEstoque
OutputDir=output
OutputBaseFilename=setup

[Files]
Source: "dist\main.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Controle de Estoque"; Filename: "{app}\main.exe"
Name: "{commondesktop}\Controle de Estoque"; Filename: "{app}\main.exe"