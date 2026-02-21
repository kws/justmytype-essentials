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

- **[pack]** — `name`, `version`, `entry_point`, `priority`; optional `description`, `source_url`.
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

## License detection

Build uses strict auto-detection from each family directory (e.g. `OFL.txt`, `LICENSE.txt`, `UFL.txt`, Apache markers). If detection fails or is ambiguous, build fails unless that family is listed in `[[license_overrides]]`.

## Environment

- **GITHUB_TOKEN** or **GH_TOKEN** — Optional; increases rate limit for GitHub API.

## Installation

From this directory: `uv pip install -e .` (or `pip install -e .`).
