"""
hints.py
--------
Prints a plain-English next-step message when something goes wrong.

This module ONLY prints advice — it never modifies files, never runs git,
never auto-fixes anything. The user always stays in control.

Calling order:
  diagnostics.check()  →  returns a result dict
  hints.print_hints()  →  prints one helpful line based on that result
"""

from __future__ import annotations


# ── Hint lookup ────────────────────────────────────────────────────────────────

# Maps each diagnostic type to a plain sentence the user can act on.
_HINTS: dict[str, str] = {
    "merge_conflict": (
        "Resolve the conflicted files manually, "
        "then run: git add <file> and continue your merge/rebase."
    ),
    "rebase_in_progress": (
        "Finish the rebase with 'git rebase --continue', "
        "or cancel it with 'git rebase --abort'."
    ),
    "detached_head": (
        "You're not on a branch. "
        "Create one first: git switch -c <branch-name>."
    ),
    "non_fast_forward_push": (
        "The remote has commits you don't have locally. "
        "Pull and rebase first, then push again."
    ),
    "dirty_working_tree": (
        "You have uncommitted changes. "
        "Commit or stash them before running this operation."
    ),
    "command_failed": (
        "Review the output above, fix the issue, and run the command again."
    ),
}


def get_hint(diagnostics_result: dict) -> str:
    """Return the hint string for a given diagnostics result, or empty string if none."""
    issue_type = diagnostics_result.get("type", "none")
    return _HINTS.get(issue_type, "")


def print_hints(diagnostics_result: dict) -> None:
    """Print a single Hint: line if there is something actionable to say.

    Prints nothing when the command succeeded cleanly.
    """
    hint = get_hint(diagnostics_result)
    if hint:
        print(f"Hint: {hint}")
