# Contributing to ESHU

Thank you for your interest in contributing to ESHU! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/eshu-installer.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add: your feature description"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest pytest-cov black ruff mypy
```

## Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

```bash
# Format code
black src/

# Lint
ruff check src/

# Type check
mypy src/
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=eshu tests/
```

## Areas for Contribution

### High Priority
- [ ] Additional package manager support (dnf, zypper, etc.)
- [ ] Better error handling and recovery
- [ ] GUI interface (Electron or Tauri)
- [ ] More Eshu's Path bundles

### Medium Priority
- [ ] Package conflict resolution
- [ ] Better size information for all package managers
- [ ] Improved caching mechanisms
- [ ] Multi-language support (i18n)

### Low Priority
- [ ] Plugin system for community bundles
- [ ] Import/export package lists
- [ ] Windows WSL2 support

## Pull Request Guidelines

1. **One feature per PR** - Keep PRs focused
2. **Write tests** - Add tests for new features
3. **Update docs** - Update README and docs as needed
4. **Follow code style** - Run black/ruff before committing
5. **Descriptive commits** - Use clear commit messages

## Commit Message Format

```
Type: Brief description

Longer description if needed

Fixes #123
```

Types:
- `Add:` New feature
- `Fix:` Bug fix
- `Docs:` Documentation changes
- `Style:` Code style changes (formatting, etc.)
- `Refactor:` Code refactoring
- `Test:` Adding or updating tests
- `Chore:` Maintenance tasks

## Adding a New Package Manager

To add support for a new package manager:

1. Add search method in `src/eshu/package_search.py`:
```python
def search_newpm(self, query: str) -> List[PackageResult]:
    """Search newpm repositories"""
    results = []
    # Implementation here
    return results
```

2. Add to `search_functions` dict in `search_all()` method

3. Add installation support in `src/eshu/package_installer.py`

4. Update documentation

## Questions?

- Open an issue for questions
- Join discussions on GitHub
- Email: support@eshu-installer.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
