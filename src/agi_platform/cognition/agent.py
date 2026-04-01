from __future__ import annotations

from dataclasses import dataclass, field

from agi_platform.data.pipeline import DataPipeline
from agi_platform.data.schemas import Experience, TaskSpec
from agi_platform.safety.governance import GovernancePolicy

from .memory import EpisodicMemory
from .planner import Planner
from .self_model import SelfModel
from .world_model import WorldModel


@dataclass(slots=True)
class CognitiveAgent:
    memory: EpisodicMemory = field(default_factory=EpisodicMemory)
    self_model: SelfModel = field(default_factory=SelfModel)
    world_model: WorldModel = field(default_factory=WorldModel)
    planner: Planner = field(default_factory=Planner)
    governance: GovernancePolicy = field(default_factory=GovernancePolicy)
    pipeline: DataPipeline = field(default_factory=DataPipeline)

    def run_task(self, task: TaskSpec) -> Experience:
        observation = self.pipeline.to_observation(task)
        action, predicted_success, uncertainty = self.planner.choose_action(
            task=task,
            self_model=self.self_model,
            world_model=self.world_model,
            governance=self.governance,
        )

        reward = self._score_action(task, action, predicted_success)
        alignment_score = 0.9 if "self-check" in action else 0.75
        outcome = "success" if reward >= 0.55 else "partial"
        introspection_note = (
            f"Observed domain={observation.context['domain']} difficulty={observation.context['difficulty']}; "
            f"predicted_success={predicted_success:.2f}; uncertainty={uncertainty:.2f}; "
            f"self_state={self.self_model.narrative_summary()}"
        )
        experience = Experience(
            task_id=task.task_id,
            domain=task.domain,
            action=action,
            reward=reward,
            uncertainty=uncertainty,
            alignment_score=alignment_score,
            introspection_note=introspection_note,
            outcome=outcome,
            metadata={"prompt": task.prompt},
        )
        self.memory.add(experience)
        self.self_model.reflect(experience)
        self.world_model.update(task.domain, reward)
        return experience

    def _score_action(self, task: TaskSpec, action: str, predicted_success: float) -> float:
        strategy_bonus = 0.06 if task.target_skill.split()[0] in action else 0.02
        reflection_bonus = 0.08 if "self-check" in action else 0.0
        difficulty_penalty = task.difficulty * 0.04
        return max(0.0, min(1.0, predicted_success + strategy_bonus + reflection_bonus - difficulty_penalty))