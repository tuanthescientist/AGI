from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean

from agi_platform.cognition.agent import CognitiveAgent
from agi_platform.data.pipeline import DataPipeline

from .curriculum import AdaptiveCurriculum
from .objectives import ObjectiveWeights
from .self_improve import SelfImprovementEngine


@dataclass(slots=True)
class TrainingReport:
    episodes: int
    average_reward: float
    average_objective_score: float
    self_model_summary: str
    governance_events: int
    domain_rewards: dict[str, float]


@dataclass(slots=True)
class ResearchTrainer:
    agent: CognitiveAgent = field(default_factory=CognitiveAgent)
    pipeline: DataPipeline = field(default_factory=DataPipeline)
    curriculum: AdaptiveCurriculum = field(default_factory=AdaptiveCurriculum)
    objectives: ObjectiveWeights = field(default_factory=ObjectiveWeights)
    improver: SelfImprovementEngine = field(default_factory=SelfImprovementEngine)

    def train(self, episodes: int = 24, improvement_interval: int = 6) -> TrainingReport:
        tasks = self.pipeline.build_curriculum(levels=4, samples_per_level=max(episodes // 4, 2))
        rewards: list[float] = []
        objective_scores: list[float] = []
        by_domain: dict[str, list[float]] = {}

        for episode in range(episodes):
            stage = self.curriculum.stage_for_episode(episode, self.agent.self_model.improvement_priorities)
            eligible = [task for task in tasks if task.difficulty <= stage.level and task.domain in stage.focus_domains]
            task = eligible[episode % len(eligible)] if eligible else tasks[episode % len(tasks)]
            experience = self.agent.run_task(task)
            rewards.append(experience.reward)
            objective_scores.append(self.objectives.score(experience))
            by_domain.setdefault(experience.domain, []).append(experience.reward)

            if (episode + 1) % improvement_interval == 0:
                proposal = self.improver.propose(self.agent.self_model, self.agent.memory)
                self.improver.apply(self.agent.self_model, proposal, self.agent.governance)

        domain_rewards = {domain: round(mean(values), 3) for domain, values in by_domain.items()}
        return TrainingReport(
            episodes=episodes,
            average_reward=round(mean(rewards), 3),
            average_objective_score=round(mean(objective_scores), 3),
            self_model_summary=self.agent.self_model.narrative_summary(),
            governance_events=len(self.agent.governance.review_log),
            domain_rewards=domain_rewards,
        )