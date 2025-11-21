# GroveGrab CLI - Summary

## What It Is
A command-line tool for downloading Spotify tracks, playlists, albums, and artists using your own Spotify API credentials and SpotDL.

## Key Features

### Download Capabilities
- Single tracks, playlists, albums, and artists
- Batch downloads from file
- High-quality audio (MP3 up to 320kbps, FLAC, OGG, OPUS, M4A)
- Automatic metadata tagging

### User Experience
- Beautiful terminal UI with progress bars
- Individual song progress for playlists/albums
- Real-time download tracking
- Interactive setup wizard
- ASCII art banner

### Task Management
- List active/completed downloads
- Cancel running downloads
- Retry failed downloads
- View detailed logs
- Background mode option

### Configuration
- Your own Spotify API credentials (free)
- Customizable download paths
- Audio format and quality settings
- Platform-specific defaults (Windows/Mac/Linux/Android)

### Cross-Platform
- Windows, macOS, Linux support
- Android (Termux) support
- Platform-specific default paths
- No Unicode issues on Windows

## Technical Highlights
- Built with Python 3.8+
- Uses SpotDL for actual downloads
- Rich terminal UI library
- Typer CLI framework
- FFmpeg for audio conversion
- Modular architecture (config, core, ui, cli)

## Installation
```bash
pip install GroveGrabCLI
```

## Quick Start
```bash
# Setup credentials
grovegrab auth

# Download something
grovegrab dl "spotify_url"
```

## Use Cases
- Personal music library backup
- Offline playlist creation
- High-quality audio collection
- Cross-platform music management
- Automated batch downloads

## Advantages
- ✅ Free and open source
- ✅ Your own API = no rate limits
- ✅ High quality audio
- ✅ Simple CLI interface
- ✅ Works on Android
- ✅ Organized folder structure
- ✅ Smart caching
- ✅ Concurrent downloads

## Requirements
- Python 3.8+
- FFmpeg
- Spotify API credentials (free)
- Internet connection

## PyPI
https://pypi.org/project/GroveGrabCLI/

## GitHub
https://github.com/GopikChenth/GroveGrab-CLI
