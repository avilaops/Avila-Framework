"""
Agent representation and management
"""
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from datetime import datetime


@dataclass
class Agent:
    """
    Represents an AI agent registered in AgentHub.

    Attributes:
        name: Unique agent identifier
        capabilities: List of agent capabilities
        health_url: HTTP endpoint for health checks
        status: Current agent status (HEALTHY, UNHEALTHY, DEGRADED, etc.)
        metadata: Additional agent metadata
        on_start: Callback when agent starts
        on_stop: Callback when agent stops
    """
    name: str
    capabilities: List[str]
    health_url: str
    status: str = "UNKNOWN"
    metadata: dict = field(default_factory=dict)
    on_start: Optional[Callable] = None
    on_stop: Optional[Callable] = None

    # Runtime stats
    total_requests: int = 0
    total_errors: int = 0
    last_health_check: Optional[datetime] = None
    uptime_start: Optional[datetime] = None

    def __post_init__(self):
        self.uptime_start = datetime.now()

    def has_capability(self, capability: str) -> bool:
        """Check if agent has specific capability"""
        return capability in self.capabilities

    def record_request(self):
        """Record successful request"""
        self.total_requests += 1

    def record_error(self):
        """Record error"""
        self.total_errors += 1

    def error_rate(self) -> float:
        """Calculate error rate"""
        if self.total_requests == 0:
            return 0.0
        return self.total_errors / self.total_requests

    def uptime_seconds(self) -> float:
        """Get uptime in seconds"""
        if not self.uptime_start:
            return 0.0
        return (datetime.now() - self.uptime_start).total_seconds()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'capabilities': self.capabilities,
            'health_url': self.health_url,
            'status': self.status,
            'metadata': self.metadata,
            'total_requests': self.total_requests,
            'total_errors': self.total_errors,
            'error_rate': self.error_rate(),
            'uptime_seconds': self.uptime_seconds(),
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None
        }
