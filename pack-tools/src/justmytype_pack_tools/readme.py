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

    Uses the same licenses list as generate_manifest so README and manifest stay in sync.
    """
    pyproject_toml = pack_dir / "pyproject.toml"
    package_name = pack_dir.name.replace("-", "_")
    if pyproject_toml.exists():
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib  # type: ignore[no-redef]
        try:
            with open(pyproject_toml, "rb") as f:
                pyproject = tomllib.load(f)
                package_name = pyproject.get("project", {}).get("name", package_name)
        except Exception:
            pass

    pack_name = pack_dir.name.replace("-", " ").replace("_", " ").title()
    families = _families_with_licenses(licenses)

    env = Environment(
        loader=PackageLoader("justmytype_pack_tools", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("readme.md.j2")
    context: dict[str, Any] = {
        "pack_name": pack_name,
        "package_name": package_name,
        "description": pack.description,
        "families": families,
        "source_repo": source.repo,
        "source_ref": source.ref,
    }
    content = template.render(**context)
    readme_path = pack_dir / "README.md"
    readme_path.write_text(content, encoding="utf-8")
