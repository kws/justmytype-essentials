# JustMyType Essentials

A small set of essential fonts that give a safe baseline for any application that needs to ensure a font is guaranteed to be available.

## Repo layout

- **pack-tools/** — Build tools for creating JustMyType font packs (fetch from upstream, build pack dirs, generate manifests). See [pack-tools/README.md](pack-tools/README.md) for full CLI usage.
- **packs/** — Font packs: `western-core` (Western baseline), `intl-rtl`, `intl-south-asia`, `intl-sea`, `intl-cjk`, `intl-africa`, and the meta-pack `international` (western + all international except CJK).

## Quickstart

Install a pack:

```bash
pip install justmytype-western-core
```

For broad international coverage (excluding East Asian), use `pip install justmytype-international`. For East Asian (CJK), add `justmytype-intl-cjk`.

Develop in this repo:

```bash
just install-tools
just fetch western-core
just build western-core
just dist western-core
```

To work on all font packs: `just fetch-all`, `just build-all`, `just dist-all`. The meta-pack has no upstream; build it with `just dist international`.

## Rationale

- Western core = universal default runtime fontset
- International packs = script-specific correctness layers
- CJK isolated = size + install ergonomics
- Meta-pack composes bundles rather than duplicating fonts

## License

This repository’s code and tooling are under the license in the root [LICENSE](LICENSE) file. Font files in each pack are under their upstream licenses (e.g. OFL); see each pack’s README and `pack_manifest.json`.
