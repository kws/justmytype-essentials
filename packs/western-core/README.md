<!-- This file is auto-generated. Do not edit manually. -->

# Western Core

Western core fonts: Inter, Noto Sans, Source Serif 4, Noto Serif, JetBrains Mono, Noto Sans Mono, Noto Sans Symbols 2, STIX Two Math

## Installation

```bash
pip install justmytype-western-core
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
| ofl/inter | OFL-1.1 | `fonts/ofl/inter/OFL.txt` |
| ofl/notosans | OFL-1.1 | `fonts/ofl/notosans/OFL.txt` |
| ofl/sourceserif4 | OFL-1.1 | `fonts/ofl/sourceserif4/OFL.txt` |
| ofl/notoserif | OFL-1.1 | `fonts/ofl/notoserif/OFL.txt` |
| ofl/jetbrainsmono | OFL-1.1 | `fonts/ofl/jetbrainsmono/OFL.txt` |
| ofl/notosansmono | OFL-1.1 | `fonts/ofl/notosansmono/OFL.txt` |
| ofl/notosanssymbols2 | OFL-1.1 | `fonts/ofl/notosanssymbols2/OFL.txt` |
| ofl/stixtwomath | OFL-1.1 | `fonts/ofl/stixtwomath/OFL.txt` |


## Upstream

Source: https://github.com/google/fonts @ main

## Development

- **Fetch:** `pack-tools fetch <pack_dir>` — downloads upstream fonts into cache.
- **Build:** `pack-tools build <pack_dir>` — copies fonts into the pack, generates `pack_manifest.json` and this README.
- **Dist:** `pip install -e .` or build the wheel from the pack directory.

README is generated during build from the same resolved license data as the manifest.