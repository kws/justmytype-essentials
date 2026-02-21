"""JustMyType pack: Southeast Asian scripts (Noto Sans Thai, Lao, Khmer, Myanmar)."""

from __future__ import annotations

from pathlib import Path

from importlib.resources import files


def get_font_pack() -> "FontPack":
    """Entry point factory for justmytype.packs. Returns a FontPack instance."""
    return _IntlSeaPack()


class _IntlSeaPack:
    """FontPack for justmytype-intl-sea."""

    def get_font_directories(self) -> list[Path]:
        return [Path(str(files("justmytype_intl_sea") / "fonts"))]

    def get_priority(self) -> int:
        return 100

    def get_name(self) -> str:
        return "justmytype-intl-sea"
