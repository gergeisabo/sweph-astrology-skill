---
name: pyswisseph-pitfalls
description: "Use when building astrology engines with pyswisseph."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [astrology, swisseph, pyswisseph, ephemeris, python, pitfalls]
    category: astrology
---

# Pyswisseph Pitfalls

## When to Use

Any time you write Python code using `swisseph` (pyswisseph) for astrological calculations. These are silent-failure pitfalls — the functions accept wrong parameters without errors and return wrong results.

Hard-won API quirks discovered while building [sweph-astrology](https://github.com/gergeisabo/sweph-astrology). Every one of these cost real debugging time. Read before writing any pyswisseph code.

## 1. swe.rise_trans constants — NOT 0, 1, 2

The `rsmi` parameter does NOT use sequential integers. The constants are:

```python
swe.CALC_RISE = 1      # NOT 0
swe.CALC_SET = 2       # NOT 1
swe.CALC_MTRANSIT = 4  # NOT 2 (upper meridian transit)
swe.CALC_ITRANSIT = 8  # NOT 4 (lower meridian transit)
```

Using `rsmi=0` for rise silently returns the WRONG time (transit time). Using `rsmi=1` for set returns rise time. The function does NOT raise an error for invalid values.

**Fix:**
```python
rise_jd = swe.rise_trans(jd, swe.SUN, rsmi=swe.CALC_RISE, geopos=geo)[1][0]
set_jd = swe.rise_trans(jd, swe.SUN, rsmi=swe.CALC_SET, geopos=geo)[1][0]
```

## 2. swe.rise_trans geopos order — [lon, lat, alt]

The `geopos` parameter is **longitude first**, not latitude first:

```python
# WRONG — silently returns wrong times
geo = (48.2264, 22.0847, 0)  # lat, lon — WRONG

# CORRECT
geo = (22.0847, 48.2264, 0)  # lon, lat, alt
```

This is counterintuitive because most GPS conventions use (lat, lon). The function accepts both orderings without error — it just computes wrong results for the wrong order.

## 3. swe.fixstar_ut return format — tuple of 3

The return is NOT `(position_tuple, flags)`. It's a 3-element tuple:

```python
result = swe.fixstar_ut("Regulus", jd, swe.FLG_SWIEPH | swe.FLG_SPEED)
pos_tuple = result[0]   # (lon, lat, dist, speed_lon, speed_lat, speed_dist)
name_str = result[1]    # "Regulus,alLeo" — star name + Bayer designation
flags = result[2]       # ephemeris flags
```

Access longitude as `result[0][0]`, not `result[0]` directly. The name string includes the Bayer designation after a comma.

## 4. swe.sol_eclipse_when_glob / swe.lun_eclipse_when return format

The return is `(rflag, (jd_tuple))`, NOT `(jd, flags)`:

```python
res = swe.sol_eclipse_when_glob(jd, swe.FLG_SWIEPH)
ecl_flags = res[0]       # integer — eclipse type flags
ecl_jd = res[1][0]       # JD of maximum eclipse (first element of tuple)
```

The flags are at `res[0]`, the JDs are at `res[1]`. The `res[1]` tuple has 10 elements (max eclipse, first contact, etc.).

Eclipse type constants:
```python
swe.ECL_TOTAL = 4
swe.ECL_ANNULAR = 8
swe.ECL_PARTIAL = 16
swe.ECL_PENUMBRAL = 64
```

## 5. sefstars.txt required for fixed stars

`swe.fixstar_ut()` **requires** `ephe/sefstars.txt` — it does NOT use a built-in catalog. Without it:

```
swisseph.Error: swisseph.fixstar_ut: SwissEph file 'sefstars.txt' not found in PATH
```

Download from the official Swiss Ephemeris GitHub:
```bash
curl -L -o ephe/sefstars.txt \
  https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sefstars.txt
```

The file is ~600KB, contains ~1600 lines of star data. It must be in the same directory as the other `.se1` ephemeris files.

## 6. swe.calc_ut with FLG_EQUATORIAL

To get declination (needed for parallels, shadbala, etc.):

```python
res, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_EQUATORIAL)
ra = res[0]       # right ascension
declination = res[1]  # declination
```

Without `FLG_EQUATORIAL`, `res[1]` is ecliptic latitude, NOT declination.

## 7. Sidereal mode — manual subtraction preferred

Two approaches exist:
- **(A) Manual:** `sidereal = (tropical - swe.get_ayanamsa(jd)) % 360`
- **(B) Flag:** `swe.set_sid_mode(SIDM_LAHIRI)` + `FLG_SIDEREAL`

Approach A is preferred because:
- It's stateless (no library-side state to leak between calls)
- It's deterministic (same inputs always produce same outputs)
- `set_sid_mode()` persists in library state and can conflict with other code

**Never read tropical values as sidereal.** This caused a multi-day bug in sweph-astrology where Astro Seek comparisons were wrong because the code assumed tropical when Astro Seek showed sidereal.

## 8. House system byte codes

```python
HOUSE_SYSTEMS = {
    "placidus": b"P",
    "koch": b"K",
    "whole_sign": b"W",
    "equal": b"E",
    "campanus": b"C",
    "regiomontanus": b"R",
    "porphyry": b"O",
}
```

Must be bytes, not strings. `b"P"` not `"P"`.

## 9. Helio/Heliocentric flag

```python
res, _ = swe.calc_ut(jd, swe.VENUS, swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_HELCTR)
```

`FLG_HELCTR` computes heliocentric positions. Sun is excluded (it's the center). Results are the same structure as geocentric but longitude is heliocentric.

## 10. Solar→lunar conversion (no built-in in pyswisseph)

pyswisseph has no lunar-calendar converter. Working approach (used in sweph-astrology's `astro` CLI): lunar day = days since last new moon + 1; lunar month = new moons since the new moon in the Jan 20–Feb 20 window (Chinese New Year rule). Find new moons by walking the Sun–Moon elongation `(moon-sun) % 360` back in 0.25-day steps until it wraps >360→small, then bisect on `elong(mid) > 180`. Sanity check: 1991-02-15 must give lunar M1 D1 (CNY was Feb 15, 1991, Xin Wei year).

## 11. Entry-point scripts with uv venvs

`uv`-created venvs have no `pip` — install a project's `[project.scripts]` entry point with `uv pip install -e . --python .venv/bin/python`. The console script then appears in `.venv/bin/`.
