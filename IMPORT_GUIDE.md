# AARU CLI - Import Examples

## Installation
```bash
pip install aarushlohit_git
```

## Usage

### Command Line
```bash
# Use the aaru command
aaru --help
aaru init
aaru save "my commit"
aaru sync
```

### Python Import
```python
# Import the aarush package
import aarush

# Check version
print(aarush.__version__)  # 1.1.0

# Import specific modules
from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info

# Use the functions
ok, output = run_git_command(["status"])
if ok:
    success("Git command successful!")
```

### Import Examples
```python
# Import the main CLI
from aarush.aaru_cli import app

# Import command modules
from aarush.commands import init, clone, status
from aarush.commands import workflow, branch, remote

# Import utilities
from aarush.git_wrapper import run_git_command
from aarush.ui import success, error, info
from aarush.config import AARU_DIR
```

## Package Structure
- **Package name**: `aarushlohit_git`
- **Import name**: `aarush`
- **Command**: `aaru`
- **Version**: 1.1.0

## Links
- PyPI: https://pypi.org/project/aarushlohit-git/
- GitHub: https://github.com/aarushlohit/GIT_PROTOCOL
- Author: aarushlohit
