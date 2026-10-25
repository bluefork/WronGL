[Setup]
AppId={{8B7A3E4F-5C2D-4A1B-9E8F-7D6C5B4A3F2E}
AppName=WronGL
AppVersion=1.0
AppPublisher=WronGL Contributors
AppPublisherURL=https://github.com/bluefork/WronGL
AppSupportURL=https://github.com/bluefork/WronGL/issues
AppUpdatesURL=https://github.com/bluefork/WronGL/releases
DefaultDirName={autopf}\WronGL
DisableProgramGroupPage=yes
LicenseFile=LICENSE
OutputDir=installer_out
OutputBaseFilename=WronGL_Setup_v1.0
SetupIconFile=wrongl\resources\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\WronGL.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\WronGL"; Filename: "{app}\WronGL.exe"
Name: "{autodesktop}\WronGL"; Filename: "{app}\WronGL.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\WronGL.exe"; Description: "{cm:LaunchProgram,WronGL}"; Flags: nowait postinstall skipifsilent