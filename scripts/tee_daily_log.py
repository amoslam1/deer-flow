#!/usr/bin/env python3
"""Stream stdin to stdout and daily-rotated log files.

Usage:
  some_command 2>&1 | python3 scripts/tee_daily_log.py langgraph

Log layout:
  logs/archive/YYYY-MM-DD/<service>.log
  logs/<service>.log -> symlink to today's file
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import pathlib
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("service", help="Service name, e.g. langgraph/gateway/frontend/nginx")
    parser.add_argument(
        "--log-root",
        default="logs",
        help="Log root directory (default: logs)",
    )
    return parser.parse_args()


def ensure_symlink(link_path: pathlib.Path, target_path: pathlib.Path) -> None:
    try:
        if link_path.is_symlink() or link_path.exists():
            link_path.unlink()
        # Use relative target for portability.
        rel = os.path.relpath(target_path, start=link_path.parent)
        link_path.symlink_to(rel)
    except OSError:
        # Symlink may fail on some systems; ignore safely.
        pass


def main() -> int:
    args = parse_args()
    log_root = pathlib.Path(args.log_root)
    service = args.service

    current_date = None
    fp = None

    def switch_file(today: str) -> None:
        nonlocal current_date, fp
        if fp is not None:
            fp.close()
        current_date = today
        current_dir = log_root / "archive" / today
        current_dir.mkdir(parents=True, exist_ok=True)
        current_file = current_dir / f"{service}.log"
        fp = current_file.open("a", encoding="utf-8")
        ensure_symlink(log_root / f"{service}.log", current_file)

    try:
        # Create today's log file eagerly so users can verify file path even before first log line.
        switch_file(dt.datetime.now().strftime("%Y-%m-%d"))
        for line in sys.stdin:
            today = dt.datetime.now().strftime("%Y-%m-%d")
            if today != current_date:
                switch_file(today)

            sys.stdout.write(line)
            sys.stdout.flush()
            if fp is not None:
                fp.write(line)
                fp.flush()
    finally:
        if fp is not None:
            fp.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
