; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "HUFSGrade1.2"
#define MyAppVersion "1.2"
#define MyAppPublisher "JMCOPORATION"
#define MyAppURL "the7mincheol@naver.com"
#define MyAppExeName "hufsgrade_ver1.2.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{5EA6F7F8-8D7D-4E4A-824C-689C39452534}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
InfoAfterFile=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\feedback.txt
OutputDir=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\innosetup
OutputBaseFilename=HUFSGrade1.2_setup
SetupIconFile=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\hufslogo.png.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\dist\hufsgrade_ver1.2.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
