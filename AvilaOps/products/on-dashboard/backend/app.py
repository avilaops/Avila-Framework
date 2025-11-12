#!/usr/bin/env python3
"""
ON - Onboarding & Operations Platform
Backend API com FastAPI + PostgreSQL + Redis
Métricas reais em tempo real para onboarding de clientes

Stack:
- FastAPI: API REST/WebSocket
- PostgreSQL: Dados transacionais
- Redis: Cache + pub/sub
- TimescaleDB: Métricas time-series
- Prometheus client: Exportação métricas
"""

from fastapi import FastAPI, WebSocket, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import redis.asyncio as redis
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import logging

# Configuração
app = FastAPI(
    title="ON - Onboarding Platform API",
    version="2.0.0",
    description="Enterprise onboarding with real-time analytics"
)

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Produção: domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus métricas
ONBOARDING_STARTED = Counter('on_onboarding_started_total', 'Total onboardings iniciados')
ONBOARDING_COMPLETED = Counter('on_onboarding_completed_total', 'Total onboardings completados')
ONBOARDING_DURATION = Histogram('on_onboarding_duration_seconds', 'Duração do onboarding')
ACTIVE_USERS = Gauge('on_active_users', 'Usuários ativos agora')
TTV_METRIC = Histogram('on_time_to_value_days', 'Time to Value em dias')
CHURN_RISK_USERS = Gauge('on_churn_risk_users', 'Usuários em risco de churn')

# Modelos
class OnboardingStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CHAMPION = "champion"
    AT_RISK = "at_risk"
    CHURNED = "churned"

class UserPlan(str, Enum):
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class OnboardingStep(str, Enum):
    SIGNUP = "signup"
    EMAIL_VERIFICATION = "email_verification"
    PROFILE_SETUP = "profile_setup"
    FIRST_PROJECT = "first_project"
    INTEGRATION = "integration"
    FIRST_AUTOMATION = "first_automation"
    TEAM_INVITE = "team_invite"
    BILLING_SETUP = "billing_setup"

class User(BaseModel):
    user_id: str = Field(..., description="UUID único do usuário")
    email: EmailStr
    name: str
    company: str
    plan: UserPlan
    signup_date: datetime
    last_login: Optional[datetime] = None
    onboarding_status: OnboardingStatus = OnboardingStatus.NOT_STARTED
    completed_steps: List[OnboardingStep] = []
    ttv_days: Optional[float] = None  # Time to Value
    total_sessions: int = 0
    features_used: List[str] = []
    support_tickets_open: int = 0
    health_score: float = Field(100.0, ge=0, le=100)  # 0-100
    region: str = "americas"
    
class OnboardingEvent(BaseModel):
    user_id: str
    event_type: str
    step: Optional[OnboardingStep] = None
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.now)

class MetricsResponse(BaseModel):
    total_users: int
    active_users: int
    avg_ttv_days: float
    completion_rate: float
    churn_risk_count: int
    champion_count: int
    daily_signups: int
    revenue_mrr: float
    health_score_avg: float

# Simulação de banco de dados (em produção: PostgreSQL)
users_db: Dict[str, User] = {}

# Redis para cache e pub/sub
redis_client: Optional[redis.Redis] = None

# Funções auxiliares
async def get_redis():
    """Dependency para Redis"""
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url("redis://localhost:6379", decode_responses=True)
    return redis_client

def calculate_health_score(user: User) -> float:
    """
    Calcula health score do usuário (0-100)
    
    Fatores:
    - Sessões recentes (+)
    - Features usadas (+)
    - Tickets abertos (-)
    - TTV rápido (+)
    - Últimos 7 dias sem login (-)
    """
    score = 100.0
    
    # Penalizar inatividade
    if user.last_login:
        days_inactive = (datetime.now() - user.last_login).days
        if days_inactive > 7:
            score -= min(30, days_inactive * 2)
    
    # Recompensar engajamento
    score += min(20, user.total_sessions * 0.5)
    score += min(15, len(user.features_used) * 3)
    
    # Penalizar tickets
    score -= min(25, user.support_tickets_open * 8)
    
    # Recompensar TTV rápido
    if user.ttv_days:
        if user.ttv_days < 3:
            score += 10
        elif user.ttv_days > 14:
            score -= 15
    
    return max(0, min(100, score))

def determine_status(user: User) -> OnboardingStatus:
    """Determina status baseado em health score e comportamento"""
    health = user.health_score
    
    if health >= 90 and len(user.completed_steps) >= 7:
        return OnboardingStatus.CHAMPION
    elif health >= 70 and len(user.completed_steps) >= 4:
        return OnboardingStatus.COMPLETED
    elif health >= 50:
        return OnboardingStatus.IN_PROGRESS
    elif health >= 30:
        return OnboardingStatus.AT_RISK
    else:
        return OnboardingStatus.CHURNED

# Endpoints
@app.post("/api/users", response_model=User, status_code=201)
async def create_user(user: User):
    """Criar novo usuário"""
    if user.user_id in users_db:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    user.health_score = calculate_health_score(user)
    user.onboarding_status = determine_status(user)
    users_db[user.user_id] = user
    
    # Métricas
    ONBOARDING_STARTED.inc()
    ACTIVE_USERS.set(len([u for u in users_db.values() if u.onboarding_status != OnboardingStatus.CHURNED]))
    
    logger.info(f"Novo usuário criado: {user.email} ({user.plan})")
    
    return user

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Obter usuário por ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return users_db[user_id]

@app.post("/api/events")
async def track_event(event: OnboardingEvent, r: redis.Redis = Depends(get_redis)):
    """Rastrear evento de onboarding"""
    if event.user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    user = users_db[event.user_id]
    
    # Atualizar baseado no evento
    if event.step and event.step not in user.completed_steps:
        user.completed_steps.append(event.step)
        
        # Time to Value = primeiro valor gerado
        if event.step == OnboardingStep.FIRST_AUTOMATION and user.ttv_days is None:
            user.ttv_days = (datetime.now() - user.signup_date).days
            TTV_METRIC.observe(user.ttv_days)
    
    if event.event_type == "session_start":
        user.total_sessions += 1
        user.last_login = datetime.now()
    
    if event.event_type == "feature_used":
        feature = event.metadata.get("feature")
        if feature and feature not in user.features_used:
            user.features_used.append(feature)
    
    # Recalcular health
    user.health_score = calculate_health_score(user)
    user.onboarding_status = determine_status(user)
    
    # Publicar evento no Redis pub/sub
    await r.publish("onboarding_events", json.dumps({
        "user_id": event.user_id,
        "event_type": event.event_type,
        "timestamp": event.timestamp.isoformat()
    }))
    
    # Métricas
    if user.onboarding_status == OnboardingStatus.COMPLETED:
        ONBOARDING_COMPLETED.inc()
    
    return {"status": "ok", "health_score": user.health_score}

@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Métricas agregadas do sistema"""
    users = list(users_db.values())
    
    if not users:
        return MetricsResponse(
            total_users=0, active_users=0, avg_ttv_days=0,
            completion_rate=0, churn_risk_count=0, champion_count=0,
            daily_signups=0, revenue_mrr=0, health_score_avg=0
        )
    
    # Calcular métricas
    active = [u for u in users if u.onboarding_status not in [OnboardingStatus.CHURNED, OnboardingStatus.NOT_STARTED]]
    completed = [u for u in users if u.onboarding_status in [OnboardingStatus.COMPLETED, OnboardingStatus.CHAMPION]]
    at_risk = [u for u in users if u.onboarding_status == OnboardingStatus.AT_RISK]
    champions = [u for u in users if u.onboarding_status == OnboardingStatus.CHAMPION]
    
    ttv_values = [u.ttv_days for u in users if u.ttv_days is not None]
    avg_ttv = sum(ttv_values) / len(ttv_values) if ttv_values else 0
    
    # Daily signups (últimas 24h)
    yesterday = datetime.now() - timedelta(days=1)
    daily = sum(1 for u in users if u.signup_date >= yesterday)
    
    # MRR (simulado baseado em planos)
    mrr_map = {"starter": 29, "pro": 99, "enterprise": 499}
    mrr = sum(mrr_map.get(u.plan.value, 0) for u in active)
    
    # Health score médio
    avg_health = sum(u.health_score for u in users) / len(users)
    
    # Atualizar Prometheus
    CHURN_RISK_USERS.set(len(at_risk))
    ACTIVE_USERS.set(len(active))
    
    return MetricsResponse(
        total_users=len(users),
        active_users=len(active),
        avg_ttv_days=round(avg_ttv, 1),
        completion_rate=round(len(completed) / len(users) * 100, 1),
        churn_risk_count=len(at_risk),
        champion_count=len(champions),
        daily_signups=daily,
        revenue_mrr=mrr,
        health_score_avg=round(avg_health, 1)
    )

@app.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """WebSocket para métricas em tempo real"""
    await websocket.accept()
    
    try:
        while True:
            metrics = await get_metrics()
            await websocket.send_json(metrics.dict())
            await asyncio.sleep(2)  # Atualizar a cada 2s
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.get("/metrics")
async def prometheus_metrics():
    """Endpoint Prometheus"""
    return generate_latest()

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users_db)
    }

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   ON - ONBOARDING PLATFORM API                            ║
    ║   Ávila Inc. - Enterprise Onboarding Solution             ║
    ╚═══════════════════════════════════════════════════════════╝
    
    📊 API: http://localhost:8000
    📖 Docs: http://localhost:8000/docs
    📈 Metrics: http://localhost:8000/metrics
    🔌 WebSocket: ws://localhost:8000/ws/metrics
    
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
