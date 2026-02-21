"""JustMyType pack: RTL scripts (Noto Sans Arabic, Noto Sans Hebrew)."""

from __future__ import annotations

from pathlib import Path

from importlib.resources import files


def get_font_pack() -> "FontPack":
    """Entry point factory for justmytype.packs. Returns a FontPack instance."""
    return _IntlRtlPack()


class _IntlRtlPack:
    """FontPack for justmytype-intl-rtl."""

    def get_font_directories(self) -> list[Path]:
        return [Path(str(files("justmytype_intl_rtl") / "fonts"))]

    def get_priority(self) -> int:
        return 100

    def get_name(self) -> str:
        return "justmytype-intl-rtl"
