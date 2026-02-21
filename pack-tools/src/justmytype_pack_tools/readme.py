"""README generation for font packs using Jinja2 templates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from justmytype_pack_tools.manifest import (
    ManifestLicenseConfig,
    ManifestPackConfig,
    ManifestSourceConfig,
)
from justmytype_pack_tools.metadata import resolve_pack_metadata


def _families_with_licenses(licenses: list[ManifestLicenseConfig]) -> list[dict[str, Any]]:
    """Build single list of families with license info: font (family path), spdx, path to full license."""
    result = []
    for lic in licenses:
        family_path = str(Path(lic.path).parent).replace("\\", "/")
        result.append(
            {
                "font": family_path,
                "spdx": lic.spdx,
                "path": lic.path,
            }
        )
    return result


def generate_readme(
    pack_dir: Path,
    pack: ManifestPackConfig,
    source: ManifestSourceConfig,
    families: list[str],
    licenses: list[ManifestLicenseConfig],
    font_root: Path,
) -> None:
    """Generate README.md for a font pack from the same resolved data as the manifest.

    Uses resolve_pack_metadata for identity/display so README and manifest stay in sync.
    """
    resolved = resolve_pack_metadata(pack)
    families_with_lic = _families_with_licenses(licenses)

    env = Environment(
        loader=PackageLoader("justmytype_pack_tools", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("readme.md.j2")
    context: dict[str, Any] = {
        "pack_name": resolved.display_name,
        "package_name": resolved.package_name,
        "description": resolved.description,
        "families": families_with_lic,
        "source_repo": source.repo,
        "source_ref": source.ref,
    }
    content = template.render(**context)
    readme_path = pack_dir / "README.md"
    readme_path.write_text(content, encoding="utf-8")
