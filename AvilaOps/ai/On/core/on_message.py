import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    NOTIFICATION = "notification"


class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Message:
    sender: str
    recipient: str
    content: str
    message_type: MessageType
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: float = None
    message_id: str = None
    metadata: Dict = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.message_id is None:
            self.message_id = f"{self.sender}_{int(self.timestamp * 1000)}"
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self):
        data = asdict(self)
        data['message_type'] = self.message_type.value
        data['priority'] = self.priority.value
        return data

    @classmethod
    def from_dict(cls, data: Dict):
        data['message_type'] = MessageType(data['message_type'])
        data['priority'] = MessagePriority(data['priority'])
        return cls(**data)


class MessageBus:
    def __init__(self, logs_dir: Path):
        self.agents: Dict[str, 'AgentNode'] = {}
        self.message_history: List[Message] = []
        self.logs_dir = logs_dir
        self.logs_dir.mkdir(exist_ok=True)
        self.message_log_path = self.logs_dir / "message_bus.log"

    def register_agent(self, agent_name: str, handler: Callable):
        """Registra um agente no message bus"""
        self.agents[agent_name] = AgentNode(agent_name, handler, self)
        self._log(f"Agente '{agent_name}' registrado no message bus")
        return self.agents[agent_name]

    def unregister_agent(self, agent_name: str):
        """Remove um agente do message bus"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            self._log(f"Agente '{agent_name}' removido do message bus")

    def send_message(self, message: Message):
        """Envia uma mensagem para um agente específico"""
        if message.recipient == "broadcast":
            self._broadcast(message)
        elif message.recipient in self.agents:
            self.message_history.append(message)
            self.agents[message.recipient].receive(message)
            self._log(f"[{message.sender} → {message.recipient}] {message.content}")
        else:
            self._log(f"Agente destinatário '{message.recipient}' não encontrado")

    def _broadcast(self, message: Message):
        """Envia mensagem para todos os agentes, exceto o remetente"""
        for agent_name, agent in self.agents.items():
            if agent_name != message.sender:
                msg = Message(
                    sender=message.sender,
                    recipient=agent_name,
                    content=message.content,
                    message_type=MessageType.BROADCAST,
                    priority=message.priority,
                    metadata=message.metadata
                )
                agent.receive(msg)
        self._log(f"[{message.sender} → BROADCAST] {message.content}")

    def get_conversation(self, agent1: str, agent2: str) -> List[Message]:
        """Retorna histórico de conversação entre dois agentes"""
        return [
            msg for msg in self.message_history
            if (msg.sender == agent1 and msg.recipient == agent2) or
               (msg.sender == agent2 and msg.recipient == agent1)
        ]

    def _log(self, message: str):
        """Registra evento no log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.message_log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)


class AgentNode:
    def __init__(self, name: str, handler: Callable, bus: MessageBus):
        self.name = name
        self.handler = handler
        self.bus = bus
        self.inbox: List[Message] = []

    def send(self, recipient: str, content: str, 
             message_type: MessageType = MessageType.REQUEST,
             priority: MessagePriority = MessagePriority.NORMAL,
             metadata: Dict = None):
        """Envia uma mensagem para outro agente"""
        message = Message(
            sender=self.name,
            recipient=recipient,
            content=content,
            message_type=message_type,
            priority=priority,
            metadata=metadata or {}
        )
        self.bus.send_message(message)

    def broadcast(self, content: str, priority: MessagePriority = MessagePriority.NORMAL):
        """Envia mensagem para todos os agentes"""
        self.send("broadcast", content, MessageType.BROADCAST, priority)

    def receive(self, message: Message):
        """Recebe uma mensagem"""
        self.inbox.append(message)
        if self.handler:
            self.handler(message)

    def reply(self, original_message: Message, content: str):
        """Responde uma mensagem"""
        self.send(
            recipient=original_message.sender,
            content=content,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            metadata={"reply_to": original_message.message_id}
        )
