"""
ÁVILA REPORT FRAMEWORK - INTEGRAÇÃO COM AGENTES ON
==================================================
Integração com sistema de agentes especializados
"""

import yaml
import json
from pathlib import Path
from datetime import datetime
from logger import logger

class AgentReporter:
    """Sistema de relatórios integrado com agentes On"""

    def __init__(self):
        self.workspace_root = Path(r"C:\Users\nicol\OneDrive\Avila")
        self.agents_path = self.workspace_root / "AvilaOps" / "ai" / "On" / "agents"
        self.available_agents = self._load_agents()

    def _load_agents(self):
        """Carregar configuração de todos os agentes"""
        agents = {}

        if not self.agents_path.exists():
            logger.warning("Pasta de agentes On não encontrada")
            return agents

        for agent_dir in self.agents_path.iterdir():
            if agent_dir.is_dir() and agent_dir.name != "orchestrator":
                config_file = agent_dir / "config.yaml"
                if config_file.exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config = yaml.safe_load(f)
                            agents[agent_dir.name] = config
                    except Exception as e:
                        logger.error(f"Erro ao carregar agente {agent_dir.name}: {e}")

        logger.info(f"Agentes carregados: {len(agents)}")
        return agents

    def get_agent_for_report_type(self, report_type):
        """Retornar o agente mais adequado para o tipo de relatório"""
        agent_mapping = {
            "financial": "sigma",  # Financeiro
            "projects": "helix",   # DevOps/Projetos
            "performance": "lumen",  # Pesquisa e análise
            "governance": "lex",   # Compliance
            "daily": "atlas",      # Corporativo
            "weekly": "atlas",
            "monthly": "atlas",
            "commercial": "vox",   # Comercial
            "marketing": "echo",   # Comunicação
            "production": "forge"  # Produção
        }

        agent_name = agent_mapping.get(report_type, "atlas")
        return self.available_agents.get(agent_name)

    def generate_agent_context(self, agent_name, report_type):
        """Gerar contexto específico do agente para o relatório"""
        agent = self.available_agents.get(agent_name)

        if not agent:
            return {"error": "Agente não encontrado"}

        context = {
            "agent_name": agent.get('agent_name'),
            "area": agent.get('area'),
            "timestamp": datetime.now().isoformat(),
            "report_type": report_type,
            "agent_perspective": self._get_agent_perspective(agent_name, report_type)
        }

        return context

    def _get_agent_perspective(self, agent_name, report_type):
        """Obter perspectiva específica do agente"""
        perspectives = {
            "atlas": {
                "focus": "Visão estratégica corporativa",
                "metrics": ["Alinhamento estratégico", "KPIs corporativos", "Objetivos de longo prazo"],
                "tone": "Executivo e estratégico"
            },
            "sigma": {
                "focus": "Análise financeira e controladoria",
                "metrics": ["ROI", "Margem de lucro", "Fluxo de caixa", "Budget compliance"],
                "tone": "Analítico e preciso"
            },
            "helix": {
                "focus": "Performance técnica e DevOps",
                "metrics": ["Uptime", "Deploy frequency", "MTTR", "Code quality"],
                "tone": "Técnico e orientado a métricas"
            },
            "lumen": {
                "focus": "Insights baseados em dados e IA",
                "metrics": ["Padrões identificados", "Predições", "Anomalias"],
                "tone": "Analítico e exploratório"
            },
            "vox": {
                "focus": "Performance comercial e CRM",
                "metrics": ["Conversão", "Pipeline", "Customer satisfaction", "Churn"],
                "tone": "Orientado a resultados comerciais"
            },
            "lex": {
                "focus": "Compliance e riscos jurídicos",
                "metrics": ["Conformidade", "Riscos identificados", "Auditorias"],
                "tone": "Formal e baseado em normas"
            },
            "echo": {
                "focus": "Comunicação e branding",
                "metrics": ["Reach", "Engagement", "Brand awareness"],
                "tone": "Criativo e orientado a audiência"
            },
            "forge": {
                "focus": "Produtividade e manufatura",
                "metrics": ["Output", "Eficiência", "Quality control"],
                "tone": "Operacional e orientado a processos"
            }
        }

        return perspectives.get(agent_name, perspectives["atlas"])

    def enrich_report_with_agent_intelligence(self, data, report_type):
        """Enriquecer dados do relatório com inteligência do agente"""
        agent_name = list(self.get_agent_for_report_type(report_type).keys())[0] if self.get_agent_for_report_type(report_type) else "atlas"
        context = self.generate_agent_context(agent_name, report_type)
        perspective = self._get_agent_perspective(agent_name, report_type)

        # Adicionar contexto do agente ao relatório
        enriched_data = data.copy()
        enriched_data['agent_context'] = {
            "agent": context.get('agent_name'),
            "area": context.get('area'),
            "perspective": perspective.get('focus'),
            "recommended_metrics": perspective.get('metrics'),
            "analysis_tone": perspective.get('tone')
        }

        # Adicionar insights do agente
        enriched_data['agent_insights'] = self._generate_agent_insights(agent_name, data, report_type)

        return enriched_data

    def _generate_agent_insights(self, agent_name, data, report_type):
        """Gerar insights específicos do agente"""
        insights = []

        # Sigma (Financeiro) - Análise financeira
        if agent_name == "sigma" and 'metrics' in data:
            if 'receitas_total' in data:
                insights.append(f"💰 Receitas: {data['receitas_total']}")
            if 'margem' in data:
                insights.append(f"📊 Margem de Lucro: {data['margem']}")

        # Helix (DevOps) - Métricas técnicas
        elif agent_name == "helix":
            insights.append("🔧 Performance técnica monitorada")
            insights.append("⚙️ Automação e CI/CD em análise")

        # Lumen (IA/Pesquisa) - Padrões e predições
        elif agent_name == "lumen":
            insights.append("🔍 Análise de padrões em andamento")
            insights.append("📈 Predições baseadas em dados históricos")

        # Atlas (Corporativo) - Visão estratégica
        elif agent_name == "atlas":
            insights.append("🎯 Alinhamento com objetivos estratégicos")
            insights.append("📊 KPIs corporativos em monitoramento")

        # Vox (Comercial) - Performance de vendas
        elif agent_name == "vox":
            insights.append("💼 Pipeline comercial analisado")
            insights.append("📞 CRM e relacionamento em foco")

        return insights

    def save_agent_memory(self, agent_name, report_data):
        """Salvar informações do relatório na memória do agente"""
        try:
            agent = self.available_agents.get(agent_name)
            if not agent:
                return False

            memory_path = Path(agent.get('memory_path', f'../../data/{agent_name}_memory.json'))

            # Resolver caminho relativo
            if not memory_path.is_absolute():
                memory_path = self.agents_path / agent_name / memory_path

            # Carregar memória existente
            if memory_path.exists():
                with open(memory_path, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
            else:
                memory = {"reports": [], "insights": []}

            # Adicionar novo relatório
            memory_entry = {
                "timestamp": datetime.now().isoformat(),
                "report_type": report_data.get('type'),
                "summary": report_data.get('summary', '')[:200],  # Primeiros 200 chars
                "key_metrics": list(report_data.get('metrics', {}).keys())[:5]  # Top 5 métricas
            }

            memory["reports"].append(memory_entry)

            # Manter apenas últimos 50 relatórios
            memory["reports"] = memory["reports"][-50:]

            # Salvar memória atualizada
            memory_path.parent.mkdir(parents=True, exist_ok=True)
            with open(memory_path, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2, ensure_ascii=False)

            logger.success(f"Memória do agente {agent_name} atualizada")
            return True

        except Exception as e:
            logger.error(f"Erro ao salvar memória do agente: {e}")
            return False

    def get_agents_summary(self):
        """Obter resumo de todos os agentes disponíveis"""
        summary = []

        for name, config in self.available_agents.items():
            summary.append({
                "nome": config.get('agent_name'),
                "area": config.get('area'),
                "status": config.get('status'),
                "modelo": config.get('model'),
                "descricao": config.get('description')
            })

        return summary

# Instância global
agent_reporter = AgentReporter()
