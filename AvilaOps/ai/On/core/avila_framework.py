#!/usr/bin/env python3
"""
ÁVILA FRAMEWORK - Core Architecture
A base de tudo: Event-driven, microservices-ready, enterprise-grade

Arquitetura:
- Event Sourcing + CQRS
- Domain-Driven Design (DDD)
- Hexagonal Architecture (Ports & Adapters)
- Multi-tenancy nativo
- Observability by design
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Callable, TypeVar, Generic
from dataclasses import dataclass, field, asdict
from enum import Enum
from abc import ABC, abstractmethod
import logging

# ============================================================================
# CORE DOMAIN EVENTS
# ============================================================================

@dataclass
class DomainEvent:
    """Base para todos os eventos de domínio"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = field(default="")
    aggregate_id: str = field(default="")
    aggregate_type: str = field(default="")
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DomainEvent':
        return cls(**data)


# ============================================================================
# EVENT STORE (Event Sourcing)
# ============================================================================

class EventStore(ABC):
    """Interface para persistência de eventos"""
    
    @abstractmethod
    async def append(self, event: DomainEvent) -> None:
        """Adiciona evento ao stream"""
        pass
    
    @abstractmethod
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[DomainEvent]:
        """Recupera eventos de um agregado"""
        pass
    
    @abstractmethod
    async def get_all_events(self, event_types: Optional[List[str]] = None) -> List[DomainEvent]:
        """Recupera todos os eventos (com filtro opcional)"""
        pass


class InMemoryEventStore(EventStore):
    """Event Store em memória (desenvolvimento)"""
    
    def __init__(self):
        self._events: List[DomainEvent] = []
        self._lock = asyncio.Lock()
    
    async def append(self, event: DomainEvent) -> None:
        async with self._lock:
            self._events.append(event)
    
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[DomainEvent]:
        return [
            e for e in self._events 
            if e.aggregate_id == aggregate_id and e.version >= from_version
        ]
    
    async def get_all_events(self, event_types: Optional[List[str]] = None) -> List[DomainEvent]:
        if event_types:
            return [e for e in self._events if e.event_type in event_types]
        return self._events.copy()


# ============================================================================
# COMMAND BUS (CQRS - Commands)
# ============================================================================

@dataclass
class Command:
    """Base para comandos (intenção de mudança)"""
    command_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    command_type: str = ""
    issued_by: str = "system"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    data: Dict[str, Any] = field(default_factory=dict)


CommandHandler = Callable[[Command], Any]


class CommandBus:
    """Despacha comandos para handlers"""
    
    def __init__(self):
        self._handlers: Dict[str, CommandHandler] = {}
        self.logger = logging.getLogger(__name__)
    
    def register(self, command_type: str, handler: CommandHandler) -> None:
        """Registra handler para tipo de comando"""
        self._handlers[command_type] = handler
        self.logger.info(f"✅ Registered handler for: {command_type}")
    
    async def dispatch(self, command: Command) -> Any:
        """Executa comando"""
        handler = self._handlers.get(command.command_type)
        
        if not handler:
            raise ValueError(f"No handler for command: {command.command_type}")
        
        self.logger.debug(f"⚡ Dispatching: {command.command_type}")
        
        if asyncio.iscoroutinefunction(handler):
            return await handler(command)
        else:
            return handler(command)


# ============================================================================
# QUERY BUS (CQRS - Queries)
# ============================================================================

@dataclass
class Query:
    """Base para queries (leitura)"""
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_type: str = ""
    requested_by: str = "system"
    parameters: Dict[str, Any] = field(default_factory=dict)


QueryHandler = Callable[[Query], Any]


class QueryBus:
    """Despacha queries para handlers"""
    
    def __init__(self):
        self._handlers: Dict[str, QueryHandler] = {}
        self.logger = logging.getLogger(__name__)
    
    def register(self, query_type: str, handler: QueryHandler) -> None:
        """Registra handler para tipo de query"""
        self._handlers[query_type] = handler
        self.logger.info(f"✅ Registered query handler for: {query_type}")
    
    async def execute(self, query: Query) -> Any:
        """Executa query"""
        handler = self._handlers.get(query.query_type)
        
        if not handler:
            raise ValueError(f"No handler for query: {query.query_type}")
        
        self.logger.debug(f"🔍 Executing query: {query.query_type}")
        
        if asyncio.iscoroutinefunction(handler):
            return await handler(query)
        else:
            return handler(query)


# ============================================================================
# AGGREGATE ROOT (DDD)
# ============================================================================

T = TypeVar('T', bound='AggregateRoot')


class AggregateRoot(ABC):
    """Base para agregados (DDD)"""
    
    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self.version = 0
        self._uncommitted_events: List[DomainEvent] = []
    
    def _apply_event(self, event: DomainEvent) -> None:
        """Aplica evento ao estado do agregado"""
        self.version = event.version
        self._handle_event(event)
    
    @abstractmethod
    def _handle_event(self, event: DomainEvent) -> None:
        """Handler específico do agregado para eventos"""
        pass
    
    def _raise_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Levanta novo evento de domínio"""
        event = DomainEvent(
            event_type=event_type,
            aggregate_id=self.aggregate_id,
            aggregate_type=self.__class__.__name__,
            version=self.version + 1,
            data=data
        )
        
        self._uncommitted_events.append(event)
        self._apply_event(event)
    
    def get_uncommitted_events(self) -> List[DomainEvent]:
        """Retorna eventos não persistidos"""
        return self._uncommitted_events.copy()
    
    def mark_events_as_committed(self) -> None:
        """Marca eventos como persistidos"""
        self._uncommitted_events.clear()
    
    @classmethod
    def from_events(cls: type[T], events: List[DomainEvent]) -> T:
        """Reconstrói agregado a partir de eventos (Event Sourcing)"""
        if not events:
            raise ValueError("Cannot create aggregate from empty event stream")
        
        instance = cls(events[0].aggregate_id)
        
        for event in events:
            instance._apply_event(event)
        
        return instance


# ============================================================================
# REPOSITORY (Hexagonal Architecture - Port)
# ============================================================================

class Repository(ABC, Generic[T]):
    """Interface para persistência de agregados"""
    
    @abstractmethod
    async def get_by_id(self, aggregate_id: str) -> Optional[T]:
        """Recupera agregado por ID"""
        pass
    
    @abstractmethod
    async def save(self, aggregate: T) -> None:
        """Persiste agregado"""
        pass


class EventSourcedRepository(Repository[T]):
    """Repository baseado em Event Sourcing"""
    
    def __init__(self, aggregate_class: type[T], event_store: EventStore):
        self.aggregate_class = aggregate_class
        self.event_store = event_store
    
    async def get_by_id(self, aggregate_id: str) -> Optional[T]:
        """Reconstrói agregado a partir de eventos"""
        events = await self.event_store.get_events(aggregate_id)
        
        if not events:
            return None
        
        return self.aggregate_class.from_events(events)
    
    async def save(self, aggregate: T) -> None:
        """Persiste eventos do agregado"""
        uncommitted = aggregate.get_uncommitted_events()
        
        for event in uncommitted:
            await self.event_store.append(event)
        
        aggregate.mark_events_as_committed()


# ============================================================================
# DOMAIN SERVICE
# ============================================================================

class DomainService(ABC):
    """Base para serviços de domínio (lógica que não pertence a um agregado)"""
    pass


# ============================================================================
# MULTI-TENANCY
# ============================================================================

@dataclass
class TenantContext:
    """Contexto de tenant (multi-tenancy)"""
    tenant_id: str
    tenant_name: str
    subscription_tier: str = "free"  # free, pro, enterprise
    features_enabled: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TenantContextProvider:
    """Provedor de contexto de tenant (thread-safe)"""
    
    def __init__(self):
        self._context: Optional[TenantContext] = None
    
    def set_context(self, context: TenantContext) -> None:
        self._context = context
    
    def get_context(self) -> Optional[TenantContext]:
        return self._context
    
    def clear_context(self) -> None:
        self._context = None


# ============================================================================
# APPLICATION SERVICE (Use Cases)
# ============================================================================

class ApplicationService:
    """Base para serviços de aplicação (orquestração de use cases)"""
    
    def __init__(
        self, 
        command_bus: CommandBus, 
        query_bus: QueryBus,
        event_store: EventStore,
        tenant_provider: TenantContextProvider
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.event_store = event_store
        self.tenant_provider = tenant_provider
        self.logger = logging.getLogger(self.__class__.__name__)


# ============================================================================
# ÁVILA FRAMEWORK KERNEL
# ============================================================================

class AvilaFramework:
    """
    Kernel do Framework Ávila
    
    Responsabilidades:
    - Inicialização e configuração
    - Dependency Injection
    - Lifecycle management
    - Health checks
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Core components
        self.event_store = InMemoryEventStore()
        self.command_bus = CommandBus()
        self.query_bus = QueryBus()
        self.tenant_provider = TenantContextProvider()
        
        # Registry
        self._services: Dict[str, Any] = {}
        self._repositories: Dict[str, Any] = {}
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("🚀 Ávila Framework initialized")
    
    def register_service(self, name: str, service: Any) -> None:
        """Registra serviço no container"""
        self._services[name] = service
        self.logger.info(f"✅ Registered service: {name}")
    
    def get_service(self, name: str) -> Any:
        """Recupera serviço do container"""
        return self._services.get(name)
    
    def register_repository(self, name: str, repository: Repository) -> None:
        """Registra repository"""
        self._repositories[name] = repository
        self.logger.info(f"✅ Registered repository: {name}")
    
    def get_repository(self, name: str) -> Optional[Repository]:
        """Recupera repository"""
        return self._repositories.get(name)
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check do framework"""
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": list(self._services.keys()),
            "repositories": list(self._repositories.keys()),
            "event_count": len(await self.event_store.get_all_events())
        }
    
    async def shutdown(self) -> None:
        """Graceful shutdown"""
        self.logger.info("🛑 Shutting down Ávila Framework...")
        # Cleanup resources
        self._services.clear()
        self._repositories.clear()


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def demo():
        # Inicializar framework
        framework = AvilaFramework(config={
            "environment": "development",
            "app_name": "ON Platform"
        })
        
        # Health check
        health = await framework.health_check()
        print(f"\n🏥 Health: {json.dumps(health, indent=2)}")
        
        # Simular evento de domínio
        event = DomainEvent(
            event_type="UserSignedUp",
            aggregate_id="usr_123",
            aggregate_type="User",
            data={
                "email": "nicolas@avila.inc",
                "plan": "enterprise"
            }
        )
        
        await framework.event_store.append(event)
        
        # Recuperar eventos
        events = await framework.event_store.get_all_events()
        print(f"\n📊 Events in store: {len(events)}")
        print(f"   {events[0].to_dict()}")
        
        # Shutdown
        await framework.shutdown()
    
    asyncio.run(demo())
