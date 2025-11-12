# coding: utf-8
"""
Script: settings.py
Função: Configurações centralizadas do Windows Dev Optimizer
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer
Descrição: Ferramenta para otimização completa do Windows para desenvolvedores
"""

import os
from pathlib import Path

# ===== INFORMAÇÕES DA APLICAÇÃO =====
APP_NAME = "Windows Dev Optimizer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Nicolas Avila"
APP_DESCRIPTION = "Ferramenta completa para otimização do Windows para desenvolvedores"

# ===== DIRETÓRIOS =====
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
CONFIG_DIR = BASE_DIR / "config"
MODULES_DIR = BASE_DIR / "modules"

# Criar diretórios se não existirem
for directory in [LOGS_DIR, REPORTS_DIR]:
    directory.mkdir(exist_ok=True)

# ===== CAMINHOS DO WINDOWS =====
WINDOWS_PATHS = {
    # Edge Browser
    'edge_data': Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'Edge' / 'User Data' / 'Default',
    'edge_history': Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'Edge' / 'User Data' / 'Default' / 'History',
    'edge_cache': Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'Edge' / 'User Data' / 'Default' / 'Cache',
    'edge_logs': Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'Edge' / 'User Data' / 'Default' / 'Logs',
    
    # Chrome (caso tenha)
    'chrome_data': Path(os.environ.get('LOCALAPPDATA', '')) / 'Google' / 'Chrome' / 'User Data' / 'Default',
    'chrome_history': Path(os.environ.get('LOCALAPPDATA', '')) / 'Google' / 'Chrome' / 'User Data' / 'Default' / 'History',
    
    # Programas instalados
    'programs_x64': Path('C:/Program Files'),
    'programs_x86': Path('C:/Program Files (x86)'),
    'appdata_programs': Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs',
    
    # Logs do Windows
    'windows_logs': Path('C:/Windows/Logs'),
    'event_logs': Path('C:/Windows/System32/winevt/Logs'),
    
    # Temp folders
    'temp': Path(os.environ.get('TEMP', '')),
    'windows_temp': Path('C:/Windows/Temp'),
}

# ===== WINDOWS BLOATWARE =====
WINDOWS_BLOATWARE = {
    # Xbox e Gaming
    'gaming': [
        'Microsoft.XboxApp',
        'Microsoft.XboxGameOverlay',
        'Microsoft.XboxGamingOverlay',
        'Microsoft.XboxIdentityProvider',
        'Microsoft.XboxSpeechToTextOverlay',
        'Microsoft.Xbox.TCUI',
        'Microsoft.GamingApp',
        'Microsoft.GamingServices',
        'Microsoft.XboxGameCallableUI',
    ],
    
    # Mídia e Entretenimento
    'media': [
        'Microsoft.ZuneMusic',
        'Microsoft.ZuneVideo',
        'Microsoft.Music',
        'Microsoft.TV',
        'SpotifyAB.SpotifyMusic',
        'Microsoft.Movies & TV',
        'Microsoft.WindowsCamera',
    ],
    
    # Redes Sociais e Comunicação
    'social': [
        'Microsoft.SkypeApp',
        'Microsoft.YourPhone',
        'Microsoft.People',
        'Microsoft.MicrosoftOfficeHub',
        'Microsoft.Getstarted',
        'Microsoft.WindowsFeedbackHub',
    ],
    
    # Utilidades desnecessárias
    'utilities': [
        'Microsoft.WindowsMaps',
        'Microsoft.WindowsAlarms',
        'Microsoft.BingWeather',
        'Microsoft.BingNews',
        'Microsoft.BingFinance',
        'Microsoft.BingSports',
        'Microsoft.BingTranslator',
        'Microsoft.WindowsSoundRecorder',
        'Microsoft.MicrosoftStickyNotes',
        'Microsoft.Print3D',
        'Microsoft.Mixed Reality Portal',
        'Microsoft.Microsoft3DViewer',
    ],
    
    # Jogos
    'games': [
        'Microsoft.MicrosoftSolitaireCollection',
        'Microsoft.MicrosoftMahjong',
        'Microsoft.FreshPaint',
        'Microsoft.Minecraft',
        'Microsoft.RobloxStudio',
        'king.com.CandyCrushSaga',
        'king.com.FarmHeroesSaga',
    ],
    
    # Cortana e assistentes
    'assistants': [
        'Microsoft.Cortana',
        'Microsoft.549981C3F5F10', # Cortana
    ]
}

# ===== OTIMIZAÇÕES PARA DESENVOLVEDORES =====
DEV_OPTIMIZATIONS = {
    # Serviços a desabilitar
    'disable_services': [
        'XboxGipSvc',           # Xbox Accessory Management Service
        'XblAuthManager',       # Xbox Live Auth Manager
        'XblGameSave',          # Xbox Live Game Save
        'XboxNetApiSvc',        # Xbox Live Networking Service
        'WSearch',              # Windows Search (pode usar Everything)
        'TabletInputService',   # Tablet Input Service
        'Themes',               # Themes service
        'WerSvc',               # Windows Error Reporting
        'DiagTrack',            # Connected User Experiences and Telemetry
        'dmwappushservice',     # WAP Push Message Routing
        'MapsBroker',           # Downloaded Maps Manager
        'lfsvc',                # Geolocation Service
        'SharedAccess',         # Internet Connection Sharing (se não usar)
        'TrkWks',               # Distributed Link Tracking Client
    ],
    
    # Configurações do registro
    'registry_tweaks': {
        # Desabilitar animações
        'HKEY_CURRENT_USER\\Control Panel\\Desktop\\MenuShowDelay': '0',
        'HKEY_CURRENT_USER\\Control Panel\\Desktop\\UserPreferencesMask': '90,32,07,80,12,00,00,00',
        
        # Melhorar performance
        'HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\\Win32PrioritySeparation': '26',
        
        # Desabilitar telemetria
        'HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection\\AllowTelemetry': '0',
        'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection\\AllowTelemetry': '0',
    },
    
    # Tarefas agendadas a desabilitar
    'disable_tasks': [
        'Microsoft\\Windows\\Application Experience\\Microsoft Compatibility Appraiser',
        'Microsoft\\Windows\\Application Experience\\ProgramDataUpdater',
        'Microsoft\\Windows\\Autochk\\Proxy',
        'Microsoft\\Windows\\Customer Experience Improvement Program\\Consolidator',
        'Microsoft\\Windows\\Customer Experience Improvement Program\\UsbCeip',
        'Microsoft\\Windows\\DiskDiagnostic\\Microsoft-Windows-DiskDiagnosticDataCollector',
        'Microsoft\\Windows\\Feedback\\Siuf\\DmClient',
        'Microsoft\\Windows\\Windows Error Reporting\\QueueReporting',
        'Microsoft\\Office\\OfficeBackgroundTaskHandlerRegistration',
    ]
}

# ===== FERRAMENTAS RECOMENDADAS PARA DESENVOLVEDORES =====
RECOMMENDED_TOOLS = {
    'essential': [
        {
            'name': 'Everything',
            'description': 'Busca instantânea de arquivos (substitui Windows Search)',
            'url': 'https://www.voidtools.com/',
            'category': 'search'
        },
        {
            'name': 'PowerToys',
            'description': 'Utilitários oficiais da Microsoft para power users',
            'url': 'https://github.com/microsoft/PowerToys',
            'category': 'utilities'
        },
        {
            'name': 'Windows Terminal',
            'description': 'Terminal moderno com suporte a múltiplas abas',
            'url': 'https://github.com/microsoft/terminal',
            'category': 'terminal'
        }
    ],
    
    'development': [
        {
            'name': 'WSL2',
            'description': 'Subsistema Linux para Windows',
            'command': 'wsl --install',
            'category': 'platform'
        },
        {
            'name': 'Docker Desktop',
            'description': 'Containerização para desenvolvimento',
            'url': 'https://www.docker.com/products/docker-desktop',
            'category': 'container'
        },
        {
            'name': 'Git',
            'description': 'Controle de versão',
            'url': 'https://git-scm.com/',
            'category': 'vcs'
        }
    ]
}

# ===== CONFIGURAÇÕES DE ANÁLISE =====
ANALYSIS_CONFIG = {
    # Período para considerar programa "não usado" (em dias)
    'unused_program_days': 90,
    
    # Tamanho mínimo para considerar limpeza (em MB)
    'min_cleanup_size': 100,
    
    # Extensões de arquivo temporário
    'temp_extensions': ['.tmp', '.temp', '.log', '.dmp', '.old', '.bak'],
    
    # Pastas de cache a limpar
    'cache_folders': [
        'AppData\\Local\\Temp',
        'AppData\\Local\\Microsoft\\Windows\\INetCache',
        'AppData\\Local\\Microsoft\\Windows\\Temporary Internet Files',
        'AppData\\Local\\CrashDumps',
    ]
}

# ===== CONFIGURAÇÕES DE RELATÓRIO =====
REPORT_CONFIG = {
    'format': 'html',  # html, json, txt
    'include_screenshots': False,
    'detailed_analysis': True,
    'safe_mode': True  # Apenas sugerir, não executar automaticamente
}

def get_user_folders():
    """Retorna pastas específicas do usuário atual"""
    username = os.environ.get('USERNAME', 'User')
    user_home = Path.home()
    
    return {
        'desktop': user_home / 'Desktop',
        'documents': user_home / 'Documents',
        'downloads': user_home / 'Downloads',
        'pictures': user_home / 'Pictures',
        'videos': user_home / 'Videos',
        'music': user_home / 'Music',
        'appdata': Path(os.environ.get('APPDATA', '')),
        'localappdata': Path(os.environ.get('LOCALAPPDATA', '')),
    }

if __name__ == "__main__":
    print(f"{APP_NAME} v{APP_VERSION}")
    print(f"Autor: {APP_AUTHOR}")
    print(f"Diretório base: {BASE_DIR}")
    
    # Verificar se caminhos existem
    print("\n=== VERIFICAÇÃO DE CAMINHOS ===")
    for name, path in WINDOWS_PATHS.items():
        exists = "✓" if path.exists() else "✗"
        print(f"{exists} {name}: {path}")