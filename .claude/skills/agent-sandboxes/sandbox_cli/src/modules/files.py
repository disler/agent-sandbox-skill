"""
File operations module for sandbox filesystem.
Provides helper functions for file management.
"""

from typing import List, Optional, Dict
from e2b import Sandbox


# Default directories to exclude when downloading/uploading
DEFAULT_EXCLUDE_DIRS = {
    # Python
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    # Astral uv
    ".uv",
    # Node/npm
    "node_modules",
    ".npm",
    # Bun
    ".bun",
    # Build outputs
    "dist",
    "build",
    # Frontend frameworks
    ".next",
    ".nuxt",
    ".output",
    ".turbo",
    ".parcel-cache",
    ".svelte-kit",
    # Testing/coverage
    "coverage",
    ".nyc_output",
    # General
    ".git",
    ".cache",
}


def list_files(sandbox_id: str, path: str = "/", depth: int = 1) -> List[Dict]:
    """
    List files in a directory.

    Args:
        sandbox_id: The sandbox ID
        path: Path to list
        depth: Depth to traverse

    Returns:
        List of file info dictionaries
    """
    sbx = Sandbox.connect(sandbox_id)
    files = sbx.files.list(path, depth=depth)

    result = []
    for f in files:
        result.append(
            {
                "name": f.name,
                "path": f.path,
                "type": f.type.value,
                "size": f.size,
                "permissions": f.permissions,
            }
        )

    return result


def read_file(sandbox_id: str, path: str) -> str:
    """
    Read a file from the sandbox.

    Args:
        sandbox_id: The sandbox ID
        path: Path to the file

    Returns:
        File content as string
    """
    sbx = Sandbox.connect(sandbox_id)
    content = sbx.files.read(path)
    return content


def write_file(sandbox_id: str, path: str, content: str) -> Dict:
    """
    Write a file to the sandbox.

    Args:
        sandbox_id: The sandbox ID
        path: Path to write to
        content: Content to write

    Returns:
        Write info dictionary
    """
    sbx = Sandbox.connect(sandbox_id)
    info = sbx.files.write(path, content)

    return {
        "path": info.path,
    }


def file_exists(sandbox_id: str, path: str) -> bool:
    """
    Check if a file or directory exists.

    Args:
        sandbox_id: The sandbox ID
        path: Path to check

    Returns:
        True if exists, False otherwise
    """
    sbx = Sandbox.connect(sandbox_id)
    exists = sbx.files.exists(path)
    return exists


def get_file_info(sandbox_id: str, path: str) -> Dict:
    """
    Get information about a file or directory.

    Args:
        sandbox_id: The sandbox ID
        path: Path to get info for

    Returns:
        File info dictionary
    """
    sbx = Sandbox.connect(sandbox_id)
    info = sbx.files.get_info(path)

    return {
        "name": info.name,
        "path": info.path,
        "type": info.type.value,
        "size": info.size,
        "permissions": info.permissions,
    }


def remove_file(sandbox_id: str, path: str) -> None:
    """
    Remove a file or directory.

    Args:
        sandbox_id: The sandbox ID
        path: Path to remove
    """
    sbx = Sandbox.connect(sandbox_id)
    sbx.files.remove(path)


def make_directory(sandbox_id: str, path: str) -> bool:
    """
    Create a directory.

    Args:
        sandbox_id: The sandbox ID
        path: Path to create

    Returns:
        True if created, False if already exists
    """
    sbx = Sandbox.connect(sandbox_id)
    created = sbx.files.make_dir(path)
    return created


def rename_file(sandbox_id: str, old_path: str, new_path: str) -> Dict:
    """
    Rename a file or directory.

    Args:
        sandbox_id: The sandbox ID
        old_path: Current path
        new_path: New path

    Returns:
        Info about renamed file
    """
    sbx = Sandbox.connect(sandbox_id)
    info = sbx.files.rename(old_path, new_path)

    return {
        "name": info.name,
        "path": info.path,
        "type": info.type.value,
    }


def read_file_bytes(sandbox_id: str, path: str) -> bytearray:
    """
    Read a file as binary data from the sandbox.

    Args:
        sandbox_id: The sandbox ID
        path: Path to the file

    Returns:
        File content as bytearray
    """
    sbx = Sandbox.connect(sandbox_id)
    content = sbx.files.read(path, format="bytes")
    return content


def write_file_bytes(sandbox_id: str, path: str, data: bytes) -> Dict:
    """
    Write binary data to a file in the sandbox.

    Args:
        sandbox_id: The sandbox ID
        path: Path to write to
        data: Binary data to write

    Returns:
        Write info dictionary
    """
    sbx = Sandbox.connect(sandbox_id)
    info = sbx.files.write(path, data)

    return {
        "path": info.path,
    }


def download_directory(
    sandbox_id: str,
    remote_path: str,
    local_path: str,
    max_depth: int = 10,
    exclude: Optional[List[str]] = None,
    include_all: bool = False,
) -> Dict:
    """
    Recursively download a directory from the sandbox to local filesystem.

    Args:
        sandbox_id: The sandbox ID
        remote_path: Remote directory path to download
        local_path: Local directory path to save to
        max_depth: Maximum recursion depth (default 10)
        exclude: Additional directory names to exclude
        include_all: If True, don't exclude any directories (download everything)

    Returns:
        Dictionary with download statistics
    """
    from pathlib import Path

    sbx = Sandbox.connect(sandbox_id)
    local_base = Path(local_path)
    remote_base = remote_path.rstrip("/")

    # Build exclusion set
    if include_all:
        exclude_set = set()
    else:
        exclude_set = DEFAULT_EXCLUDE_DIRS.copy()
        if exclude:
            exclude_set.update(exclude)

    stats = {
        "files_downloaded": 0,
        "directories_created": 0,
        "total_bytes": 0,
        "skipped_dirs": [],
        "errors": [],
        "files": [],
    }

    def process_directory(remote_dir: str, local_dir: Path, depth: int = 0):
        if depth > max_depth:
            stats["errors"].append(f"Max depth exceeded at {remote_dir}")
            return

        local_dir.mkdir(parents=True, exist_ok=True)
        stats["directories_created"] += 1

        try:
            items = sbx.files.list(remote_dir)
        except Exception as e:
            stats["errors"].append(f"Failed to list {remote_dir}: {e}")
            return

        for item in items:
            item_remote_path = item.path
            rel_path = item_remote_path[len(remote_base) :].lstrip("/")
            item_local_path = (
                local_base / rel_path if rel_path else local_dir / item.name
            )

            if item.type.value == "dir":
                if item.name in exclude_set:
                    stats["skipped_dirs"].append(item_remote_path)
                    continue
                process_directory(item_remote_path, item_local_path, depth + 1)
            else:
                try:
                    data = sbx.files.read(item_remote_path, format="bytes")
                    item_local_path.parent.mkdir(parents=True, exist_ok=True)
                    item_local_path.write_bytes(data)
                    stats["files_downloaded"] += 1
                    stats["total_bytes"] += len(data)
                    stats["files"].append(str(item_local_path))
                except Exception as e:
                    stats["errors"].append(
                        f"Failed to download {item_remote_path}: {e}"
                    )

    process_directory(remote_base, local_base)
    return stats


def edit_file(
    sandbox_id: str,
    path: str,
    old_string: str,
    new_string: str,
    replace_all: bool = False,
) -> Dict:
    """
    Edit a file by replacing a string.

    Args:
        sandbox_id: The sandbox ID
        path: Path to the file
        old_string: String to find and replace
        new_string: Replacement string
        replace_all: If True, replace all occurrences; otherwise just the first

    Returns:
        Dictionary with edit info including replacement count
    """
    sbx = Sandbox.connect(sandbox_id)

    # Read current content
    content = sbx.files.read(path)

    # Check if old_string exists
    if old_string not in content:
        raise ValueError(f"String not found in file: {old_string[:50]}...")

    # Count occurrences
    count = content.count(old_string)

    # Perform replacement
    if replace_all:
        new_content = content.replace(old_string, new_string)
        replacements = count
    else:
        new_content = content.replace(old_string, new_string, 1)
        replacements = 1

    # Write back
    info = sbx.files.write(path, new_content)

    return {
        "path": info.path,
        "replacements": replacements,
        "total_occurrences": count,
    }


def upload_directory(
    sandbox_id: str,
    local_path: str,
    remote_path: str,
    max_depth: int = 10,
    exclude: Optional[List[str]] = None,
    include_all: bool = False,
) -> Dict:
    """
    Recursively upload a directory from local filesystem to the sandbox.

    Args:
        sandbox_id: The sandbox ID
        local_path: Local directory path to upload
        remote_path: Remote directory path to save to
        max_depth: Maximum recursion depth (default 10)
        exclude: Additional directory names to exclude
        include_all: If True, don't exclude any directories (upload everything)

    Returns:
        Dictionary with upload statistics
    """
    from pathlib import Path

    sbx = Sandbox.connect(sandbox_id)
    local_base = Path(local_path)
    remote_base = remote_path.rstrip("/")

    if not local_base.exists():
        raise FileNotFoundError(f"Local path does not exist: {local_path}")
    if not local_base.is_dir():
        raise NotADirectoryError(f"Local path is not a directory: {local_path}")

    # Build exclusion set
    if include_all:
        exclude_set = set()
    else:
        exclude_set = DEFAULT_EXCLUDE_DIRS.copy()
        if exclude:
            exclude_set.update(exclude)

    stats = {
        "files_uploaded": 0,
        "directories_created": 0,
        "total_bytes": 0,
        "skipped_dirs": [],
        "errors": [],
        "files": [],
    }

    def process_directory(local_dir: Path, remote_dir: str, depth: int = 0):
        if depth > max_depth:
            stats["errors"].append(f"Max depth exceeded at {local_dir}")
            return

        # Create remote directory
        try:
            sbx.files.make_dir(remote_dir)
            stats["directories_created"] += 1
        except Exception:
            pass  # Directory may already exist

        for item in local_dir.iterdir():
            rel_path = item.relative_to(local_base)
            item_remote_path = f"{remote_base}/{rel_path}".replace("\\", "/")

            if item.is_dir():
                if item.name in exclude_set:
                    stats["skipped_dirs"].append(str(item))
                    continue
                process_directory(item, item_remote_path, depth + 1)
            else:
                try:
                    data = item.read_bytes()
                    sbx.files.write(item_remote_path, data)
                    stats["files_uploaded"] += 1
                    stats["total_bytes"] += len(data)
                    stats["files"].append(item_remote_path)
                except Exception as e:
                    stats["errors"].append(f"Failed to upload {item}: {e}")

    process_directory(local_base, remote_base)
    return stats
