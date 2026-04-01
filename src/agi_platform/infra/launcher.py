from __future__ import annotations

from agi_platform.infra.topology import TrainingTopology


def build_launch_plan(mode: str = "local") -> list[str]:
    topology = TrainingTopology.default()
    if mode == "local":
        return [
            "set PYTHONPATH=src&& python -m agi_platform.main train --episodes 24",
            f"REM topology: {topology.describe()}",
        ]
    if mode == "ray":
        return [
            f"ray start --head --num-cpus=8 --num-gpus={max(1, topology.total_gpus())}",
            "python -m agi_platform.main train --episodes 24",
        ]
    if mode == "slurm":
        return [
            "sbatch --job-name=agi-train --wrap=\"python -m agi_platform.main train --episodes 24\"",
            f"# topology: {topology.describe()}",
        ]
    raise ValueError(f"Unsupported mode: {mode}")