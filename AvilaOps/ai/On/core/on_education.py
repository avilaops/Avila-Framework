"""Lightweight education utilities for agent enablement."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List

from .on_storage import add_task

BASE_DIR = Path(__file__).resolve().parents[1]
MEMORY_DIR = BASE_DIR / "registry" / "memory"


@dataclass
class Module:
    title: str
    description: str
    duration_min: int


@dataclass
class AgentCurriculum:
    agent: str
    modules: List[Module] = field(default_factory=list)

    def add_module(self, module: Module) -> None:
        self.modules.append(module)

    def persist(self) -> Path:
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        target = MEMORY_DIR / f"{self.agent}_curriculum.json"
        payload = {"agent": self.agent, "modules": [asdict(m) for m in self.modules]}
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return target


class EducationService:
    """Coordinates curriculum and task creation for agents."""

    def __init__(self, agent: str) -> None:
        self.agent = agent
        self.curriculum = AgentCurriculum(agent=agent)

    def assign_module(self, title: str, description: str, duration_min: int) -> None:
        module = Module(title=title, description=description, duration_min=duration_min)
        self.curriculum.add_module(module)
        add_task(self.agent, f"Estudar: {title}")

    def export_curriculum(self) -> Path:
        return self.curriculum.persist()
