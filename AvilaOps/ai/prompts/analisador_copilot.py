"""
Script de Análise de Dados do Copilot para Personalização Setorial
Analisa os dados de chat replay para identificar padrões e oportunidades de melhoria
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import re
from collections import Counter, defaultdict

class CopilotAnalyzer:
    def __init__(self, data_file: str):
        """Inicializa o analisador com dados do arquivo JSON"""
        with open(data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.prompts = self.data['prompts']
        
    def extrair_metricas_performance(self) -> Dict[str, Any]:
        """Extrai métricas de performance dos dados"""
        metricas = {
            'tempo_resposta_total': [],
            'tempo_primeiro_token': [],
            'uso_tokens_prompt': [],
            'uso_tokens_completion': [],
            'tokens_cached': [],
            'duracao_total': []
        }
        
        for prompt in self.prompts:
            for log in prompt.get('logs', []):
                if log.get('metadata'):
                    meta = log['metadata']
                    
                    # Performance timing
                    if 'timeToFirstToken' in meta:
                        metricas['tempo_primeiro_token'].append(meta['timeToFirstToken'])
                    
                    if 'duration' in meta:
                        metricas['duracao_total'].append(meta['duration'])
                    
                    # Usage tokens
                    if 'usage' in meta:
                        usage = meta['usage']
                        metricas['uso_tokens_prompt'].append(usage.get('prompt_tokens', 0))
                        metricas['uso_tokens_completion'].append(usage.get('completion_tokens', 0))
                        
                        # Cache efficiency
                        cached = usage.get('prompt_tokens_details', {}).get('cached_tokens', 0)
                        metricas['tokens_cached'].append(cached)
        
        # Calcular estatísticas
        stats = {}
        for key, values in metricas.items():
            if values:
                stats[key] = {
                    'media': sum(values) / len(values),
                    'mediana': sorted(values)[len(values)//2],
                    'min': min(values),
                    'max': max(values),
                    'total': len(values)
                }
        
        return stats
    
    def classificar_prompts_por_setor(self) -> Dict[str, List[str]]:
        """Classifica prompts por possível setor baseado em palavras-chave"""
        
        # Definir vocabulário setorial
        vocabularios = {
            'tecnologia': [
                'código', 'API', 'função', 'desenvolvimento', 'debug', 'deploy', 
                'aplicação', 'sistema', 'software', 'programação', 'script',
                'dados', 'algoritmo', 'database', 'servidor'
            ],
            'financeiro': [
                'análise', 'ROI', 'investimento', 'custos', 'receita', 'lucro',
                'orçamento', 'finanças', 'contabilidade', 'auditoria', 'compliance',
                'relatório financeiro', 'balanço'
            ],
            'operacional': [
                'processo', 'operação', 'otimização', 'eficiência', 'produtividade',
                'workflow', 'automatização', 'melhoria', 'procedimento', 'gestão',
                'qualidade', 'performance', 'monitoramento'
            ],
            'marketing': [
                'campanha', 'cliente', 'produto', 'vendas', 'marketing', 'branding',
                'comunicação', 'estratégia', 'mercado', 'público', 'conteúdo'
            ],
            'juridico': [
                'contrato', 'legal', 'compliance', 'regulamentação', 'lei',
                'jurídico', 'auditoria', 'governança', 'política'
            ]
        }
        
        classificacao = defaultdict(list)
        
        for prompt in self.prompts:
            texto = prompt['prompt'].lower()
            pontuacao_setor = defaultdict(int)
            
            # Pontuar por setor baseado em palavras-chave
            for setor, palavras in vocabularios.items():
                for palavra in palavras:
                    if palavra in texto:
                        pontuacao_setor[setor] += 1
            
            # Classificar no setor com maior pontuação
            if pontuacao_setor:
                setor_provavel = max(pontuacao_setor.keys(), key=lambda k: pontuacao_setor[k])
                classificacao[setor_provavel].append(texto)
            else:
                classificacao['geral'].append(texto)
        
        return dict(classificacao)
    
    def analisar_ferramentas_utilizadas(self) -> Dict[str, Any]:
        """Analisa quais ferramentas são mais utilizadas"""
        tools_counter = Counter()
        tools_por_prompt = defaultdict(list)
        
        for i, prompt in enumerate(self.prompts):
            for log in prompt.get('logs', []):
                if log.get('metadata', {}).get('tools'):
                    tools = log['metadata']['tools']
                    for tool in tools:
                        tool_name = tool['function']['name']
                        tools_counter[tool_name] += 1
                        tools_por_prompt[i].append(tool_name)
        
        return {
            'ferramentas_mais_usadas': tools_counter.most_common(10),
            'total_ferramentas_disponiveis': len(set(tools_counter.keys())),
            'uso_por_prompt': dict(tools_por_prompt)
        }
    
    def analisar_padroes_temporais(self) -> Dict[str, Any]:
        """Analisa padrões temporais de uso"""
        timestamps = []
        intervalos = []
        
        for prompt in self.prompts:
            for log in prompt.get('logs', []):
                if log.get('metadata', {}).get('startTime'):
                    timestamp = datetime.fromisoformat(
                        log['metadata']['startTime'].replace('Z', '+00:00')
                    )
                    timestamps.append(timestamp)
        
        if len(timestamps) > 1:
            timestamps.sort()
            for i in range(1, len(timestamps)):
                intervalo = (timestamps[i] - timestamps[i-1]).total_seconds()
                intervalos.append(intervalo)
        
        return {
            'primeiro_uso': timestamps[0] if timestamps else None,
            'ultimo_uso': timestamps[-1] if timestamps else None,
            'total_sessoes': len(timestamps),
            'intervalo_medio_segundos': sum(intervalos) / len(intervalos) if intervalos else 0,
            'uso_por_hora': self._agrupar_por_hora(timestamps)
        }
    
    def _agrupar_por_hora(self, timestamps: List[datetime]) -> Dict[int, int]:
        """Agrupa uso por hora do dia"""
        uso_por_hora = defaultdict(int)
        for ts in timestamps:
            uso_por_hora[ts.hour] += 1
        return dict(uso_por_hora)
    
    def gerar_relatorio_completo(self) -> Dict[str, Any]:
        """Gera relatório completo de análise"""
        return {
            'resumo_geral': {
                'total_prompts': self.data['totalPrompts'],
                'total_logs': self.data['totalLogEntries'],
                'data_exportacao': self.data['exportedAt']
            },
            'metricas_performance': self.extrair_metricas_performance(),
            'classificacao_setorial': self.classificar_prompts_por_setor(),
            'analise_ferramentas': self.analisar_ferramentas_utilizadas(),
            'padroes_temporais': self.analisar_padroes_temporais()
        }
    
    def gerar_recomendacoes(self) -> List[str]:
        """Gera recomendações baseadas na análise"""
        relatorio = self.gerar_relatorio_completo()
        recomendacoes = []
        
        # Análise de performance
        perf = relatorio['metricas_performance']
        if 'tempo_primeiro_token' in perf:
            tempo_medio = perf['tempo_primeiro_token']['media']
            if tempo_medio > 3000:  # > 3 segundos
                recomendacoes.append(
                    f"⚡ PERFORMANCE: Tempo médio de resposta alto ({tempo_medio:.0f}ms). "
                    "Considere otimizar cache ou reduzir complexidade dos prompts."
                )
        
        # Análise setorial
        setores = relatorio['classificacao_setorial']
        setor_dominante = max(setores.keys(), key=lambda k: len(setores[k]))
        recomendacoes.append(
            f"🎯 PERSONALIZAÇÃO: Setor predominante é '{setor_dominante}'. "
            "Considere criar templates específicos para este domínio."
        )
        
        # Análise de ferramentas
        tools = relatorio['analise_ferramentas']
        if tools['ferramentas_mais_usadas']:
            tool_top = tools['ferramentas_mais_usadas'][0][0]
            recomendacoes.append(
                f"🔧 FERRAMENTAS: '{tool_top}' é a ferramenta mais usada. "
                "Otimize sua performance e considere criar shortcuts."
            )
        
        # Análise temporal
        temporal = relatorio['padroes_temporais']
        if temporal['uso_por_hora']:
            hora_pico = max(temporal['uso_por_hora'].keys(), 
                           key=lambda k: temporal['uso_por_hora'][k])
            recomendacoes.append(
                f"⏰ TEMPORAL: Pico de uso às {hora_pico}h. "
                "Considere recursos adicionais neste horário."
            )
        
        return recomendacoes

def main():
    """Função principal para executar a análise"""
    
    # Caminho para o arquivo de dados
    data_file = r"c:\Users\nicol\OneDrive\Avila\AvilaOps\ai\prompts\copilot_all_prompts_2025-11-10T14-14-46.chatreplay.json"
    
    try:
        # Inicializar analisador
        analyzer = CopilotAnalyzer(data_file)
        
        # Gerar análise completa
        relatorio = analyzer.gerar_relatorio_completo()
        
        # Gerar recomendações
        recomendacoes = analyzer.gerar_recomendacoes()
        
        # Salvar relatório
        with open('relatorio_analise_copilot.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
        
        # Imprimir resumo
        print("=" * 60)
        print("RELATÓRIO DE ANÁLISE DO COPILOT")
        print("=" * 60)
        print(f"Total de Prompts: {relatorio['resumo_geral']['total_prompts']}")
        print(f"Total de Logs: {relatorio['resumo_geral']['total_logs']}")
        print()
        
        print("RECOMENDAÇÕES:")
        print("-" * 40)
        for i, rec in enumerate(recomendacoes, 1):
            print(f"{i}. {rec}")
        print()
        
        print("CLASSIFICAÇÃO SETORIAL:")
        print("-" * 40)
        for setor, prompts in relatorio['classificacao_setorial'].items():
            print(f"{setor.upper()}: {len(prompts)} prompts")
        
        print("\nRelatório completo salvo em 'relatorio_analise_copilot.json'")
        
    except Exception as e:
        print(f"Erro na análise: {e}")
        print("Verifique se o arquivo de dados existe e está no formato correto.")

if __name__ == "__main__":
    main()