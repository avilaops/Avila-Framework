#!/usr/bin/env python3
"""
Lumen Analytics para Logs do sync-center.ps1
Processa logs de sincronização e gera métricas para Prometheus/Grafana

Integração: sync-center.ps1 logs → Lumen analytics → datasets/ → Prometheus
"""

import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class SyncCenterAnalytics:
    """Analisa logs do sync-center.ps1 e extrai métricas"""
    
    def __init__(self, logs_path=None):
        if logs_path is None:
            logs_path = Path("C:/Users/nicol/OneDrive/Avila/Logs")
        self.logs_path = Path(logs_path)
        self.metrics = defaultdict(lambda: defaultdict(int))
        self.events = []
        
    def parse_log_line(self, line):
        """Parse linha de log do sync-center.ps1
        Formato: [HH:mm:ss] [LEVEL] Message
        """
        # Regex para extrair timestamp, level e mensagem
        pattern = r'\[(\d{2}:\d{2}:\d{2})\] \[(\w+)\] (.+)'
        match = re.match(pattern, line)
        
        if not match:
            return None
            
        time_str, level, message = match.groups()
        
        return {
            'time': time_str,
            'level': level,
            'message': message
        }
    
    def extract_metrics_from_message(self, message):
        """Extrai métricas específicas de mensagens"""
        metrics = {}
        
        # Detectar mudanças
        if match := re.search(r'Detectadas (\d+) mudanças', message):
            metrics['changes_detected'] = int(match.group(1))
            
        # Detectar push
        if 'Push concluído' in message:
            metrics['git_push_success'] = 1
            
        # Detectar pull
        if 'Pull concluído' in message:
            metrics['git_pull_success'] = 1
            
        # Detectar erros
        if match := re.search(r'Erro no (push|pull):', message):
            operation = match.group(1)
            metrics[f'git_{operation}_error'] = 1
            
        # Rotação de logs
        if match := re.search(r'Rotacao concluida: (\d+) logs', message):
            metrics['logs_rotated'] = int(match.group(1))
            
        # Configurações atualizadas
        if 'Configuração atualizada:' in message:
            metrics['config_updates'] = 1
            
        # Arquivo modificado
        if match := re.search(r'Arquivo modificado: (.+) \((\w+)\)', message):
            filename, change_type = match.groups()
            metrics['file_modifications'] = 1
            metrics[f'change_type_{change_type.lower()}'] = 1
            
        return metrics
    
    def analyze_log_file(self, log_file):
        """Analisa um arquivo de log completo"""
        if not log_file.exists():
            print(f"⚠️  Log não encontrado: {log_file}")
            return
            
        date_str = log_file.stem.split('_')[-1]  # sync-YYYY-MM-DD.log
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = self.parse_log_line(line.strip())
                if not parsed:
                    continue
                    
                # Contar por nível
                self.metrics[date_str]['level_' + parsed['level']] += 1
                
                # Extrair métricas da mensagem
                msg_metrics = self.extract_metrics_from_message(parsed['message'])
                for key, value in msg_metrics.items():
                    self.metrics[date_str][key] += value
                    
                # Armazenar eventos importantes
                if parsed['level'] in ['ERROR', 'WARN', 'SUCCESS']:
                    self.events.append({
                        'date': date_str,
                        'time': parsed['time'],
                        'level': parsed['level'],
                        'message': parsed['message']
                    })
    
    def analyze_all_logs(self, days=30):
        """Analisa logs dos últimos N dias"""
        print(f"🔍 Analisando logs dos últimos {days} dias...")
        
        # Buscar arquivos sync-*.log
        log_files = sorted(self.logs_path.glob("sync-*.log"))
        
        if not log_files:
            print("⚠️  Nenhum log sync-center encontrado")
            return
            
        # Filtrar por data (últimos N dias)
        cutoff_date = datetime.now() - timedelta(days=days)
        
        analyzed_count = 0
        for log_file in log_files:
            try:
                # Extrair data do nome do arquivo
                date_str = log_file.stem.split('_')[-1]
                log_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                if log_date < cutoff_date:
                    continue
                    
                self.analyze_log_file(log_file)
                analyzed_count += 1
                
            except ValueError:
                print(f"⚠️  Formato de data inválido: {log_file.name}")
                continue
        
        print(f"✅ {analyzed_count} arquivos de log analisados")
    
    def generate_summary(self):
        """Gera resumo das métricas coletadas"""
        summary = {
            'period': {
                'start': min(self.metrics.keys()) if self.metrics else None,
                'end': max(self.metrics.keys()) if self.metrics else None,
                'total_days': len(self.metrics)
            },
            'totals': defaultdict(int),
            'daily': dict(self.metrics),
            'recent_events': self.events[-20:],  # Últimos 20 eventos
            'top_issues': []
        }
        
        # Agregar totais
        for date, metrics in self.metrics.items():
            for key, value in metrics.items():
                summary['totals'][key] += value
        
        # Identificar dias com mais problemas
        error_counts = {
            date: metrics.get('level_ERROR', 0) + metrics.get('level_WARN', 0)
            for date, metrics in self.metrics.items()
        }
        
        top_error_days = sorted(
            error_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        summary['top_issues'] = [
            {'date': date, 'issues': count}
            for date, count in top_error_days if count > 0
        ]
        
        return summary
    
    def export_to_json(self, output_file):
        """Exporta métricas para JSON (datasets/)"""
        summary = self.generate_summary()
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Métricas exportadas: {output_path}")
        return summary
    
    def print_summary(self):
        """Imprime resumo no console"""
        summary = self.generate_summary()
        
        print("\n" + "=" * 60)
        print("📊 RESUMO DE MÉTRICAS - SYNC CENTER")
        print("=" * 60)
        
        period = summary['period']
        print(f"\n📅 Período: {period['start']} até {period['end']}")
        print(f"   Total de dias: {period['total_days']}")
        
        totals = summary['totals']
        print(f"\n📈 Métricas Totais:")
        print(f"   🔄 Git Pushes: {totals.get('git_push_success', 0)}")
        print(f"   📥 Git Pulls: {totals.get('git_pull_success', 0)}")
        print(f"   📝 Mudanças Detectadas: {totals.get('changes_detected', 0)}")
        print(f"   📄 Arquivos Modificados: {totals.get('file_modifications', 0)}")
        print(f"   ⚙️  Configs Atualizadas: {totals.get('config_updates', 0)}")
        
        print(f"\n📊 Por Nível:")
        print(f"   ✅ SUCCESS: {totals.get('level_SUCCESS', 0)}")
        print(f"   ℹ️  INFO: {totals.get('level_INFO', 0)}")
        print(f"   ⚠️  WARN: {totals.get('level_WARN', 0)}")
        print(f"   ❌ ERROR: {totals.get('level_ERROR', 0)}")
        
        if summary['top_issues']:
            print(f"\n🚨 Dias com Mais Problemas:")
            for issue in summary['top_issues']:
                print(f"   {issue['date']}: {issue['issues']} problemas")
        
        if summary['recent_events']:
            print(f"\n📋 Eventos Recentes:")
            for event in summary['recent_events'][-5:]:
                icon = {
                    'SUCCESS': '✅',
                    'ERROR': '❌',
                    'WARN': '⚠️',
                    'INFO': 'ℹ️'
                }.get(event['level'], '•')
                print(f"   {icon} {event['date']} {event['time']} - {event['message'][:60]}")
        
        print("\n" + "=" * 60)

def main():
    """Função principal"""
    print("🚀 SYNC CENTER ANALYTICS - LUMEN")
    print("Processando logs de sincronização...\n")
    
    # Inicializar analytics
    analytics = SyncCenterAnalytics()
    
    # Analisar logs
    analytics.analyze_all_logs(days=30)
    
    # Exibir resumo
    analytics.print_summary()
    
    # Exportar para datasets
    output_file = Path(__file__).parent.parent / "datasets" / "sync_center" / "metrics.json"
    analytics.export_to_json(output_file)
    
    print("\n✅ Analytics concluída!")
    print("📍 Próximos passos:")
    print("   1. Integrar com Prometheus (exporter)")
    print("   2. Criar dashboard Grafana")
    print("   3. Configurar alertas no Atlas")

if __name__ == "__main__":
    main()
