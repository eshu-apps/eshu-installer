# ESHU Architecture Documentation

## Overview

ESHU (Easy Setup Utility) is an AI-driven universal package installer that abstracts away the complexity of multiple package managers on Linux systems. It uses LLM intelligence to interpret natural language queries, search across all available package managers, and adaptively handle installation issues.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              User Interface                              │
│                         (CLI via Typer + Rich)                           │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          Command Router (cli.py)                         │
│  • install    • search    • profile    • config    • version            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
                 ▼               ▼               ▼
┌──────────────────────┐ ┌──────────────┐ ┌─────────────────┐
│   LLM Engine         │ │   System     │ │   Package       │
│  (llm_engine.py)     │ │   Profiler   │ │   Searcher      │
│                      │ │  (system_    │ │  (package_      │
│ • Query interpret    │ │   profiler.  │ │   search.py)    │
│ • Reshult ranking     │ │   py)        │ │                 │
│ • Install planning   │ │              │ │ • Multi-manager │
│ • Error analysis     │ │ • Distro     │ │   search        │
│                      │ │   detection  │ │ • Reshult        │
│ Providers:           │ │ • Package    │ │   ranking       │
│ • Anthropic Claude   │ │   scanning   │ │ • Parallel      │
│ • OpenAI GPT         │ │ • Manager    │ │   execution     │
│ • Ollama (local)     │ │   detection  │ │                 │
└──────────┬───────────┘ └──────┬───────┘ └────────┬────────┘
           │                    │                   │
           │                    │                   │
           └────────────────────┼───────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Package Installer   │
                    │    (installer.py)     │
                    │                       │
                    │ • Command execution   │
                    │ • Dependency handling │
                    │ • Build management    │
                    │ • Error recovery      │
                    │ • Verification        │
                    └───────────┬───────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              Package Manager Abstraction Layer                          │
│                                                                          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │ pacman │ │  yay   │ │  apt   │ │flatpak │ │  snap  │ │ cargo  │   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              │
│  │  npm   │ │  pip   │ │  dnf   │ │ zypper │ │  gem   │              │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Operating System                                 │
│                    (Arch, Debian, Fedora, etc.)                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Configuration Management (`config.py`)

**Purpose**: Centralized configuration using Pydantic models

**Key Features**:
- Environment variable support
- JSON configuration files
- Multiple LLM provider support
- Package manager priority ordering
- Cache and build directory management

**Configuration Hierarchy**:
1. Environment variables (`ESHU_*`)
2. User config (`~/.config/eshu/config.json`)
3. System config (`/etc/eshu/config.json`)
4. Defaults

**Example**:
```python
config = ESHUConfig(
    llm_provider="anthropic",
    model_name="claude-3-5-sonnet-20241022",
    package_manager_priority=["pacman", "yay", "apt", "flatpak"],
    cache_dir=Path("/var/cache/eshu"),
    prefer_native=True
)
```

### 2. System Profiler (`system_profiler.py`)

**Purpose**: Scan and cache system state

**Responsibilities**:
- Detect Linux distribution and version
- Identify available package managers
- Scan installed packages across all managers
- Cache results for performance
- Track dependencies

**Data Model**:
```python
@dataclass
class SystemProfile:
    distro: str
    distro_version: str
    kernel: str
    arch: str
    available_managers: List[str]
    installed_packages: Dict[str, PackageInfo]
    timestamp: str
```

**Scanning Process**:
1. Read `/etc/os-release` for distro info
2. Check for package manager binaries in PATH
3. Query each manager for installed packages
4. Parse and normalize package information
5. Cache to `/var/cache/eshu/system_profile.json`

**Performance**:
- First scan: 5-10 seconds
- Cached reads: <100ms
- TTL: 1 hour (configurable)

### 3. Package Searcher (`package_search.py`)

**Purpose**: Unified search across all package managers

**Architecture**:
```python
class PackageSearcher:
    def search_all(query: str) -> List[PackageReshult]:
        # Parallel search across all managers
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.search_pacman, query),
                executor.submit(self.search_apt, query),
                executor.submit(self.search_flatpak, query),
                # ... etc
            }
            return collect_results(futures)
```

**Search Methods**:
- `search_pacman()`: Parse `pacman -Ss` output
- `search_yay()`: Parse `yay -Ss` for AUR packages
- `search_apt()`: Parse `apt-cache search` output
- `search_flatpak()`: Parse `flatpak search` output
- `search_snap()`: Parse `snap find` output
- `search_cargo()`: Parse `cargo search` output
- `search_npm()`: Parse `npm search --json` output
- `search_pip()`: Use `pip index versions`

**Reshult Ranking**:
1. Exact name match: +100 points
2. Name starts with query: +50 points
3. Name contains query: +25 points
4. Description match: +10 points
5. Native package manager: +5 points
6. Already installed: +2 points

**Parallelization**:
- Uses ThreadPoolExecutor with max 5 workers
- 15-second timeout per search
- Graceful failure handling

### 4. LLM Engine (`llm_engine.py`)

**Purpose**: AI-powered intelligence layer

**Capabilities**:

#### Query Interpretation
```python
def interpret_query(query: str, profile: SystemProfile) -> Dict:
    # Input: "install hyprland"
    # Output: {
    #   "search_terms": ["hyprland"],
    #   "preferred_manager": None,
    #   "intent": "install",
    #   "requirements": []
    # }
```

#### Reshult Ranking & Recommendation
```python
def rank_and_recommend(
    query: str,
    results: List[PackageReshult],
    profile: SystemProfile
) -> List[Tuple[PackageReshult, str]]:
    # Returns ordered results with explanations
    # Example: "✓ RECOMMENDED: hyprland from pacman is the stable release..."
```

#### Installation Planning
```python
def generate_install_plan(
    package: PackageReshult,
    profile: SystemProfile
) -> Dict:
    # Returns: {
    #   "commands": ["sudo pacman -S hyprland"],
    #   "requires_build": False,
    #   "build_system": None,
    #   "dependencies": [],
    #   "post_install": [],
    #   "notes": "Standard installation"
    # }
```

#### Error Analysis
```python
def handle_error(
    error_output: str,
    package: PackageReshult,
    profile: SystemProfile
) -> Dict:
    # Analyzes error and suggests fixes
    # Returns: {
    #   "error_type": "dependency",
    #   "diagnosis": "Missing base-devel",
    #   "solutions": ["Install base-devel package group"],
    #   "commands": ["sudo pacman -S base-devel"]
    # }
```

**Provider Support**:

| Provider   | Model                      | Cost    | Speed  | Quality |
|------------|----------------------------|---------|--------|---------|
| Anthropic  | claude-3-5-sonnet-20241022 | $$$     | Fast   | Best    |
| OpenAI     | gpt-4-turbo-preview        | $$$     | Fast   | Great   |
| Ollama     | llama3.1:8b                | Free    | Medium | Good    |

### 5. Package Installer (`installer.py`)

**Purpose**: Execute installation with adaptive error handling

**Installation Flow**:
```
1. Generate installation plan (via LLM)
2. Display plan to user
3. Confirm installation
4. Install dependencies (if needed)
5. Execute installation commands
6. Handle errors adaptively
7. Run post-install steps
8. Verify installation
```

**Error Handling**:
```python
try:
    subprocess.run(install_command, check=True)
except CalledProcessError as e:
    # Use LLM to analyze error
    analysis = llm.handle_error(e.stderr, package, profile)
    
    # Display diagnosis and solutions
    print(f"Error: {analysis['diagnosis']}")
    print(f"Solutions: {analysis['solutions']}")
    
    # Offer to apply fixes
    if user_confirms():
        execute_commands(analysis['commands'])
        retry_installation()
```

**Build System Support**:
- **make**: `./configure && make && sudo make install`
- **cmake**: `mkdir build && cd build && cmake .. && make && sudo make install`
- **cargo**: `cargo build --release && cargo install --path .`
- **meson**: `meson setup build && meson compile -C build && sudo meson install -C build`
- **python**: `pip install .` or `python setup.py install`

**Verification**:
1. Check if binary exists in PATH
2. Query package manager for installation status
3. Verify version if possible

### 6. CLI Interface (`cli.py`)

**Purpose**: User-facing command-line interface

**Commands**:

#### `eshu install <query>`
- Interprets query with LLM
- Searches all package managers
- Displays ranked results
- Installs selected package
- Handles errors adaptively

**Options**:
- `-y, --yes`: Auto-confirm
- `-r, --refresh`: Refresh system profile
- `-m, --manager`: Prefer specific manager

#### `eshu search <query>`
- Searches all package managers
- Displays results in table format
- Shows installation status

#### `eshu profile`
- Displays system information
- Shows available package managers
- Lists installed packages (with `--packages`)
- Forces refresh (with `--refresh`)

#### `eshu config <action>`
- `show`: Display current configuration
- `set-key`: Set API key
- `set-provider`: Change LLM provider

#### `eshu version`
- Shows ESHU version

**UI Components**:
- **Rich Console**: Colored, formatted output
- **Tables**: Structured data display
- **Panels**: Highlighted information boxes
- **Progress Spinners**: Visual feedback during operations

## Data Flow

### Installation Flow

```
User Input: "eshu install hyprland"
    │
    ▼
┌─────────────────────────────────────┐
│ 1. Load Configuration               │
│    - Read config file               │
│    - Check API keys                 │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 2. Load System Profile              │
│    - Check cache (TTL: 1h)          │
│    - Or scan system                 │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 3. Interpret Query (LLM)            │
│    Input: "hyprland"                │
│    Output: {search_terms: [...]}    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. Search All Package Managers      │
│    - Parallel execution             │
│    - 5 workers, 15s timeout         │
│    - Collect results                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 5. Rank Reshults                     │
│    - Score by relevance             │
│    - Sort by score                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 6. LLM Recommendation               │
│    - Analyze results                │
│    - Recommend best option          │
│    - Provide explanation            │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 7. Display Reshults                  │
│    - Show table                     │
│    - Highlight recommendation       │
│    - Prompt for selection           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 8. Generate Install Plan (LLM)      │
│    - Commands                       │
│    - Dependencies                   │
│    - Build requirements             │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 9. Execute Installation             │
│    - Install dependencies           │
│    - Run install commands           │
│    - Handle errors (LLM)            │
│    - Post-install steps             │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 10. Verify Installation             │
│     - Check PATH                    │
│     - Query package manager         │
│     - Report success                │
└─────────────────────────────────────┘
```

## Caching Strategy

### System Profile Cache
- **Location**: `/var/cache/eshu/system_profile.json`
- **TTL**: 1 hour (configurable)
- **Size**: ~100KB - 1MB depending on installed packages
- **Invalidation**: Manual refresh or TTL expiry

### Benefits
- Fast subsequent queries (<100ms vs 5-10s)
- Reduced system load
- Consistent results during session

## Security Considerations

### 1. Command Execution
- All `sudo` commands require user confirmation
- Commands are displayed before execution
- No arbitrary code execution from LLM responses

### 2. API Keys
- Stored in config file with user-only permissions
- Environment variable support for CI/CD
- Never logged or displayed

### 3. Package Verification
- Checksums verified by package managers
- GPG signature validation (pacman, apt)
- AUR packages show PKGBUILD before build

### 4. Build Isolation
- Builds run in `/tmp/eshu-builds`
- Separate directory per package
- Cleaned after installation

## Performance Optimization

### 1. Parallel Search
```python
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(search_fn, query) for search_fn in searches]
    results = [f.result(timeout=15) for f in as_completed(futures)]
```

### 2. Caching
- System profile cached for 1 hour
- LLM responses could be cached (future)
- Package search results cached per session

### 3. Lazy Loading
- Package managers loaded on-demand
- LLM client initialized only when needed
- System scan deferred until required

## Error Handling

### Levels of Error Handling

1. **Package Manager Errors**
   - Captured via subprocess stderr
   - Analyzed by LLM
   - Suggested fixes presented to user

2. **LLM Errors**
   - Fallback to rule-based parsing
   - Graceful degradation
   - User notified of reduced functionality

3. **Network Errors**
   - Retry with exponential backoff
   - Timeout after 15 seconds
   - Continue with available results

4. **Permission Errors**
   - Clear error messages
   - Suggest `sudo` if needed
   - Check file permissions

## Extensibility

### Adding New Package Managers

1. **Implement Search Method**:
```python
def search_newpm(self, query: str) -> List[PackageReshult]:
    result = subprocess.run(["newpm", "search", query], ...)
    return parse_results(result.stdout)
```

2. **Add to Search Functions**:
```python
search_functions = {
    "newpm": self.search_newpm,
    # ... existing managers
}
```

3. **Implement Installation**:
```python
if package.manager == "newpm":
    commands = [f"newpm install {package.name}"]
```

### Adding New LLM Providers

1. **Update Config**:
```python
class ESHUConfig(BaseModel):
    newprovider_api_key: Optional[str] = None
```

2. **Initialize Client**:
```python
elif self.config.llm_provider == "newprovider":
    self.client = NewProviderClient(api_key=...)
```

3. **Implement Methods**:
```python
if self.config.llm_provider == "newprovider":
    response = self.client.complete(prompt)
```

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Mock external dependencies
- Test error conditions

### Integration Tests
- Test component interactions
- Use test package managers
- Verify end-to-end flows

### System Tests
- Test on real systems
- Multiple distributions
- Various package managers

## Future Enhancements

### Planned Features
1. **Package Conflict Resolution**
   - Detect conflicting packages
   - Suggest alternatives
   - Handle version conflicts

2. **Rollback Functionality**
   - Track installations
   - Revert failed installs
   - Snapshot system state

3. **GUI Interface**
   - Electron or Tauri app
   - Visual package browser
   - Installation history

4. **Plugin System**
   - Custom package managers
   - Custom LLM providers
   - Custom search algorithms

5. **Package Recommendations**
   - Suggest related packages
   - Popular alternatives
   - Security updates

6. **Multi-Language Support**
   - Internationalization
   - Localized package descriptions
   - Regional package mirrors

## Dependencies

### Core Dependencies
- **Python**: ≥3.10
- **anthropic**: ≥0.18.0 (optional)
- **openai**: ≥1.12.0 (optional)
- **rich**: ≥13.7.0 (UI)
- **typer**: ≥0.9.0 (CLI)
- **pydantic**: ≥2.5.0 (config)
- **aiohttp**: ≥3.9.0 (async HTTP)
- **psutil**: ≥5.9.0 (system info)

### System Dependencies
- Package managers (pacman, apt, etc.)
- Build tools (make, cmake, cargo, etc.)
- Git (for AUR and source builds)

## Deployment

### Installation Methods

1. **pip install**:
```bash
pip install eshu
```

2. **From source**:
```bash
git clone https://github.com/yourusername/eshu
cd eshu
pip install -e .
```

3. **System-wide**:
```bash
sudo pip install eshu
```

### Systemd Service

```ini
[Unit]
Description=ESHU System Profiler
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/eshu profile --refresh

[Install]
WantedBy=multi-user.target
```

## Monitoring & Logging

### Logging Levels
- **DEBUG**: Detailed execution trace
- **INFO**: Normal operations
- **WARNING**: Recoverable errors
- **ERROR**: Failed operations

### Metrics
- Installation success rate
- Average installation time
- LLM API usage
- Cache hit rate

## License

MIT License - See LICENSE file

## Contributing

See CONTRIBUTING.md for guidelines

---

**ESHU Architecture** - Built for extensibility, performance, and reliability.
