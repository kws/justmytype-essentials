<!-- This file is auto-generated. Do not edit manually. -->

# Intl Sea

Southeast Asian scripts: Noto Sans Thai, Lao, Khmer, Myanmar

## Installation

```bash
pip install justmytype-intl-sea
```

## Usage

```python
from justmytype import FontRegistry

registry = FontRegistry()
font = registry.find_font(family="Inter", weight=400)
if font:
    # Use font.path to load the font file
    pass
```

## Families

| Font | License | Full text |
|------|---------|-----------|
| ofl/notosansthai | OFL-1.1 | `fonts/ofl/notosansthai/OFL.txt` |
| ofl/notosanslao | OFL-1.1 | `fonts/ofl/notosanslao/OFL.txt` |
| ofl/notosanskhmer | OFL-1.1 | `fonts/ofl/notosanskhmer/OFL.txt` |
| ofl/notosansmyanmar | OFL-1.1 | `fonts/ofl/notosansmyanmar/OFL.txt` |


## Upstream

Source: https://github.com/google/fonts @ main

## Development

- **Fetch:** `pack-tools fetch <pack_dir>` — downloads upstream fonts into cache.
- **Build:** `pack-tools build <pack_dir>` — copies fonts into the pack, generates `pack_manifest.json` and this README.
- **Dist:** `pip install -e .` or build the wheel from the pack directory.

README is generated during build from the same resolved license data as the manifest.