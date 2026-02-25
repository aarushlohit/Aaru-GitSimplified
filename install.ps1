# ============================================================
#  AARU CLI — Easy Installer for Windows (PowerShell)
#  Usage (run in PowerShell as normal user):
#    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#    .\install.ps1
#  One-liner:
#    iwr https://raw.githubusercontent.com/aarushlohit/GIT_PROTOCOL/main/install.ps1 | iex
# ============================================================

$ErrorActionPreference = "Stop"
$PACKAGE = "aarushlohit-git"

function Write-OK   { param($msg) Write-Host "  [OK] $msg" -ForegroundColor Green  }
function Write-Warn { param($msg) Write-Host "  [!]  $msg" -ForegroundColor Yellow }
function Write-Fail { param($msg) Write-Host "  [X]  $msg" -ForegroundColor Red; exit 1 }
function Write-Info { param($msg) Write-Host "  -->  $msg" }

Write-Host ""
Write-Host "  =====================================" -ForegroundColor Cyan
Write-Host "     AARU CLI - Easy Windows Installer " -ForegroundColor Cyan
Write-Host "  =====================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check Python ─────────────────────────────────────────
Write-Info "Checking for Python..."
$pyCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3") {
            $pyCmd = $cmd
            Write-OK "Found $ver"
            break
        }
    }
}

if (-not $pyCmd) {
    Write-Warn "Python 3 not found."
    Write-Host ""
    $choice = Read-Host "  Download Python now? [Y/n]"
    if ($choice -ne "n" -and $choice -ne "N") {
        Start-Process "https://www.python.org/downloads/"
        Write-Host ""
        Write-Host "  After installing Python, re-run this script." -ForegroundColor Yellow
        Write-Host "  IMPORTANT: Check 'Add Python to PATH' during install!" -ForegroundColor Yellow
    }
    exit 1
}

# ── 2. Install the package ───────────────────────────────────
Write-Info "Installing $PACKAGE via pip..."
try {
    & $pyCmd -m pip install --user --upgrade $PACKAGE
    Write-OK "Package installed"
} catch {
    Write-Fail "pip install failed: $_"
}

# ── 3. Find the Scripts directory and add to user PATH ───────
Write-Info "Locating Scripts directory..."

# Get user site-packages, then derive Scripts path
$scriptsDir = $null
try {
    $userBase = & $pyCmd -c "import site; print(site.getuserbase())"
    $scriptsDir = Join-Path $userBase "Scripts"
} catch {}

if (-not $scriptsDir -or -not (Test-Path $scriptsDir)) {
    # Fallback: search common locations
    $candidates = @(
        "$env:APPDATA\Python\Scripts",
        "$env:LOCALAPPDATA\Programs\Python\*\Scripts",
        "$env:USERPROFILE\AppData\Roaming\Python\*\Scripts"
    )
    foreach ($p in $candidates) {
        $found = Resolve-Path $p -ErrorAction SilentlyContinue
        if ($found) { $scriptsDir = $found.Path; break }
    }
}

if (-not $scriptsDir) {
    Write-Warn "Could not find Scripts directory automatically."
    Write-Warn "Run:  $pyCmd -c `"import site; print(site.getuserbase())`"  to find it."
    Write-Warn "Then add that folder\Scripts to your user PATH manually."
} else {
    Write-OK "Scripts dir: $scriptsDir"

    # Add to user PATH permanently (no admin required)
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($currentPath -notlike "*$scriptsDir*") {
        [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$scriptsDir", "User")
        $env:PATH += ";$scriptsDir"
        Write-OK "Added to user PATH permanently"
        Write-Warn "PATH update takes effect in new terminal windows."
    } else {
        Write-OK "Scripts dir already in PATH"
    }
}

# ── 4. Verify ────────────────────────────────────────────────
Write-Host ""
if (Get-Command "aaru" -ErrorAction SilentlyContinue) {
    Write-OK "'aaru' command is ready!"
} else {
    # Try refreshing PATH in current session
    $env:PATH = [Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                [Environment]::GetEnvironmentVariable("PATH","User")
    if (Get-Command "aaru" -ErrorAction SilentlyContinue) {
        Write-OK "'aaru' command is ready!"
    } else {
        Write-Warn "'aaru' will work in a NEW terminal window."
        Write-Warn "In THIS window, use:  $pyCmd -m aarush --help"
    }
}

Write-Host ""
Write-Host "  ✅  AARU CLI installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "  Quick start:"
Write-Host "    aaru aaru          <- show banner"
Write-Host "    aaru --help        <- all commands"
Write-Host "    aaru init          <- init a repo"
Write-Host ""
Write-Host "  Fallback (this terminal only):"
Write-Host "    $pyCmd -m aarush aaru"
Write-Host ""
