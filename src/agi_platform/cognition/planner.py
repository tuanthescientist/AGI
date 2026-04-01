from __future__ import annotations

from dataclasses import dataclass

from agi_platform.data.schemas import TaskSpec
from agi_platform.safety.governance import GovernancePolicy

from .self_model import SelfModel
from .world_model import WorldModel


@dataclass(slots=True)
class Planner:
    exploration_bias: float = 0.2

    def candidate_actions(self, task: TaskSpec, self_model: SelfModel) -> list[str]:
        low_confidence = task.domain in self_model.improvement_priorities
        common = [
            f"plan -> solve -> self-check for {task.target_skill}",
            f"retrieve priors -> attempt -> verify constraints for {task.target_skill}",
            f"decompose problem -> reason carefully -> calibrate answer for {task.target_skill}",
        ]
        if low_confidence:
            common.append(f"probe weakness -> request internal critique -> self-check for {task.target_skill}")
        return common

    def choose_action(
        self,
        task: TaskSpec,
        self_model: SelfModel,
        world_model: WorldModel,
        governance: GovernancePolicy,
    ) -> tuple[str, float, float]:
        best = ("reflect only", 0.0, 1.0)
        for action in self.candidate_actions(task, self_model):
            if not governance.review_action(action):
                continue
            predicted, uncertainty = world_model.predict_success(task, action, self_model)
            score = predicted - uncertainty * 0.35 + self.exploration_bias * (1.0 - predicted)
            if score > best[1] - best[2] * 0.35:
                best = (action, predicted, uncertainty)
        return best