"""Central resolution of pack identity and display metadata.

All pack-level values used by README and manifest generation are derived here
from ManifestPackConfig so they stay consistent.
"""

from __future__ import annotations

from dataclasses import dataclass

from justmytype_pack_tools.manifest import ManifestPackConfig


def _humanize_name(name: str) -> str:
    """Turn canonical name into a short human-friendly title (e.g. deckr-fonts -> Deckr Fonts)."""
    if not name:
        return ""
    return name.replace("-", " ").replace("_", " ").title()


@dataclass(frozen=True, slots=True)
class ResolvedPackMetadata:
    """Resolved pack identity and display fields for README/manifest.

    All values come from pack config; no folder names or pyproject.
    """

    display_name: str  # H1 / short human title
    package_name: str  # pip install name (same as pack.name)
    description: str  # longer descriptive text
    name: str  # canonical pack name (same as pack.name)


def resolve_pack_metadata(pack: ManifestPackConfig) -> ResolvedPackMetadata:
    """Resolve pack identity and display metadata from config.

    Rules:
    - display_name = pack.display_name if set, else humanize(pack.name)
    - package_name = pack.name
    - description = pack.description
    - name = pack.name
    """
    name = pack.name or ""
    display_name = (pack.display_name or "").strip()
    if not display_name:
        display_name = _humanize_name(name)
    return ResolvedPackMetadata(
        display_name=display_name,
        package_name=name,
        description=pack.description or "",
        name=name,
    )
