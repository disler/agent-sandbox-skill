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
        table.add_row("Template", info["template_id"])
        table.add_row("Started At", info["started_at"])

        if info["metadata"]:
            table.add_row("Metadata", str(info["metadata"]))

        console.print(table)

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

        table = Table(title=f"Running Sandboxes ({len(sandboxes)})")
        table.add_column("Sandbox ID", style="cyan", no_wrap=True)
        table.add_column("Template", style="green")
        table.add_column("Started At", style="yellow")
        table.add_column("Metadata", style="dim")

        for sbx in sandboxes:
            metadata_str = str(sbx["metadata"]) if sbx["metadata"] else "-"
            table.add_row(
                sbx["sandbox_id"],
                sbx["template_id"],
                sbx["started_at"],
                metadata_str,
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
