"""
commands/setup.py
-----------------
Setup and configuration commands.
  config_user  → configure git user.name and user.email
"""

from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info
import typer


def config_user(name: str = None, email: str = None) -> None:
    """
    Configure Git user name and email globally.
    
    If name or email not provided, prompts the user to enter them.
    This is essential for making commits.
    """
    # Get current config if exists
    ok, current_name = run_git_command(["config", "--global", "user.name"])
    ok2, current_email = run_git_command(["config", "--global", "user.email"])
    
    if ok and current_name.strip():
        info(f"Current user.name: {current_name.strip()}")
    if ok2 and current_email.strip():
        info(f"Current user.email: {current_email.strip()}")
    
    # Get name if not provided
    if not name:
        if ok and current_name.strip():
            name = typer.prompt("Enter your name", default=current_name.strip())
        else:
            name = typer.prompt("Enter your name")
    
    # Get email if not provided
    if not email:
        if ok2 and current_email.strip():
            email = typer.prompt("Enter your email", default=current_email.strip())
        else:
            email = typer.prompt("Enter your email")
    
    # Set user.name
    ok, out = run_git_command(["config", "--global", "user.name", name])
    if not ok:
        error(f"Failed to set user.name: {out}")
        return
    
    # Set user.email
    ok, out = run_git_command(["config", "--global", "user.email", email])
    if not ok:
        error(f"Failed to set user.email: {out}")
        return
    
    success("Git user configured successfully!")
    info(f"  user.name  = {name}")
    info(f"  user.email = {email}")
