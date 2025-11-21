"""
Core download manager - Adapted from GroveGrab web version
Handles SpotDL integration and download queue management
"""
from __future__ import annotations

import json
import logging
import re
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from threading import RLock
from typing import List, Optional
import platformdirs
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


logger = logging.getLogger(__name__)


def check_internet_connection():
    """Check if internet connection is available"""
    try:
        # Try to connect to Google's DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


class DownloadManager:
    def __init__(self):
        # Use platform-specific config directory for CLI
        config_dir = Path(platformdirs.user_config_dir("grovegrab"))
        config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = config_dir / "config.json"
        self.tasks_dir = config_dir / "tasks"
        self.tasks_dir.mkdir(exist_ok=True)
        self.logs_dir = config_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.tasks = {}  # task_id -> task_data (JSON-serializable)
        self.tasks_lock = RLock()  # Use RLock to allow reentrant locking
        self.processes = {}  # task_id -> subprocess.Popen

        self.config = self._load_config()
        self._load_tasks()

    # ---------------------------- Config ---------------------------- #
    def _load_config(self) -> dict:
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")

        default_config = {
            'client_id': '',
            'client_secret': '',
            'redirect_uri': 'http://localhost:8888/callback',
            'default_download_path': str(Path.home() / 'Music' / 'GroveGrab'),
            'audio_format': 'mp3',
            'audio_quality': '320k',
            'has_credentials': False,
        }
        self._save_config(default_config)
        return default_config

    def _save_config(self, config: dict):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get_config(self) -> dict:
        return self.config.copy()

    def update_config(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        redirect_uri: str | None = None,
        download_path: str | None = None,
        audio_format: str | None = None,
        audio_quality: str | None = None,
    ) -> bool:
        try:
            if client_id is not None:
                self.config['client_id'] = client_id
            if client_secret is not None:
                self.config['client_secret'] = client_secret
            if redirect_uri is not None:
                self.config['redirect_uri'] = redirect_uri
            if download_path is not None:
                self.config['default_download_path'] = download_path
            if audio_format is not None:
                self.config['audio_format'] = audio_format
            if audio_quality is not None:
                self.config['audio_quality'] = audio_quality

            self.config['has_credentials'] = bool(
                self.config.get('client_id') and self.config.get('client_secret')
            )

            self._save_config(self.config)
            return True
        except Exception as e:
            logger.error(f"Failed to update config: {e}")
            return False

    # ---------------------------- Task Persistence ---------------------------- #
    def _load_tasks(self):
        """Load tasks from disk"""
        try:
            for task_file in self.tasks_dir.glob("*.json"):
                with open(task_file, 'r', encoding='utf-8') as f:
                    task = json.load(f)
                    self.tasks[task['id']] = task
        except Exception as e:
            logger.error(f"Failed to load tasks: {e}")
    
    def _save_task(self, task_id: str):
        """Save a single task to disk"""
        try:
            with self.tasks_lock:
                if task_id in self.tasks:
                    task_file = self.tasks_dir / f"{task_id}.json"
                    with open(task_file, 'w', encoding='utf-8') as f:
                        json.dump(self.tasks[task_id], f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save task {task_id}: {e}")

    # ---------------------------- Validation ---------------------------- #
    def validate_url(self, url: str) -> dict:
        patterns = {
            'track': r'spotify\.com/track/([a-zA-Z0-9]+)',
            'playlist': r'spotify\.com/playlist/([a-zA-Z0-9]+)',
            'album': r'spotify\.com/album/([a-zA-Z0-9]+)',
            'artist': r'spotify\.com/artist/([a-zA-Z0-9]+)',
        }
        for url_type, pattern in patterns.items():
            m = re.search(pattern, url)
            if m:
                return {'valid': True, 'type': url_type, 'id': m.group(1), 'url': url}
        return {
            'valid': False,
            'error': 'Invalid Spotify URL. Please provide a valid track, playlist, album, or artist URL.',
        }

    # ---------------------------- Tasks ---------------------------- #
    def start_download(self, task_id: str, url: str, download_path: str | None = None):
        # Check internet connection first
        if not check_internet_connection():
            with self.tasks_lock:
                self.tasks[task_id] = {
                    'id': task_id,
                    'url': url,
                    'type': 'download',
                    'status': 'failed',
                    'progress': 0,
                    'total_tracks': 0,
                    'completed_tracks': 0,
                    'failed_tracks': 0,
                    'current_track': '',
                    'tracks': [],
                    'download_path': download_path or self.config.get('default_download_path'),
                    'logs': ['ERROR: No internet connection detected. Please check your network and try again.'],
                    'failed_track_list': [],
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'cancelled': False,
                }
                self._save_task(task_id)
            logger.error(f"Task {task_id}: No internet connection")
            return

        if not download_path:
            download_path = self.config.get('default_download_path')
        
        # Initialize task first so we can log
        with self.tasks_lock:
            self.tasks[task_id] = {
                'id': task_id,
                'url': url,
                'type': 'download',
                'status': 'running',
                'progress': 0,
                'total_tracks': 0,
                'completed_tracks': 0,
                'failed_tracks': 0,
                'current_track': '',
                'tracks': [],
                'download_path': download_path,
                'logs': [],
                'failed_track_list': [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'cancelled': False,
            }
            self._save_task(task_id)
        
        # Check if URL is playlist or album - create subfolder with name
        validation = self.validate_url(url)
        if validation.get('valid') and validation.get('type') in ['playlist', 'album']:
            self._log(task_id, f"Detecting {validation['type']} name...")
            playlist_name = self._get_playlist_name(url)
            if playlist_name:
                download_path = str(Path(download_path) / playlist_name)
                self._log(task_id, f"Creating folder: {playlist_name}")
                # Update task with new path
                with self.tasks_lock:
                    self.tasks[task_id]['download_path'] = download_path
                    self._save_task(task_id)
        
        Path(download_path).mkdir(parents=True, exist_ok=True)

        try:
            self._log(task_id, f"Starting download for: {url}")
            self._log(task_id, f"Download path: {download_path}")

            cmd = self._build_spotdl_command(url, download_path=download_path)
            result = self._execute_spotdl(task_id, cmd)

            with self.tasks_lock:
                if self.tasks[task_id].get('cancelled'):
                    self.tasks[task_id]['status'] = 'cancelled'
                    final_msg = 'Download cancelled by user'
                elif result['success']:
                    self.tasks[task_id]['status'] = 'completed'
                    self.tasks[task_id]['progress'] = 100
                    final_msg = 'Download completed successfully!'
                else:
                    self.tasks[task_id]['status'] = 'failed'
                    final_msg = f"Download failed: {result.get('error', 'Unknown error')}"
                self.tasks[task_id]['updated_at'] = datetime.now().isoformat()
                self._save_task(task_id)

            self._log(task_id, final_msg)
        except Exception as e:
            logger.error(f"Download error for task {task_id}: {e}")
            with self.tasks_lock:
                self.tasks[task_id]['status'] = 'failed'
                self.tasks[task_id]['updated_at'] = datetime.now().isoformat()
                self._save_task(task_id)
            self._log(task_id, f"Error: {str(e)}")

    # ---------------------------- SpotDL ---------------------------- #
    def _get_playlist_name(self, url: str) -> str | None:
        """Extract playlist/album name from Spotify metadata using Spotipy API"""
        try:
            # Use Spotify API to get album/playlist name
            validation = self.validate_url(url)
            if not validation.get('valid'):
                return None
            
            url_type = validation.get('type')
            spotify_id = validation.get('id')
            
            # Suppress Spotipy cache warnings by temporarily redirecting stderr
            import sys
            import os
            old_stderr = sys.stderr
            try:
                sys.stderr = open(os.devnull, 'w')
                
                # Initialize Spotify client without credentials (public API)
                sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                    client_id=None,
                    client_secret=None
                ))
                
                name = None
                
                # Get metadata based on URL type
                if url_type == 'album':
                    result = sp.album(spotify_id)
                    name = result.get('name')
                    logger.info(f"Album: {name} by {result.get('artists', [{}])[0].get('name', 'Unknown')}")
                    
                elif url_type == 'playlist':
                    result = sp.playlist(spotify_id)
                    name = result.get('name')
                    logger.info(f"Playlist: {name} by {result.get('owner', {}).get('display_name', 'Unknown')}")
            finally:
                sys.stderr.close()
                sys.stderr = old_stderr
            
            if name:
                # Clean up name for use as folder
                name = name.strip('"\'')
                # Remove invalid filename characters
                name = re.sub(r'[<>:"/\\|?*]', '_', name)
                # Limit length
                if len(name) > 100:
                    name = name[:100]
                return name
            
            # Fallback: use URL type + ID
            return f"{url_type}_{spotify_id[:8]}"
            
        except Exception as e:
            logger.error(f"Failed to get playlist name: {e}")
            # Fallback: use URL type + ID if we have it
            try:
                validation = self.validate_url(url)
                if validation.get('valid'):
                    return f"{validation.get('type')}_{validation.get('id')[:8]}"
            except:
                pass
            return None

    def _build_spotdl_command(
        self, url: str, download_path: str | None = None, preload_only: bool = False
    ) -> List[str]:
        cmd = ['spotdl']
        cmd.append(url)

        # SpotDL 3.9.6 doesn't support --client-id/--client-secret
        # It uses YouTube Music by default which doesn't need Spotify credentials

        if not preload_only:
            if download_path:
                cmd.extend(['--output', download_path])

            audio_format = self.config.get('audio_format', 'mp3')
            cmd.extend(['--output-format', audio_format])

        return cmd

    def _execute_spotdl(self, task_id: str, cmd: List[str]) -> dict:
        try:
            self._log(task_id, f"Executing: {' '.join(cmd[:2])}...")

            # On Windows, use CREATE_NO_WINDOW to prevent console output leakage
            import sys
            import os
            creationflags = 0
            if sys.platform == 'win32':
                creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0x08000000
            
            # Set environment to suppress Python warnings from SpotDL
            env = os.environ.copy()
            env['PYTHONWARNINGS'] = 'ignore'
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=False,  # Read as bytes to handle \r properly
                bufsize=0,   # Unbuffered
                creationflags=creationflags,
                env=env
            )
            with self.tasks_lock:
                self.processes[task_id] = process

            dns_error_count = 0
            buffer = b''
            
            # Read output character by character to handle \r as line delimiter
            while True:
                char = process.stdout.read(1)
                if not char:
                    break
                
                buffer += char
                
                # Process line on \n or \r
                if char == b'\n' or char == b'\r':
                    line = buffer.decode('utf-8', errors='replace').strip()
                    buffer = b''
                    
                    if not line:
                        continue

                    if 'getaddrinfo failed' in line or 'Failed to resolve' in line:
                        dns_error_count += 1
                        if dns_error_count == 1:
                            self._log(task_id, 'WARNING: Network/DNS error detected. Retrying...')
                        continue

                    if 'ConnectionResetError' in line or 'Connection broken' in line:
                        self._log(task_id, 'WARNING: Connection issue detected. SpotDL will retry automatically...')
                        continue

                    # Filter out unwanted lines
                    unwanted_patterns = [
                        "Couldn't read cache",
                        "Couldn't write token to cache",
                        "pkg_resources is deprecated",
                        "import pkg_resources",
                        "UserWarning",
                        "argument_parser.py",  # Filter SpotDL internal warnings
                        "Refrain from using this package"
                    ]
                    if any(skip in line for skip in unwanted_patterns):
                        continue

                    with self.tasks_lock:
                        if self.tasks.get(task_id, {}).get('cancelled'):
                            try:
                                process.terminate()
                            except Exception:
                                pass
                            return {'success': False, 'error': 'Cancelled by user'}

                    self._log(task_id, line)
                    self._parse_progress(task_id, line)

            # Process any remaining buffer
            if buffer:
                line = buffer.decode('utf-8', errors='replace').strip()
                if line:
                    self._log(task_id, line)
                    self._parse_progress(task_id, line)

            process.wait()
            
            if dns_error_count > 10:
                self._log(task_id, 'ERROR: Download failed: Network/DNS resolution errors. Please check your internet connection.')
                return {'success': False, 'error': 'Network connectivity issues - DNS resolution failed'}
            
            if process.returncode == 0:
                # Mark all tracks as completed (SpotDL doesn't output completion messages)
                with self.tasks_lock:
                    task = self.tasks.get(task_id)
                    if task:
                        for track in task.get('tracks', []):
                            if track['status'] != 'failed':
                                track['status'] = 'completed'
                                track['progress'] = 100
                        task['completed_tracks'] = len([t for t in task.get('tracks', []) if t['status'] == 'completed'])
                        task['progress'] = 100
                return {'success': True}
            return {'success': False, 'error': f'Process exited with code {process.returncode}'}
        except Exception as e:
            logger.error(f"SpotDL execution error: {e}")
            error_msg = str(e)
            if 'getaddrinfo failed' in error_msg:
                error_msg = 'Network error: Cannot resolve Spotify/YouTube domains. Check your internet connection.'
            return {'success': False, 'error': error_msg}
        finally:
            with self.tasks_lock:
                self.processes.pop(task_id, None)

    # ---------------------------- Parsing ---------------------------- #
    def _parse_progress(self, task_id: str, line: str):
        with self.tasks_lock:
            task = self.tasks.get(task_id)
            if not task:
                return

            # Match "Found X songs" pattern
            m_total = re.search(r"Found\s+(\d+)\s+(songs?|tracks?)", line, re.IGNORECASE)
            if m_total:
                try:
                    task['total_tracks'] = int(m_total.group(1))
                except Exception:
                    pass

            # Extract track title from various patterns
            title = None
            
            # Pattern 1: Quoted strings (most common)
            m_title_quoted = re.search(r'"([^"\n]+)"', line)
            if m_title_quoted:
                title = m_title_quoted.group(1)
            
            # Pattern 2: "Searching YouTube Music for..." 
            if not title:
                m_searching = re.search(r'Searching YouTube Music for "([^"]+)"', line)
                if m_searching:
                    title = m_searching.group(1)
            
            # Pattern 3: "Found YouTube URL for..."
            if not title:
                m_found_url = re.search(r'Found YouTube URL for "([^"]+)"', line)
                if m_found_url:
                    title = m_found_url.group(1)
            
            # Pattern 4: Downloading/Processing
            if not title:
                m_processing = re.search(r"(?:Downloading|Processing)[:\s]+(.+)$", line, re.IGNORECASE)
                if m_processing:
                    title = m_processing.group(1).strip()

            def ensure_track(t_title: str):
                if not t_title:
                    return None
                for t in task['tracks']:
                    if t.get('title') == t_title:
                        return t
                t = {'title': t_title, 'status': 'queued', 'progress': 0}
                task['tracks'].append(t)
                return t

            percent = None
            m_pct = re.search(r"(\d{1,3})%", line)
            if m_pct:
                try:
                    percent = max(0, min(100, int(m_pct.group(1))))
                except Exception:
                    percent = None

            lowered = line.lower()

            # Detect album/playlist fetching
            if 'fetching album' in lowered or 'fetching playlist' in lowered:
                task['status'] = 'searching'
            
            # Track searching phase
            if 'searching youtube music' in lowered and title:
                task['current_track'] = title
                t = ensure_track(title)
                if t and t['status'] == 'queued':
                    t['status'] = 'searching'
                    t['progress'] = 25  # Searching
                # Update total tracks based on number of unique tracks we've seen
                if task.get('total_tracks', 0) == 0:
                    task['total_tracks'] = len(task['tracks'])

            # Track downloading phase
            if ('downloading' in lowered or 'processing' in lowered) and title:
                task['current_track'] = title
                t = ensure_track(title)
                if t:
                    t['status'] = 'downloading'
                    if percent is not None:
                        t['progress'] = percent
            
            # Track found URL (means search completed, starting download)
            if 'found youtube url' in lowered and title:
                t = ensure_track(title)
                if t:
                    t['status'] = 'downloading'
                    t['progress'] = 50  # Found URL, halfway there

            # Track completed (SpotDL doesn't output this, so we infer from process completion)
            if 'downloaded' in lowered or 'completed' in lowered:
                t = ensure_track(title or task.get('current_track'))
                if t and t['status'] != 'completed':
                    t['status'] = 'completed'
                    t['progress'] = 100
                    task['completed_tracks'] = (task.get('completed_tracks') or 0) + 1

            # Track failed
            if 'failed' in lowered or 'error' in lowered:
                t = ensure_track(title or task.get('current_track'))
                if t and t['status'] != 'failed':
                    t['status'] = 'failed'
                    if percent is None:
                        t['progress'] = 0
                    task['failed_tracks'] = (task.get('failed_tracks') or 0) + 1
                    task['failed_track_list'].append(line)

            # Calculate overall progress from individual track progress
            tracks = task.get('tracks', [])
            if tracks:
                total_progress = sum(t.get('progress', 0) for t in tracks)
                task['progress'] = int(total_progress / len(tracks))
                task['total_tracks'] = len(tracks)
            else:
                task['progress'] = 0

            task['updated_at'] = datetime.now().isoformat()

    # ---------------------------- Logging ---------------------------- #
    def _log(self, task_id: str, message: str):
        timestamp = datetime.now().strftime('%H:%M:%S')
        entry = f"[{timestamp}] {message}"
        with self.tasks_lock:
            if task_id in self.tasks:
                self.tasks[task_id].setdefault('logs', []).append(entry)
                self._save_task(task_id)
        logger.info(f"Task {task_id}: {message}")

    # ---------------------------- Public API ---------------------------- #
    def get_all_tasks(self) -> List[dict]:
        with self.tasks_lock:
            return list(self.tasks.values())

    def get_task(self, task_id: str) -> Optional[dict]:
        with self.tasks_lock:
            return self.tasks.get(task_id)

    def get_task_logs(self, task_id: str) -> Optional[List[str]]:
        with self.tasks_lock:
            task = self.tasks.get(task_id)
            return task['logs'] if task else None

    def cancel_task(self, task_id: str) -> bool:
        proc = None
        with self.tasks_lock:
            task = self.tasks.get(task_id)
            if not task or task['status'] != 'running':
                return False
            task['cancelled'] = True
            task['status'] = 'cancelled'
            task['updated_at'] = datetime.now().isoformat()
            for t in task.get('tracks', []):
                if t.get('status') in ('downloading', 'queued'):
                    t['status'] = 'cancelled'
            task['current_track'] = ''
            proc = self.processes.get(task_id)

        try:
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except Exception:
                    if proc.poll() is None:
                        proc.kill()
        except Exception:
            pass

        self._log(task_id, 'Stop requested by user')
        return True

    def delete_task(self, task_id: str) -> bool:
        with self.tasks_lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            proc = self.processes.pop(task_id, None)
        try:
            if proc and proc.poll() is None:
                proc.terminate()
        except Exception:
            pass
        with self.tasks_lock:
            self.tasks.pop(task_id, None)
        return True

    def retry_failed(self, task_id: str) -> bool:
        with self.tasks_lock:
            task = self.tasks.get(task_id)
            if not task or task['status'] != 'failed':
                return False
            task['failed_tracks'] = 0
            task['failed_track_list'] = []
            task['status'] = 'running'
            task['updated_at'] = datetime.now().isoformat()

        import threading

        thread = threading.Thread(
            target=self.start_download, args=(task_id, task['url'], task.get('download_path'))
        )
        thread.daemon = True
        thread.start()
        return True
