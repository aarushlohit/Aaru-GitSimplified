"""
diagnostics.py
--------------
Figures out *what went wrong* after a git command runs (or before).

Each check function is a simple yes/no question about the repo's current state.
The main entry point is check(), which runs all of them in priority order
and returns the first problem it finds.

Return value is always a dict:
  { "type": "<issue_name>", "message": "<human-readable description>" }

If nothing is wrong, it returns { "type": "none", ... }.

Possible issue types:
  merge_conflict        - files have conflict markers (<<<<<<<)
  non_fast_forward_push - remote has commits we don't have; push was rejected
  rebase_in_progress    - a rebase is paused mid-way
  detached_head         - not on any branch; commits would be lost
  dirty_working_tree    - uncommitted changes exist
  command_failed        - generic non-zero exit code
  none                  - everything is fine
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .utils import run_quiet_command


# ── Individual checks ──────────────────────────────────────────────────────────

def _contains_merge_conflict(stdout: str, stderr: str) -> bool:
    """True if git printed conflict-related keywords in its output."""
    combined = f"{stdout}\n{stderr}".lower()
    return "merge conflict" in combined or "conflict" in combined


def _contains_non_fast_forward(stdout: str, stderr: str) -> bool:
    """True if a push was rejected because the remote has newer commits."""
    combined = f"{stdout}\n{stderr}".lower()
    return "non-fast-forward" in combined or "failed to push some refs" in combined


def _is_rebase_in_progress(cwd: Optional[Path]) -> bool:
    """True if git left behind a rebase-in-progress folder inside .git/.

    Git creates 'rebase-merge' or 'rebase-apply' while a rebase is paused.
    If those folders exist, there's unfinished business.
    """
    ok, git_dir_path = run_quiet_command(["git", "rev-parse", "--git-dir"], cwd=cwd)
    if not ok or not git_dir_path:
        return False

    git_dir = Path(git_dir_path)

    # git rev-parse --git-dir can return a relative path (e.g. ".git")
    # Make it absolute so our .exists() checks work correctly
    if not git_dir.is_absolute() and cwd is not None:
        git_dir = cwd / git_dir

    return (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists()


def _is_detached_head(cwd: Optional[Path]) -> bool:
    """True if the repo is in detached HEAD state (not on any named branch).

    git returns the literal string 'HEAD' when you're not on a branch.
    Any commits made in this state are dangling and can be garbage-collected.
    """
    ok, branch_name = run_quiet_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    return ok and branch_name == "HEAD"


def _is_dirty_working_tree(cwd: Optional[Path]) -> bool:
    """True if there are uncommitted changes in the working directory.

    'git status --porcelain' prints one line per changed file.
    An empty output means the tree is clean.
    """
    ok, status_output = run_quiet_command(["git", "status", "--porcelain"], cwd=cwd)
    return ok and bool(status_output.strip())


# ── Main entry point ───────────────────────────────────────────────────────────

def check(
    *,
    git_command: list[str],
    returncode: int,
    stdout: str,
    stderr: str,
    cwd: Optional[Path] = None,
) -> dict:
    """Run all checks and return the first problem found.

    Checks are ordered from most specific to most generic.
    Always returns a dict with 'type' and 'message' keys.
    """
    # Did the output mention a merge conflict?
    if _contains_merge_conflict(stdout, stderr):
        return {"type": "merge_conflict", "message": "Merge conflict detected."}

    # Was a push rejected because the remote is ahead?
    if _contains_non_fast_forward(stdout, stderr):
        return {"type": "non_fast_forward_push", "message": "Push rejected (non-fast-forward)."}

    # Is a rebase paused waiting for the user to resolve something?
    if _is_rebase_in_progress(cwd):
        return {"type": "rebase_in_progress", "message": "A rebase operation is in progress."}

    # Not on any branch — commits made here could be lost
    if _is_detached_head(cwd):
        return {"type": "detached_head", "message": "Repository is in detached HEAD state."}

    # There are modified/untracked files that haven't been committed
    if _is_dirty_working_tree(cwd):
        return {"type": "dirty_working_tree", "message": "Working tree has uncommitted changes."}

    # The command just plain failed and none of the above explain why
    if returncode != 0:
        failed_cmd = " ".join(git_command)
        return {"type": "command_failed", "message": f"Command failed: {failed_cmd}"}

    # Nothing went wrong
    return {"type": "none", "message": "No issues detected."}
