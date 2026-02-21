"""Orchestration API for pack-tools. Single implementation of fetch/build/manifest flow.

Other tools can call run_fetch, run_build, run_manifest (or run individual stages)
without duplicating logic. CLI delegates to these functions.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from justmytype_pack_tools.config import load_pack_config
from justmytype_pack_tools.download import download_family_tree, get_github_token
from justmytype_pack_tools.filesystem import copy_tree
from justmytype_pack_tools.licenses import resolve_licenses
from justmytype_pack_tools.manifest import (
    ManifestLicenseConfig,
    ManifestPackConfig,
    ManifestSourceConfig,
    generate_manifest,
)
from justmytype_pack_tools.readme import generate_readme


def resolve_font_root(pack_dir: Path, pack: ManifestPackConfig) -> Path:
    """Resolve fonts directory: pack_dir/src/{package_dir or justmytype_*}/fonts."""
    src = pack_dir / "src"
    if not src.exists():
        raise FileNotFoundError(f"src/ not found in {pack_dir}")
    if pack.package_dir:
        return src / pack.package_dir / "fonts"
    candidates = [d for d in src.iterdir() if d.is_dir() and d.name.startswith("justmytype_")]
    if not candidates:
        raise FileNotFoundError(f"no justmytype_* directory in {src}")
    return candidates[0] / "fonts"


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FetchRequest:
    """Parameters for run_fetch."""

    pack_dir: Path
    cache_dir: Path | None = None  # default: pack_dir/cache
    on_family: Callable[[str], None] | None = None  # optional progress callback per family


@dataclass(frozen=True, slots=True)
class FetchResult:
    """Result of run_fetch."""

    cache_root: Path
    families: list[str]


def run_fetch(request: FetchRequest) -> FetchResult:
    """Fetch font families from upstream (GitHub) into cache.

    Reads families and source from pack_dir/upstream.toml. source.ref is required.
    Raises ValueError on config errors; FileNotFoundError if upstream.toml missing.
    """
    upstream_toml = request.pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        raise FileNotFoundError(f"upstream.toml not found in {request.pack_dir}")
    pack, source, families, _, _ = load_pack_config(upstream_toml, require_ref=True)
    if not source.repo:
        raise ValueError("source.repo is required in upstream.toml")
    cache_root = request.cache_dir or (request.pack_dir / "cache")
    cache_root.mkdir(parents=True, exist_ok=True)
    token = get_github_token()
    for family_path in families:
        if request.on_family is not None:
            request.on_family(family_path)
        download_family_tree(
            repo_url=source.repo,
            ref=source.ref,
            family_path=family_path,
            cache_dir=cache_root,
            token=token,
        )
    return FetchResult(cache_root=cache_root, families=families)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BuildRequest:
    """Parameters for run_build."""

    pack_dir: Path
    cache_dir: Path | None = None  # default: pack_dir/cache
    tool_version: str = "0.1.0"
    generate_manifest: bool = True
    generate_readme: bool = True
    include_timestamp: bool = False  # if True, manifest gets build.timestamp (for provenance)


@dataclass(frozen=True, slots=True)
class BuildResult:
    """Result of run_build."""

    font_root: Path
    manifest_path: Path | None  # set if generate_manifest was True
    readme_path: Path | None  # set if generate_readme was True
    licenses: list[ManifestLicenseConfig]


def run_build(request: BuildRequest) -> BuildResult:
    """Copy fetched families from cache into pack fonts dir; optionally generate manifest and README.

    Resolves licenses (auto-detect + allowlist). Raises ValueError if a family has
    no detected license and no override. FileNotFoundError if upstream.toml missing
    or src/fonts layout invalid; ValueError if cache missing for a family.
    """
    upstream_toml = request.pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        raise FileNotFoundError(f"upstream.toml not found in {request.pack_dir}")
    pack, source, families, _, overrides = load_pack_config(upstream_toml, require_ref=True)
    cache_root = request.cache_dir or (request.pack_dir / "cache")
    font_root = resolve_font_root(request.pack_dir, pack)
    font_root.mkdir(parents=True, exist_ok=True)
    family_dirs: list[Path] = []
    for family_path in families:
        cached = cache_root / source.ref / family_path
        if not cached.is_dir():
            raise FileNotFoundError(
                f"Cache missing for {family_path}. Run fetch first."
            )
        dest_family = font_root / family_path
        dest_family.parent.mkdir(parents=True, exist_ok=True)
        copy_tree(cached, dest_family)
        family_dirs.append(dest_family)
    resolved = resolve_licenses(families, family_dirs, overrides)
    licenses = [ManifestLicenseConfig(spdx=spdx, path=path) for spdx, path in resolved]

    manifest_path: Path | None = None
    if request.generate_manifest:
        output = font_root / "pack_manifest.json"
        generate_manifest(
            output_path=output,
            pack=pack,
            source=source,
            families=families,
            font_root=font_root,
            licenses=licenses,
            tool_version=request.tool_version,
            include_timestamp=request.include_timestamp,
        )
        manifest_path = output

    readme_path: Path | None = None
    if request.generate_readme:
        generate_readme(request.pack_dir, pack, source, families, licenses, font_root)
        readme_path = request.pack_dir / "README.md"

    return BuildResult(
        font_root=font_root,
        manifest_path=manifest_path,
        readme_path=readme_path,
        licenses=licenses,
    )


# ---------------------------------------------------------------------------
# Manifest-only
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ManifestRequest:
    """Parameters for run_manifest."""

    pack_dir: Path
    font_root: Path | None = None  # default: resolved from pack_dir + config
    output: Path | None = None  # default: font_root/pack_manifest.json
    tool_version: str = "0.1.0"
    include_timestamp: bool = False


@dataclass(frozen=True, slots=True)
class ManifestResult:
    """Result of run_manifest."""

    output_path: Path
    manifest: dict[str, Any]


def run_manifest(request: ManifestRequest) -> ManifestResult:
    """Generate pack_manifest.json only. Fonts must already be present.

    Reads pack/source/families/licenses from pack_dir/upstream.toml.
    Raises FileNotFoundError if upstream.toml or font_root missing.
    """
    upstream_toml = request.pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        raise FileNotFoundError(f"upstream.toml not found in {request.pack_dir}")
    pack, source, families, licenses, _ = load_pack_config(upstream_toml)
    font_root = request.font_root
    if font_root is None:
        font_root = resolve_font_root(request.pack_dir, pack)
        if not font_root.exists():
            raise FileNotFoundError(f"fonts/ not found at {font_root}")
    output_path = request.output or (font_root / "pack_manifest.json")
    manifest = generate_manifest(
        output_path=output_path,
        pack=pack,
        source=source,
        families=families,
        font_root=font_root,
        licenses=licenses,
        tool_version=request.tool_version,
        include_timestamp=request.include_timestamp,
    )
    return ManifestResult(output_path=output_path, manifest=manifest)
