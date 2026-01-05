#!/usr/bin/env bash
#
# ESHU Installer - User-Friendly Installation Script
# Handles Python virtual environments automatically
#

set -e

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

print_info "Installation directory: $INSTALL_DIR"
print_info "Binary directory: $BIN_DIR"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Check if already installed
if [ -d "$VENV_DIR" ]; then
    print_warning "ESHU is already installed"
    read -p "Do you want to reinstall? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled"
        exit 0
    fi
    print_info "Removing old installation..."
    rm -rf "$VENV_DIR"
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

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install from local directory
if pip install -e "$SCRIPT_DIR" > /tmp/eshu-install.log 2>&1; then
    print_success "ESHU installed successfully"
else
    print_error "Installation failed. Check /tmp/eshu-install.log for details"
    cat /tmp/eshu-install.log
    exit 1
fi

# Create wrapper script
print_header "Creating System Command"

WRAPPER_SCRIPT="$BIN_DIR/eshu"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/usr/bin/env bash
# ESHU wrapper script
VENV_DIR="$HOME/.local/share/eshu/venv"
source "$VENV_DIR/bin/activate"
exec python -m eshu.cli_enhanced "$@"
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
