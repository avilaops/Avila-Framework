# coding: utf-8
"""
Script: main.py
Função: Aplicação FastAPI principal
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
Descrição: API REST com interface HTMX para Windows optimization
"""

import logging
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Caminhos base do framework
APP_DIR = Path(__file__).resolve().parent
FRAMEWORK_DIR = APP_DIR.parent
PROJECT_ROOT = FRAMEWORK_DIR.parent
STATIC_DIR = FRAMEWORK_DIR / "output"
TEMPLATES_DIR = FRAMEWORK_DIR / "templates"
LOG_DIR = PROJECT_ROOT / "logs"

# Importações internas
from ..core import settings, setup_logging, init_sentry
from ..services import get_optimizer_service
from ..exporters import (
    MarkdownExporter, 
    ExcelExporter, 
    EmailExporter, 
    WhatsAppExporter
)

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Inicializar Sentry
sentry_enabled = init_sentry()
if sentry_enabled:
    logger.info("Sentry inicializado para monitoramento")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciamento do ciclo de vida da aplicação"""
    logger.info("🚀 Iniciando Windows Dev Optimizer Framework")
    
    # Inicialização
    try:
        # Verificar serviços
        optimizer = get_optimizer_service()
        logger.info("✅ Serviço de otimização inicializado")
        
        # Criar diretórios necessários
        STATIC_DIR.mkdir(exist_ok=True)
        LOG_DIR.mkdir(exist_ok=True)
        
        logger.info("📁 Diretórios criados")
        
    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
        raise
    
    yield
    
    # Limpeza
    logger.info("🛑 Finalizando Windows Dev Optimizer Framework")

# Criar aplicação FastAPI
app = FastAPI(
    title="Windows Dev Optimizer Framework",
    description="Framework para otimização de sistemas Windows para desenvolvimento",
    version="1.0.0",
    lifespan=lifespan
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Arquivos estáticos e templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Instâncias dos exportadores
md_exporter = MarkdownExporter()
excel_exporter = ExcelExporter()
email_exporter = EmailExporter()
whatsapp_exporter = WhatsAppExporter()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página inicial"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": settings.app_name,
        "app_version": settings.app_version
    })

@app.get("/health")
async def health_check():
    """Health check para monitoramento"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "timestamp": settings.timestamp
    }

# =============================================================================
# ROTAS DE ANÁLISE
# =============================================================================

@app.post("/api/analysis/system")
async def analyze_system(background_tasks: BackgroundTasks):
    """Executa análise completa do sistema"""
    try:
        optimizer = get_optimizer_service()
        
        logger.info("Iniciando análise do sistema")
        analysis_result = await optimizer.get_system_analysis()
        
        logger.info("Análise do sistema concluída")
        
        return {
            "success": True,
            "data": analysis_result,
            "message": "Análise do sistema concluída com sucesso"
        }
        
    except Exception as e:
        logger.error(f"Erro na análise do sistema: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@app.get("/api/analysis/recommendations")
async def get_recommendations():
    """Obtém recomendações de otimização"""
    try:
        optimizer = get_optimizer_service()
        
        logger.info("Gerando recomendações")
        recommendations = await optimizer.get_optimization_recommendations()
        
        return {
            "success": True,
            "data": recommendations,
            "message": "Recomendações geradas com sucesso"
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar recomendações: {e}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    """Página de análise do sistema"""
    return templates.TemplateResponse("analysis.html", {
        "request": request,
        "page_title": "Análise do Sistema"
    })

@app.get("/htmx/analysis/results")
async def htmx_analysis_results(request: Request):
    """Componente HTMX com resultados da análise"""
    try:
        optimizer = get_optimizer_service()
        analysis_result = await optimizer.get_system_analysis()
        
        return templates.TemplateResponse("components/analysis_results.html", {
            "request": request,
            "analysis": analysis_result
        })
        
    except Exception as e:
        logger.error(f"Erro HTMX análise: {e}")
        return templates.TemplateResponse("components/error.html", {
            "request": request,
            "error": str(e)
        })

# =============================================================================
# ROTAS DE OTIMIZAÇÃO
# =============================================================================

@app.post("/api/optimization/developer")
async def optimize_for_development(
    request: Request,
    background_tasks: BackgroundTasks
):
    """Executa otimização para desenvolvimento"""
    try:
        # Obter opções do corpo da requisição
        body = await request.json()
        options = body.get("options", {})
        
        optimizer = get_optimizer_service()
        
        logger.info(f"Iniciando otimização com opções: {options}")
        result = await optimizer.optimize_for_development(options)
        
        # Enviar notificação em background
        background_tasks.add_task(
            _send_optimization_notification,
            result
        )
        
        return {
            "success": True,
            "data": result,
            "message": "Otimização para desenvolvimento concluída"
        }
        
    except Exception as e:
        logger.error(f"Erro na otimização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.post("/api/optimization/remove-bloatware")
async def remove_bloatware(request: Request):
    """Remove bloatware especificado"""
    try:
        body = await request.json()
        apps_to_remove = body.get("apps", None)
        
        optimizer = get_optimizer_service()
        
        logger.info("Iniciando remoção de bloatware")
        result = await optimizer.remove_bloatware(apps_to_remove)
        
        return {
            "success": True,
            "data": result,
            "message": "Remoção de bloatware concluída"
        }
        
    except Exception as e:
        logger.error(f"Erro na remoção de bloatware: {e}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/optimization", response_class=HTMLResponse)
async def optimization_page(request: Request):
    """Página de otimização"""
    return templates.TemplateResponse("optimization.html", {
        "request": request,
        "page_title": "Otimização do Sistema"
    })

# =============================================================================
# ROTAS DE EXPORTAÇÃO
# =============================================================================

@app.post("/api/export/markdown")
async def export_markdown(request: Request):
    """Exporta relatório em Markdown"""
    try:
        body = await request.json()
        export_type = body.get("type", "analysis")  # analysis ou recommendations
        
        if export_type == "analysis":
            optimizer = get_optimizer_service()
            data = await optimizer.get_system_analysis()
            filepath = await md_exporter.export_analysis_report(data)
        else:
            optimizer = get_optimizer_service()
            data = await optimizer.get_optimization_recommendations()
            filepath = await md_exporter.export_recommendations_report(data)
        
        return {
            "success": True,
            "filepath": filepath,
            "message": "Relatório Markdown exportado com sucesso"
        }
        
    except Exception as e:
        logger.error(f"Erro ao exportar MD: {e}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.post("/api/export/excel")
async def export_excel(request: Request):
    """Exporta relatório em Excel"""
    try:
        body = await request.json()
        export_type = body.get("type", "analysis")
        
        if export_type == "analysis":
            optimizer = get_optimizer_service()
            data = await optimizer.get_system_analysis()
            filepath = await excel_exporter.export_analysis_report(data)
        else:
            optimizer = get_optimizer_service()
            data = await optimizer.get_optimization_recommendations()
            filepath = await excel_exporter.export_recommendations_report(data)
        
        return {
            "success": True,
            "filepath": filepath,
            "message": "Relatório Excel exportado com sucesso"
        }
        
    except Exception as e:
        logger.error(f"Erro ao exportar Excel: {e}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.post("/api/export/email")
async def export_email(request: Request):
    """Envia relatório por email"""
    try:
        body = await request.json()
        to_emails = body.get("emails", [])
        export_type = body.get("type", "analysis")
        attach_files = body.get("attach_files", [])
        
        if not to_emails:
            raise HTTPException(status_code=400, detail="Lista de emails é obrigatória")
        
        optimizer = get_optimizer_service()
        
        if export_type == "analysis":
            data = await optimizer.get_system_analysis()
            success = await email_exporter.send_analysis_report(
                data, to_emails, attach_files=attach_files
            )
        else:
            data = await optimizer.get_optimization_recommendations()
            success = await email_exporter.send_recommendations_report(
                data, to_emails, attach_files=attach_files
            )
        
        if success:
            return {
                "success": True,
                "message": f"Relatório enviado para {len(to_emails)} emails"
            }
        else:
            raise HTTPException(status_code=500, detail="Falha no envio do email")
        
    except Exception as e:
        logger.error(f"Erro ao enviar email: {e}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.post("/api/export/whatsapp")
async def export_whatsapp(request: Request):
    """Envia resumo via WhatsApp"""
    try:
        body = await request.json()
        phone_numbers = body.get("phones", [])
        export_type = body.get("type", "analysis")
        
        optimizer = get_optimizer_service()
        
        if export_type == "analysis":
            data = await optimizer.get_system_analysis()
            success = await whatsapp_exporter.send_analysis_summary(data, phone_numbers)
        else:
            data = await optimizer.get_optimization_recommendations()
            success = await whatsapp_exporter.send_recommendations_summary(data, phone_numbers)
        
        if success:
            return {
                "success": True,
                "message": "Resumo enviado via WhatsApp"
            }
        else:
            raise HTTPException(status_code=500, detail="Falha no envio WhatsApp")
        
    except Exception as e:
        logger.error(f"Erro ao enviar WhatsApp: {e}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/export", response_class=HTMLResponse)
async def export_page(request: Request):
    """Página de exportação"""
    return templates.TemplateResponse("export.html", {
        "request": request,
        "page_title": "Exportar Relatórios"
    })

# =============================================================================
# ROTAS DE LOGS (SERVER-SENT EVENTS)
# =============================================================================

@app.get("/api/logs/stream")
async def stream_logs():
    """Stream de logs em tempo real via Server-Sent Events"""
    
    async def event_generator():
        """Gerador de eventos de log"""
        log_file = LOG_DIR / "app.log"
        
        if not log_file.exists():
            yield f"data: {{'level': 'info', 'message': 'Log file not found', 'timestamp': '{settings.timestamp}'}}\n\n"
            return
        
        # Ler últimas linhas do log
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Enviar últimas 50 linhas
                for line in lines[-50:]:
                    if line.strip():
                        try:
                            # Tentar fazer parse do JSON log
                            import json
                            log_data = json.loads(line.strip())
                            yield f"data: {line.strip()}\n\n"
                        except:
                            # Log simples não estruturado
                            yield f"data: {{'level': 'info', 'message': '{line.strip()}', 'timestamp': '{settings.timestamp}'}}\n\n"
                        
                        await asyncio.sleep(0.1)  # Pequena pausa
                        
        except Exception as e:
            yield f"data: {{'level': 'error', 'message': 'Error reading logs: {str(e)}', 'timestamp': '{settings.timestamp}'}}\n\n"
    
    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/logs", response_class=HTMLResponse)
async def logs_page(request: Request):
    """Página de logs em tempo real"""
    return templates.TemplateResponse("logs.html", {
        "request": request,
        "page_title": "Logs do Sistema"
    })

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

async def _send_optimization_notification(result: dict):
    """Envia notificação de otimização concluída"""
    try:
        await whatsapp_exporter.send_optimization_complete(result)
        logger.info("Notificação de conclusão enviada")
    except Exception as e:
        logger.warning(f"Erro ao enviar notificação: {e}")

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "framework.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )