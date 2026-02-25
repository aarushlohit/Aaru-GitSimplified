"""
commands/branch.py
------------------
Branch management commands.
  create <branch> → git checkout -b <branch>
  switch <branch> → git checkout <branch>
  delete <branch> → git branch -d <branch>
"""

from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info


def create(branch: str, switch: bool = False) -> None:
    """Create a new branch. Stays on current branch unless switch=True."""
    if not branch or not branch.strip():
        error("Branch name cannot be empty.")
        return

    if switch:
        ok, out = run_git_command(["checkout", "-b", branch.strip()])
        if not ok:
            error(f"Failed to create branch '{branch}': {out}")
            return
        success(f"Created and switched to branch '{branch}'.")
    else:
        ok, out = run_git_command(["branch", branch.strip()])
        if not ok:
            error(f"Failed to create branch '{branch}': {out}")
            return
        success(f"Created branch '{branch}'. You're still on your current branch.")


def switch(branch: str) -> None:
    """Switch to an existing branch."""
    if not branch or not branch.strip():
        error("Branch name cannot be empty.")
        return

    ok, out = run_git_command(["checkout", branch.strip()])
    if not ok:
        error(f"Failed to switch to branch '{branch}': {out}")
        return

    success(f"Switched to branch '{branch}'.")
    info(out)


def delete(branch: str, force: bool = False, confirm: bool = False) -> None:
    """
    Delete a branch.
    - Default (safe):  refuses if branch has unmerged commits.
    - --force:         force-delete even if unmerged.
    - --confirm:       required safety gate to actually execute.
    """
    if not branch or not branch.strip():
        error("Branch name cannot be empty.")
        return

    if not confirm:
        label = "force-delete" if force else "delete"
        error(
            f"Branch '{branch}' was NOT deleted.\n"
            f"  Add --confirm to {label} it."
        )
        return

    flag = "-D" if force else "-d"
    ok, out = run_git_command(["branch", flag, branch.strip()])
    if not ok:
        if not force and "not fully merged" in out:
            error(
                f"Branch '{branch}' has unmerged commits — delete aborted.\n"
                f"  Use --force --confirm to force-delete it."
            )
        else:
            error(f"Failed to delete branch '{branch}': {out}")
        return

    label = "Force-deleted" if force else "Deleted"
    success(f"{label} branch '{branch}'.")


def list_branches() -> None:
    """List all local branches."""
    ok, out = run_git_command(["branch", "-a"])
    if not ok:
        error(f"Failed to list branches: {out}")
        return

    info("Branches:")
    print(out)
