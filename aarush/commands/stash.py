"""
commands/stash.py
-----------------
Stash management commands.
  stash      → git stash push
  stash_pop  → git stash pop
  stash_list → git stash list
"""

from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info


def stash(message: str | None = None) -> None:
    """
    Stash current working-tree changes.
    Optionally tag the stash with a descriptive message.
    """
    args = ["stash", "push"]
    if message and message.strip():
        args += ["-m", message.strip()]

    ok, out = run_git_command(args)
    if not ok:
        error(f"Stash failed: {out}")
        return

    success("Changes stashed.")
    info(out)


def stash_pop() -> None:
    """Apply the most recent stash and remove it from the stash list."""
    ok, out = run_git_command(["stash", "pop"])
    if not ok:
        error(f"Stash pop failed: {out}")
        return

    success("Stash applied and removed.")
    info(out)


def stash_list() -> None:
    """List all stashed changesets."""
    ok, out = run_git_command(["stash", "list"])
    if not ok:
        error(f"Failed to list stashes: {out}")
        return

    if not out:
        info("No stashes found.")
        return

    info("Stash list:")
    print(out)
