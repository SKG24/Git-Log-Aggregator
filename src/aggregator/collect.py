
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Iterable
import glob
import os

def _is_glob(pattern: str) -> bool:
    return any(ch in pattern for ch in ["*", "?", "["])

def _iter_log_files_from_source(src: str) -> Iterable[Path]:
    p = Path(src)
    # Glob pattern support (cross-platform)
    if _is_glob(src):
        for m in glob.glob(src, recursive=True):
            mp = Path(m)
            if mp.is_file():
                yield mp
        return

    # Direct file
    if p.is_file():
        yield p
        return

    # Directory → gather *.log (recursive)
    if p.is_dir():
        # Accept *.log and *.txt (some logs use .txt)
        for mp in p.rglob("*"):
            if mp.is_file() and mp.suffix.lower() in {".log", ".txt"}:
                yield mp
        return

    # If it doesn't exist, ignore silently (user may add later)
    return

def source_name_from_path(path: Path) -> str:
    """
    Derive a stable source name: last directory + filename without extension
    Example: /var/log/app/app1.log -> app_app1
    """
    stem = path.stem
    parent = path.parent.name
    name = f"{parent}_{stem}" if parent else stem
    # sanitize
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name)
    return safe or "unknown"

def collect_sources(sources: List[str]) -> Dict[str, List[str]]:
    """
    Return dict: {source_name: [lines, ...]}
    """
    collected: Dict[str, List[str]] = {}
    for src in sources:
        for fpath in _iter_log_files_from_source(src):
            sname = source_name_from_path(fpath)
            try:
                with fpath.open("r", encoding="utf-8", errors="replace") as f:
                    lines = f.read().splitlines()
            except Exception:
                # Fallback with cp1252 on Windows if needed
                with fpath.open("r", encoding="cp1252", errors="replace") as f:
                    lines = f.read().splitlines()

            collected.setdefault(sname, []).extend(lines)
    return collected