#!/usr/bin/env python3
"""
ON PLATFORM - REST API
FastAPI + WebSocket + Prometheus metrics

Endpoints:
- POST /api/v1/users/enroll
- POST /api/v1/users/{user_id}/steps
- GET /api/v1/users/{user_id}/status
- GET /api/v1/analytics/cohort
- WebSocket /ws/events (real-time event stream)
- GET /metrics (Prometheus)
- GET /health
"""

import sys
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, EmailStr
import uvicorn

# Prometheus metrics desabilitado temporariamente (evitar conflitos)
PROMETHEUS_AVAILABLE = False

# Import ON Platform
sys.path.insert(0, str(Path(__file__).parent.parent))
from on_platform import ONPlatform, TenantContext

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class EnrollUserRequest(BaseModel):
    email: EmailStr
    company_id: str
    metadata: Dict[str, Any] = {}


class CompleteStepRequest(BaseModel):
    step_id: str
    step_number: int
    metadata: Dict[str, Any] = {}


class UserStatusResponse(BaseModel):
    user_id: str
    email: str | None
    status: str
    current_step: int
    completed_steps: int
    ttv_days: int | None
    engagement_score: float
    features_activated: List[str]
    support_tickets: int
    at_risk: bool


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="ON Platform API",
    description="Enterprise Onboarding SaaS - Powered by Ávila Framework",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: configurar domains específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
platform: ONPlatform | None = None
active_websockets: List[WebSocket] = []

# ============================================================================
# STARTUP / SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Inicializa ON Platform"""
    global platform
    
    print("\n🚀 Starting ON Platform API...")
    
    platform = ONPlatform()
    await platform.start()
    
    # Default tenant (multi-tenancy via header em produção)
    platform.framework.tenant_provider.set_context(TenantContext(
        tenant_id="default",
        tenant_name="Default Tenant",
        subscription_tier="enterprise"
    ))
    
    print("✅ API Ready!\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Graceful shutdown"""
    global platform
    
    print("\n🛑 Shutting down ON Platform API...")
    
    # Fechar WebSockets
    for ws in active_websockets:
        try:
            await ws.close()
        except:
            pass
    
    # Shutdown framework
    if platform:
        await platform.framework.shutdown()
    
    print("✅ Shutdown complete\n")


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

async def get_platform() -> ONPlatform:
    """DI: Retorna instância da plataforma"""
    if not platform:
        raise HTTPException(status_code=503, detail="Platform not initialized")
    return platform


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/api/v1/users/enroll", status_code=201)
async def enroll_user(
    request: EnrollUserRequest,
    platform: ONPlatform = Depends(get_platform)
):
    """
    Cadastra novo usuário no onboarding
    
    Returns:
        user_id, status, signup_date
    """
    try:
        # Gerar user_id
        import uuid
        user_id = f"usr_{uuid.uuid4().hex[:8]}"
        
        # Enroll
        result = await platform.onboarding_service.enroll_user(
            user_id=user_id,
            email=request.email,
            company_id=request.company_id
        )
        
        # Metrics
        if PROMETHEUS_AVAILABLE:
            enrollments_total.labels(company=request.company_id).inc()
        
        # Broadcast via WebSocket
        await broadcast_event({
            "type": "user_enrolled",
            "data": result
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/users/{user_id}/steps")
async def complete_step(
    user_id: str,
    request: CompleteStepRequest,
    platform: ONPlatform = Depends(get_platform)
):
    """
    Marca etapa como completa
    
    Returns:
        current_step, engagement_score
    """
    try:
        result = await platform.onboarding_service.track_step_completion(
            user_id=user_id,
            step_id=request.step_id,
            step_number=request.step_number
        )
        
        # Metrics
        if PROMETHEUS_AVAILABLE:
            steps_completed_total.inc()
        
        # Broadcast
        await broadcast_event({
            "type": "step_completed",
            "data": {"user_id": user_id, **result}
        })
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/users/{user_id}/status", response_model=UserStatusResponse)
async def get_user_status(
    user_id: str,
    platform: ONPlatform = Depends(get_platform)
):
    """
    Retorna status atual do onboarding do usuário
    """
    try:
        status = await platform.onboarding_service.get_user_status(user_id)
        
        if "error" in status:
            raise HTTPException(status_code=404, detail=status["error"])
        
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/analytics/cohort")
async def get_cohort_analytics(
    company_id: str,
    platform: ONPlatform = Depends(get_platform)
):
    """
    Analytics de onboarding por empresa (cohort analysis)
    
    Returns:
        total_users, completed, at_risk, completion_rate, average_ttv_days
    """
    try:
        analytics = await platform.onboarding_service.get_cohort_analytics(company_id)
        
        # Update Prometheus gauge
        if PROMETHEUS_AVAILABLE:
            users_at_risk.set(analytics['at_risk'])
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check(platform: ONPlatform = Depends(get_platform)):
    """Health check endpoint"""
    health = await platform.health_check()
    return health


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    if not PROMETHEUS_AVAILABLE:
        return PlainTextResponse("Metrics not available", status_code=501)
    
    return PlainTextResponse(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# ============================================================================
# WEBSOCKET - Real-time Event Stream
# ============================================================================

async def broadcast_event(event: Dict[str, Any]):
    """Broadcast event para todos os WebSockets conectados"""
    disconnected = []
    
    for ws in active_websockets:
        try:
            await ws.send_json(event)
        except:
            disconnected.append(ws)
    
    # Remover desconectados
    for ws in disconnected:
        active_websockets.remove(ws)


@app.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    """
    WebSocket para receber eventos em tempo real
    
    Eventos:
    - user_enrolled
    - step_completed
    - user_at_risk
    - value_achieved
    """
    await websocket.accept()
    active_websockets.append(websocket)
    
    try:
        # Enviar mensagem de boas-vindas
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to ON Platform event stream",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Manter conexão aberta
        while True:
            # Aguardar mensagem do cliente (ping/pong)
            data = await websocket.receive_text()
            
            if data == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        active_websockets.remove(websocket)
        print(f"WebSocket disconnected (active: {len(active_websockets)})")


# ============================================================================
# ROOT
# ============================================================================

@app.get("/")
async def root():
    """API info"""
    return {
        "app": "ON Platform API",
        "version": "1.0.0",
        "framework": "Ávila Framework",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
        "websocket": "ws://localhost:8000/ws/events"
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║          🚀 ON PLATFORM API - Enterprise SaaS           ║
    ║                                                          ║
    ║  Powered by Ávila Framework                              ║
    ║  Event-Driven | CQRS | Multi-Tenant                      ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    
    📡 API: http://localhost:8000
    📚 Docs: http://localhost:8000/docs
    🏥 Health: http://localhost:8000/health
    📊 Metrics: http://localhost:8000/metrics
    🌐 WebSocket: ws://localhost:8000/ws/events
    
    """)
    
    uvicorn.run(
        "on_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
