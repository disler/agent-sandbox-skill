"""
File operations module for sandbox filesystem.
Provides helper functions for file management.
"""

from typing import List, Optional, Dict
from e2b import Sandbox


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
        result.append({
            "name": f.name,
            "path": f.path,
            "type": f.type.value,
            "size": f.size,
            "permissions": f.permissions,
        })

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
