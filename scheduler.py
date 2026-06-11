#!/usr/bin/env python3
"""
scheduler.py — Black Sea Monitor scraper pipeline scheduler

Usage:
    python scheduler.py            # start scheduler (runs indefinitely)
    python scheduler.py --run-now  # run all scripts immediately then exit

Intervals:
    daily   — avito_rental.py, civilian_confidence.py
    weekly  — domclick.py, restate.py
    monthly — refinery_pressure.py
    always  — compute.py --write  (after every fetch run)
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.resolve()
FETCH = ROOT / "fetch"
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)

PYTHON = sys.executable  # use the same interpreter that launched this script


# ---------------------------------------------------------------------------
# Logging setup — two handlers: update.log (INFO+) and errors.log (WARNING+)
# ---------------------------------------------------------------------------

def _rotating(name: str, level: int) -> TimedRotatingFileHandler:
    h = TimedRotatingFileHandler(
        LOGS / name, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    h.setLevel(level)
    h.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s"))
    return h


log = logging.getLogger("bsm")
log.setLevel(logging.DEBUG)
log.addHandler(_rotating("update.log", logging.INFO))
log.addHandler(_rotating("errors.log", logging.WARNING))

# Also echo INFO+ to stdout so nohup/terminal shows progress
_stdout = logging.StreamHandler(sys.stdout)
_stdout.setLevel(logging.INFO)
_stdout.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s"))
log.addHandler(_stdout)


# ---------------------------------------------------------------------------
# Script runner
# ---------------------------------------------------------------------------

def run_script(rel_path: str, extra_args: list[str] | None = None) -> bool:
    """Run a fetch script. Returns True on success, False on failure."""
    args = [PYTHON, str(FETCH / rel_path)] + (extra_args or [])
    label = rel_path
    log.info("START  %s", label)
    try:
        result = subprocess.run(
            args,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300,  # 5-minute hard timeout per script
        )
    except subprocess.TimeoutExpired:
        log.error("TIMEOUT  %s  (exceeded 300s)", label)
        return False
    except Exception as exc:
        log.error("ERROR  %s  — %s", label, exc)
        return False

    if result.returncode == 0:
        log.info("OK     %s", label)
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                log.debug("  [stdout] %s", line)
        return True
    else:
        log.warning(
            "FAIL   %s  (exit %d)\n  stdout: %s\n  stderr: %s",
            label,
            result.returncode,
            result.stdout.strip()[:500],
            result.stderr.strip()[:500],
        )
        return False


def run_compute() -> bool:
    """Always run compute.py --write after a fetch batch."""
    args = [PYTHON, str(FETCH / "compute.py"), "--write"]
    log.info("START  compute.py --write")
    try:
        result = subprocess.run(
            args, cwd=str(ROOT), capture_output=True, text=True, timeout=120
        )
    except Exception as exc:
        log.error("ERROR  compute.py — %s", exc)
        return False

    if result.returncode == 0:
        log.info("OK     compute.py --write")
        return True
    else:
        log.warning(
            "FAIL   compute.py (exit %d)\n  stdout: %s\n  stderr: %s",
            result.returncode,
            result.stdout.strip()[:500],
            result.stderr.strip()[:500],
        )
        return False


# ---------------------------------------------------------------------------
# Schedule state  (simple file-based — no external dependencies)
# ---------------------------------------------------------------------------

STATE_FILE = LOGS / ".last_run"


def _load_state() -> dict[str, datetime]:
    state: dict[str, datetime] = {}
    if STATE_FILE.exists():
        for line in STATE_FILE.read_text(encoding="utf-8").splitlines():
            parts = line.strip().split("\t")
            if len(parts) == 2:
                try:
                    state[parts[0]] = datetime.fromisoformat(parts[1])
                except ValueError:
                    pass
    return state


def _save_state(state: dict[str, datetime]) -> None:
    lines = [f"{k}\t{v.isoformat()}" for k, v in sorted(state.items())]
    STATE_FILE.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Job definitions
# ---------------------------------------------------------------------------

JOBS: list[dict] = [
    # script (relative to fetch/), interval, extra_args
    {"script": "avito_rental.py",         "interval": timedelta(days=1),  "args": ["--write"]},
    {"script": "civilian_confidence.py",  "interval": timedelta(days=1),  "args": ["--write"]},
    {"script": "domclick.py",             "interval": timedelta(weeks=1), "args": ["--write"]},
    {"script": "restate.py",              "interval": timedelta(weeks=1), "args": ["--write"]},
    {"script": "refinery_pressure.py",    "interval": timedelta(days=30), "args": ["--write"]},
]


def _is_due(key: str, interval: timedelta, state: dict[str, datetime]) -> bool:
    last = state.get(key)
    if last is None:
        return True
    return datetime.now() >= last + interval


# ---------------------------------------------------------------------------
# Run modes
# ---------------------------------------------------------------------------

def run_now(jobs: list[dict] | None = None) -> None:
    """Run all (or specified) jobs immediately, then compute."""
    targets = jobs or JOBS
    log.info("=== RUN-NOW: %d script(s) ===", len(targets))
    any_succeeded = False
    for job in targets:
        ok = run_script(job["script"], job.get("args"))
        if ok:
            any_succeeded = True
    if any_succeeded:
        run_compute()
    log.info("=== RUN-NOW complete ===")


def run_scheduler(poll_seconds: int = 60) -> None:
    """Main scheduler loop — checks every poll_seconds whether any job is due."""
    log.info("=== Black Sea Monitor scheduler started (poll=%ds) ===", poll_seconds)
    state = _load_state()

    while True:
        due_jobs = [j for j in JOBS if _is_due(j["script"], j["interval"], state)]

        if due_jobs:
            log.info("--- Tick: %d job(s) due ---", len(due_jobs))
            any_succeeded = False
            for job in due_jobs:
                ok = run_script(job["script"], job.get("args"))
                state[job["script"]] = datetime.now()
                if ok:
                    any_succeeded = True
            _save_state(state)
            if any_succeeded:
                run_compute()
        else:
            # Log next-due times once per hour (suppress the other ticks)
            now = datetime.now()
            if now.minute == 0:
                for job in JOBS:
                    last = state.get(job["script"])
                    nxt = (last + job["interval"]) if last else now
                    log.info("  next: %-32s → %s", job["script"], nxt.strftime("%Y-%m-%d %H:%M"))

        time.sleep(poll_seconds)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Black Sea Monitor scheduler")
    parser.add_argument(
        "--run-now",
        action="store_true",
        help="Run all fetch scripts immediately then exit (ignores schedule state)",
    )
    parser.add_argument(
        "--poll",
        type=int,
        default=60,
        help="Scheduler poll interval in seconds (default: 60)",
    )
    args = parser.parse_args()

    if args.run_now:
        run_now()
        sys.exit(0)
    else:
        run_scheduler(poll_seconds=args.poll)


if __name__ == "__main__":
    main()
