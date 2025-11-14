"""
Health Checker - Monitor agent health and availability
"""
import time
import threading
import requests
from typing import Callable, Dict
from datetime import datetime


class HealthChecker:
    """
    Monitors agent health via HTTP health checks.

    Features:
    - Periodic health checks
    - Timeout handling
    - Callback on status change
    - Health history tracking

    Example:
        checker = HealthChecker(interval=5)
        checker.monitor(agent, on_health_change)
        checker.start()
    """

    def __init__(self, interval: int = 5, timeout: int = 3):
        """
        Initialize health checker.

        Args:
            interval: Seconds between health checks
            timeout: HTTP request timeout in seconds
        """
        self.interval = interval
        self.timeout = timeout
        self.monitored_agents: Dict = {}  # agent -> callback
        self.running = False
        self.start_time = None

        # Health history
        self.health_history: Dict[str, list] = {}  # agent_name -> [bool, bool, ...]
        self.max_history = 100

    def monitor(self, agent, callback: Callable):
        """
        Start monitoring an agent.

        Args:
            agent: Agent instance to monitor
            callback: Function called on health change (agent, is_healthy)
        """
        self.monitored_agents[agent] = callback
        self.health_history[agent.name] = []

    def unmonitor(self, agent):
        """Stop monitoring an agent"""
        if agent in self.monitored_agents:
            del self.monitored_agents[agent]
        if agent.name in self.health_history:
            del self.health_history[agent.name]

    def check_health(self, agent) -> bool:
        """
        Perform single health check.

        Args:
            agent: Agent to check

        Returns:
            True if healthy, False otherwise
        """
        try:
            response = requests.get(
                agent.health_url,
                timeout=self.timeout
            )

            agent.last_health_check = datetime.now()

            # Consider 2xx status codes as healthy
            is_healthy = 200 <= response.status_code < 300

            # Record in history
            if agent.name in self.health_history:
                self.health_history[agent.name].append(is_healthy)
                if len(self.health_history[agent.name]) > self.max_history:
                    self.health_history[agent.name] = self.health_history[agent.name][-self.max_history:]

            return is_healthy

        except requests.exceptions.Timeout:
            agent.last_health_check = datetime.now()
            return False
        except requests.exceptions.ConnectionError:
            agent.last_health_check = datetime.now()
            return False
        except Exception as e:
            print(f"❌ Health check error for {agent.name}: {e}")
            agent.last_health_check = datetime.now()
            return False

    def start(self):
        """Start health checking loop"""
        self.running = True
        self.start_time = time.time()

        while self.running:
            for agent, callback in list(self.monitored_agents.items()):
                is_healthy = self.check_health(agent)

                # Call callback
                try:
                    callback(agent, is_healthy)
                except Exception as e:
                    print(f"❌ Health callback error for {agent.name}: {e}")

            # Sleep until next check
            time.sleep(self.interval)

    def stop(self):
        """Stop health checking"""
        self.running = False

    def get_agent_uptime(self, agent_name: str) -> float:
        """
        Calculate agent uptime percentage.

        Args:
            agent_name: Name of agent

        Returns:
            Uptime as percentage (0.0 to 1.0)
        """
        if agent_name not in self.health_history:
            return 0.0

        history = self.health_history[agent_name]
        if not history:
            return 0.0

        healthy_checks = sum(1 for h in history if h)
        return healthy_checks / len(history)

    def get_stats(self) -> Dict:
        """Get health checker statistics"""
        total_agents = len(self.monitored_agents)

        uptimes = {
            name: self.get_agent_uptime(name)
            for name in self.health_history.keys()
        }

        avg_uptime = sum(uptimes.values()) / len(uptimes) if uptimes else 0.0

        return {
            'total_monitored': total_agents,
            'interval_seconds': self.interval,
            'timeout_seconds': self.timeout,
            'avg_uptime': avg_uptime,
            'agent_uptimes': uptimes
        }
