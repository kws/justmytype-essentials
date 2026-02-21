"""Deterministic copy of directory trees (for assembling pack fonts from cache)."""

from __future__ import annotations

import shutil
from pathlib import Path


def copy_tree(src: Path, dest: Path) -> None:
    """Copy directory tree from src to dest, preserving structure.

    dest must not exist or must be an empty directory; existing files are overwritten.
    Copy is deterministic (sorted iteration).
    """
    src = Path(src).resolve()
    dest = Path(dest).resolve()
    if not src.is_dir():
        raise NotADirectoryError(str(src))
    dest.mkdir(parents=True, exist_ok=True)
    for item in sorted(src.iterdir()):
        dest_item = dest / item.name
        if item.is_dir():
            copy_tree(item, dest_item)
        else:
            shutil.copy2(item, dest_item)
