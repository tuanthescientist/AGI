from __future__ import annotations

import argparse
from pathlib import Path

from agi_platform.config import load_toml
from agi_platform.infra.launcher import build_launch_plan
from agi_platform.training.trainer import ResearchTrainer


def _config_path(name: str) -> Path:
    return Path(__file__).resolve().parents[2] / "configs" / name


def command_demo() -> None:
    trainer = ResearchTrainer()
    report = trainer.train(episodes=8, improvement_interval=4)
    _print_report(report)


def command_train(episodes: int) -> None:
    trainer = ResearchTrainer()
    report = trainer.train(episodes=episodes, improvement_interval=max(2, episodes // 4))
    _print_report(report)


def command_architecture() -> None:
    model_cfg = load_toml(_config_path("model.toml"))
    train_cfg = load_toml(_config_path("train.toml"))
    print("AGI Research Platform Architecture")
    print("- cognitive loop: memory -> world model -> planner -> reflection")
    print("- self-model calibration and improvement priorities")
    print("- adaptive curriculum and multi-objective training")
    print(f"- model config: {model_cfg}")
    print(f"- train config: {train_cfg}")


def command_launch_plan(mode: str) -> None:
    for line in build_launch_plan(mode):
        print(line)


def _print_report(report: ResearchTrainer | object) -> None:
    print("=== Training Report ===")
    print(f"episodes: {report.episodes}")
    print(f"average_reward: {report.average_reward}")
    print(f"average_objective_score: {report.average_objective_score}")
    print(f"self_model_summary: {report.self_model_summary}")
    print(f"governance_events: {report.governance_events}")
    print(f"domain_rewards: {report.domain_rewards}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AGI research platform")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("demo", help="Run a short demonstration")

    train = sub.add_parser("train", help="Run a training loop")
    train.add_argument("--episodes", type=int, default=24)

    sub.add_parser("architecture", help="Print architecture details")

    plan = sub.add_parser("launch-plan", help="Print infrastructure launch plan")
    plan.add_argument("--mode", choices=["local", "ray", "slurm"], default="local")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "demo":
        command_demo()
    elif args.command == "train":
        command_train(args.episodes)
    elif args.command == "architecture":
        command_architecture()
    elif args.command == "launch-plan":
        command_launch_plan(args.mode)
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()