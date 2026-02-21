# JustMyType Essentials

Is a small set of essential fonts that will give a safe baseline
for any application that needs to ensure that a font is guaranteed
to be available. 


---

## **justmytype-western-core**

**Purpose:** Small, safe baseline for most Python applications (UI / web / print / PDF) in Western contexts. Covers Western scripts plus symbols & math.

**Sans**

* Inter (primary UI / general sans)
* Noto Sans (coverage fallback)

**Serif**

* Source Serif 4 (primary serif)
* Noto Serif (coverage fallback)

**Monospace**

* JetBrains Mono (primary mono)
* Noto Sans Mono (coverage fallback)

**Symbols / Math**

* Noto Sans Symbols 2
* STIX Two Math

---

## **justmytype-intl-rtl**

**Purpose:** Correct rendering & shaping for right-to-left scripts.

* Noto Sans Arabic
* Noto Sans Hebrew

(Serif variants optional, not required for baseline reliability.)

---

## **justmytype-intl-south-asia**

**Purpose:** Indic scripts requiring proper shaping engines & glyph coverage.

Baseline set:

* Noto Sans Devanagari
* Noto Sans Bengali
* Noto Sans Tamil
* Noto Sans Telugu

(Expandable later if needed: Gujarati, Kannada, Malayalam, etc.)

---

## **justmytype-intl-sea**

**Purpose:** Southeast Asian scripts commonly missing from Western systems.

* Noto Sans Thai
* Noto Sans Lao
* Noto Sans Khmer
* Noto Sans Myanmar

---

## **justmytype-intl-cjk**

**Purpose:** Explicitly large, opt-in bundle for East Asian typography.

* Noto Sans JP
* Noto Sans KR
* Noto Sans SC (Simplified Chinese)
* Noto Sans TC (Traditional Chinese)

(Separated due to size characteristics.)

---

## **justmytype-intl-africa**

**Purpose:** Non-Latin scripts relevant to African language contexts.

* Noto Sans Ethiopic

(Deliberately minimal; Latin-ext already covered by Western core.)

---

## **justmytype-international** (Meta-pack)

**Purpose:** Broad international coverage **excluding CJK by default**.

Depends on:

* justmytype-western-core
* justmytype-intl-rtl
* justmytype-intl-south-asia
* justmytype-intl-sea
* justmytype-intl-africa

Does **not** include:

* justmytype-intl-cjk (opt-in only)

---

### Structural Philosophy We Settled On

* **Western core = universal default runtime fontset**
* **International packs = script-specific correctness layers**
* **CJK isolated = size + install ergonomics**
* **Meta-pack composes bundles rather than duplicating fonts**

---