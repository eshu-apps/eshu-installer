# Changelog

All notable changes to ESHU Installer will be documented in this file.

## [0.4.6] - 2026-01-10

### 🔥 Major Features

#### Eshu's Path - Community Database Building
- **AI now generates bundle recommendations for ALL users** (free + premium)
- Free users see first 2 packages + teaser ("... and X more (Premium)")
- Premium users see full bundle with one-click install
- **Every search helps build the community recommendations database**
- All bundles stored in database with success/failure tracking

#### Complete Analytics Integration
- **Installation tracking**: Success/failure/duration for all installs
- **Error tracking**: Error patterns, recovery attempts
- **Manager usage**: Statistics on which package managers work best
- **Performance metrics**: System scan, search, and install times
- **Bundle tracking**: Success/failure rates for AI-generated bundles

### Added
- Analytics tracking for installation success/failure (singles + bundles)
- Performance tracking for system scans, package searches, installs
- Package manager usage statistics
- Error pattern collection
- Bundle success/failure rate tracking in database
- Free user display for AI-generated bundles (obfuscated)

### Changed
- **BREAKING**: Eshu's Path now generates for everyone (was premium-only)
  - Free users: See teaser, contribute to database
  - Premium users: Full access to install bundles
- Analytics initialization moved before system scan (for performance tracking)

### Fixed
- Analytics module was only tracking searches (10% functional)
  - Now tracks installations, errors, performance, manager usage (100% functional)
- Bundle database wasn't tracking success/failure rates
  - Now fully tracks usage, successes, and failures
- Free users never saw AI-generated bundles
  - Now see obfuscated bundles and contribute to database

### Privacy
- All tracking remains local-first (stored in `~/.cache/eshu/`)
- No PII collected (no names, emails, IP addresses)
- Opt-out available: `eshu config set analytics_enabled false`
- See PRIVACY.md for complete details

---

## [0.4.5] - 2026-01-09

### Fixed
- System scan reduced from 5 minutes to 2 seconds (removed pacman -Qi loop)
- LLM 404 errors now completely silent (no user interruption)
- Multi-number selection from search results now works
- Systemd service installation restored

### Added
- Setup wizard runs on first install
- Initial profile scan during installation

---

## [0.4.0] - 2026-01-08

### Added
- Ghost Mode (FREE!) - Try packages in isolated environments
- Eshufile export/apply for reproducible setups
- GitHub repository search integration
- System maintenance command
- Setup wizard for AI configuration
- Update command for easy upgrades
- Stats tracking
- Trace integration for package bisection

---

## [0.3.0] - 2026-01-05

### Initial Features
- Universal package search across all managers
- AI-powered package installation
- System profiling and caching
- Premium features: Snapshots, Cleanup, Unlimited AI
- Multi-package manager support (pacman, apt, yay, paru, flatpak, snap, etc.)
- License management
- LLM provider configuration (Ollama, Anthropic, OpenAI)
