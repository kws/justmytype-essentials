"""Strict auto-detection of font family licenses with allowlist overrides."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# Known license filenames in google/fonts family dirs and their SPDX
LICENSE_FILENAMES = [
    ("OFL.txt", "OFL-1.1"),
    ("OFL", "OFL-1.1"),
    ("LICENSE.txt", None),  # content-based
    ("LICENSE", None),
    ("UFL.txt", "UFL-1.0"),
    ("UFL", "UFL-1.0"),
]

# Content snippets that imply Apache-2.0
APACHE_MARKERS = [
    "apache license",
    "apache 2.0",
    "licensed under the apache",
    "http://www.apache.org/licenses/license-2.0",
]


@dataclass(frozen=True, slots=True)
class LicenseOverride:
    """Explicit license override per family (allowlist)."""

    family_path: str
    spdx: str


def detect_license_in_dir(family_dir: Path) -> str | None:
    """Detect SPDX license from a family directory (e.g. cache/ref/ofl/inter).

    Looks for OFL.txt, LICENSE.txt, UFL.txt etc. Returns SPDX string or None if
    unknown/ambiguous.
    """
    if not family_dir.is_dir():
        return None
    for filename, default_spdx in LICENSE_FILENAMES:
        path = family_dir / filename
        if not path.is_file():
            continue
        if default_spdx:
            return default_spdx
        # Content-based for LICENSE / LICENSE.txt
        try:
            text = path.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        for marker in APACHE_MARKERS:
            if marker in text:
                return "Apache-2.0"
        if "open font license" in text or "sil open font" in text or "ofl" in text:
            return "OFL-1.1"
        if "ubuntu font licence" in text or "ufl" in text:
            return "UFL-1.0"
    return None


def resolve_licenses(
    family_paths: list[str],
    family_dirs: list[Path],
    overrides: list[LicenseOverride],
) -> list[tuple[str, str]]:
    """Resolve (spdx, license_file_path) for each family; fail if unresolved and not allowlisted.

    family_paths and family_dirs must align by index (path for each dir).
    overrides are from upstream.toml [[license_overrides]].

    Returns list of unique (spdx, path) for manifest. Path is relative to pack fonts root.
    Raises ValueError if a family has no detected license and no override.
    """
    override_map = {o.family_path: o.spdx for o in overrides}
    resolved: list[tuple[str, str]] = []  # (spdx, rel_path)
    seen: set[tuple[str, str]] = set()

    for family_path, dir_path in zip(family_paths, family_dirs, strict=True):
        detected = detect_license_in_dir(dir_path)
        spdx = override_map.get(family_path) or detected
        if not spdx:
            raise ValueError(
                f"License unknown for family {family_path!r} (no override in [[license_overrides]]). "
                "Add a [[license_overrides]] entry with family = ... and spdx = ... for this pack."
            )
        lic_filename = _license_filename_in_dir(dir_path)
        if lic_filename:
            lic_path = f"{family_path}/{lic_filename}"
        else:
            lic_path = f"LICENSES/{spdx}.txt"
        key = (spdx, lic_path)
        if key not in seen:
            seen.add(key)
            resolved.append(key)
    return resolved


def _license_filename_in_dir(family_dir: Path) -> str | None:
    """Return filename of first license file found in the family dir."""
    for filename, _ in LICENSE_FILENAMES:
        path = family_dir / filename
        if path.is_file():
            return filename
    return None
