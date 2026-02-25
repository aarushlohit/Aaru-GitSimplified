"""
utils.py
--------
Small helper functions used across multiple Aaru modules.

Nothing business-logic here — just boring plumbing:
  - run a subprocess quietly
  - find the repo root
  - get the current branch name
  - generate a timestamp
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess
from typing import Optional


def utc_timestamp() -> str:
    """Return the current time as an ISO-8601 string in UTC.

    Example output: '2026-02-24T10:30:00.000000+00:00'
    Used when writing log entries so every record has a precise timestamp.
    """
    return datetime.now(timezone.utc).isoformat()


def run_quiet_command(args: list[str], cwd: Optional[Path] = None) -> tuple[bool, str]:
    """Run any shell command and return (success, output) without printing anything.

    - On success  → returns (True,  stdout text)
    - On failure  → returns (False, stderr text)

    Used internally to ask git questions (e.g. 'what branch am I on?')
    without those calls showing up in the user's terminal.
    """
    result = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,   # swallow stdout + stderr
        text=True,             # give us strings, not bytes
    )

    if result.returncode == 0:
        return True, result.stdout.strip()

    # Prefer stderr for error messages; fall back to stdout if stderr is empty
    error_output = (result.stderr or result.stdout).strip()
    return False, error_output


def get_repo_root(cwd: Optional[Path] = None) -> Path:
    """Ask git where the repository root folder is.

    Falls back to the current working directory if we're not inside a git repo.
    This is needed so the logger always writes logs to the right place.
    """
    ok, root_path = run_quiet_command(["git", "rev-parse", "--show-toplevel"], cwd=cwd)
    if ok and root_path:
        return Path(root_path)

    # Not a git repo — use cwd as a safe fallback
    return cwd or Path.cwd()


def get_current_branch(cwd: Optional[Path] = None) -> str:
    """Return the name of the currently checked-out branch.

    Returns 'unknown' if git isn't available or the repo is in a weird state.
    This is logged with every command so you can trace what happened on which branch.
    """
    ok, branch_name = run_quiet_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    if ok and branch_name:
        return branch_name
    return "unknown"
