
from pathlib import Path
from aggregator.analyze import analyze_files, write_summary

def test_analyze_and_write(tmp_path: Path):
    f = tmp_path / "2026-01-15_app.log"
    f.write_text(
        "2026-01-15T10:00:00Z INFO start\n"
        "2026-01-15T10:01:00Z WARN low\n"
        "2026-01-15T10:02:00Z ERROR boom\n", encoding="utf-8"
    )
    res = analyze_files([f])
    assert res[f.name]["ERROR"] == 1
    out = write_summary(str(tmp_path), res, day="2026-01-15")
    assert out.exists()
    assert "1 errors" in out.read_text(encoding="utf-8")