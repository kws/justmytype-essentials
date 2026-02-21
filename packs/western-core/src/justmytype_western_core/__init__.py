"""JustMyType pack: Western core fonts."""

from __future__ import annotations

from pathlib import Path

from importlib.resources import files


def get_font_pack() -> "FontPack":
    """Entry point factory for justmytype.packs. Returns a FontPack instance."""
    return _WesternCorePack()


class _WesternCorePack:
    """FontPack for justmytype-western-core."""

    def get_font_directories(self) -> list[Path]:
        return [Path(str(files("justmytype_western_core") / "fonts"))]

    def get_priority(self) -> int:
        return 100

    def get_name(self) -> str:
        return "justmytype-western-core"
