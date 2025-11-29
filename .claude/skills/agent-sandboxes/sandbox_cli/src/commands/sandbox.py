"""
Sandbox management commands.
"""

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from ..modules import sandbox as sbx_module

console = Console()


@click.group()
def sandbox():
    """Sandbox lifecycle management commands."""
    pass


@sandbox.command()
@click.option("--template", "-t", default=None, help="Sandbox template name or ID")
@click.option("--timeout", default=300, help="Sandbox timeout in seconds")
@click.option("--env", "-e", multiple=True, help="Environment variables (KEY=VALUE)")
@click.option("--metadata", "-m", multiple=True, help="Metadata (KEY=VALUE)")
@click.option("--auto-pause", is_flag=True, help="Enable auto-pause (beta)")
def create(template, timeout, env, metadata, auto_pause):
    """Create a new sandbox."""
    try:
        # Parse env vars
        envs = {}
        for e in env:
            if "=" in e:
                key, value = e.split("=", 1)
                envs[key] = value

        # Parse metadata
        meta = {}
        for m in metadata:
            if "=" in m:
                key, value = m.split("=", 1)
                meta[key] = value

        console.print("[yellow]Creating sandbox...[/yellow]")

        sbx = sbx_module.create_sandbox(
            template=template,
            timeout=timeout,
            envs=envs if envs else None,
            metadata=meta if meta else None,
            auto_pause=auto_pause,
        )

        console.print(f"[green]✓ Sandbox created: {sbx.sandbox_id}[/green]")
        console.print(f"[dim]Template: {template or 'base'}[/dim]")
        console.print(f"[dim]Timeout: {timeout}s[/dim]")
        if auto_pause:
            console.print("[dim]Auto-pause: enabled[/dim]")

        # Important: save the sandbox_id for the user
        console.print(f"\n[cyan]Export for reuse:[/cyan] export SANDBOX_ID={sbx.sandbox_id}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@sandbox.command()
@click.argument("sandbox_id")
@click.option("--timeout", default=None, help="Update timeout in seconds")
def connect(sandbox_id, timeout):
    """Connect to an existing sandbox."""
    try:
        console.print(f"[yellow]Connecting to sandbox: {sandbox_id}[/yellow]")

        sbx = sbx_module.get_sandbox(sandbox_id, timeout=timeout)
        is_running = sbx.is_running()

        if is_running:
            console.print(f"[green]✓ Connected to sandbox: {sandbox_id}[/green]")
            console.print(f"[dim]Status: Running[/dim]")
        else:
            console.print(f"[red]✗ Sandbox not running[/red]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@sandbox.command()
@click.argument("sandbox_id")
def kill(sandbox_id):
    """Kill a sandbox."""
    try:
        console.print(f"[yellow]Killing sandbox: {sandbox_id}[/yellow]")

        killed = sbx_module.kill_sandbox(sandbox_id)

        if killed:
            console.print(f"[green]✓ Sandbox killed[/green]")
        else:
            console.print(f"[red]✗ Sandbox not found[/red]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


def _build_default_public_url(sandbox_id: str, port: int = 5173) -> str:
    """Build the default public URL for a sandbox."""
    return f"https://{port}-{sandbox_id}.e2b.dev"


@sandbox.command()
@click.argument("sandbox_id")
def info(sandbox_id):
    """Get sandbox information."""
    try:
        console.print(f"[yellow]Getting info for: {sandbox_id}[/yellow]")

        info = sbx_module.get_sandbox_info(sandbox_id)

        table = Table(title=f"Sandbox Info: {sandbox_id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Sandbox ID", info["sandbox_id"])
        table.add_row("Default Public URL", _build_default_public_url(info["sandbox_id"]))
        table.add_row("Template", info["template_id"])

        # Display state with color
        state = info.get("state", "unknown")
        if state == "running":
            table.add_row("State", "[green]Running[/green]")
        elif state == "paused":
            table.add_row("State", "[yellow]Paused[/yellow]")
        else:
            table.add_row("State", f"[dim]{state}[/dim]")

        table.add_row("Started At", info["started_at"])

        # Only show expiration for running sandboxes
        if state == "running" and info.get("end_at"):
            table.add_row("Expires At", info["end_at"])
            # Calculate time remaining
            from datetime import datetime, timezone
            try:
                end_at = datetime.fromisoformat(info["end_at"])
                now = datetime.now(timezone.utc)
                remaining = end_at - now
                total_mins = int(remaining.total_seconds() / 60)
                if total_mins > 0:
                    hours, mins = divmod(total_mins, 60)
                    if hours > 0:
                        table.add_row("Time Remaining", f"{hours}h {mins}m")
                    else:
                        table.add_row("Time Remaining", f"{mins}m")
                else:
                    table.add_row("Time Remaining", "[red]Expired[/red]")
            except Exception:
                pass
        elif state == "paused":
            table.add_row("Time Remaining", "[yellow]Paused (up to 30 days)[/yellow]")

        if info["metadata"]:
            table.add_row("Metadata", str(info["metadata"]))

        console.print(table)

        # Get and display metrics
        try:
            metrics = sbx_module.get_sandbox_metrics(sandbox_id)
            if metrics:
                # Get the latest metric entry
                latest = metrics[-1]

                metrics_table = Table(title="Resource Metrics (Latest)")
                metrics_table.add_column("Resource", style="cyan")
                metrics_table.add_column("Used", style="yellow", justify="right")
                metrics_table.add_column("Total", style="green", justify="right")
                metrics_table.add_column("Usage", style="magenta", justify="right")

                # CPU
                cpu_pct = f"{latest['cpu_used_pct']:.1f}%"
                metrics_table.add_row(
                    "CPU",
                    cpu_pct,
                    f"{latest['cpu_count']} cores",
                    cpu_pct,
                )

                # Memory - convert to human readable
                mem_used_mb = latest["mem_used"] / (1024 * 1024)
                mem_total_mb = latest["mem_total"] / (1024 * 1024)
                mem_pct = (latest["mem_used"] / latest["mem_total"]) * 100 if latest["mem_total"] > 0 else 0
                metrics_table.add_row(
                    "Memory",
                    f"{mem_used_mb:.1f} MB",
                    f"{mem_total_mb:.1f} MB",
                    f"{mem_pct:.1f}%",
                )

                # Disk - convert to human readable
                disk_used_gb = latest["disk_used"] / (1024 * 1024 * 1024)
                disk_total_gb = latest["disk_total"] / (1024 * 1024 * 1024)
                disk_pct = (latest["disk_used"] / latest["disk_total"]) * 100 if latest["disk_total"] > 0 else 0
                metrics_table.add_row(
                    "Disk",
                    f"{disk_used_gb:.2f} GB",
                    f"{disk_total_gb:.2f} GB",
                    f"{disk_pct:.1f}%",
                )

                console.print(metrics_table)
            else:
                console.print("[dim]Metrics not yet available (sandbox may have just started)[/dim]")
        except Exception as metrics_err:
            console.print(f"[dim]Could not fetch metrics: {metrics_err}[/dim]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@sandbox.command()
@click.argument("sandbox_id")
def pause(sandbox_id):
    """Pause a sandbox (beta)."""
    try:
        console.print(f"[yellow]Pausing sandbox: {sandbox_id}[/yellow]")

        sbx_module.pause_sandbox(sandbox_id)

        console.print(f"[green]✓ Sandbox paused[/green]")
        console.print(f"[dim]Use 'connect' to resume[/dim]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


def _format_duration(seconds: int) -> str:
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        mins = seconds // 60
        return f"{mins}m"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        if mins > 0:
            return f"{hours}h {mins}m"
        return f"{hours}h"


@sandbox.command(name="extend-lifetime")
@click.argument("sandbox_id")
@click.argument("seconds", type=int)
def extend_lifetime(sandbox_id, seconds):
    """Extend sandbox lifetime by adding seconds to remaining time."""
    try:
        console.print(f"[yellow]Extending sandbox {sandbox_id} by {_format_duration(seconds)}...[/yellow]")

        result = sbx_module.extend_sandbox_timeout(sandbox_id, seconds)

        if result.get('hit_max_limit'):
            console.print(f"[yellow]⚠ Hit 24-hour maximum limit![/yellow]")
            console.print(f"[dim]Requested: {_format_duration(result['requested_remaining'])}[/dim]")
            console.print(f"[dim]Actual: {_format_duration(result['new_remaining'])}[/dim]")
            console.print(f"[dim]Max expiration: {result['max_end_at']}[/dim]")
        else:
            console.print(f"[green]✓ Sandbox lifetime extended[/green]")
            console.print(f"[dim]Added: {_format_duration(result['added_seconds'])}[/dim]")
            console.print(f"[dim]Previous remaining: {_format_duration(result['previous_remaining'])}[/dim]")
            console.print(f"[dim]New remaining: {_format_duration(result['new_remaining'])}[/dim]")
            console.print(f"[dim]New expiration: {result['new_end_at']}[/dim]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@sandbox.command()
@click.argument("sandbox_id")
def status(sandbox_id):
    """Check if sandbox is running."""
    try:
        is_running = sbx_module.is_sandbox_running(sandbox_id)

        if is_running:
            console.print(f"[green]✓ Sandbox {sandbox_id} is running[/green]")
        else:
            console.print(f"[red]✗ Sandbox {sandbox_id} is not running[/red]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@sandbox.command(name="get-host")
@click.argument("sandbox_id")
@click.option("--port", "-p", required=True, type=int, help="Port number to expose (e.g., 5173 for Vite)")
def get_host(sandbox_id, port):
    """Get public hostname for an exposed port."""
    try:
        console.print(f"[yellow]Getting public host for port {port}...[/yellow]")

        host = sbx_module.get_host(sandbox_id, port)
        url = f"https://{host}"

        console.print(f"[green]✓ Public URL: {url}[/green]")
        console.print(f"[dim]Sandbox: {sandbox_id}[/dim]")
        console.print(f"[dim]Port: {port}[/dim]")

        # Print just the URL for easy piping
        rprint(url)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@sandbox.command()
@click.option("--limit", "-l", default=20, help="Maximum number of sandboxes to list")
def list(limit):
    """List all running sandboxes."""
    try:
        console.print(f"[yellow]Listing sandboxes (limit: {limit})...[/yellow]")

        sandboxes = sbx_module.list_sandboxes(limit=limit)

        if not sandboxes:
            console.print("[dim]No running sandboxes found[/dim]")
            return

        table = Table(title=f"Sandboxes ({len(sandboxes)})")
        table.add_column("Sandbox ID", style="cyan", no_wrap=True)
        table.add_column("Default Public URL", style="blue", no_wrap=True)
        table.add_column("State", no_wrap=True)
        table.add_column("Template", style="green")
        table.add_column("Started At", style="yellow")
        table.add_column("Metadata", style="dim")

        for sbx in sandboxes:
            metadata_str = str(sbx["metadata"]) if sbx["metadata"] else "-"
            state = sbx.get("state", "unknown")
            if state == "running":
                state_str = "[green]Running[/green]"
            elif state == "paused":
                state_str = "[yellow]Paused[/yellow]"
            else:
                state_str = f"[dim]{state}[/dim]"
            table.add_row(
                sbx["sandbox_id"],
                _build_default_public_url(sbx["sandbox_id"]),
                state_str,
                sbx["template_id"],
                sbx["started_at"],
                metadata_str,
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
