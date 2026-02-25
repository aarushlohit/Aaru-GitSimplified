from aarush.git_wrapper import run_git_command

from aarush.ui import success,error,info

def run():
    """
    Show the current repository status in a clean way
    """
    ok,output = run_git_command(["status"])
    if not ok:
        error("Not a git Repository")
        error(output)
    else:
     info("Repository Status:")
     print(output)
