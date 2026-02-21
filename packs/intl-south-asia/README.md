<!-- This file is auto-generated. Do not edit manually. -->

# Intl South Asia

Indic scripts: Noto Sans Devanagari, Bengali, Tamil, Telugu

## Installation

```bash
pip install justmytype-intl-south-asia
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
| ofl/notosansdevanagari | OFL-1.1 | `fonts/ofl/notosansdevanagari/OFL.txt` |
| ofl/notosansbengali | OFL-1.1 | `fonts/ofl/notosansbengali/OFL.txt` |
| ofl/notosanstamil | OFL-1.1 | `fonts/ofl/notosanstamil/OFL.txt` |
| ofl/notosanstelugu | OFL-1.1 | `fonts/ofl/notosanstelugu/OFL.txt` |


## Upstream

Source: https://github.com/google/fonts @ main

## Development

- **Fetch:** `pack-tools fetch <pack_dir>` — downloads upstream fonts into cache.
- **Build:** `pack-tools build <pack_dir>` — copies fonts into the pack, generates `pack_manifest.json` and this README.
- **Dist:** `pip install -e .` or build the wheel from the pack directory.

README is generated during build from the same resolved license data as the manifest.