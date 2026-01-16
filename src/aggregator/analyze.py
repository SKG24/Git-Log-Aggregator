
from __future__ import annotations
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Iterable, Tuple

def _today_ymd() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")

def analyze_files(files: Iterable[Path]) -> dict[str, Counter]:
    results: dict[str, Counter] = {}
    for fpath in files:
        if not fpath.exists() or not fpath.is_file():
            continue
        cnt = Counter({"ERROR": 0, "WARN": 0, "INFO": 0})
        with fpath.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if "ERROR" in line:
                    cnt["ERROR"] += 1
                if "WARN" in line:
                    cnt["WARN"] += 1
                if "INFO" in line:
                    cnt["INFO"] += 1
        results[fpath.name] = cnt
    return results

def write_summary(report_dir: str, analysis: dict[str, Counter], day: str | None = None) -> Path:
    day = day or _today_ymd()
    outdir = Path(report_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"summary-{day}.txt"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"{day} Summary:\n")
        for fname, cnt in sorted(analysis.items()):
            f.write(f"{fname}: {cnt['ERROR']} errors, {cnt['WARN']} warnings, {cnt['INFO']} info\n")
    return out
