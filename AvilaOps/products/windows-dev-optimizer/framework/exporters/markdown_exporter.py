# coding: utf-8
"""
Script: markdown_exporter.py
Função: Exportador para formato Markdown
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
Descrição: Exportação de relatórios em formato Markdown
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)

class MarkdownExporter:
    """Exportador para formato Markdown"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    async def export_analysis_report(self, analysis_data: Dict[str, Any], filename: str = None) -> str:
        """Exporta relatório de análise em Markdown"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"windows_analysis_report_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        try:
            content = self._generate_analysis_markdown(analysis_data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Relatório exportado para: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao exportar relatório MD: {e}")
            raise
    
    def _generate_analysis_markdown(self, data: Dict[str, Any]) -> str:
        """Gera conteúdo Markdown do relatório de análise"""
        
        timestamp = data.get("timestamp", datetime.now().isoformat())
        
        content = f"""# Windows Dev Optimizer - Relatório de Análise

**Data:** {timestamp}  
**Ferramenta:** Windows Dev Optimizer Framework  
**Autor:** Avila Ops

---

## 📋 Resumo Executivo

Este relatório apresenta a análise completa do sistema Windows focada em otimização para desenvolvimento.

"""
        
        # Informações do Sistema
        if "system_info" in data and not isinstance(data["system_info"], dict) or "error" not in data.get("system_info", {}):
            content += self._add_system_info_section(data["system_info"])
        
        # Análise do Edge
        if "edge_analysis" in data and "error" not in data.get("edge_analysis", {}):
            content += self._add_edge_analysis_section(data["edge_analysis"])
        
        # Análise de Programas
        if "programs_analysis" in data and "error" not in data.get("programs_analysis", {}):
            content += self._add_programs_analysis_section(data["programs_analysis"])
        
        # Bloatware Detectado
        if "bloatware_detected" in data:
            content += self._add_bloatware_section(data["bloatware_detected"])
        
        # Rodapé
        content += self._add_footer()
        
        return content
    
    def _add_system_info_section(self, system_info: Dict[str, Any]) -> str:
        """Adiciona seção de informações do sistema"""
        
        content = """## 🖥️ Informações do Sistema

| Especificação | Valor |
|---------------|--------|
"""
        
        content += f"| **Plataforma** | {system_info.get('platform', 'N/A')} |\n"
        content += f"| **Processador** | {system_info.get('processor', 'N/A')} |\n"
        content += f"| **Arquitetura** | {system_info.get('architecture', ['N/A'])[0]} |\n"
        content += f"| **Memória Total** | {system_info.get('memory_total_gb', 'N/A')} GB |\n"
        content += f"| **Memória Disponível** | {system_info.get('memory_available_gb', 'N/A')} GB |\n"
        
        # Informações de disco
        if "disk_usage" in system_info:
            content += "\n### 💾 Uso de Disco\n\n"
            for drive, info in system_info["disk_usage"].items():
                content += f"**Drive {drive}:**\n"
                content += f"- Total: {info.get('total_gb', 'N/A')} GB\n"
                content += f"- Livre: {info.get('free_gb', 'N/A')} GB\n"
                content += f"- Usado: {info.get('used_percent', 'N/A')}%\n\n"
        
        content += "\n---\n\n"
        return content
    
    def _add_edge_analysis_section(self, edge_data: Dict[str, Any]) -> str:
        """Adiciona seção de análise do Edge"""
        
        content = """## 🌐 Análise do Microsoft Edge

### Estatísticas de Uso

"""
        
        if "history_stats" in edge_data:
            stats = edge_data["history_stats"]
            content += f"- **Total de Entradas no Histórico:** {stats.get('total_entries', 'N/A')}\n"
            content += f"- **Sites Únicos Visitados:** {stats.get('unique_sites', 'N/A')}\n"
            content += f"- **Período Analisado:** {stats.get('date_range', 'N/A')}\n\n"
        
        if "top_sites" in edge_data:
            content += "### 🔝 Sites Mais Visitados\n\n"
            content += "| Site | Visitas |\n|------|--------|\n"
            
            for site in edge_data["top_sites"][:10]:  # Top 10
                content += f"| {site.get('domain', 'N/A')} | {site.get('visit_count', 'N/A')} |\n"
            content += "\n"
        
        if "productivity_analysis" in edge_data:
            prod = edge_data["productivity_analysis"]
            content += "### 📈 Análise de Produtividade\n\n"
            content += f"- **Sites de Desenvolvimento:** {prod.get('dev_sites_percentage', 'N/A')}%\n"
            content += f"- **Sites Sociais:** {prod.get('social_sites_percentage', 'N/A')}%\n"
            content += f"- **Outros Sites:** {prod.get('other_sites_percentage', 'N/A')}%\n\n"
        
        content += "---\n\n"
        return content
    
    def _add_programs_analysis_section(self, programs_data: Dict[str, Any]) -> str:
        """Adiciona seção de análise de programas"""
        
        content = """## 📦 Análise de Programas Instalados

### Estatísticas Gerais

"""
        
        if "total_programs" in programs_data:
            content += f"- **Total de Programas:** {programs_data['total_programs']}\n"
        
        if "programs_by_size" in programs_data:
            content += f"- **Programas Analisados por Tamanho:** {len(programs_data['programs_by_size'])}\n"
        
        if "unused_programs" in programs_data:
            unused_count = len(programs_data["unused_programs"])
            content += f"- **Programas Não Utilizados:** {unused_count}\n"
        
        content += "\n"
        
        # Programas por tamanho
        if "programs_by_size" in programs_data and len(programs_data["programs_by_size"]) > 0:
            content += "### 📊 Maiores Programas (Top 10)\n\n"
            content += "| Programa | Tamanho (MB) | Última Execução |\n"
            content += "|----------|--------------|------------------|\n"
            
            for program in programs_data["programs_by_size"][:10]:
                name = program.get("display_name", "N/A")
                size = program.get("size_mb", "N/A")
                last_used = program.get("last_used", "N/A")
                content += f"| {name} | {size} | {last_used} |\n"
            content += "\n"
        
        # Programas não utilizados
        if "unused_programs" in programs_data and len(programs_data["unused_programs"]) > 0:
            content += "### ⚠️ Programas Não Utilizados Recentemente\n\n"
            content += "| Programa | Tamanho (MB) | Instalado em |\n"
            content += "|----------|--------------|---------------|\n"
            
            for program in programs_data["unused_programs"][:15]:  # Top 15
                name = program.get("display_name", "N/A")
                size = program.get("size_mb", "N/A")
                install_date = program.get("install_date", "N/A")
                content += f"| {name} | {size} | {install_date} |\n"
            content += "\n"
        
        content += "---\n\n"
        return content
    
    def _add_bloatware_section(self, bloatware_list: List[Dict[str, Any]]) -> str:
        """Adiciona seção de bloatware detectado"""
        
        content = f"""## 🗑️ Bloatware Detectado

**Total Detectado:** {len(bloatware_list)} aplicativos

"""
        
        if len(bloatware_list) > 0:
            content += "| Aplicativo | Categoria | Seguro Remover | Descrição |\n"
            content += "|------------|-----------|----------------|------------|\n"
            
            for app in bloatware_list:
                name = app.get("name", "N/A")
                category = app.get("category", "N/A")
                safe = "✅ Sim" if app.get("safe_to_remove", False) else "⚠️ Verificar"
                description = app.get("description", "N/A")
                
                content += f"| {name} | {category} | {safe} | {description} |\n"
            content += "\n"
        else:
            content += "✅ **Nenhum bloatware detectado no sistema.**\n\n"
        
        content += "---\n\n"
        return content
    
    async def export_recommendations_report(self, recommendations: Dict[str, Any], filename: str = None) -> str:
        """Exporta relatório de recomendações em Markdown"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"optimization_recommendations_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        try:
            content = self._generate_recommendations_markdown(recommendations)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Relatório de recomendações exportado para: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao exportar recomendações MD: {e}")
            raise
    
    def _generate_recommendations_markdown(self, data: Dict[str, Any]) -> str:
        """Gera conteúdo Markdown do relatório de recomendações"""
        
        timestamp = data.get("timestamp", datetime.now().isoformat())
        
        content = f"""# Windows Dev Optimizer - Recomendações de Otimização

**Data:** {timestamp}  
**Ferramenta:** Windows Dev Optimizer Framework  
**Autor:** Avila Ops

---

## 🎯 Recomendações de Otimização

Este relatório apresenta recomendações personalizadas para otimizar o sistema Windows para desenvolvimento.

"""
        
        # Performance
        if "performance" in data and len(data["performance"]) > 0:
            content += "## ⚡ Performance\n\n"
            for rec in data["performance"]:
                priority_icon = self._get_priority_icon(rec.get("priority", "low"))
                content += f"### {priority_icon} {rec.get('category', 'N/A').title()}\n\n"
                content += f"**Descrição:** {rec.get('description', 'N/A')}\n\n"
                content += f"**Ação Recomendada:** `{rec.get('action', 'N/A')}`\n\n"
                content += "---\n\n"
        
        # Limpeza
        if "cleanup" in data and len(data["cleanup"]) > 0:
            content += "## 🧹 Limpeza\n\n"
            for rec in data["cleanup"]:
                priority_icon = self._get_priority_icon(rec.get("priority", "low"))
                content += f"### {priority_icon} {rec.get('category', 'N/A').title()}\n\n"
                content += f"**Descrição:** {rec.get('description', 'N/A')}\n\n"
                content += f"**Ação Recomendada:** `{rec.get('action', 'N/A')}`\n\n"
                
                if "apps" in rec:
                    content += "**Aplicativos Identificados:**\n"
                    for app in rec["apps"][:5]:  # Limitar a 5
                        content += f"- {app.get('name', 'N/A')}\n"
                    content += "\n"
                
                content += "---\n\n"
        
        # Desenvolvimento
        if "development" in data and len(data["development"]) > 0:
            content += "## 👨‍💻 Desenvolvimento\n\n"
            for rec in data["development"]:
                priority_icon = self._get_priority_icon(rec.get("priority", "low"))
                content += f"### {priority_icon} {rec.get('category', 'N/A').title()}\n\n"
                content += f"**Descrição:** {rec.get('description', 'N/A')}\n\n"
                content += f"**Ação Recomendada:** `{rec.get('action', 'N/A')}`\n\n"
                content += "---\n\n"
        
        # Segurança
        if "security" in data and len(data["security"]) > 0:
            content += "## 🔒 Segurança\n\n"
            for rec in data["security"]:
                priority_icon = self._get_priority_icon(rec.get("priority", "low"))
                content += f"### {priority_icon} {rec.get('category', 'N/A').title()}\n\n"
                content += f"**Descrição:** {rec.get('description', 'N/A')}\n\n"
                content += f"**Ação Recomendada:** `{rec.get('action', 'N/A')}`\n\n"
                content += "---\n\n"
        
        content += self._add_footer()
        
        return content
    
    def _get_priority_icon(self, priority: str) -> str:
        """Retorna ícone baseado na prioridade"""
        icons = {
            "high": "🔴",
            "medium": "🟡", 
            "low": "🟢"
        }
        return icons.get(priority.lower(), "🔵")
    
    def _add_footer(self) -> str:
        """Adiciona rodapé padrão"""
        return f"""
---

## 📝 Informações Adicionais

- **Ferramenta:** Windows Dev Optimizer Framework
- **Versão:** 1.0.0
- **Desenvolvido por:** Nicolas Avila - Avila Ops
- **Data de Geração:** {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}

### 📞 Suporte

Para dúvidas ou suporte:
- **Email:** nicolas@avila.inc
- **WhatsApp:** +55 17 99781-1471

---

*Relatório gerado automaticamente pelo Windows Dev Optimizer Framework*
"""