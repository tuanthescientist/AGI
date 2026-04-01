from __future__ import annotations

from pathlib import Path
import tomllib


def load_toml(path: str | Path) -> dict:
    with open(path, "rb") as handle:
        return tomllib.load(handle)