from __future__ import annotations

from dataclasses import dataclass, field

from .generators import SyntheticTaskFactory
from .schemas import Observation, TaskSpec


@dataclass(slots=True)
class DataPipeline:
    factory: SyntheticTaskFactory = field(default_factory=SyntheticTaskFactory)

    def build_curriculum(self, levels: int = 4, samples_per_level: int = 6) -> list[TaskSpec]:
        return self.factory.curriculum(levels=levels, samples_per_level=samples_per_level)

    def to_observation(self, task: TaskSpec) -> Observation:
        return Observation(
            task_id=task.task_id,
            prompt=task.prompt,
            context={
                "domain": task.domain,
                "difficulty": task.difficulty,
                "target_skill": task.target_skill,
                "success_criteria": task.success_criteria,
            },
        )