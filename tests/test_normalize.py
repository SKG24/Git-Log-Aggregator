from aggregator.normalize import normalize_lines

def test_normalize_iso():
    lines = ["2026-01-15 10:00:01 INFO started app", "2026-01-15T10:00:02Z warn low mem"]
    out = normalize_lines(lines, local_tz="UTC", normalize_mode="UTC")
    assert len(out) == 2
    assert out[0].startswith("2026-01-15T10:00:01Z")
    assert "INFO" in out[0]
    assert "WARN" in out[1]

def test_normalize_missing_ts_to_now():
    out = normalize_lines(["No timestamp here"], local_tz="UTC", normalize_mode="UTC")
    assert len(out) == 1
    assert "INFO" in out[0]  # default severity
