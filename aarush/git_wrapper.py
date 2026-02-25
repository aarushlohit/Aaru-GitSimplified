import subprocess as sub
from typing import List,Tuple

def run_git_command(args:List[str]) -> Tuple[bool,str]:
    """
    Run git <args parameter>
    return true ,stdout if success false,stderr if failure
    """
    cmd = ["git"] + args
    try:
        completed = sub.run(cmd,
                            capture_output=True,
                            text=True,
                            check=True)
        return True,completed.stdout.strip()
    except sub.CalledProcessError as e:
        return False,(e.stderr or e.stdout).strip()
    
        


        
        