"""
CLI entrypoint for Git-Based Log Aggregator.

Usage:
  python -m aggregator --help
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __app_name__, __version__
from .config import load_config, ensure_dirs
from .collect import collect_sources
from .normalize import normalize_lines
from .store import store_normalized
from .analyze import analyze_files, write_summary
from .gitops import stage_and_commit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description="Git-first log aggregation and analysis tool.",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit.",
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("collect", help="Collect logs from configured sources.")
    sub.add_parser("normalize", help="Normalize timestamps and formats.")
    sub.add_parser("store", help="Store normalized logs.")
    sub.add_parser("analyze", help="Analyze logs and generate report.")

    run_p = sub.add_parser(
        "run",
        help="Run full pipeline (collect -> normalize -> store -> analyze).",
    )
    run_p.add_argument(
        "--commit",
        action="store_true",
        help="Stage and commit generated artifacts.",
    )

    return parser


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

    cfg = load_config()
    ensure_dirs(cfg)

    if args.command == "collect":
        data = collect_sources(cfg["sources"])
        if not data:
            print("No logs collected.")
            return 0

        for name, lines in data.items():
            print(f"{name}: {len(lines)} lines")
        return 0

    if args.command == "normalize":
        data = collect_sources(cfg["sources"])
        total = 0

        for name, lines in data.items():
            normalized = normalize_lines(
                lines,
                local_tz=cfg["timezone"],
                normalize_mode=cfg["normalize_timestamp"],
            )
            print(f"{name}: {len(normalized)} normalized lines")
            for sample in normalized[:3]:
                print("  ", sample)
            total += len(normalized)

        if total == 0:
            print("No lines to normalize.")
        return 0

    if args.command == "store":
        data = collect_sources(cfg["sources"])
        normalized = {
            name: normalize_lines(
                lines,
                cfg["timezone"],
                cfg["normalize_timestamp"],
            )
            for name, lines in data.items()
        }

        written = store_normalized(normalized, cfg["output_dir"])
        if not written:
            print("No logs written.")
            return 0

        for path in written:
            print(f"Wrote: {path}")
        return 0

    if args.command == "analyze":
        files = list(Path(cfg["output_dir"]).glob("*.log"))
        if not files:
            print("No log files found. Run 'store' or 'run' first.")
            return 0

        summary = analyze_files(files)
        out = write_summary(cfg["report_dir"], summary)
        print(f"Wrote summary: {out}")
        return 0

    if args.command == "run":
        data = collect_sources(cfg["sources"])
        if not data:
            print("No data collected.")
            return 0

        normalized = {
            name: normalize_lines(
                lines,
                cfg["timezone"],
                cfg["normalize_timestamp"],
            )
            for name, lines in data.items()
        }

        written = store_normalized(normalized, cfg["output_dir"])
        files = list(Path(cfg["output_dir"]).glob("*.log"))

        summary = analyze_files(files)
        out = write_summary(cfg["report_dir"], summary)

        print(
            f"Pipeline complete. "
            f"Stored {len(written)} file(s). "
            f"Summary at: {out}"
        )

        if args.commit:
            msg = cfg["commit_message_format"].format(
                date=out.stem.replace("summary-", "")
            )
            _, commit_rc = stage_and_commit([*written, out], msg)
            if commit_rc == 0:
                print(f"Committed with message: {msg}")
            else:
                print("Warning: git commit failed.")

        return 0

    print(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())