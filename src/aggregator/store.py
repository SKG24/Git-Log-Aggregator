
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Dict, List

def _today_ymd() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")

def _safe_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name)

def store_normalized(
    normalized: Dict[str, List[str]],
    output_dir: str,
    day: str | None = None
) -> list[Path]:
    """
    Write normalized lines to files:
      data/logs/<YYYY-MM-DD>_<source>.log
    Returns list of written file Paths.
    """
    out_paths: list[Path] = []
    day = day or _today_ymd()
    base = Path(output_dir)
    base.mkdir(parents=True, exist_ok=True)

    for src, lines in normalized.items():
        fname = f"{day}_{_safe_name(src)}.log"
        fpath = base / fname
        with fpath.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))
        out_paths.append(fpath)

    return out_paths