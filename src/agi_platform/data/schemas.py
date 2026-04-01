from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Observation:
    task_id: str
    prompt: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TaskSpec:
    task_id: str
    domain: str
    difficulty: int
    target_skill: str
    prompt: str
    success_criteria: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Experience:
    task_id: str
    domain: str
    action: str
    reward: float
    uncertainty: float
    alignment_score: float
    introspection_note: str
    outcome: str
    metadata: dict[str, Any] = field(default_factory=dict)