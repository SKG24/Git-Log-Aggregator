
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

DEFAULTS: Dict[str, Any] = {
    "sources": [],
    "normalize_timestamp": "UTC",
    "commit_message_format": "logs: add {date} aggregated logs",
    "output_dir": "data/logs",
    "report_dir": "data/reports",
    "timezone": "UTC",
}

def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_config(root: Path | None = None) -> Dict[str, Any]:
    """
    Load config/aggregator.json + optional aggregator.override.json.
    Returns a merged dict with defaults applied.
    """
    root = root or Path.cwd()
    base = _load_json(root / "config" / "aggregator.json")
    override = _load_json(root / "config" / "aggregator.override.json")

    merged = {**DEFAULTS, **base, **override}

    # Basic validation
    if not isinstance(merged["sources"], list):
        raise ValueError("config: 'sources' must be a list of paths.")
    if not isinstance(merged["output_dir"], str):
        raise ValueError("config: 'output_dir' must be a string path.")
    if not isinstance(merged["report_dir"], str):
        raise ValueError("config: 'report_dir' must be a string path.")

    return merged

def ensure_dirs(cfg: Dict[str, Any], root: Path | None = None) -> None:
    root = root or Path.cwd()

    output_dir = root / cfg["output_dir"]
    report_dir = root / cfg["report_dir"]

    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
