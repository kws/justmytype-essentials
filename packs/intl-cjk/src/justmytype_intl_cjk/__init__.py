"""JustMyType pack: East Asian scripts (Noto Sans JP, KR, SC, TC)."""

from __future__ import annotations

from pathlib import Path

from importlib.resources import files


def get_font_pack() -> "FontPack":
    """Entry point factory for justmytype.packs. Returns a FontPack instance."""
    return _IntlCjkPack()


class _IntlCjkPack:
    """FontPack for justmytype-intl-cjk."""

    def get_font_directories(self) -> list[Path]:
        return [Path(str(files("justmytype_intl_cjk") / "fonts"))]

    def get_priority(self) -> int:
        return 100

    def get_name(self) -> str:
        return "justmytype-intl-cjk"
