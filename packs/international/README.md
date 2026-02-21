# justmytype-international

Meta-pack for broad international font coverage. Installing this package brings in:

- **justmytype-western-core** — Western scripts, symbols, math
- **justmytype-intl-rtl** — Noto Sans Arabic, Noto Sans Hebrew
- **justmytype-intl-south-asia** — Noto Sans Devanagari, Bengali, Tamil, Telugu
- **justmytype-intl-sea** — Noto Sans Thai, Lao, Khmer, Myanmar
- **justmytype-intl-africa** — Noto Sans Ethiopic

CJK (East Asian) fonts are **not** included. For Japanese, Korean, and Chinese (Simplified/Traditional), install **justmytype-intl-cjk** separately:

```bash
pip install justmytype-intl-cjk
```

## Installation

```bash
pip install justmytype-international
```

## Usage

After installation, use JustMyType as usual. The dependent packs register their fonts automatically.

```python
from justmytype import FontRegistry

registry = FontRegistry()
# All international packs (except CJK) are available
font = registry.find_font(family="Noto Sans Arabic", weight=400)
```
