
from pathlib import Path
from aggregator.collect import collect_sources

def test_collect_from_dir(tmp_path: Path):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "app1.log").write_text("2026-01-15 10:00:01 INFO started\n", encoding="utf-8")
    (logs / "app2.txt").write_text("2026-01-15 10:00:02 ERROR fail\n", encoding="utf-8")
    data = collect_sources([str(logs)])
    assert len(data) == 2
    assert sum(len(v) for v in data.values()) == 2

def test_collect_from_glob(tmp_path: Path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "x.log").write_text("line1\n", encoding="utf-8")
    (tmp_path / "b" / "y.log").write_text("line2\n", encoding="utf-8")
    pattern = str(tmp_path / "**" / "*.log")
    data = collect_sources([pattern])
    assert sum(len(v) for v in data.values()) == 2
