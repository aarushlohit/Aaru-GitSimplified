"""
commands/info.py
----------------
Information and display commands.
  show_banner  → display AARU ASCII art banner with system info and author image
"""

from aarush.git_wrapper import run_git_command
from aarush.ui import info
import subprocess
import sys
import os


def show_banner() -> None:
    """
    Display a cool ASCII art banner with AARU CLI information and author image.
    Uses custom fastfetch configuration to display GitHub avatar.
    """
    
    # AARU ASCII Art with Author Info Banner
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║        █████╗  █████╗ ██████╗ ██╗   ██╗    ██████╗██╗     ██╗             ║
    ║       ██╔══██╗██╔══██╗██╔══██╗██║   ██║   ██╔════╝██║     ██║             ║
    ║       ███████║███████║██████╔╝██║   ██║   ██║     ██║     ██║             ║
    ║       ██╔══██║██╔══██║██╔══██╗██║   ██║   ██║     ██║     ██║             ║
    ║       ██║  ██║██║  ██║██║  ██║╚██████╔╝   ╚██████╗███████╗██║             ║
    ║       ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝╚══════╝╚═╝             ║
    ║                                                                           ║
    ║              🚀 A Clean & Powerful Git Workflow Engine 🚀                 ║
    ║                                                                           ║
    ║   ┌───────────────────────────────────────────────────────────────────┐   ║
    ║   │  👤 Created by: aarushlohit                                       │   ║
    ║   │  🐙 GitHub: github.com/aarushlohit                                │   ║
    ║   │  🌐 Creator of Zairok Presents                                    │   ║
    ║   │  📸 Instagram: @aarushlohit_01                                    │   ║
    ║   │  🖼️  Avatar: avatars.githubusercontent.com/u/141929019            │   ║
    ║   └───────────────────────────────────────────────────────────────────┘   ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    
    print("\033[1;36m" + banner + "\033[0m")  # Cyan color
    
    # Get Git version
    ok, git_version = run_git_command(["--version"])
    if ok:
        print(f"\033[1;32m  ✓ Git:\033[0m {git_version.strip()}")
    
    # Get Python version
    python_version = f"Python {sys.version.split()[0]}"
    print(f"\033[1;32m  ✓ Python:\033[0m {python_version}")
    
    # Try to show repository info if in a git repo
    ok, branch = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    if ok:
        print(f"\n\033[1;33m  📍 Current Branch:\033[0m {branch.strip()}")
        
        # Get repo root
        ok, repo_root = run_git_command(["rev-parse", "--show-toplevel"])
        if ok:
            print(f"\033[1;33m  📂 Repository:\033[0m {repo_root.strip()}")
        
        # Get remote if exists
        ok, remote = run_git_command(["remote", "get-url", "origin"])
        if ok:
            print(f"\033[1;33m  🌐 Origin:\033[0m {remote.strip()}")
    
    print("\n\033[1;35m  💡 Quick Start:\033[0m")
    print("     aaru init              - Initialize a new repository")
    print("     aaru save <message>    - Save changes with a commit")
    print("     aaru sync              - Pull and push changes")
    print("     aaru fork-sync         - Sync with upstream fork")
    print("     aaru --help            - Show all commands")
    
    # Try to run custom fastfetch in image-capable terminals  
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(script_dir), '.aaru_fastfetch.jsonc')
        
        if os.path.exists(config_path) and os.environ.get('TERM_PROGRAM') in ['WezTerm', 'iTerm.app', 'kitty']:
            print("\n\033[1;34m  ═══ System Info with Author Image ═══\033[0m\n")
            subprocess.run(
                ["fastfetch", "--config", config_path],
                capture_output=False,
                timeout=5
            )
    except:
        pass
    
    print("\n")
