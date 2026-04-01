from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CurriculumStage:
    level: int
    focus_domains: list[str]


@dataclass(slots=True)
class AdaptiveCurriculum:
    max_level: int = 4

    def stage_for_episode(self, episode_index: int, priorities: list[str]) -> CurriculumStage:
        level = min(self.max_level, 1 + episode_index // 6)
        focus = priorities if priorities else ["reasoning", "planning"]
        return CurriculumStage(level=level, focus_domains=focus)