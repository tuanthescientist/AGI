from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class NodeSpec:
    role: str
    replicas: int
    cpu: int = 4
    memory_gb: int = 16
    gpu: int = 0


@dataclass(slots=True)
class TrainingTopology:
    nodes: list[NodeSpec] = field(default_factory=list)

    @classmethod
    def default(cls) -> "TrainingTopology":
        return cls(
            nodes=[
                NodeSpec(role="controller", replicas=1, cpu=2, memory_gb=8),
                NodeSpec(role="trainer", replicas=2, cpu=8, memory_gb=32, gpu=1),
                NodeSpec(role="evaluator", replicas=1, cpu=4, memory_gb=16),
                NodeSpec(role="memory", replicas=1, cpu=4, memory_gb=24),
            ]
        )

    def total_gpus(self) -> int:
        return sum(node.gpu * node.replicas for node in self.nodes)

    def describe(self) -> str:
        parts = [
            f"{node.role} x{node.replicas} (cpu={node.cpu}, mem={node.memory_gb}GB, gpu={node.gpu})"
            for node in self.nodes
        ]
        return "; ".join(parts)