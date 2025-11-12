"""Lightweight publish/subscribe bus for inter-agent coordination."""

from __future__ import annotations

from collections import defaultdict
from threading import Lock
from typing import Callable, DefaultDict, Dict, List

from .on_logger import AgentLogger
from .on_message import Message

EventHandler = Callable[[Message], None]


class EventBus:
    """Simple in-memory event hub with per-topic subscribers."""

    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, List[EventHandler]] = defaultdict(list)
        self._lock = Lock()
        self._logger = AgentLogger("system")

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        with self._lock:
            self._subscribers[topic].append(handler)
            self._logger.log(f"Handler inscrito para tópico '{topic}'.")

    def publish(self, message: Message) -> None:
        handlers = list(self._subscribers.get(message.topic, ()))
        if not handlers:
            self._logger.log(f"Nenhum assinante para '{message.topic}'.")
            return
        for handler in handlers:
            try:
                handler(message)
            except Exception as exc:  # defensive guard for user handlers
                self._logger.log(f"Erro ao processar mensagem em '{message.topic}': {exc}")

    def topics(self) -> List[str]:
        return list(self._subscribers.keys())

    def snapshot(self) -> Dict[str, int]:
        return {topic: len(handlers) for topic, handlers in self._subscribers.items()}
