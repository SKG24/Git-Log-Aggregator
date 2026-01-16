
from pathlib import Path
from aggregator.store import store_normalized

def test_store_writes_files(tmp_path: Path):
    normalized = {"app_app1": ["2026-01-15T10:00:01Z INFO started"]}
    out = store_normalized(normalized, output_dir=str(tmp_path))
    assert len(out) == 1
    assert out[0].exists()
    assert out[0].read_text(encoding="utf-8").strip().endswith("started")