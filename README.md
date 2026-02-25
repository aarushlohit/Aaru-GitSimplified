# AARU CLI

**A Clean & Powerful Git Workflow Engine**

[![PyPI Version](https://img.shields.io/pypi/v/aarushlohit-git.svg)](https://pypi.org/project/aarushlohit-git/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/aarushlohit-git.svg)](https://pypi.org/project/aarushlohit-git/)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)](https://github.com/aarushlohit/GIT_PROTOCOL)

> Created by **aarushlohit** · [github.com/aarushlohit](https://github.com/aarushlohit) · [Zairok App](https://zairok.web.app)

AARU wraps Git with a clean, opinionated command surface. Every destructive or side-effect action requires an explicit confirmation flag — you always see what will happen before it happens.

## 🎉 What's New in v2.0

- **One-command install:** `pip install aarushlohit-git` — works on all platforms
- **Zero PATH hassles:** `python3 -m aarush` works immediately after install (no terminal restart)
- **Easy installers:** One-line bash/PowerShell scripts with auto PATH setup for Linux/macOS/Windows
- **Rich terminal UI:** Colored output with ✔/✖/ℹ icons for better readability
- **Complete command suite:** 23 commands covering all Git workflows — init, save, sync, fork-sync, checkout-pr, and more
- **Safety-first design:** Destructive commands require explicit `--confirm` or `--yes` flags
- **Professional banner:** `aaru aaru` shows system info, repo status, and quick start guide

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
  - [Info & Setup](#info--setup)
  - [Repository](#repository)
  - [Workflow](#workflow)
  - [Branch](#branch)
  - [Remote](#remote)
  - [Stash](#stash)
  - [Raw Passthrough](#raw-passthrough)
- [Safety Model](#safety-model)
- [Real-World Workflows](#real-world-workflows)

---

## Installation

### Option 1 — pip (recommended, all platforms)

```bash
pip install aarushlohit-git
```

After install, if `aaru` isn't recognised yet (PATH not updated), use this fallback **immediately**:

```bash
python3 -m aarush --help   # Linux / macOS
python  -m aarush --help   # Windows
```

Open a **new terminal** and `aaru` will work everywhere.

---

### Option 2 — Easy installer scripts

#### Linux / macOS — one-liner

```bash
# From the repo:
bash install.sh

# Or directly from GitHub (no clone needed):
curl -fsSL https://raw.githubusercontent.com/aarushlohit/GIT_PROTOCOL/main/install.sh | bash
```

- Auto-detects `pipx` → falls back to `pip --user`
- Handles externally-managed Python (Arch, Debian 12+, Ubuntu 23+)
- Automatically adds `~/.local/bin` to your shell config

#### Windows — double-click installer

```
install_windows.bat
```

- Double-click it in Explorer or run it in Command Prompt
- Auto-detects Python, downloads Python installer if missing
- Permanently adds the Scripts folder to your user PATH (no admin required)

#### Windows — PowerShell one-liner

```powershell
# Run in PowerShell:
iwr https://raw.githubusercontent.com/aarushlohit/GIT_PROTOCOL/main/install.ps1 | iex
```

---

### Option 3 — Standalone binary (no Python required)

```bash
# Linux / macOS:
./build_exe.sh
sudo cp dist/aaru /usr/local/bin/

# Windows:
build_exe.bat
# Then copy dist\aaru.exe to a folder in your PATH
```

---

### Upgrading

```bash
pip install --upgrade aarushlohit-git
```

---

## Quick Start

```bash
# 1. Initialize a new repo
aaru init

# 2. Set your Git identity (one-time)
aaru config-user --name "Your Name" --email "you@example.com"

# 3. Do some work, then save it
aaru save "add login page"

# 4. Push to remote
aaru send --yes

# 5. Pull + push in one step
aaru sync
```

---

## Command Reference

### Info & Setup

---

#### `aaru aaru`
Display the ASCII art banner with system info (Git version, Python version, repo, remote URL).

```bash
aaru aaru
```

---

#### `aaru config-user`
Configure your Git user name and email globally. Interactive prompts if flags are omitted.

```bash
aaru config-user --name "Jane Doe" --email "jane@example.com"
aaru config-user        # prompts for both
```

| Flag | Description |
|------|-------------|
| `--name`, `-n` | Your full name |
| `--email`, `-e` | Your email address |

---

### Repository

---

#### `aaru init`
Initialize a new Git repository in the current directory and create a `.aaru` workspace folder.

```bash
aaru init
```

---

#### `aaru clone <repo-url>`
Clone a remote repository and set up the `.aaru` directory automatically.

```bash
aaru clone https://github.com/user/repo.git
```

---

#### `aaru config`
Print the current Git configuration (equivalent to `git config --list`).

```bash
aaru config
```

---

### Workflow

---

#### `aaru status`
Show the working-tree status — modified files, staged files, untracked files.

```bash
aaru status
```

---

#### `aaru save <message>`
Stage **all** changed files and commit in one step.  
Equivalent to: `git add -A && git commit -m "<message>"`

```bash
aaru save "fix navbar alignment"
aaru save "initial commit"
```

---

#### `aaru history`
Show a compact, decorated commit graph with branch pointers.

```bash
aaru history
```

---

#### `aaru diff`
Show unstaged changes in the working tree.

```bash
aaru diff
```

---

#### `aaru undo`
Soft-undo the last commit. Keeps all your changes in the working tree (nothing is lost).  
Equivalent to: `git reset HEAD~1`

**Without `--confirm`:** shows which commit would be undone — does NOT undo yet.  
**With `--confirm`:** actually runs the undo.

```bash
aaru undo              # preview: "Would undo: abc1234 fix navbar"
aaru undo --confirm    # actually undoes the commit
```

| Flag | Description |
|------|-------------|
| `--confirm` | Required to actually execute the undo |

---

### Branch

---

#### `aaru create <branch>`
Create a new branch. By default you **stay on your current branch** — the new branch is created but not switched to.

```bash
aaru create feature/login          # creates branch, stays where you are
aaru create feature/login --switch # creates AND switches to it
```

| Flag | Description |
|------|-------------|
| `--switch` | Switch to the new branch after creating it |

---

#### `aaru switch <branch>`
Switch to an existing branch.

```bash
aaru switch main
aaru switch feature/login
```

---

#### `aaru delete <branch>`
Delete a branch. Safe by default — refuses if the branch has unmerged commits.  
Requires `--confirm` to actually execute.

```bash
aaru delete old-branch                      # blocked: shows error with instructions
aaru delete old-branch --confirm            # safe delete (refuses if unmerged)
aaru delete old-branch --force --confirm    # force-delete even if unmerged
```

| Flag | Description |
|------|-------------|
| `--confirm` | Required to actually delete |
| `--force` | Force-delete even if branch has unmerged commits |

---

#### `aaru branches`
List all local and remote branches.

```bash
aaru branches
```

---

### Remote

---

#### `aaru send`
Push the current branch to its remote tracking branch.

**Without `--yes`:** shows a preview of commits that would be pushed — does NOT push.  
**With `--yes`:** actually pushes.

```bash
aaru send          # preview: shows commits to be pushed
aaru send --yes    # push confirmed
```

| Flag | Description |
|------|-------------|
| `--yes` | Confirm and execute the push |

---

#### `aaru update`
Fetch all remotes without merging. Equivalent to `git fetch --all`.

```bash
aaru update
```

---

#### `aaru sync`
Pull remote changes then push local commits in one step.  
Equivalent to: `git pull && git push`

Use `--no-push` to only pull without pushing.

```bash
aaru sync              # pull + push
aaru sync --no-push    # pull only
```

| Flag | Description |
|------|-------------|
| `--no-push` | Pull only — skip the push step |

---

#### `aaru add-upstream <url>`
Add the `upstream` remote for a forked repository (one-time setup before using `fork-sync`).  
Prompts for URL if not provided.

```bash
aaru add-upstream https://github.com/original/repo.git
aaru add-upstream    # prompts for URL
```

---

#### `aaru fork-sync`
Sync your fork with the original upstream repository.

**Steps performed:**
1. Fetch from `upstream` remote
2. Merge `upstream/<current-branch>` into your local branch
3. Push the updated branch to `origin` (your fork)

```bash
# One-time setup:
aaru add-upstream https://github.com/original/repo.git

# Then sync any time:
aaru fork-sync              # fetch + merge + push
aaru fork-sync --no-push    # fetch + merge only (don't push)
aaru fork-sync myupstream   # use a different upstream remote name
```

| Argument / Flag | Description |
|------|-------------|
| `[upstream]` | Name of the upstream remote (default: `upstream`) |
| `--no-push` | Pull from upstream only — skip pushing to origin |

---

#### `aaru checkout-pr <number>`
Fetch a pull request as a local branch for testing.

**Without `--switch`:** fetches the PR branch, you **stay on your current branch**.  
**With `--switch`:** fetches and switches to the PR branch.

```bash
aaru checkout-pr 42                       # fetch PR #42, stay on current branch
aaru checkout-pr 42 --switch              # fetch and switch to pr-42
aaru checkout-pr 42 --remote upstream     # fetch from a different remote
```

| Flag | Description |
|------|-------------|
| `--switch` | Switch to the PR branch after fetching |
| `--remote`, `-r` | Remote to fetch from (default: `origin`) |

---

### Stash

---

#### `aaru stash [label]`
Stash all current working-tree changes. Optionally tag the stash with a label.

```bash
aaru stash                          # stash with no label
aaru stash "wip: auth refactor"     # stash with a descriptive label
```

---

#### `aaru stash-pop`
Apply the most recent stash and remove it from the stash list.

```bash
aaru stash-pop
```

---

#### `aaru stash-list`
List all saved stashes.

```bash
aaru stash-list
```

---

### Raw Passthrough

#### `aaru raw -- <git args>`
Pass any git command directly through the AARU pipeline. Use `--` to separate AARU flags from git flags.

```bash
aaru raw -- log --oneline -10
aaru raw -- rebase -i HEAD~3
aaru raw -- remote -v
aaru raw -- cherry-pick abc1234
```

> **Note:** The `--` separator is required whenever your git command includes flags (anything starting with `-`).

---

## Safety Model

AARU follows one rule: **commands with side effects are safe by default and require an explicit opt-in flag.**

| Command | Without the flag | Opt-in flag |
|---------|------------------|-------------|
| `send` | Shows preview of commits to push | `--yes` to push |
| `undo` | Shows which commit would be undone | `--confirm` to run |
| `delete` | Shows error with instructions | `--confirm` to delete |
| `delete` (unmerged) | Shows error with instructions | `--force --confirm` |
| `create` | Creates branch, stays on current | `--switch` to also switch |
| `checkout-pr` | Fetches PR, stays on current branch | `--switch` to also switch |
| `sync` | Pull + push | `--no-push` to skip push |
| `fork-sync` | Fetch + merge + push | `--no-push` to skip push |

---

## Real-World Workflows

### Starting a new feature

```bash
aaru status                          # check current state
aaru create feature/user-auth        # create branch, stay on current
aaru switch feature/user-auth        # switch to it when ready
# ... write code ...
aaru save "add JWT middleware"
aaru send --yes                      # push to remote
```

### Undoing a bad commit

```bash
aaru undo                  # preview: "Would undo: abc1234 oops wrong file"
aaru undo --confirm        # actually undo it
# fix your files
aaru save "correct commit message"
```

### Syncing a fork with upstream

```bash
# One-time setup
aaru add-upstream https://github.com/original/project.git

# Every time you want to sync
aaru fork-sync              # fetch upstream + merge + push to your fork
aaru fork-sync --no-push    # only pull from upstream, review before pushing
```

### Testing a pull request locally

```bash
aaru checkout-pr 84                  # fetch pr-84, stay on current branch
# review the diff with: aaru diff
aaru checkout-pr 84 --switch         # now switch to it and test
aaru switch main                     # done testing, switch back
```

### Saving work-in-progress before switching context

```bash
aaru stash "wip: payment flow"       # stash current work with a label
aaru switch hotfix/login-crash       # switch context
# ... fix the bug ...
aaru save "fix login crash on mobile"
aaru send --yes
aaru switch feature/payment          # come back
aaru stash-pop                       # restore your work
```

### Cleaning up old branches

```bash
aaru branches                                    # see all branches
aaru delete old-experiment                       # blocked — shows what to add
aaru delete old-experiment --confirm             # safe delete
aaru delete wip-never-merged --force --confirm   # force delete unmerged branch
```

---

## Getting Help

Every command has built-in help:

```bash
aaru --help
aaru <command> --help

# Examples:
aaru send --help
aaru delete --help
aaru fork-sync --help
aaru checkout-pr --help
```
