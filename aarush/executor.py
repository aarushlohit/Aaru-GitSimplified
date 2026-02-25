"""
executor.py
-----------
Every git command in Aaru goes through this file. No exceptions.

The execute() function is the single choke-point that:
  1. Asks policy: "are we even allowed to run this?"
  2. Runs the actual git command via subprocess
  3. Asks diagnostics: "did something go wrong that we should name?"
  4. Prints a hint to the user if there's an actionable problem
  5. Writes a log entry so we have a full audit trail

Return value (always a dict so callers get consistent data):
  {
    "ok":          True / False,
    "status":      "success" | "failed" | "blocked",
    "stdout":      "...",
    "stderr":      "...",
    "risk_level":  "low" | "medium" | "high",
    "diagnostics": { "type": "...", "message": "..." },
    "policy":      { "risk_level": "...", "has_diagnostics": bool, ... },
  }
"""

from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Optional

from . import diagnostics
from . import hints
from . import logger
from . import policy


def execute(
    *,
    aaru_command: str,        # The Aaru verb — e.g. "save", "sync", "raw"
    git_command: list[str],   # The actual git args — e.g. ["commit", "-m", "fix"]
    ai_model: Optional[str] = None,   # Pass the model name if called from an AI agent
    ai_prompt: Optional[str] = None,  # Pass the prompt that triggered this, if any
    yes: bool = False,                # User explicitly confirmed a high-risk action
    cwd: Optional[Path] = None,       # Run in this directory (defaults to cwd)
) -> dict:
    """Run one git command through the full Aaru safety pipeline.

    See module docstring for return shape.
    """

    # ── Step 1: Policy pre-flight ──────────────────────────────────────────────
    # Before touching git at all, ask policy whether this command is allowed.
    # Blocked commands (force-push, hard-reset, etc.) are stopped here.
    allowed, block_message, risk_level = policy.preflight(
        git_command,
        require_confirmation=yes,
    )

    if not allowed:
        # Command was rejected — log it and return immediately without running git
        blocked_result = {
            "ok":          False,
            "status":      "blocked",
            "stdout":      "",
            "stderr":      block_message,    # Tells the user *why* it was blocked
            "risk_level":  risk_level,
            "diagnostics": {"type": "none", "message": "Command blocked before execution."},
            "policy":      {"risk_level": risk_level, "blocked": True},
        }
        logger.log(
            aaru_command=aaru_command,
            git_command=git_command,
            stdout="",
            stderr=block_message,
            status="blocked",
            risk_level=risk_level,
            ai_model=ai_model,
            ai_prompt=ai_prompt,
            cwd=cwd,
        )
        return blocked_result

    # ── Step 2: Run the git command ────────────────────────────────────────────
    # We prepend "git" so callers only pass the sub-command args.
    # capture_output=True keeps stdout/stderr off the terminal until we decide
    # what to do with them.
    process = subprocess.run(
        ["git", *git_command],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )

    stdout = process.stdout.strip()
    stderr = process.stderr.strip()
    status = "success" if process.returncode == 0 else "failed"

    # ── Step 3: Diagnose what happened ────────────────────────────────────────
    # Even a failed command may have a specific named cause (conflict, detached
    # HEAD, etc.). diagnostics.check() figures out which one.
    diag = diagnostics.check(
        git_command=git_command,
        returncode=process.returncode,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
    )

    # ── Step 4: Post-run policy summary ───────────────────────────────────────
    # classify_risk() is cheap to call again; this also checks diagnostics data.
    policy_summary = policy.validate(git_command, diag)
    risk_level = policy_summary.get("risk_level", risk_level)

    # ── Step 5: Print a hint if something needs the user's attention ──────────
    # This is purely advisory — nothing is auto-fixed.
    hints.print_hints(diag)

    # ── Step 6: Write the log entry ───────────────────────────────────────────
    logger.log(
        aaru_command=aaru_command,
        git_command=git_command,
        stdout=stdout,
        stderr=stderr,
        status=status,
        risk_level=risk_level,
        ai_model=ai_model,
        ai_prompt=ai_prompt,
        cwd=cwd,
    )

    # ── Return everything the caller might need ────────────────────────────────
    return {
        "ok":          process.returncode == 0,
        "status":      status,
        "stdout":      stdout,
        "stderr":      stderr,
        "risk_level":  risk_level,
        "diagnostics": diag,
        "policy":      policy_summary,
    }
