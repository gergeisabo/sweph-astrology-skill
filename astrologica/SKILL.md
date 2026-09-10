---
name: astrologica
description: "Use when any birth chart or astrological calculation is needed. Shared hub: birth data, positions, houses, CLI, gold birth; routes each system to its dedicated skill."
version: 3.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [astrology, hub, engine, positions, houses, cli]
    category: astrology
    related_skills: [western-astrology, vedic-astrology, bazi, human-design, ziwei, mayan, numerology, divination, destiny-matrix, astrology-readings]
---

# Astrologica — Shared Hub

Fully local astrology engine at `~/Projects/astrologica`. **No external API calls.**
This skill is the FOUNDATION only: birth data, planetary positions, houses, and the CLI.
For any specific system, load its dedicated skill — do NOT mix systems here.

## ROUTE FIRST — which skill handles what

| User wants… | Load THIS skill | CLI |
|---|---|---|
| Natal chart, aspects, transits, synastry, returns, profections/firdaria, eclipses, astrogeo | `western-astrology` | `astro natal / transits / timing / svg` |
| Vedic/Jyotish chart, nakshatra, dasha, panchang, yogas, doshas, muhurat, ashtakavarga | `vedic-astrology` | `astro vedic` |
| BaZi four pillars, ten gods, luck pillars, day master | `bazi` | `astro bazi` |
| Human Design chart, type/authority, gates, channels, Rave Variables | `human-design` | `astro hd` |
| Zi Wei Dou Shu | `ziwei` | `astro ziwei` |
| Mayan tzolkin/haab/long count/dreamspell | `mayan` | `astro mayan` |
| Life path / name numbers | `numerology` | `astro numerology` |
| Tarot, I Ching, runes, geomancy | `divination` | (no CLI) |
| Destiny Matrix (Ladini) chakras | `destiny-matrix` | (no CLI) |
| **Multi-system reading synthesis** | `astrology-readings` | — |

Load the routed skill for details, gold data, and pitfalls. This hub only gives the
shared mechanics every system needs.

## When to Use

User asks for any astrological calculation, OR you are about to dispatch to a per-system
skill and need the shared birth/position/house API and the standard birth-data questions.

## Quick Start (shared foundation)

```python
from astrologica.core import BirthData, compute_positions, compute_houses

# ALWAYS ask for birth data first: date, time, lat, lon, tz — never guess
birth = BirthData("1991-02-15", "18:45:00", 48.2264, 22.0847,
                  tz="Europe/Budapest", place="Kisvárda")

pos = compute_positions(birth)                # tropical dict
sid = compute_positions(birth, sidereal=True) # Lahiri ayanamsa (Vedic)
houses = compute_houses(birth)                # Placidus default
wh = compute_houses(birth, system="whole_sign", sidereal=True)  # Vedic
```

`PlanetPosition` attrs: `.name .longitude .latitude .speed .retrograde .sign (0-11)
.degree_in_sign .sign_name` and `.dms()`.

## Returned Dict Keys (all 14 — naming is critical)

```
Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn,
Uranus, Neptune, Pluto, Rahu, Ketu, Chiron, Lilith
```

- `Rahu` = North Node (NOT "North Node"); `Ketu` = South Node (computed as opposite of Rahu)
- **Node mode matters (~1.4°):** Rahu/Ketu default to the **MEAN** node — classical
  Jyotish convention, and what the reference chart quotes (Capricorn 26°42' = 296.713°).
  The TRUE node is 298.869° for the gold birth — a 1.1565° (69.4') gap. Override per call
  (`compute_positions(birth, node="true")`), per CLI (`--node true`), or env
  `ASTROLOGICA_NODE=true`. Always state which mode a published node used before calling
  it "wrong".
- `Lilith` = Mean Black Moon Lilith (swe body 12); `Chiron` = centaur Chiron (swe body 15)
- **NEVER hardcode a planet list** — iterate `pos.items()`, or Rahu/Ketu/Chiron/Lilith get silently skipped.
- **House = `houses.house_of(p.longitude)` ALWAYS** — never eyeball from cusps (Placidus cusps are non-uniform → off-by-one errors).

## Critical Rules

1. **ALWAYS ask for birth data first** — never guess or use placeholders.
2. **Tropical default for Western**; `sidereal=True` for Vedic/Jyotish.
3. **Timezone = IANA** (e.g. "Europe/Budapest"), never a UTC offset.
4. **Coordinates** lat/lon decimal degrees (positive N/E, negative S/W).
5. **Time format** "HH:MM:SS" (include seconds).
6. **House system**: default Placidus; `system="whole_sign"` for Vedic.

## Command Line (CLI)

Console script `astro` at `~/Projects/astrologica/.venv/bin/astro`
(also `.venv/bin/python -m astrologica.cli`). Birth data via a saved profile, explicit
flags, or the default `gold` profile. `--profile` works in any position.

```bash
cd ~/Projects/astrologica
.venv/bin/astro natal|vedic|hd|bazi|ziwei|destiny|mayan [flags]  # per-system
.venv/bin/astro gochara [YYYY-MM-DD]                         # Vedic transits + Sade Sati + SAV
.venv/bin/astro shadbala                                     # six-fold strength
.venv/bin/astro hd-transits [YYYY-MM-DD]
.venv/bin/astro astrogeo [--relocate LAT LON]                # ACG lines + parans
.venv/bin/astro horary --question "..." [--when "YYYY-MM-DD HH:MM:SS"]
.venv/bin/astro electional --activity marriage --from 2026-10-01 --to 2026-11-30
.venv/bin/astro natal --node true                            # Rahu/Ketu: mean (default) | true
.venv/bin/astro transits [YYYY-MM-DD]                        # transits for a date
.venv/bin/astro timing --age 35 [--solar-return]             # profections / returns
.venv/bin/astro numerology --name "Full Name"
.venv/bin/astro svg natal|vedic [out.svg]                    # chart wheel → SVG
.venv/bin/astro profiles list | add NAME --date .. --time .. --lat .. --lon .. --tz .. [--place ..]
.venv/bin/astro selftest                                     # gold-data checks, exit 1 on fail
```

Example for an arbitrary chart: `astro natal --profile NAME`, or
`astro natal --date 1985-03-20 --time 10:30:00 --lat 47.5 --lon 19.04 --tz Europe/Budapest`.
Profiles live in `~/.config/astro/profiles.json`.

## Gold Birth (default profile `gold` — Gergely Szabó)

- **1991-02-15 18:45 Europe/Budapest** (CET). UT 17:45. Kisvárda 48.2264 N, 22.0847 E.
- Tropical Sun **26.54° Aquarius** · Sidereal Sun **2.81° Aquarius** · Tropical ASC **Virgo 17.95°**
- Ayanamsa Lahiri 1991-02-15: **~23.7331°**
- Notes/docs: `/mnt/hdd/00-obsidian/ASTROLOGY/BIRTH CHART DATA.md`
- **Birth-time trap (do not reintroduce):** the only correct input is local **18:45** CET = 17:45 UT. Passing `17:45` as the *local* time silently computes a chart one hour early — sidereal Lagna **Leo 13.23°** instead of the correct **Leo 24.2°**, every house shifted. This bug was live in `tests/test_core_verify.py` until 2026-09-10 (fix commit 435e5ce); the suite passed while verifying the wrong sky because its expected values had been generated for the bad anchor.
- Feb 15 Sun is ~**26.54° Aquarius tropical**; **2.81° Aquarius is the SIDEREAL (Lahiri)** value — never mix the columns. `core.py`'s docstring had them swapped and was corrected 2026-09-10.

## Full Engine (module → dedicated skill)

Engine modules at `~/Projects/astrologica/astrologica/`:
`core.py` (this hub) · `cli.py` (this hub) · `render.py` (SVG/markdown; see western-astrology)
`western.py western_ext.py timing.py astrogeo.py hellenistic.py horary.py` → **western-astrology**
`vedic.py vedic_ext.py shadbala.py` → **vedic-astrology**
`bazi.py` → **bazi** · `hd.py hd_ext.py` → **human-design** · `ziwei.py` → **ziwei**
`mayan.py` → **mayan** · `numerology.py` → **numerology** · `divination.py` → **divination**
`destiny.py` (real Ladini matrix as of 2026-09-06) → **destiny-matrix**

## Mandatory Output Rule (all natal systems)

NEVER omit detail: every planet/point (incl. Rahu/Ketu/Chiron/Lilith/Fortune/Vertex), every
retrograde marker, every house assignment — all from computed values (`house_of()`),
never eyeballed or skipped.

## Tests

```bash
cd ~/Projects/astrologica
.venv/bin/python -m pytest tests/ -q  # expect 535 passed
```
