# PyPI Release Instructions

## Quick Release (After building)

```bash
# Upload to PyPI
python -m twine upload dist/*

# Or upload only version 1.0.2
python -m twine upload dist/grovegrabcli-1.0.2*
```

## Complete Release Process

### 1. Update Version
- Edit `pyproject.toml` - change version number
- Edit `grovegrab/__init__.py` - change __version__
- Update `CHANGELOG.md` with changes

### 2. Build Package
```bash
# Clean old builds
Remove-Item -Path dist,build -Recurse -Force -ErrorAction SilentlyContinue

# Build new package
python -m build
```

### 3. Test Build Locally (Optional)
```bash
# Install in editable mode
pip install -e .

# Or install from built wheel
pip install dist/grovegrabcli-1.0.2-py3-none-any.whl --force-reinstall

# Test the command
grovegrab --help
```

### 4. Upload to PyPI
```bash
# Install twine if not already installed
pip install twine

# Upload to PyPI
python -m twine upload dist/*

# You'll be prompted for:
# Username: __token__
# Password: your-pypi-token (starts with pypi-)
```

### 5. Verify Upload
```bash
# Check on PyPI
# https://pypi.org/project/GroveGrabCLI/

# Test install from PyPI
pip install --upgrade GroveGrabCLI

# Verify version
grovegrab version
```

### 6. Commit and Tag
```bash
git add .
git commit -m "Release v1.0.2: Improved error messages and documentation"
git tag v1.0.2
git push origin main --tags
```

## Version 1.0.2 Changes

### Improvements
- Better error message when Spotify credentials are missing
- Added prominent setup warning in README
- Added troubleshooting section for common errors
- Show config file location in error messages
- Created CHANGELOG.md

### User Impact
The main user complaint was "it's not working" after installing from PyPI. The issue was that users need to configure Spotify API credentials first by running `grovegrab auth`. This release makes that requirement crystal clear with:

1. Updated README with ⚠️ IMPORTANT section at the top
2. Better CLI error messages with step-by-step instructions
3. Troubleshooting section specifically for the "No client_id" error

## PyPI API Token Setup

If you don't have a PyPI token yet:

1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. Click "Add API token"
4. Name: "GroveGrab CLI"
5. Scope: "Project: GroveGrabCLI" (or "Entire account")
6. Copy the token (starts with `pypi-`)
7. Save it securely (you won't see it again)

### Using the token
```bash
# When prompted by twine:
Username: __token__
Password: pypi-...your-token-here...
```

Or store in `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-...your-token-here...
```
