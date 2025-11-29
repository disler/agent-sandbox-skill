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


def extend_sandbox_timeout(sandbox_id: str, additional_seconds: int) -> dict:
    """
    Extend sandbox timeout by adding time to the remaining lifetime.

    Args:
        sandbox_id: The sandbox ID to extend
        additional_seconds: Seconds to add to remaining time

    Returns:
        Dictionary with old_end_at, new_end_at, added_seconds, and hit_max_limit flag
    """
    from datetime import datetime, timezone, timedelta

    MAX_LIFETIME_SECONDS = 86400  # 24 hours - E2B Pro limit

    # Get current info
    info = Sandbox.get_info(sandbox_id)
    old_end_at = info.end_at
    started_at = info.started_at

    # Calculate time since start (to check against 24h limit)
    now = datetime.now(timezone.utc)
    time_since_start = (now - started_at).total_seconds()

    # Calculate remaining seconds
    remaining = (old_end_at - now).total_seconds()
    remaining = max(0, remaining)  # Don't go negative

    # Calculate new total timeout (what we want)
    requested_timeout = int(remaining + additional_seconds)

    # Check if we're already at max lifetime
    max_end_at = started_at + timedelta(seconds=MAX_LIFETIME_SECONDS)
    time_until_max = (max_end_at - now).total_seconds()
    time_until_max = max(0, time_until_max)

    # Cap the timeout at the maximum allowed
    actual_timeout = min(requested_timeout, int(time_until_max))
    hit_max_limit = requested_timeout > time_until_max

    # Set the new timeout
    sbx = get_sandbox(sandbox_id)
    sbx.set_timeout(actual_timeout)

    # Get updated info to verify
    updated_info = Sandbox.get_info(sandbox_id)
    actual_new_remaining = (updated_info.end_at - datetime.now(timezone.utc)).total_seconds()

    return {
        "old_end_at": str(old_end_at),
        "new_end_at": str(updated_info.end_at),
        "added_seconds": additional_seconds,
        "previous_remaining": int(remaining),
        "new_remaining": int(actual_new_remaining),
        "requested_remaining": requested_timeout,
        "hit_max_limit": hit_max_limit,
        "max_end_at": str(max_end_at),
    }


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
        "state": info.state,
        "started_at": str(info.started_at),
        "end_at": str(info.end_at) if info.end_at else None,
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


def get_sandbox_metrics(sandbox_id: str) -> list:
    """
    Get sandbox resource metrics.

    Args:
        sandbox_id: The sandbox ID to get metrics for

    Returns:
        List of metric entries (may be empty if sandbox just started)
    """
    metrics = Sandbox.get_metrics(sandbox_id)

    return [
        {
            "timestamp": str(m.timestamp),
            "cpu_count": m.cpu_count,
            "cpu_used_pct": m.cpu_used_pct,
            "mem_used": m.mem_used,
            "mem_total": m.mem_total,
            "disk_used": m.disk_used,
            "disk_total": m.disk_total,
        }
        for m in metrics
    ]


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
            "state": sbx.state,
            "started_at": str(sbx.started_at),
            "metadata": sbx.metadata,
        }
        for sbx in sandboxes
    ]
