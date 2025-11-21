# 🎵 GroveGrab Setup Guide

## Quick Fix: "No client_id" Error

If you see this error:
```
Failed to get playlist name: No client_id. Pass it or set a SPOTIPY_CLIENT_ID environment variable.
```

**You need to set up FREE Spotify API credentials first!** Takes 2 minutes:

### Step 1: Install GroveGrab
```bash
pip install GroveGrabCLI
```

### Step 2: Get Spotify API Credentials (FREE!)

1. Go to https://developer.spotify.com/dashboard
2. Log in with your Spotify account (free account works!)
3. Click **"Create an App"**
4. Enter any name (e.g., "My GroveGrab")
5. Enter any description
6. Click **"Create"**
7. You'll see your **Client ID** - copy it
8. Click **"Show Client Secret"** - copy it too
9. Click **"Edit Settings"**
10. Add Redirect URI: `http://localhost:8888/callback`
11. Click **"Save"**

### Step 3: Configure GroveGrab
```bash
grovegrab auth
```

Paste your Client ID and Client Secret when prompted.

### Step 4: Download!
```bash
grovegrab dl "https://open.spotify.com/track/..."
```

## That's it! 🎉

Your credentials are saved locally. You only need to do this once.

## Still Having Issues?

### Make sure FFmpeg is installed:
```bash
# Windows (with Chocolatey)
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

### Check your config:
```bash
grovegrab config --show
```

### View help:
```bash
grovegrab --help
grovegrab dl --help
```

## More Examples

```bash
# Download a playlist
grovegrab dl "https://open.spotify.com/playlist/..."

# Download an album
grovegrab dl "https://open.spotify.com/album/..."

# Custom output folder
grovegrab dl "url" --output ~/Music/MyFolder

# High quality FLAC
grovegrab dl "url" --format flac

# Watch progress
grovegrab dl "url" --watch
```

---

**Questions?** Check the README: https://github.com/GopikChenth/GroveGrab-CLI
