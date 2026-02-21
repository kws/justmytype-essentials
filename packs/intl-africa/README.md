<!-- This file is auto-generated. Do not edit manually. -->

# Intl Africa

African scripts: Noto Sans Ethiopic

## Installation

```bash
pip install justmytype-intl-africa
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
| ofl/notosansethiopic | OFL-1.1 | `fonts/ofl/notosansethiopic/OFL.txt` |


## Upstream

Source: https://github.com/google/fonts @ main

## Development

- **Fetch:** `pack-tools fetch <pack_dir>` — downloads upstream fonts into cache.
- **Build:** `pack-tools build <pack_dir>` — copies fonts into the pack, generates `pack_manifest.json` and this README.
- **Dist:** `pip install -e .` or build the wheel from the pack directory.

README is generated during build from the same resolved license data as the manifest.