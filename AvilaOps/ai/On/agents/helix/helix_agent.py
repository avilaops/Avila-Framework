import sys
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from _bootstrap import ensure_on_namespace

ensure_on_namespace()

from on.core.on_telemetry import tracer, meter
from on.core.on_logger import AgentLogger
from on.core.on_health import heartbeat

REQUESTS_COUNTER = meter.create_counter(
    name="helix_requests_total",
    description="Total de requisições tratadas pelo Helix"
)

class HelixAgent:
    def __init__(self, bus):
        self.name = "Helix"
        self.bus = bus
        self.logger = AgentLogger(self.name)
        self.bus.register(self.name)
        self.bus.listen(self.name, self.handle)

    def handle(self, msg):
        with tracer.start_as_current_span("helix_handle_message") as span:
            span.set_attribute("agent", self.name)
            span.set_attribute("message.type", msg.type)
            REQUESTS_COUNTER.add(1, {"agent": self.name})
            heartbeat(self.name)
            self.logger.log(f"Recebida mensagem {msg.type} de {msg.sender}")
