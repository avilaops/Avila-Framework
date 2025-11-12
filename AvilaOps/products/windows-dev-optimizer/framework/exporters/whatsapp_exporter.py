# coding: utf-8
"""
Script: whatsapp_exporter.py
Função: Exportador via WhatsApp
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
Descrição: Envio de relatórios via WhatsApp
"""

import logging
import aiohttp
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..core.config import settings

logger = logging.getLogger(__name__)

class WhatsAppExporter:
    """Exportador via WhatsApp"""
    
    def __init__(self):
        self.whatsapp_token = settings.whatsapp_token
        self.whatsapp_url = settings.whatsapp_url
        self.whatsapp_phone = settings.whatsapp_phone
    
    async def send_analysis_summary(
        self, 
        analysis_data: Dict[str, Any], 
        phone_numbers: List[str] = None
    ) -> bool:
        """Envia resumo da análise via WhatsApp"""
        
        if phone_numbers is None:
            phone_numbers = [self.whatsapp_phone] if self.whatsapp_phone else []
        
        if not phone_numbers:
            logger.error("Nenhum número de telefone configurado")
            return False
        
        try:
            # Gerar mensagem de resumo
            message = self._generate_analysis_summary(analysis_data)
            
            # Enviar para todos os números
            success_count = 0
            for phone in phone_numbers:
                if await self._send_whatsapp_message(phone, message):
                    success_count += 1
            
            if success_count > 0:
                logger.info(f"Resumo de análise enviado para {success_count} números")
            
            return success_count == len(phone_numbers)
            
        except Exception as e:
            logger.error(f"Erro ao enviar resumo via WhatsApp: {e}")
            return False
    
    async def send_recommendations_summary(
        self, 
        recommendations: Dict[str, Any], 
        phone_numbers: List[str] = None
    ) -> bool:
        """Envia resumo das recomendações via WhatsApp"""
        
        if phone_numbers is None:
            phone_numbers = [self.whatsapp_phone] if self.whatsapp_phone else []
        
        if not phone_numbers:
            logger.error("Nenhum número de telefone configurado")
            return False
        
        try:
            # Gerar mensagem de resumo
            message = self._generate_recommendations_summary(recommendations)
            
            # Enviar para todos os números
            success_count = 0
            for phone in phone_numbers:
                if await self._send_whatsapp_message(phone, message):
                    success_count += 1
            
            if success_count > 0:
                logger.info(f"Resumo de recomendações enviado para {success_count} números")
            
            return success_count == len(phone_numbers)
            
        except Exception as e:
            logger.error(f"Erro ao enviar recomendações via WhatsApp: {e}")
            return False
    
    async def send_optimization_complete(
        self, 
        results: Dict[str, Any], 
        phone_numbers: List[str] = None
    ) -> bool:
        """Envia notificação de otimização concluída"""
        
        if phone_numbers is None:
            phone_numbers = [self.whatsapp_phone] if self.whatsapp_phone else []
        
        try:
            message = self._generate_optimization_complete_message(results)
            
            success_count = 0
            for phone in phone_numbers:
                if await self._send_whatsapp_message(phone, message):
                    success_count += 1
            
            return success_count == len(phone_numbers)
            
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de conclusão: {e}")
            return False
    
    async def _send_whatsapp_message(self, phone_number: str, message: str) -> bool:
        """Envia mensagem via API do WhatsApp"""
        
        if not self.whatsapp_token or not self.whatsapp_url:
            logger.warning("Configurações do WhatsApp não encontradas")
            return False
        
        try:
            # Formatação do número
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number.replace('-', '').replace(' ', '')
            
            # Payload para API
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.whatsapp_token}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.whatsapp_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        logger.info(f"Mensagem WhatsApp enviada para {phone_number}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"Erro na API WhatsApp: {response.status} - {error_text}")
                        return False
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem WhatsApp para {phone_number}: {e}")
            return False
    
    def _generate_analysis_summary(self, analysis_data: Dict[str, Any]) -> str:
        """Gera mensagem resumida da análise"""
        
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        message = f"""🖥️ *Windows Dev Optimizer*
📊 *Análise do Sistema Concluída*

🕐 *Data:* {timestamp}

📋 *RESUMO:*
"""
        
        # Sistema
        if "system_info" in analysis_data and "error" not in analysis_data.get("system_info", {}):
            sys_info = analysis_data["system_info"]
            memory_total = sys_info.get("memory_total_gb", "N/A")
            memory_available = sys_info.get("memory_available_gb", "N/A")
            
            message += f"""
💾 *Memória:* {memory_available}GB/{memory_total}GB disponível"""
        
        # Programas
        if "programs_analysis" in analysis_data and "error" not in analysis_data.get("programs_analysis", {}):
            prog_analysis = analysis_data["programs_analysis"]
            total_programs = prog_analysis.get("total_programs", "N/A")
            message += f"""
📦 *Programas:* {total_programs} instalados"""
            
            if "unused_programs" in prog_analysis:
                unused_count = len(prog_analysis["unused_programs"])
                message += f"""
⚠️ *Não utilizados:* {unused_count} programas"""
        
        # Bloatware
        if "bloatware_detected" in analysis_data:
            bloatware_count = len(analysis_data["bloatware_detected"])
            if bloatware_count > 0:
                message += f"""
🗑️ *Bloatware:* {bloatware_count} detectados"""
            else:
                message += f"""
✅ *Bloatware:* Nenhum detectado"""
        
        # Edge
        if "edge_analysis" in analysis_data and "history_stats" in analysis_data["edge_analysis"]:
            edge_stats = analysis_data["edge_analysis"]["history_stats"]
            unique_sites = edge_stats.get("unique_sites", "N/A")
            message += f"""
🌐 *Edge:* {unique_sites} sites únicos visitados"""
        
        message += f"""

📱 *Relatórios completos disponíveis via email ou download.*

---
*Avila Ops - Windows Optimization*
📧 nicolas@avila.inc
📱 +55 17 99781-1471"""
        
        return message
    
    def _generate_recommendations_summary(self, recommendations: Dict[str, Any]) -> str:
        """Gera mensagem resumida das recomendações"""
        
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        message = f"""🎯 *Windows Dev Optimizer*
💡 *Recomendações de Otimização*

🕐 *Data:* {timestamp}

🚀 *PRIORIDADES:*
"""
        
        # Contar por prioridade
        high_count = 0
        medium_count = 0
        low_count = 0
        
        for category in ["performance", "cleanup", "development", "security"]:
            if category in recommendations:
                for rec in recommendations[category]:
                    priority = rec.get("priority", "low").lower()
                    if priority == "high":
                        high_count += 1
                    elif priority == "medium":
                        medium_count += 1
                    else:
                        low_count += 1
        
        if high_count > 0:
            message += f"""
🔴 *ALTA:* {high_count} recomendações críticas"""
        
        if medium_count > 0:
            message += f"""
🟡 *MÉDIA:* {medium_count} recomendações importantes"""
        
        if low_count > 0:
            message += f"""
🟢 *BAIXA:* {low_count} melhorias opcionais"""
        
        message += f"""

📋 *CATEGORIAS:*"""
        
        # Performance
        if "performance" in recommendations and len(recommendations["performance"]) > 0:
            message += f"""
⚡ *Performance:* {len(recommendations["performance"])} itens"""
        
        # Cleanup
        if "cleanup" in recommendations and len(recommendations["cleanup"]) > 0:
            message += f"""
🧹 *Limpeza:* {len(recommendations["cleanup"])} itens"""
        
        # Development
        if "development" in recommendations and len(recommendations["development"]) > 0:
            message += f"""
👨‍💻 *Desenvolvimento:* {len(recommendations["development"])} itens"""
        
        # Security
        if "security" in recommendations and len(recommendations["security"]) > 0:
            message += f"""
🔒 *Segurança:* {len(recommendations["security"])} itens"""
        
        message += f"""

📄 *Relatório detalhado com instruções completas disponível.*

---
*Avila Ops - Windows Optimization*
📧 nicolas@avila.inc
📱 +55 17 99781-1471"""
        
        return message
    
    def _generate_optimization_complete_message(self, results: Dict[str, Any]) -> str:
        """Gera mensagem de otimização concluída"""
        
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        message = f"""✅ *Windows Dev Optimizer*
🎉 *Otimização Concluída!*

🕐 *Finalizada em:* {timestamp}

📊 *RESULTADOS:*
"""
        
        # Processar resultados
        if "options_applied" in results:
            options = results["options_applied"]
            message += f"""
⚙️ *Configurações aplicadas:*"""
            
            if options.get("enable_developer_mode"):
                message += f"""
✅ Modo desenvolvedor ativado"""
            
            if options.get("install_chocolatey"):
                message += f"""
✅ Chocolatey instalado"""
            
            if options.get("configure_git"):
                message += f"""
✅ Git configurado"""
            
            if options.get("optimize_visual_studio"):
                message += f"""
✅ Visual Studio otimizado"""
        
        if "apps_removed" in results and len(results["apps_removed"]) > 0:
            message += f"""

🗑️ *Bloatware removido:*
📦 {len(results["apps_removed"])} aplicativos removidos"""
        
        message += f"""

🚀 *Sistema otimizado para desenvolvimento!*

💡 *Próximos passos:*
• Reiniciar o computador para aplicar todas as mudanças
• Verificar se todos os programas necessários estão funcionando
• Configurar ambientes de desenvolvimento específicos

---
*Avila Ops - Windows Optimization*
📧 nicolas@avila.inc
📱 +55 17 99781-1471"""
        
        return message
    
    async def send_file(
        self, 
        phone_number: str, 
        file_path: str, 
        caption: str = None
    ) -> bool:
        """Envia arquivo via WhatsApp (se suportado pela API)"""
        
        # Nota: Esta funcionalidade depende da API específica do WhatsApp utilizada
        # Algumas APIs não suportam envio de arquivos
        
        logger.info(f"Funcionalidade de envio de arquivo não implementada para: {file_path}")
        
        # Alternativa: enviar mensagem informando sobre o arquivo
        if caption:
            fallback_message = f"""📄 *Arquivo Disponível*

{caption}

💡 *Para acessar:* Solicite o arquivo por email ou acesse o sistema web.

---
*Avila Ops - Windows Optimization*"""
            
            return await self._send_whatsapp_message(phone_number, fallback_message)
        
        return False