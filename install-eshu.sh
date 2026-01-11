#!/usr/bin/env bash
#
# ESHU Installer - User-Friendly Installation Script
# Handles Python virtual environments automatically
#
# Usage:
#   ./install-eshu.sh           # Interactive install
#   ./install-eshu.sh --force   # Force reinstall without prompting
#

set -e

# Parse arguments
FORCE_INSTALL=false
for arg in "$@"; do
    case $arg in
        -f|--force)
            FORCE_INSTALL=true
            shift
            ;;
    esac
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run this script as root"
    print_info "ESHU will ask for sudo when needed"
    exit 1
fi

print_header "ESHU Universal Package Installer"
echo ""
echo "This script will install ESHU in a Python virtual environment"
echo "and create a system-wide command for easy access."
echo ""

# Detect Python version
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
        PYTHON_CMD="python3"
        print_success "Found Python $PYTHON_VERSION"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    print_error "Python 3.9+ is required but not found"
    print_info "Install Python with: sudo pacman -S python python-pip"
    exit 1
fi

# Check for pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    print_error "pip is not installed"
    print_info "Install pip with: sudo pacman -S python-pip"
    exit 1
fi

print_success "pip is available"

# Determine installation directory
INSTALL_DIR="$HOME/.local/share/eshu"
BIN_DIR="$HOME/.local/bin"
VENV_DIR="$INSTALL_DIR/venv"
REPO_URL="https://github.com/eshu-apps/eshu-installer.git"

# Check if running from a cloned git repo
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -d "$SCRIPT_DIR/.git" ]; then
    # User has cloned the repo - use that location for installation
    INSTALL_DIR="$SCRIPT_DIR"
    VENV_DIR="$INSTALL_DIR/venv"
    print_info "Detected git repository at: $INSTALL_DIR"
    print_info "Installing from your cloned repo"
else
    print_info "Installation directory: $INSTALL_DIR"
fi

print_info "Binary directory: $BIN_DIR"

# Create directories
mkdir -p "$BIN_DIR"

# Check if git is available (only needed if not installing from existing repo)
if [ ! -d "$SCRIPT_DIR/.git" ]; then
    if ! command -v git &> /dev/null; then
        print_error "git is required but not installed"
        print_info "Install git with your package manager"
        exit 1
    fi
fi

# Check if already installed
if [ -d "$VENV_DIR" ]; then
    if [ "$FORCE_INSTALL" = true ]; then
        print_info "Force reinstall requested, removing old installation..."
        rm -rf "$VENV_DIR"
    else
        # Check if stdin is a terminal (interactive)
        if [ -t 0 ]; then
            print_warning "ESHU is already installed"
            read -p "Do you want to reinstall? [y/N] " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_info "Installation cancelled"
                print_info "To update, run: eshu update"
                exit 0
            fi
            print_info "Removing old installation..."
            rm -rf "$VENV_DIR"
        else
            # Non-interactive (piped from curl) - auto-update
            print_info "ESHU is already installed, updating..."
            rm -rf "$VENV_DIR"
        fi
    fi
fi

# Clone or update repository (only if not installing from existing repo)
if [ ! -d "$SCRIPT_DIR/.git" ]; then
    print_header "Downloading ESHU"

    if [ -d "$INSTALL_DIR/.git" ]; then
        print_info "Updating existing repository..."
        git -C "$INSTALL_DIR" pull
        print_success "Repository updated"
    else
        print_info "Cloning repository..."
        if git clone "$REPO_URL" "$INSTALL_DIR" > /dev/null 2>&1; then
            print_success "Repository cloned"
        else
            print_error "Failed to clone repository"
            exit 1
        fi
    fi
fi

# Create virtual environment
print_header "Creating Python Virtual Environment"
$PYTHON_CMD -m venv "$VENV_DIR"
print_success "Virtual environment created"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
print_success "pip upgraded"

# Install ESHU
print_header "Installing ESHU"
print_info "This may take a minute..."

# Install from cloned directory
if pip install -e "$INSTALL_DIR" > /tmp/eshu-install.log 2>&1; then
    print_success "ESHU installed successfully"
else
    print_error "Installation failed. Check /tmp/eshu-install.log for details"
    cat /tmp/eshu-install.log
    exit 1
fi

# Create wrapper script
print_header "Creating System Command"

WRAPPER_SCRIPT="$BIN_DIR/eshu"
cat > "$WRAPPER_SCRIPT" << EOF
#!/usr/bin/env bash
# ESHU wrapper script
VENV_DIR="$VENV_DIR"
source "\$VENV_DIR/bin/activate"
exec python -m eshu.cli_enhanced "\$@"
EOF

chmod +x "$WRAPPER_SCRIPT"
print_success "Created eshu command at $WRAPPER_SCRIPT"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    print_warning "~/.local/bin is not in your PATH"
    echo ""
    print_info "Add this to your shell config (~/.bashrc or ~/.config/fish/config.fish):"
    echo ""
    if [ -n "$FISH_VERSION" ]; then
        echo "  set -gx PATH \$HOME/.local/bin \$PATH"
    else
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
    echo ""
    print_info "Then reload your shell or run: source ~/.bashrc"
    echo ""
fi

# Test installation
print_header "Testing Installation"
if "$WRAPPER_SCRIPT" --version &> /dev/null; then
    print_success "ESHU is working correctly!"
else
    print_warning "ESHU command created but test failed"
    print_info "Try running: eshu --help"
fi

# Print next steps
print_header "Installation Complete!"
echo ""
print_success "ESHU has been installed successfully!"
echo ""
print_info "Quick Start:"
echo "  eshu search firefox       # Search for packages"
echo "  eshu install hyprland     # Install packages"
echo "  eshu profile              # View system info"
echo ""
print_info "Optional: Add AI Features"
echo "  1. Install Ollama (free, local):"
echo "     curl -fsSL https://ollama.com/install.sh | sh"
echo "     ollama pull llama3.1:8b"
echo "     eshu config set-provider ollama"
echo ""
echo "  2. Or use Anthropic Claude (paid API):"
echo "     export ANTHROPIC_API_KEY='your-key'"
echo "     eshu config set-provider anthropic"
echo ""
print_info "Documentation: https://github.com/eshu-apps/eshu-installer"
print_info "Premium Features: https://eshuapps.gumroad.com/l/eshu-premium"
echo ""
print_success "Happy installing! 🚀"
echo ""

# Install systemd service for auto-profiling
print_header "System Profiling Service"
echo ""
print_info "Install systemd service to auto-scan system at boot?"
print_info "Benefits: Instant searches, pre-cached system info"
echo ""
read -p "Install service? [Y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    SYSTEMD_SRC="$INSTALL_DIR/systemd"

    if [ -d "$SYSTEMD_SRC" ]; then
        # Update service file to use correct eshu path
        sudo cp "$SYSTEMD_SRC/eshu-profiler.service" /etc/systemd/system/
        sudo cp "$SYSTEMD_SRC/eshu-profiler.timer" /etc/systemd/system/

        # Update ExecStart path in service
        sudo sed -i "s|/usr/bin/eshu|$WRAPPER_SCRIPT|g" /etc/systemd/system/eshu-profiler.service

        sudo systemctl daemon-reload
        sudo systemctl enable --now eshu-profiler.timer

        print_success "Systemd service installed and enabled!"
        print_info "System will be profiled at boot + daily"
        print_info "Run manually: sudo systemctl start eshu-profiler"
    else
        print_warning "Systemd files not found, skipping"
    fi
fi

# Run initial profile scan
print_header "Initial System Scan"
print_info "Scanning system (one-time, ~2 seconds)..."
"$WRAPPER_SCRIPT" profile --refresh &>/dev/null || print_warning "Profile scan failed (non-critical)"

# Run setup wizard if this is the first install
if [ ! -f "$INSTALL_DIR/.setup_complete" ]; then
    print_header "Running Setup Wizard"
    "$WRAPPER_SCRIPT" setup
    touch "$INSTALL_DIR/.setup_complete"
fi
