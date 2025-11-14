"""
AgentHub Core - Orchestration and Registry
"""
import time
import threading
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

from .agent import Agent
from .bus import MessageBus
from .health import HealthChecker


@dataclass
class AgentHubConfig:
    """Configuration for AgentHub"""
    health_check_interval: int = 5  # seconds
    auto_restart: bool = True
    auto_scaling: bool = False
    max_workers_per_agent: int = 5
    dashboard_port: int = 8080
    enable_tracing: bool = True
    enable_metrics: bool = True


class AgentHub:
    """
    Central orchestration hub for AI agents.

    Features:
    - Agent registry and discovery
    - Health monitoring
    - Message bus coordination
    - Auto-scaling
    - Distributed tracing
    - Metrics collection

    Example:
        hub = AgentHub()

        archivus = hub.register(
            name="Archivus",
            capabilities=["catalog", "search"],
            health_url="http://localhost:8001/health"
        )

        hub.start()  # Dashboard on :8080
    """

    def __init__(self, config: Optional[AgentHubConfig] = None):
        self.config = config or AgentHubConfig()
        self.agents: Dict[str, Agent] = {}
        self.bus = MessageBus()
        self.health_checker = HealthChecker(interval=self.config.health_check_interval)
        self._running = False
        self._threads: List[threading.Thread] = []

        # Metrics
        self.metrics = {
            'total_agents': 0,
            'healthy_agents': 0,
            'messages_sent': 0,
            'auto_restarts': 0,
            'scaling_events': 0
        }

        # Darwin integration
        self._darwin_enabled = False
        self._learned_fixes: List[Dict] = []

    def register(
        self,
        name: str,
        capabilities: List[str],
        health_url: str,
        on_start: Optional[Callable] = None,
        on_stop: Optional[Callable] = None
    ) -> Agent:
        """
        Register a new agent in the hub.

        Args:
            name: Unique agent identifier
            capabilities: List of capabilities (e.g., ["catalog", "search"])
            health_url: HTTP endpoint for health checks
            on_start: Optional callback when agent starts
            on_stop: Optional callback when agent stops

        Returns:
            Registered Agent instance
        """
        if name in self.agents:
            raise ValueError(f"Agent {name} already registered")

        agent = Agent(
            name=name,
            capabilities=capabilities,
            health_url=health_url,
            on_start=on_start,
            on_stop=on_stop
        )

        self.agents[name] = agent
        self.metrics['total_agents'] += 1

        # Subscribe agent to bus
        self.bus.register_agent(agent)

        # Start health monitoring
        self.health_checker.monitor(agent, self._on_health_check)

        # Publish registration event
        self.bus.publish("agent.registered", {
            "name": name,
            "capabilities": capabilities,
            "timestamp": datetime.now().isoformat()
        })

        return agent

    def unregister(self, name: str):
        """Remove agent from hub"""
        if name not in self.agents:
            raise ValueError(f"Agent {name} not found")

        agent = self.agents[name]
        self.health_checker.unmonitor(agent)
        self.bus.unregister_agent(agent)
        del self.agents[name]

        self.metrics['total_agents'] -= 1

        self.bus.publish("agent.unregistered", {
            "name": name,
            "timestamp": datetime.now().isoformat()
        })

    def get_agent(self, name: str) -> Optional[Agent]:
        """Get agent by name"""
        return self.agents.get(name)

    def list_agents(self) -> List[Agent]:
        """List all registered agents"""
        return list(self.agents.values())

    def start(self):
        """Start AgentHub orchestration"""
        if self._running:
            print("⚠️  AgentHub already running")
            return

        self._running = True

        # Start health checker
        health_thread = threading.Thread(target=self.health_checker.start, daemon=True)
        health_thread.start()
        self._threads.append(health_thread)

        # Start message bus
        bus_thread = threading.Thread(target=self.bus.start, daemon=True)
        bus_thread.start()
        self._threads.append(bus_thread)

        # Start dashboard (if enabled)
        if self.config.dashboard_port:
            dashboard_thread = threading.Thread(target=self._start_dashboard, daemon=True)
            dashboard_thread.start()
            self._threads.append(dashboard_thread)

        print(f"✅ AgentHub started")
        print(f"📡 Message Bus: Active")
        print(f"🩺 Health Checker: Monitoring {len(self.agents)} agents")
        if self.config.dashboard_port:
            print(f"📊 Dashboard: http://localhost:{self.config.dashboard_port}")

    def stop(self):
        """Stop AgentHub"""
        if not self._running:
            return

        self._running = False
        self.health_checker.stop()
        self.bus.stop()

        print("🛑 AgentHub stopped")

    def _on_health_check(self, agent: Agent, is_healthy: bool):
        """Handle health check results"""
        if is_healthy:
            if agent.status != "HEALTHY":
                agent.status = "HEALTHY"
                self.bus.publish("agent.healthy", {
                    "name": agent.name,
                    "timestamp": datetime.now().isoformat()
                })
            self.metrics['healthy_agents'] = sum(
                1 for a in self.agents.values() if a.status == "HEALTHY"
            )
        else:
            agent.status = "UNHEALTHY"
            self.bus.publish("agent.unhealthy", {
                "name": agent.name,
                "timestamp": datetime.now().isoformat()
            })

            # Auto-restart if enabled
            if self.config.auto_restart:
                print(f"🔄 Auto-restarting {agent.name}...")
                self._restart_agent(agent)

    def _restart_agent(self, agent: Agent):
        """Restart unhealthy agent"""
        try:
            if agent.on_stop:
                agent.on_stop()

            time.sleep(1)

            if agent.on_start:
                agent.on_start()

            agent.status = "RESTARTING"
            self.metrics['auto_restarts'] += 1

            self.bus.publish("agent.restarted", {
                "name": agent.name,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"❌ Failed to restart {agent.name}: {e}")
            agent.status = "FAILED"

    def _start_dashboard(self):
        """Start web dashboard (placeholder)"""
        print(f"📊 Dashboard would run on port {self.config.dashboard_port}")
        # TODO: Implement actual web server with real-time dashboard

    def enable_darwin(self, darwin_instance=None):
        """
        Enable Darwin self-healing integration.

        When enabled, AgentHub will:
        - Detect agent failures
        - Apply Darwin fixes automatically
        - Share learned fixes across all agents
        """
        self._darwin_enabled = True

        # Subscribe to error events
        @self.bus.subscribe("agent.error")
        def on_error(event):
            if darwin_instance:
                # Apply Darwin healing
                fix = darwin_instance.heal(event['error'])
                if fix:
                    self._learned_fixes.append(fix)
                    # Broadcast fix to all agents
                    self.bus.publish("fix.learned", {
                        "fix": fix,
                        "from_agent": event['agent'],
                        "timestamp": datetime.now().isoformat()
                    })

        print("🧬 Darwin integration enabled")

    def get_metrics(self) -> Dict:
        """Get current hub metrics"""
        return {
            **self.metrics,
            'uptime_seconds': time.time() - self.health_checker.start_time if self.health_checker.start_time else 0,
            'bus_messages': self.bus.message_count,
            'learned_fixes': len(self._learned_fixes)
        }
