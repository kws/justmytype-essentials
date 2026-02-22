"""Tests for manifest generation."""

from pathlib import Path
from unittest.mock import patch

import pytest

from justmytype_pack_tools.manifest import (
    ManifestLicenseConfig,
    ManifestPackConfig,
    ManifestSourceConfig,
    generate_manifest,
)


def test_generate_manifest_includes_variant_when_parse_font_metadata_returns_it(
    tmp_path: Path,
) -> None:
    """Generated manifest font entries include variant when parse_font_metadata provides it."""
    font_root = tmp_path / "fonts"
    font_root.mkdir()
    (font_root / "Inter-Regular.ttf").write_bytes(b"x" * 100)  # dummy file

    pack = ManifestPackConfig(
        name="test-pack",
        version="0.1.0",
        entry_point="test-pack",
        priority=100,
    )
    source = ManifestSourceConfig(repo="https://github.com/google/fonts", ref="main")
    licenses: list[ManifestLicenseConfig] = []
    output_path = tmp_path / "pack_manifest.json"

    meta_with_variant = {
        "family": "Inter",
        "style": "normal",
        "weight": 400,
        "width": "normal",
        "postscript_name": "Inter-Regular",
        "variant": "Regular",
    }

    with patch("justmytype_pack_tools.manifest.parse_font_metadata", return_value=meta_with_variant):
        result = generate_manifest(
            output_path=output_path,
            pack=pack,
            source=source,
            families=["inter"],
            font_root=font_root,
            licenses=licenses,
        )

    assert "fonts" in result
    assert len(result["fonts"]) == 1
    assert result["fonts"][0].get("variant") == "Regular"


def test_generate_manifest_fallback_entry_includes_variant_none(tmp_path: Path) -> None:
    """When parse_font_metadata returns None, fallback font entry includes variant: None."""
    font_root = tmp_path / "fonts"
    font_root.mkdir()
    (font_root / "bad.ttf").write_bytes(b"x")

    pack = ManifestPackConfig(
        name="test-pack",
        version="0.1.0",
        entry_point="test-pack",
        priority=100,
    )
    source = ManifestSourceConfig(repo="https://github.com/google/fonts", ref="main")
    licenses: list[ManifestLicenseConfig] = []
    output_path = tmp_path / "pack_manifest.json"

    with patch("justmytype_pack_tools.manifest.parse_font_metadata", return_value=None):
        result = generate_manifest(
            output_path=output_path,
            pack=pack,
            source=source,
            families=[],
            font_root=font_root,
            licenses=licenses,
        )

    assert len(result["fonts"]) == 1
    assert result["fonts"][0]["variant"] is None
