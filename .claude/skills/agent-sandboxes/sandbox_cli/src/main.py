"""
E2B Sandbox CLI - Main entry point.

A comprehensive CLI for managing E2B sandboxes and performing operations.
"""

import click
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables
# Path from src/main.py: src -> sandbox_cli -> agent-sandboxes -> skills -> .claude -> root (6 levels)
root_dir = Path(__file__).parent.parent.parent.parent.parent.parent
load_dotenv(root_dir / ".env")

# Import command groups
from .commands.sandbox import sandbox
from .commands.files import files
from .commands.exec import exec
from .commands.browser import browser

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    E2B Sandbox CLI - Control sandboxes from the command line.

    This CLI provides comprehensive sandbox management capabilities:
    - Create, connect to, and manage sandboxes (sandbox)
    - Perform file operations with SDK APIs (files)
    - Execute any command with full control (exec)
    - Browser automation for UI validation (browser)

    Most commands require a SANDBOX_ID. You can get one by:
    1. Creating a new sandbox: sbx init
    2. Or: sbx sandbox create

    Tip: For multi-agent workflows, capture the sandbox ID in your context
    and use it directly in commands (avoid shell variables for safety).
    """
    pass


# Add command groups
cli.add_command(sandbox)
cli.add_command(files)
cli.add_command(exec)
cli.add_command(browser)


# Add an init command for quick sandbox setup
@cli.command()
@click.option(
    "--template",
    "-t",
    default=None,
    help="Sandbox template name or ID",
)
@click.option(
    "--timeout", default=600, help="Sandbox timeout in seconds (default: 10 minutes)"
)
@click.option("--env", "-e", multiple=True, help="Environment variables (KEY=VALUE)")
@click.option("--name", "-n", default=None, help="Sandbox name (stored in metadata)")
def init(template, timeout, env, name):
    """
    Initialize a new sandbox and display the ID.

    Creates a new sandbox and outputs the sandbox ID. Capture the ID
    from the output and store it in your context for subsequent commands.

    Templates:
        Use --template to specify a pre-built template with tools installed.

    Examples:
        sbx init
        sbx init --template fullstack-vue-fastapi-node22 --timeout 43200 --name my-workflow
    """
    try:
        from .modules import sandbox as sbx_module

        console.print("[yellow]Initializing new sandbox...[/yellow]")
        if template:
            console.print(f"[dim]Template: {template}[/dim]")

        # Parse env vars
        envs = {}
        for e in env:
            if "=" in e:
                key, value = e.split("=", 1)
                envs[key] = value

        # Add name to metadata if provided
        metadata = {}
        if name:
            metadata["name"] = name

        sbx = sbx_module.create_sandbox(
            template=template,
            timeout=timeout,
            envs=envs if envs else None,
            metadata=metadata if metadata else None,
        )

        console.print(f"\n[green]✓ Sandbox created successfully![/green]")
        console.print(f"\n[cyan]Sandbox ID:[/cyan] {sbx.sandbox_id}")
        if name:
            console.print(f"[cyan]Name:[/cyan] {name}")
        if template:
            console.print(f"[dim]Template: {template}[/dim]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


if __name__ == "__main__":
    cli()
