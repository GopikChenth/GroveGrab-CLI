"""
Terminal UI components using Rich
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn, TimeRemainingColumn
from rich.live import Live
from rich.prompt import Prompt, Confirm
from pathlib import Path
import time
import uuid
import threading


class UIManager:
    def __init__(self, console: Console):
        self.console = console
    
    def run_setup_wizard(self):
        """Interactive setup wizard"""
        self.console.print(Panel.fit(
            "[bold cyan]🎵 GroveGrab Setup Wizard[/bold cyan]\n\n"
            "Get your Spotify API credentials from:\n"
            "[link]https://developer.spotify.com/dashboard[/link]",
            border_style="cyan"
        ))
        
        client_id = Prompt.ask("\n[cyan]Spotify Client ID[/cyan]")
        client_secret = Prompt.ask("[cyan]Spotify Client Secret[/cyan]", password=True)
        
        download_path = Prompt.ask(
            "[cyan]Default download path[/cyan]",
            default=str(Path.home() / "Music" / "GroveGrab")
        )
        
        format_choice = Prompt.ask(
            "[cyan]Audio format[/cyan]",
            choices=["mp3", "flac", "ogg", "opus", "m4a"],
            default="mp3"
        )
        
        quality = Prompt.ask(
            "[cyan]Audio quality[/cyan]",
            choices=["128k", "192k", "256k", "320k"],
            default="320k"
        )
        
        # Save config
        from .config import ConfigManager
        config = ConfigManager()
        config.update(
            client_id=client_id,
            client_secret=client_secret,
            default_download_path=download_path,
            audio_format=format_choice,
            audio_quality=quality
        )
        
        self.console.print("\n[green]OK: Configuration saved![/green]")
        self.console.print(f"Config location: [dim]{config.config_file}[/dim]")
    
    def show_config(self):
        """Display current configuration"""
        from .config import ConfigManager
        config = ConfigManager()
        
        table = Table(title="Current Configuration", show_header=True)
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        # Mask credentials
        client_id = config.get("client_id", "")
        client_secret = config.get("client_secret", "")
        
        table.add_row("Client ID", f"{client_id[:8]}..." if client_id else "[red]Not set[/red]")
        table.add_row("Client Secret", "***" if client_secret else "[red]Not set[/red]")
        table.add_row("Download Path", config.get("default_download_path", ""))
        table.add_row("Audio Format", config.get("audio_format", ""))
        table.add_row("Audio Quality", config.get("audio_quality", ""))
        table.add_row("Config File", str(config.config_file))
        
        self.console.print(table)
    
    def show_live_progress(self, task_id: str, url: str, output: str = None, download_manager=None):
        """Show live progress with Rich"""
        if download_manager is None:
            from .core import DownloadManager
            dm = DownloadManager()
        else:
            dm = download_manager
        
        # Start download in background
        thread = threading.Thread(
            target=dm.start_download,
            args=(task_id, url, output),
            daemon=True
        )
        thread.start()
        
        # Create progress display (no spinner due to Windows encoding issues)
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            
            main_task = progress.add_task("[cyan]Downloading...", total=100)
            track_tasks = {}  # Map track titles to progress task IDs
            
            while True:
                task = dm.get_task(task_id)
                if not task:
                    time.sleep(0.1)
                    continue
                
                # Update overall progress
                total_tracks = task.get('total_tracks', 0)
                completed_tracks = task.get('completed_tracks', 0)
                failed_tracks = task.get('failed_tracks', 0)
                
                if total_tracks > 0:
                    desc = f"[cyan]Overall: {completed_tracks}/{total_tracks} tracks"
                    if failed_tracks > 0:
                        desc += f" ({failed_tracks} failed)"
                    desc += "[/cyan]"
                else:
                    desc = f"[cyan]{task.get('current_track', 'Downloading...')}[/cyan]"
                
                progress.update(
                    main_task,
                    completed=task['progress'],
                    description=desc
                )
                
                # Show individual tracks for playlists/albums
                tracks = task.get('tracks', [])
                if tracks:
                    for track in tracks:
                        track_title = track.get('title', 'Unknown')
                        track_status = track.get('status', 'queued')
                        track_progress = track.get('progress', 0)
                        
                        # Create or update progress bar for this track
                        if track_title not in track_tasks:
                            # Determine color based on status
                            if track_status == 'completed':
                                color = "green"
                            elif track_status == 'failed':
                                color = "red"
                            elif track_status == 'downloading':
                                color = "yellow"
                            else:
                                color = "dim"
                            
                            track_tasks[track_title] = progress.add_task(
                                f"[{color}]{track_title[:50]}[/{color}]",
                                total=100
                            )
                        
                        # Update track progress
                        task_obj = track_tasks[track_title]
                        
                        # Update color based on status
                        if track_status == 'completed':
                            color = "green"
                            track_progress = 100
                        elif track_status == 'failed':
                            color = "red"
                        elif track_status == 'downloading':
                            color = "yellow"
                        else:
                            color = "dim"
                        
                        progress.update(
                            task_obj,
                            completed=track_progress,
                            description=f"[{color}]{track_title[:50]}[/{color}]"
                        )
                
                # Check if done
                if task['status'] in ['completed', 'failed', 'cancelled']:
                    break
                
                time.sleep(0.5)
        
        # Show final status
        task = dm.get_task(task_id)
        if task['status'] == 'completed':
            self.console.print(f"\n[green]OK: Download complete![/green]")
            self.console.print(f"[dim]Location: {task['download_path']}[/dim]")
            
            # Show summary
            total = task.get('total_tracks', 0)
            completed = task.get('completed_tracks', 0)
            failed = task.get('failed_tracks', 0)
            if total > 0:
                msg = f"Downloaded: {completed}/{total} tracks"
                if failed > 0:
                    msg += f" ({failed} failed)"
                self.console.print(f"[dim]{msg}[/dim]")
        elif task['status'] == 'failed':
            self.console.print(f"\n[red]Error: Download failed[/red]")
            self.console.print(f"[dim]Run 'grovegrab logs {task_id[:8]}' for details[/dim]")
        else:
            self.console.print(f"\n[yellow]Warning: Download cancelled[/yellow]")
        
        thread.join(timeout=2)
    
    def show_simple_progress(self, task_id: str, url: str, output: str = None, download_manager=None):
        """Simple progress without live updates"""
        if download_manager is None:
            from .core import DownloadManager
            dm = DownloadManager()
        else:
            dm = download_manager
        
        self.console.print(f"[cyan]Starting download...[/cyan]")
        self.console.print(f"Task ID: [dim]{task_id[:8]}[/dim]")
        
        thread = threading.Thread(
            target=dm.start_download,
            args=(task_id, url, output),
            daemon=True
        )
        thread.start()
        
        # Wait a moment for initial status
        time.sleep(1)
        
        self.console.print("[green]OK:[/green] Download started")
        self.console.print(f"Watch progress: [cyan]grovegrab list[/cyan]")
        self.console.print(f"View logs: [cyan]grovegrab logs {task_id[:8]}[/cyan]")
    
    def show_tasks_table(self, tasks: list):
        """Display tasks in a table"""
        if not tasks:
            self.console.print("[yellow]No active tasks[/yellow]")
            return
        
        table = Table(title="Download Tasks", show_header=True)
        table.add_column("ID", style="dim")
        table.add_column("Status", style="cyan")
        table.add_column("Progress", style="green")
        table.add_column("Current Track", style="white")
        table.add_column("Stats", style="blue")
        
        for task in tasks:
            status_emoji = {
                'running': '>',
                'completed': 'OK',
                'failed': 'ERR',
                'cancelled': 'STOP'
            }.get(task['status'], '?')
            
            stats = f"{task['completed_tracks']}/{task['total_tracks']}"
            if task['failed_tracks'] > 0:
                stats += f" ({task['failed_tracks']} failed)"
            
            table.add_row(
                task['id'][:8],
                f"{status_emoji} {task['status']}",
                f"{task['progress']}%",
                task.get('current_track', '-')[:40],
                stats
            )
        
        self.console.print(table)
    
    def show_logs(self, task_id: str):
        """Display task logs"""
        from .core import DownloadManager
        dm = DownloadManager()
        
        logs = dm.get_task_logs(task_id)
        if not logs:
            self.console.print(f"[red]Error:[/red] No logs found for task {task_id[:8]}")
            return
        
        self.console.print(Panel.fit(
            f"[bold cyan]Logs for task {task_id[:8]}[/bold cyan]",
            border_style="cyan"
        ))
        
        for log in logs:
            self.console.print(log)
    
    def follow_logs(self, task_id: str):
        """Follow logs in real-time"""
        from .core import DownloadManager
        dm = DownloadManager()
        
        self.console.print(f"[cyan]Following logs for task {task_id[:8]}[/cyan]")
        self.console.print("[dim]Press Ctrl+C to stop[/dim]\n")
        
        last_count = 0
        try:
            while True:
                logs = dm.get_task_logs(task_id)
                if logs and len(logs) > last_count:
                    for log in logs[last_count:]:
                        self.console.print(log)
                    last_count = len(logs)
                
                task = dm.get_task(task_id)
                if task and task['status'] in ['completed', 'failed', 'cancelled']:
                    self.console.print(f"\n[cyan]Task {task['status']}[/cyan]")
                    break
                
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Stopped following logs[/yellow]")
    
    def batch_download(self, urls: list, workers: int):
        """Download multiple URLs with progress"""
        from concurrent.futures import ThreadPoolExecutor
        from .core import DownloadManager
        
        dm = DownloadManager()
        
        self.console.print(f"[cyan]Starting batch download of {len(urls)} URLs[/cyan]")
        
        with Progress(console=self.console) as progress:
            task = progress.add_task("[cyan]Downloading...", total=len(urls))
            
            def download_one(url):
                task_id = str(uuid.uuid4())
                dm.start_download(task_id, url)
                progress.advance(task)
            
            with ThreadPoolExecutor(max_workers=workers) as executor:
                executor.map(download_one, urls)
        
        self.console.print("[green]OK: Batch download complete![/green]")
