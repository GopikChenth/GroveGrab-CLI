# GroveGrab CLI - API Reference

Complete API documentation for all modules, classes, and functions.

## Table of Contents

- [CLI Module](#cli-module)
- [Core Module](#core-module)
- [Config Module](#config-module)
- [UI Module](#ui-module)

---

## CLI Module

**File:** `grovegrab/cli.py`

Main command-line interface using Typer framework.

### Commands

#### download

Download from a Spotify URL.

```python
def download(
    url: str,
    output: str = None,
    format: str = None,
    quality: str = None,
    watch: bool = False,
    detach: bool = False
)
```

**Parameters:**
- `url` (str, required): Spotify URL to download
- `output` (str, optional): Custom download directory
- `format` (str, optional): Audio format (mp3, flac, ogg, opus, m4a)
- `quality` (str, optional): Audio quality (128k, 192k, 256k, 320k)
- `watch` (bool, default=False): Watch progress in real-time
- `detach` (bool, default=False): Run in background

**Examples:**
```bash
grovegrab dl "https://open.spotify.com/track/..."
grovegrab dl "url" --format flac --quality 320k
grovegrab dl "url" --output ~/Music --watch
```

**Raises:**
- `typer.Exit(1)`: If credentials not configured or URL invalid

---

#### setup

Configure Spotify API credentials.

```python
def setup(interactive: bool = True)
```

**Parameters:**
- `interactive` (bool, default=True): Run interactive setup wizard

**Examples:**
```bash
grovegrab auth
grovegrab auth --no-interactive
```

**Notes:**
- Guides user through credential setup
- Saves configuration to platform-specific location
- Requires Spotify Developer account

---

#### config

Manage configuration settings.

```python
def config(show: bool = False, reset: bool = False)
```

**Parameters:**
- `show` (bool, default=False): Display current configuration
- `reset` (bool, default=False): Reset all settings to defaults

**Examples:**
```bash
grovegrab config --show
grovegrab config --reset
```

**Notes:**
- Reset requires user confirmation
- Shows sanitized credentials (client secret hidden)

---

#### list

List download tasks.

```python
def list(all: bool = False)
```

**Parameters:**
- `all` (bool, default=False): Show all tasks including completed

**Examples:**
```bash
grovegrab list
grovegrab list --all
```

**Output:**
Displays table with:
- Task ID (first 8 characters)
- Status (running, completed, failed, cancelled)
- Type (track, playlist, album, artist)
- Progress percentage
- URL

---

#### cancel

Cancel a running download task.

```python
def cancel(task_id: str)
```

**Parameters:**
- `task_id` (str, required): Task ID or partial ID (first 8+ chars)

**Examples:**
```bash
grovegrab cancel a1b2c3d4
grovegrab cancel a1b2c3d4-5678-90ab-cdef-1234567890ab
```

**Raises:**
- `typer.Exit(1)`: If task not found, ambiguous ID, or not running

**Notes:**
- Supports partial task ID matching
- Shows error if multiple tasks match partial ID

---

#### retry

Retry a failed download task.

```python
def retry(task_id: str)
```

**Parameters:**
- `task_id` (str, required): Task ID or partial ID

**Examples:**
```bash
grovegrab retry a1b2c3d4
```

**Raises:**
- `typer.Exit(1)`: If task not found or not in failed state

---

#### logs

View logs for a download task.

```python
def logs(task_id: str, follow: bool = False)
```

**Parameters:**
- `task_id` (str, required): Task ID or partial ID
- `follow` (bool, default=False): Follow log output (like tail -f)

**Examples:**
```bash
grovegrab logs a1b2c3d4
grovegrab logs a1b2c3d4 --follow
```

**Notes:**
- Follow mode updates in real-time
- Press Ctrl+C to stop following

---

#### batch

Download multiple URLs from a file.

```python
def batch(file: Path, workers: int = 3)
```

**Parameters:**
- `file` (Path, required): File containing URLs (one per line)
- `workers` (int, default=3): Number of concurrent downloads

**Examples:**
```bash
grovegrab batch urls.txt
grovegrab batch urls.txt --workers 5
```

**File Format:**
```
https://open.spotify.com/track/...
https://open.spotify.com/playlist/...
https://open.spotify.com/album/...
```

**Raises:**
- `typer.Exit(1)`: If file not found or empty

---

#### version

Show version information.

```python
def version()
```

**Examples:**
```bash
grovegrab version
```

**Output:**
```
GroveGrab CLI v1.0.0
Built for music lovers
```

---

## Core Module

**File:** `grovegrab/core.py`

Download manager and SpotDL integration.

### DownloadManager Class

Main class for managing downloads.

```python
class DownloadManager:
    def __init__(self):
        """Initialize download manager with platform-specific paths."""
```

#### Methods

##### validate_url

Validate a Spotify URL.

```python
def validate_url(self, url: str) -> dict:
    """
    Validate and parse Spotify URL.
    
    Args:
        url: Spotify URL to validate
        
    Returns:
        dict: {
            'valid': bool,
            'type': str,  # 'track', 'playlist', 'album', 'artist'
            'error': str  # Error message if invalid
        }
    """
```

**Examples:**
```python
manager = DownloadManager()
result = manager.validate_url("https://open.spotify.com/track/...")

if result['valid']:
    print(f"Valid {result['type']} URL")
else:
    print(f"Error: {result['error']}")
```

---

##### start_download

Start a download task.

```python
def start_download(
    self, 
    task_id: str, 
    url: str, 
    output_dir: str = None,
    format: str = None,
    quality: str = None
) -> bool:
    """
    Start downloading from Spotify URL.
    
    Args:
        task_id: Unique task identifier
        url: Spotify URL
        output_dir: Custom output directory (optional)
        format: Audio format (optional)
        quality: Audio quality (optional)
        
    Returns:
        bool: True if started successfully
    """
```

**Thread Safety:** Creates separate thread for each download

---

##### get_task_status

Get status of a download task.

```python
def get_task_status(self, task_id: str) -> dict:
    """
    Get current status of a task.
    
    Args:
        task_id: Task identifier
        
    Returns:
        dict: {
            'id': str,
            'status': str,  # 'running', 'completed', 'failed', 'cancelled'
            'progress': float,  # 0-100
            'type': str,
            'url': str,
            'error': str  # If failed
        }
    """
```

---

##### cancel_task

Cancel a running task.

```python
def cancel_task(self, task_id: str) -> bool:
    """
    Cancel a running download.
    
    Args:
        task_id: Task identifier
        
    Returns:
        bool: True if cancelled successfully
    """
```

---

##### retry_failed

Retry a failed task.

```python
def retry_failed(self, task_id: str) -> bool:
    """
    Retry a failed download.
    
    Args:
        task_id: Task identifier
        
    Returns:
        bool: True if restarted successfully
    """
```

---

##### get_all_tasks

Get all download tasks.

```python
def get_all_tasks(self) -> list[dict]:
    """
    Get list of all tasks.
    
    Returns:
        list: List of task dictionaries
    """
```

---

##### get_task_logs

Get logs for a task.

```python
def get_task_logs(self, task_id: str) -> str:
    """
    Get log output for a task.
    
    Args:
        task_id: Task identifier
        
    Returns:
        str: Log content
    """
```

---

## Config Module

**File:** `grovegrab/config.py`

Configuration management with platform-specific storage.

### ConfigManager Class

Manages application configuration.

```python
class ConfigManager:
    def __init__(self):
        """Initialize config manager with platform-specific paths."""
```

#### Methods

##### get_config

Get current configuration.

```python
def get_config(self) -> dict:
    """
    Get current configuration.
    
    Returns:
        dict: {
            'spotify': {
                'client_id': str,
                'client_secret': str
            },
            'download': {
                'output_dir': str,
                'format': str,
                'quality': str
            }
        }
    """
```

---

##### save_config

Save configuration to disk.

```python
def save_config(self, config: dict) -> None:
    """
    Save configuration.
    
    Args:
        config: Configuration dictionary
    """
```

---

##### has_credentials

Check if Spotify credentials are configured.

```python
def has_credentials(self) -> bool:
    """
    Check if Spotify API credentials are set.
    
    Returns:
        bool: True if credentials configured
    """
```

---

##### reset

Reset configuration to defaults.

```python
def reset(self) -> None:
    """Reset configuration to default values."""
```

---

##### get_config_path

Get configuration file path.

```python
def get_config_path(self) -> Path:
    """
    Get path to configuration file.
    
    Returns:
        Path: Platform-specific config file path
    """
```

**Platform Paths:**
- Windows: `C:\Users\<user>\AppData\Local\grovegrab\grovegrab\config.json`
- macOS: `~/Library/Application Support/grovegrab/config.json`
- Linux: `~/.config/grovegrab/config.json`

---

## UI Module

**File:** `grovegrab/ui.py`

Terminal user interface using Rich library.

### UIManager Class

Manages terminal UI components.

```python
class UIManager:
    def __init__(self, console: Console):
        """
        Initialize UI manager.
        
        Args:
            console: Rich Console instance
        """
```

#### Methods

##### run_setup_wizard

Run interactive setup wizard.

```python
def run_setup_wizard(self) -> None:
    """
    Run interactive setup wizard for configuration.
    
    Prompts for:
    - Spotify Client ID
    - Spotify Client Secret
    - Download directory
    - Audio format
    - Audio quality
    """
```

**Interactive:** Uses Rich prompts for user input

---

##### show_config

Display current configuration.

```python
def show_config(self) -> None:
    """
    Display current configuration in a formatted table.
    
    Shows:
    - Spotify credentials (sanitized)
    - Download settings
    - Config file location
    """
```

---

##### show_tasks_table

Display tasks in a table.

```python
def show_tasks_table(self, tasks: list[dict]) -> None:
    """
    Display tasks in formatted table.
    
    Args:
        tasks: List of task dictionaries
        
    Columns:
    - Task ID (first 8 chars)
    - Status
    - Type
    - Progress
    - URL (truncated)
    """
```

---

##### show_live_progress

Show live progress for a download.

```python
def show_live_progress(
    self, 
    task_id: str, 
    url: str, 
    output_dir: str = None
) -> None:
    """
    Display live progress for a download task.
    
    Args:
        task_id: Task identifier
        url: Spotify URL
        output_dir: Output directory (optional)
        
    Features:
    - Real-time progress bar
    - Status updates
    - ETA calculation
    """
```

---

##### show_simple_progress

Show simple progress (non-blocking).

```python
def show_simple_progress(
    self, 
    task_id: str, 
    url: str, 
    output_dir: str = None
) -> None:
    """
    Display simple progress and detach.
    
    Args:
        task_id: Task identifier
        url: Spotify URL
        output_dir: Output directory (optional)
    """
```

---

##### follow_logs

Follow logs in real-time.

```python
def follow_logs(self, task_id: str) -> None:
    """
    Follow task logs in real-time (like tail -f).
    
    Args:
        task_id: Task identifier
        
    Notes:
    - Updates every second
    - Press Ctrl+C to stop
    """
```

---

##### show_logs

Display task logs.

```python
def show_logs(self, task_id: str) -> None:
    """
    Display task logs.
    
    Args:
        task_id: Task identifier
    """
```

---

##### batch_download

Download multiple URLs with progress.

```python
def batch_download(self, urls: list[str], workers: int = 3) -> None:
    """
    Download multiple URLs with worker pool.
    
    Args:
        urls: List of Spotify URLs
        workers: Number of concurrent downloads
        
    Features:
    - Concurrent downloads
    - Overall progress tracking
    - Success/failure summary
    """
```

---

## Data Structures

### Task Dictionary

```python
{
    'id': str,              # UUID
    'status': str,          # 'running', 'completed', 'failed', 'cancelled'
    'progress': float,      # 0-100
    'type': str,            # 'track', 'playlist', 'album', 'artist'
    'url': str,             # Spotify URL
    'output_dir': str,      # Download directory
    'error': str,           # Error message (if failed)
    'created_at': str,      # ISO timestamp
    'updated_at': str       # ISO timestamp
}
```

### Config Dictionary

```python
{
    'spotify': {
        'client_id': str,
        'client_secret': str
    },
    'download': {
        'output_dir': str,      # Default: ~/Music/GroveGrab
        'format': str,          # Default: 'mp3'
        'quality': str          # Default: '320k'
    }
}
```

### Validation Result

```python
{
    'valid': bool,
    'type': str,            # 'track', 'playlist', 'album', 'artist', or None
    'error': str            # Error message if invalid
}
```

---

## Constants

### Audio Formats

```python
SUPPORTED_FORMATS = ['mp3', 'flac', 'ogg', 'opus', 'm4a']
```

### Audio Quality

```python
QUALITY_OPTIONS = ['128k', '192k', '256k', '320k']
```

### Task Status

```python
STATUS_RUNNING = 'running'
STATUS_COMPLETED = 'completed'
STATUS_FAILED = 'failed'
STATUS_CANCELLED = 'cancelled'
```

### Content Types

```python
TYPE_TRACK = 'track'
TYPE_PLAYLIST = 'playlist'
TYPE_ALBUM = 'album'
TYPE_ARTIST = 'artist'
```

---

## Error Handling

### Common Exceptions

#### Configuration Errors
```python
# Not configured
if not config_manager.has_credentials():
    raise typer.Exit(1)
```

#### Validation Errors
```python
result = manager.validate_url(url)
if not result['valid']:
    # Handle invalid URL
    raise typer.Exit(1)
```

#### Task Errors
```python
# Task not found
if not matching_tasks:
    raise typer.Exit(1)

# Ambiguous task ID
if len(matching_tasks) > 1:
    raise typer.Exit(1)
```

---

## Exit Codes

- `0`: Success
- `1`: General error (invalid input, not found, etc.)
- `130`: Interrupted by user (Ctrl+C)

---

## Threading Model

- **Main Thread:** CLI commands, UI rendering
- **Download Threads:** One thread per active download
- **Thread Safety:** Task dictionary protected with locks

---

## File System Layout

```
~/.config/grovegrab/          # or platform equivalent
├── config.json               # Configuration
└── tasks/                    # Task data
    ├── <task-id>.json        # Task metadata
    └── <task-id>.log         # Task logs

~/Music/GroveGrab/            # Default downloads
├── Track Name.mp3
├── Album Name/
│   ├── 01 - Song.mp3
│   └── 02 - Song.mp3
└── Playlist Name/
    └── ...
```

---

## Example Usage

### Complete Workflow

```python
from grovegrab.core import DownloadManager
from grovegrab.config import ConfigManager
from grovegrab.ui import UIManager
from rich.console import Console

# Initialize
config = ConfigManager()
manager = DownloadManager()
console = Console()
ui = UIManager(console)

# Configure (first time)
if not config.has_credentials():
    ui.run_setup_wizard()

# Validate URL
url = "https://open.spotify.com/track/..."
result = manager.validate_url(url)

if result['valid']:
    # Start download
    task_id = str(uuid.uuid4())
    manager.start_download(task_id, url)
    
    # Show progress
    ui.show_live_progress(task_id, url)
    
    # Check status
    status = manager.get_task_status(task_id)
    print(f"Status: {status['status']}")
```

---

## Performance Considerations

### Memory Usage
- ~100MB base memory
- ~20MB per active download
- Task history limited to 1000 entries

### Concurrency
- Default: 3 concurrent downloads in batch mode
- Maximum recommended: 10 concurrent downloads
- SpotDL handles rate limiting

### Storage
- Config file: <1KB
- Task metadata: ~500 bytes per task
- Logs: ~10KB per task

---

## Version History

### v1.0.0 (Current)
- Initial release
- 9 CLI commands
- SpotDL 3.9.6 integration
- Rich terminal UI
- Cross-platform support
- Batch download mode
- Task management
- Configuration system

---

## See Also

- [Getting Started Guide](../GETTING_STARTED.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [Developer Guide](DEVELOPER_GUIDE.md)
- [README](../README.md)
