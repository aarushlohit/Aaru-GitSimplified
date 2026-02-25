"""
logger.py
---------
Writes a record to .vibe/logs/session.jsonl after every git command.

Each line in that file is a self-contained JSON object describing exactly
what ran, when, on which branch, and whether it succeeded.
This gives you a full audit trail of everything Aaru has done.

Log format (one JSON object per line):
  {
    "timestamp":   "2026-02-24T10:30:00+00:00",
    "branch":      "main",
    "aaru_command":  "save",
    "git_command": "commit -m fix typo",
    "stdout":      "[main abc1234] fix typo",
    "stderr":      "",
    "status":      "success",   # success | failed | blocked
    "ai_model":    null,        # filled in when called from an AI agent
    "ai_prompt":   null,        # the prompt that triggered this command
    "risk_level":  "low"
  }
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from .config import LOG_RELATIVE_PATH
from .utils import get_current_branch, get_repo_root, utc_timestamp


def _get_log_file(cwd: Optional[Path] = None) -> Path:
    """Work out the full path to session.jsonl and create the folder if missing."""
    repo_root = get_repo_root(cwd=cwd)
    log_file = repo_root / LOG_RELATIVE_PATH

    # Make sure .vibe/logs/ exists before we try to write to it
    log_file.parent.mkdir(parents=True, exist_ok=True)

    return log_file


def log(
    *,
    aaru_command: str,       # e.g. "save", "sync", "raw"
    git_command: list[str],  # e.g. ["commit", "-m", "fix typo"]
    stdout: str,
    stderr: str,
    status: str,             # "success", "failed", or "blocked"
    risk_level: str,         # "low", "medium", or "high"
    ai_model: Optional[str] = None,   # e.g. "gpt-4o" — set externally
    ai_prompt: Optional[str] = None,  # the prompt that kicked off this command
    cwd: Optional[Path] = None,
) -> None:
    """Append one line to session.jsonl recording everything about this command.

    The file is append-only — nothing is ever overwritten or deleted.
    One line = one git command execution.
    """
    entry: dict[str, Any] = {
        "timestamp":    utc_timestamp(),
        "branch":       get_current_branch(cwd=cwd),
        "aaru_command": aaru_command,
        "git_command":  " ".join(git_command),
        "stdout":       stdout,
        "stderr":       stderr,
        "status":       status,
        "ai_model":     ai_model,
        "ai_prompt":    ai_prompt,
        "risk_level":   risk_level,
    }

    log_file = _get_log_file(cwd=cwd)

    # Open in append mode so we never overwrite previous entries
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
