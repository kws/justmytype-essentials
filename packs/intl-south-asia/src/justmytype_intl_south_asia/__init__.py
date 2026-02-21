"""JustMyType pack: Indic scripts (Noto Sans Devanagari, Bengali, Tamil, Telugu)."""

from __future__ import annotations

from pathlib import Path

from importlib.resources import files


def get_font_pack() -> "FontPack":
    """Entry point factory for justmytype.packs. Returns a FontPack instance."""
    return _IntlSouthAsiaPack()


class _IntlSouthAsiaPack:
    """FontPack for justmytype-intl-south-asia."""

    def get_font_directories(self) -> list[Path]:
        return [Path(str(files("justmytype_intl_south_asia") / "fonts"))]

    def get_priority(self) -> int:
        return 100

    def get_name(self) -> str:
        return "justmytype-intl-south-asia"
