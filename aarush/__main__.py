"""
Allows running AARU CLI as a Python module:
    python -m aarush

This is the fallback for when 'aaru' is not yet in PATH
(e.g. right after pip install before restarting terminal).
"""
from aarush.aaru_cli import main

main()
