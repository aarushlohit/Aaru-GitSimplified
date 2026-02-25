@echo off
REM Build AARU CLI as Windows Executable
REM This script creates a standalone aaru.exe file

echo.
echo ================================
echo   AARU CLI - EXE Builder
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] PyInstaller not found. Installing...
    python -m pip install pyinstaller
    echo.
)

REM Install dependencies
echo [INFO] Installing dependencies...
python -m pip install -r requirements.txt
echo.

REM Build the executable
echo [INFO] Building aaru.exe...
echo This may take a few minutes...
echo.

pyinstaller --clean aaru.spec

if %errorlevel% equ 0 (
    echo.
    echo ================================
    echo   Build Successful!
    echo ================================
    echo.
    echo The executable has been created at:
    echo   dist\aaru.exe
    echo.
    echo You can:
    echo   1. Run it directly: dist\aaru.exe
    echo   2. Copy it to a folder in your PATH
    echo   3. Create a desktop shortcut
    echo.
    echo Recommended: Add 'dist' folder to your system PATH
    echo.
) else (
    echo.
    echo [ERROR] Build failed. Please check the errors above.
    pause
    exit /b 1
)

pause
