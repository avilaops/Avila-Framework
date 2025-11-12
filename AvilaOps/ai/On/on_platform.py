#!/usr/bin/env python3
"""
ON PLATFORM - Enterprise Onboarding SaaS
Construído sobre Ávila Framework

Domínio: Gestão de onboarding de clientes B2B
Features:
- Multi-tenant (isolamento por empresa)
- Workflows personalizáveis
- Analytics em tempo real
- Integrações (Slack, Teams, Email)
- ML-powered: churn prediction, engagement scoring
"""

import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

# Import do Framework
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
from avila_framework import (
    AvilaFramework, AggregateRoot, DomainEvent, Command, Query,
    Repository, EventSourcedRepository, ApplicationService, TenantContext
)

# ============================================================================
# DOMAIN MODEL - ON PLATFORM
# ============================================================================

class UserOnboardingStatus:
    """Estados do onboarding"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    AT_RISK = "at_risk"
    COMPLETED = "completed"
    CHURNED = "churned"


@dataclass
class OnboardingWorkflow:
    """Workflow de onboarding"""
    workflow_id: str
    name: str
    steps: List[Dict[str, Any]]
    estimated_duration_days: int
    success_criteria: Dict[str, Any]


class UserOnboarding(AggregateRoot):
    """
    Agregado: Onboarding de um usuário
    
    Invariantes:
    - TTV (Time-to-Value) deve ser minimizado
    - Usuário deve completar etapas críticas em ordem
    - Support tickets > 3 = escalação automática
    """
    
    def __init__(self, user_id: str):
        super().__init__(user_id)
        
        # Estado
        self.user_id = user_id
        self.email: Optional[str] = None
        self.company_id: Optional[str] = None
        self.signup_date: Optional[datetime] = None
        self.status = UserOnboardingStatus.NOT_STARTED
        self.current_step = 0
        self.completed_steps: List[str] = []
        self.ttv_days: Optional[int] = None
        self.engagement_score = 0.0
        self.support_tickets_count = 0
        self.features_activated: List[str] = []
    
    def _handle_event(self, event: DomainEvent) -> None:
        """Aplica eventos ao estado"""
        
        if event.event_type == "UserSignedUp":
            self.email = event.data['email']
            self.company_id = event.data['company_id']
            self.signup_date = datetime.fromisoformat(event.data['signup_date'])
            self.status = UserOnboardingStatus.IN_PROGRESS
        
        elif event.event_type == "StepCompleted":
            self.completed_steps.append(event.data['step_id'])
            self.current_step = event.data['step_number']
            self.engagement_score = event.data.get('engagement_score', self.engagement_score)
        
        elif event.event_type == "FeatureActivated":
            self.features_activated.append(event.data['feature_name'])
        
        elif event.event_type == "ValueAchieved":
            self.ttv_days = event.data['ttv_days']
            self.status = UserOnboardingStatus.COMPLETED
        
        elif event.event_type == "SupportTicketOpened":
            self.support_tickets_count += 1
            if self.support_tickets_count > 3:
                self.status = UserOnboardingStatus.AT_RISK
        
        elif event.event_type == "UserChurned":
            self.status = UserOnboardingStatus.CHURNED
    
    # ========================================================================
    # COMMANDS (Comportamentos)
    # ========================================================================
    
    def sign_up(self, email: str, company_id: str) -> None:
        """Registra novo usuário"""
        if self.version > 0:
            raise ValueError("User already signed up")
        
        self._raise_event("UserSignedUp", {
            "email": email,
            "company_id": company_id,
            "signup_date": datetime.now(timezone.utc).isoformat()
        })
    
    def complete_step(self, step_id: str, step_number: int, engagement_score: float) -> None:
        """Marca etapa como completa"""
        if step_id in self.completed_steps:
            raise ValueError(f"Step {step_id} already completed")
        
        self._raise_event("StepCompleted", {
            "step_id": step_id,
            "step_number": step_number,
            "engagement_score": engagement_score
        })
    
    def activate_feature(self, feature_name: str) -> None:
        """Ativa feature do produto"""
        if feature_name in self.features_activated:
            return  # Idempotente
        
        self._raise_event("FeatureActivated", {
            "feature_name": feature_name,
            "activated_at": datetime.now(timezone.utc).isoformat()
        })
    
    def achieve_value(self) -> None:
        """Marca que usuário atingiu valor (TTV)"""
        if self.status == UserOnboardingStatus.COMPLETED:
            return  # Já atingiu
        
        if not self.signup_date:
            raise ValueError("Cannot calculate TTV without signup date")
        
        ttv_days = (datetime.now(timezone.utc) - self.signup_date).days
        
        self._raise_event("ValueAchieved", {
            "ttv_days": ttv_days,
            "features_count": len(self.features_activated)
        })
    
    def open_support_ticket(self, ticket_id: str, severity: str) -> None:
        """Registra ticket de suporte"""
        self._raise_event("SupportTicketOpened", {
            "ticket_id": ticket_id,
            "severity": severity,
            "opened_at": datetime.now(timezone.utc).isoformat()
        })
    
    def churn(self, reason: str) -> None:
        """Marca usuário como churned"""
        self._raise_event("UserChurned", {
            "reason": reason,
            "churned_at": datetime.now(timezone.utc).isoformat(),
            "days_active": (datetime.now(timezone.utc) - self.signup_date).days if self.signup_date else 0
        })


# ============================================================================
# APPLICATION SERVICES (Use Cases)
# ============================================================================

class OnboardingService(ApplicationService):
    """
    Serviço de aplicação: Orquestra casos de uso de onboarding
    """
    
    async def enroll_user(
        self, 
        user_id: str, 
        email: str, 
        company_id: str
    ) -> Dict[str, Any]:
        """
        Use Case: Cadastrar novo usuário no onboarding
        """
        # Criar agregado
        onboarding = UserOnboarding(user_id)
        onboarding.sign_up(email, company_id)
        
        # Persistir
        repo = EventSourcedRepository(UserOnboarding, self.event_store)
        await repo.save(onboarding)
        
        self.logger.info(f"✅ User enrolled: {user_id} ({email})")
        
        return {
            "user_id": user_id,
            "status": onboarding.status,
            "signup_date": onboarding.signup_date.isoformat() if onboarding.signup_date else None
        }
    
    async def track_step_completion(
        self,
        user_id: str,
        step_id: str,
        step_number: int
    ) -> Dict[str, Any]:
        """
        Use Case: Registrar conclusão de etapa
        """
        # Recuperar agregado
        repo = EventSourcedRepository(UserOnboarding, self.event_store)
        onboarding = await repo.get_by_id(user_id)
        
        if not onboarding:
            raise ValueError(f"User {user_id} not found")
        
        # Calcular engagement score (exemplo simples)
        engagement_score = min(100.0, (step_number / 10) * 100)
        
        # Aplicar comando
        onboarding.complete_step(step_id, step_number, engagement_score)
        
        # Persistir
        await repo.save(onboarding)
        
        self.logger.info(f"✅ Step completed: {user_id} -> {step_id}")
        
        return {
            "user_id": user_id,
            "current_step": onboarding.current_step,
            "engagement_score": onboarding.engagement_score
        }
    
    async def get_user_status(self, user_id: str) -> Dict[str, Any]:
        """
        Query: Status do onboarding do usuário
        """
        repo = EventSourcedRepository(UserOnboarding, self.event_store)
        onboarding = await repo.get_by_id(user_id)
        
        if not onboarding:
            return {"error": "User not found"}
        
        return {
            "user_id": onboarding.user_id,
            "email": onboarding.email,
            "status": onboarding.status,
            "current_step": onboarding.current_step,
            "completed_steps": len(onboarding.completed_steps),
            "ttv_days": onboarding.ttv_days,
            "engagement_score": onboarding.engagement_score,
            "features_activated": onboarding.features_activated,
            "support_tickets": onboarding.support_tickets_count,
            "at_risk": onboarding.status == UserOnboardingStatus.AT_RISK
        }
    
    async def get_cohort_analytics(self, company_id: str) -> Dict[str, Any]:
        """
        Query: Analytics de onboarding por empresa (tenant)
        """
        # Recuperar todos os eventos de UserSignedUp
        all_events = await self.event_store.get_all_events()
        
        # Filtrar por company
        company_users = [
            e.aggregate_id for e in all_events 
            if e.event_type == "UserSignedUp" and e.data.get('company_id') == company_id
        ]
        
        # Reconstruir agregados
        repo = EventSourcedRepository(UserOnboarding, self.event_store)
        
        users_data = []
        for user_id in company_users:
            user = await repo.get_by_id(user_id)
            if user:
                users_data.append({
                    "user_id": user.user_id,
                    "status": user.status,
                    "ttv_days": user.ttv_days,
                    "engagement_score": user.engagement_score
                })
        
        # Calcular métricas
        total_users = len(users_data)
        completed = sum(1 for u in users_data if u['status'] == UserOnboardingStatus.COMPLETED)
        at_risk = sum(1 for u in users_data if u['status'] == UserOnboardingStatus.AT_RISK)
        
        ttv_values = [u['ttv_days'] for u in users_data if u['ttv_days'] is not None]
        avg_ttv = sum(ttv_values) / len(ttv_values) if ttv_values else None
        
        return {
            "company_id": company_id,
            "total_users": total_users,
            "completed": completed,
            "at_risk": at_risk,
            "completion_rate": (completed / total_users * 100) if total_users > 0 else 0,
            "average_ttv_days": round(avg_ttv, 1) if avg_ttv else None,
            "users": users_data
        }


# ============================================================================
# ON PLATFORM - Application
# ============================================================================

class ONPlatform:
    """
    ON Platform - Aplicação principal
    """
    
    def __init__(self):
        # Inicializar framework
        self.framework = AvilaFramework(config={
            "app_name": "ON Platform",
            "version": "1.0.0",
            "environment": "production"
        })
        
        # Registrar serviços
        self.onboarding_service = OnboardingService(
            command_bus=self.framework.command_bus,
            query_bus=self.framework.query_bus,
            event_store=self.framework.event_store,
            tenant_provider=self.framework.tenant_provider
        )
        
        self.framework.register_service("onboarding", self.onboarding_service)
    
    async def start(self) -> None:
        """Inicializa plataforma"""
        print("\n" + "=" * 60)
        print("🚀 ON PLATFORM - Enterprise Onboarding SaaS")
        print("=" * 60)
        print(f"Powered by: Ávila Framework")
        print(f"Version: 1.0.0")
        print(f"Environment: Production")
        print("=" * 60)
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check"""
        framework_health = await self.framework.health_check()
        
        return {
            **framework_health,
            "platform": "ON",
            "version": "1.0.0"
        }


# ============================================================================
# DEMO / SMOKE TEST
# ============================================================================

async def demo():
    """Demonstração da ON Platform"""
    
    # Inicializar plataforma
    platform = ONPlatform()
    await platform.start()
    
    # Configurar tenant
    platform.framework.tenant_provider.set_context(TenantContext(
        tenant_id="company_avila",
        tenant_name="Ávila Inc.",
        subscription_tier="enterprise",
        features_enabled=["advanced_analytics", "custom_workflows", "api_access"]
    ))
    
    service = platform.onboarding_service
    
    print("\n📊 CENÁRIO: Onboarding de 3 usuários\n")
    
    # User 1: Sucesso rápido
    user1 = await service.enroll_user("usr_001", "user1@cliente.com", "company_avila")
    print(f"✅ User 1 enrolled: {user1}")
    
    await service.track_step_completion("usr_001", "step_welcome", 1)
    await service.track_step_completion("usr_001", "step_setup", 2)
    await service.track_step_completion("usr_001", "step_first_action", 3)
    
    repo = EventSourcedRepository(UserOnboarding, service.event_store)
    u1 = await repo.get_by_id("usr_001")
    u1.activate_feature("dashboard")
    u1.activate_feature("reports")
    u1.achieve_value()
    await repo.save(u1)
    
    # User 2: At risk
    user2 = await service.enroll_user("usr_002", "user2@cliente.com", "company_avila")
    print(f"✅ User 2 enrolled: {user2}")
    
    u2 = await repo.get_by_id("usr_002")
    u2.open_support_ticket("ticket_001", "high")
    u2.open_support_ticket("ticket_002", "high")
    u2.open_support_ticket("ticket_003", "critical")
    u2.open_support_ticket("ticket_004", "critical")
    await repo.save(u2)
    
    # User 3: Progresso médio
    user3 = await service.enroll_user("usr_003", "user3@cliente.com", "company_avila")
    print(f"✅ User 3 enrolled: {user3}")
    
    await service.track_step_completion("usr_003", "step_welcome", 1)
    
    # Analytics
    print("\n📈 ANALYTICS - Company Cohort:\n")
    analytics = await service.get_cohort_analytics("company_avila")
    
    print(f"Total Users: {analytics['total_users']}")
    print(f"Completed: {analytics['completed']}")
    print(f"At Risk: {analytics['at_risk']}")
    print(f"Completion Rate: {analytics['completion_rate']:.1f}%")
    print(f"Average TTV: {analytics['average_ttv_days']} days")
    
    print("\n👤 USER STATUS:")
    for user in analytics['users']:
        icon = "✅" if user['status'] == 'completed' else "⚠️" if user['status'] == 'at_risk' else "🔄"
        print(f"  {icon} {user['user_id']}: {user['status']} (score: {user['engagement_score']:.1f})")
    
    # Health check
    print("\n🏥 HEALTH CHECK:")
    health = await platform.health_check()
    print(f"Status: {health['status']}")
    print(f"Events in store: {health['event_count']}")
    
    # Event stream
    print("\n📜 EVENT STREAM (últimos 5):")
    events = await service.event_store.get_all_events()
    for event in events[-5:]:
        print(f"  • {event.event_type} @ {event.timestamp} → {event.aggregate_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())
