#define MyAppName "MP3Downloader"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Daniel Culpian"

[Setup]
AppId={{B43E32D8-5B76-4A5A-8F12-7C3B82A06D91}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\MP3Downloader
DefaultGroupName=MP3Downloader
PrivilegesRequired=lowest
OutputDir=.
OutputBaseFilename=MP3Downloader-Setup
SetupIconFile=bin\media\MP3Downloader.ico
UninstallDisplayIcon={app}\MP3Downloader.exe
WizardStyle=modern
Compression=lzma
SolidCompression=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Files]
Source: "dist\MP3Downloader\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MP3Downloader"; Filename: "{app}\MP3Downloader.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\MP3Downloader"; Filename: "{app}\MP3Downloader.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\MP3Downloader.exe"; Description: "Abrir MP3Downloader"; Flags: postinstall nowait skipifsilent