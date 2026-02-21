# justmytype-pack-tools

Build tools for creating JustMyType font packs. Fetch font families from the [google/fonts](https://github.com/google/fonts) repo (or any GitHub repo), assemble pack directories, and generate `pack_manifest.json`. Usable from the justmytype_essentials mono-repo or standalone.

## Commands

- **fetch** — Download configured font families from upstream (GitHub API) into a cache. Requires `source.ref` in `upstream.toml`.
- **build** — Copy fetched families from cache into the pack’s `fonts/` dir, resolve licenses (auto-detect + allowlist), and generate `pack_manifest.json`. Fails if a family’s license is unknown and not overridden.
- **manifest** — Generate `pack_manifest.json` only (fonts must already be present). Use after manual copy or when licenses are defined in config.

## Usage (mono-repo)

From repo root:

```bash
just fetch western-core    # fetch families into cache/
just build western-core    # copy from cache + manifest
just dist western-core     # build wheel
```

Or via CLI with shared cache:

```bash
pack-tools fetch packs/western-core --cache-dir cache
pack-tools build packs/western-core --cache-dir cache
```

## Usage (standalone / other repos)

1. Add an `upstream.toml` next to your pack (see schema below).
2. Run from the pack directory or pass the pack path:

```bash
pack-tools fetch . --cache-dir ./cache
pack-tools build . --cache-dir ./cache
```

No dependency on `packs/<name>` layout; `--cache-dir` and pack path can be any directories.

## upstream.toml schema

- **[pack]** — `name` (required), `version`, `entry_point`, `priority`; optional `description`, `source_url`, `package_dir`, `display_name`.
- **[source]** — `repo` (e.g. `https://github.com/google/fonts`), `ref` (commit SHA, branch, or tag; **required** for fetch/build), optional `archive_sha256`.
- **families** — List of paths relative to repo root (e.g. `["ofl/inter", "apache/sourceserif4"]`). Must match the upstream repo exactly (fetch fails with 404 if a path does not exist).
- **[[licenses]]** — Optional static list of `spdx` and `path` (used by `manifest` command when not using build).
- **[[license_overrides]]** — Optional allowlist: `family` path + `spdx`. Use when auto-detection fails or to override; build fails if a family has no detected license and no override.

Example:

```toml
[pack]
name = "my-font-pack"
version = "0.1.0"
entry_point = "my-pack"
priority = 100

[source]
repo = "https://github.com/google/fonts"
ref = "main"

families = ["ofl/inter", "ofl/notosans"]

[[license_overrides]]
family = "ofl/inter"
spdx = "OFL-1.1"
```

### Pack metadata semantics

Pack identity and display text are resolved in one place and used by both manifest and README generation.

| Field | Source | Meaning |
|-------|--------|--------|
| **name** | `[pack].name` (required) | Canonical code/package identifier; used for `pip install` and manifest `pack.name`. |
| **display_name** | `[pack].display_name` (optional) | Short human-friendly title; written to manifest when set, used for README H1. If unset, pack-tools derives it for README from `name`. |
| **description** | `[pack].description` (optional) | Longer descriptive text; written to manifest and README. |
| **package_dir** | `[pack].package_dir` (optional) | When set, pack-tools uses `src/{package_dir}/fonts` for font layout. |

Manifest includes `pack.name` (always), and optionally `pack.description` and `pack.display_name`. README title and install command use the same resolved values so they stay consistent. When `display_name` is absent, the recommended fallback is `pack.name`; each application may choose what is most appropriate (e.g. humanizing `pack.name`).

## License detection

Build uses strict auto-detection from each family directory (e.g. `OFL.txt`, `LICENSE.txt`, `UFL.txt`, Apache markers). If detection fails or is ambiguous, build fails unless that family is listed in `[[license_overrides]]`.

## Programmatic API

Other tools can run the same logic without shelling out to the CLI. Use the pipeline functions with typed request/result objects.

**Full build** (copy from cache + manifest + README, same as `pack-tools build`):

```python
from pathlib import Path
from justmytype_pack_tools import run_build, BuildRequest

result = run_build(BuildRequest(pack_dir=Path("packs/western-core"), cache_dir=Path("cache")))
# result.font_root, result.manifest_path, result.readme_path, result.licenses
```

**Fetch only**:

```python
from justmytype_pack_tools import run_fetch, FetchRequest

result = run_fetch(FetchRequest(pack_dir=Path("."), cache_dir=Path("./cache")))
# result.cache_root, result.families
```

**Manifest only** (fonts already in place):

```python
from justmytype_pack_tools import run_manifest, ManifestRequest

result = run_manifest(ManifestRequest(pack_dir=Path("."), font_root=Path("src/pkg/fonts")))
# result.output_path, result.manifest
```

**Build with stages toggled** (e.g. copy + licenses but no README, or no manifest):

```python
result = run_build(BuildRequest(
    pack_dir=Path("."),
    generate_manifest=True,
    generate_readme=False,
))
```

Raises `FileNotFoundError` or `ValueError` on config/cache errors; handle as needed.

## Manifest build timestamp

By default, generated `pack_manifest.json` does **not** include `build.timestamp`. That keeps manifests deterministic and makes diffs easier to trace (only `source.ref`, file hashes, and `tool_version` change when inputs change). To record build time for provenance, pass `include_timestamp=True` when calling the API (e.g. `BuildRequest(..., include_timestamp=True)` or `ManifestRequest(..., include_timestamp=True)`). The CLI does not add a flag for this; use the programmatic API if you need it.

## Environment

- **GITHUB_TOKEN** or **GH_TOKEN** — Optional; increases rate limit for GitHub API.

## Installation

From this directory: `uv pip install -e .` (or `pip install -e .`).
