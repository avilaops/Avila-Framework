import logging

from _bootstrap import ensure_on_namespace

ensure_on_namespace()

from on.core.on_storage import log as db_log

logger = logging.getLogger("on.core")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

class AgentLogger:
    def __init__(self, agent_name: str):
        self.agent = agent_name

    def log(self, text: str):
        self.info(text)

    def info(self, text: str) -> None:
        self._record(logger.info, text)

    def warning(self, text: str) -> None:
        self._record(logger.warning, text)

    def error(self, text: str) -> None:
        self._record(logger.error, text)

    def _record(self, level_fn, text: str) -> None:
        msg = f"[{self.agent}] {text}"
        level_fn(msg)
        db_log(self.agent, text)
