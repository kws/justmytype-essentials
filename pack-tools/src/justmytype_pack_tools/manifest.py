"""Manifest generation for font packs.

Produces pack_manifest.json per the schema in justmytype/docs/manifest.md.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from justmytype.parser import parse_font_metadata

# Font file extensions to include in manifest
FONT_EXTENSIONS = {".ttf", ".otf", ".ttc", ".woff", ".woff2"}


def get_build_timestamp() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(block)
    return sha256_hash.hexdigest()


def _find_font_files(directory: Path) -> Iterator[Path]:
    """Recursively find font files under directory."""
    if not directory.exists():
        return
    try:
        for item in sorted(directory.iterdir()):
            try:
                if item.is_dir():
                    yield from _find_font_files(item)
                elif item.suffix.lower() in FONT_EXTENSIONS:
                    yield item
            except OSError:
                continue
    except OSError:
        return


@dataclass(frozen=True, slots=True)
class ManifestPackConfig:
    """Pack section of manifest."""

    name: str
    version: str
    entry_point: str
    priority: int
    description: str = ""
    source_url: str = ""
    package_dir: str = ""  # optional; when set, pack-tools uses src/{package_dir}/fonts
    display_name: str = ""  # optional; short human title (README H1); else humanize(name)


@dataclass(frozen=True, slots=True)
class ManifestSourceConfig:
    """Source section of manifest."""

    repo: str
    ref: str
    archive_sha256: str = ""


@dataclass(frozen=True, slots=True)
class ManifestLicenseConfig:
    """Single license entry."""

    spdx: str
    path: str


def generate_manifest(
    output_path: Path,
    pack: ManifestPackConfig,
    source: ManifestSourceConfig,
    families: list[str],
    font_root: Path,
    licenses: list[ManifestLicenseConfig],
    tool_version: str = "0.1.0",
    include_timestamp: bool = False,
) -> dict[str, Any]:
    """Generate pack_manifest.json for a font pack.

    Scans font_root for font files, extracts metadata with fonttools, and writes
    the manifest to output_path. Per-file entries use path relative to font_root.

    Args:
        output_path: Where to write pack_manifest.json.
        pack: Pack identity and metadata.
        source: Upstream repo and ref.
        families: Logical family paths from upstream (e.g. ["ofl/inter", "ofl/notosans"]).
        font_root: Directory containing font files (searched recursively).
        licenses: License entries (spdx + path in pack).
        tool_version: Version of pack-tools that produced this manifest.
        include_timestamp: If True, include build.timestamp for provenance; default False for deterministic output.

    Returns:
        The manifest dict (also written to output_path).
    """
    timestamp = get_build_timestamp() if include_timestamp else None
    font_entries: list[dict[str, Any]] = []
    seen_families: set[str] = set()

    for font_path in _find_font_files(font_root):
        try:
            rel_path = font_path.relative_to(font_root)
        except ValueError:
            continue
        path_str = str(rel_path).replace("\\", "/")
        sha256 = compute_sha256(font_path)
        meta = parse_font_metadata(font_path)
        if meta is None:
            font_entries.append(
                {
                    "path": path_str,
                    "sha256": sha256,
                    "family": "",
                    "style": "normal",
                    "weight": None,
                    "width": None,
                    "postscript_name": None,
                    "variant": None,
                }
            )
            continue
        seen_families.add(meta["family"])
        font_entries.append(
            {
                "path": path_str,
                "sha256": sha256,
                "family": meta["family"],
                "style": meta["style"],
                "weight": meta["weight"],
                "width": meta["width"],
                "postscript_name": meta["postscript_name"],
                "variant": meta.get("variant"),
            }
        )

    manifest = {
        "manifest_version": "1.0",
        "pack": {
            "name": pack.name,
            "version": pack.version,
            "entry_point": pack.entry_point,
            "priority": pack.priority,
        },
        "source": {
            "repo": source.repo,
            "ref": source.ref,
        },
        "build": {
            "tool_version": tool_version,
            **({"timestamp": timestamp} if timestamp is not None else {}),
        },
        "families": families,
        "fonts": font_entries,
        "licenses": [{"spdx": lic.spdx, "path": lic.path} for lic in licenses],
    }

    if pack.description:
        manifest["pack"]["description"] = pack.description
    if pack.source_url:
        manifest["pack"]["source_url"] = pack.source_url
    if (pack.display_name or "").strip():
        manifest["pack"]["display_name"] = pack.display_name.strip()
    if source.archive_sha256:
        manifest["source"]["archive_sha256"] = source.archive_sha256

    manifest["family_count"] = len(seen_families)
    manifest["font_file_count"] = len(font_entries)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest
