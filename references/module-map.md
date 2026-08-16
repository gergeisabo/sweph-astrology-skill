# Astrologica Module Map

Quick reference for which module to import for each task.

## Core
```python
from astrologica.core import BirthData, compute_positions, compute_houses
```

## Western
```python
from astrologica.western import natal_chart, aspects, transits, synastry, solar_return, progressions
from astrologica.western_ext import midpoints, harmonics, fixed_stars, moon_phase, sun_times, element_balance
```

## Timing
```python
from astrologica.timing import profections, firdaria, eclipses, transit_calendar, lunar_return, retrograde_periods
```

## Vedic
```python
from astrologica.vedic import nakshatra, vimshottari_dasha, panchang, varga_chart, yogas, doshas
from astrologica.vedic_ext import ashtakoota, muhurat_scan, ashtakavarga_bav
```

## Astrogeography
```python
from astrologica.astrogeo import acg_lines, relocation_chart, local_space_lines
```

## Chinese
```python
from astrologica.bazi import four_pillars, day_master, ten_gods, luck_pillars
from astrologica.ziwei import ziwei_chart
```

## Human Design
```python
from astrologica.hd import compute as hd_compute
from astrologica.hd_ext import hd_compatibility, incarnation_cross, hd_circuitry
```

## Other Systems
```python
from astrologica.destiny import compute_destiny
from astrologica.mayan import tzolkin, haab, long_count, dreamspell
from astrologica.numerology import pythagorean, chaldean, kabbalistic, vedic
from astrologica.divination import tarot_daily, tarot_spread, iching, runes, geomancy
from astrologica.hellenistic import hermetic_lots, egyptian_bounds, zodiacal_releasing_from_fortune
```

## Render
```python
from astrologica.render import western_wheel_svg, vedic_wheel_svg, aspect_grid_svg, transit_calendar_markdown, muhurat_markdown
```
