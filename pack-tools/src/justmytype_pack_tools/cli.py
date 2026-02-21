"""CLI for pack-tools."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from justmytype_pack_tools.config import load_pack_config
from justmytype_pack_tools.download import download_family_tree, get_github_token
from justmytype_pack_tools.filesystem import copy_tree
from justmytype_pack_tools.licenses import resolve_licenses
from justmytype_pack_tools.manifest import (
    ManifestLicenseConfig,
    generate_manifest,
)
from justmytype_pack_tools.readme import generate_readme


@click.group()
def main() -> None:
    """Build tools for creating JustMyType font packs."""
    pass


@main.command("fetch")
@click.argument("pack_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option(
    "--cache-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Cache root (default: pack_dir/cache)",
)
def fetch_cmd(pack_dir: Path, cache_dir: Path | None) -> None:
    """Fetch font families from upstream (GitHub) into cache.

    Reads families and source.ref from pack_dir/upstream.toml. source.ref is required.
    """
    upstream_toml = pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        click.echo(f"Error: upstream.toml not found in {pack_dir}", err=True)
        sys.exit(1)
    try:
        pack, source, families, _, _ = load_pack_config(upstream_toml, require_ref=True)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    if not source.repo:
        click.echo("Error: source.repo is required in upstream.toml", err=True)
        sys.exit(1)
    cache_root = cache_dir or (pack_dir / "cache")
    cache_root.mkdir(parents=True, exist_ok=True)
    token = get_github_token()
    for family_path in families:
        click.echo(f"Fetching {family_path}...")
        download_family_tree(
            repo_url=source.repo,
            ref=source.ref,
            family_path=family_path,
            cache_dir=cache_root,
            token=token,
        )
    click.echo(f"Done. Cached under {cache_root}")


@main.command("build")
@click.argument("pack_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option(
    "--cache-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Cache root (default: pack_dir/cache)",
)
@click.option(
    "--tool-version",
    default="0.1.0",
    help="pack-tools version to record in manifest",
)
def build_cmd(pack_dir: Path, cache_dir: Path | None, tool_version: str) -> None:
    """Copy fetched families from cache into pack fonts dir and generate manifest.

    Resolves licenses (auto-detect + allowlist). Fails if license unknown and not overridden.
    """
    upstream_toml = pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        click.echo(f"Error: upstream.toml not found in {pack_dir}", err=True)
        sys.exit(1)
    try:
        pack, source, families, _, overrides = load_pack_config(upstream_toml, require_ref=True)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    cache_root = cache_dir or (pack_dir / "cache")
    src = pack_dir / "src"
    if not src.exists():
        click.echo(f"Error: src/ not found in {pack_dir}", err=True)
        sys.exit(1)
    candidates = [d for d in src.iterdir() if d.is_dir() and d.name.startswith("justmytype_")]
    if not candidates:
        click.echo(f"Error: no justmytype_* directory in {src}", err=True)
        sys.exit(1)
    font_root = candidates[0] / "fonts"
    font_root.mkdir(parents=True, exist_ok=True)
    family_dirs: list[Path] = []
    for family_path in families:
        cached = cache_root / source.ref / family_path
        if not cached.is_dir():
            click.echo(f"Error: cache missing for {family_path}. Run 'pack-tools fetch {pack_dir}' first.", err=True)
            sys.exit(1)
        dest_family = font_root / family_path
        dest_family.parent.mkdir(parents=True, exist_ok=True)
        copy_tree(cached, dest_family)
        family_dirs.append(dest_family)
    try:
        resolved = resolve_licenses(families, family_dirs, overrides)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    licenses = [ManifestLicenseConfig(spdx=spdx, path=path) for spdx, path in resolved]
    output = font_root / "pack_manifest.json"
    generate_manifest(
        output_path=output,
        pack=pack,
        source=source,
        families=families,
        font_root=font_root,
        licenses=licenses,
        tool_version=tool_version,
    )
    click.echo(f"Done. Wrote {output}")
    generate_readme(pack_dir, pack, source, families, licenses, font_root)
    click.echo("Generated README.md")


@main.command("manifest")
@click.argument("pack_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option(
    "--font-root",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Directory containing font files (default: pack_dir/src/justmytype_*/fonts)",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Output path for pack_manifest.json (default: font_root/pack_manifest.json)",
)
@click.option(
    "--tool-version",
    default="0.1.0",
    help="pack-tools version to record in manifest",
)
def manifest_cmd(
    pack_dir: Path,
    font_root: Path | None,
    output: Path | None,
    tool_version: str,
) -> None:
    """Generate pack_manifest.json for a font pack.

    Reads pack/source/families/licenses from pack_dir/upstream.toml.
    Scans font_root for font files and writes pack_manifest.json.
    """
    upstream_toml = pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        click.echo(f"Error: upstream.toml not found in {pack_dir}", err=True)
        sys.exit(1)

    if font_root is None:
        src = pack_dir / "src"
        if not src.exists():
            click.echo(f"Error: src/ not found in {pack_dir}", err=True)
            sys.exit(1)
        candidates = [d for d in src.iterdir() if d.is_dir() and d.name.startswith("justmytype_")]
        if not candidates:
            click.echo(f"Error: no justmytype_* directory in {src}", err=True)
            sys.exit(1)
        font_root = candidates[0] / "fonts"
        if not font_root.exists():
            click.echo(f"Error: fonts/ not found in {candidates[0]}", err=True)
            sys.exit(1)

    if output is None:
        output = font_root / "pack_manifest.json"

    try:
        pack, source, families, licenses, _ = load_pack_config(upstream_toml)
        generate_manifest(
            output_path=output,
            pack=pack,
            source=source,
            families=families,
            font_root=font_root,
            licenses=licenses,
            tool_version=tool_version,
        )
        click.echo(f"✓ Wrote {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
