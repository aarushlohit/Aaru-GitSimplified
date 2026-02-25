from aarush.git_wrapper import run_git_command
from aarush.ui  import success,error,info
import os

def run():
    '''
    init a git repository and set up folder for it'''
    
    inside,output = run_git_command(["rev-parse","--is-inside-work-tree"])

    if inside:
        error("Already inside a Git Repository...")

    info("Initializing Git Repository...")
    ok,out = run_git_command(["init"])
    if not ok:
        error("Git Init Failed")
        error(out)
    try:
       os.makedirs(".aaru",exist_ok=True)
       success("Created .aaru folder")

    except Exception as e:
        error(f"Could not create .aaru folder: {e}")
    success("Git initialized Successfully")