from __future__ import annotations

from dataclasses import dataclass

from agi_platform.cognition.memory import EpisodicMemory
from agi_platform.cognition.self_model import SelfModel
from agi_platform.safety.governance import GovernancePolicy


@dataclass(slots=True)
class SelfImprovementEngine:
    step_size: float = 0.05

    def propose(self, self_model: SelfModel, memory: EpisodicMemory) -> dict[str, float]:
        priorities = self_model.improvement_priorities or ["reasoning"]
        recent_reward = memory.summary().get("avg_reward", 0.0)
        magnitude = self.step_size if recent_reward < 0.8 else self.step_size / 2
        return {domain: magnitude for domain in priorities}

    def apply(self, self_model: SelfModel, change_set: dict[str, float], governance: GovernancePolicy) -> bool:
        if not governance.review_self_change(change_set):
            return False
        for domain, delta in change_set.items():
            current = self_model.capability_scores.get(domain, 0.5)
            self_model.capability_scores[domain] = max(0.0, min(1.0, current + delta))
        self_model._refresh_priorities()
        return True