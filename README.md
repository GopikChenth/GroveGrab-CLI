# 🎵 GroveGrab CLI

A lightweight, fast command-line tool to download Spotify music (tracks, playlists, albums, artists) with your own free Spotify API credentials.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/pypi-v1.0.6-blue.svg)](https://pypi.org/project/GroveGrabCLI/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📖 What is GroveGrab CLI?

GroveGrab CLI downloads Spotify music using **SpotDL** (fetches audio from YouTube) with your **free Spotify API credentials** for metadata. Perfect for offline listening, backups, or building your personal music library.

**Key Features:**
- ✅ Download tracks, playlists, albums, and entire artist discographies
- ✅ High-quality audio (MP3 320kbps, FLAC, OGG, OPUS, M4A)
- ✅ Beautiful real-time progress tracking with individual song status
- ✅ Cross-platform: Windows, macOS, Linux, Android (Termux)
- ✅ Batch downloads from file lists
- ✅ Task management: pause, resume, retry failed downloads

---

## 📦 Installation

### Prerequisites
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **FFmpeg** (required for audio conversion)

### Install FFmpeg First

<details>
<summary><b>Windows</b></summary>

```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```
</details>

<details>
<summary><b>macOS</b></summary>

```bash
brew install ffmpeg
```
</details>

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt update && sudo apt install ffmpeg
```
</details>

<details>
<summary><b>Android (Termux)</b></summary>

```bash
pkg install ffmpeg
```
</details>

### Install GroveGrab

```bash
pip install GroveGrabCLI
```

### Platform-Specific Setup

<details>
<summary><b>Android (Termux) - Extra Steps</b></summary>

1. **Install Termux from [F-Droid](https://f-droid.org/)** (NOT Play Store)

2. **Install dependencies:**
   ```bash
   pkg update && pkg upgrade
   pkg install python ffmpeg
   ```

3. **Enable storage access:**
   ```bash
   termux-setup-storage
   ```

4. **Install GroveGrab:**
   ```bash
   pip install GroveGrabCLI
   ```

5. **Configure paths** (when running `grovegrab auth`):
   - Internal: `/storage/emulated/0/Music/GroveGrab`
   - SD Card: `/storage/XXXX-XXXX/Music/GroveGrab` (check `ls /storage/`)
</details>

---

## 🚀 Quick Start (2 Minutes Setup)

### Step 1: Get FREE Spotify API Credentials

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in (free Spotify account works!)
3. Click **"Create an App"** → name it anything → **Create**
4. Copy your **Client ID** and **Client Secret** (click "Show")
5. Click **"Edit Settings"** → Add these Redirect URIs:
   - `http://localhost:8888/callback`
   - `http://127.0.0.1:8888/callback`
6. Click **Save**

### Step 2: Configure GroveGrab

```bash
grovegrab auth
```
Paste your credentials when prompted. Done! 🎉

### Step 3: Download Music

```bash
# Download a track
grovegrab dl "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"

# Download a playlist
grovegrab dl "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"

# Download with progress display
grovegrab dl "spotify_url" --watch
```

---

## 💻 Usage

### Basic Downloads

```bash
# Download track/playlist/album/artist
grovegrab dl "spotify_url"

# Watch real-time progress
grovegrab dl "url" --watch

# Custom output folder
grovegrab dl "url" --output ~/Music/MyFolder

# High-quality FLAC
grovegrab dl "url" --format flac
```

### Batch Downloads

Create a file `urls.txt`:
```
https://open.spotify.com/track/...
https://open.spotify.com/playlist/...
https://open.spotify.com/album/...
```

Then run:
```bash
grovegrab batch urls.txt
```

### Task Management

```bash
grovegrab list              # Show active downloads
grovegrab list --all        # Show all downloads
grovegrab cancel <task-id>  # Cancel download
grovegrab retry <task-id>   # Retry failed
grovegrab logs <task-id>    # View logs
```

### Configuration

```bash
grovegrab auth              # Setup/reconfigure
grovegrab config --show     # View settings
grovegrab version           # Show version
```

---

## 🎨 Example Output

**Playlist Download:**
```
Starting download: playlist
Overall: 15/31 tracks ████████████░░░░░░░░ 48%
Anirudh Ravichander - Pathala Pathala ─── 100%
The Weeknd - Blinding Lights ──────────── 100%
Drake - God's Plan ─────────────────────── 75%
```

**Task List:**
```
┌─ Download Tasks ─────────────────────────────────┐
│ ID       Status      Progress  Stats             │
├──────────────────────────────────────────────────┤
│ a1b2c3d4 running     67%       3/5               │
│ e5f6g7h8 completed   100%      10/10             │
└──────────────────────────────────────────────────┘
```

---

## ⚙️ Configuration

### Config File Locations
- **Windows**: `%APPDATA%\grovegrab\config.json`
- **Linux/Mac**: `~/.config/grovegrab/config.json`
- **Android**: `~/.config/grovegrab/config.json`

### Available Options

| Setting | Default | Options |
|---------|---------|---------|
| `audio_format` | `mp3` | `mp3`, `flac`, `ogg`, `opus`, `m4a` |
| `audio_quality` | `320k` | `128k`, `192k`, `256k`, `320k` |
| `download_path` | `~/Music/GroveGrab` | Any valid path |

### Change Settings

**Via setup wizard:**
```bash
grovegrab auth
```

**Via environment variables:**
```bash
export SPOTIFY_CLIENT_ID="your_id"
export SPOTIFY_CLIENT_SECRET="your_secret"
```

**Per download:**
```bash
grovegrab dl "url" --format flac --output ~/Music/Custom
```

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **Multi-format Support** | MP3 (320k), FLAC, OGG, OPUS, M4A |
| **Real-time Progress** | Individual track progress in playlists |
| **Task Management** | Cancel, retry, view logs for all downloads |
| **Batch Downloads** | Download multiple URLs from file |
| **Smart Organization** | Auto-organized by Artist/Album/Track |
| **Cross-Platform** | Windows, macOS, Linux, Android (Termux) |
| **Free & Open Source** | MIT License, no subscriptions |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"No client_id" error** | Run `grovegrab auth` to configure Spotify credentials ([Get them here](https://developer.spotify.com/dashboard)) |
| **FFmpeg not found** | Install FFmpeg: `choco install ffmpeg` (Win) / `brew install ffmpeg` (Mac) / `apt install ffmpeg` (Linux) |
| **Download fails** | Check logs: `grovegrab logs <task-id>`, then retry: `grovegrab retry <task-id>` |
| **Invalid credentials** | Reconfigure: `grovegrab auth`, verify at [Spotify Dashboard](https://developer.spotify.com/dashboard) |
| **Android storage issues** | Run `termux-setup-storage` and use `/storage/emulated/0/Music/GroveGrab` |

**Need more help?** [Open an issue](https://github.com/GopikChenth/GroveGrab-CLI/issues)

---

## 📄 License & Legal

**License:** MIT License - Free for personal use  
**Legal Notice:** This tool is for **personal use only**. Respect copyright laws and support artists through legitimate streaming services.

Uses [SpotDL](https://github.com/spotDL/spotify-downloader) (fetches audio from YouTube) with Spotify API for metadata.

---

## 🙏 Credits

Built with [SpotDL](https://github.com/spotDL/spotify-downloader) • [Typer](https://typer.tiangolo.com/) • [Rich](https://rich.readthedocs.io/)

---

## 📞 Support

- 🐛 [Report Issues](https://github.com/GopikChenth/GroveGrab-CLI/issues)
- ⭐ [Star on GitHub](https://github.com/GopikChenth/GroveGrab-CLI)
- 📦 [View on PyPI](https://pypi.org/project/GroveGrabCLI/)

---

## 📝 Changelog

### v1.0.6 (2025-11-29) - CRITICAL FIX
- ✅ Fixed SpotDL command structure for 3.9.6+ compatibility
- ✅ Fixed path template syntax (`{ext}` instead of `{output-ext}`)
- ✅ Downloads now work correctly

### v1.0.5 (2025-11-21)
- New ASCII banner with gradient colors
- First-run setup experience

### v1.0.4 (2025-11-21)
- Android/Termux installation guide
- Platform-specific tips

### v1.0.3 (2025-11-21)
- Android/Termux support with auto path detection

### v1.0.2 (2025-11-21)
- Improved error messages for missing credentials

---

**Made with ❤️ for music lovers**
