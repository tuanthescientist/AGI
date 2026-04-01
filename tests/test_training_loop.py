from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agi_platform.cognition.agent import CognitiveAgent
from agi_platform.data.pipeline import DataPipeline
from agi_platform.training.trainer import ResearchTrainer


class TrainingLoopTests(unittest.TestCase):
    def test_agent_generates_experience(self) -> None:
        pipeline = DataPipeline()
        task = pipeline.build_curriculum(levels=1, samples_per_level=1)[0]
        agent = CognitiveAgent()
        experience = agent.run_task(task)

        self.assertGreaterEqual(experience.reward, 0.0)
        self.assertLessEqual(experience.reward, 1.0)
        self.assertIn(task.domain, agent.self_model.capability_scores)

    def test_research_trainer_runs(self) -> None:
        trainer = ResearchTrainer()
        report = trainer.train(episodes=10, improvement_interval=5)

        self.assertEqual(report.episodes, 10)
        self.assertGreater(report.average_reward, 0.0)
        self.assertTrue(report.domain_rewards)
        self.assertGreaterEqual(report.governance_events, 10)


if __name__ == "__main__":
    unittest.main()