from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Iterable

def _run(cmd: list[str]) -> int:
    return subprocess.run(cmd, check=False).returncode

def stage_and_commit(paths: Iterable[Path], message: str) -> tuple[int, int]:
    """
    Stage given paths and commit with message.
    Returns (add_rc, commit_rc). Non-zero rc indicates failure.
    Note: Requires running inside a git repo.
    """
    add_rc = _run(["git", "add", *[str(p) for p in paths]])
    commit_rc = _run(["git", "commit", "-m", message])
    return add_rc, commit_rc
