#!/usr/bin/env bash
# ============================================================
#  AARU CLI — Easy Installer for Linux & macOS
#  Usage:
#    bash install.sh
#  One-liner (from GitHub):
#    curl -fsSL https://raw.githubusercontent.com/aarushlohit/GIT_PROTOCOL/main/install.sh | bash
# ============================================================
set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

PACKAGE="aarushlohit-git"

banner() {
    echo ""
    echo -e "${CYAN}${BOLD}╔══════════════════════════════════╗${RESET}"
    echo -e "${CYAN}${BOLD}║       AARU CLI — Installer       ║${RESET}"
    echo -e "${CYAN}${BOLD}╚══════════════════════════════════╝${RESET}"
    echo ""
}

ok()   { echo -e "${GREEN}  ✔ $*${RESET}"; }
warn() { echo -e "${YELLOW}  ⚠ $*${RESET}"; }
fail() { echo -e "${RED}  ✖ $*${RESET}"; exit 1; }
info() { echo -e "  → $*"; }

# ── 1. Check Python ─────────────────────────────────────────
check_python() {
    if command -v python3 &>/dev/null; then
        PY="python3"
    elif command -v python &>/dev/null && python -c "import sys; sys.exit(0 if sys.version_info[0]==3 else 1)" 2>/dev/null; then
        PY="python"
    else
        fail "Python 3 not found.\nPlease install Python 3.8+: https://python.org/downloads"
    fi
    PY_VER=$($PY -c "import sys; print('.'.join(map(str,sys.version_info[:2])))")
    ok "Python $PY_VER found ($PY)"
}

# ── 2. Detect shell config file ──────────────────────────────
detect_shell_rc() {
    case "${SHELL:-$(command -v sh)}" in
        */zsh)  echo "$HOME/.zshrc" ;;
        */fish) echo "$HOME/.config/fish/config.fish" ;;
        */bash) echo "$HOME/.bashrc" ;;
        *)      echo "$HOME/.profile" ;;
    esac
}

# ── 3. Add dir to PATH permanently ──────────────────────────
add_to_path() {
    local dir="$1"
    local rc
    rc=$(detect_shell_rc)
    if [[ ":$PATH:" != *":$dir:"* ]]; then
        if [[ "$rc" == *.fish ]]; then
            echo "fish_add_path $dir" >> "$rc"
        else
            echo "export PATH=\"$dir:\$PATH\"" >> "$rc"
        fi
        export PATH="$dir:$PATH"
        warn "Added $dir to PATH in $rc"
        warn "Run:  source $rc   (or restart your terminal)"
    fi
}

# ── 4. Install ───────────────────────────────────────────────
install_aaru() {
    # Try pipx first — cleanest, no PATH headaches
    if command -v pipx &>/dev/null; then
        info "Installing via pipx..."
        pipx install "$PACKAGE" --force
        pipx ensurepath
        ok "Installed via pipx"
        return 0
    fi

    # Detect externally-managed env (PEP 668 — Arch, Debian 12+, Ubuntu 23+)
    EXTERNALLY_MANAGED=false
    if $PY -m pip install --dry-run --user pip 2>&1 | grep -q "externally-managed"; then
        EXTERNALLY_MANAGED=true
    fi

    if [ "$EXTERNALLY_MANAGED" = true ]; then
        info "Externally-managed Python detected — will install pipx first..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get install -y pipx 2>/dev/null && pipx ensurepath || true
        elif command -v pacman &>/dev/null; then
            sudo pacman -S --noconfirm python-pipx 2>/dev/null || true
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y pipx 2>/dev/null || true
        elif command -v brew &>/dev/null; then
            brew install pipx && pipx ensurepath || true
        else
            $PY -m pip install --user pipx 2>/dev/null || true
            add_to_path "$HOME/.local/bin"
        fi

        if command -v pipx &>/dev/null; then
            pipx install "$PACKAGE" --force
            pipx ensurepath
            ok "Installed via pipx"
            return 0
        fi

        # Last resort
        warn "pipx unavailable — using pip with --break-system-packages"
        $PY -m pip install --user --break-system-packages "$PACKAGE"
    else
        info "Installing via pip..."
        $PY -m pip install --user --upgrade "$PACKAGE"
    fi

    add_to_path "$HOME/.local/bin"
    ok "Installed via pip"
}

# ── 5. Verify ────────────────────────────────────────────────
verify() {
    if command -v aaru &>/dev/null; then
        ok "'aaru' command is ready!"
    else
        warn "'aaru' is installed but not yet on PATH in this session."
        echo ""
        local rc
        rc=$(detect_shell_rc)
        echo -e "  ${BOLD}Activate it now:${RESET}"
        echo -e "    source $rc"
        echo "  Or just open a new terminal."
    fi
}

# ── Main ─────────────────────────────────────────────────────
main() {
    banner
    check_python
    install_aaru

    echo ""
    echo -e "${GREEN}${BOLD}✅  AARU CLI installed successfully!${RESET}"
    echo ""
    verify
    echo ""
    echo "  Quick start:"
    echo "    aaru aaru          ← show banner"
    echo "    aaru --help        ← all commands"
    echo "    aaru init          ← init a repo"
    echo ""
    echo "  Immediate fallback (no restart needed):"
    echo "    python3 -m aarush --help"
    echo ""
}

main
