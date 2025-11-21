# GroveGrab CLI - Architecture Documentation

Technical architecture and design decisions.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Module Design](#module-design)
- [Data Flow](#data-flow)
- [Threading Model](#threading-model)
- [Storage Architecture](#storage-architecture)
- [Design Patterns](#design-patterns)
- [Technology Stack](#technology-stack)
- [Security Considerations](#security-considerations)

---

## Overview

GroveGrab CLI is a terminal-based application for downloading Spotify content. It follows a modular architecture with clear separation of concerns.

### Design Goals

1. **Simplicity:** Easy to use, minimal configuration
2. **Modularity:** Clean separation between CLI, core logic, and UI
3. **Extensibility:** Easy to add new features and commands
4. **Cross-Platform:** Works on Windows, macOS, and Linux
5. **Performance:** Efficient resource usage, concurrent downloads

### Architecture Style

- **Layered Architecture:** CLI → Core → External Services
- **Component-Based:** Independent modules with clear interfaces
- **Event-Driven:** Task status updates via polling

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                       │
│                    (Terminal + Rich UI)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Commands
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       CLI Layer (cli.py)                     │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐  │
│  │ download │  setup   │  config  │   list   │  cancel   │  │
│  └──────────┴──────────┴──────────┴──────────┴───────────┘  │
│  ┌──────────┬──────────┬──────────┬──────────┐              │
│  │  retry   │   logs   │  batch   │ version  │              │
│  └──────────┴──────────┴──────────┴──────────┘              │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌────────────────┐ ┌────────────┐ ┌────────────────┐
│   UI Manager   │ │   Config   │ │    Download    │
│   (ui.py)      │ │  Manager   │ │    Manager     │
│                │ │ (config.py)│ │   (core.py)    │
│ - Progress     │ │            │ │                │
│ - Tables       │ │ - Storage  │ │ - Validation   │
│ - Wizards      │ │ - Defaults │ │ - Tasks        │
│ - Logs         │ │ - Paths    │ │ - Threading    │
└────────────────┘ └────────────┘ └────┬───────────┘
                                        │
                                        ▼
                         ┌──────────────────────────┐
                         │   External Services       │
                         │  ┌──────────┬──────────┐ │
                         │  │ SpotDL   │ Spotify  │ │
                         │  │          │   API    │ │
                         │  └──────────┴──────────┘ │
                         └──────────────────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────┐
                         │     File System           │
                         │  - Downloads              │
                         │  - Config                 │
                         │  - Logs                   │
                         └──────────────────────────┘
```

---

## Module Design

### 1. CLI Module (`cli.py`)

**Purpose:** Command-line interface and argument parsing

**Responsibilities:**
- Define CLI commands
- Parse arguments and options
- Validate user input
- Coordinate between modules
- Handle errors and exit codes

**Dependencies:**
- Typer (CLI framework)
- Rich (console output)
- Core, Config, UI modules

**Design Pattern:** Command Pattern

```python
# Each command is independent
@app.command()
def download(...):
    # 1. Validate input
    # 2. Call core module
    # 3. Display UI
    # 4. Handle errors
```

---

### 2. Core Module (`core.py`)

**Purpose:** Business logic and download management

**Responsibilities:**
- URL validation
- Task lifecycle management
- SpotDL integration
- Progress tracking
- Thread management

**Dependencies:**
- SpotDL
- Platformdirs
- Threading

**Design Pattern:** Manager Pattern

```python
class DownloadManager:
    def __init__(self):
        self.tasks = {}       # In-memory task storage
        self.threads = {}     # Active download threads
        
    def start_download(self, ...):
        # 1. Create task
        # 2. Spawn thread
        # 3. Monitor progress
```

**Key Components:**

#### Task Manager
- Creates and tracks download tasks
- Maintains task state
- Provides task queries

#### Download Engine
- Builds SpotDL commands
- Executes downloads in threads
- Parses progress output

#### Progress Monitor
- Reads SpotDL output
- Updates task progress
- Detects completion/errors

---

### 3. Config Module (`config.py`)

**Purpose:** Configuration management

**Responsibilities:**
- Load/save configuration
- Validate settings
- Provide defaults
- Platform-specific paths

**Dependencies:**
- Platformdirs
- JSON

**Design Pattern:** Singleton Pattern

```python
class ConfigManager:
    def __init__(self):
        self.config_path = self._get_config_path()
        self.config = self._load_config()
        
    def get_config(self):
        return self.config
        
    def save_config(self, config):
        # Atomic write with backup
```

**Storage Format:**
```json
{
  "spotify": {
    "client_id": "...",
    "client_secret": "..."
  },
  "download": {
    "output_dir": "/path/to/music",
    "format": "mp3",
    "quality": "320k"
  }
}
```

---

### 4. UI Module (`ui.py`)

**Purpose:** Terminal user interface

**Responsibilities:**
- Display formatted output
- Show progress bars
- Run interactive wizards
- Render tables and panels

**Dependencies:**
- Rich (all components)
- Core module (for data)
- Config module (for settings)

**Design Pattern:** Presenter Pattern

```python
class UIManager:
    def __init__(self, console):
        self.console = console
        
    def show_live_progress(self, task_id, url):
        # 1. Create progress bar
        # 2. Poll task status
        # 3. Update display
        # 4. Handle completion
```

**UI Components:**

#### Setup Wizard
- Interactive prompts
- Input validation
- Help text
- Confirmation

#### Progress Display
- Real-time progress bars
- Status indicators
- ETA calculation
- Multi-task support

#### Tables
- Task listing
- Configuration display
- Formatted columns
- Color coding

---

## Data Flow

### Download Flow

```
User Command
     │
     ▼
CLI validates input
     │
     ▼
Check credentials ──────────> Config Manager
     │
     ▼
Validate URL ───────────────> Core Manager
     │
     ▼
Create task ────────────────> Task Storage
     │
     ▼
Spawn thread ───────────────> Download Thread
     │                              │
     │                              ▼
     │                         Build SpotDL command
     │                              │
     │                              ▼
     │                         Execute download
     │                              │
     │                              ▼
     │                         Parse progress ──────> Update task
     │                              │
     │                              ▼
     ▼                         Write to disk
UI polls task status
     │
     ▼
Display progress
     │
     ▼
Task completes
```

### Configuration Flow

```
User runs setup
     │
     ▼
UI shows wizard ────────────> Prompt for credentials
     │
     ▼
Validate input
     │
     ▼
Save to config ─────────────> Config Manager
     │
     ▼
Write to disk ──────────────> Platform-specific path
     │
     ▼
Confirm to user
```

---

## Threading Model

### Thread Architecture

```
Main Thread
├── CLI processing
├── UI rendering
└── Task polling

Download Thread 1
├── SpotDL execution
├── Progress parsing
└── File writing

Download Thread 2
├── SpotDL execution
├── Progress parsing
└── File writing

...
```

### Thread Safety

**Shared Resources:**
- `tasks` dictionary (protected by implicit GIL)
- Config file (atomic writes)
- Log files (buffered writes)

**Synchronization:**
```python
# Task dictionary updates are atomic in CPython
self.tasks[task_id] = {
    'status': 'running',
    'progress': progress
}

# File writes use atomic operations
with open(file, 'w') as f:
    json.dump(config, f)
```

**Thread Lifecycle:**
1. Main thread creates download thread
2. Download thread runs independently
3. Main thread polls task status
4. Download thread updates task state
5. Download thread exits on completion

---

## Storage Architecture

### Directory Structure

```
Platform Config Directory
├── config.json              # Application configuration
└── tasks/                   # Task storage
    ├── <uuid>.json          # Task metadata
    └── <uuid>.log           # Task logs

Download Directory
├── Track Name.mp3
├── Album Name/
│   ├── 01 - Song.mp3
│   └── 02 - Song.mp3
└── Playlist Name/
    └── ...
```

### Platform-Specific Paths

**Windows:**
```
Config: C:\Users\<user>\AppData\Local\grovegrab\grovegrab\
Downloads: C:\Users\<user>\Music\GroveGrab\
```

**macOS:**
```
Config: ~/Library/Application Support/grovegrab/
Downloads: ~/Music/GroveGrab/
```

**Linux:**
```
Config: ~/.config/grovegrab/
Downloads: ~/Music/GroveGrab/
```

### Data Persistence

**Configuration:**
- Format: JSON
- Updates: Atomic writes
- Backup: None (small file, easy to recreate)

**Task Metadata:**
- Format: JSON per task
- Updates: On status change
- Retention: Last 1000 tasks

**Logs:**
- Format: Plain text
- Updates: Appended in real-time
- Retention: With task metadata

---

## Design Patterns

### 1. Command Pattern (CLI)

Each CLI command is a separate function with clear responsibility.

```python
@app.command()
def download(...):
    # Single responsibility: handle download command
```

**Benefits:**
- Easy to add new commands
- Clear separation of concerns
- Testable in isolation

---

### 2. Manager Pattern (Core)

DownloadManager centralizes download operations.

```python
class DownloadManager:
    def start_download(self, ...): ...
    def cancel_task(self, ...): ...
    def get_task_status(self, ...): ...
```

**Benefits:**
- Single point of control
- Consistent task handling
- Easy to extend

---

### 3. Singleton Pattern (Config)

One ConfigManager instance manages all configuration.

```python
config_manager = ConfigManager()  # Created once
```

**Benefits:**
- Consistent state
- No redundant file reads
- Thread-safe access

---

### 4. Presenter Pattern (UI)

UIManager separates display logic from data.

```python
class UIManager:
    def show_tasks_table(self, tasks):
        # Presentation logic only
```

**Benefits:**
- Reusable UI components
- Easy to test
- Flexible display options

---

### 5. Facade Pattern (Integration)

Core module provides simple interface to SpotDL complexity.

```python
def start_download(self, task_id, url, ...):
    # Hides SpotDL command building
    # Hides progress parsing
    # Hides thread management
```

**Benefits:**
- Simple public API
- Complex implementation hidden
- Easy to swap implementations

---

## Technology Stack

### Core Libraries

**Typer**
- Purpose: CLI framework
- Why: Type-safe, auto-help, subcommands
- Version: 0.20.0

**Rich**
- Purpose: Terminal UI
- Why: Beautiful output, progress bars, tables
- Version: 14.2.0

**SpotDL**
- Purpose: Spotify downloading
- Why: Mature, feature-rich, well-maintained
- Version: 3.9.6

**Platformdirs**
- Purpose: Cross-platform paths
- Why: Standard, reliable, lightweight
- Version: 4.5.0

### Architecture Benefits

1. **Typer + Rich:** Perfect CLI/UI combination
2. **SpotDL:** Battle-tested download engine
3. **Platformdirs:** Cross-platform without complexity
4. **Pure Python:** No compiled dependencies

---

## Security Considerations

### Credential Storage

**Current:** Plain text JSON

**Rationale:**
- Spotify credentials are low-risk (read-only API)
- OS-level file permissions provide basic protection
- Matches web version approach

**Future:** Consider system keyring for sensitive data

### Input Validation

**URL Validation:**
```python
def validate_url(self, url):
    # Regex validation
    # Type checking
    # Error handling
```

**File Path Validation:**
```python
def sanitize_path(self, path):
    # Resolve absolute path
    # Check existence
    # Verify permissions
```

### Command Injection Prevention

**SpotDL Execution:**
```python
# Use list-based command (prevents shell injection)
cmd = ['spotdl', 'download', url]
subprocess.Popen(cmd, ...)  # Not shell=True
```

### Error Handling

**Principle:** Fail securely, log safely

```python
try:
    # Operation
except Exception as e:
    # Log error (sanitized)
    # Show user-friendly message
    # Exit gracefully
```

---

## Performance Characteristics

### Resource Usage

**Memory:**
- Base: ~100MB
- Per download: ~20MB
- Max recommended: 10 concurrent downloads

**CPU:**
- Minimal (mostly I/O bound)
- SpotDL handles transcoding

**Disk:**
- Config: <1KB
- Logs: ~10KB per task
- Downloads: Variable (music files)

### Scalability

**Current Limits:**
- Task history: 1000 tasks
- Concurrent downloads: Configurable (default: 3)
- No built-in rate limiting (SpotDL handles it)

**Bottlenecks:**
- Network bandwidth
- Spotify API rate limits
- Disk I/O

---

## Extension Points

### Adding New Commands

```python
@app.command()
def new_command(...):
    """New command implementation"""
    # 1. Parse arguments
    # 2. Call core module
    # 3. Display result
```

### Adding New Features

**Search Functionality:**
```python
# core.py
def search(self, query):
    # Use Spotipy for search
    # Return results
    
# cli.py
@app.command()
def search(query: str):
    results = manager.search(query)
    ui.show_results(results)
```

**Daemon Mode:**
```python
# core.py
def start_daemon(self):
    # Background service
    # Watch queue directory
    # Auto-download
```

---

## Testing Strategy

### Unit Tests

**Module:** Each module independently
**Mock:** External services (SpotDL, file system)
**Focus:** Business logic, validation

### Integration Tests

**Scope:** Module interactions
**Mock:** Only external services
**Focus:** Data flow, state management

### End-to-End Tests

**Scope:** Full command execution
**Mock:** Minimal (file system only)
**Focus:** User workflows

---

## Migration from Web Version

### Code Reuse

**Reused:**
- Download manager logic (80%)
- URL validation
- Progress parsing
- Error handling

**Replaced:**
- Flask → Typer
- React → Rich
- WebSocket → File-based polling
- Browser → Terminal

### Architecture Changes

| Aspect | Web Version | CLI Version |
|--------|-------------|-------------|
| **UI** | React components | Rich widgets |
| **API** | REST endpoints | Direct calls |
| **State** | Redux store | In-memory dict |
| **Updates** | WebSocket | Polling |
| **Distribution** | Electron | PyPI/Binary |

---

## Future Architecture

### Planned Enhancements

1. **Plugin System**
   - Load external downloaders
   - Custom output formats
   - Post-processing hooks

2. **Remote Management**
   - Web dashboard
   - REST API
   - Mobile app control

3. **Distributed Downloads**
   - Multiple machines
   - Load balancing
   - Shared queue

4. **Advanced Caching**
   - Metadata cache
   - Resume downloads
   - Deduplication

---

## Appendix

### Dependencies Graph

```
grovegrab
├── typer
│   └── click
├── rich
│   ├── markdown-it-py
│   └── pygments
├── spotdl
│   ├── spotipy
│   ├── ytmusicapi
│   ├── yt-dlp
│   ├── pytube
│   └── mutagen
└── platformdirs
```

### File Sizes

```
cli.py:     257 lines  ~8KB
core.py:    260 lines  ~9KB
config.py:   90 lines  ~3KB
ui.py:      260 lines  ~9KB
Total:      867 lines ~29KB
```

### Complexity Metrics

```
Cyclomatic Complexity: Low (2-5 per function)
Coupling: Loose (clear module boundaries)
Cohesion: High (single responsibility)
```

---

## See Also

- [API Reference](API_REFERENCE.md)
- [Developer Guide](DEVELOPER_GUIDE.md)
- [Getting Started](../GETTING_STARTED.md)
- [README](../README.md)
