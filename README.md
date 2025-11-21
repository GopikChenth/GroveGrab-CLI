# 🎵 GroveGrab CLI

A powerful command-line tool for downloading Spotify tracks, playlists, albums, and artists using your own Spotify API credentials.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

- 🎵 **Download Everything** - Tracks, playlists, albums, and artists
- 🔐 **Your API Credentials** - Use your own Spotify API to avoid rate limits
- 🎨 **Beautiful CLI** - Rich terminal UI with progress bars and colors
- 📋 **Individual Song Progress** - See each song's download progress in playlists/albums
- 🎧 **High Quality** - Download in MP3 (up to 320kbps), FLAC, OGG, OPUS, or M4A
- ⚡ **Fast & Efficient** - Concurrent downloads with real-time progress
- 📊 **Task Management** - List, cancel, retry, and view logs for all downloads
- 🔄 **Batch Downloads** - Download multiple URLs from a file
- 💾 **Smart Caching** - Skip already downloaded tracks
- 💻 **Windows Compatible** - Full support for Windows console (no Unicode issues)

## 📦 Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install GroveGrabCLI
```

### Option 2: Install from Source

```bash
git clone https://github.com/yourusername/grovegrab-cli.git
cd grovegrab-cli
pip install -e .
```

### Option 3: Install on Android (Termux)

1. **Install Termux** from [F-Droid](https://f-droid.org/) (NOT Play Store - outdated version)

2. **Update packages and install dependencies:**
   ```bash
   pkg update && pkg upgrade
   pkg install python ffmpeg
   ```

3. **Install GroveGrab:**
   ```bash
   pip install GroveGrabCLI
   ```

4. **Set up storage access (IMPORTANT for Android):**
   ```bash
   termux-setup-storage
   ```
   This allows access to your phone's internal storage and SD card.

5. **Configure download directory:**
   ```bash
   grovegrab auth
   ```
   When prompted for download path, use:
   - Internal Storage: `/storage/emulated/0/Music/GroveGrab`
   - SD Card: `/storage/XXXX-XXXX/Music/GroveGrab` (replace XXXX with your SD card ID)
   
   To find your SD card path:
   ```bash
   ls /storage/
   ```

### Prerequisites

- **Python 3.8+**
- **FFmpeg** - Required by SpotDL for audio conversion
  ```bash
  # Windows (Chocolatey)
  choco install ffmpeg
  
  # macOS
  brew install ffmpeg
  
  # Linux (Ubuntu/Debian)
  sudo apt install ffmpeg
  
  # Android (Termux)
  pkg install ffmpeg
  ```

## 🚀 Quick Start

### ⚠️ IMPORTANT: First Time Setup Required

**Before downloading anything, you MUST configure Spotify API credentials:**

```bash
grovegrab auth
```

This will guide you through getting free API credentials from Spotify.

#### How to get Spotify API credentials (FREE):

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (free account works!)
3. Click "Create an App"
4. Give it any name (e.g., "My GroveGrab")
5. Copy your **Client ID** and **Client Secret**
6. Click "Edit Settings" and add redirect URI: `http://localhost:8888/callback`
7. Save, then run `grovegrab auth` and paste your credentials

### Download Your First Track

```bash
grovegrab dl "https://open.spotify.com/track/..."
```

That's it! 🎉

## 📖 Usage

### Basic Commands

```bash
# Download a track/playlist/album
grovegrab dl "spotify_url"

# Download with custom settings
grovegrab dl "url" --format flac --quality 320k --output ~/Music

# Watch progress in real-time
grovegrab dl "url" --watch

# Run in background
grovegrab dl "url" --detach
```

### Configuration

```bash
# Run setup wizard
grovegrab auth

# Show current configuration
grovegrab config --show

# Reset configuration
grovegrab config --reset
```

### Task Management

```bash
# List active downloads
grovegrab list

# List all downloads (including completed)
grovegrab list --all

# Cancel a download
grovegrab cancel <task-id>

# Retry a failed download
grovegrab retry <task-id>

# View logs
grovegrab logs <task-id>

# Follow logs in real-time
grovegrab logs <task-id> --follow
```

### Batch Downloads

```bash
# Download from a file containing URLs
grovegrab batch urls.txt

# With custom worker count
grovegrab batch urls.txt --workers 5
```

**Example `urls.txt`:**
```
https://open.spotify.com/track/...
https://open.spotify.com/playlist/...
https://open.spotify.com/album/...
```

### Other Commands

```bash
# Show version
grovegrab version

# Get help
grovegrab --help
grovegrab dl --help
```

## 🎨 Screenshots

### Single Track Download
```
Starting download: track
Downloading: Artist - Song Name ████████████░░░░░░░░ 60%
```

### Playlist Download (Individual Songs)
```
Starting download: playlist
Overall: 15/31 tracks (2 failed) ████████████░░░░░░░░ 48%
Anirudh Ravichander - Pathala Pathala ───────────── 100%
The Weeknd - Blinding Lights ────────────────────── 100%
Drake - God's Plan ───────────────────────────────── 75%
Ed Sheeran - Shape of You ────────────────────────── 30%
```

### Task List
```
┌─ Download Tasks ────────────────────────────────────────────┐
│ ID       Status         Progress  Current Track    Stats    │
├──────────────────────────────────────────────────────────────┤
│ a1b2c3d4 > running     67%       Drake - Hotline  3/5       │
│ e5f6g7h8 OK completed  100%      -                10/10     │
│ i9j0k1l2 ERR failed    45%       -                5/12 (2)  │
└──────────────────────────────────────────────────────────────┘
```

## ⚙️ Configuration

Configuration is stored at:
- **Linux/Mac**: `~/.config/grovegrab/config.json`
- **Windows**: `%APPDATA%\grovegrab\config.json`

### Environment Variables

You can also set credentials via environment variables:

```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
export GROVEGRAB_OUTPUT="~/Music"
```

### Configuration Options

| Setting | Default | Options |
|---------|---------|---------|
| `audio_format` | `mp3` | `mp3`, `flac`, `ogg`, `opus`, `m4a` |
| `audio_quality` | `320k` | `128k`, `192k`, `256k`, `320k` |
| `default_download_path` | Platform-specific (see below) | Any valid path |

**Default Download Paths:**
- **Windows/Mac/Linux**: `~/Music/GroveGrab`
- **Android (Termux)**: `/storage/emulated/0/Music/GroveGrab`

### Changing Download Directory

#### Option 1: During Setup
```bash
grovegrab auth
# Enter your desired path when prompted
```

#### Option 2: Edit Config File
```bash
# Windows
notepad %APPDATA%\grovegrab\config.json

# Mac/Linux
nano ~/.config/grovegrab/config.json

# Android (Termux)
nano ~/.config/grovegrab/config.json
```

Change the `default_download_path` value:
```json
{
  "default_download_path": "/storage/emulated/0/Music/MyFolder"
}
```

#### Option 3: Per Download
```bash
grovegrab dl "url" --output /path/to/folder
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/grovegrab-cli.git
cd grovegrab-cli

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black grovegrab/

# Lint code
flake8 grovegrab/
```

### Project Structure

```
grovegrab-cli/
├── grovegrab/
│   ├── __init__.py      # Package info
│   ├── __main__.py      # Entry point
│   ├── cli.py           # CLI commands
│   ├── core.py          # Download manager
│   ├── config.py        # Configuration
│   └── ui.py            # Terminal UI
├── tests/               # Unit tests
├── docs/                # Documentation
├── requirements.txt     # Dependencies
├── setup.py             # Setup script
└── pyproject.toml       # Project metadata
```

## 🐛 Troubleshooting

### ❌ "No client_id. Pass it or set a SPOTIPY_CLIENT_ID environment variable"

**This is the most common issue!** You need to configure Spotify API credentials first:

```bash
# Run this command to set up your credentials:
grovegrab auth
```

Get free credentials from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) (see Quick Start section above).

### FFmpeg not found
```bash
# Install FFmpeg first
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

### No internet connection
```bash
# Check your network connection
ping google.com
```

### Download fails
```bash
# View detailed logs
grovegrab logs <task-id>

# Retry the download
grovegrab retry <task-id>
```

### Invalid credentials
```bash
# Re-run setup
grovegrab auth

# Or check your credentials at
# https://developer.spotify.com/dashboard
```

### Config location

Your configuration is stored at:
- **Windows**: `C:\Users\YourName\AppData\Local\grovegrab\grovegrab\config.json`
- **Linux/Mac**: `~/.config/grovegrab/config.json`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Notice

This tool is for personal use only. Please comply with:
- Spotify's Terms of Service
- YouTube's Terms of Service (SpotDL uses YouTube as audio source)
- Copyright laws in your jurisdiction

**Always support artists by using legitimate streaming services!**

## 🙏 Acknowledgments

- **[SpotDL](https://github.com/spotDL/spotify-downloader)** - The amazing tool that powers the downloads
- **[Typer](https://typer.tiangolo.com/)** - Beautiful CLI framework
- **[Rich](https://rich.readthedocs.io/)** - Gorgeous terminal formatting
- **GroveGrab Web** - The original web version this CLI is based on

## 📞 Support

- 🐛 [Report Bug](https://github.com/yourusername/grovegrab-cli/issues)
- 💡 [Request Feature](https://github.com/yourusername/grovegrab-cli/issues)
- 📖 [Documentation](https://github.com/yourusername/grovegrab-cli/wiki)

---

**Made with ❤️ for music lovers**

*If you enjoy this project, consider ⭐ starring the repository!*
