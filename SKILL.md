---
name: astrologica
description: "Local astrology engine — Western, Vedic, BaZi, HD, Divination, Numerology, Mayan, Destiny Matrix, Zi Wei, timing/transits, muhurat. No API needed."
version: 2.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [astrology, vedic, western, bazi, human-design, tarot, numerology, mayan]
    category: astrology
---

# Astrologica — Local Astrology Engine

Fully local astrology computation engine. No external API calls, no rate limits, no credits.

## When to Use

User asks for: natal chart, transits, synastry, compatibility, muhurat (electional timing), vedic chart, dasha, bazi four pillars, human design, tarot, numerology, mayan calendar, destiny matrix, zi wei dou shu, profections, firdaria, eclipses, astrocartography, or any astrological calculation.

## Quick Start

```python
from astrologica.core import BirthData, compute_positions, compute_houses
from astrologica.western import natal_chart, aspects, transits, synastry
from astrologica.vedic import nakshatra, vimshottari_dasha, panchang
from astrologica.bazi import four_pillars
from astrologica.hd import compute as hd_compute

# ALWAYS ask for birth data first: date, time, lat, lon, tz
birth = BirthData("1991-02-15", "18:45:00", 48.2264, 22.0847,
                  tz="Europe/Budapest", place="Kisvárda")

# Planetary positions (tropical)
pos = compute_positions(birth)  # dict of PlanetPosition objects

# Sidereal (Lahiri ayanamsa)
sid = compute_positions(birth, sidereal=True)

# Houses
houses = compute_houses(birth)  # .cusps, .ascendant, .mc, .house_of(lon)

# PlanetPosition attributes: .name, .longitude, .latitude, .speed, .retrograde,
#   .sign (0-11), .degree_in_sign, .sign_name (property), .dms() method
```

## Returned Dict Keys

`compute_positions()` returns exactly these 14 keys:

```
Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn,
Uranus, Neptune, Pluto, Rahu, Ketu, Chiron, Lilith
```

**Critical naming:**
- `Rahu` = North Node (NOT "North Node")
- `Ketu` = South Node (NOT "South Node") — computed as opposite of Rahu, not in PLANETS dict but added by compute_positions
- `Lilith` = Mean Black Moon Lilith (swe body 12)
- `Chiron` = centaur Chiron (swe body 15)

**NEVER hardcode a planet name list.** Always iterate `pos.items()`:

```python
# CORRECT — works regardless of which keys exist
for name, p in pos.items():
    house = houses.house_of(p.longitude)
    retro = " Rx" if p.retrograde else ""
    print(f"{name:12s}: {p.sign_name} {p.degree_in_sign:.2f}{retro}  House {house}")

# WRONG — will silently skip Rahu/Ketu/Chiron/Lilith if names don't match
planet_order = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn',
                'Uranus','Neptune','Pluto','North Node']  # ← WRONG KEY NAMES
for name in planet_order:
    if name in pos:  # silently fails for North Node
        ...
```

**House assignment:** ALWAYS use `houses.house_of(planet.longitude)`. Never eyeball from cusp degrees — cusp boundaries are non-uniform in Placidus and visual estimation produces off-by-one house errors.

## Module Map

| Module | Functions | Use For |
|--------|-----------|---------|
| `core.py` | BirthData, compute_positions, compute_houses, PlanetPosition, Houses | Foundation — all other modules use this |
| `western.py` | natal_chart, aspects, essential_dignities, transits, synastry, solar_return, progressions | Western tropical astrology |
| `western_ext.py` | midpoints, antiscia, harmonics, draconic, heliocentric, composite, davison, fixed_stars, moon_phase, sun_times, planetary_hours, receptions, hyleg_alcochoden, almuten, moon_void_of_course, gauquelin_sectors, lunation_phase, element_balance, declination_parallels | Extended Western techniques |
| `timing.py` | profections, firdaria, tertiary/minor_progressions, symbolic/primary_directions, lunar/solar/planetary_return, ingresses, retrograde_periods, eclipses, transit_calendar, forecast_calendar | Predictive timing |
| `astrogeo.py` | acg_lines, local_space_lines, geodetic_chart, parans, relocation_chart | Astrocartography & relocation |
| `vedic.py` | nakshatra, vimshottari_dasha, ashtottari_dasha, panchang, varga_chart, yogas, doshas, vedic_chart | Vedic (Jyotish) astrology |
| `vedic_ext.py` | ashtakoota, dashakoota, muhurat_scan, ashtakavarga_bav, sav | Vedic compatibility, muhurat, ashtakavarga (full Parasara BAV; pass houses= for Lagna; SAV=337) |
| `bazi.py` | four_pillars, day_master, ten_gods, luck_pillars, element_balance | Chinese Four Pillars |
| `hd.py` | compute (→ HumanDesignChart), gate_at_longitude | Human Design (incl. Rave Variables: determination, environment, motivation, perspective, sense, cognition) |
| `hd_ext.py` | hd_transits, hd_compatibility, incarnation_cross, hd_circuitry, design_date | Extended Human Design |
| `ziwei.py` | ziwei_chart | Zi Wei Dou Shu: 14 main + 16 minor stars, year-stem sihua (Lu/Quan/Ke/Ji). Lunar month/day/hour. |
| `destiny.py` | compute_destiny | Destiny Matrix (Ladini) |
| `mayan.py` | tzolkin, haab, long_count, dreamspell | Mayan calendar |
| `numerology.py` | full_profile, life_path_number, birthday_number, attitude_number, personal_year, name_number, soul_urge_number, personality_number, vedic_number | Numerology systems (there is NO `pythagorean()` — use `full_profile(name, date_str)`) |
| `divination.py` | tarot_daily, tarot_spread, iching, runes, geomancy | Divination |
| `hellenistic.py` | hermetic_lots, egyptian_bounds, zodiacal_releasing_from_fortune | Hellenistic techniques |
| `render.py` | western_wheel_svg(planets_dict, cusps_list, asc), vedic_wheel_svg(planets_dict, cusps_list), aspect_grid_svg, transit_calendar_markdown, muhurat_markdown, save_svg | SVG/Markdown output |
| `cli.py` | `astro` console script (main) | Terminal access to everything below |

## Critical Rules

1. **ALWAYS ask for birth data first** — never guess or use placeholders
2. **Sidereal vs Tropical**: `compute_positions(birth, sidereal=True)` for Vedic/Jyotish; default is tropical for Western
3. **Timezone**: always use IANA tz (e.g. "Europe/Budapest"), not UTC offset
4. **Coordinates**: lat/lon in decimal degrees (positive=N/E, negative=S/W)
5. **Time format**: "HH:MM:SS" (include seconds)
6. **House system**: default is Placidus; pass `system="whole_sign"` for Vedic

## Command Line (CLI)

Installed as console script `astro` (or `.venv/bin/astro`, or `.venv/bin/python -m astrologica.cli`). Birth data via `--profile`, explicit flags, or the `gold` profile default (Gergely, 1991-02-15 18:45 Kisvárda).

```bash
cd ~/Projects/astrologica
.venv/bin/astro natal [--sidereal] [--whole-sign] [--profile NAME | --date D --time T --lat N --lon N --tz TZ]
.venv/bin/astro hd                       # Human Design incl. Variables
.venv/bin/astro vedic                    # Lahiri: planets + nakshatras + dasha
.venv/bin/astro bazi                     # Four Pillars JSON
.venv/bin/astro ziwei                    # Zi Wei (solar→lunar conversion built in, note printed)
.venv/bin/astro mayan
.venv/bin/astro timing --age 35 [--solar-return]
.venv/bin/astro numerology --name "Full Name" [--year 2026]
.venv/bin/astro transits [YYYY-MM-DD]
.venv/bin/astro svg natal|vedic [out.svg]
.venv/bin/astro profiles list | add NAME --date .. --time .. --lat .. --lon .. --tz .. [--place ..]
.venv/bin/astro selftest                 # gold-data sanity checks, exit 1 on fail
```

Profiles live in `~/.config/astro/profiles.json`. `--profile` works in ANY position (`astro hd --profile gold` == `astro --profile gold hd`).

## Verification Reference

Birth data: 1991-02-15 18:45 CET, Kisvárda (48.2264°N, 22.0847°E)
- Sidereal Sun: Aquarius ~2.81° (Lahiri ayanamsa)
- Sidereal Moon: Aquarius ~14.71°
- Tropical ASC: Virgo ~17.95°
- Ayanamsa Lahiri 1991-02-15: ~23.7331°
- 283 tests total (all green)

## Pitfalls

- FLG_SIDEREAL: use manual subtraction (tropical - ayanamsa) not swe.FLG_SIDEREAL flag
- swe.rise_trans: rsmi uses swe.CALC_RISE=1, swe.CALC_SET=2, swe.CALC_MTRANSIT=4 (NOT 0,1,2)
- swe.rise_trans geopos: [lon, lat, alt] — NOT [lat, lon, alt]
- swe.fixstar_ut: needs ephe/sefstars.txt file (downloaded from aloistr/swisseph GitHub)
- BaZi formulas: month1_stem = ((year_stem % 5) * 2 + 2) % 10; zi_stem = ((day_stem % 5) * 2 + 2) % 10
- `destiny.compute()` is a SIMPLER grid, not the Ladini chakra table — for Destiny Matrix use the `esoteric-computation` skill instead (verified: center E=11 Justice, tail D=10 Wheel for 1991-02-15; the engine gives different values)
- `ziwei_chart(year_stem, year_branch, lunar_month, lunar_day, hour_branch)` takes LUNAR month/day and indices, not BirthData; the CLI does the solar→lunar conversion (Swiss Ephemeris new-moon walk)
- Mayan functions (`tzolkin`, `haab`, `long_count`) take a DATE STRING, not BirthData

## Function Signature Notes

These functions have non-obvious signatures — check before calling:

| Function | Signature | Notes |
|----------|-----------|-------|
| `vimshottari_dasha` | `(birth, moon_longitude)` | Requires explicit sidereal Moon longitude as 2nd arg |
| `hermetic_lots` | `(pos, houses, is_day)` | `is_day` bool required (Sun below horizon = False) |
| `zodiacal_releasing_from_fortune` | `(pos, houses, is_day)` | Same `is_day` requirement |
| `moon_phase` | `(birth)` | Takes BirthData, NOT pos dict |
| `element_balance` | `(pos)` | Takes pos dict, NOT BirthData |
| `nakshatra` | `(longitude)` | Single float longitude; returns dict with keys: number, name, pada, ruler, deity, degree_in_nakshatra |

**Day/Night determination:** Sun below the ASC-DSC axis (houses 1-6 in a day chart = houses 7-12) means night chart. In Placidus: if Sun's house is 7-12 → day chart; houses 1-6 → night chart. For this birth: Sun in House 6 = night chart → `is_day=False`.

## Mandatory Output Checklist

When generating a natal chart reading, EVERY item below MUST appear in the output. No omissions, no shortcuts. Use `pos.items()` and `houses.house_of()` for all calculations — never hardcode or eyeball.

### Planetary Positions Table (all 14 points + ASC/MC)

```
ASC, MC, Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn,
Uranus, Neptune, Pluto, Rahu (North Node), Ketu (South Node),
Chiron, Lilith, Lot of Fortune, Vertex
```

For each point display: **sign, degree, retrograde marker (Rx or nothing), house number**.

- Retrograde: check `.retrograde` on every PlanetPosition — do NOT assume only outer planets go Rx. Nodes (Rahu/Ketu) and Chiron are frequently retrograde.
- House: always `houses.house_of(p.longitude)` — never estimate from cusp degrees.
- Fortune: compute via `hermetic_lots(pos, houses, is_day)` — requires day/night determination.
- Vertex: compute via `swe.houses(jd, lat, lon, b'P')` — it's in `ascmc[3]`.

### Additional mandatory sections
- Aspects (with orb and applying/separating)
- Element/Mode balance
- House cusps (all 12)

## Human Design Variables

The `compute()` function returns a `HumanDesignChart` with these Variable fields:

| Variable | Source | Field |
|---|---|---|
| Determination (Digestion) | Design Sun Color | `determination_color` |
| Environment | Design Nodes Color | `environment_color` |
| Motivation | Personality Sun Color | `motivation_color` |
| Perspective | Personality Nodes Color | `perspective_color` |
| Sense | Personality Sun Tone | `sense_tone` |
| Cognition | Design Sun Tone | `cognition_tone` |

**Critical: Nodes must use TRUE NODE** (not Mean Node) for Environment and Perspective.

**Determination/Environment variant** (Active/Passive): Tones 1-3 = Left/Active, Tones 4-6 = Right/Passive. Use `determination_tone` and `environment_tone` for this.

**Mapping dictionaries** (official IHDS/Jovian Archive names):
- Determination Colors: Appetite(1), Taste(2), Thirst(3), Touch(4), Sound(5), Light(6)
- Environment Colors: Caves(1), Markets(2), Kitchens(3), Mountains(4), Valleys(5), Shores(6)
- Motivation Colors: Fear(1), Hope(2), Desire(3), Need(4), Guilt(5), Innocence(6)
- Perspective Colors: Survival(1), Possibility(2), Power(3), Wanting(4), Probability(5), Personal(6)
- Sense Tones: Security(1), Uncertainty(2), Action(3), Meditation(4), Judgment(5), Acceptance(6)
- Cognition Tones: Smell(1), Taste(2), Outer Vision(3), Inner Vision(4), Feeling(5), Touch(6)

## Running

```bash
cd ~/Projects/astrologica
.venv/bin/python -m pytest tests/ -q  # expect 283 passed
```
