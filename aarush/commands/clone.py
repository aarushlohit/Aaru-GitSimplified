import os

from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info


def run(repo_url: str) -> None:
    """
    Clone a Git repository and initialise a .aaru metadata directory inside it.
    """
    if not repo_url or not repo_url.strip():
        error("Repository URL is required.")
        return

    info(f"Cloning repository from {repo_url}...")

    ok, output = run_git_command(["clone", repo_url.strip()])
    if not ok:
        error(f"Failed to clone repository: {output}")
        return  # stop — do NOT create .aaru on a failed clone

    success("Repository cloned successfully.")

    # Derive repo name from URL (strips .git suffix if present)
    repo_name = repo_url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    try:
        aaru_path = os.path.join(repo_name, ".aaru")
        os.makedirs(aaru_path, exist_ok=True)
        info(f"Initialized .aaru directory in '{repo_name}'")
    except Exception as e:
        error(f"Failed to create .aaru directory: {e}")
        