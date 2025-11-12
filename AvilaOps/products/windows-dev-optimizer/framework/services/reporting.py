# coding: utf-8
"""
Script: reporting.py
Função: Serviço de relatórios unificado
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
Descrição: Integração dos módulos de otimização via FastAPI
"""

import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Importar módulos existentes do Windows Dev Optimizer
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from modules.edge_analyzer import EdgeAnalyzer
from modules.program_analyzer import ProgramAnalyzer
from modules.bloatware_remover import BloatwareRemover
from modules.developer_optimizer import DeveloperOptimizer
from config.settings import Config

logger = logging.getLogger(__name__)

class WindowsOptimizerService:
    """Serviço que encapsula as funcionalidades do Windows Dev Optimizer"""
    
    def __init__(self):
        self.config = Config()
        self.edge_analyzer = EdgeAnalyzer()
        self.program_analyzer = ProgramAnalyzer()
        self.bloatware_remover = BloatwareRemover()
        self.developer_optimizer = DeveloperOptimizer()
        
    async def get_system_analysis(self) -> Dict[str, Any]:
        """Executa análise completa do sistema"""
        logger.info("Iniciando análise completa do sistema")
        
        try:
            # Execução paralela das análises que não modificam o sistema
            edge_task = asyncio.create_task(self._analyze_edge_async())
            programs_task = asyncio.create_task(self._analyze_programs_async())
            
            edge_data, programs_data = await asyncio.gather(
                edge_task, programs_task, return_exceptions=True
            )
            
            # Verificar se há exceções
            if isinstance(edge_data, Exception):
                logger.error(f"Erro na análise do Edge: {edge_data}")
                edge_data = {"error": str(edge_data)}
                
            if isinstance(programs_data, Exception):
                logger.error(f"Erro na análise de programas: {programs_data}")
                programs_data = {"error": str(programs_data)}
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "edge_analysis": edge_data,
                "programs_analysis": programs_data,
                "system_info": await self._get_system_info(),
                "bloatware_detected": await self._detect_bloatware_async()
            }
            
            logger.info("Análise completa do sistema finalizada")
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise do sistema: {e}")
            raise
    
    async def _analyze_edge_async(self) -> Dict[str, Any]:
        """Análise do Edge de forma assíncrona"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.edge_analyzer.analyze)
    
    async def _analyze_programs_async(self) -> Dict[str, Any]:
        """Análise de programas de forma assíncrona"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.program_analyzer.analyze)
    
    async def _detect_bloatware_async(self) -> List[Dict[str, Any]]:
        """Detecção de bloatware de forma assíncrona"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.bloatware_remover.detect_bloatware)
    
    async def _get_system_info(self) -> Dict[str, Any]:
        """Coleta informações básicas do sistema"""
        import platform
        import psutil
        
        try:
            return {
                "platform": platform.platform(),
                "processor": platform.processor(),
                "architecture": platform.architecture(),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "disk_usage": {
                    drive: {
                        "total_gb": round(psutil.disk_usage(drive).total / (1024**3), 2),
                        "free_gb": round(psutil.disk_usage(drive).free / (1024**3), 2),
                        "used_percent": round((psutil.disk_usage(drive).used / psutil.disk_usage(drive).total) * 100, 1)
                    }
                    for drive in ['C:\\', 'D:\\'] if Path(drive).exists()
                }
            }
        except Exception as e:
            logger.warning(f"Erro ao coletar informações do sistema: {e}")
            return {"error": str(e)}
    
    async def optimize_for_development(self, options: Dict[str, bool] = None) -> Dict[str, Any]:
        """Executa otimizações para desenvolvimento"""
        logger.info("Iniciando otimização para desenvolvimento")
        
        if options is None:
            options = {
                "enable_developer_mode": True,
                "install_chocolatey": True,
                "configure_git": True,
                "optimize_visual_studio": True,
                "configure_wsl": False
            }
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self.developer_optimizer.optimize, 
                options
            )
            
            logger.info("Otimização para desenvolvimento finalizada")
            return {
                "timestamp": datetime.now().isoformat(),
                "options_applied": options,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização para desenvolvimento: {e}")
            raise
    
    async def remove_bloatware(self, apps_to_remove: List[str] = None) -> Dict[str, Any]:
        """Remove bloatware especificado"""
        logger.info("Iniciando remoção de bloatware")
        
        try:
            loop = asyncio.get_event_loop()
            
            if apps_to_remove is None:
                # Detectar bloatware primeiro
                detected = await self._detect_bloatware_async()
                apps_to_remove = [app["name"] for app in detected if app.get("safe_to_remove", False)]
            
            result = await loop.run_in_executor(
                None,
                self.bloatware_remover.remove_apps,
                apps_to_remove
            )
            
            logger.info("Remoção de bloatware finalizada")
            return {
                "timestamp": datetime.now().isoformat(),
                "apps_removed": apps_to_remove,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Erro na remoção de bloatware: {e}")
            raise
    
    async def get_optimization_recommendations(self) -> Dict[str, Any]:
        """Gera recomendações de otimização baseadas na análise"""
        logger.info("Gerando recomendações de otimização")
        
        try:
            analysis = await self.get_system_analysis()
            
            recommendations = {
                "timestamp": datetime.now().isoformat(),
                "performance": [],
                "cleanup": [],
                "development": [],
                "security": []
            }
            
            # Análise de memória
            if "system_info" in analysis and not isinstance(analysis["system_info"], dict):
                memory_available = analysis["system_info"].get("memory_available_gb", 0)
                if memory_available < 4:
                    recommendations["performance"].append({
                        "priority": "high",
                        "category": "memory",
                        "description": "Memória disponível baixa. Considere fechar aplicações desnecessárias.",
                        "action": "close_unused_apps"
                    })
            
            # Análise de bloatware
            if "bloatware_detected" in analysis:
                bloatware_count = len(analysis["bloatware_detected"])
                if bloatware_count > 0:
                    recommendations["cleanup"].append({
                        "priority": "medium",
                        "category": "bloatware",
                        "description": f"Encontrados {bloatware_count} aplicativos de bloatware.",
                        "action": "remove_bloatware",
                        "apps": analysis["bloatware_detected"]
                    })
            
            # Análise de programas não utilizados
            if "programs_analysis" in analysis and "unused_programs" in analysis["programs_analysis"]:
                unused_count = len(analysis["programs_analysis"]["unused_programs"])
                if unused_count > 5:
                    recommendations["cleanup"].append({
                        "priority": "low",
                        "category": "unused_programs",
                        "description": f"Encontrados {unused_count} programas não utilizados recentemente.",
                        "action": "review_unused_programs"
                    })
            
            # Recomendações para desenvolvimento
            recommendations["development"].extend([
                {
                    "priority": "medium",
                    "category": "dev_tools",
                    "description": "Ativar modo desenvolvedor do Windows",
                    "action": "enable_developer_mode"
                },
                {
                    "priority": "low",
                    "category": "package_manager",
                    "description": "Instalar Chocolatey para gerenciamento de pacotes",
                    "action": "install_chocolatey"
                }
            ])
            
            logger.info("Recomendações de otimização geradas")
            return recommendations
            
        except Exception as e:
            logger.error(f"Erro ao gerar recomendações: {e}")
            raise

# Singleton global para reutilização
_optimizer_service = None

def get_optimizer_service() -> WindowsOptimizerService:
    """Retorna instância singleton do serviço"""
    global _optimizer_service
    if _optimizer_service is None:
        _optimizer_service = WindowsOptimizerService()
    return _optimizer_service