"""
commands/workflow.py
--------------------
Workflow commands: multi-step operations that combine git primitives.
  save    → git add -A + git commit -m "<message>"
  history → git log (via registry)
  diff    → git diff   (via registry)
  undo    → git reset HEAD~1 (soft) — keeps changes staged
"""

from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info


def save(message: str) -> None:
    """
    Stage all changes and commit with the given message.
    Equivalent to: git add -A && git commit -m "<message>"
    """
    if not message or not message.strip():
        error("Commit message cannot be empty.")
        return

    # Stage all changes
    ok, out = run_git_command(["add", "-A"])
    if not ok:
        error(f"Staging failed: {out}")
        return

    info("All changes staged.")

    # Commit
    ok, out = run_git_command(["commit", "-m", message.strip()])
    if not ok:
        error(f"Commit failed: {out}")
        return

    success(f"Saved: {out}")


def undo(confirm: bool = False) -> None:
    """
    Soft-undo the last commit — keeps changes in the working tree.
    Equivalent to: git reset HEAD~1
    Requires --confirm to actually run (safety gate).
    """
    if not confirm:
        ok, last = run_git_command(["log", "-1", "--oneline"])
        preview = last.strip() if ok else "(could not read last commit)"
        error(
            f"Undo was NOT run.\n"
            f"  Would undo: {preview}\n"
            f"  Add --confirm to proceed."
        )
        return

    ok, out = run_git_command(["reset", "HEAD~1"])
    if not ok:
        error(f"Undo failed: {out}")
        return

    success("Last commit undone. Changes are back in your working tree.")
    info(out)
