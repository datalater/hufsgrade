; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{71B31D91-F5A1-4463-AB12-B556CCA41C53}
AppName=HUFSGrade1.3
AppVersion=1.3
;AppVerName=HUFSGrade1.3 1.3
AppPublisher=JMCORPORATION
AppPublisherURL=the7mincheol@naver.com
AppSupportURL=the7mincheol@naver.com
AppUpdatesURL=the7mincheol@naver.com
DefaultDirName={pf}\HUFSGrade1.3
DisableProgramGroupPage=yes
InfoAfterFile=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\feedback.txt
OutputDir=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\innosetup
OutputBaseFilename=HUFSGrade1.3_setup
SetupIconFile=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\hufslogo.png.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\dist\hufsgrade_ver1.3.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-20160909\PyQt4\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\HUFSGrade1.3"; Filename: "{app}\hufsgrade_ver1.3.exe"
Name: "{commondesktop}\HUFSGrade1.3"; Filename: "{app}\hufsgrade_ver1.3.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\hufsgrade_ver1.3.exe"; Description: "{cm:LaunchProgram,HUFSGrade1.3}"; Flags: nowait postinstall skipifsilent

