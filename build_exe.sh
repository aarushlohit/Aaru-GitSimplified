#!/bin/bash
# Build AARU CLI as standalone executable for Linux
# This creates a single binary that can run without Python installed

echo ""
echo "================================"
echo "  AARU CLI - Binary Builder"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    exit 1
fi

echo "[OK] Python is installed"
python3 --version
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "[INFO] PyInstaller not found. Installing..."
    python3 -m pip install --user pyinstaller
    echo ""
fi

# Install dependencies
echo "[INFO] Installing dependencies..."
python3 -m pip install --user -r requirements.txt
echo ""

# Build the executable
echo "[INFO] Building aaru binary..."
echo "This may take a few minutes..."
echo ""

pyinstaller --clean aaru.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "  Build Successful!"
    echo "================================"
    echo ""
    echo "The executable has been created at:"
    echo "  dist/aaru"
    echo ""
    echo "You can:"
    echo "  1. Run it directly: ./dist/aaru"
    echo "  2. Copy to /usr/local/bin: sudo cp dist/aaru /usr/local/bin/"
    echo "  3. Add dist folder to PATH"
    echo ""
    echo "Installation command:"
    echo "  sudo cp dist/aaru /usr/local/bin/ && sudo chmod +x /usr/local/bin/aaru"
    echo ""
else
    echo ""
    echo "[ERROR] Build failed. Please check the errors above."
    exit 1
fi
