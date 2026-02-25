"""
config.py
---------
Shared settings used by logger, policy, and executor.

Change things here once and every module picks it up automatically.
"""

from __future__ import annotations

from pathlib import Path


# Where every command run by Aaru gets recorded (relative to the repo root).
# The file is in JSONL format — one JSON object per line.
LOG_RELATIVE_PATH = Path(".vibe") / "logs" / "session.jsonl"

# Branches that must never be deleted through Aaru.
# Add your own project branches here if needed.
PROTECTED_BRANCHES = {"main", "master", "develop", "production"}

