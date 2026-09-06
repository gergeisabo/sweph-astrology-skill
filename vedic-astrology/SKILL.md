---
name: vedic-astrology
description: "Use when computing Vedic/Jyotish astrology — sidereal charts, nakshatras, Vimshottari/Ashtottari dasha, vargas, yogas, doshas, panchang, ashtakoota matching, muhurat, ashtakavarga. Runs live local astrologica engine."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [astrology, vedic, jyotish, dasha, nakshatra, muhurat]
    category: astrology
    related_skills: [astrologica]
---

# Vedic Astrology / Jyotish (astrologica)

Sidereal (Lahiri) system. Engine: `~/Projects/astrologica`, run with `~/Projects/astrologica/.venv/bin/python`, cwd `~/Projects/astrologica`.

## Non-negotiables

1. **`sidereal=True` everywhere**: `pos = compute_positions(birth, sidereal=True)`. Tropical values are useless for Jyotish (≈23.73° off in 1991).
2. **Whole-sign houses**: `ws = compute_houses(birth, sidereal=True, system="whole_sign")`; house = sign counted from the ASC sign. Assign ONLY via `ws.house_of(lon)`.
3. Keys are `Rahu`/`Ketu` (never "North Node").
4. Ayanamsa: `from astrologica.core import get_ayanamsa; get_ayanamsa(birth.julian_day())` — takes a **JD float**, not BirthData. Gold: **23.7331**.

```python
from astrologica.core import BirthData, compute_positions, compute_houses
from astrologica.vedic import (vedic_chart, nakshatra, vimshottari_dasha,
    ashtottari_dasha, varga_chart, yogas, doshas, panchang)

birth = BirthData("1991-02-15", "18:45:00", 48.2264, 22.0847,
                  tz="Europe/Budapest", place="Kisvárda")
sid = compute_positions(birth, sidereal=True)
ws  = compute_houses(birth, sidereal=True, system="whole_sign")
lagna_sign = int(ws.ascendant // 30)   # 0-11, needed by yogas()
```

## Core (vedic.py)

| Call | Signature | Returns |
|---|---|---|
| `vedic_chart(birth)` | one-shot | keys: `positions, houses, lagna_sign, nakshatra_moon, panchang, yogas, doshas, dignities` |
| `nakshatra(longitude)` | **float** sidereal longitude | `{number, name, pada, ruler, deity, degree_in_nakshatra}` |
| `vimshottari_dasha(birth, sid["Moon"].longitude)` | needs **(birth, sidereal Moon lon)** | 9 dicts `{lord, start_date, end_date, duration_years}` |
| `ashtottari_dasha(birth, sid["Sun"].longitude)` | needs **(birth, sidereal Sun lon)** | 8 dicts, same shape |
| `varga_chart(sid, 9)` | pos dict + varga num (1,3,9,...) | dict of PlanetPosition per division (D9 navamsa, D3 drekkana...) |
| `yogas(sid, ws, lagna_sign)` | **lagna_sign int required** | list `{name, ...}` |
| `doshas(sid, ws)` | pos + houses | list `{name, ...}` (empty list if none) |
| `panchang(birth)` | BirthData | `{tithi: {number,name,paksha}, nakshatra: {...}, yoga, karana, vara, vara_index}` |

## Extended (vedic_ext.py)

```python
from astrologica.vedic_ext import ashtakoota, muhurat_scan, ashtakavarga_bav, sav

ashtakoota(moon_nak1, moon_nak2)   # nakshatra NUMBERS (0-26), e.g. (24, 10)
#   {total, max: 36, varna, vashya, tara, yoni, graha_maitri, gana, bhakoot, nadi,
#    person1_nakshatra, person2_nakshatra, verdict}

muhurat_scan(birth, "marriage", "2026-06-01", "2026-06-30",
             place_lat=48.2264, place_lon=22.0847)
#   list {date, day, score, notes[...]}

ashtakavarga_bav(sid, "Sun", houses=ws)   # pass houses= for Lagna row (else 7 planets only)
sav(sid, houses=ws)                       # dict sign_index 0-11 → points; total must be 337
```

**Ashtakavarga:** BAV per planet: `{0: 2, 1: 5, ..., 11: 4}` (Sun sums 48). SAV total is always **337**; pass `houses=ws` to include the Lagna contribution — a SAV ≠ 337 means houses were omitted.

## CLI

```bash
cd ~/Projects/astrologica
.venv/bin/astro vedic      # gold profile: sidereal planets + nakshatra/pada + houses + Vimshottari
```

## Gold verification (1991-02-15 18:45, Kisvárda — all values from live runs)

- Ayanamsa (Lahiri, JD of birth): **23.7331**
- Sidereal Sun **Aquarius 2.81°** (Dhanishtha p3, H7) · sidereal Moon **Aquarius 14.71°** (lon 314.708)
- **Whole-sign sidereal ASC: Leo** — ascendant 144.218° = Leo (sign index 4) 24.22°; lagna_sign = 4
- Sidereal Mercury **Capricorn 21.86°** (Shravana p4, H6) · Jupiter Cancer 12.58° ℞ (H12) · Rahu Capricorn 4.14° ℞ (H6)
- nakshatra(314.708) = `{number: 24, name: 'Shatabhisha', pada: 3, ruler: 'Rahu', deity: 'Varuna', degree_in_nakshatra: 8.04}`
- Vimshottari (from sid Moon): Rahu 1991-02-15→1998-04-09 (7.14y), Jupiter →2014-04-09 (16y), Saturn →2033-04-08 (19y), Mercury →2050
- Ashtottari (from sid Sun): first period Mars 1991-02-15→1992-05-21 (1.26y), 8 periods
- varga D9: Sun Libra, Moon Aquarius · D3: Moon Gemini
- yogas: 1 — Budhaditya Yoga · doshas: [] (none)
- panchang: tithi 1 Pratipada (Shukla), nakshatra Shatabhisha p3, plus yoga/karana/vara
- ashtakoota(24, 10): total 22.5/36, verdict 'Good match' (Shatabhisha × Purva Phalguni)
- muhurat_scan marriage Jun-2026: 30 slots, first 2026-06-04 Thu score 25
- SAV (houses=ws): {0:25, 1:35, 2:33, 3:22, 4:24, 5:26, 6:28, 7:36, 8:34, 9:24, 10:21, 11:29} — **total 337** ✓

## Rules

- Every reading: all 14 sidereal bodies incl. Rahu/Ketu/Chiron/Lilith, each with sign, degree, nakshatra+pada, house (`ws.house_of`), Rx marker.
- Lagna = whole-sign sidereal ASC sign (Leo for the gold birth); never mix tropical ASC (Virgo 17.95) into a Vedic reading.
- `vimshottari_dasha`/`ashtottari_dasha` do NOT compute the Moon/Sun themselves — always pass the sidereal longitude explicitly.
