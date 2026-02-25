"""
cli.py
------
Phase 2 Typer CLI — every command goes through executor.execute().

This is the Phase 2 integration layer that replaces direct git_wrapper calls.
All commands follow the same pattern:
  1. Call executor.execute() with the Aaru command name + git args
  2. Call _print_result() to show output and exit cleanly on errors

AI-aware flags available on every command:
  --ai-model   Name of the AI model that triggered this run (e.g. 'gpt-4o')
  --ai-prompt  The prompt text that led to this git operation
  These are optional and get saved in the session log for traceability.
"""

from __future__ import annotations

from typing import Optional
import typer

from .executor import execute


app = typer.Typer(help="Aaru CLI")


def _print_result(result: dict) -> None:
    """Print stdout/stderr from the git command and exit with code 1 on failure.

    Called after every execute() call. Keeps all command handlers tiny.
    """
    if result["stdout"]:
        print(result["stdout"])
    if result["stderr"]:
        print(result["stderr"])
    if not result["ok"]:
        raise typer.Exit(code=1)


@app.command("save")
def save(
    message: str = typer.Argument(..., help="Commit message."),
    ai_model: Optional[str] = typer.Option(None, "--ai-model", help="AI model name (optional, for audit trail)."),
    ai_prompt: Optional[str] = typer.Option(None, "--ai-prompt", help="The prompt that triggered this commit (optional)."),
) -> None:
    """Stage every changed file and commit — equivalent to: git add -A && git commit -m '...'"""

    # First stage everything in the working tree
    add_result = execute(
        aaru_command="save",
        git_command=["add", "-A"],
        ai_model=ai_model,
        ai_prompt=ai_prompt,
    )
    _print_result(add_result)  # stops here if staging failed

    # Then commit with the provided message
    commit_result = execute(
        aaru_command="save",
        git_command=["commit", "-m", message],
        ai_model=ai_model,
        ai_prompt=ai_prompt,
    )
    _print_result(commit_result)


@app.command("create")
def create(
    branch: str = typer.Argument(..., help="Name of the new branch."),
    switch: bool = typer.Option(False, "--switch", help="Also switch to the new branch after creating it."),
    ai_model: Optional[str] = typer.Option(None, "--ai-model"),
    ai_prompt: Optional[str] = typer.Option(None, "--ai-prompt"),
) -> None:
    """Create a new branch (stays on your current branch).

    Use --switch to also switch to it after creating.
    """
    git_cmd = ["checkout", "-b", branch] if switch else ["branch", branch]
    result = execute(
        aaru_command="create",
        git_command=git_cmd,
        ai_model=ai_model,
        ai_prompt=ai_prompt,
    )
    if result.get("ok"):
        if switch:
            typer.echo(f"✔ Created and switched to branch '{branch}'.")
        else:
            typer.echo(f"✔ Created branch '{branch}'. You're still on your current branch.")
    else:
        _print_result(result)


@app.command("send")
def send(
    yes: bool = typer.Option(False, "--yes", help="Required to confirm if policy marks this as high-risk."),
    ai_model: Optional[str] = typer.Option(None, "--ai-model"),
    ai_prompt: Optional[str] = typer.Option(None, "--ai-prompt"),
) -> None:
    """Push the current branch to the remote (git push)."""
    result = execute(
        aaru_command="send",
        git_command=["push"],
        ai_model=ai_model,
        ai_prompt=ai_prompt,
        yes=yes,
    )
    _print_result(result)


@app.command("sync")
def sync(
    yes: bool = typer.Option(False, "--yes", help="Required to confirm if policy marks this as high-risk."),
    ai_model: Optional[str] = typer.Option(None, "--ai-model"),
    ai_prompt: Optional[str] = typer.Option(None, "--ai-prompt"),
) -> None:
    """Pull remote changes (rebase) then push local commits."""

    # Step 1: Pull from remote and rebase local commits on top
    pull_result = execute(
        aaru_command="sync",
        git_command=["pull", "--rebase"],
        ai_model=ai_model,
        ai_prompt=ai_prompt,
        yes=yes,
    )
    _print_result(pull_result)  # stops here if pull/rebase failed

    # Step 2: Push the rebased commits to remote
    push_result = execute(
        aaru_command="sync",
        git_command=["push"],
        ai_model=ai_model,
        ai_prompt=ai_prompt,
        yes=yes,
    )
    _print_result(push_result)


@app.command("pr")
def pr(
    ai_model: Optional[str] = typer.Option(None, "--ai-model"),
    ai_prompt: Optional[str] = typer.Option(None, "--ai-prompt"),
) -> None:
    """Print the origin remote URL so you can open a pull request in your browser."""
    result = execute(
        aaru_command="pr",
        git_command=["remote", "get-url", "origin"],
        ai_model=ai_model,
        ai_prompt=ai_prompt,
    )
    _print_result(result)


@app.command("raw")
def raw(
    git_args: list[str] = typer.Argument(..., help="Any git sub-command and flags, e.g. log --oneline -10"),
    yes: bool = typer.Option(False, "--yes", help="Required to confirm if policy marks this as high-risk."),
    ai_model: Optional[str] = typer.Option(None, "--ai-model"),
    ai_prompt: Optional[str] = typer.Option(None, "--ai-prompt"),
) -> None:
    """Pass any git command through the Aaru safety pipeline.

    Example: aaru raw -- log --oneline -10
    The command still goes through policy checks and gets logged.
    """
    result = execute(
        aaru_command="raw",
        git_command=git_args,
        ai_model=ai_model,
        ai_prompt=ai_prompt,
        yes=yes,
    )
    _print_result(result)


def main() -> None:
    """Typer entry point — called by the 'aaru' console script."""
    app()


if __name__ == "__main__":
    main()
