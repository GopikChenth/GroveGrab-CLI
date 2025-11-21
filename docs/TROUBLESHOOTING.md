# GroveGrab CLI - Troubleshooting Guide

Solutions to common issues and error messages.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Problems](#configuration-problems)
- [Download Errors](#download-errors)
- [Performance Issues](#performance-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Error Messages](#error-messages)
- [Debug Mode](#debug-mode)
- [Getting Help](#getting-help)

---

## Installation Issues

### Issue: "pip: command not found"

**Cause:** Python pip not installed or not in PATH

**Solution:**
```bash
# Windows
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# macOS
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

# Linux (Debian/Ubuntu)
sudo apt-get install python3-pip

# Linux (Fedora)
sudo dnf install python3-pip
```

### Issue: "Module not found" after installation

**Cause:** Package not properly installed or wrong Python environment

**Solution:**
```bash
# Verify Python version
python --version  # Should be 3.8+

# Reinstall package
pip uninstall GroveGrabCLI
pip install GroveGrabCLI

# Or install in development mode
cd GroveGrab-CLI
pip install -e .

# Verify installation
grovegrab version
```

### Issue: "Permission denied" during installation

**Cause:** Insufficient permissions

**Solution:**
```bash
# Use --user flag
pip install --user GroveGrabCLI

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install GroveGrabCLI
```

### Issue: Python version incompatibility

**Cause:** Python version too old or too new

**Solution:**
```bash
# Check Python version
python --version

# Requirement: Python 3.8+
# If you have Python 3.14, SpotDL 3.9.x will be used
# If you have Python 3.13 or lower, SpotDL 4.x can be used

# Install specific Python version
# - Use pyenv (macOS/Linux)
# - Download from python.org (Windows)
# - Use conda environments

# Create environment with specific version
conda create -n grovegrab python=3.11
conda activate grovegrab
pip install GroveGrabCLI
```

---

## Configuration Problems

### Issue: "No Spotify credentials configured"

**Cause:** Spotify API credentials not set up

**Solution:**
```bash
# Run setup wizard
grovegrab auth

# You'll need:
# 1. Spotify Client ID
# 2. Spotify Client Secret

# Get credentials:
# 1. Go to https://developer.spotify.com/dashboard
# 2. Log in with Spotify account
# 3. Create new app
# 4. Copy Client ID and Client Secret
# 5. Enter in setup wizard
```

### Issue: "Invalid credentials"

**Cause:** Wrong Client ID or Secret

**Solution:**
```bash
# Verify credentials at Spotify Dashboard
# https://developer.spotify.com/dashboard

# Run setup again with correct credentials
grovegrab auth

# Test with simple download
grovegrab dl "https://open.spotify.com/track/..."
```

### Issue: Config file corrupted

**Cause:** Manual edit or disk error

**Solution:**
```bash
# Reset configuration
grovegrab config --reset

# Run setup again
grovegrab auth

# Or manually delete config file
# Windows: C:\Users\<user>\AppData\Local\grovegrab\grovegrab\config.json
# macOS: ~/Library/Application Support/grovegrab/config.json
# Linux: ~/.config/grovegrab/config.json
```

### Issue: Can't find config file

**Cause:** Permission issue or incorrect path

**Solution:**
```bash
# Check config location
grovegrab config --show

# Verify directory exists and has permissions
# Windows:
dir "C:\Users\%USERNAME%\AppData\Local\grovegrab\grovegrab"

# macOS/Linux:
ls -la ~/Library/Application\ Support/grovegrab  # macOS
ls -la ~/.config/grovegrab                        # Linux

# Create directory if missing
mkdir -p <config-directory>

# Run setup
grovegrab auth
```

---

## Download Errors

### Issue: "Invalid URL"

**Cause:** Malformed or unsupported Spotify URL

**Solution:**
```bash
# Ensure URL is from Spotify
# Valid patterns:
https://open.spotify.com/track/...
https://open.spotify.com/playlist/...
https://open.spotify.com/album/...
https://open.spotify.com/artist/...

# Copy URL from Spotify app:
# Right-click → Share → Copy Link

# Don't use:
# - Spotify URIs (spotify:track:...)
# - Short URLs (spotify.link/...)
# - Non-Spotify URLs
```

### Issue: "Download failed" or stalls

**Cause:** Network issues, API rate limits, or invalid content

**Solution:**
```bash
# Check network connection
ping open.spotify.com

# View error details
grovegrab logs <task_id>

# Retry download
grovegrab retry <task_id>

# Try with single worker
grovegrab batch urls.txt --workers 1

# Wait a few minutes if rate limited
# Spotify API has rate limits
```

### Issue: "Track not found" or "Content unavailable"

**Cause:** Content not available in your region or removed from Spotify

**Solution:**
```bash
# Verify URL in Spotify app or web player
# Check if track/album is available in your region

# Some content is region-locked
# Some content may be removed by artists

# No workaround for unavailable content
```

### Issue: Incomplete downloads

**Cause:** Network interruption or disk space

**Solution:**
```bash
# Check disk space
# Windows: dir
# macOS/Linux: df -h

# Retry failed task
grovegrab retry <task_id>

# Monitor with watch mode
grovegrab dl "url" --watch

# For unstable connections, reduce workers
grovegrab batch urls.txt --workers 1
```

### Issue: Wrong metadata or file names

**Cause:** SpotDL metadata issue

**Solution:**
```bash
# SpotDL tries to match with YouTube
# Sometimes metadata may be incorrect

# Check SpotDL version
pip show spotdl

# Update SpotDL
pip install --upgrade spotdl

# Report to SpotDL project:
# https://github.com/spotDL/spotify-downloader/issues
```

---

## Performance Issues

### Issue: Downloads are slow

**Cause:** Network speed, single worker, or API rate limits

**Solution:**
```bash
# Use more workers for batch downloads
grovegrab batch urls.txt --workers 5

# Check network speed
# Spotify downloads from YouTube
# Speed depends on YouTube servers

# Try different time of day
# Network may be congested during peak hours
```

### Issue: High CPU usage

**Cause:** Audio transcoding

**Solution:**
```bash
# Use native format (mp3) to reduce transcoding
grovegrab dl "url" --format mp3

# Reduce concurrent downloads
grovegrab batch urls.txt --workers 2

# Close other applications
```

### Issue: High memory usage

**Cause:** Too many concurrent downloads

**Solution:**
```bash
# Reduce workers
grovegrab batch urls.txt --workers 2

# Download sequentially
grovegrab batch urls.txt --workers 1

# Restart if memory leaks suspected
```

### Issue: Disk space running out

**Cause:** Large downloads, insufficient space

**Solution:**
```bash
# Check disk space
# Windows: dir
# macOS/Linux: df -h

# Use lower quality
grovegrab dl "url" --quality 192k

# Use compressed format
grovegrab dl "url" --format opus --quality 128k

# Change output directory to larger drive
grovegrab dl "url" --output "/path/to/larger/drive"
```

---

## Platform-Specific Issues

### Windows Issues

#### Issue: PowerShell execution policy

**Error:** "script execution is disabled on this system"

**Solution:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set to allow scripts (run as Administrator)
Set-ExecutionPolicy RemoteSigned

# Or bypass for single command
powershell -ExecutionPolicy Bypass -Command "grovegrab dl 'url'"
```

#### Issue: Long path names

**Error:** "The filename or extension is too long"

**Solution:**
```bash
# Enable long paths in Windows 10+
# Run as Administrator:
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f

# Or use shorter output path
grovegrab dl "url" --output "C:\Music"

# Or edit registry manually:
# Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
# Set LongPathsEnabled to 1
```

#### Issue: Antivirus blocking

**Cause:** Some antivirus software flags Python executables

**Solution:**
```bash
# Add exception for Python and grovegrab
# Windows Defender:
# Settings → Update & Security → Windows Security → Virus & threat protection
# → Manage settings → Exclusions → Add exclusion

# Add these paths:
# C:\Users\<user>\AppData\Local\Programs\Python\
# C:\Users\<user>\AppData\Local\grovegrab\
```

### macOS Issues

#### Issue: "grovegrab: command not found"

**Cause:** pip installs to user bin not in PATH

**Solution:**
```bash
# Check where grovegrab is installed
pip show -f grovegrab | grep Location

# Add to PATH in ~/.zshrc or ~/.bash_profile
echo 'export PATH="$HOME/Library/Python/3.x/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Or use full path
~/Library/Python/3.x/bin/grovegrab dl "url"
```

#### Issue: Certificate verification errors

**Cause:** SSL certificate issue

**Solution:**
```bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command

# Or update certifi
pip install --upgrade certifi

# Or temporarily bypass (not recommended)
export SSL_CERT_FILE=""
```

#### Issue: Permission denied on system Python

**Cause:** macOS System Integrity Protection

**Solution:**
```bash
# Use Homebrew Python (recommended)
brew install python3
pip3 install GroveGrabCLI

# Or use virtual environment
python3 -m venv ~/venv
source ~/venv/bin/activate
pip install GroveGrabCLI
```

### Linux Issues

#### Issue: "command not found"

**Cause:** Not installed or not in PATH

**Solution:**
```bash
# Check installation
pip show grovegrab

# Add user bin to PATH (~/.bashrc or ~/.zshrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or use full path
~/.local/bin/grovegrab dl "url"
```

#### Issue: Missing dependencies

**Cause:** System dependencies not installed

**Solution:**
```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install python3 python3-pip ffmpeg

# Fedora
sudo dnf install python3 python3-pip ffmpeg

# Arch
sudo pacman -S python python-pip ffmpeg

# Install grovegrab
pip3 install GroveGrabCLI
```

#### Issue: Permission issues

**Cause:** Incorrect file permissions

**Solution:**
```bash
# Fix permissions on config directory
chmod -R 755 ~/.config/grovegrab

# Fix permissions on downloads
chmod -R 755 ~/Music/GroveGrab

# Run without sudo (use --user flag)
pip install --user GroveGrabCLI
```

---

## Error Messages

### "Error: No Spotify credentials configured"

**Solution:**
```bash
grovegrab auth
```

### "Error: Invalid URL"

**Solution:**
```bash
# Use valid Spotify URL
grovegrab dl "https://open.spotify.com/track/..."
```

### "Error: Task not found"

**Solution:**
```bash
# List all tasks to find correct ID
grovegrab list --all

# Use correct task ID
grovegrab logs <correct_task_id>
```

### "Warning: Multiple tasks match"

**Solution:**
```bash
# Use more characters from task ID
# Instead of: grovegrab cancel a1
# Use: grovegrab cancel a1b2c3d4
```

### "Error: File not found"

**Solution:**
```bash
# For batch command, verify file exists
ls urls.txt

# Use correct path
grovegrab batch /full/path/to/urls.txt
```

### "Error: Permission denied"

**Solution:**
```bash
# Check directory permissions
ls -la ~/Music/GroveGrab

# Fix permissions
chmod 755 ~/Music/GroveGrab

# Or use different output directory
grovegrab dl "url" --output ~/Downloads
```

### SpotDL errors

**"ERROR: Unable to extract video data"**

**Solution:**
```bash
# YouTube-DL/yt-dlp issue
# Update SpotDL and dependencies
pip install --upgrade spotdl yt-dlp

# Try again
grovegrab retry <task_id>
```

**"ERROR: HTTP Error 429: Too Many Requests"**

**Solution:**
```bash
# Rate limited by YouTube
# Wait 10-15 minutes
# Reduce concurrent downloads
grovegrab batch urls.txt --workers 1
```

---

## Debug Mode

### Enable Verbose Logging

```bash
# Set environment variable
# Windows:
set GROVEGRAB_DEBUG=1
grovegrab dl "url"

# macOS/Linux:
export GROVEGRAB_DEBUG=1
grovegrab dl "url"
```

### Check Log Files

```bash
# View task logs
grovegrab logs <task_id>

# Follow logs in real-time
grovegrab logs <task_id> --follow

# Log file location:
# Windows: C:\Users\<user>\AppData\Local\grovegrab\grovegrab\tasks\<task_id>.log
# macOS: ~/Library/Application Support/grovegrab/tasks/<task_id>.log
# Linux: ~/.config/grovegrab/tasks/<task_id>.log
```

### Diagnostic Commands

```bash
# Check version
grovegrab version

# View configuration
grovegrab config --show

# List all tasks
grovegrab list --all

# Check Python version
python --version

# Check installed packages
pip list | grep -E "grovegrab|spotdl|typer|rich"

# Check SpotDL directly
spotdl --version
```

---

## Getting Help

### Before Asking for Help

1. **Check this guide** for your issue
2. **View task logs:** `grovegrab logs <task_id>`
3. **Check configuration:** `grovegrab config --show`
4. **Verify setup:** `grovegrab version`
5. **Try fresh setup:** `grovegrab config --reset && grovegrab auth`

### Gather Information

When reporting issues, include:

```bash
# System information
# Operating System and version
# Python version
python --version

# GroveGrab version
grovegrab version

# SpotDL version
pip show spotdl

# Error message
grovegrab logs <task_id>

# Command used
# (What you typed)

# Expected vs actual behavior
```

### Where to Get Help

1. **Documentation**
   - [README](../README.md)
   - [Getting Started](../GETTING_STARTED.md)
   - [Examples](EXAMPLES.md)
   - [API Reference](API_REFERENCE.md)

2. **GitHub Issues**
   - Search existing issues
   - Create new issue with details
   - Include diagnostic information

3. **SpotDL Issues**
   - For download engine problems
   - https://github.com/spotDL/spotify-downloader/issues

4. **Community**
   - GitHub Discussions
   - Stack Overflow (tag: grovegrab, spotdl)

### Creating Good Bug Reports

**Template:**

```markdown
## Environment
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- Python: 3.11.5
- GroveGrab: 1.0.0
- SpotDL: 3.9.6

## Description
Brief description of the issue

## Steps to Reproduce
1. Run `grovegrab auth`
2. Run `grovegrab dl "url"`
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happened

## Error Message
```
Paste error message or log output here
```

## Additional Context
Any other relevant information
```

---

## Common Solutions Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Command not found | `pip install GroveGrabCLI` or add to PATH |
| No credentials | `grovegrab auth` |
| Invalid URL | Use Spotify share link |
| Download failed | `grovegrab retry <task_id>` |
| Slow downloads | `grovegrab batch urls.txt --workers 5` |
| Out of space | Use `--quality 192k` or `--format opus` |
| Permission denied | `chmod 755 <directory>` |
| Rate limited | Wait 10 minutes, reduce workers |
| Config corrupted | `grovegrab config --reset` |
| Task not found | `grovegrab list --all` to find ID |

---

## Advanced Troubleshooting

### Clean Reinstall

```bash
# Uninstall completely
pip uninstall GroveGrabCLI spotdl

# Clear cache
pip cache purge

# Reinstall
pip install GroveGrabCLI

# Fresh setup
grovegrab config --reset
grovegrab auth
```

### Reset Everything

```bash
# Remove config
# Windows:
rmdir /s /q "%LOCALAPPDATA%\grovegrab"

# macOS:
rm -rf ~/Library/Application\ Support/grovegrab

# Linux:
rm -rf ~/.config/grovegrab

# Reinstall and setup
pip install --upgrade GroveGrabCLI
grovegrab auth
```

### Network Debugging

```bash
# Test Spotify API access
curl https://api.spotify.com/v1/

# Test YouTube access (SpotDL uses this)
curl https://www.youtube.com/

# Check DNS
nslookup open.spotify.com
nslookup youtube.com

# Test with VPN if issues persist
# Some ISPs may block or throttle
```

---

## Still Having Issues?

If you've tried everything and still have problems:

1. **Create a GitHub issue** with full diagnostic information
2. **Include logs** from failed tasks
3. **Describe your environment** in detail
4. **Provide reproduction steps**

We're here to help make GroveGrab work for you!

---

## See Also

- [Getting Started](../GETTING_STARTED.md)
- [Usage Examples](EXAMPLES.md)
- [API Reference](API_REFERENCE.md)
- [Developer Guide](DEVELOPER_GUIDE.md)
- [README](../README.md)
