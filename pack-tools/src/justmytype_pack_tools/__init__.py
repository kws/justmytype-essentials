"""Build tools for JustMyType font packs."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from justmytype_pack_tools.manifest import (
    generate_manifest,
    get_build_timestamp,
)
from justmytype_pack_tools.pipeline import (
    BuildRequest,
    BuildResult,
    FetchRequest,
    FetchResult,
    ManifestRequest,
    ManifestResult,
    resolve_font_root,
    run_build,
    run_fetch,
    run_manifest,
)

try:
    __version__ = version("justmytype_pack_tools")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = [
    "generate_manifest",
    "get_build_timestamp",
    "resolve_font_root",
    "run_fetch",
    "run_build",
    "run_manifest",
    "FetchRequest",
    "FetchResult",
    "BuildRequest",
    "BuildResult",
    "ManifestRequest",
    "ManifestResult",
]
