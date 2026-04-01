from __future__ import annotations

from dataclasses import dataclass, field

from .schemas import TaskSpec


DOMAIN_SKILLS = {
    "reasoning": ["abductive inference", "causal compression", "hypothesis ranking"],
    "planning": ["long-horizon decomposition", "resource allocation", "constraint tracking"],
    "tool_use": ["tool selection", "verification", "result synthesis"],
    "introspection": ["calibration", "error attribution", "self-correction"],
}


@dataclass(slots=True)
class SyntheticTaskFactory:
    domains: list[str] = field(default_factory=lambda: list(DOMAIN_SKILLS.keys()))

    def generate(self, level: int, index: int) -> TaskSpec:
        domain = self.domains[(level + index) % len(self.domains)]
        skill = DOMAIN_SKILLS[domain][(level * 3 + index) % len(DOMAIN_SKILLS[domain])]
        task_id = f"{domain}-{level:02d}-{index:03d}"
        prompt = (
            f"Solve a {domain} challenge at difficulty {level}. "
            f"Primary target: {skill}. Explain strategy and provide a self-check."
        )
        success = (
            f"Demonstrate {skill}, maintain internal consistency, and articulate uncertainty."
        )
        return TaskSpec(
            task_id=task_id,
            domain=domain,
            difficulty=level,
            target_skill=skill,
            prompt=prompt,
            success_criteria=success,
            metadata={"curriculum_level": level, "generator": "synthetic"},
        )

    def curriculum(self, levels: int, samples_per_level: int) -> list[TaskSpec]:
        tasks: list[TaskSpec] = []
        for level in range(1, levels + 1):
            for index in range(samples_per_level):
                tasks.append(self.generate(level=level, index=index))
        return tasks