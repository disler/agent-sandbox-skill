"""
Command execution module for sandbox.
Provides helper functions for running commands.
"""

from typing import Optional, Dict, List
from e2b import Sandbox


def run_command(
    sandbox_id: str,
    cmd: str,
    cwd: Optional[str] = None,
    envs: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = 60,
) -> Dict:
    """
    Run a command in the sandbox and wait for it to complete.

    Args:
        sandbox_id: The sandbox ID
        cmd: Command to execute
        cwd: Working directory
        envs: Environment variables
        timeout: Command timeout in seconds

    Returns:
        Command result dictionary with stdout, stderr, exit_code
    """
    sbx = Sandbox.connect(sandbox_id)
    result = sbx.commands.run(cmd, cwd=cwd, envs=envs, timeout=timeout)

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.exit_code,
    }


def run_command_background(
    sandbox_id: str,
    cmd: str,
    cwd: Optional[str] = None,
    envs: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = 60,
) -> Dict:
    """
    Run a command in the background and return immediately.

    Args:
        sandbox_id: The sandbox ID
        cmd: Command to execute
        cwd: Working directory
        envs: Environment variables
        timeout: Command timeout in seconds

    Returns:
        Dictionary with pid (process starts immediately, does not wait)
    """
    sbx = Sandbox.connect(sandbox_id)
    handle = sbx.commands.run(cmd, background=True, cwd=cwd, envs=envs, timeout=timeout)
    pid = handle.pid

    # Do NOT wait - return immediately for true background execution
    return {
        "pid": pid,
        "stdout": "",
        "stderr": "",
        "exit_code": -1,  # -1 indicates process is still running
    }


def list_processes(sandbox_id: str) -> List[Dict]:
    """
    List all running processes in the sandbox.

    Args:
        sandbox_id: The sandbox ID

    Returns:
        List of process info dictionaries
    """
    sbx = Sandbox.connect(sandbox_id)
    processes = sbx.commands.list()

    result = []
    for proc in processes:
        result.append({
            "pid": proc.pid,
        })

    return result


def kill_process(sandbox_id: str, pid: int) -> bool:
    """
    Kill a process by PID.

    Args:
        sandbox_id: The sandbox ID
        pid: Process ID to kill

    Returns:
        True if killed, False if not found
    """
    sbx = Sandbox.connect(sandbox_id)
    killed = sbx.commands.kill(pid)
    return killed
