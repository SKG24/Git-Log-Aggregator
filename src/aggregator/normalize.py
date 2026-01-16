
from __future__ import annotations
import re
from datetime import datetime
from typing import Iterable, List, Tuple
from zoneinfo import ZoneInfo

ISO_RE = re.compile(
    r"^(?P<ts>"
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}"
    r"(?:\.\d{1,6})?"
    r"(?:Z|[+-]\d{2}:\d{2})?"
    r")\s*(?P<rest>.*)$"
)

SEVERITY_RE = re.compile(r"\b(ERROR|WARN|WARNING|INFO|DEBUG|CRITICAL)\b", re.IGNORECASE)

def _to_iso_utc(ts_str: str, local_tz: str, normalize_mode: str) -> str:
    # Try parsing common ISO first
    dt = None
    try:
        # Handle basic forms; if no tzinfo present, assume local_tz
        if ts_str.endswith("Z") or re.search(r"[+-]\d{2}:\d{2}$", ts_str):
            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(ts_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=ZoneInfo(local_tz))
    except Exception:
        pass

    if dt is None:
        # If can't parse, assume now in local_tz
        now = datetime.now(ZoneInfo(local_tz))
        dt = now

    if normalize_mode.upper() == "UTC":
        dt = dt.astimezone(ZoneInfo("UTC"))

    return dt.isoformat(timespec="seconds").replace("+00:00", "Z") if dt.utcoffset().total_seconds() == 0 else dt.isoformat(timespec="seconds")

def _normalize_severity(text: str) -> str:
    m = SEVERITY_RE.search(text)
    if not m:
        # default to INFO if not found
        return "INFO", text
    sev = m.group(1).upper().replace("WARNING", "WARN")
    return sev, text

def normalize_lines(
    lines: Iterable[str],
    local_tz: str = "UTC",
    normalize_mode: str = "UTC"
) -> List[str]:
    """
    Normalize each line to:
      ISO8601 timestamp in UTC (or local), followed by severity, then message.

    If no timestamp found, inject current time.
    If no severity found, default INFO.
    """
    out: List[str] = []
    for raw in lines:
        raw = raw.strip("\n")
        m = ISO_RE.match(raw)
        if m:
            ts_str = m.group("ts")
            rest = m.group("rest").strip()
            iso = _to_iso_utc(ts_str, local_tz, normalize_mode)
            sev, rest2 = _normalize_severity(rest)
            out.append(f"{iso} {sev} {rest2}")
        else:
            # Missing timestamp; inject now
            iso = _to_iso_utc("", local_tz, normalize_mode)
            sev, rest2 = _normalize_severity(raw)
            out.append(f"{iso} {sev} {rest2}")
    return out
