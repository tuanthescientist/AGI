from __future__ import annotations

from dataclasses import dataclass, field

from agi_platform.data.schemas import Experience


@dataclass(slots=True)
class SelfModel:
    capability_scores: dict[str, float] = field(
        default_factory=lambda: {
            "reasoning": 0.5,
            "planning": 0.5,
            "tool_use": 0.5,
            "introspection": 0.5,
        }
    )
    calibration: float = 0.6
    improvement_priorities: list[str] = field(default_factory=list)

    def reflect(self, experience: Experience) -> None:
        old_score = self.capability_scores.get(experience.domain, 0.5)
        delta = (experience.reward - experience.uncertainty * 0.2) * 0.08
        self.capability_scores[experience.domain] = max(0.0, min(1.0, old_score + delta))

        self.calibration = max(
            0.0,
            min(1.0, self.calibration * 0.92 + (1.0 - experience.uncertainty) * 0.08),
        )
        self._refresh_priorities()

    def _refresh_priorities(self) -> None:
        ranked = sorted(self.capability_scores.items(), key=lambda item: item[1])
        self.improvement_priorities = [domain for domain, _ in ranked[:2]]

    def narrative_summary(self) -> str:
        focus = ", ".join(self.improvement_priorities or ["maintain balance"])
        return (
            f"Calibration={self.calibration:.2f}; "
            f"priorities={focus}; "
            f"capabilities={self.capability_scores}"
        )