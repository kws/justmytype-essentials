"""CLI for pack-tools. Delegates to pipeline API."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from justmytype_pack_tools.pipeline import (
    BuildRequest,
    FetchRequest,
    ManifestRequest,
    run_build,
    run_fetch,
    run_manifest,
)


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
    try:
        result = run_fetch(
            FetchRequest(
                pack_dir=pack_dir,
                cache_dir=cache_dir,
                on_family=lambda fp: click.echo(f"Fetching {fp}..."),
            )
        )
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    click.echo(f"Done. Cached under {result.cache_root}")


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
    try:
        result = run_build(
            BuildRequest(
                pack_dir=pack_dir,
                cache_dir=cache_dir,
                tool_version=tool_version,
                generate_manifest=True,
                generate_readme=True,
            )
        )
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    if result.manifest_path is not None:
        click.echo(f"Done. Wrote {result.manifest_path}")
    if result.readme_path is not None:
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
    try:
        result = run_manifest(
            ManifestRequest(
                pack_dir=pack_dir,
                font_root=font_root,
                output=output,
                tool_version=tool_version,
            )
        )
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    click.echo(f"✓ Wrote {result.output_path}")


if __name__ == "__main__":
    main()
