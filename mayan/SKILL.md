---
name: mayan
description: "Use when a Mayan calendar reading is needed (Tzolkin, Haab, Long Count, Dreamspell, compatibility). Date strings only — no BirthData, no birth time or place required."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [astrology, mayan, tzolkin, haab, long-count, dreamspell, calendar]
    category: astrology
    related_skills: [astrologica]
---

# Mayan Calendar — `astrologica.mayan`

Pure date arithmetic, no dependencies. GMT correlation 584283 (epoch Aug 11, 3114 BCE).

## ⚠️ API shape — DATE STRINGS, NOT BirthData

All functions take `date_str: str` like `'1991-02-15'` (YYYY-MM-DD). They do NOT accept
`BirthData` objects and ignore time/place entirely — pass the raw date string only.

```python
from astrologica import mayan
# run with: ~/Projects/astrologica/.venv/bin/python, cwd ~/Projects/astrologica
```

## Functions

| Call | Returns |
|---|---|
| `mayan.long_count('1991-02-15')` | baktun..kin + `long_count_str` |
| `mayan.tzolkin('1991-02-15')` | `{number, day_name, full}` (260-day sacred calendar) |
| `mayan.haab('1991-02-15')` | `{day, month, full}` (365-day solar) |
| `mayan.dreamspell('1991-02-15')` | `{kin, tone, seal, full}` (Arguelles) |
| `mayan.full('1991-02-15')` | all four above under one dict |
| `mayan.compatibility('1991-02-15', '1990-06-01')` | Tzolkin affinity of two dates |

## Gold values — verified live ('1991-02-15')

- `long_count` → `12.18.17.15.0`
- `tzolkin` → **6 Ahau**
- `haab` → **13 Wo**
- `dreamspell` → **Kin 260: 13 Ahau**
- `compatibility('1991-02-15','1990-06-01')` → 6 Ahau / 7 Imix, affinity "high", same_seal False

## Dreamspell correlation warning

`dreamspell` uses its OWN calendar: epoch **July 26, 1987** = Kin 260 (13 Ahau), i.e. the
'13-moon'/Arguelles correlation, deliberately different from the traditional Long Count.
So for '1991-02-15' Tzolkin says 6 Ahau while Dreamspell says 13 Ahau — that divergence is
correct, not a bug (mayan offsets were fixed in engine history; do not "fix" them again).

## CLI

```bash
cd ~/Projects/astrologica && .venv/bin/astro mayan --date 1991-02-15
```
Note: date is a `--date` FLAG — a bare positional date is rejected. CLI prints Tzolkin,
Haab, Long Count (no Dreamspell); use Python for Dreamspell/full/compatibility.
