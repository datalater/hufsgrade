; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{2339E519-1954-4D08-8A07-9C3392F55A92}
AppName=HUFSGrade1.6
AppVersion=1.6
;AppVerName=HUFSGrade1.6 1.6
AppPublisher=JMCORPORATION
AppPublisherURL=the7mincheol@naver.com
AppSupportURL=the7mincheol@naver.com
AppUpdatesURL=the7mincheol@naver.com
DefaultDirName={pf}\HUFSGrade1.6
DisableProgramGroupPage=yes
InfoBeforeFile=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-160922@law\hufsgrade-master\PyQt4\HUFSGrade1.6_before_guide.txt
InfoAfterFile=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-160922@law\hufsgrade-master\PyQt4\HUFSGrade1.6_after_guide.txt
OutputDir=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-160922@law\hufsgrade-master\PyQt4\innosetup
OutputBaseFilename=HUFSGrade1.6_setup
SetupIconFile=C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-160922@law\hufsgrade-master\PyQt4\hufslogo.png.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-160922@law\hufsgrade-master\PyQt4\dist_ver1.6\hufsgrade_ver1.6.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\hufs\Downloads\download\lawjmc\hufsgrade-160922@law\hufsgrade-master\PyQt4\dist_ver1.6\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\HUFSGrade1.6"; Filename: "{app}\hufsgrade_ver1.6.exe"
Name: "{commondesktop}\HUFSGrade1.6"; Filename: "{app}\hufsgrade_ver1.6.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\hufsgrade_ver1.6.exe"; Description: "{cm:LaunchProgram,HUFSGrade1.6}"; Flags: nowait postinstall skipifsilent

