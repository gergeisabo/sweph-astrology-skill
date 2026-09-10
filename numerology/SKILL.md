---
name: numerology
description: "Use when computing numerology from a name or birth date. Life path, soul urge, expression, chaldean, kabbalistic, vedic. Hungarian: számmisztika, életszám, sorsszám."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [astrology, numerology, life-path, soul-urge, chaldean, kabbalistic, vedic]
    category: astrology
    related_skills: [astrologica, destiny-matrix]
---

# Numerology — `astrologica.numerology`

Pure arithmetic, no dependencies. Inputs: `name: str` (ASCII letters; non-ASCII like
'ó' contribute 0 — pass 'Gergely Szabo' style transliteration if needed) and
`date_str: str` like `'1991-02-15'`. NOT BirthData objects.

```python
from astrologica import numerology
# run with: ~/Projects/astrologica/.venv/bin/python, cwd ~/Projects/astrologica
```

## Entry point

`numerology.full_profile(name, date_str, system='pythagorean')` — the ONLY complete
profile. There is **NO `pythagorean()` function**; the system is the `system=` param of
`name_number` / `soul_urge_number` / `personality_number` / `full_profile`
(`'pythagorean'` | `'chaldean'` | `'kabbalistic'`).

## Functions (all verified live)

| Call | Note |
|---|---|
| `numerology.full_profile('Gergely Szabó', '1991-02-15')` | everything below in one dict |
| `numerology.life_path_number('1991-02-15')` | → 1 |
| `numerology.birthday_number('1991-02-15')` | day-of-month reduced → 6 |
| `numerology.attitude_number('1991-02-15')` | month+day → 8 |
| `numerology.personal_year('1991-02-15', 2026)` | needs current year → 9 |
| `numerology.name_number(name, system=...)` | Expression/Destiny; systems differ |
| `numerology.soul_urge_number(name, system=...)` | vowels only |
| `numerology.personality_number(name, system=...)` | consonants only |
| `numerology.vedic_number('1991-02-15')` | root number + planet (1=Sun) |

Reduction keeps master numbers 11/22/33; `personal_year` reduces master numbers too.

## Gold profile — verified live

`full_profile('Gergely Szabó', '1991-02-15')`:
life_path **1 "The Leader"**, birthday 6, attitude 8, expression 1, **soul_urge 11**
(Master Intuitive), personality 8, vedic root 1/Sun.

Per-system for that name: expression — pythagorean 1, chaldean 8, kabbalistic 1;
soul_urge 11 in all three; personality — 8 / 6 / 8.

## Cross-reference

Destiny Matrix (Ladini) numerology lives in the separate **destiny-matrix** skill —
do not duplicate it here.

## CLI

```bash
cd ~/Projects/astrologica && .venv/bin/astro numerology --name "Gergely Szabó" --date 1991-02-15 [--year 2026]
```
Prints the full_profile JSON. Flag-based; `--name` is required.
