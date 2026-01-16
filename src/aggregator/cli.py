
"""
CLI entrypoint for Git-Based Log Aggregator.

Usage:
  python -m aggregator --help
"""
from __future__ import annotations
from .config import load_config, ensure_dirs
from .collect import collect_sources
from .normalize import normalize_lines
from .store import store_normalized
import argparse
import sys
from . import __app_name__, __version__

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog=__app_name__,
        description="Git-first log aggregation and analysis tool."
    )
    p.add_argument("--version", action="store_true", help="Show version and exit.")
    sub = p.add_subparsers(dest="command")

    # Plan ahead: we’ll wire these as modules land
    sub.add_parser("collect", help="Collect logs from configured sources.")
    sub.add_parser("normalize", help="Normalize timestamps/format.")
    sub.add_parser("store", help="Store normalized logs into data/logs.")
    sub.add_parser("analyze", help="Analyze logs and produce summary.")
    sub.add_parser("run", help="Run end-to-end pipeline (collect→normalize→store→analyze).")

    return p

def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"{__app_name__} {__version__}")
        return 0

    if not args.command:
        parser.print_help()
        return 0
        
    if args.command == "collect":
        cfg = load_config()
        ensure_dirs(cfg)
        data = collect_sources(cfg["sources"])
        if not data:
            print("No logs collected. Check 'sources' in config.")
            return 0
        for name, lines in data.items():
            print(f"{name}: {len(lines)} lines")
        return 0

    if args.command == "normalize":
        cfg = load_config()
        ensure_dirs(cfg)
        data = collect_sources(cfg["sources"])
        total = 0
        for name, lines in data.items():
            norm = normalize_lines(lines, local_tz=cfg["timezone"], normalize_mode=cfg["normalize_timestamp"])
            print(f"{name}: {len(norm)} normalized lines")
            # show first 3 as a preview
            for sample in norm[:3]:
                print("  ", sample)
            total += len(norm)
        if total == 0:
            print("No lines to normalize.")
        return 0

    if args.command == "store":
        cfg = load_config()
        ensure_dirs(cfg)
        data = collect_sources(cfg["sources"])
        normalized = {name: normalize_lines(lines, cfg["timezone"], cfg["normalize_timestamp"])
                      for name, lines in data.items()}
        written = store_normalized(normalized, cfg["output_dir"])
        for p in written:
            print(f"Wrote: {p}")
        if not written:
            print("No normalized logs written.")
        return 0

    if args.command == "run":
        cfg = load_config()
        ensure_dirs(cfg)
        data = collect_sources(cfg["sources"])
        normalized = {n: normalize_lines(v, cfg["timezone"], cfg["normalize_timestamp"]) for n, v in data.items()}
        written = store_normalized(normalized, cfg["output_dir"])
        print(f"Stored {len(written)} file(s). Next: analyze (next branch).")
        return 0

    # Stubs for now
    print(f"Command '{args.command}' not implemented yet. Coming soon.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

