#define MyAppName "Windows Dev Optimizer"
#define MyAppPublisher "AvilaOps"
#define MyAppURL "https://avila.inc"
#define MyAppVersion GetDateTimeString("yyyymmdd", "", "")
#define SourceDir "..\\build\\inno_dist\\WindowsDevOptimizer"
#define OutputDir "..\\exports\\installers"

[Setup]
AppId={{D9B3191C-89E6-45D9-BF1C-4A8C9C2E51F1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={localappdata}\\Avila\\WindowsDevOptimizer
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64
Compression=lzma
SolidCompression=yes
OutputDir={#OutputDir}
OutputBaseFilename={#MyAppName}_{#MyAppVersion}_Setup
WizardStyle=modern
ChangesEnvironment=yes
UninstallDisplayIcon={app}\\launch_windows_dev_optimizer.cmd
SetupLogging=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#SourceDir}\\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{autoprograms}\\{#MyAppName}"; Filename: "pwsh.exe"; Parameters: "-NoLogo -ExecutionPolicy Bypass -File \"{app}\\launch_windows_dev_optimizer.ps1\""; WorkingDir: "{app}"
Name: "{autoprograms}\\{#MyAppName}\\Instalar dependências"; Filename: "pwsh.exe"; Parameters: "-NoLogo -ExecutionPolicy Bypass -File \"{app}\\install_dependencies.ps1\""; WorkingDir: "{app}"
Name: "{autoprograms}\\{#MyAppName}\\Desinstalar"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "pwsh.exe"; Parameters: "-NoLogo -ExecutionPolicy Bypass -File \"{app}\\launch_windows_dev_optimizer.ps1\""; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "pwsh.exe"; Parameters: "-NoLogo -ExecutionPolicy Bypass -File \"{app}\\install_dependencies.ps1\""; WorkingDir: "{app}"; Description: "Executar instalação das dependências Python"; Flags: postinstall shellexec runasoriginaluser
Filename: "pwsh.exe"; Parameters: "-NoLogo -ExecutionPolicy Bypass -File \"{app}\\launch_windows_dev_optimizer.ps1\""; WorkingDir: "{app}"; Description: "Abrir Windows Dev Optimizer agora"; Flags: postinstall nowait shellexec skipifsilent runasoriginaluser

[UninstallDelete]
Type: filesandordirs; Name: "{app}\\.venv"
