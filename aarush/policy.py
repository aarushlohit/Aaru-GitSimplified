"""
policy.py
---------
Guardrails that decide whether a git command is allowed to run.

This module answers two questions:
  1. Should we refuse to run this command at all? (blocked commands)
  2. How dangerous is this command? (risk classification)

Blocked forever (no override):
  - push --force       → would overwrite remote history
  - reset --hard       → destroys local uncommitted work
  - delete a protected branch (main, master, develop, production)

High-risk (needs --yes to proceed):
  - anything else classified as "high" that isn't outright blocked

Medium-risk (allowed, just logged):
  - push, merge, rebase

Low-risk (runs without any fuss):
  - everything else
"""

from __future__ import annotations

from typing import Optional

from .config import PROTECTED_BRANCHES


# ── Risk classification ────────────────────────────────────────────────────────

def classify_risk(git_command: list[str]) -> str:
    """Look at the git command and return how dangerous it is.

    Returns one of: 'low', 'medium', 'high'
    """
    # Force-push rewrites shared history — always high risk
    if "push" in git_command and "--force" in git_command:
        return "high"

    # Hard reset throws away uncommitted work with no recovery — always high risk
    if "reset" in git_command and "--hard" in git_command:
        return "high"

    # Deleting a branch: high if it's a protected branch, medium otherwise
    if len(git_command) >= 3 and git_command[0] == "branch" and git_command[1] in {"-d", "-D"}:
        branch_to_delete = git_command[2]
        if branch_to_delete in PROTECTED_BRANCHES:
            return "high"
        return "medium"

    # Rebase and merge rewrite or combine history — worth noting
    if "rebase" in git_command or "merge" in git_command:
        return "medium"

    # A plain push affects the remote — medium but allowed
    if "push" in git_command:
        return "medium"

    # Everything else (status, log, diff, add, etc.) is safe
    return "low"


# ── Block list ─────────────────────────────────────────────────────────────────

def _is_blocked(git_command: list[str]) -> tuple[bool, Optional[str]]:
    """Check if the command is on the permanent block list.

    Returns (is_blocked, reason_message).
    Blocked commands can never run — not even with --yes.
    """
    if "push" in git_command and "--force" in git_command:
        return True, "Blocked by policy: push --force is not allowed."

    if "reset" in git_command and "--hard" in git_command:
        return True, "Blocked by policy: reset --hard is not allowed."

    # Check if someone is trying to delete a protected branch
    if len(git_command) >= 3 and git_command[0] == "branch" and git_command[1] in {"-d", "-D"}:
        branch_to_delete = git_command[2]
        if branch_to_delete in PROTECTED_BRANCHES:
            return True, f"Blocked by policy: deleting protected branch '{branch_to_delete}' is not allowed."

    return False, None


# ── Pre-run gate ───────────────────────────────────────────────────────────────

def preflight(
    git_command: list[str],
    *,
    require_confirmation: bool,  # True when the user passed --yes
) -> tuple[bool, str, str]:
    """Run all safety checks before the command is executed.

    Call this before subprocess.run().
    Returns: (allowed, reason_message, risk_level)

    - If allowed is False, print the message and stop.
    - risk_level is passed along so it can be logged.
    """
    risk_level = classify_risk(git_command)
    is_blocked, block_reason = _is_blocked(git_command)

    # Hard block — refuse no matter what
    if is_blocked:
        return False, block_reason or "Blocked by policy.", risk_level

    # High-risk commands need the user to explicitly say --yes
    if risk_level == "high" and not require_confirmation:
        return (
            False,
            "High-risk command requires explicit confirmation. Re-run with --yes.",
            risk_level,
        )

    return True, "Allowed", risk_level


# ── Post-run summary ───────────────────────────────────────────────────────────

def validate(git_command: list[str], diagnostics_result: dict) -> dict:
    """Produce a policy summary after the command has already run.

    This is merged into the executor's return value and then logged.
    It does not block anything — it's purely informational.
    """
    risk_level = classify_risk(git_command)
    issue_type = diagnostics_result.get("type", "none")

    return {
        "risk_level":       risk_level,
        "has_diagnostics":  issue_type != "none",  # True if something went wrong
        "diagnostics_type": issue_type,
    }
