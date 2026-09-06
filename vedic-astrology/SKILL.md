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
    ashtottari_dasha, yogini_dasha, kalachakra_dasha, varga_chart, yogas,
    doshas, panchang)
from astrologica.shadbala import shadbala
from astrologica.vedic_ext import (ashtakoota, kp_sublord, chara_karakas,
    karakamsa, jaimini_aspects, arudha_pada, jaimini_yogas, lal_kitab_dasha)

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
| `yogini_dasha(birth, sid["Moon"].longitude)` | needs **(birth, sidereal Moon lon)** | 8 dicts `{yogini, lord_planet, start_date, end_date, duration_years}` (36y cycle) |
| `kalachakra_dasha(birth, sid["Moon"].longitude)` | needs **(birth, sidereal Moon lon)** | 9 dicts `{sign, sign_index, start_date, end_date, duration_years}` (sign-based) |
| `varga_chart(sid, 9)` | pos dict + varga num (1..60; 16 classical supported) | dict of PlanetPosition per division (D9 navamsa, D3 drekkana...) |
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

### KP (Krishnamurti Paddhati) sub-lords

```python
kp_pos = compute_positions(birth, sidereal=True, ayanamsa="krishnamurti")  # NOT lahiri!
kp_hs  = compute_houses(birth, sidereal=True, ayanamsa="krishnamurti")
kp_sublord(lon)            # {star, star_lord, sub_lord, sub_sub_lord, degree_in_star}
kp_sublords(kp_pos, houses=kp_hs)  # dict planet→sublord + "cusps" key (12 dicts)
```

Sub-division is Vimshottari-proportional (star → sub → sub-sub). **Pitfall:** must use the `krishnamurti` ayanamsa, not `lahiri` — the two differ by ~5-6' and change sub-lords near boundaries.

### Jaimini

```python
chara_karakas(sid)                 # 7 karakas [{karaka, planet, degree_in_sign}]; AK first
chara_karakas(sid, include_rahu=True)  # 8-karaka scheme (+ Karmakaraka)
karakamsa(sid)                     # {atmakaraka, karakamsa_sign, ...} (D9 sign of AK)
jaimini_aspects(sign)              # list of 3 sign indices (Rasi Drishti)
arudha_pada(sid, ws)               # dict 1..12 → {house, lord, arudha_sign, ...}
jaimini_yogas(sid, ws)             # list [{name, description}] (AK/AmK Raja Yoga)
```

Chara karakas rank planets by **degree within sign** (highest = Atmakaraka). Rahu is excluded from the 7-karaka scheme; pass `include_rahu=True` for the 8-karaka scheme.

### Lal Kitab dasha

```python
lal_kitab_dasha(birth)   # 7 dicts {lord, start_date, end_date, duration_years=5}
```

35-year cycle (Saturn→Jupiter→Mars→Sun→Venus→Mercury→Moon, 5y each), starting from the weekday lord. Simplified progression table — document as such.

## Shadbala (shadbala.py)

```python
from astrologica.shadbala import shadbala
sb = shadbala(birth, sid, ws)   # positions + houses optional (auto-computed)
# sb[planet] = {sthana: {uccha, saptavargaja, ojayugma, kendradi, drekkana, total},
#               dig, kala: {...components, total}, cheshta, naisargika, drik,
#               total_virupas, total_rupas, ishta, kashta}
```

Six-fold strength per B.V. Raman: Sthana, Dig, Kala, Cheshta, Naisargika, Drik — each in virupas (1/60 rupa). `total_rupas = total_virupas / 60`. Only the 7 classical planets are scored (no Rahu/Ketu/outers).

**Pitfalls:** (1) Naisargika bala is FIXED — Sun 60 > Moon 51.43 > Venus 42.86 > Jupiter 34.29 > Mercury 25.71 > Mars 17.14 > Saturn 8.57 (sums 240). (2) Saptavargaja uses natural friendship only (moolatrikona 45, own 30, mitra 15, sama 7.5, shatru 3.75) — NOT the compound five-fold friendship. (3) Ishta/Kashta = √(uccha·cheshta) and √((60−uccha)·(60−cheshta)).

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
- Yogini (Moon Shatabhisha #24): first **Dhanya** (3y, balance 1.19y) → Bhramari → Bhadrika → Ulka → Siddha → Sankata → Mangala → Pingala
- Kalachakra (Moon Shatabhisha p3, Apasavya group): first **Capricorn** (4y, balance 2.35y) → Sagittarius(10) → Aries(7) → Taurus(16) → Gemini(9) → Cancer(21) → Leo(5) → Virgo(9) → Libra(16)
- KP (krishnamurti ayanamsa): Moon Shatabhisha → star_lord Rahu, sub_lord **Ketu**, sub_sub Rahu
- Chara karakas (7): AK **Venus** (28.16°), AmK Mercury (21.96°), BK Moon (14.80°), MK Mars (14.45°), PK Jupiter (12.67°), GK Saturn (7.38°), DK Sun (2.91°)
- Karakamsa: AK Venus → navamsa **Gemini** (sign 2)
- Jaimini aspect Aries(0) → [Leo 4, Scorpio 7, Aquarius 10]; Taurus(1) → [Cancer 3, Libra 6, Capricorn 9]
- Arudha AL (house 1) → **Libra**
- Lal Kitab: starts **Venus** (Friday), 7 × 5y → Mercury, Moon, Saturn, Jupiter, Mars, Sun
- Shadbala rupas: Sun 9.61, Moon 9.24, Mars 6.67, Mercury 6.15, Jupiter 9.12, Venus 8.12, Saturn 8.19 · Ishta: Sun 49.56, Moon 51.22, Venus 52.36 · Kashta: Mars 13.28 (only planet with kashta > 0)
- Shadbala invariant: Sun in Leo sthana 262.08 > Sun in Aquarius 247.92
- Varga D2 (Hora) fixed: odd sign 0-15°→Leo, 15-30°→Cancer; even reversed · D30 (Trimsamsa) 5 unequal parts (Mars/Saturn/Jupiter/Mercury/Venus)

## Rules

- Every reading: all 14 sidereal bodies incl. Rahu/Ketu/Chiron/Lilith, each with sign, degree, nakshatra+pada, house (`ws.house_of`), Rx marker.
- Lagna = whole-sign sidereal ASC sign (Leo for the gold birth); never mix tropical ASC (Virgo 17.95) into a Vedic reading.
- `vimshottari_dasha`/`ashtottari_dasha` do NOT compute the Moon/Sun themselves — always pass the sidereal longitude explicitly.
