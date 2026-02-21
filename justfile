# justfile
set shell := ["bash", "-euo", "pipefail", "-c"]

PACKS := "western-core intl-rtl intl-south-asia intl-sea intl-cjk intl-africa"
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
    cd packs/{{pack}} && uv build --wheel -o ../../dist && cd ../..

# Fetch all packs
fetch-all:
    @for pkg in {{PACKS}}; do echo "Fetching $pkg..." && just fetch $pkg; done

# Build all packs
build-all:
    @for pkg in {{PACKS}}; do echo "Building $pkg..." && just build $pkg; done

# Dist all packs
dist-all:
    @for pkg in {{PACKS}}; do echo "Distributing $pkg..." && just dist $pkg; done