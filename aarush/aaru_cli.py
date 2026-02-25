"""
aaru_cli.py
-----------
Entry point for the AARU CLI.

Command map:
  Repository : init, clone, config
  Workflow   : status, save, history, diff, undo
  Branch     : create, switch, delete, branches
  Remote     : send, update, sync
  Stash      : stash, stash-pop, stash-list
  Passthrough: raw <any git args>
"""

import typer
from typing import Optional, Annotated

# ── command modules ────────────────────────────────────────────────────────────
from aarush.commands import init     as init_cmd
from aarush.commands import clone    as clone_cmd
from aarush.commands import status   as status_cmd
from aarush.commands import workflow as workflow_cmd
from aarush.commands import branch   as branch_cmd
from aarush.commands import remote   as remote_cmd
from aarush.commands import stash    as stash_cmd
from aarush.commands import setup    as setup_cmd
from aarush.commands import info     as info_cmd
from aarush.command_registry import dispatch
from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info

# ── app ────────────────────────────────────────────────────────────────────────
app = typer.Typer(
    help="AARU — a clean Git workflow engine",
    no_args_is_help=True,
)

# ── Setup ──────────────────────────────────────────────────────────────────────

@app.command("aaru")
def aaru():
    """
    Display AARU CLI banner with ASCII art and system information.
    Shows Git version, Python version, repo info, and author details.
    """
    info_cmd.show_banner()


@app.command("config-user")
def config_user(
    name: Annotated[Optional[str], typer.Option("--name", "-n", help="Your full name")] = None,
    email: Annotated[Optional[str], typer.Option("--email", "-e", help="Your email address")] = None
):
    """
    Configure Git user name and email (required for commits).
    
    If name or email not provided, you'll be prompted to enter them.
    This sets the global git config.
    
    Example:
      aaru config-user --name "John Doe" --email "john@example.com"
      aaru config-user    (interactive prompts)
    """
    setup_cmd.config_user(name, email)


# ── Repository ─────────────────────────────────────────────────────────────────

@app.command("init")
def init():
    """Initialize a Git repository with a .aaru workspace."""
    init_cmd.run()


@app.command("clone")
def clone(repo_url: str):
    """Clone a remote repository and set up .aaru directory."""
    clone_cmd.run(repo_url)


@app.command("config")
def config():
    """List current Git configuration."""
    dispatch("config")


# ── Workflow ───────────────────────────────────────────────────────────────────

@app.command("status")
def status():
    """Show repository working-tree status."""
    status_cmd.run()


@app.command("save")
def save(message: Annotated[str, typer.Argument(help="Commit message")]):
    """Stage all changes and commit. Equivalent to: git add -A && git commit -m."""
    workflow_cmd.save(message)


@app.command("history")
def history():
    """Show a compact, decorated commit graph."""
    dispatch("history")


@app.command("diff")
def diff():
    """Show unstaged changes in the working tree."""
    dispatch("diff")


@app.command("undo")
def undo(
    confirm: Annotated[bool, typer.Option("--confirm", help="Confirm the undo — required to actually run.")] = False,
):
    """
    Soft-undo the last commit — keeps changes in the working tree.

    Without --confirm: shows which commit would be undone.
    With --confirm: actually runs the undo.
    """
    workflow_cmd.undo(confirm=confirm)


# ── Branch ─────────────────────────────────────────────────────────────────────

@app.command("create")
def create(
    branch: Annotated[str, typer.Argument(help="New branch name")],
    switch: Annotated[bool, typer.Option("--switch", help="Also switch to the new branch after creating it.")] = False,
):
    """Create a new branch (stays on your current branch). Use --switch to also switch to it."""
    branch_cmd.create(branch, switch=switch)


@app.command("switch")
def switch(branch: Annotated[str, typer.Argument(help="Branch to switch to")]):
    """Switch to an existing branch."""
    branch_cmd.switch(branch)


@app.command("delete")
def delete(
    branch: Annotated[str, typer.Argument(help="Branch to delete")],
    confirm: Annotated[bool, typer.Option("--confirm", help="Confirm the deletion — required to actually delete.")] = False,
    force: Annotated[bool, typer.Option("--force", help="Force-delete even if branch has unmerged commits.")] = False,
):
    """
    Delete a branch (safe — refuses if unmerged).

    Add --confirm to actually delete.
    Add --force --confirm to force-delete even if unmerged.
    """
    branch_cmd.delete(branch, force=force, confirm=confirm)


@app.command("branches")
def branches():
    """List all local and remote branches."""
    branch_cmd.list_branches()


# ── Remote ─────────────────────────────────────────────────────────────────────

@app.command("add-upstream")
def add_upstream(url: Annotated[Optional[str], typer.Argument(help="URL of the original repository")] = None):
    """
    Add upstream remote for a forked repository (one-time setup).
    
    If URL is not provided, you'll be prompted to enter it.
    This is needed before using fork-sync.
    
    Example:
      aaru add-upstream https://github.com/original/repo.git
    """
    remote_cmd.add_upstream(url)


@app.command("send")
def send(
    yes: Annotated[bool, typer.Option("--yes", help="Confirm and execute the push.")] = False,
):
    """
    Push current branch to remote.

    Without --yes: previews commits to be pushed, does NOT push.
    With --yes: confirms and executes the push.
    """
    remote_cmd.send(yes=yes)


@app.command("update")
def update():
    """Fetch all remotes without merging."""
    remote_cmd.update()


@app.command("sync")
def sync(
    no_push: Annotated[bool, typer.Option("--no-push", help="Pull only — skip the push step.")] = False,
):
    """
    Pull remote changes then push local commits (pull + push).

    Add --no-push to only pull, without pushing.
    """
    remote_cmd.sync(no_push=no_push)


@app.command("fork-sync")
def fork_sync(
    upstream: Annotated[str, typer.Argument(help="Name of the upstream remote")] = "upstream",
    no_push: Annotated[bool, typer.Option("--no-push", help="Pull from upstream without pushing to origin")] = False
):
    """
    Sync your fork with the original (upstream) repository.

    Steps:
      1. Fetch from <upstream> (default: 'upstream')
      2. Merge upstream/<current-branch> into your local branch
      3. Push updated branch to origin (your fork)
         Use --no-push to skip pushing (just pull from upstream)

    Setup (one-time):
      git remote add upstream <original-repo-url>

    Example:
      aaru fork-sync                  # Pull from upstream and push to origin
      aaru fork-sync --no-push        # Pull from upstream only (no push)
    """
    remote_cmd.fork_sync(upstream, no_push=no_push)


@app.command("checkout-pr")
def checkout_pr(
    pr_number: Annotated[int, typer.Argument(help="Pull request number")],
    remote: Annotated[str, typer.Option("--remote", "-r", help="Remote name")] = "origin",
    switch: Annotated[bool, typer.Option("--switch", help="Switch to the PR branch after fetching.")] = False,
):
    """
    Fetch a pull request as a local branch for testing.

    Default: fetches PR branch, stays on your current branch.
    Add --switch to also switch to the PR branch.

    Example:
      aaru checkout-pr 42              # Fetch PR #42, stay on current branch
      aaru checkout-pr 42 --switch     # Fetch and switch to PR branch
      aaru checkout-pr 42 --remote upstream
    """
    remote_cmd.checkout_pr(pr_number, remote, switch=switch)


# ── Stash ──────────────────────────────────────────────────────────────────────

@app.command("stash")
def stash(
    message: Annotated[Optional[str], typer.Argument(help="Optional stash label")] = None
):
    """Stash current working-tree changes."""
    stash_cmd.stash(message)


@app.command("stash-pop")
def stash_pop():
    """Apply the most recent stash and remove it from the stash list."""
    stash_cmd.stash_pop()


@app.command("stash-list")
def stash_list():
    """List all stashed changesets."""
    stash_cmd.stash_list()


# ── Full Git passthrough ───────────────────────────────────────────────────────

@app.command("raw")
def raw(
    args: Annotated[list[str], typer.Argument(help="Any git command and its arguments")]
):
    """
    Pass any command directly to Git.
    Example: aaru raw -- log --oneline -10
    """
    if not args:
        error("Provide at least one git argument.")
        raise typer.Exit(1)

    ok, output = run_git_command(args)
    if not ok:
        error(output)
        raise typer.Exit(1)

    print(output)


# ── entry ──────────────────────────────────────────────────────────────────────

def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()



