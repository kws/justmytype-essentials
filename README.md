# JustMyType Essentials

A small set of essential fonts that give a safe baseline for any application that needs to ensure a font is guaranteed to be available.

## Repo layout

- **pack-tools/** — Build tools for creating JustMyType font packs (fetch from upstream, build pack dirs, generate manifests). See [pack-tools/README.md](pack-tools/README.md) for full CLI usage.
- **packs/** — Font packs, e.g. `western-core` (Inter, Noto Sans, Source Serif 4, Noto Serif, JetBrains Mono, Noto Sans Mono, Noto Sans Symbols 2, STIX Two Math).

## Quickstart

Install a pack:

```bash
pip install justmytype-western-core
```

Develop in this repo:

```bash
just install-tools
just fetch western-core
just build western-core
just dist western-core
```

## License

This repository’s code and tooling are under the license in the root [LICENSE](LICENSE) file. Font files in each pack are under their upstream licenses (e.g. OFL); see each pack’s README and `pack_manifest.json`.
