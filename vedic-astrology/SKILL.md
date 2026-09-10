---
name: vedic-astrology
description: "Use when computing Vedic/Jyotish charts, dasha, nakshatra, muhurat. Sidereal charts, Vimshottari/Ashtottari dasha, vargas, yogas, doshas, panchang, ashtakoota, ashtakavarga. Hungarian: védikus horoszkóp, jós."
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

ashtakoota(moon_nak1, moon_nak2)   # nakshatra NUMBERS (0-26); n1 = bride/girl, n2 = groom/boy
#   {total, max: 36, varna, vashya, tara, yoni, graha_maitri, gana, bhakoot, nadi,
#    person1_nakshatra, person2_nakshatra, verdict}

**Standard Guna Milan tables (no simplifications).**  Varna, Vashya, Graha
Maitri and Bhakoot are keyed to the **Moon sign** (each nakshatra's *principal*
rashi = sign of its first pada, `(n*4)//9`); Tara, Yoni, Gana and Nadi are
keyed to the nakshatra.  Varna (groom ≥ bride) and Vashya (bride × groom
matrix) are directional.  Point tables:

| Koota | Max | Rule |
|---|---|---|
| Varna | 1 | groom's varna ≥ bride's (Brahmin>Kshatriya>Vaishya>Shudra) |
| Vashya | 2 | 5-type matrix (Chatushpad/Jalachar/Vanchar/Keet/Dwipad) |
| Tara | 3 | bidirectional mod-9; Vipat(3)/Pratyari(5)/Vadha(7) malefic |
| Yoni | 4 | 14-animal matrix (4 same / 3 friend / 2 neutral / 1 / 0 enemy) |
| Graha Maitri | 5 | Moon-sign lords' natural friendship (5 same/friends, 4 f+n, 3 n+n, 1 f+e, 0.5 n+e, 0 e+e) |
| Gana | 6 | Deva/Manushya/Rakshasa (6 same, 5 D+M, 1 D+R, 0 M+R) |
| Bhakoot | 7 | sign distance: good 1/1, 1/7, 3/11, 4/10; bad 2/12, 5/9, 6/8 |
| Nadi | 8 | 3 nadis; different = 8, same = 0 (nadi dosha) |

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

35-year cycle (Saturn→Jupiter→Mars→Sun→Venus→Mercury→Moon, 5y each), starting from the birth weekday's ruler — the standard Lal Kitab graha dasha.

## Vedic Transits — Gochara (`gochara.py`)

CLI: `astro gochara [YYYY-MM-DD]` (added 2026-09-10). All positions sidereal (Lahiri).

```python
from astrologica.gochara import gochara, sade_sati, vedic_transit_report

g = gochara(birth, "2026-09-06")        # or datetime(...), or "today" (default)
# g['grahas'][name] = {transit_sign, transit_sign_index, degree_in_sign,
#   house_from_moon, house_from_lagna, retrograde, favorable_from_moon}
# g['natal_moon_sign'] (Janma Rashi), g['transit_moon_nakshatra']

s = sade_sati(birth, "2026-09-06")
# {active, phase 1|2|3, saturn_sign, house_from_moon,
#  phases: {phase: {description, start, end_estimated}}}  dates from ephemeris

r = vedic_transit_report(birth)          # gochara + sade_sati + SAV weighting
# r['sav_weighting'][name] = {sav_bindus_in_transit_sign, sav_verdict}
# classical 25-bindu rule: >25 auspicious, <25 challenging
```

**Benefic tables (favorable_from_moon)** — standard Gochara houses from natal Moon: Sun 3/6/10/11 · Moon 1/3/6/7/10/11 · Mars 3/6/11 · Mercury 2/4/6/8/10/11 · Jupiter 2/5/7/9/11 · Venus 1/2/3/4/5/8/9/11/12 · Saturn 3/6/11 · Rahu 3/6/10/11 · Ketu 3/6/11.

**Gold (2026-09-06, Moon Kumbha/Aquarius):** Saturn sidereal Pisces (entered 2025-03-29), H2 from Moon, Rx — **Sade Sati phase 3 active** (setting phase, until ~2027-06-02). Phase 1 was 2022-07-12→2023-01-17 (Saturn's 2nd Capricorn pass), phase 2 while on Aquarius. Jupiter Cancer H6 (unfavorable). Transit Moon Ardra pada 2. Saturn's transit sign has 29 SAV bindus (auspicious).

## Shadbala (shadbala.py)

```python
from astrologica.shadbala import shadbala
sb = shadbala(birth, sid, ws)   # positions + houses optional (auto-computed)
# sb[planet] = {sthana: {uccha, saptavargaja, ojayugma, kendradi, drekkana, total},
#               dig, kala: {...components, total}, cheshta, naisargika, drik,
#               total_virupas, total_rupas, ishta, kashta}
```

Six-fold strength per B.V. Raman: Sthana, Dig, Kala, Cheshta, Naisargika, Drik — each in virupas (1/60 rupa). `total_rupas = total_virupas / 60`. Only the 7 classical planets are scored (no Rahu/Ketu/outers).

**Pitfalls:** (1) Naisargika bala is FIXED — Sun 60 > Moon 51.43 > Venus 42.86 > Jupiter 34.29 > Mercury 25.71 > Mars 17.14 > Saturn 8.57 (sums 240). (2) Saptavargaja uses natural friendship only (moolatrikona 45, own 30, mitra 15, sama 7.5, shatru 3.75) — NOT the compound five-fold friendship. (3) Ishta/Kashta = √(uccha·cheshta) and √((60−uccha)·(60−cheshta)). (4) **Kala bala uses ACTUAL sunrise/sunset** via `swe.rise_trans` (CALC_RISE/CALC_SET): Nathonnatha, Tribhaga and Hora all split the real day/night length — a hora is 1/12 of the day (sunrise→sunset) or 1/12 of the night (sunset→sunrise), NOT a fixed clock hour. The vara (weekday) is anchored at sunrise, so a pre-dawn birth belongs to the previous day's vara. Gold birth (18:45 night) → hora lord **Sun**.

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
- ashtakoota(23, 10): total **20.5/36**, verdict 'Good match' (Shatabhisha × Purva Phalguni — gold Moon Shatabhisha = index 23)
- ashtakoota(7, 7): total **28/36** (Pushya × Pushya — published reference; both Madhya nadi → nadi 0)
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
- Shadbala rupas: Sun 9.21, Moon 8.91, Mars 6.33, Mercury 6.15, Jupiter 8.72, Venus 7.73, Saturn 7.85 · Ishta: Sun 49.56, Moon 51.22, Venus 52.36 · Kashta: Mars 13.28 (only planet with kashta > 0)
- Shadbala invariant: Sun in Leo sthana 262.08 > Sun in Aquarius 247.92
- Varga D2 (Hora) fixed: odd sign 0-15°→Leo, 15-30°→Cancer; even reversed · D30 (Trimsamsa) 5 unequal parts (Mars/Saturn/Jupiter/Mercury/Venus)

## Rules

- Every reading: all 14 sidereal bodies incl. Rahu/Ketu/Chiron/Lilith, each with sign, degree, nakshatra+pada, house (`ws.house_of`), Rx marker.
- Lagna = whole-sign sidereal ASC sign (Leo for the gold birth); never mix tropical ASC (Virgo 17.95) into a Vedic reading.
- `vimshottari_dasha`/`ashtottari_dasha` do NOT compute the Moon/Sun themselves — always pass the sidereal longitude explicitly.
