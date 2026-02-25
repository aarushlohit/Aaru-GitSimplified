"""
command_registry.py
-------------------
Registry for simple Git passthrough commands.
Maps aaru command names to their Git equivalents.
No logic, no duplication — just a dispatch table.
"""

from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info

# Map: aaru-command-name -> git args prefix
# Extra args passed at call-time are appended.
REGISTRY: dict[str, list[str]] = {
    "history": ["log", "--oneline", "--graph", "--decorate"],
    "diff":    ["diff"],
    "config":  ["config", "--list"],
}


def dispatch(command: str, extra: list[str] | None = None) -> None:
    """
    Look up a command in the registry and execute it.
    :param command: aaru command name (key in REGISTRY)
    :param extra:   additional git args appended to the base args
    """
    if command not in REGISTRY:
        error(f"Unknown command: '{command}'")
        return

    args = REGISTRY[command] + (extra or [])
    ok, output = run_git_command(args)

    if not ok:
        error(f"[{command}] failed: {output}")
        return

    info(f"[{command}]")
    print(output)
