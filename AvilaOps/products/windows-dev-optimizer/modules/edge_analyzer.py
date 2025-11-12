# coding: utf-8
"""
Script: edge_analyzer.py
Função: Módulo de análise de logs do Microsoft Edge
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer
Descrição: Analisa histórico, cache, cookies e outros dados do Microsoft Edge
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import logging

class EdgeAnalyzer:
    def __init__(self):
        self.edge_path = Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'Edge' / 'User Data' / 'Default'
        self.history_db = self.edge_path / 'History'
        self.cache_path = self.edge_path / 'Cache'
        self.cookies_db = self.edge_path / 'Cookies'
        self.bookmarks_file = self.edge_path / 'Bookmarks'
        self.preferences_file = self.edge_path / 'Preferences'
        
        self.logger = logging.getLogger(__name__)
    
    def check_edge_installation(self) -> bool:
        """Verifica se o Edge está instalado e localiza os arquivos"""
        return self.edge_path.exists() and self.history_db.exists()
    
    def get_browsing_history(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """Extrai histórico de navegação dos últimos X dias"""
        if not self.history_db.exists():
            self.logger.warning("Arquivo de histórico não encontrado")
            return []
        
        # Copiar arquivo temporariamente (Edge pode estar usando)
        temp_history = self.edge_path / 'temp_history.db'
        try:
            import shutil
            shutil.copy2(self.history_db, temp_history)
            
            conn = sqlite3.connect(temp_history)
            cursor = conn.cursor()
            
            # Calcular timestamp de X dias atrás
            cutoff_date = datetime.now() - timedelta(days=days_back)
            cutoff_timestamp = int(cutoff_date.timestamp() * 1000000)
            
            query = """
            SELECT 
                urls.url,
                urls.title,
                urls.visit_count,
                urls.last_visit_time,
                visits.visit_time,
                visits.visit_duration
            FROM urls
            LEFT JOIN visits ON urls.id = visits.url
            WHERE urls.last_visit_time > ?
            ORDER BY urls.last_visit_time DESC
            """
            
            cursor.execute(query, (cutoff_timestamp,))
            results = cursor.fetchall()
            
            history_data = []
            for row in results:
                # Converter timestamp do Chrome/Edge para datetime
                if row[3]:  # last_visit_time
                    visit_time = datetime.fromtimestamp((row[3] - 11644473600000000) / 1000000)
                else:
                    visit_time = None
                
                history_data.append({
                    'url': row[0],
                    'title': row[1] or 'Sem título',
                    'visit_count': row[2] or 0,
                    'last_visit': visit_time,
                    'duration': row[5] or 0
                })
            
            conn.close()
            return history_data
            
        except Exception as e:
            self.logger.error(f"Erro ao ler histórico: {e}")
            return []
        finally:
            if temp_history.exists():
                temp_history.unlink()
    
    def get_most_visited_sites(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retorna os sites mais visitados"""
        history = self.get_browsing_history(days_back=90)
        
        # Agrupar por domínio
        domain_stats = {}
        for entry in history:
            try:
                from urllib.parse import urlparse
                domain = urlparse(entry['url']).netloc
                if domain:
                    if domain not in domain_stats:
                        domain_stats[domain] = {
                            'domain': domain,
                            'visit_count': 0,
                            'total_duration': 0,
                            'last_visit': None
                        }
                    
                    domain_stats[domain]['visit_count'] += entry['visit_count']
                    domain_stats[domain]['total_duration'] += entry['duration']
                    
                    if not domain_stats[domain]['last_visit'] or \
                       (entry['last_visit'] and entry['last_visit'] > domain_stats[domain]['last_visit']):
                        domain_stats[domain]['last_visit'] = entry['last_visit']
            except:
                continue
        
        # Ordenar por visitas e retornar top sites
        sorted_sites = sorted(domain_stats.values(), 
                            key=lambda x: x['visit_count'], 
                            reverse=True)
        
        return sorted_sites[:limit]
    
    def analyze_productivity_sites(self) -> Dict[str, Any]:
        """Analisa sites visitados categorizando produtividade"""
        
        productive_domains = [
            'github.com', 'stackoverflow.com', 'docs.microsoft.com',
            'developer.mozilla.org', 'w3schools.com', 'python.org',
            'nodejs.org', 'reactjs.org', 'angular.io', 'vuejs.org',
            'docker.com', 'kubernetes.io', 'aws.amazon.com',
            'azure.microsoft.com', 'cloud.google.com'
        ]
        
        entertainment_domains = [
            'youtube.com', 'netflix.com', 'facebook.com', 'instagram.com',
            'twitter.com', 'tiktok.com', 'twitch.tv', 'reddit.com'
        ]
        
        most_visited = self.get_most_visited_sites(50)
        
        productive_time = 0
        entertainment_time = 0
        neutral_time = 0
        
        categorized_sites = {
            'productive': [],
            'entertainment': [],
            'neutral': []
        }
        
        for site in most_visited:
            domain = site['domain'].lower()
            duration = site['total_duration']
            
            if any(prod_domain in domain for prod_domain in productive_domains):
                categorized_sites['productive'].append(site)
                productive_time += duration
            elif any(ent_domain in domain for ent_domain in entertainment_domains):
                categorized_sites['entertainment'].append(site)
                entertainment_time += duration
            else:
                categorized_sites['neutral'].append(site)
                neutral_time += duration
        
        total_time = productive_time + entertainment_time + neutral_time
        
        return {
            'categorized_sites': categorized_sites,
            'time_analysis': {
                'productive_time': productive_time,
                'entertainment_time': entertainment_time,
                'neutral_time': neutral_time,
                'total_time': total_time,
                'productivity_percentage': (productive_time / total_time * 100) if total_time > 0 else 0
            }
        }
    
    def get_cache_size(self) -> Dict[str, int]:
        """Calcula tamanho do cache do Edge"""
        cache_info = {
            'total_size': 0,
            'file_count': 0,
            'folders': {}
        }
        
        if not self.cache_path.exists():
            return cache_info
        
        try:
            for root, dirs, files in os.walk(self.cache_path):
                folder_size = 0
                for file in files:
                    try:
                        file_path = Path(root) / file
                        size = file_path.stat().st_size
                        folder_size += size
                        cache_info['total_size'] += size
                        cache_info['file_count'] += 1
                    except:
                        continue
                
                if folder_size > 0:
                    cache_info['folders'][root] = folder_size
        
        except Exception as e:
            self.logger.error(f"Erro ao calcular cache: {e}")
        
        return cache_info
    
    def get_cookies_info(self) -> Dict[str, Any]:
        """Analisa cookies armazenados"""
        if not self.cookies_db.exists():
            return {'count': 0, 'domains': []}
        
        temp_cookies = self.edge_path / 'temp_cookies.db'
        try:
            import shutil
            shutil.copy2(self.cookies_db, temp_cookies)
            
            conn = sqlite3.connect(temp_cookies)
            cursor = conn.cursor()
            
            # Contar cookies por domínio
            cursor.execute("""
                SELECT host_key, COUNT(*) as cookie_count
                FROM cookies
                GROUP BY host_key
                ORDER BY cookie_count DESC
            """)
            
            results = cursor.fetchall()
            conn.close()
            
            return {
                'total_count': sum(row[1] for row in results),
                'domains': [{'domain': row[0], 'count': row[1]} for row in results[:20]]
            }
        
        except Exception as e:
            self.logger.error(f"Erro ao analisar cookies: {e}")
            return {'count': 0, 'domains': []}
        finally:
            if temp_cookies.exists():
                temp_cookies.unlink()
    
    def get_bookmarks(self) -> List[Dict[str, Any]]:
        """Extrai bookmarks salvos"""
        if not self.bookmarks_file.exists():
            return []
        
        try:
            with open(self.bookmarks_file, 'r', encoding='utf-8') as f:
                bookmarks_data = json.load(f)
            
            bookmarks = []
            
            def extract_bookmarks(node, folder_name=""):
                if node.get('type') == 'url':
                    bookmarks.append({
                        'name': node.get('name', ''),
                        'url': node.get('url', ''),
                        'folder': folder_name,
                        'date_added': node.get('date_added', '')
                    })
                elif node.get('type') == 'folder':
                    folder_name = node.get('name', '')
                    for child in node.get('children', []):
                        extract_bookmarks(child, folder_name)
            
            # Processar todas as pastas de bookmarks
            roots = bookmarks_data.get('roots', {})
            for root_name, root_data in roots.items():
                if isinstance(root_data, dict) and 'children' in root_data:
                    for child in root_data['children']:
                        extract_bookmarks(child, root_name)
            
            return bookmarks
        
        except Exception as e:
            self.logger.error(f"Erro ao ler bookmarks: {e}")
            return []
    
    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório completo da análise do Edge"""
        if not self.check_edge_installation():
            return {'error': 'Edge não encontrado ou não instalado'}
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'edge_installation': {
                'found': True,
                'path': str(self.edge_path),
                'version': self._get_edge_version()
            },
            'browsing_history': {
                'recent_history': self.get_browsing_history(days_back=7),
                'most_visited': self.get_most_visited_sites(),
                'productivity_analysis': self.analyze_productivity_sites()
            },
            'storage_analysis': {
                'cache': self.get_cache_size(),
                'cookies': self.get_cookies_info(),
                'bookmarks_count': len(self.get_bookmarks())
            },
            'bookmarks': self.get_bookmarks()
        }
        
        return report
    
    def _get_edge_version(self) -> str:
        """Tenta obter a versão do Edge"""
        try:
            if self.preferences_file.exists():
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    prefs = json.load(f)
                    return prefs.get('extensions', {}).get('last_chrome_version', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    def clear_browsing_data(self, data_types: List[str]) -> Dict[str, bool]:
        """
        Limpa dados de navegação especificados
        data_types: ['history', 'cache', 'cookies', 'downloads']
        """
        results = {}
        
        # ATENÇÃO: Edge deve estar fechado para isso funcionar
        if 'cache' in data_types:
            results['cache'] = self._clear_cache()
        
        if 'history' in data_types:
            results['history'] = self._clear_history()
        
        if 'cookies' in data_types:
            results['cookies'] = self._clear_cookies()
        
        return results
    
    def _clear_cache(self) -> bool:
        """Limpa cache do Edge"""
        try:
            if self.cache_path.exists():
                import shutil
                shutil.rmtree(self.cache_path)
                self.cache_path.mkdir()
                return True
        except Exception as e:
            self.logger.error(f"Erro ao limpar cache: {e}")
        return False
    
    def _clear_history(self) -> bool:
        """Limpa histórico do Edge"""
        try:
            if self.history_db.exists():
                self.history_db.unlink()
                return True
        except Exception as e:
            self.logger.error(f"Erro ao limpar histórico: {e}")
        return False
    
    def _clear_cookies(self) -> bool:
        """Limpa cookies do Edge"""
        try:
            if self.cookies_db.exists():
                self.cookies_db.unlink()
                return True
        except Exception as e:
            self.logger.error(f"Erro ao limpar cookies: {e}")
        return False

if __name__ == "__main__":
    analyzer = EdgeAnalyzer()
    
    if analyzer.check_edge_installation():
        print("✓ Edge encontrado!")
        
        # Teste rápido
        history = analyzer.get_browsing_history(days_back=7)
        print(f"Histórico recente: {len(history)} entradas")
        
        most_visited = analyzer.get_most_visited_sites(10)
        print(f"Sites mais visitados: {len(most_visited)}")
        
        productivity = analyzer.analyze_productivity_sites()
        print(f"Análise de produtividade: {productivity['time_analysis']['productivity_percentage']:.1f}% produtivo")
        
        cache = analyzer.get_cache_size()
        print(f"Cache: {cache['total_size'] / (1024*1024):.1f} MB")
        
    else:
        print("✗ Edge não encontrado!")