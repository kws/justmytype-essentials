"""Thin HTTP helpers for GitHub API (Contents and file download)."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True, slots=True)
class ContentEntry:
    """Single entry from GitHub Contents API."""

    path: str
    type: str  # "file" | "dir"
    sha: str
    download_url: str | None = None
    size: int = 0


def _parse_repo_url(repo_url: str) -> tuple[str, str]:
    """Extract owner and repo from URL like https://github.com/owner/repo."""
    repo_url = repo_url.rstrip("/")
    if "/github.com/" in repo_url:
        parts = repo_url.split("/github.com/")[-1].split("/")
        if len(parts) >= 2:
            return parts[0], parts[1].replace(".git", "")
    if repo_url.startswith("https://github.com/") or repo_url.startswith("http://github.com/"):
        parts = repo_url.replace("http://github.com/", "").replace("https://github.com/", "").split("/")
        if len(parts) >= 2:
            return parts[0], parts[1].replace(".git", "")
    raise ValueError(f"Cannot parse owner/repo from: {repo_url}")


def _api_request(url: str, token: str | None = None) -> bytes:
    """GET URL with optional Authorization. Raises on 4xx/5xx."""
    headers: dict[str, str] = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers, method="GET")
    for attempt in range(3):
        try:
            with urlopen(req, timeout=30) as resp:
                return resp.read()
        except HTTPError as e:
            if e.code == 403 and "rate limit" in (e.reason or "").lower():
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
            raise
        except URLError:
            if attempt < 2:
                time.sleep(1)
                continue
            raise
    raise RuntimeError("Unreachable")


def list_directory(owner: str, repo: str, path: str, ref: str, token: str | None = None) -> list[ContentEntry]:
    """List contents of a directory in the repo at the given ref.

    path is relative to repo root (e.g. "ofl/inter").
    """
    path = path.strip("/") or ""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}"
    data = _api_request(url, token=token)
    raw = json.loads(data.decode("utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"Expected list of contents for {path}, got {type(raw).__name__}")
    entries = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = item.get("name") or ""
        entry_path = f"{path}/{name}" if path else name
        entries.append(
            ContentEntry(
                path=entry_path,
                type=item.get("type", "file"),
                sha=item.get("sha", ""),
                download_url=item.get("download_url"),
                size=int(item.get("size") or 0),
            )
        )
    return entries


def list_directory_recursive(owner: str, repo: str, path: str, ref: str, token: str | None = None) -> list[ContentEntry]:
    """Recursively list all files under path (directory). Returns only files, with download_url set."""
    path = path.strip("/") or ""
    result: list[ContentEntry] = []
    stack = [path] if path else [""]
    while stack:
        current = stack.pop()
        entries = list_directory(owner, repo, current, ref, token=token)
        for entry in entries:
            if entry.type == "dir":
                stack.append(entry.path)
            else:
                result.append(entry)
    return result


def download_file(download_url: str, dest: Path, token: str | None = None) -> None:
    """Download a single file from GitHub raw/download URL to dest."""
    if not isinstance(dest, Path):
        dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(download_url, headers=headers, method="GET")
    with urlopen(req, timeout=60) as resp:
        data = resp.read()
    dest.write_bytes(data)
