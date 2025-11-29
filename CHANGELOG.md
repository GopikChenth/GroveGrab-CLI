# Changelog

All notable changes to GroveGrab CLI will be documented in this file.

## [1.0.6] - 2025-11-29

### Fixed
- **CRITICAL: Fixed SpotDL command structure** - Removed incorrect "download" subcommand that was causing "unrecognized arguments" errors
- **Fixed path template syntax** - Changed `{output-ext}` to `{ext}` for compatibility with SpotDL 3.9.6
- **Fixed download verification** - Added proper null checks and file verification after download completes
- Downloads now work correctly with SpotDL 3.9.6+ syntax

### Changed
- Simplified SpotDL command building to use `spotdl [url] [options]` format
- Uses YouTube Music by default (more reliable than direct YouTube)
- Better error handling for missing download paths
- Added success verification with actual file count

## [1.0.5] - 2025-11-21

### Added
- **New ASCII banner** with "GROVEGRAB" text and tagline "Your music — no limits, no loading"
- **First-run experience** - interactive setup prompt on first use
- Welcome message with quick setup guide
- Option to run setup wizard immediately or later

### Changed
- Improved banner gradient colors (cyan to magenta)
- Better onboarding flow for new users
- More user-friendly error messages

## [1.0.4] - 2025-11-21

### Added
- Comprehensive Android/Termux installation guide in README
- Platform-specific tips during auth setup wizard for Android users
- Detailed instructions for changing download directory
- SD card path detection guide for Android

### Changed
- Improved setup wizard with Android-specific path suggestions
- Enhanced documentation with three methods to change download directory

## [1.0.3] - 2025-11-21

### Added
- **Android/Termux support** - Automatic platform detection for default download paths
- Platform-specific defaults: `/storage/emulated/0/Music/GroveGrab` for Android, `~/Music/GroveGrab` for Windows/Mac/Linux

### Changed
- Improved default path logic to automatically detect Termux environment

## [1.0.2] - 2025-11-21

### Changed
- **Improved error message** when Spotify credentials are not configured
- Added clearer setup instructions in error output
- Updated README with prominent first-time setup warning
- Added troubleshooting section for common "No client_id" error
- Better documentation about where config files are stored

### Fixed
- Users now get clear guidance when trying to download without credentials

## [1.0.1] - 2025-11-21

### Added
- Initial PyPI release
- Support for downloading tracks, playlists, albums, and artists
- Interactive auth setup wizard
- Real-time progress tracking
- Task management (list, cancel, retry)
- Batch downloads
- Beautiful ASCII art banner
- Comprehensive documentation

## [1.0.0] - 2025-11-21

### Added
- Initial release
- Core download functionality
- Configuration management
- CLI interface with Typer
