# 🪟 AARU CLI - Windows Installation

Quick guide for Windows users.

---

## 🚀 Quick Install (Recommended)

### With Python Installed

1. **Clone the repository:**
   ```batch
   git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
   cd GIT_PROTOCOL
   ```

2. **Run installer:**
   ```batch
   install_windows.bat
   ```

3. **Restart Command Prompt or PowerShell**

4. **Test:**
   ```batch
   aaru --help
   ```

---

## 🔥 Standalone EXE (No Python Required)

Perfect if you don't have Python or want a portable version.

### Method 1: Build from Source

**Requirements:** Python (only for building)

```batch
git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
cd GIT_PROTOCOL
build_exe.bat
```

The executable will be at: `dist\aaru.exe`

### Method 2: Download Pre-built (Coming Soon)

Download `aaru.exe` from [Releases](https://github.com/aarushlohit/GIT_PROTOCOL/releases)

---

## 📌 Adding to PATH

### Option 1: Add dist folder to PATH

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Click "Advanced" → "Environment Variables"
3. Under "User variables", find and select "Path"
4. Click "Edit" → "New"
5. Add: `C:\path\to\GIT_PROTOCOL\dist`
   - Replace with your actual path
   - Example: `C:\Users\YourName\Downloads\GIT_PROTOCOL\dist`
6. Click OK on all windows
7. **Restart Command Prompt**

### Option 2: Copy to System folder (Requires Admin)

```batch
REM Run Command Prompt as Administrator
copy dist\aaru.exe C:\Windows\System32\
```

### Option 3: Portable Usage

Just double-click `dist\aaru.exe` or run:
```batch
cd dist
aaru.exe --help
```

---

## ✅ Verify Installation

```batch
aaru --help
aaru aaru
```

You should see the help menu or ASCII art banner.

---

## 🐛 Troubleshooting

### "aaru is not recognized as internal or external command"

**Solution 1:** Restart Command Prompt or PowerShell

**Solution 2:** Check if Python Scripts folder is in PATH
- Open Command Prompt
- Run: `echo %PATH%`
- Look for: `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\Scripts`

**Solution 3:** Use full path
```batch
C:\path\to\dist\aaru.exe --help
```

**Solution 4:** Reinstall with admin rights
```batch
REM Right-click Command Prompt → Run as Administrator
pip install aarushlohit_git
```

### "Python is not installed"

Either:
1. Install Python from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
2. Use the standalone EXE (no Python needed)

### Permission Errors

Run Command Prompt as Administrator:
- Press `Win + X`
- Select "Command Prompt (Admin)" or "PowerShell (Admin)"

---

## 📖 Quick Start

```batch
REM Initialize a new repository
mkdir my-project
cd my-project
aaru init

REM Make some changes
echo "# My Project" > README.md
aaru save "Initial commit"

REM Work with branches
aaru create feature-branch
aaru switch main
aaru branches

REM Sync with remote
aaru send
aaru sync

REM Get help
aaru --help
```

---

## 🎯 Which Installation Method to Choose?

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **pipinstall** | Python developers | Easy updates | Requires Python |
| **Standalone EXE** | Everyone | No Python needed | Larger file size |
| **System install** | Power users | Available for all users | Needs admin |

**Recommendation:** If you have Python → use `install_windows.bat`  
**Recommendation:** If you don't have Python → build standalone EXE

---

## 🔄 Updating

### pip installation:
```batch
pip install --upgrade aarushlohit_git
```

### Standalone EXE:
Download new version or rebuild:
```batch
git pull
build_exe.bat
```

---

## 🗑️ Uninstall

### pip installation:
```batch
pip uninstall aarushlohit_git
```

### Standalone EXE:
Just delete `aaru.exe` and remove from PATH if added.

---

## 💡 Tips

1. **Add to Start Menu:** Create shortcut to `dist\aaru.exe` in:
   `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`

2. **Desktop Shortcut:** Right-click `dist\aaru.exe` → Send to → Desktop

3. **Git Bash:** Works in Git Bash, Command Prompt, and PowerShell

4. **VSCode Terminal:** Works in VSCode integrated terminal

---

## 📞 Need Help?

- 📖 Full guide: [INSTALL.md](INSTALL.md)
- 🐛 Issues: [GitHub Issues](https://github.com/aarushlohit/GIT_PROTOCOL/issues)
- 📧 Contact: aarushlohit@users.noreply.github.com

---

**Made with ❤️ by aarushlohit**
