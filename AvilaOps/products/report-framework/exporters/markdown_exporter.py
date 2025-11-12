"""
ÁVILA REPORT FRAMEWORK - EXPORTADOR MARKDOWN
============================================
Gerador de relatórios em formato Markdown
Integrado com Archivus (governança) e Agentes On
"""

import os
from datetime import datetime
from config import get_timestamp, REPORT_TYPES
from logger import log_export_action
from archivus_integration import archivus_integration
from agents_integration import agent_reporter

class MarkdownExporter:
    """Exportador para formato Markdown"""

    def __init__(self):
        self.extension = ".md"

    def export(self, data, report_type, filename=None):
        """Exportar dados para Markdown"""
        try:
            log_export_action("markdown", "arquivo", "started")

            # ENRIQUECER COM INTELIGÊNCIA DO AGENTE
            enriched_data = agent_reporter.enrich_report_with_agent_intelligence(data, report_type)

            if not filename:
                timestamp = get_timestamp("filename")
                filename = f"avila_report_{report_type}_{timestamp}{self.extension}"

            content = self._generate_markdown_content(enriched_data, report_type)

            # SALVAR EM PASTA OFICIAL DO ARCHIVUS
            report_category = self._map_to_archivus_category(report_type)
            filepath = archivus_integration.save_to_official_location(
                filename,
                content,
                report_category
            )

            # REGISTRAR COM ARCHIVUS PARA GOVERNANÇA
            archivus_integration.register_with_archivus(
                filepath,
                {
                    'type': report_type,
                    'category': report_category,
                    'format': 'markdown',
                    'timestamp': get_timestamp("br")
                }
            )

            # SALVAR NA MEMÓRIA DO AGENTE
            agent_name = list(agent_reporter.get_agent_for_report_type(report_type).keys())[0] if agent_reporter.get_agent_for_report_type(report_type) else "atlas"
            agent_reporter.save_agent_memory(agent_name, enriched_data)

            log_export_action("markdown", filepath, "completed")
            return filepath

        except Exception as e:
            log_export_action("markdown", "arquivo", "error")
            raise e

    def _map_to_archivus_category(self, report_type):
        """Mapear tipo de relatório para categoria Archivus"""
        mapping = {
            "financial": "Analises",
            "governance": "Auditorias",
            "performance": "Performance",
            "projects": "Analises",
            "daily": "Conversas",
            "weekly": "Analises",
            "monthly": "Analises",
            "commercial": "Analises",
            "custom": "Analises"
        }
        return mapping.get(report_type, "Analises")

    def _generate_markdown_content(self, data, report_type):
        """Gerar conteúdo Markdown"""
        report_info = REPORT_TYPES.get(report_type, REPORT_TYPES["custom"])
        timestamp = get_timestamp("br")

        # OBTER CONTEXTO DO AGENTE
        agent_context = data.get('agent_context', {})
        agent_insights = data.get('agent_insights', [])

        content = f"""# {report_info['icon']} {report_info['name']}

**Documento:** Relatório {report_type.title()}
**Data/Hora:** {timestamp}
**Gerado por:** Ávila Report Framework
**Frequência:** {report_info['frequency']}

---

## 🤖 Análise por Agente Especializado

**Agente:** {agent_context.get('agent', 'N/A')}
**Área:** {agent_context.get('area', 'N/A')}
**Perspectiva:** {agent_context.get('perspective', 'N/A')}
**Tom de Análise:** {agent_context.get('analysis_tone', 'N/A')}

### 💡 Insights do Agente

"""
        # Adicionar insights do agente
        for insight in agent_insights:
            content += f"{insight}\n"

        content += f"""

---

## 📊 Resumo Executivo

{data.get('summary', 'Resumo não disponível')}

## 📈 Métricas Principais

"""

        # Adicionar métricas se disponíveis
        if 'metrics' in data:
            for metric_name, metric_value in data['metrics'].items():
                content += f"- **{metric_name}:** {metric_value}\n"

        # Adicionar métricas recomendadas pelo agente
        if agent_context.get('recommended_metrics'):
            content += f"\n### 🎯 Métricas Recomendadas por {agent_context.get('agent', 'Agente')}\n\n"
            for metric in agent_context.get('recommended_metrics', []):
                content += f"- {metric}\n"

        content += f"""

## 📋 Detalhes

{data.get('details', 'Detalhes não disponíveis')}

"""

        # Adicionar seções específicas por tipo de relatório
        if report_type == "financial":
            content += self._add_financial_section(data)
        elif report_type == "projects":
            content += self._add_projects_section(data)
        elif report_type == "performance":
            content += self._add_performance_section(data)
        elif report_type == "governance":
            content += self._add_governance_section(data)

        # Rodapé
        content += f"""
---

## 📋 Informações do Relatório

- **Tipo:** {report_info['name']}
- **Data de Geração:** {timestamp}
- **Sistema:** Ávila Report Framework v1.0
- **Responsável:** AvilaOps Team
- **Agente Responsável:** {agent_context.get('agent', 'N/A')}

## � Governança e Integridade (Archivus)

- **Localização Oficial:** Docs/Relatorios/{self._map_to_archivus_category(report_type)}/
- **Hash SHA256:** [Calculado automaticamente pelo Archivus]
- **Status de Compliance:** Conforme
- **Backup:** Automático (retenção conforme política Archivus)

## �🔗 Links Úteis

- [Dashboard Principal](../../Docs/Dashboard-Principal.md)
- [Procedimentos de Governança](../governance/)
- [Repositório GitHub](https://github.com/avilaops/Avila-Framework)

---

*Relatório gerado automaticamente pelo Ávila Report Framework*
*Integrado com Archivus (governança) e Sistema de Agentes On*
"""

        return content

    def _add_financial_section(self, data):
        """Seção específica para relatórios financeiros"""
        return """
## 💰 Análise Financeira

### Receitas
- **Total:** {receitas_total}
- **Variação:** {receitas_variacao}

### Despesas
- **Total:** {despesas_total}
- **Variação:** {despesas_variacao}

### Resultado
- **Lucro/Prejuízo:** {resultado}
- **Margem:** {margem}

""".format(
            receitas_total=data.get('receitas_total', 'N/A'),
            receitas_variacao=data.get('receitas_variacao', 'N/A'),
            despesas_total=data.get('despesas_total', 'N/A'),
            despesas_variacao=data.get('despesas_variacao', 'N/A'),
            resultado=data.get('resultado', 'N/A'),
            margem=data.get('margem', 'N/A')
        )

    def _add_projects_section(self, data):
        """Seção específica para relatórios de projetos"""
        return """
## 🏗️ Status dos Projetos

### Em Andamento
- **Quantidade:** {projetos_andamento}
- **Progresso Médio:** {progresso_medio}

### Concluídos
- **Quantidade:** {projetos_concluidos}
- **Taxa de Sucesso:** {taxa_sucesso}

### Atrasados
- **Quantidade:** {projetos_atrasados}
- **Impacto:** {impacto_atraso}

""".format(
            projetos_andamento=data.get('projetos_andamento', 'N/A'),
            progresso_medio=data.get('progresso_medio', 'N/A'),
            projetos_concluidos=data.get('projetos_concluidos', 'N/A'),
            taxa_sucesso=data.get('taxa_sucesso', 'N/A'),
            projetos_atrasados=data.get('projetos_atrasados', 'N/A'),
            impacto_atraso=data.get('impacto_atraso', 'N/A')
        )

    def _add_performance_section(self, data):
        """Seção específica para relatórios de performance"""
        return """
## 🚀 Indicadores de Performance

### Eficiência
- **Score Geral:** {score_eficiencia}
- **Tendência:** {tendencia_eficiencia}

### Qualidade
- **Score:** {score_qualidade}
- **Incidentes:** {incidentes}

### Produtividade
- **Score:** {score_produtividade}
- **Variação:** {variacao_produtividade}

""".format(
            score_eficiencia=data.get('score_eficiencia', 'N/A'),
            tendencia_eficiencia=data.get('tendencia_eficiencia', 'N/A'),
            score_qualidade=data.get('score_qualidade', 'N/A'),
            incidentes=data.get('incidentes', 'N/A'),
            score_produtividade=data.get('score_produtividade', 'N/A'),
            variacao_produtividade=data.get('variacao_produtividade', 'N/A')
        )

    def _add_governance_section(self, data):
        """Seção específica para relatórios de governança"""
        return """
## 🏛️ Compliance e Governança

### Conformidade
- **Score:** {score_compliance}
- **Não Conformidades:** {nao_conformidades}

### Auditoria
- **Última Auditoria:** {ultima_auditoria}
- **Status:** {status_auditoria}

### Riscos
- **Alto:** {riscos_alto}
- **Médio:** {riscos_medio}
- **Baixo:** {riscos_baixo}

""".format(
            score_compliance=data.get('score_compliance', 'N/A'),
            nao_conformidades=data.get('nao_conformidades', 'N/A'),
            ultima_auditoria=data.get('ultima_auditoria', 'N/A'),
            status_auditoria=data.get('status_auditoria', 'N/A'),
            riscos_alto=data.get('riscos_alto', 'N/A'),
            riscos_medio=data.get('riscos_medio', 'N/A'),
            riscos_baixo=data.get('riscos_baixo', 'N/A')
        )
