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

## Module Map

| Module | Functions | Use For |
|--------|-----------|---------|
| `core.py` | BirthData, compute_positions, compute_houses, PlanetPosition, Houses | Foundation — all other modules use this |
| `western.py` | natal_chart, aspects, essential_dignities, transits, synastry, solar_return, progressions | Western tropical astrology |
| `western_ext.py` | midpoints, antiscia, harmonics, draconic, heliocentric, composite, davison, fixed_stars, moon_phase, sun_times, planetary_hours, receptions, hyleg_alcochoden, almuten, moon_void_of_course, gauquelin_sectors, lunation_phase, element_balance, declination_parallels | Extended Western techniques |
| `timing.py` | profections, firdaria, tertiary/minor_progressions, symbolic/primary_directions, lunar/solar/planetary_return, ingresses, retrograde_periods, eclipses, transit_calendar, forecast_calendar | Predictive timing |
| `astrogeo.py` | acg_lines, local_space_lines, geodetic_chart, parans, relocation_chart | Astrocartography & relocation |
| `vedic.py` | nakshatra, vimshottari_dasha, ashtottari_dasha, panchang, varga_chart, yogas, doshas, vedic_chart | Vedic (Jyotish) astrology |
| `vedic_ext.py` | ashtakoota, dashakoota, muhurat_scan, ashtakavarga_bav, sav | Vedic compatibility, muhurat, ashtakavarga |
| `bazi.py` | four_pillars, day_master, ten_gods, luck_pillars, element_balance | Chinese Four Pillars |
| `hd.py` | compute (→ HumanDesignChart), gate_at_longitude | Human Design |
| `hd_ext.py` | hd_transits, hd_compatibility, incarnation_cross, hd_circuitry, design_date | Extended Human Design |
| `ziwei.py` | ziwei_chart | Zi Wei Dou Shu (Purple Star) |
| `destiny.py` | compute_destiny | Destiny Matrix (Ladini) |
| `mayan.py` | tzolkin, haab, long_count, dreamspell | Mayan calendar |
| `numerology.py` | pythagorean, chaldean, kabbalistic, vedic | Numerology systems |
| `divination.py` | tarot_daily, tarot_spread, iching, runes, geomancy | Divination |
| `hellenistic.py` | hermetic_lots, egyptian_bounds, zodiacal_releasing_from_fortune | Hellenistic techniques |
| `render.py` | western_wheel_svg, vedic_wheel_svg, aspect_grid_svg, transit_calendar_markdown, muhurat_markdown, save_svg | SVG/Markdown output |

## Critical Rules

1. **ALWAYS ask for birth data first** — never guess or use placeholders
2. **Sidereal vs Tropical**: `compute_positions(birth, sidereal=True)` for Vedic/Jyotish; default is tropical for Western
3. **Timezone**: always use IANA tz (e.g. "Europe/Budapest"), not UTC offset
4. **Coordinates**: lat/lon in decimal degrees (positive=N/E, negative=S/W)
5. **Time format**: "HH:MM:SS" (include seconds)
6. **House system**: default is Placidus; pass `system="whole_sign"` for Vedic

## Verification Reference

Birth data: 1991-02-15 18:45 CET, Kisvárda (48.2264°N, 22.0847°E)
- Sidereal Sun: Aquarius ~2.81° (Lahiri ayanamsa)
- Sidereal Moon: Aquarius ~14.71°
- Tropical ASC: Virgo ~17.95°
- Ayanamsa Lahiri 1991-02-15: ~23.7331°
- 146 core tests + 115 extension tests = 261 total (all green)

## Pitfalls

- FLG_SIDEREAL: use manual subtraction (tropical - ayanamsa) not swe.FLG_SIDEREAL flag
- swe.rise_trans: rsmi uses swe.CALC_RISE=1, swe.CALC_SET=2, swe.CALC_MTRANSIT=4 (NOT 0,1,2)
- swe.rise_trans geopos: [lon, lat, alt] — NOT [lat, lon, alt]
- swe.fixstar_ut: needs ephe/sefstars.txt file (downloaded from aloistr/swisseph GitHub)
- BaZi formulas: month1_stem = ((year_stem % 5) * 2 + 2) % 10; zi_stem = ((day_stem % 5) * 2 + 2) % 10

## Running

```bash
cd ~/Projects/astrologica
source .venv/bin/activate  # or: .venv/bin/python
python -m pytest tests/ -q  # expect 261 passed
```
