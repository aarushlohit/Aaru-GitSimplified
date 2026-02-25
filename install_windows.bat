@echo off
REM ============================================================
REM  AARU CLI — Easy Windows Installer
REM  Double-click this file or run in Command Prompt!
REM ============================================================
title AARU CLI Installer

echo.
echo  =========================================
echo   AARU CLI - Easy Windows Installer
echo  =========================================
echo.

REM ── 1. Check Python ─────────────────────────────────────────
echo  [..] Checking for Python...

python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  [OK] Found %%v
    set PY=python
    goto :install
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%v in ('py --version 2^>^&1') do echo  [OK] Found %%v
    set PY=py
    goto :install
)

echo  [X]  Python 3 not found.
echo.
echo  You need Python 3.8 or higher.
echo  Opening download page in your browser...
start https://www.python.org/downloads/
echo.
echo  IMPORTANT: Check "Add Python to PATH" during installation!
echo.
pause
exit /b 1

:install
REM ── 2. Install the package ───────────────────────────────────
echo.
echo  [..] Installing aarushlohit-git via pip...
echo.

%PY% -m pip install --user --upgrade aarushlohit-git
if %errorlevel% neq 0 (
    echo.
    echo  [X]  pip install failed. Trying without --user flag...
    %PY% -m pip install --upgrade aarushlohit-git
    if %errorlevel% neq 0 (
        echo  [X]  Installation failed. Check errors above.
        pause
        exit /b 1
    )
)
echo.
echo  [OK] Package installed.

REM ── 3. Find Scripts dir and add to PATH ─────────────────────
echo  [..] Adding 'aaru' command to your PATH...

for /f "tokens=*" %%p in ('%PY% -c "import site; print(site.getuserbase())"') do set USER_BASE=%%p
set SCRIPTS_DIR=%USER_BASE%\Scripts
echo  [OK] Scripts dir: %SCRIPTS_DIR%

REM Read current user PATH from registry
for /f "skip=2 tokens=2*" %%a in ('reg query HKCU\Environment /v PATH 2^>nul') do set CUR_PATH=%%b

if "%CUR_PATH%"=="" (
    setx PATH "%SCRIPTS_DIR%" >nul 2>&1
    set PATH=%PATH%;%SCRIPTS_DIR%
    echo  [OK] PATH set to include %SCRIPTS_DIR%
    goto :verify
)

echo %CUR_PATH% | findstr /i "%SCRIPTS_DIR%" >nul 2>&1
if %errorlevel% neq 0 (
    setx PATH "%CUR_PATH%;%SCRIPTS_DIR%" >nul 2>&1
    set PATH=%PATH%;%SCRIPTS_DIR%
    echo  [OK] Added to user PATH permanently.
    echo  [!]  Open a NEW terminal for 'aaru' to work everywhere.
) else (
    echo  [OK] Already in PATH.
    set PATH=%PATH%;%SCRIPTS_DIR%
)

:verify
REM ── 4. Verify ────────────────────────────────────────────────
echo.
where aaru >nul 2>&1
if %errorlevel% equ 0 (
    echo  [OK] 'aaru' is ready in this window!
) else (
    echo  [!]  'aaru' will work in a NEW terminal window.
    echo  [!]  In THIS window:  %PY% -m aarush --help
)

echo.
echo  =========================================
echo   AARU CLI installed successfully!
echo  =========================================
echo.
echo  Open a new terminal/cmd window, then:
echo.
echo    aaru aaru          ^<-- show banner
echo    aaru --help        ^<-- all commands
echo    aaru init          ^<-- init a repo
echo.
echo  Right now in this window:
echo    %PY% -m aarush aaru
echo.
pause
