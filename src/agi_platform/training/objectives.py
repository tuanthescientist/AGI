from __future__ import annotations

from dataclasses import dataclass

from agi_platform.data.schemas import Experience


@dataclass(slots=True)
class ObjectiveWeights:
    reward: float = 0.55
    novelty: float = 0.15
    introspection: float = 0.15
    alignment: float = 0.15

    def score(self, experience: Experience) -> float:
        novelty = 0.8 if "probe weakness" in experience.action else 0.45
        introspection = 0.9 if "self_state=" in experience.introspection_note else 0.6
        return (
            experience.reward * self.reward
            + novelty * self.novelty
            + introspection * self.introspection
            + experience.alignment_score * self.alignment
        )