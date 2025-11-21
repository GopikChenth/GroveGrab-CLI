"""
GroveGrab CLI - Main Command Line Interface
"""
import typer
from rich.console import Console
from rich.prompt import Confirm
from pathlib import Path
import sys
import uuid
import os

from .core import DownloadManager
from .config import ConfigManager
from .ui import UIManager

# Initialize
app = typer.Typer(
    name="grovegrab",
    help="Download Spotify tracks, playlists, albums, and artists",
    add_completion=False
)
console = Console()
config_manager = ConfigManager()
download_manager = DownloadManager()
ui = UIManager(console)


def show_ascii_banner():
    """Display the GroveGrab ASCII art banner with colorful gradient"""
    try:
        # Get the directory where this file is located (inside grovegrab package)
        current_dir = Path(__file__).parent
        ascii_file = current_dir / "ascii-art.txt"
        
        if ascii_file.exists():
            ascii_art = ascii_file.read_text(encoding='utf-8')
            lines = ascii_art.rstrip().split('\n')
            
            # Gradient colors: cyan -> purple -> magenta
            colors = [
                '#00d4ff',  # Line 1: Bright cyan
                '#00c8f0',  # Line 2: Cyan
                '#00bce0',  # Line 3: Light blue
                '#00b0d0',  # Line 4: Blue
                '#00a4c0',  # Line 5: Blue-purple
                '#7b68ee',  # Line 6: Purple
                '#9370db',  # Line 7: Medium purple
                '#ba55d3',  # Line 8: Orchid
                '#da70d6',  # Line 9: Light orchid
                '#ff00ff',  # Line 10: Magenta (tagline)
            ]
            
            # Print each line with its gradient color
            for i, line in enumerate(lines):
                if i < len(colors):
                    console.print(f"[{colors[i]}]{line}[/{colors[i]}]")
                else:
                    console.print(f"[{colors[-1]}]{line}[/{colors[-1]}]")
            
            console.print()  # Add a blank line after the banner
    except Exception:
        # Silently fail if ASCII art can't be loaded
        pass


def check_first_run():
    """Check if this is first run and prompt for setup"""
    if not config_manager.has_credentials():
        show_ascii_banner()
        console.print()
        console.print("[yellow]👋 Welcome to GroveGrab![/yellow]")
        console.print()
        console.print("Before you can download music, you need to set up your Spotify API credentials.")
        console.print("This is [green]FREE[/green] and takes just 2 minutes!")
        console.print()
        console.print("📋 Quick Setup:")
        console.print("   1. Get credentials from [link]https://developer.spotify.com/dashboard[/link]")
        console.print("   2. Run: [cyan]grovegrab auth[/cyan]")
        console.print("   3. Start downloading!")
        console.print()
        
        from rich.prompt import Confirm
        if Confirm.ask("Would you like to set up now?", default=True):
            ui.run_setup_wizard()
            console.print()
            console.print("[green]✓[/green] Setup complete! You can now download music.")
            console.print()
            return True
        else:
            console.print()
            console.print("[yellow]Remember to run[/yellow] [cyan]grovegrab auth[/cyan] [yellow]before downloading![/yellow]")
            console.print()
            raise typer.Exit(0)
    return False


@app.command(name="dl")
def download(
    url: str = typer.Argument(..., help="Spotify URL to download"),
    output: str = typer.Option(None, "--output", "-o", help="Download directory"),
    format: str = typer.Option(None, "--format", "-f", help="Audio format (mp3, flac, etc.)"),
    quality: str = typer.Option(None, "--quality", "-q", help="Audio quality (128k, 192k, 256k, 320k)"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch progress in real-time"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run in background")
):
    """
    Download from a Spotify URL
    
    Examples:
    
        grovegrab dl "https://open.spotify.com/track/..."
        
        grovegrab dl "url" --format flac --quality 320k
        
        grovegrab dl "url" --output ~/Music --watch
    """
    # Check if first run and prompt for setup
    if check_first_run():
        # User just completed setup, continue with download
        pass
    
    # Validate URL
    validation = download_manager.validate_url(url)
    if not validation['valid']:
        console.print(f"[red]Error:[/red] Invalid URL: {validation['error']}")
        raise typer.Exit(1)
    
    console.print(f"[cyan]Starting download:[/cyan] {validation['type']}")
    
    # Start download
    task_id = str(uuid.uuid4())
    
    if watch:
        ui.show_live_progress(task_id, url, output, download_manager=download_manager)
    elif detach:
        ui.show_simple_progress(task_id, url, output, download_manager=download_manager)
    else:
        ui.show_live_progress(task_id, url, output, download_manager=download_manager)


@app.command(name="auth")
def setup(
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Interactive setup")
):
    """
    Configure Spotify API credentials
    
    Get credentials from: https://developer.spotify.com/dashboard
    """
    # Show ASCII banner
    show_ascii_banner()
    
    if interactive:
        ui.run_setup_wizard()
    else:
        console.print("[yellow]Open auth wizard with:[/yellow] grovegrab auth")


@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    reset: bool = typer.Option(False, "--reset", help="Reset configuration")
):
    """
    Manage configuration
    """
    if reset:
        if Confirm.ask("Reset all configuration?"):
            config_manager.reset()
            console.print("[green]OK:[/green] Configuration reset")
        return
    
    if show:
        ui.show_config()
    else:
        console.print("Use --show to view or run 'grovegrab auth' to configure")


@app.command()
def list(
    all: bool = typer.Option(False, "--all", "-a", help="Show all tasks including completed")
):
    """
    List download tasks
    """
    tasks = download_manager.get_all_tasks()
    
    if not all:
        tasks = [t for t in tasks if t['status'] == 'running']
    
    ui.show_tasks_table(tasks)


@app.command()
def cancel(task_id: str = typer.Argument(..., help="Task ID to cancel")):
    """
    Cancel a running download task
    """
    # Find task by partial ID
    all_tasks = download_manager.get_all_tasks()
    matching = [t for t in all_tasks if t['id'].startswith(task_id)]
    
    if not matching:
        console.print(f"[red]Error:[/red] Task not found: {task_id}")
        raise typer.Exit(1)
    
    if len(matching) > 1:
        console.print(f"[yellow]Warning:[/yellow] Multiple tasks match: {task_id}")
        for t in matching:
            console.print(f"  - {t['id'][:8]}")
        raise typer.Exit(1)
    
    full_id = matching[0]['id']
    if download_manager.cancel_task(full_id):
        console.print(f"[green]OK:[/green] Task {task_id} cancelled")
    else:
        console.print(f"[red]Error:[/red] Task not running")
        raise typer.Exit(1)


@app.command()
def retry(task_id: str = typer.Argument(..., help="Task ID to retry")):
    """
    Retry a failed download task
    """
    # Find task by partial ID
    all_tasks = download_manager.get_all_tasks()
    matching = [t for t in all_tasks if t['id'].startswith(task_id)]
    
    if not matching:
        console.print(f"[red]Error:[/red] Task not found: {task_id}")
        raise typer.Exit(1)
    
    if len(matching) > 1:
        console.print(f"[yellow]Warning:[/yellow] Multiple tasks match: {task_id}")
        for t in matching:
            console.print(f"  - {t['id'][:8]}")
        raise typer.Exit(1)
    
    full_id = matching[0]['id']
    if download_manager.retry_failed(full_id):
        console.print(f"[green]OK:[/green] Task {task_id} restarted")
    else:
        console.print(f"[red]Error:[/red] Task not failed")
        raise typer.Exit(1)


@app.command()
def logs(
    task_id: str = typer.Argument(..., help="Task ID"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log output")
):
    """
    View logs for a download task
    """
    # Find task by partial ID
    all_tasks = download_manager.get_all_tasks()
    matching = [t for t in all_tasks if t['id'].startswith(task_id)]
    
    if not matching:
        console.print(f"[red]Error:[/red] Task not found: {task_id}")
        raise typer.Exit(1)
    
    if len(matching) > 1:
        console.print(f"[yellow]Warning:[/yellow] Multiple tasks match: {task_id}")
        for t in matching:
            console.print(f"  - {t['id'][:8]}")
        raise typer.Exit(1)
    
    full_id = matching[0]['id']
    
    if follow:
        ui.follow_logs(full_id)
    else:
        ui.show_logs(full_id)


@app.command()
def batch(
    file: Path = typer.Argument(..., help="File containing URLs (one per line)"),
    workers: int = typer.Option(3, "--workers", "-w", help="Concurrent downloads")
):
    """
    Download multiple URLs from a file
    
    Example file.txt:
        https://open.spotify.com/track/...
        https://open.spotify.com/playlist/...
        https://open.spotify.com/album/...
    """
    if not file.exists():
        console.print(f"[red]Error:[/red] File not found: {file}")
        raise typer.Exit(1)
    
    urls = [line.strip() for line in file.read_text().splitlines() if line.strip()]
    
    if not urls:
        console.print(f"[red]Error:[/red] No URLs found in file")
        raise typer.Exit(1)
    
    console.print(f"[cyan]Found {len(urls)} URLs[/cyan]")
    ui.batch_download(urls, workers)


@app.command()
def version():
    """
    Show version information
    """
    # Show ASCII banner
    show_ascii_banner()
    
    from . import __version__
    console.print(f"[cyan]GroveGrab CLI[/cyan] v{__version__}")
    console.print("Built for music lovers")


def main():
    """Entry point for the CLI"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Warning: Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
