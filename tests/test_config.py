
from pathlib import Path
from aggregator.config import load_config, ensure_dirs

def test_load_config_defaults(tmp_path: Path):
    # Create a minimal repo-like structure without config files
    (tmp_path / "config").mkdir()
    cfg = load_config(tmp_path)
    assert "sources" in cfg
    assert "output_dir" in cfg
    assert cfg["normalize_timestamp"] in ("UTC", "Asia/Kolkata")

def test_ensure_dirs(tmp_path: Path):
    (tmp_path / "config").mkdir()
    # Write a base config to tmp
    (tmp_path / "config" / "aggregator.json").write_text(
        '{"output_dir":"data/logs","report_dir":"data/reports"}',
        encoding="utf-8"
    )
    cfg = load_config(tmp_path)
    ensure_dirs(cfg)
    assert (tmp_path / "data" / "logs").exists()
    assert (tmp_path / "data" / "reports").exists()
