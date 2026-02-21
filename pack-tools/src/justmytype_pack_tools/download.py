"""Download font family trees from GitHub (e.g. google/fonts) with caching."""

from __future__ import annotations

from pathlib import Path

from justmytype_pack_tools.github_api import (
    _parse_repo_url,
    download_file,
    list_directory_recursive,
)


def get_github_token() -> str | None:
    """Return GITHUB_TOKEN from environment if set."""
    import os
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def download_family_tree(
    repo_url: str,
    ref: str,
    family_path: str,
    cache_dir: Path,
    token: str | None = None,
) -> Path:
    """Download a single family directory from a GitHub repo at ref into cache.

    Uses GitHub Contents API recursively. Cache layout: cache_dir / ref / family_path / ...
    (e.g. cache/google_fonts/abc123/ofl/inter/Inter-Regular.ttf).

    Args:
        repo_url: Repo URL (e.g. https://github.com/google/fonts).
        ref: Git ref (commit SHA, branch, or tag).
        family_path: Path relative to repo root (e.g. ofl/inter).
        cache_dir: Root cache directory.
        token: Optional GitHub token for higher rate limits.

    Returns:
        Path to the downloaded family directory inside cache (cache_dir / ref / family_path).
    """
    owner, repo = _parse_repo_url(repo_url)
    token = token or get_github_token()
    family_path = family_path.strip("/")
    out_root = cache_dir / ref / family_path
    out_root.mkdir(parents=True, exist_ok=True)
    entries = list_directory_recursive(owner, repo, family_path, ref, token=token)
    for entry in entries:
        if not entry.download_url:
            continue
        # entry.path is e.g. "ofl/inter/Inter-Regular.ttf"; we want relative to family_path
        if entry.path.startswith(family_path + "/"):
            rel = entry.path[len(family_path) + 1 :]
        else:
            rel = entry.path
        dest = out_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        download_file(entry.download_url, dest, token=token)
    return out_root
