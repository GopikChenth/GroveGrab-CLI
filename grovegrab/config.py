"""
Configuration management for GroveGrab CLI
"""
from pathlib import Path
import json
import platformdirs
import sys
import os
from typing import Optional


class ConfigManager:
    def __init__(self):
        self.config_dir = Path(platformdirs.user_config_dir("grovegrab"))
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = self._load()
    
    def _load(self) -> dict:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                return json.loads(self.config_file.read_text())
            except Exception:
                return self._default_config()
        return self._default_config()
    
    def _get_default_download_path(self) -> str:
        """Get platform-specific default download path"""
        # Check if running on Android (Termux)
        if 'com.termux' in os.environ.get('PREFIX', ''):
            # Termux/Android default path
            return "/storage/emulated/0/Music/GroveGrab"
        else:
            # Windows/Mac/Linux default path
            return str(Path.home() / "Music" / "GroveGrab")
    
    def _default_config(self) -> dict:
        """Default configuration"""
        return {
            "client_id": "",
            "client_secret": "",
            "redirect_uri": "http://localhost:8888/callback",
            "default_download_path": self._get_default_download_path(),
            "audio_format": "mp3",
            "audio_quality": "320k"
        }
    
    def save(self):
        """Save configuration to file"""
        self.config_file.write_text(json.dumps(self.config, indent=2))
    
    def has_credentials(self) -> bool:
        """Check if credentials are configured"""
        return bool(self.config.get("client_id") and self.config.get("client_secret"))
    
    def update(self, **kwargs):
        """Update configuration"""
        self.config.update(kwargs)
        self.save()
    
    def reset(self):
        """Reset to default configuration"""
        self.config = self._default_config()
        self.save()
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
