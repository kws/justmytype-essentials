# justfile
set shell := ["bash", "-euo", "pipefail", "-c"]

PACKS := "western-core"
CACHE_DIR := "cache"

help:
    @just --list

# Install pack-tools (run from repo root after uv sync in pack-tools/)
install-tools:
    cd pack-tools && uv pip install -e . && cd ..

# Install a pack in development mode
install pack:
    @echo "Installing {{pack}}..."
    cd packs/{{pack}} && uv pip install -e . && cd ../..

# Fetch font families from upstream into shared cache
fetch pack:
    pack-tools fetch packs/{{pack}} --cache-dir {{CACHE_DIR}}

# Build pack (copy from cache + generate manifest)
build pack:
    pack-tools build packs/{{pack}} --cache-dir {{CACHE_DIR}}

# Generate pack_manifest.json only (run after fonts are in pack's fonts/)
manifest pack:
    pack-tools manifest packs/{{pack}}

# Build distribution wheel for a pack
dist pack:
    cd packs/{{pack}} && python -m build --wheel --outdir ../../dist && cd ../..

# Fetch all packs
fetch-all:
    @for pack in {{PACKS}}; do echo "Fetching $$pack..."; just fetch $$pack; done

# Build all packs
build-all:
    @for pack in {{PACKS}}; do echo "Building $$pack..."; just build $$pack; done
