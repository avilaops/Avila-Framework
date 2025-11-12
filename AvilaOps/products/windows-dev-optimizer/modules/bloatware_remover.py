# coding: utf-8
"""
Script: bloatware_remover.py
Função: Módulo de remoção de bloatware do Windows
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer
Descrição: Remove aplicativos desnecessários e otimiza o sistema para desenvolvedores
"""

import subprocess
import winreg
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

class BloatwareRemover:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Apps do Windows Store que podem ser removidos
        self.removable_apps = [
            # Xbox e Gaming
            "Microsoft.XboxApp",
            "Microsoft.XboxGameOverlay", 
            "Microsoft.XboxGamingOverlay",
            "Microsoft.XboxIdentityProvider",
            "Microsoft.XboxSpeechToTextOverlay",
            "Microsoft.Xbox.TCUI",
            "Microsoft.GamingApp",
            "Microsoft.GamingServices",
            
            # Mídia e Entretenimento
            "Microsoft.ZuneMusic",
            "Microsoft.ZuneVideo", 
            "SpotifyAB.SpotifyMusic",
            "Microsoft.WindowsCamera",
            
            # Redes Sociais
            "Microsoft.SkypeApp",
            "Microsoft.YourPhone",
            "Microsoft.People",
            "Microsoft.WindowsFeedbackHub",
            
            # Utilitários desnecessários
            "Microsoft.WindowsMaps",
            "Microsoft.WindowsAlarms",
            "Microsoft.BingWeather",
            "Microsoft.BingNews",
            "Microsoft.BingFinance",
            "Microsoft.BingSports",
            "Microsoft.WindowsSoundRecorder",
            "Microsoft.MicrosoftStickyNotes",
            "Microsoft.Print3D",
            "Microsoft.Mixed Reality Portal",
            "Microsoft.Microsoft3DViewer",
            
            # Jogos
            "Microsoft.MicrosoftSolitaireCollection",
            "Microsoft.MicrosoftMahjong",
            "Microsoft.FreshPaint",
            "king.com.CandyCrushSaga",
            "king.com.FarmHeroesSaga",
            
            # Cortana (pode ser removido no Windows 11)
            "Microsoft.549981C3F5F10",  # Cortana
        ]
        
        # Apps que NUNCA devem ser removidos (críticos para o sistema)
        self.protected_apps = [
            "Microsoft.WindowsStore",
            "Microsoft.WindowsTerminal", 
            "Microsoft.DesktopAppInstaller",
            "Microsoft.VCLibs",
            "Microsoft.UI.Xaml",
            "Microsoft.NET.Native",
            "Microsoft.WindowsNotepad",
            "Microsoft.WindowsCalculator",
            "Microsoft.Windows.Photos",
            "Microsoft.MSPaint",
            "Microsoft.PowerShell",
            "Microsoft.MicrosoftEdge",
            "Microsoft.WebMediaExtensions",
            "Microsoft.WebpImageExtension",
            "Microsoft.ScreenSketch"
        ]
    
    def scan_installed_apps(self) -> Dict[str, List[Dict[str, Any]]]:
        """Escaneia apps instalados e categoriza em removíveis/protegidos"""
        try:
            # Usar PowerShell para obter lista completa de apps
            cmd = ["powershell", "-Command", "Get-AppxPackage | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.returncode != 0:
                self.logger.error(f"Erro ao executar PowerShell: {result.stderr}")
                return {"removable": [], "protected": [], "other": []}
            
            apps_data = json.loads(result.stdout)
            
            # Garantir que apps_data seja uma lista
            if isinstance(apps_data, dict):
                apps_data = [apps_data]
            
            removable = []
            protected = []
            other = []
            
            for app in apps_data:
                app_info = {
                    "name": app.get("Name", ""),
                    "package_full_name": app.get("PackageFullName", ""),
                    "publisher": app.get("Publisher", ""),
                    "version": app.get("Version", ""),
                    "install_location": app.get("InstallLocation", ""),
                    "is_framework": app.get("IsFramework", False),
                    "size_mb": self._get_app_size(app.get("InstallLocation", ""))
                }
                
                app_name = app_info["name"]
                
                if app_name in self.protected_apps:
                    protected.append(app_info)
                elif any(removable_name in app_name for removable_name in self.removable_apps):
                    removable.append(app_info)
                else:
                    other.append(app_info)
            
            return {
                "removable": removable,
                "protected": protected, 
                "other": other
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao escanear apps: {e}")
            return {"removable": [], "protected": [], "other": []}
    
    def _get_app_size(self, install_location: str) -> float:
        """Calcula tamanho aproximado do app"""
        if not install_location or not Path(install_location).exists():
            return 0.0
        
        try:
            total_size = 0
            for root, dirs, files in os.walk(install_location):
                for file in files:
                    try:
                        file_path = Path(root) / file
                        total_size += file_path.stat().st_size
                    except:
                        continue
            
            return total_size / (1024 * 1024)  # Converter para MB
        except:
            return 0.0
    
    def remove_app(self, package_name: str, for_all_users: bool = False) -> Dict[str, Any]:
        """Remove um app específico"""
        try:
            # Verificar se é app protegido
            if any(protected in package_name for protected in self.protected_apps):
                return {
                    "success": False,
                    "error": "App está protegido contra remoção",
                    "package": package_name
                }
            
            # Comando PowerShell para remoção
            if for_all_users:
                cmd = [
                    "powershell", "-Command", 
                    f"Get-AppxPackage -AllUsers '{package_name}' | Remove-AppxPackage -AllUsers"
                ]
            else:
                cmd = [
                    "powershell", "-Command",
                    f"Get-AppxPackage '{package_name}' | Remove-AppxPackage"
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                self.logger.info(f"App removido com sucesso: {package_name}")
                return {
                    "success": True,
                    "package": package_name,
                    "message": "App removido com sucesso"
                }
            else:
                error_msg = result.stderr or "Erro desconhecido"
                self.logger.error(f"Erro ao remover {package_name}: {error_msg}")
                return {
                    "success": False,
                    "package": package_name,
                    "error": error_msg
                }
                
        except Exception as e:
            return {
                "success": False,
                "package": package_name,
                "error": str(e)
            }
    
    def remove_multiple_apps(self, package_names: List[str]) -> Dict[str, Any]:
        """Remove múltiplos apps"""
        results = {
            "total_attempted": len(package_names),
            "successful": [],
            "failed": [],
            "skipped": []
        }
        
        for package_name in package_names:
            # Verificar se é protegido
            if any(protected in package_name for protected in self.protected_apps):
                results["skipped"].append({
                    "package": package_name,
                    "reason": "App protegido"
                })
                continue
            
            result = self.remove_app(package_name)
            
            if result["success"]:
                results["successful"].append(package_name)
            else:
                results["failed"].append({
                    "package": package_name,
                    "error": result["error"]
                })
        
        return results
    
    def disable_cortana(self) -> Dict[str, Any]:
        """Desabilita Cortana via registro"""
        try:
            # Chave do registro para desabilitar Cortana
            key_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
            
            # Criar/abrir chave
            try:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            except PermissionError:
                return {
                    "success": False,
                    "error": "Permissão negada. Execute como administrador."
                }
            
            # Definir valores para desabilitar Cortana
            winreg.SetValueEx(key, "AllowCortana", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "DisableWebSearch", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ConnectedSearchUseWeb", 0, winreg.REG_DWORD, 0)
            
            winreg.CloseKey(key)
            
            return {
                "success": True,
                "message": "Cortana desabilitada com sucesso"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def disable_telemetry(self) -> Dict[str, Any]:
        """Desabilita coleta de dados do Windows"""
        try:
            telemetry_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 0),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", "AllowTelemetry", 0),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\DataCollection", "AllowTelemetry", 0),
            ]
            
            results = []
            
            for hkey, key_path, value_name, value_data in telemetry_keys:
                try:
                    key = winreg.CreateKey(hkey, key_path)
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
                    winreg.CloseKey(key)
                    results.append(f"✓ {key_path}")
                except PermissionError:
                    results.append(f"✗ {key_path} (sem permissão)")
                except Exception as e:
                    results.append(f"✗ {key_path} ({str(e)})")
            
            return {
                "success": True,
                "message": "Configurações de telemetria aplicadas",
                "details": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def disable_unnecessary_services(self) -> Dict[str, Any]:
        """Desabilita serviços desnecessários para desenvolvedores"""
        services_to_disable = [
            "XboxGipSvc",           # Xbox Accessory Management
            "XblAuthManager",       # Xbox Live Auth Manager  
            "XblGameSave",          # Xbox Live Game Save
            "XboxNetApiSvc",        # Xbox Live Networking
            "WSearch",              # Windows Search (pode usar Everything)
            "TabletInputService",   # Serviço de entrada de tablet
            "WerSvc",               # Windows Error Reporting
            "DiagTrack",            # Telemetria
            "dmwappushservice",     # WAP Push Message Routing
            "MapsBroker",           # Downloaded Maps Manager
            "lfsvc",                # Geolocation Service
        ]
        
        results = {
            "disabled": [],
            "failed": [],
            "not_found": []
        }
        
        for service in services_to_disable:
            try:
                # Verificar se o serviço existe
                cmd_check = ["sc", "query", service]
                check_result = subprocess.run(cmd_check, capture_output=True, text=True)
                
                if check_result.returncode != 0:
                    results["not_found"].append(service)
                    continue
                
                # Parar o serviço
                cmd_stop = ["sc", "stop", service]
                stop_result = subprocess.run(cmd_stop, capture_output=True, text=True)
                
                # Desabilitar o serviço
                cmd_disable = ["sc", "config", service, "start=", "disabled"]
                disable_result = subprocess.run(cmd_disable, capture_output=True, text=True)
                
                if disable_result.returncode == 0:
                    results["disabled"].append(service)
                else:
                    results["failed"].append({
                        "service": service,
                        "error": disable_result.stderr
                    })
                
            except Exception as e:
                results["failed"].append({
                    "service": service,
                    "error": str(e)
                })
        
        return {
            "success": len(results["disabled"]) > 0,
            "message": f"Desabilitados {len(results['disabled'])} serviços",
            "results": results
        }
    
    def apply_performance_tweaks(self) -> Dict[str, Any]:
        """Aplica ajustes de performance para desenvolvedores"""
        tweaks = [
            # Desabilitar animações
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "MenuShowDelay", "0"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", 3),
            
            # Otimizar para performance
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\PriorityControl", "Win32PrioritySeparation", 38),
            
            # Desabilitar Superfetch
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnableSuperfetch", 0),
        ]
        
        results = []
        
        for hkey, key_path, value_name, value_data in tweaks:
            try:
                key = winreg.CreateKey(hkey, key_path)
                
                if isinstance(value_data, str):
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
                else:
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
                
                winreg.CloseKey(key)
                results.append(f"✓ {key_path}\\{value_name}")
                
            except PermissionError:
                results.append(f"✗ {key_path}\\{value_name} (sem permissão)")
            except Exception as e:
                results.append(f"✗ {key_path}\\{value_name} ({str(e)})")
        
        return {
            "success": True,
            "message": "Ajustes de performance aplicados",
            "details": results
        }
    
    def generate_removal_report(self) -> Dict[str, Any]:
        """Gera relatório de apps que podem ser removidos"""
        apps_scan = self.scan_installed_apps()
        
        removable_apps = apps_scan["removable"]
        total_removable_size = sum(app["size_mb"] for app in removable_apps)
        
        # Categorizar por tipo
        categories = {
            "gaming": [],
            "media": [],
            "social": [],
            "utilities": [],
            "other": []
        }
        
        gaming_keywords = ["xbox", "gaming", "game"]
        media_keywords = ["zune", "music", "camera", "spotify"]
        social_keywords = ["skype", "people", "phone"]
        
        for app in removable_apps:
            name_lower = app["name"].lower()
            
            if any(keyword in name_lower for keyword in gaming_keywords):
                categories["gaming"].append(app)
            elif any(keyword in name_lower for keyword in media_keywords):
                categories["media"].append(app)
            elif any(keyword in name_lower for keyword in social_keywords):
                categories["social"].append(app)
            elif "bing" in name_lower or "maps" in name_lower or "weather" in name_lower:
                categories["utilities"].append(app)
            else:
                categories["other"].append(app)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_removable": len(removable_apps),
                "total_size_mb": total_removable_size,
                "potential_savings_gb": total_removable_size / 1024,
                "categories_count": {cat: len(apps) for cat, apps in categories.items()}
            },
            "categories": categories,
            "recommendations": self._generate_removal_recommendations(categories)
        }
    
    def _generate_removal_recommendations(self, categories: Dict[str, List]) -> List[str]:
        """Gera recomendações de remoção"""
        recommendations = []
        
        if categories["gaming"]:
            recommendations.append(
                f"Apps de Gaming ({len(categories['gaming'])}): Remova se você não joga no Windows. "
                "Inclui Xbox apps que consomem recursos."
            )
        
        if categories["media"]:
            recommendations.append(
                f"Apps de Mídia ({len(categories['media'])}): Considere remover se usa outros players. "
                "Zune e apps similares são raramente utilizados."
            )
        
        if categories["social"]:
            recommendations.append(
                f"Apps Sociais ({len(categories['social'])}): Skype e People podem ser removidos "
                "se você usa outras ferramentas de comunicação."
            )
        
        if categories["utilities"]:
            recommendations.append(
                f"Utilitários ({len(categories['utilities'])}): Apps Bing podem ser removidos "
                "se você prefere usar o navegador para essas funções."
            )
        
        return recommendations
    
    def create_restore_point(self) -> Dict[str, Any]:
        """Cria ponto de restauração antes das modificações"""
        try:
            restore_point_name = f"Windows Dev Optimizer - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            cmd = [
                "powershell", "-Command",
                f"Checkpoint-Computer -Description '{restore_point_name}' -RestorePointType 'MODIFY_SETTINGS'"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Ponto de restauração criado: {restore_point_name}"
                }
            else:
                return {
                    "success": False,
                    "error": f"Erro ao criar ponto de restauração: {result.stderr}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

if __name__ == "__main__":
    remover = BloatwareRemover()
    
    print("Escaneando apps instalados...")
    apps = remover.scan_installed_apps()
    
    print(f"✓ Apps removíveis: {len(apps['removable'])}")
    print(f"✓ Apps protegidos: {len(apps['protected'])}")
    print(f"✓ Outros apps: {len(apps['other'])}")
    
    if apps['removable']:
        print("\n=== APPS REMOVÍVEIS ===")
        for app in apps['removable'][:10]:  # Mostrar apenas os primeiros 10
            print(f"• {app['name']} ({app['size_mb']:.1f} MB)")
    
    report = remover.generate_removal_report()
    print(f"\nPotencial economia de espaço: {report['summary']['potential_savings_gb']:.1f} GB")