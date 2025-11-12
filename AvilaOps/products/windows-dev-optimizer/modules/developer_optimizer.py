# coding: utf-8
"""
Script: developer_optimizer.py
Função: Módulo de otimização para desenvolvedores
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer
Descrição: Aplica configurações específicas para melhorar performance em desenvolvimento
"""

import subprocess
import winreg
import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging
import psutil

class DeveloperOptimizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Ferramentas essenciais para desenvolvedores
        self.essential_tools = {
            "Git": {
                "check_command": ["git", "--version"],
                "install_command": "winget install Git.Git",
                "description": "Sistema de controle de versão"
            },
            "Node.js": {
                "check_command": ["node", "--version"],
                "install_command": "winget install OpenJS.NodeJS",
                "description": "Runtime JavaScript"
            },
            "Python": {
                "check_command": ["python", "--version"],
                "install_command": "winget install Python.Python.3.12",
                "description": "Linguagem de programação Python"
            },
            "Docker": {
                "check_command": ["docker", "--version"],
                "install_command": "winget install Docker.DockerDesktop",
                "description": "Plataforma de containerização"
            },
            "PowerToys": {
                "check_command": ["powertoys", "--version"],
                "install_command": "winget install Microsoft.PowerToys",
                "description": "Utilitários do Windows"
            },
            "Windows Terminal": {
                "check_command": ["wt", "--version"],
                "install_command": "winget install Microsoft.WindowsTerminal",
                "description": "Terminal moderno"
            },
            "VS Code": {
                "check_command": ["code", "--version"],
                "install_command": "winget install Microsoft.VisualStudioCode",
                "description": "Editor de código"
            }
        }
        
        # Configurações de performance
        self.performance_settings = {
            # Visual Effects - Desabilitar para performance
            "visual_effects": {
                "key": winreg.HKEY_CURRENT_USER,
                "path": r"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects",
                "values": {
                    "VisualFXSetting": 3  # Custom settings
                }
            },
            
            # Menu delays - Reduzir para responsividade
            "menu_delays": {
                "key": winreg.HKEY_CURRENT_USER,
                "path": r"Control Panel\\Desktop",
                "values": {
                    "MenuShowDelay": "0",
                    "WaitToKillAppTimeout": "2000",
                    "HungAppTimeout": "1000",
                    "AutoEndTasks": "1"
                }
            },
            
            # Priority settings - Otimizar para programas
            "priority_control": {
                "key": winreg.HKEY_LOCAL_MACHINE,
                "path": r"SYSTEM\\CurrentControlSet\\Control\\PriorityControl",
                "values": {
                    "Win32PrioritySeparation": 38  # Otimizado para programas
                }
            },
            
            # Memory management
            "memory_management": {
                "key": winreg.HKEY_LOCAL_MACHINE,
                "path": r"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management",
                "values": {
                    "ClearPageFileAtShutdown": 0,
                    "DisablePagingExecutive": 1,
                    "LargeSystemCache": 0
                }
            }
        }
    
    def check_system_specs(self) -> Dict[str, Any]:
        """Analisa especificações do sistema"""
        try:
            # CPU Info
            cpu_info = {
                "name": "Unknown",
                "cores": psutil.cpu_count(logical=False),
                "threads": psutil.cpu_count(logical=True),
                "frequency": psutil.cpu_freq().max if psutil.cpu_freq() else "Unknown"
            }
            
            # RAM Info
            memory = psutil.virtual_memory()
            ram_info = {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_percent": memory.percent
            }
            
            # Disk Info
            disk_info = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "used_percent": round((usage.used / usage.total) * 100, 1)
                    })
                except:
                    continue
            
            # Windows Version
            import platform
            windows_info = {
                "version": platform.version(),
                "release": platform.release(),
                "architecture": platform.architecture()[0]
            }
            
            return {
                "cpu": cpu_info,
                "ram": ram_info,
                "disks": disk_info,
                "windows": windows_info
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter specs do sistema: {e}")
            return {}
    
    def check_installed_tools(self) -> Dict[str, Dict[str, Any]]:
        """Verifica quais ferramentas de desenvolvimento estão instaladas"""
        tool_status = {}
        
        for tool_name, tool_info in self.essential_tools.items():
            try:
                result = subprocess.run(
                    tool_info["check_command"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    version = result.stdout.strip()
                    tool_status[tool_name] = {
                        "installed": True,
                        "version": version,
                        "description": tool_info["description"]
                    }
                else:
                    tool_status[tool_name] = {
                        "installed": False,
                        "install_command": tool_info["install_command"],
                        "description": tool_info["description"]
                    }
                    
            except (subprocess.TimeoutExpired, FileNotFoundError):
                tool_status[tool_name] = {
                    "installed": False,
                    "install_command": tool_info["install_command"],
                    "description": tool_info["description"]
                }
            except Exception as e:
                tool_status[tool_name] = {
                    "installed": False,
                    "error": str(e),
                    "install_command": tool_info["install_command"],
                    "description": tool_info["description"]
                }
        
        return tool_status
    
    def install_missing_tools(self, tools_to_install: List[str]) -> Dict[str, Any]:
        """Instala ferramentas de desenvolvimento faltantes"""
        installation_results = {}
        
        for tool_name in tools_to_install:
            if tool_name not in self.essential_tools:
                installation_results[tool_name] = {
                    "success": False,
                    "error": "Ferramenta não reconhecida"
                }
                continue
            
            install_command = self.essential_tools[tool_name]["install_command"]
            
            try:
                self.logger.info(f"Instalando {tool_name}...")
                
                # Executar comando de instalação
                result = subprocess.run(
                    install_command.split(),
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutos timeout
                )
                
                if result.returncode == 0:
                    installation_results[tool_name] = {
                        "success": True,
                        "message": f"{tool_name} instalado com sucesso"
                    }
                else:
                    installation_results[tool_name] = {
                        "success": False,
                        "error": result.stderr or "Erro desconhecido na instalação"
                    }
                    
            except subprocess.TimeoutExpired:
                installation_results[tool_name] = {
                    "success": False,
                    "error": "Timeout na instalação"
                }
            except Exception as e:
                installation_results[tool_name] = {
                    "success": False,
                    "error": str(e)
                }
        
        return installation_results
    
    def apply_performance_settings(self) -> Dict[str, Any]:
        """Aplica configurações de performance"""
        results = {
            "applied": [],
            "failed": [],
            "requires_restart": False
        }
        
        for setting_name, setting_config in self.performance_settings.items():
            try:
                key = winreg.CreateKey(setting_config["key"], setting_config["path"])
                
                for value_name, value_data in setting_config["values"].items():
                    try:
                        if isinstance(value_data, str):
                            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
                        else:
                            winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
                        
                        self.logger.info(f"Aplicado: {setting_name}.{value_name}")
                        
                    except Exception as e:
                        self.logger.error(f"Erro ao aplicar {setting_name}.{value_name}: {e}")
                
                winreg.CloseKey(key)
                results["applied"].append(setting_name)
                
                # Algumas configurações requerem restart
                if setting_name in ["priority_control", "memory_management"]:
                    results["requires_restart"] = True
                
            except PermissionError:
                results["failed"].append({
                    "setting": setting_name,
                    "error": "Permissão negada. Execute como administrador."
                })
            except Exception as e:
                results["failed"].append({
                    "setting": setting_name,
                    "error": str(e)
                })
        
        return results
    
    def configure_windows_defender(self) -> Dict[str, Any]:
        """Configura Windows Defender para desenvolvimento"""
        try:
            # Adicionar exclusões para pastas de desenvolvimento
            dev_folders = [
                str(Path.home() / "Documents"),
                str(Path.home() / "source"),
                str(Path.home() / "repos"),
                str(Path.home() / "projects"),
                "C:\\dev",
                "C:\\projects",
                "C:\\workspace"
            ]
            
            exclusions_added = []
            exclusions_failed = []
            
            for folder in dev_folders:
                if Path(folder).exists():
                    try:
                        cmd = [
                            "powershell", "-Command",
                            f"Add-MpPreference -ExclusionPath '{folder}'"
                        ]
                        
                        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                        
                        if result.returncode == 0:
                            exclusions_added.append(folder)
                        else:
                            exclusions_failed.append(folder)
                    except:
                        exclusions_failed.append(folder)
            
            # Adicionar exclusões para processos de desenvolvimento
            dev_processes = [
                "node.exe",
                "npm.exe", 
                "yarn.exe",
                "python.exe",
                "git.exe",
                "code.exe",
                "devenv.exe"  # Visual Studio
            ]
            
            for process in dev_processes:
                try:
                    cmd = [
                        "powershell", "-Command",
                        f"Add-MpPreference -ExclusionProcess '{process}'"
                    ]
                    subprocess.run(cmd, capture_output=True, text=True, shell=True)
                except:
                    pass
            
            return {
                "success": True,
                "exclusions_added": exclusions_added,
                "exclusions_failed": exclusions_failed,
                "message": f"Configurado {len(exclusions_added)} exclusões no Windows Defender"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def setup_development_environment(self) -> Dict[str, Any]:
        """Configura ambiente completo de desenvolvimento"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "errors": [],
            "recommendations": []
        }
        
        # 1. Verificar sistema
        results["steps"].append("Analisando sistema...")
        system_specs = self.check_system_specs()
        
        # Verificar se o sistema atende requisitos mínimos
        if system_specs.get("ram", {}).get("total_gb", 0) < 8:
            results["errors"].append("Sistema com menos de 8GB RAM pode ter performance limitada")
        
        # 2. Verificar ferramentas instaladas
        results["steps"].append("Verificando ferramentas de desenvolvimento...")
        tools_status = self.check_installed_tools()
        
        missing_tools = [name for name, status in tools_status.items() if not status["installed"]]
        if missing_tools:
            results["recommendations"].append(
                f"Ferramentas não instaladas: {', '.join(missing_tools)}"
            )
        
        # 3. Aplicar configurações de performance
        results["steps"].append("Aplicando configurações de performance...")
        perf_results = self.apply_performance_settings()
        
        if perf_results["failed"]:
            results["errors"].extend([f"Falha em: {item['setting']}" for item in perf_results["failed"]])
        
        if perf_results["requires_restart"]:
            results["recommendations"].append("Reinicie o sistema para aplicar todas as configurações")
        
        # 4. Configurar Windows Defender
        results["steps"].append("Configurando Windows Defender...")
        defender_results = self.configure_windows_defender()
        
        if not defender_results["success"]:
            results["errors"].append(f"Erro no Defender: {defender_results.get('error')}")
        
        # 5. Gerar recomendações específicas
        results["recommendations"].extend(self._generate_dev_recommendations(system_specs, tools_status))
        
        results["summary"] = {
            "system_ready": len(results["errors"]) == 0,
            "tools_installed": len(tools_status) - len(missing_tools),
            "total_tools": len(tools_status),
            "recommendations_count": len(results["recommendations"])
        }
        
        return results
    
    def _generate_dev_recommendations(self, system_specs: Dict, tools_status: Dict) -> List[str]:
        """Gera recomendações específicas baseadas no sistema"""
        recommendations = []
        
        # Recomendações de hardware
        ram_gb = system_specs.get("ram", {}).get("total_gb", 0)
        if ram_gb < 16:
            recommendations.append(
                f"Sistema com {ram_gb}GB RAM. Considere upgrade para 16GB+ para desenvolvimento pesado"
            )
        
        # Recomendações de SSD
        for disk in system_specs.get("disks", []):
            if disk["device"] == "C:\\" and disk["fstype"] != "NTFS":
                recommendations.append("Considere SSD para disco principal para melhor performance")
        
        # Recomendações de ferramentas
        if not tools_status.get("Git", {}).get("installed"):
            recommendations.append("Git é essencial para controle de versão")
        
        if not tools_status.get("VS Code", {}).get("installed"):
            recommendations.append("VS Code é recomendado como editor principal")
        
        if not tools_status.get("PowerToys", {}).get("installed"):
            recommendations.append("PowerToys adiciona funcionalidades úteis ao Windows")
        
        # Recomendações de WSL
        recommendations.append("Considere instalar WSL2 para ambiente Linux no Windows")
        
        return recommendations
    
    def enable_developer_mode(self) -> Dict[str, Any]:
        """Habilita modo de desenvolvedor do Windows"""
        try:
            key_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AppModelUnlock"
            
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            winreg.SetValueEx(key, "AllowDevelopmentWithoutDevLicense", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "AllowAllTrustedApps", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            return {
                "success": True,
                "message": "Modo de desenvolvedor habilitado"
            }
            
        except PermissionError:
            return {
                "success": False,
                "error": "Permissão negada. Execute como administrador."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def install_wsl2(self) -> Dict[str, Any]:
        """Instala WSL2 (Windows Subsystem for Linux)"""
        try:
            # Verificar se WSL já está instalado
            check_cmd = ["wsl", "--list"]
            result = subprocess.run(check_cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and "Ubuntu" in result.stdout:
                return {
                    "success": True,
                    "message": "WSL2 já está instalado",
                    "already_installed": True
                }
            
            # Instalar WSL2
            install_cmd = ["wsl", "--install", "-d", "Ubuntu"]
            result = subprocess.run(install_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "WSL2 instalado com sucesso. Reinicie o sistema.",
                    "requires_restart": True
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr or "Erro na instalação do WSL2"
                }
                
        except FileNotFoundError:
            return {
                "success": False,
                "error": "WSL não está disponível neste sistema"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

if __name__ == "__main__":
    optimizer = DeveloperOptimizer()
    
    print("=== WINDOWS DEV OPTIMIZER ===\n")
    
    # Verificar especificações
    print("Verificando especificações do sistema...")
    specs = optimizer.check_system_specs()
    print(f"✓ RAM: {specs.get('ram', {}).get('total_gb', 0)} GB")
    print(f"✓ CPU: {specs.get('cpu', {}).get('cores', 0)} cores / {specs.get('cpu', {}).get('threads', 0)} threads")
    
    # Verificar ferramentas
    print("\nVerificando ferramentas de desenvolvimento...")
    tools = optimizer.check_installed_tools()
    
    for tool_name, status in tools.items():
        if status["installed"]:
            print(f"✓ {tool_name}: {status['version']}")
        else:
            print(f"✗ {tool_name}: Não instalado")
    
    # Configurar ambiente
    print("\nConfigurando ambiente de desenvolvimento...")
    setup_result = optimizer.setup_development_environment()
    
    if setup_result["summary"]["system_ready"]:
        print("✓ Sistema configurado com sucesso!")
    else:
        print("⚠ Configuração concluída com alguns problemas")
    
    if setup_result["recommendations"]:
        print("\n=== RECOMENDAÇÕES ===")
        for rec in setup_result["recommendations"]:
            print(f"• {rec}")