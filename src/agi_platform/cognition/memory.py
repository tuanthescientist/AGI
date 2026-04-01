from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean

from agi_platform.data.schemas import Experience


@dataclass(slots=True)
class EpisodicMemory:
    capacity: int = 512
    experiences: list[Experience] = field(default_factory=list)

    def add(self, experience: Experience) -> None:
        self.experiences.append(experience)
        if len(self.experiences) > self.capacity:
            self.experiences = self.experiences[-self.capacity :]

    def recent(self, n: int = 5) -> list[Experience]:
        return self.experiences[-n:]

    def summary(self) -> dict[str, float | int]:
        if not self.experiences:
            return {"count": 0, "avg_reward": 0.0, "avg_alignment": 0.0}
        return {
            "count": len(self.experiences),
            "avg_reward": round(mean(exp.reward for exp in self.experiences), 3),
            "avg_alignment": round(mean(exp.alignment_score for exp in self.experiences), 3),
        }