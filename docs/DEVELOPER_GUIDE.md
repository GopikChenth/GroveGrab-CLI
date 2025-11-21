# GroveGrab CLI - Developer Guide

Complete guide for contributing to and extending GroveGrab CLI.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Adding Features](#adding-features)
- [Testing](#testing)
- [Building & Distribution](#building--distribution)
- [Debugging](#debugging)
- [Contributing](#contributing)

---

## Getting Started

### Prerequisites

**Required:**
- Python 3.8 or higher
- Git
- pip

**Recommended:**
- Virtual environment tool (venv, virtualenv, conda)
- Code editor with Python support (VS Code, PyCharm)
- Basic understanding of CLI applications

### Quick Start

```bash
# Clone repository
git clone <repository-url>
cd GroveGrab-CLI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest black flake8 mypy

# Verify installation
grovegrab version
```

---

## Development Setup

### Environment Setup

#### 1. Virtual Environment

```bash
# Create
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Verify
which python  # Should point to venv
```

#### 2. Install Dependencies

```bash
# Runtime dependencies
pip install -e .

# Development dependencies
pip install -e ".[dev]"

# Or manually
pip install pytest black flake8 mypy
```

#### 3. Configure Editor

**VS Code (settings.json):**
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "editor.formatOnSave": true
}
```

**PyCharm:**
- Enable Black formatter
- Configure Flake8 linter
- Set line length to 88

---

## Project Structure

```
GroveGrab-CLI/
├── grovegrab/              # Main package
│   ├── __init__.py         # Package metadata
│   ├── __main__.py         # Entry point
│   ├── cli.py              # CLI commands
│   ├── core.py             # Business logic
│   ├── config.py           # Configuration
│   └── ui.py               # User interface
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_core.py
│   ├── test_config.py
│   └── test_ui.py
├── docs/                   # Documentation
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   └── DEVELOPER_GUIDE.md
├── requirements.txt        # Runtime dependencies
├── pyproject.toml         # Project metadata
├── setup.py               # Installation script
├── README.md              # User documentation
├── GETTING_STARTED.md     # Quick start guide
├── LICENSE                # MIT License
└── .gitignore             # Git ignore patterns
```

### Module Responsibilities

**cli.py**
- Command definitions
- Argument parsing
- User input validation
- Error handling

**core.py**
- Download management
- URL validation
- Task lifecycle
- SpotDL integration

**config.py**
- Configuration storage
- Settings management
- Platform paths
- Defaults

**ui.py**
- Terminal rendering
- Progress display
- Interactive wizards
- Tables and panels

---

## Coding Standards

### Style Guide

Follow PEP 8 with these specifics:

**Line Length:** 88 characters (Black default)

**Imports:**
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import typer
from rich.console import Console

# Local
from .core import DownloadManager
from .config import ConfigManager
```

**Docstrings:**
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
    """
    pass
```

**Type Hints:**
```python
# Always use type hints
def download(url: str, output: str = None) -> bool:
    pass

# Use typing module for complex types
from typing import Optional, List, Dict

def get_tasks() -> List[Dict[str, str]]:
    pass
```

### Naming Conventions

**Functions/Methods:** `snake_case`
```python
def validate_url(url: str) -> dict:
    pass
```

**Classes:** `PascalCase`
```python
class DownloadManager:
    pass
```

**Constants:** `UPPER_SNAKE_CASE`
```python
DEFAULT_FORMAT = "mp3"
MAX_WORKERS = 10
```

**Private:** Prefix with `_`
```python
def _internal_function():
    pass

class MyClass:
    def __init__(self):
        self._private_var = None
```

### Code Formatting

**Use Black:**
```bash
# Format entire project
black grovegrab/

# Check without modifying
black --check grovegrab/

# Format specific file
black grovegrab/cli.py
```

**Use Flake8:**
```bash
# Lint entire project
flake8 grovegrab/

# With specific rules
flake8 --max-line-length=88 --extend-ignore=E203 grovegrab/
```

### Type Checking

**Use MyPy:**
```bash
# Type check entire project
mypy grovegrab/

# Strict mode
mypy --strict grovegrab/
```

---

## Adding Features

### Adding a New CLI Command

**Step 1: Define Command**

```python
# grovegrab/cli.py

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results")
):
    """
    Search for tracks, albums, or artists.
    
    Examples:
    
        grovegrab search "artist name"
        
        grovegrab search "track" --limit 20
    """
    # 1. Validate input
    if not query.strip():
        console.print("[red]Error:[/red] Query cannot be empty")
        raise typer.Exit(1)
    
    # 2. Call core function
    results = download_manager.search(query, limit)
    
    # 3. Display results
    ui.show_search_results(results)
```

**Step 2: Implement Core Logic**

```python
# grovegrab/core.py

def search(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
    """
    Search Spotify for content.
    
    Args:
        query: Search query
        limit: Maximum results
        
    Returns:
        List of search results
    """
    # Implementation
    pass
```

**Step 3: Add UI Component**

```python
# grovegrab/ui.py

def show_search_results(self, results: List[Dict[str, str]]) -> None:
    """
    Display search results in a table.
    
    Args:
        results: List of search results
    """
    table = Table(title="Search Results")
    table.add_column("Type")
    table.add_column("Name")
    table.add_column("Artist")
    table.add_column("URL")
    
    for result in results:
        table.add_row(
            result['type'],
            result['name'],
            result['artist'],
            result['url']
        )
    
    self.console.print(table)
```

**Step 4: Test**

```python
# tests/test_cli.py

def test_search_command():
    """Test search command."""
    from typer.testing import CliRunner
    from grovegrab.cli import app
    
    runner = CliRunner()
    result = runner.invoke(app, ["search", "test query"])
    
    assert result.exit_code == 0
    assert "Search Results" in result.stdout
```

---

### Adding Configuration Options

**Step 1: Update Config Schema**

```python
# grovegrab/config.py

DEFAULT_CONFIG = {
    'spotify': {
        'client_id': '',
        'client_secret': '',
    },
    'download': {
        'output_dir': str(Path.home() / 'Music' / 'GroveGrab'),
        'format': 'mp3',
        'quality': '320k',
        'threads': 3,  # NEW OPTION
    }
}
```

**Step 2: Add CLI Option**

```python
# grovegrab/cli.py

@app.command()
def download(
    url: str = typer.Argument(...),
    threads: int = typer.Option(None, "--threads", "-t", help="Download threads")
):
    # Use config value if not specified
    if threads is None:
        threads = config_manager.get_config()['download']['threads']
    
    # Use in download
    download_manager.start_download(url, threads=threads)
```

**Step 3: Update Setup Wizard**

```python
# grovegrab/ui.py

def run_setup_wizard(self):
    # ... existing prompts ...
    
    threads = IntPrompt.ask(
        "Concurrent downloads",
        default=3,
        show_default=True
    )
    
    config['download']['threads'] = threads
```

---

### Adding External Integrations

**Example: YouTube Music Support**

**Step 1: Add Dependency**

```python
# requirements.txt
ytmusicapi>=1.0.0
```

**Step 2: Extend Core**

```python
# grovegrab/core.py

from ytmusicapi import YTMusic

class DownloadManager:
    def __init__(self):
        self.ytmusic = YTMusic()
        # ... existing init ...
    
    def validate_url(self, url: str) -> dict:
        # Check for YouTube Music URL
        if 'music.youtube.com' in url:
            return self._validate_ytmusic_url(url)
        
        # Existing Spotify validation
        return self._validate_spotify_url(url)
```

---

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Fixtures
├── test_cli.py              # CLI tests
├── test_core.py             # Core logic tests
├── test_config.py           # Config tests
└── test_ui.py               # UI tests
```

### Writing Tests

**Unit Test Example:**

```python
# tests/test_core.py

import pytest
from grovegrab.core import DownloadManager

def test_validate_track_url():
    """Test track URL validation."""
    manager = DownloadManager()
    
    result = manager.validate_url("https://open.spotify.com/track/123")
    
    assert result['valid'] is True
    assert result['type'] == 'track'
    assert result['error'] is None

def test_validate_invalid_url():
    """Test invalid URL validation."""
    manager = DownloadManager()
    
    result = manager.validate_url("not_a_url")
    
    assert result['valid'] is False
    assert result['error'] is not None
```

**CLI Test Example:**

```python
# tests/test_cli.py

from typer.testing import CliRunner
from grovegrab.cli import app

runner = CliRunner()

def test_version_command():
    """Test version command."""
    result = runner.invoke(app, ["version"])
    
    assert result.exit_code == 0
    assert "GroveGrab CLI" in result.stdout

def test_download_without_credentials():
    """Test download fails without credentials."""
    result = runner.invoke(app, ["download", "test_url"])
    
    assert result.exit_code == 1
    assert "credentials" in result.stdout.lower()
```

**Fixture Example:**

```python
# tests/conftest.py

import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_config_dir():
    """Create temporary config directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_config(temp_config_dir):
    """Create mock configuration."""
    config = {
        'spotify': {
            'client_id': 'test_id',
            'client_secret': 'test_secret'
        },
        'download': {
            'output_dir': str(temp_config_dir),
            'format': 'mp3',
            'quality': '320k'
        }
    }
    return config
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_cli.py

# Run specific test
pytest tests/test_cli.py::test_version_command

# With coverage
pytest --cov=grovegrab

# Generate HTML coverage report
pytest --cov=grovegrab --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Mocking External Services

```python
# tests/test_core.py

from unittest.mock import Mock, patch

@patch('grovegrab.core.subprocess.Popen')
def test_download_execution(mock_popen):
    """Test download command execution."""
    # Setup mock
    mock_process = Mock()
    mock_process.poll.return_value = None
    mock_popen.return_value = mock_process
    
    # Test
    manager = DownloadManager()
    result = manager.start_download('task_id', 'spotify_url')
    
    # Verify
    assert result is True
    mock_popen.assert_called_once()
```

---

## Building & Distribution

### Building Package

**Source Distribution:**
```bash
python setup.py sdist
```

**Wheel Distribution:**
```bash
pip install wheel
python setup.py bdist_wheel
```

**Both:**
```bash
python setup.py sdist bdist_wheel
```

**Output:** `dist/grovegrab-1.0.0.tar.gz` and `.whl`

### Building Standalone Binary

**Using PyInstaller:**

```bash
# Install PyInstaller
pip install pyinstaller

# Create spec file
pyi-makespec --name=grovegrab --onefile grovegrab/__main__.py

# Edit grovegrab.spec if needed

# Build binary
pyinstaller grovegrab.spec

# Output: dist/grovegrab.exe (Windows) or dist/grovegrab (Unix)
```

**PyInstaller Spec Example:**

```python
# grovegrab.spec

a = Analysis(
    ['grovegrab/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['typer', 'rich', 'spotdl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='grovegrab',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
```

### Publishing to PyPI

**Setup:**
```bash
# Install tools
pip install twine

# Create PyPI account at https://pypi.org

# Create API token
# Settings → API tokens → Add API token
```

**Test on TestPyPI:**
```bash
# Build
python setup.py sdist bdist_wheel

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ grovegrab
```

**Publish to PyPI:**
```bash
# Upload
twine upload dist/*

# Verify
pip install grovegrab
```

---

## Debugging

### Debug Mode

**Enable Verbose Output:**

```python
# grovegrab/cli.py

# Add debug flag
@app.callback()
def callback(debug: bool = typer.Option(False, "--debug")):
    """Enable debug mode."""
    if debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
```

**Usage:**
```bash
grovegrab --debug download "url"
```

### Logging

**Add Logging:**

```python
# grovegrab/core.py

import logging

logger = logging.getLogger(__name__)

class DownloadManager:
    def start_download(self, task_id, url):
        logger.debug(f"Starting download: {task_id}")
        logger.info(f"URL: {url}")
        
        try:
            # Download logic
            logger.debug("Download completed")
        except Exception as e:
            logger.error(f"Download failed: {e}", exc_info=True)
```

### Debugging with VS Code

**launch.json:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "GroveGrab CLI",
      "type": "python",
      "request": "launch",
      "module": "grovegrab",
      "args": ["download", "test_url"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Common Issues

**Import Errors:**
```bash
# Reinstall in development mode
pip install -e .
```

**Path Issues:**
```python
# Debug paths
from grovegrab.config import ConfigManager
cm = ConfigManager()
print(cm.get_config_path())
```

**Thread Issues:**
```python
# Add thread logging
import threading
print(f"Active threads: {threading.active_count()}")
print(f"Threads: {threading.enumerate()}")
```

---

## Contributing

### Workflow

1. **Fork repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Make changes**
4. **Run tests**
   ```bash
   pytest
   black grovegrab/
   flake8 grovegrab/
   ```
5. **Commit changes**
   ```bash
   git commit -m "Add my feature"
   ```
6. **Push branch**
   ```bash
   git push origin feature/my-feature
   ```
7. **Create pull request**

### Commit Messages

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructure
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```
feat: add search command

Implement Spotify search functionality with:
- Track search
- Album search
- Artist search

Closes #42
```

```
fix: handle empty config file

Check for empty config file before parsing.
Prevents JSON decode error on first run.
```

### Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages clear
- [ ] PR description complete

---

## Resources

### Documentation
- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [SpotDL Documentation](https://spotdl.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)

### Tools
- [Black](https://black.readthedocs.io/) - Code formatter
- [Flake8](https://flake8.pycqa.org/) - Linter
- [MyPy](https://mypy.readthedocs.io/) - Type checker
- [PyInstaller](https://pyinstaller.org/) - Binary builder

### Community
- GitHub Issues - Bug reports
- GitHub Discussions - Questions
- Pull Requests - Contributions

---

## See Also

- [API Reference](API_REFERENCE.md)
- [Architecture](ARCHITECTURE.md)
- [Getting Started](../GETTING_STARTED.md)
- [README](../README.md)
