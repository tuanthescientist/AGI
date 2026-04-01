from __future__ import annotations

from dataclasses import dataclass, field

from agi_platform.data.schemas import TaskSpec

from .self_model import SelfModel


@dataclass(slots=True)
class WorldModel:
    domain_success_priors: dict[str, float] = field(
        default_factory=lambda: {
            "reasoning": 0.48,
            "planning": 0.46,
            "tool_use": 0.44,
            "introspection": 0.52,
        }
    )

    def predict_success(self, task: TaskSpec, action: str, self_model: SelfModel) -> tuple[float, float]:
        base = self.domain_success_priors.get(task.domain, 0.45)
        capability = self_model.capability_scores.get(task.domain, 0.5)
        introspective_bonus = 0.08 if "self-check" in action else 0.0
        planning_bonus = 0.06 if "plan" in action else 0.0
        predicted = max(0.0, min(1.0, base * 0.45 + capability * 0.45 + introspective_bonus + planning_bonus))
        uncertainty = max(0.1, 1.0 - predicted + task.difficulty * 0.05)
        return predicted, min(1.0, uncertainty)

    def update(self, domain: str, reward: float) -> None:
        current = self.domain_success_priors.get(domain, 0.45)
        self.domain_success_priors[domain] = max(0.0, min(1.0, current * 0.9 + reward * 0.1))