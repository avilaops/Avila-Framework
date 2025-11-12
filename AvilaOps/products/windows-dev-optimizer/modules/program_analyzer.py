# coding: utf-8
"""
Script: program_analyzer.py
Função: Módulo de análise de programas instalados
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer
Descrição: Identifica programas não utilizados há muito tempo
"""

import winreg
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import psutil

class ProgramAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Registro do Windows onde estão os programas instalados
        self.uninstall_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        
        # Programas do Windows que NÃO devem ser removidos
        self.windows_essential = [
            'Microsoft Visual C++', 'Visual Studio', '.NET Framework', '.NET Core',
            'Windows SDK', 'Microsoft Office', 'Windows Update', 'Windows Defender',
            'Intel', 'AMD', 'NVIDIA', 'Realtek', 'Microsoft Edge WebView2',
            'Windows Feature Experience Pack', 'App Installer', 'Microsoft Store',
            'Microsoft Photos', 'Microsoft Calculator', 'Microsoft Notepad',
            'Windows Terminal', 'PowerShell', 'OneDrive', 'Microsoft Teams'
        ]
        
        # Diretórios de programas
        self.program_dirs = [
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)"),
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs'
        ]
    
    def get_installed_programs(self) -> List[Dict[str, Any]]:
        """Obtém lista completa de programas instalados via registro"""
        programs = []
        
        for hkey, subkey_path in self.uninstall_keys:
            try:
                with winreg.OpenKey(hkey, subkey_path) as key:
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            program_info = self._get_program_info(hkey, f"{subkey_path}\\{subkey_name}")
                            
                            if program_info and self._is_valid_program(program_info):
                                programs.append(program_info)
                            
                            i += 1
                        except WindowsError:
                            break
            except FileNotFoundError:
                continue
            except Exception as e:
                self.logger.error(f"Erro ao acessar registro {subkey_path}: {e}")
        
        # Remover duplicatas baseado no nome
        unique_programs = {}
        for program in programs:
            key = program['display_name'].lower()
            if key not in unique_programs:
                unique_programs[key] = program
        
        return list(unique_programs.values())
    
    def _get_program_info(self, hkey: int, subkey_path: str) -> Optional[Dict[str, Any]]:
        """Extrai informações de um programa do registro"""
        try:
            with winreg.OpenKey(hkey, subkey_path) as key:
                program_info = {
                    'registry_key': subkey_path,
                    'hkey': 'HKLM' if hkey == winreg.HKEY_LOCAL_MACHINE else 'HKCU'
                }
                
                # Campos importantes do registro
                fields = {
                    'DisplayName': 'display_name',
                    'DisplayVersion': 'version',
                    'Publisher': 'publisher',
                    'InstallDate': 'install_date',
                    'EstimatedSize': 'size_kb',
                    'InstallLocation': 'install_location',
                    'UninstallString': 'uninstall_string',
                    'URLInfoAbout': 'url',
                    'HelpLink': 'help_link',
                    'WindowsInstaller': 'windows_installer'
                }
                
                for reg_field, prog_field in fields.items():
                    try:
                        value, _ = winreg.QueryValueEx(key, reg_field)
                        program_info[prog_field] = value
                    except FileNotFoundError:
                        program_info[prog_field] = None
                
                return program_info
                
        except Exception as e:
            self.logger.debug(f"Erro ao ler programa em {subkey_path}: {e}")
            return None
    
    def _is_valid_program(self, program_info: Dict[str, Any]) -> bool:
        """Verifica se é um programa válido (não update, driver, etc.)"""
        if not program_info.get('display_name'):
            return False
        
        name = program_info['display_name'].lower()
        
        # Filtrar atualizações, drivers e componentes do sistema
        invalid_keywords = [
            'update', 'hotfix', 'kb', 'security update',
            'driver', 'redistributable', 'runtime',
            'language pack', 'mui', 'toolkit'
        ]
        
        return not any(keyword in name for keyword in invalid_keywords)
    
    def get_program_usage_stats(self) -> Dict[str, Dict[str, Any]]:
        """Analisa uso dos programas baseado em arquivos e processos"""
        programs = self.get_installed_programs()
        usage_stats = {}
        
        # Obter processos ativos
        running_processes = {proc.name().lower() for proc in psutil.process_iter(['name'])}
        
        for program in programs:
            name = program['display_name']
            install_location = program.get('install_location')
            
            stats = {
                'install_date': self._parse_install_date(program.get('install_date')),
                'size_mb': (program.get('size_kb', 0) or 0) / 1024 if program.get('size_kb') else 0,
                'last_used': None,
                'currently_running': False,
                'executable_found': False,
                'days_since_install': None,
                'days_since_last_use': None
            }
            
            # Calcular dias desde instalação
            if stats['install_date']:
                days_since_install = (datetime.now() - stats['install_date']).days
                stats['days_since_install'] = days_since_install
            
            # Verificar se está rodando
            if install_location and Path(install_location).exists():
                stats['executable_found'] = True
                stats['last_used'] = self._get_last_file_access(install_location)
                
                # Verificar se processo está ativo
                try:
                    exe_files = list(Path(install_location).glob("*.exe"))
                    for exe_file in exe_files:
                        if exe_file.name.lower() in running_processes:
                            stats['currently_running'] = True
                            stats['last_used'] = datetime.now()
                            break
                except:
                    pass
            
            # Calcular dias desde último uso
            if stats['last_used']:
                stats['days_since_last_use'] = (datetime.now() - stats['last_used']).days
            
            usage_stats[name] = stats
        
        return usage_stats
    
    def _parse_install_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Converte data de instalação do registro para datetime"""
        if not date_str:
            return None
        
        try:
            # Formato: YYYYMMDD
            if len(date_str) == 8 and date_str.isdigit():
                return datetime.strptime(date_str, "%Y%m%d")
        except:
            pass
        
        return None
    
    def _get_last_file_access(self, directory: str) -> Optional[datetime]:
        """Obtém data do último acesso a arquivos no diretório"""
        try:
            directory = Path(directory)
            if not directory.exists():
                return None
            
            latest_access = None
            
            # Verificar arquivos .exe primeiro (mais provável de indicar uso)
            for exe_file in directory.rglob("*.exe"):
                try:
                    stat = exe_file.stat()
                    access_time = datetime.fromtimestamp(max(stat.st_atime, stat.st_mtime))
                    
                    if not latest_access or access_time > latest_access:
                        latest_access = access_time
                except:
                    continue
            
            # Se não encontrou .exe, verificar outros arquivos
            if not latest_access:
                for file_path in directory.rglob("*"):
                    try:
                        if file_path.is_file():
                            stat = file_path.stat()
                            access_time = datetime.fromtimestamp(max(stat.st_atime, stat.st_mtime))
                            
                            if not latest_access or access_time > latest_access:
                                latest_access = access_time
                    except:
                        continue
            
            return latest_access
            
        except Exception as e:
            self.logger.debug(f"Erro ao verificar acesso a {directory}: {e}")
            return None
    
    def identify_unused_programs(self, days_threshold: int = 90) -> List[Dict[str, Any]]:
        """Identifica programas não usados há X dias"""
        usage_stats = self.get_program_usage_stats()
        unused_programs = []
        
        for program_name, stats in usage_stats.items():
            # Pular programas essenciais do Windows
            if self._is_windows_essential(program_name):
                continue
            
            # Considerar não usado se:
            # 1. Nunca foi usado (sem data de último uso)
            # 2. Não foi usado há mais de X dias
            # 3. Não está rodando atualmente
            
            is_unused = False
            reason = ""
            
            if not stats['currently_running']:
                if stats['days_since_last_use'] is None:
                    # Nunca foi usado (provavelmente)
                    if stats['days_since_install'] and stats['days_since_install'] > days_threshold:
                        is_unused = True
                        reason = f"Instalado há {stats['days_since_install']} dias, nunca usado"
                elif stats['days_since_last_use'] > days_threshold:
                    is_unused = True
                    reason = f"Não usado há {stats['days_since_last_use']} dias"
            
            if is_unused:
                # Buscar informações completas do programa
                programs = self.get_installed_programs()
                program_info = next((p for p in programs if p['display_name'] == program_name), None)
                
                if program_info:
                    unused_info = {
                        **program_info,
                        **stats,
                        'unused_reason': reason,
                        'recommended_action': self._get_recommended_action(program_info, stats)
                    }
                    unused_programs.append(unused_info)
        
        # Ordenar por tamanho (maiores primeiro) para priorizar limpeza
        unused_programs.sort(key=lambda x: x.get('size_mb', 0), reverse=True)
        
        return unused_programs
    
    def _is_windows_essential(self, program_name: str) -> bool:
        """Verifica se é um programa essencial do Windows"""
        name_lower = program_name.lower()
        return any(essential.lower() in name_lower for essential in self.windows_essential)
    
    def _get_recommended_action(self, program_info: Dict[str, Any], stats: Dict[str, Any]) -> str:
        """Sugere ação recomendada para o programa"""
        size_mb = stats.get('size_mb', 0)
        days_unused = stats.get('days_since_last_use', 0) or 0
        
        if size_mb > 500:  # Programas grandes (>500MB)
            return "Remoção recomendada - programa grande não utilizado"
        elif days_unused > 180:  # Não usado há mais de 6 meses
            return "Remoção recomendada - não utilizado há muito tempo"
        elif days_unused > 90:  # Não usado há mais de 3 meses
            return "Considere remoção - não utilizado recentemente"
        else:
            return "Monitorar uso"
    
    def get_disk_space_analysis(self) -> Dict[str, Any]:
        """Analisa uso de espaço em disco pelos programas"""
        programs = self.get_installed_programs()
        usage_stats = self.get_program_usage_stats()
        
        total_size = 0
        unused_size = 0
        largest_programs = []
        
        for program in programs:
            name = program['display_name']
            size_mb = usage_stats.get(name, {}).get('size_mb', 0)
            total_size += size_mb
            
            # Verificar se é programa não usado
            if name in usage_stats:
                stats = usage_stats[name]
                if (stats.get('days_since_last_use', 0) or 0) > 90 and not stats.get('currently_running', False):
                    unused_size += size_mb
            
            # Adicionar aos maiores programas
            if size_mb > 0:
                largest_programs.append({
                    'name': name,
                    'size_mb': size_mb,
                    'publisher': program.get('publisher', 'Desconhecido'),
                    'install_date': stats.get('install_date') if name in usage_stats else None
                })
        
        # Ordenar maiores programas
        largest_programs.sort(key=lambda x: x['size_mb'], reverse=True)
        
        return {
            'total_programs': len(programs),
            'total_size_mb': total_size,
            'unused_size_mb': unused_size,
            'potential_savings_mb': unused_size,
            'largest_programs': largest_programs[:20]  # Top 20
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório completo da análise de programas"""
        programs = self.get_installed_programs()
        usage_stats = self.get_program_usage_stats()
        unused_programs = self.identify_unused_programs()
        disk_analysis = self.get_disk_space_analysis()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_programs': len(programs),
                'unused_programs': len(unused_programs),
                'potential_space_savings_mb': sum(p.get('size_mb', 0) for p in unused_programs),
                'potential_space_savings_gb': sum(p.get('size_mb', 0) for p in unused_programs) / 1024
            },
            'unused_programs': unused_programs,
            'disk_analysis': disk_analysis,
            'recommendations': self._generate_recommendations(unused_programs, disk_analysis)
        }
        
        return report
    
    def _generate_recommendations(self, unused_programs: List[Dict], disk_analysis: Dict) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        if unused_programs:
            total_savings = sum(p.get('size_mb', 0) for p in unused_programs)
            recommendations.append(
                f"Encontrados {len(unused_programs)} programas não utilizados que podem liberar "
                f"{total_savings/1024:.1f} GB de espaço"
            )
            
            # Top 3 programas que mais liberam espaço
            top_space_wasters = sorted(unused_programs, key=lambda x: x.get('size_mb', 0), reverse=True)[:3]
            for program in top_space_wasters:
                if program.get('size_mb', 0) > 100:  # Só recomendar se > 100MB
                    recommendations.append(
                        f"Considere remover '{program['display_name']}' - "
                        f"{program.get('size_mb', 0):.0f} MB não utilizados há "
                        f"{program.get('days_since_last_use', 'muito')} dias"
                    )
        
        return recommendations

if __name__ == "__main__":
    analyzer = ProgramAnalyzer()
    
    print("Analisando programas instalados...")
    programs = analyzer.get_installed_programs()
    print(f"✓ Encontrados {len(programs)} programas instalados")
    
    print("Analisando uso dos programas...")
    unused = analyzer.identify_unused_programs()
    print(f"✓ Encontrados {len(unused)} programas não utilizados")
    
    if unused:
        print("\n=== TOP 5 PROGRAMAS NÃO UTILIZADOS ===")
        for program in unused[:5]:
            print(f"• {program['display_name']} - {program.get('size_mb', 0):.0f} MB")
            print(f"  {program['unused_reason']}")
    
    disk_analysis = analyzer.get_disk_space_analysis()
    print(f"\n=== ANÁLISE DE ESPAÇO ===")
    print(f"Total de programas: {disk_analysis['total_programs']}")
    print(f"Espaço total: {disk_analysis['total_size_mb']/1024:.1f} GB")
    print(f"Espaço liberável: {disk_analysis['unused_size_mb']/1024:.1f} GB")