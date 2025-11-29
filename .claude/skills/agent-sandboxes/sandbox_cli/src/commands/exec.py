"""
Advanced command execution with full E2B SDK features.
"""

import click
from rich.console import Console
from ..modules import commands as cmd_module

console = Console()


@click.command()
@click.argument("sandbox_id")
@click.argument("command")
@click.option("--cwd", default=None, help="Working directory")
@click.option("--user", default=None, help="Run as specific user (e.g., 'user', 'root')")
@click.option("--root", is_flag=True, help="Run as root user (shortcut for --user root)")
@click.option("--shell", is_flag=True, help="Execute in shell context (enables pipes, redirections, wildcards)")
@click.option("--env", "-e", multiple=True, help="Environment variables (KEY=VALUE)")
@click.option("--timeout", default=60, type=int, help="Command timeout in seconds (0 for unlimited)")
@click.option("--background", is_flag=True, help="Run in background")
@click.option("--stdin", is_flag=True, help="Enable stdin for the command")
def exec(sandbox_id, command, cwd, user, root, shell, env, timeout, background, stdin):
    r"""
    Execute a command with full control over execution environment.

    This is the most powerful command execution tool, supporting:
    - Custom working directory (--cwd)
    - User selection (--user or --root flag)
    - Shell context for pipes/redirections (--shell)
    - Environment variables (--env)
    - Background execution (--background)
    - Stdin support (--stdin)
    - Timeout control (--timeout)

    Examples:
        # Basic execution
        sbx exec $SANDBOX_ID "python --version"

        # Run as root
        sbx exec $SANDBOX_ID "apt-get update" --root

        # With custom environment
        sbx exec $SANDBOX_ID "echo \$VAR" --env VAR=value

        # In specific directory
        sbx exec $SANDBOX_ID "pwd" --cwd /home/user/project

        # Shell features (pipes, redirections)
        sbx exec $SANDBOX_ID "ps aux | grep python" --shell

        # Background with no timeout
        sbx exec $SANDBOX_ID "long-running-task" --background --timeout 0

        # Complex privileged operation
        sbx exec $SANDBOX_ID "apt-get update && apt-get install -y nginx" --root --timeout 300
    """
    try:
        # Handle --root flag
        if root:
            user = "root"

        # Parse env vars
        envs = {}
        for e in env:
            if "=" in e:
                key, value = e.split("=", 1)
                envs[key] = value

        # Wrap in shell if requested
        actual_command = command
        if shell:
            actual_command = f'/bin/bash -c "{command}"'
            console.print(f"[yellow]Executing shell command: {command}[/yellow]")
        else:
            console.print(f"[yellow]Executing: {command}[/yellow]")

        if user:
            console.print(f"[dim]User: {user}[/dim]")
        if cwd:
            console.print(f"[dim]Working directory: {cwd}[/dim]")
        if envs:
            console.print(f"[dim]Environment: {', '.join(f'{k}={v}' for k, v in envs.items())}[/dim]")
        if stdin:
            console.print(f"[dim]Stdin: enabled[/dim]")

        if background:
            result = cmd_module.run_command_background(
                sandbox_id,
                actual_command,
                cwd=cwd,
                envs=envs if envs else None,
                timeout=timeout if timeout > 0 else None,
            )
            console.print(f"\n[green]✓ Background command started[/green]")
            console.print(f"[cyan]PID: {result['pid']}[/cyan]")
            console.print(f"[dim]Process is running in background[/dim]")
            return  # Exit early for background commands
        else:
            result = cmd_module.run_command(
                sandbox_id,
                actual_command,
                cwd=cwd,
                envs=envs if envs else None,
                timeout=timeout if timeout > 0 else None,
            )
            console.print(f"\n[cyan]Exit code: {result['exit_code']}[/cyan]")

        if result["stdout"]:
            console.print("\n[green]STDOUT:[/green]")
            console.print(result["stdout"], markup=False)

        if result["stderr"]:
            console.print("\n[red]STDERR:[/red]")
            console.print(result["stderr"], markup=False)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
