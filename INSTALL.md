# 📦 AARU CLI - Installation Guide

Complete installation instructions for all platforms.

---

## 🐧 Linux Installation

### Method 1: User Installation (Recommended) ⭐

No sudo required, installs to `~/.local/bin`

```bash
git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
cd GIT_PROTOCOL
./install.sh
```

Select option **1** when prompted.

If `aaru` command is not found after installation:
```bash
source ~/.bashrc  # or ~/.zshrc for zsh users
```

**Manual PATH setup (if needed):**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### Method 2: System-Wide Installation

Requires sudo, available for all users

```bash
git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
cd GIT_PROTOCOL
./install.sh
```

Select option **2** when prompted.

---

### Method 3: Standalone Binary 🚀

No Python required after build! Perfect for:
- Systems without Python
- Air-gapped environments
- Production servers

```bash
git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
cd GIT_PROTOCOL

# Build the binary
./build_exe.sh

# Install system-wide
sudo cp dist/aaru /usr/local/bin/
sudo chmod +x /usr/local/bin/aaru

# Verify installation
aaru --help
```

**Binary location:** `dist/aaru`

---

## 🪟 Windows Installation

### Method 1: Python Installation (Recommended for Python users)

#### Prerequisites:
- Python 3.8 or higher
- Make sure "Add Python to PATH" was checked during Python installation

#### Installation:

```batch
git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
cd GIT_PROTOCOL
install_windows.bat
```

Select option **1** for user installation (no admin required).

**Verify installation:**
```batch
aaru --help
```

**If command not found:** Restart Command Prompt or PowerShell.

---

### Method 2: Standalone EXE 🔥 (Recommended for all users)

No Python installation required! Perfect for:
- Non-Python users
- Quick deployment
- Portable usage

#### Option A: Download Pre-built EXE (Coming Soon)

Download `aaru.exe` from [Releases](https://github.com/aarushlohit/GIT_PROTOCOL/releases)

#### Option B: Build from Source

**Prerequisites:**
- Python 3.8+ (only for building)
- Git for Windows

**Build steps:**
```batch
git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
cd GIT_PROTOCOL
build_exe.bat
```

The executable will be created at: `dist\aaru.exe`

**Installation options:**

1. **Add to PATH (Recommended):**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Go to "Advanced" → "Environment Variables"
   - Under "User variables", select "Path" → "Edit"
   - Click "New" and add the full path to `dist` folder
   - Example: `C:\Users\YourName\GIT_PROTOCOL\dist`
   - Click OK and restart Command Prompt

2. **Copy to System folder (Requires Admin):**
   ```batch
   copy dist\aaru.exe C:\Windows\System32\
   ```

3. **Portable usage:**
   - Just run `dist\aaru.exe` directly
   - Create a desktop shortcut

**Verify:**
```batch
aaru --help
```

---

## 🍎 macOS Installation

### Method 1: User Installation

```bash
git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
cd GIT_PROTOCOL
./install.sh
```

Select option **1** when prompted.

Add to PATH if needed:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

### Method 2: Homebrew (Coming Soon)

```bash
brew install aarushlohit/tap/aaru
```

---

## 📦 PyPI Installation

Available on PyPI as `aarushlohit_git`:

```bash
# Linux/macOS
pip install --user aarushlohit_git

# Windows
pip install aarushlohit_git
```

**Upgrade:**
```bash
pip install --upgrade aarushlohit_git
```

---

## 🔧 Development Installation

For contributors and developers:

```bash
git clone https://github.com/aarushlohit/GIT_PROTOCOL.git
cd GIT_PROTOCOL

# Linux/macOS
python3 -m pip install --user -e .

# Windows  
python -m pip install --user -e .
```

This creates an editable installation that reflects code changes immediately.

---

## ✅ Verify Installation

After installation, verify it works:

```bash
# Check version and help
aaru --help
aaru aaru

# Quick test
mkdir test-repo
cd test-repo
aaru init
aaru status
```

---

## 🐛 Troubleshooting

### Linux/macOS: "aaru: command not found"

**Solution 1:** Restart your terminal

**Solution 2:** Add to PATH manually
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Solution 3:** Use full path
```bash
~/.local/bin/aaru --help
```

---

### Windows: "aaru is not recognized"

**Solution 1:** Restart Command Prompt or PowerShell

**Solution 2:** Check Python Scripts in PATH
- Python scripts folder should be in PATH
- Usually: `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\Scripts\`

**Solution 3:** Reinstall with admin rights
```batch
# Run Command Prompt as Administrator
pip install aarushlohit_git
```

**Solution 4:** Use the EXE version (see above)

---

### Permission Denied (Linux/macOS)

If you get permission errors:

```bash
# Don't use sudo pip!
# Instead use --user flag
python3 -m pip install --user aarushlohit_git
```

---

### Python Version Issues

AARU requires Python 3.8+

Check your version:
```bash
python3 --version  # Linux/macOS
python --version   # Windows
```

If you have an older version, upgrade Python first.

---

## 🔄 Uninstallation

### pip installation:
```bash
pip uninstall aarushlohit_git
```

### Binary installation (Linux):
```bash
sudo rm /usr/local/bin/aaru
```

### Binary installation (Windows):
```batch
del C:\Windows\System32\aaru.exe
```

Or remove from PATH and delete the `dist` folder.

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Open an issue: [GitHub Issues](https://github.com/aarushlohit/GIT_PROTOCOL/issues)
3. Include:
   - Your OS and version
   - Python version (`python --version`)
   - Installation method used
   - Error messages

---

**Made with ❤️ by aarushlohit**
