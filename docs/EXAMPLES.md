# GroveGrab CLI - Usage Examples

Comprehensive examples for all features and use cases.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Download Examples](#download-examples)
- [Configuration](#configuration)
- [Task Management](#task-management)
- [Batch Operations](#batch-operations)
- [Advanced Usage](#advanced-usage)
- [Automation & Scripting](#automation--scripting)
- [Real-World Scenarios](#real-world-scenarios)

---

## Basic Usage

### First Time Setup

```bash
# Install GroveGrab CLI
pip install GroveGrabCLI

# Run setup wizard
grovegrab auth

# Follow prompts:
# 1. Enter Spotify Client ID
# 2. Enter Spotify Client Secret
# 3. Choose download directory (default: ~/Music/GroveGrab)
# 4. Select audio format (default: mp3)
# 5. Select audio quality (default: 320k)

# Verify setup
grovegrab config --show
```

### Getting Help

```bash
# General help
grovegrab --help

# Command-specific help
grovegrab dl --help
grovegrab batch --help
grovegrab config --help

# View version
grovegrab version
```

---

## Download Examples

### Single Track

```bash
# Basic track download
grovegrab dl "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"

# Watch progress in real-time
grovegrab dl "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp" --watch

# Custom output directory
grovegrab dl "https://open.spotify.com/track/..." --output "D:\My Music"

# High-quality FLAC
grovegrab dl "https://open.spotify.com/track/..." --format flac

# Lower quality for space saving
grovegrab dl "https://open.spotify.com/track/..." --quality 192k
```

### Playlist

```bash
# Download entire playlist
grovegrab dl "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"

# Watch progress
grovegrab dl "https://open.spotify.com/playlist/..." --watch

# Custom format and quality
grovegrab dl "https://open.spotify.com/playlist/..." \
  --format ogg \
  --quality 256k
```

### Album

```bash
# Download album
grovegrab dl "https://open.spotify.com/album/2ODvWsOgouMbaA5xf0RkJe"

# Watch progress
grovegrab dl "https://open.spotify.com/album/..." --watch

# Lossless FLAC
grovegrab dl "https://open.spotify.com/album/..." --format flac
```

### Artist (All Tracks)

```bash
# Download all artist tracks
grovegrab dl "https://open.spotify.com/artist/0TnOYISbd1XYRBk9myaseg"

# Warning: Can be very large!
# Watch progress recommended
grovegrab dl "https://open.spotify.com/artist/..." --watch
```

### Format Options

```bash
# MP3 (default, widely compatible)
grovegrab dl "url" --format mp3

# FLAC (lossless, large files)
grovegrab dl "url" --format flac

# OGG (good quality, smaller than FLAC)
grovegrab dl "url" --format ogg

# Opus (best compression, modern)
grovegrab dl "url" --format opus

# M4A (Apple ecosystem)
grovegrab dl "url" --format m4a
```

### Quality Options

```bash
# 128k - Good for mobile/streaming (~4MB per track)
grovegrab dl "url" --quality 128k

# 192k - Better quality (~6MB per track)
grovegrab dl "url" --quality 192k

# 256k - Great quality (~8MB per track)
grovegrab dl "url" --quality 256k

# 320k - Best MP3 quality (~10MB per track)
grovegrab dl "url" --quality 320k
```

---

## Configuration

### View Configuration

```bash
# Show all settings
grovegrab config --show

# Output example:
# +-------------+----------------------------------------+
# | Setting     | Value                                  |
# +-------------+----------------------------------------+
# | Client ID   | abc123...                              |
# | Secret      | ***                                    |
# | Output Dir  | C:\Users\User\Music\GroveGrab          |
# | Format      | mp3                                    |
# | Quality     | 320k                                   |
# +-------------+----------------------------------------+
```

### Reconfigure

```bash
# Run setup wizard again
grovegrab auth

# This allows you to:
# - Update Spotify credentials
# - Change download directory
# - Update default format
# - Update default quality
```

### Reset Configuration

```bash
# Reset to defaults (prompts for confirmation)
grovegrab config --reset

# You'll need to run setup again after reset
grovegrab auth
```

### Configuration File Location

**Windows:**
```
C:\Users\<username>\AppData\Local\grovegrab\grovegrab\config.json
```

**macOS:**
```
~/Library/Application Support/grovegrab/config.json
```

**Linux:**
```
~/.config/grovegrab/config.json
```

---

## Task Management

### List Active Downloads

```bash
# Show only running tasks
grovegrab list

# Output:
# +----------+----------+----------+----------+---------------------------+
# | Task ID  | Status   | Type     | Progress | URL                       |
# +----------+----------+----------+----------+---------------------------+
# | a1b2c3d4 | running  | playlist | 45%      | https://open.spotify.com/…|
# +----------+----------+----------+----------+---------------------------+
```

### List All Tasks

```bash
# Include completed and failed tasks
grovegrab list --all

# Shows full history with statuses:
# - running
# - completed
# - failed
# - cancelled
```

### Cancel Download

```bash
# Cancel by full task ID
grovegrab cancel a1b2c3d4-5678-90ab-cdef-1234567890ab

# Cancel by partial task ID (first 8 characters)
grovegrab cancel a1b2c3d4

# Confirms cancellation
# OK: Task a1b2c3d4 cancelled
```

### Retry Failed Download

```bash
# Retry a failed task
grovegrab retry a1b2c3d4

# Use case: Network issues, API errors
# Restarts the download from beginning
```

### View Task Logs

```bash
# View logs for a task
grovegrab logs a1b2c3d4

# Follow logs in real-time (like tail -f)
grovegrab logs a1b2c3d4 --follow

# Press Ctrl+C to stop following
```

---

## Batch Operations

### Basic Batch Download

**Create URLs file:**
```bash
# urls.txt
https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp
https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b
https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
https://open.spotify.com/album/2ODvWsOgouMbaA5xf0RkJe
```

**Download:**
```bash
# Process URLs with default 3 concurrent downloads
grovegrab batch urls.txt

# Custom number of workers
grovegrab batch urls.txt --workers 5

# More workers = faster but more CPU/network usage
# Recommended: 3-5 workers
```

### Advanced Batch Examples

**Mixed content types:**
```bash
# urls.txt can contain any mix of:
# - Tracks
# - Playlists
# - Albums
# - Artists

grovegrab batch urls.txt --workers 3
```

**Large batch operations:**
```bash
# For 100+ URLs, use more workers
grovegrab batch large_collection.txt --workers 10

# Monitor progress
# Shows overall completion and success/failure counts
```

**Incremental batch download:**
```bash
# Download first batch
grovegrab batch batch1.txt

# Add more URLs later
grovegrab batch batch2.txt

# No duplicates - GroveGrab tracks what's downloaded
```

---

## Advanced Usage

### Custom Download Directory Per Download

```bash
# Organize by genre
grovegrab dl "rock_playlist_url" --output "D:\Music\Rock"
grovegrab dl "jazz_playlist_url" --output "D:\Music\Jazz"

# Organize by year
grovegrab dl "2023_hits_url" --output "D:\Music\2023"

# Temporary storage
grovegrab dl "url" --output "C:\Temp\Downloads"
```

### Quality vs Format Combinations

```bash
# Best quality lossless
grovegrab dl "url" --format flac
# Result: ~30MB per track, perfect quality

# High quality MP3
grovegrab dl "url" --format mp3 --quality 320k
# Result: ~10MB per track, excellent quality

# Balanced quality/size
grovegrab dl "url" --format ogg --quality 256k
# Result: ~6MB per track, great quality

# Maximum compression
grovegrab dl "url" --format opus --quality 128k
# Result: ~3MB per track, good quality
```

### Background Downloads

```bash
# Start download and detach
grovegrab dl "url" --detach

# Check status later
grovegrab list

# View progress
grovegrab logs <task_id>
```

### Partial Task ID Usage

```bash
# Full task ID (UUID)
a1b2c3d4-5678-90ab-cdef-1234567890ab

# You can use just the first 8 characters
a1b2c3d4

# Works for all task commands
grovegrab cancel a1b2c3d4
grovegrab retry a1b2c3d4
grovegrab logs a1b2c3d4
```

---

## Automation & Scripting

### Windows PowerShell Scripts

**Daily playlist download:**
```powershell
# daily-download.ps1

$playlist = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
$output = "D:\Music\Daily"
$date = Get-Date -Format "yyyy-MM-dd"
$folder = "$output\$date"

New-Item -ItemType Directory -Path $folder -Force
grovegrab dl $playlist --output $folder --watch
```

**Batch download from list:**
```powershell
# batch-download.ps1

param(
    [string]$UrlsFile = "urls.txt",
    [int]$Workers = 5
)

if (Test-Path $UrlsFile) {
    grovegrab batch $UrlsFile --workers $Workers
    Write-Host "Download completed!"
} else {
    Write-Error "URLs file not found: $UrlsFile"
}
```

**Run script:**
```powershell
.\daily-download.ps1
.\batch-download.ps1 -UrlsFile "my-playlists.txt" -Workers 3
```

### Linux/macOS Shell Scripts

**Automated backup:**
```bash
#!/bin/bash
# backup-playlists.sh

PLAYLISTS=(
    "https://open.spotify.com/playlist/..."
    "https://open.spotify.com/playlist/..."
    "https://open.spotify.com/playlist/..."
)

OUTPUT_DIR="$HOME/Music/Backups/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

for playlist in "${PLAYLISTS[@]}"; do
    echo "Downloading: $playlist"
    grovegrab dl "$playlist" --output "$OUTPUT_DIR"
done

echo "Backup complete: $OUTPUT_DIR"
```

**Scheduled download (cron):**
```bash
# Edit crontab
crontab -e

# Add line (daily at 2 AM)
0 2 * * * /usr/local/bin/grovegrab dl "playlist_url" --output ~/Music/Daily

# Weekly backup (Sunday at 3 AM)
0 3 * * 0 /home/user/scripts/backup-playlists.sh
```

### Python Integration

```python
#!/usr/bin/env python3
# download_script.py

import subprocess
import sys

def download_spotify(url, output_dir=None, format='mp3', quality='320k'):
    """Download from Spotify using GroveGrab CLI."""
    cmd = ['grovegrab', 'download', url, '--format', format, '--quality', quality]
    
    if output_dir:
        cmd.extend(['--output', output_dir])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Success: {url}")
        return True
    else:
        print(f"Failed: {url}")
        print(result.stderr)
        return False

if __name__ == '__main__':
    # Read URLs from file
    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    # Download all
    for url in urls:
        download_spotify(url, output_dir='~/Music/Auto')
```

---

## Real-World Scenarios

### Scenario 1: Music Library Migration

**Goal:** Migrate Spotify playlists to local library

```bash
# Step 1: Export playlist URLs from Spotify
# (Use Spotify web player, copy each playlist URL)

# Step 2: Create URLs file
cat > my-library.txt << EOF
https://open.spotify.com/playlist/favorites
https://open.spotify.com/playlist/workout
https://open.spotify.com/playlist/chill
https://open.spotify.com/playlist/party
EOF

# Step 3: Download all in high quality
grovegrab batch my-library.txt --workers 5

# Step 4: Verify downloads
grovegrab list --all

# Step 5: Check output directory
ls ~/Music/GroveGrab/
```

### Scenario 2: Offline Music Collection

**Goal:** Build offline collection for travel

```bash
# Download favorite albums in FLAC
grovegrab dl "album_url_1" --format flac --output ~/Music/Offline
grovegrab dl "album_url_2" --format flac --output ~/Music/Offline
grovegrab dl "album_url_3" --format flac --output ~/Music/Offline

# Or use batch mode
cat > offline-collection.txt << EOF
album_url_1
album_url_2
album_url_3
EOF

grovegrab batch offline-collection.txt --workers 3
```

### Scenario 3: DJ/Event Preparation

**Goal:** Download music for upcoming event

```bash
# Create event playlist on Spotify
# Copy playlist URL

# Download in high quality
grovegrab dl "event_playlist_url" \
  --format mp3 \
  --quality 320k \
  --output "D:\Events\2024-12-31-NYE" \
  --watch

# Verify all tracks downloaded
ls "D:\Events\2024-12-31-NYE"
```

### Scenario 4: Podcast Archive

**Goal:** Archive favorite podcasts

```bash
# Spotify podcast URLs work too
grovegrab dl "https://open.spotify.com/show/..." \
  --output ~/Podcasts/Archive \
  --format mp3 \
  --quality 128k

# Lower quality for podcasts (speech)
# Saves space without quality loss
```

### Scenario 5: Collaborative Playlist Backup

**Goal:** Backup collaborative playlists regularly

**Script: backup-collaborative.sh**
```bash
#!/bin/bash

PLAYLISTS=(
    "collaborative_playlist_1_url"
    "collaborative_playlist_2_url"
)

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="$HOME/Music/Backups/$DATE"

mkdir -p "$BACKUP_DIR"

for playlist in "${PLAYLISTS[@]}"; do
    grovegrab dl "$playlist" \
      --output "$BACKUP_DIR" \
      --format mp3 \
      --quality 320k
done

echo "Backup completed: $BACKUP_DIR"

# Optional: Create archive
cd "$HOME/Music/Backups"
tar -czf "${DATE}.tar.gz" "$DATE"
echo "Archive created: ${DATE}.tar.gz"
```

**Automate with cron:**
```bash
# Weekly backup (Sundays at 2 AM)
0 2 * * 0 /home/user/scripts/backup-collaborative.sh
```

### Scenario 6: Multi-Format Library

**Goal:** Maintain library in multiple formats

```bash
# High quality for home
grovegrab dl "playlist_url" \
  --format flac \
  --output ~/Music/HighQuality

# Mobile-friendly version
grovegrab dl "playlist_url" \
  --format mp3 \
  --quality 192k \
  --output ~/Music/Mobile

# Car system (space limited)
grovegrab dl "playlist_url" \
  --format mp3 \
  --quality 128k \
  --output ~/Music/Car
```

### Scenario 7: New Release Monitoring

**Goal:** Auto-download new releases from favorite artists

**Script: new-releases.py**
```python
#!/usr/bin/env python3

import subprocess
from datetime import datetime

# Artist URLs to monitor
ARTISTS = [
    "artist_1_url",
    "artist_2_url",
]

def download_artist(url):
    """Download all tracks from artist."""
    date = datetime.now().strftime('%Y-%m-%d')
    output = f"~/Music/NewReleases/{date}"
    
    cmd = [
        'grovegrab', 'download', url,
        '--output', output,
        '--format', 'mp3',
        '--quality', '320k'
    ]
    
    subprocess.run(cmd)

if __name__ == '__main__':
    for artist in ARTISTS:
        print(f"Checking: {artist}")
        download_artist(artist)
```

---

## Tips & Best Practices

### 1. Use Watch Mode for Long Downloads

```bash
# Always use --watch for playlists/albums
grovegrab dl "playlist_url" --watch

# See progress, ETA, and catch errors early
```

### 2. Organize with Output Directories

```bash
# Create organized structure
grovegrab dl "rock_url" --output ~/Music/Rock
grovegrab dl "jazz_url" --output ~/Music/Jazz
grovegrab dl "classical_url" --output ~/Music/Classical
```

### 3. Balance Quality and Storage

```bash
# For archival: FLAC
grovegrab dl "url" --format flac

# For daily listening: 320k MP3
grovegrab dl "url" --format mp3 --quality 320k

# For mobile: 192k MP3
grovegrab dl "url" --format mp3 --quality 192k
```

### 4. Use Batch Mode for Efficiency

```bash
# Instead of running 50 individual commands
# Create URLs file and run once
grovegrab batch urls.txt --workers 5
```

### 5. Monitor with List Command

```bash
# Check active downloads
grovegrab list

# Review history
grovegrab list --all

# View logs for issues
grovegrab logs <task_id>
```

---

## Error Recovery

### Handling Failed Downloads

```bash
# Check failed tasks
grovegrab list --all | grep failed

# Retry specific task
grovegrab retry <task_id>

# View error details
grovegrab logs <task_id>
```

### Network Issues

```bash
# Download with watch mode to catch issues early
grovegrab dl "url" --watch

# If network drops, retry
grovegrab retry <task_id>

# For unstable connections, download one at a time
grovegrab batch urls.txt --workers 1
```

### Invalid Credentials

```bash
# Reconfigure credentials
grovegrab auth

# Test with simple download
grovegrab dl "track_url"
```

---

## See Also

- [Getting Started Guide](../GETTING_STARTED.md)
- [API Reference](API_REFERENCE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [README](../README.md)
