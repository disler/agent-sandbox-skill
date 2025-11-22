"""
Sandbox connection and management module.
Provides helper functions for sandbox lifecycle operations.
"""

from typing import Optional, Dict
from e2b import Sandbox


def get_sandbox(sandbox_id: str, timeout: Optional[int] = None) -> Sandbox:
    """
    Connect to an existing sandbox by ID.

    Args:
        sandbox_id: The sandbox ID to connect to
        timeout: Optional timeout for the sandbox in seconds

    Returns:
        Connected Sandbox instance
    """
    return Sandbox.connect(sandbox_id, timeout=timeout)


def create_sandbox(
    template: Optional[str] = None,
    timeout: Optional[int] = None,
    envs: Optional[Dict[str, str]] = None,
    metadata: Optional[Dict[str, str]] = None,
    auto_pause: bool = False,
) -> Sandbox:
    """
    Create a new sandbox.

    Args:
        template: Sandbox template name or ID
        timeout: Timeout for the sandbox in seconds (default 300)
        envs: Environment variables for the sandbox
        metadata: Custom metadata for the sandbox
        auto_pause: Enable auto-pause (beta feature)

    Returns:
        New Sandbox instance
    """
    if auto_pause:
        return Sandbox.beta_create(
            template=template,
            timeout=timeout,
            envs=envs,
            metadata=metadata,
            auto_pause=True,
        )
    else:
        return Sandbox.create(
            template=template,
            timeout=timeout,
            envs=envs,
            metadata=metadata,
        )


def kill_sandbox(sandbox_id: str) -> bool:
    """
    Kill a sandbox by ID.

    Args:
        sandbox_id: The sandbox ID to kill

    Returns:
        True if sandbox was killed, False if not found
    """
    return Sandbox.kill(sandbox_id)


def get_host(sandbox_id: str, port: int) -> str:
    """
    Get the public hostname for an exposed port.

    Args:
        sandbox_id: The sandbox ID
        port: The port number to expose (e.g., 5173 for Vite)

    Returns:
        Public hostname (e.g., "xxxxx.e2b.app")
    """
    sbx = get_sandbox(sandbox_id)
    host = sbx.get_host(port)
    return host


def pause_sandbox(sandbox_id: str) -> None:
    """
    Pause a sandbox (beta feature).

    Args:
        sandbox_id: The sandbox ID to pause
    """
    Sandbox.beta_pause(sandbox_id)


def get_sandbox_info(sandbox_id: str) -> dict:
    """
    Get sandbox information.

    Args:
        sandbox_id: The sandbox ID to get info for

    Returns:
        Dictionary with sandbox info
    """
    info = Sandbox.get_info(sandbox_id)
    return {
        "sandbox_id": info.sandbox_id,
        "template_id": info.template_id,
        "started_at": str(info.started_at),
        "metadata": info.metadata,
    }


def is_sandbox_running(sandbox_id: str) -> bool:
    """
    Check if a sandbox is running.

    Args:
        sandbox_id: The sandbox ID to check

    Returns:
        True if running, False otherwise
    """
    sbx = get_sandbox(sandbox_id)
    result = sbx.is_running()
    return result


def list_sandboxes(limit: int = 20) -> list:
    """
    List all running sandboxes.

    Args:
        limit: Maximum number of sandboxes to return (default 20)

    Returns:
        List of dictionaries with sandbox info
    """
    paginator = Sandbox.list()
    sandboxes = paginator.next_items()

    # Limit the results
    sandboxes = sandboxes[:limit]

    return [
        {
            "sandbox_id": sbx.sandbox_id,
            "template_id": sbx.template_id,
            "started_at": str(sbx.started_at),
            "metadata": sbx.metadata,
        }
        for sbx in sandboxes
    ]
