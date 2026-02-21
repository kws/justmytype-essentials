"""Configuration loading for font pack upstream.toml."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from justmytype_pack_tools.licenses import LicenseOverride
from justmytype_pack_tools.manifest import (
    ManifestLicenseConfig,
    ManifestPackConfig,
    ManifestSourceConfig,
)


def _load_toml(file_path: Path) -> dict[str, Any]:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]

    with open(file_path, "rb") as f:
        return tomllib.load(f)


def _normalize_family_path(path: str) -> str:
    """Normalize family path (e.g. ofl/inter)."""
    return path.strip("/").replace("\\", "/")


def load_pack_config(
    upstream_toml_path: Path,
    require_ref: bool = False,
) -> tuple[ManifestPackConfig, ManifestSourceConfig, list[str], list[ManifestLicenseConfig], list[LicenseOverride]]:
    """Load pack, source, families, licenses, and license overrides from upstream.toml.

    Expected sections:
      [pack] name, version, entry_point, priority, description?, source_url?
      [source] repo, ref, archive_sha256?
      families = ["ofl/inter", ...]
      [[licenses]] spdx = "...", path = "..."  (optional if using auto-detect + overrides)
      [[license_overrides]] family = "ofl/inter", spdx = "OFL-1.1"

    If require_ref is True, raises ValueError when source.ref is missing.
    """
    config = _load_toml(upstream_toml_path)
    pack_dict = config.get("pack", {})
    source_dict = config.get("source", {})

    pack = ManifestPackConfig(
        name=pack_dict.get("name", ""),
        version=pack_dict.get("version", ""),
        entry_point=pack_dict.get("entry_point", ""),
        priority=int(pack_dict.get("priority", 100)),
        description=pack_dict.get("description", ""),
        source_url=pack_dict.get("source_url", ""),
    )
    ref = source_dict.get("ref", "").strip()
    if require_ref and not ref:
        raise ValueError(
            "source.ref is required for fetch/build. Set ref to a commit SHA, branch, or tag in upstream.toml [source]."
        )
    source = ManifestSourceConfig(
        repo=source_dict.get("repo", ""),
        ref=ref,
        archive_sha256=source_dict.get("archive_sha256", ""),
    )
    families = [_normalize_family_path(p) for p in config.get("families", [])]
    licenses = [
        ManifestLicenseConfig(spdx=lic.get("spdx", ""), path=lic.get("path", ""))
        for lic in config.get("licenses", [])
    ]
    overrides = [
        LicenseOverride(
            family_path=_normalize_family_path(o.get("family", "")),
            spdx=(o.get("spdx") or "").strip(),
        )
        for o in config.get("license_overrides", [])
        if o.get("family") and o.get("spdx")
    ]
    return pack, source, families, licenses, overrides
