# JustMyType Essentials

A small set of essential fonts that give a safe baseline for any application that needs to ensure a font is guaranteed to be available.

## Repo layout

- **pack-tools/** — Build tools for creating JustMyType font packs (fetch from upstream, build pack dirs, generate manifests). See [pack-tools/README.md](pack-tools/README.md) for full CLI usage.
- **packs/** — Font packs: `western-core` (Western baseline), `intl-rtl`, `intl-south-asia`, `intl-sea`, `intl-cjk`, `intl-africa`, and the meta-pack `international` (western + all international except CJK). See [plan.md](plan.md) for the full list and rationale.

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
