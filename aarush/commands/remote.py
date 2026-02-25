"""
commands/remote.py
------------------
Remote interaction commands.
  send        → git push
  update      → git fetch
  sync        → git pull + git push  (full two-way sync)
  fork_sync   → fetch upstream, merge into current branch, push to origin
  add_upstream → add upstream remote for forks
  checkout_pr → checkout a pull request locally for testing
"""

from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info
import typer


def add_upstream(url: str = None) -> None:
    """
    Add the upstream remote for a forked repository.
    This is a one-time setup needed before using fork-sync.
    
    If URL is not provided, prompts the user to enter it.
    """
    # Check if upstream already exists
    ok, remotes = run_git_command(["remote"])
    if not ok:
        error(f"Could not list remotes: {remotes}")
        return
    
    remote_list = remotes.splitlines()
    if "upstream" in remote_list:
        info("Upstream remote already exists:")
        ok, upstream_url = run_git_command(["remote", "get-url", "upstream"])
        if ok:
            info(f"  upstream → {upstream_url.strip()}")
        
        # Ask if they want to update it
        update = typer.confirm("Do you want to update the upstream URL?")
        if not update:
            info("Keeping existing upstream remote.")
            return
        
        # Get new URL if not provided
        if not url:
            url = typer.prompt("Enter the new upstream repository URL")
        
        # Update existing upstream
        ok, out = run_git_command(["remote", "set-url", "upstream", url])
        if not ok:
            error(f"Failed to update upstream: {out}")
            return
        
        success(f"Upstream remote updated to: {url}")
        return
    
    # Upstream doesn't exist, add it
    if not url:
        info("Add the original repository as 'upstream' remote.")
        info("This is needed for fork-sync to work.")
        url = typer.prompt("Enter the upstream repository URL")
    
    ok, out = run_git_command(["remote", "add", "upstream", url])
    if not ok:
        error(f"Failed to add upstream: {out}")
        return
    
    success(f"Upstream remote added: {url}")
    info("You can now use 'aaru fork-sync' to sync with upstream!")


def send(yes: bool = False) -> None:
    """
    Push current branch to its remote tracking branch.
    Requires --yes to confirm (safety gate).
    Without --yes, shows a preview of commits that would be pushed.
    """
    if not yes:
        ok, ahead = run_git_command(["log", "@{u}..", "--oneline"])
        if ok and ahead.strip():
            info(f"Commits that would be pushed:\n{ahead.strip()}")
        elif ok:
            info("Nothing new to push (branch already up to date).")
            return
        error(
            "Push was NOT run.\n"
            "  Add --yes to confirm and execute the push."
        )
        return

    ok, out = run_git_command(["push"])
    if not ok:
        error(f"Push failed: {out}")
        return

    success("Changes pushed to remote.")
    if out:
        info(out)


def update() -> None:
    """Fetch all remotes without merging."""
    ok, out = run_git_command(["fetch", "--all"])
    if not ok:
        error(f"Fetch failed: {out}")
        return

    success("Remote refs updated (fetch).")
    info(out)


def sync(no_push: bool = False) -> None:
    """
    Pull remote changes then push local commits.
    Equivalent to: git pull && git push
    Use no_push=True to skip the push step.
    Aborts the push if pull fails to prevent partial sync.
    """
    info("Pulling remote changes...")
    ok, out = run_git_command(["pull"])
    if not ok:
        error(f"Pull failed — aborting sync: {out}")
        return

    if out:
        info(out)

    if no_push:
        success("Pull complete. Skipped push (--no-push).")
        return

    info("Pushing local commits...")
    ok, out = run_git_command(["push"])
    if not ok:
        error(f"Push failed: {out}")
        return

    success("Sync complete. Pulled and pushed successfully.")
    if out:
        info(out)


def fork_sync(upstream: str = "upstream", no_push: bool = False) -> None:
    """
    Sync a forked repository with its original (upstream) repo.

    Workflow:
      1. Verify the upstream remote exists.
      2. git fetch <upstream>
      3. Detect the current branch.
      4. git merge <upstream>/<branch>  — brings upstream changes in.
      5. git push origin <branch>       — keeps your fork up to date (skip if no_push=True).
    """
    # ── 1. Verify upstream remote exists ──────────────────────────────────────
    ok, remotes = run_git_command(["remote"])
    if not ok:
        error(f"Could not list remotes: {remotes}")
        return

    remote_list = remotes.splitlines()
    if upstream not in remote_list:
        error(
            f"No remote named '{upstream}' found.\n"
            f"  Add it first:  git remote add {upstream} <original-repo-url>\n"
            f"  Available remotes: {', '.join(remote_list) or 'none'}"
        )
        return

    # ── 2. Fetch from upstream ────────────────────────────────────────────────
    info(f"Fetching from '{upstream}'...")
    ok, out = run_git_command(["fetch", upstream])
    if not ok:
        error(f"Fetch from '{upstream}' failed: {out}")
        return
    if out:
        info(out)

    # ── 3. Detect current branch ──────────────────────────────────────────────
    ok, branch = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    if not ok:
        error(f"Could not determine current branch: {branch}")
        return
    info(f"Current branch: {branch}")

    # ── 4. Merge upstream/<branch> ────────────────────────────────────────────
    upstream_ref = f"{upstream}/{branch}"
    info(f"Merging {upstream_ref} into '{branch}'...")
    ok, out = run_git_command(["merge", upstream_ref])
    if not ok:
        error(
            f"Merge from {upstream_ref} failed: {out}\n"
            "  Resolve conflicts then run 'aaru send' to push."
        )
        return
    info(out)

    # ── 5. Push to origin (optional) ──────────────────────────────────────────
    if no_push:
        success(f"Fork synced! '{branch}' is now up-to-date with {upstream_ref}.")
        info("Skipped push to origin (--no-push flag).")
    else:
        info(f"Pushing '{branch}' to origin...")
        ok, out = run_git_command(["push", "origin", branch])
        if not ok:
            error(f"Push to origin failed: {out}")
            return

        success(f"Fork synced! '{branch}' is now up-to-date with {upstream_ref} and pushed to origin.")
        if out:
            info(out)


def checkout_pr(pr_number: int, remote: str = "origin", switch: bool = False) -> None:
    """
    Fetch a pull request as a local branch.
    Default: stays on your current branch after fetching.
    Use switch=True to also switch to the PR branch.

    Args:
        pr_number: The pull request number (e.g., 42)
        remote: The remote name (default: 'origin')
        switch: Switch to the PR branch after fetching (default: False)

    Workflow:
      1. Fetch the PR from remote → local branch pr-{number}
      2. (optional) Switch to PR branch if switch=True
    """
    branch_name = f"pr-{pr_number}"
    
    # Check if branch already exists
    ok, existing = run_git_command(["rev-parse", "--verify", branch_name])
    if ok:
        info(f"Branch '{branch_name}' already exists.")
        checkout = typer.confirm(f"Do you want to checkout existing branch '{branch_name}'?")
        if checkout:
            ok, out = run_git_command(["checkout", branch_name])
            if not ok:
                error(f"Failed to checkout '{branch_name}': {out}")
                return
            success(f"Checked out existing branch '{branch_name}'.")
            return
        else:
            info("Aborting PR checkout.")
            return
    
    # Fetch the PR
    info(f"Fetching PR #{pr_number} from '{remote}'...")
    pr_ref = f"pull/{pr_number}/head:{branch_name}"
    ok, out = run_git_command(["fetch", remote, pr_ref])
    if not ok:
        error(f"Failed to fetch PR #{pr_number}: {out}")
        info("Make sure the PR number is correct and you have access to the repository.")
        return

    if out:
        info(out)

    success(f"Fetched PR #{pr_number} as local branch '{branch_name}'.")

    if not switch:
        info(f"You're still on your current branch.")
        info(f"  To switch:  aaru switch {branch_name}")
        info(f"  Or re-run:  aaru checkout-pr {pr_number} --switch")
        return

    info(f"Switching to '{branch_name}'...")
    ok, out = run_git_command(["checkout", branch_name])
    if not ok:
        error(f"Failed to switch to '{branch_name}': {out}")
        return

    success(f"Checked out PR #{pr_number} as branch '{branch_name}'.")
    info("You can now test this PR locally.")
    info(f"When done, switch back with: aaru switch <your-branch>")

