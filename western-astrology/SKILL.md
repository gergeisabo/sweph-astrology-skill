---
name: western-astrology
description: "Use when computing Western tropical astrology — natal charts, aspects, dignities, transits, synastry, solar return, progressions, profections, firdaria, eclipses, ACG. Runs live local astrologica engine."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [astrology, western, natal, transits, timing]
    category: astrology
    related_skills: [astrologica]
---

# Western Astrology (astrologica)

Tropical Western system. Engine: `~/Projects/astrologica`, run with `~/Projects/astrologica/.venv/bin/python` (no pip in venv), cwd `~/Projects/astrologica`.

```python
from astrologica.core import BirthData, compute_positions, compute_houses
from astrologica.western import (natal_chart, aspects, essential_dignities,
    transits, synastry, solar_return, progressions)

birth = BirthData("1991-02-15", "18:45:00", 48.2264, 22.0847,
                  tz="Europe/Budapest", place="Kisvárda")
pos = compute_positions(birth)          # tropical, 14 keys (Rahu/Ketu NOT "North Node")
houses = compute_houses(birth)          # Placidus; .house_of(lon) is the ONLY house assigner
```

## Core (western.py)

| Call | Signature | Returns |
|---|---|---|
| `natal_chart(birth, house_system="placidus")` | full chart | keys: `planets, houses, aspects, dignities, chart_point` |
| `aspects(pos, orbs=None)` | Ptolemaic pairs | list of `{planet1, planet2, type, orb, applying}` |
| `essential_dignities(pos)` | traditional rulerships | `{planet: 'Domicile'|'Exalted'|'Detriment'|'Fall'|None}` |
| `transits(birth, "2026-03-01", orb=1.0)` | date str or datetime | keys: `transit_date, transit_positions, natal_positions, aspects` |
| `synastry(birth1, birth2)` | cross-chart | keys: `chart1_planets, chart2_planets, aspects, house_overlays` (person-2 planet → house in chart 1) |
| `solar_return(birth, 2026)` | year int | keys: `year, datetime, planets, houses, natal_sun_longitude, return_sun_longitude` (no ASC key — read `houses`) |
| `progressions(birth, "2026-02-15")` | secondary (day=a year) | keys: `progressed_positions, progressed_houses, target_date, years_elapsed` |

## Extended (western_ext.py)

| Call | Signature | Returns |
|---|---|---|
| `midpoints(pos)` | all pairs | `{"Sun/Moon": 119.26, ...}` (91 pairs for 14 points) |
| `fixed_stars(birth, stars=None, aspect_orb=2.0)` | star aspects | list of `{star, longitude, sign, degree_in_sign, aspects}` |
| `moon_phase(birth)` | takes BirthData (NOT pos) | `{angle, phase_name, phase_index, illumination_pct, sun_sign, moon_sign}` |
| `sun_times(birth)` | rise/set/noon | `{sunrise, sunset, solar_noon, day_length_hours}` (UTC strings) |
| `planetary_hours(birth)` | Chaldean order | 12 dicts `{hour, period, ruler, start_jd, end_jd}` |
| `moon_void_of_course(birth)` | 48h lookahead | `{is_void_of_course, moon_sign, moon_longitude, last_aspect_jd}` |
| `element_balance(pos)` | takes pos dict | `{elements, modes, total_planets, dominant_element, dominant_mode}` |
| `declination_parallels(birth, orb=1.0)` | parallels | list of `{type: 'parallel'|'contra-parallel', planet1, planet2, decl1, decl2, orb}` |
| `sabian(degree)` | 0-360 longitude (truncates) | `{degree, sign, degree_in_sign, element, modality, symbol}` — neutral gloss (Rudhyar/Jones text is copyright-encumbered; JSON at `astrologica/data/sabian_symbols.json`, 360 entries) |

## Timing (timing.py)

| Call | Signature | Returns |
|---|---|---|
| `profections(birth, target_age=35)` | omit age → full table | `{age, activated_house, profection_sign, profection_sign_index, profection_lord}` |
| `firdaria(birth)` | auto day/night (Sun house 7-12=day) | list `{ruler, start_age, end_age, duration_years, sub_periods_count}` — night sequence here |
| `eclipses("2026-01-01", "2026-12-31")` | date range | list `{type: solar|lunar, date_utc, subtype, jd}` |
| `retrograde_periods("Mercury", "2026-01-01", "2026-12-31")` | planet + range | list `{type: retrograde_start|retrograde_end|direct, date_utc, planet, longitude, sign}` |
| `ingresses("Jupiter", "2026-01-01", "2026-12-31")` | planet + range | list `{date_utc, planet, from_sign, to_sign}` |
| `transit_calendar(birth, 2026, 3, major_orb=3.0)` | year+month | per-day list `{date, aspects: [{transit, natal, aspect, orb, applying}]}` |
| `solar_arc(birth, target_age)` | Naibod key (~0.9856°/yr) | `{type, key, target_age, arc_degrees, arc_per_year, directed_positions}` — natal+age×arc. Distinct from `symbolic_directions` (exact 1°/yr) |
| `primary_directions(birth, target_age)` | Placidus semi-arc | `{type, method, target_age, directed_asc, directed_asc_sign, directed_mc, directed_mc_sign}` — MC directed 1° RA/yr (Ptolemy); ASC via oblique ascension |
| `primary_direction(birth, "Sun", "MC")` | Placidus semi-arc | `{arc_degrees, directed_age, directed_date_utc, promissor_ra, promissor_declination, ramc, ascensional_difference, diurnal_semi_arc, nocturnal_semi_arc, meridian_distance, proportional_part}` — arc = (RAMC − RA) mod 360; Ptolemy key 1° RA = 1 year |
| `ascensional_difference(decl, lat)` / `semi_arcs(decl, lat)` | spherical trig | AD = asin(tan δ · tan φ); DSA = 90°+AD, NSA = 90°−AD |

## Horary & Electional (horary.py)

```python
from astrologica import horary
from datetime import datetime, timezone
moment = datetime(2026, 3, 15, 14, 30, tzinfo=timezone.utc)
place = (47.4979, 19.0402)          # (lat, lon)

horary.horary_chart(question, moment, place)
#   moment: tz-aware datetime OR BirthData. Returns:
#   {question, moment_utc, ascendant, ascendant_longitude,
#    querent: {lord, sign, dignity}, quesited: {lord, sign, dignity},
#    moon: {sign, degree_in_sign, void_of_course, aspects, next_aspect},
#    significator_aspects, receptions, antiscia, verdict}
#   L1 = ruler of Asc, L7 = ruler of 7th (quesited); Moon = co-significator.
#   verdict weighs several testimonies (not just one aspect test):
#     +2 applying L1-L7 aspect, -1 separating; +3 mutual reception between
#     significators, +1 reception by sign; +1 Moon's next aspect to a
#     significator; +1 antiscion contact; -2 Moon void-of-course.
#   receptions: [{type: mutual_reception|reception, ...}] (traditional
#     domicile, 7 planets). antiscia: antiscion-of-one-significator falls on
#     the other (3° orb). next_aspect: Moon's next applying major aspect.

horary.electional_scan(activity, from_date, to_date, place, hour=12)
#   activity in: marriage, business, money, surgery, travel, house, study, general
#   casts noon chart daily; scores Moon sign (favourable list) + not-VOC.
#   Returns {activity, favourable_moon_signs, from_date, to_date, place,
#            candidates (sorted by score desc), best_date}.
#   VOC days always excluded. Reuses western_ext.moon_void_of_course.
```

## Astro*cartography (astrogeo.py) & Hellenistic (hellenistic.py)

```python
from astrologica.astrogeo import acg_lines, relocation_chart
acg_lines(birth, planets=["Sun","Moon"], step_deg=2.0)
#   {"Sun": [{"longitude": -158.14, "angle": "ASC", "planet_longitude": 326.54, "sign": "Aquarius"}, ...]}
relocation_chart(birth, target_lat=51.5074, target_lon=-0.1278)
#   keys: asc_sign, ascendant, houses, mc, mc_sign, positions, original/relocation_location

from astrologica.hellenistic import (hermetic_lots, zodiacal_releasing_from_fortune,
    zodiacal_releasing_lot)
is_day = houses.house_of(pos["Sun"].longitude) in {7,8,9,10,11,12}   # REQUIRED bool
hermetic_lots(pos, houses, is_day)      # {Fortune, Spirit, Eros, Necessity, Courage, Victory}
zodiacal_releasing_lot(pos, houses, is_day)   # (lot_name, lot_longitude, lot_sign) —
    #   Spirit by day, Fortune by night (the sect light's lot).  Both = ASC+Sun−Moon.
zodiacal_releasing_from_fortune(pos, houses, is_day, max_level=2)
    #   list of 12 L1 dicts {level, sign, sign_index, start_year, end_year,
    #   duration_years, ruler, sub_periods}.  Full ZR:
    #   * L1 sign period = its domicile ruler's minor years — Mars 15, Venus 8,
    #     Mercury 20, Moon 25, Sun 19, Jupiter 12, Saturn 27 (Capricorn) / 30
    #     (Aquarius, the Valens adjustment).  Cycle = 211 years.
    #   * L2 sub_periods run zodiacally from the L1 sign, minor-years in MONTHS,
    #     with a Loosing of the Bond (sub_periods[i]["loosing_of_bond"]) in each
    #     L1 sign whose period > ~17.58y (Leo/Virgo/Gemini/Cancer/Capricorn/
    #     Aquarius): the sequence jumps to the opposite sign instead of repeating.
```

**is_day is required by the hellenistic functions.** This gold birth: Sun in H6 → **night chart, `is_day=False`** → ZR releases from the Lot of **Fortune** (Virgo 6.05°). L1 = Virgo 0-20 (**Mercury**), not Venus.

## CLI

```bash
cd ~/Projects/astrologica
.venv/bin/astro natal                    # gold profile: full tropical chart + cusps
.venv/bin/astro timing --age 35          # profections + firdaria + returns
.venv/bin/astro transits [YYYY-MM-DD]    # default = today
.venv/bin/astro svg natal [out.svg]      # SVG wheel (also: svg vedic)
```

## Gold verification (1991-02-15 18:45, Kisvárda — all values from live runs)

- Tropical Sun **Aquarius 26.54°** (H6); ASC **Virgo 17.95°** (167.95°); MC Gemini 14.86° (74.86°)
- aspects: 26 found, e.g. Sun square Pluto orb 6.18 separating
- essential_dignities: Sun Detriment, Venus Exalted, Saturn Domicile (rest None)
- solar_return(2026): 2026-02-15 05:39:48 UTC
- progressions to 2026-02-15: years_elapsed 35.0, progressed Sun **Aries 1.60°**
- synastry vs 1990-06-21 London: 77 cross-aspects; overlays Sun→H10, Moon→H9
- moon_phase: New Moon (angle 11.9°, 1.1% illum) · element_balance: Water dominant (35.7%), mode Cardinal
- planetary_hours[0]: Saturn (day 1) · voc: False (Moon Pisces 338.44°)
- profections(35): house 12, Leo, lord Sun · firdaria age 35: Mars (32-39); first period Moon (0-9, night seq)
- eclipses 2026: 4, first solar annular 2026-02-17 12:11 UTC · Mercury Rx 2026: 6 events, first start 2026-02-26 06:47 Pisces
- Jupiter ingress 2026: Cancer→Leo 2026-06-29 · transit_calendar Mar 2026: 31 days
- acg Sun ASC line at lon -158.14 (Aquarius) · relocation to London: ASC 152.83° (Leo 2.83°)
- hermetic_lots(night): Fortune 156.05, Spirit 179.85, Eros 356.00, Necessity 153.37, Courage 40.88, Victory 342.66
- ZR (night, Fortune Virgo 6.05°): L1 Virgo 0-20 Mercury → Libra 8 → Scorpio 15 → Sagittarius 12 → Capricorn 27 → Aquarius 30 → Pisces 12 → Aries 15 → Taurus 8 → Gemini 20 → Cancer 25 → Leo 19 (cycle 211y). LB (→ opposite sign) in Virgo→Pisces, Capricorn→Cancer, Aquarius→Leo, Gemini→Sagittarius, Cancer→Capricorn, Leo→Aquarius
- solar_arc(1): arc 0.985647° (Naibod) · solar_arc(88): 86.737° ≈ HD's 88° offset
- primary_direction(Sun→MC): arc 104.796° (age 104.8, ~2095-12). AD −14.576°, DSA 75.424°, NSA 104.576°, PP ≈ 1.00 (Sun near IC). RAMC = 73.567° (MC RA), Sun RA 328.771°
- horary 2026-03-15 14:30 UTC Budapest: ASC Virgo 150.33°, L1 Mercury (Virgo Detriment), L7 Jupiter (Pisces Exalted), Moon Aquarius not-VOC · receptions include Mercury(L1) received by Jupiter(L7) · verdict "inconclusive (reception by sign … ; separating aspect …)"
- electional marriage 2026-06-01..10 Budapest: 2 candidates, best 2026-06-07 (Pisces Moon)
- sabian(0): Aries 1° · sabian(88): Gemini 29° · sabian(359): Pisces 30°

## Rules

- Iterate `pos.items()` — never hardcode planet lists (Rahu/Ketu/Chiron/Lilith are real keys).
- House assignment ONLY via `houses.house_of(p.longitude)`.
- Reading mandate: never omit a point — all 14 bodies + ASC/MC + Fortune (+ Vertex via `swe.houses(...)[1][3]`), every Rx marker, every house.
