---
name: bazi
description: "Use when computing BaZi Four Pillars, Ten Gods, luck pillars, or element balance. Live-verified against the gold birth."
version: 1.0.0
metadata:
  hermes:
    tags: [bazi, four-pillars, chinese-astrology, ten-gods]
    category: astrology
    related_skills: [astrologica]
---

# BaZi (Four Pillars of Destiny) — `astrologica.bazi`

Engine: pure calendar math (no Swiss Ephemeris). Run with
`~/Projects/astrologica/.venv/bin/python`, cwd `~/Projects/astrologica`.
CLI: `.venv/bin/astro bazi` (gold profile default).

## Setup + gold birth (verified 2026-09)

```python
from astrologica.core import BirthData
from astrologica import bazi
birth = BirthData("1991-02-15", "18:45:00", 48.2264, 22.0847,
                  tz="Europe/Budapest", place="Kisvárda")
```

## API (all verified live)

- `bazi.four_pillars(birth) -> dict` — keys `year/month/day/hour`, each a dict
  with `stem, branch, stem_cn, branch_cn, stem_index, branch_index, animal,
  stem_element, branch_element, pillar`.
  Gold: **Xin Wei / Geng Yin / Bing Chen / Ding You**.
- `bazi.day_master(birth) -> str` — Gold: **Bing** (Yang Fire, 丙).
- `bazi.element_balance(pillars) -> dict[str,int]` — takes the four_pillars
  dict, counts 8 chars. Gold: Wood 1, Fire 2, Earth 2, Metal 3, Water 0.
- `bazi.ten_gods(birth) -> dict[str,str]` — 7 keys: `year_stem, year_branch,
  month_stem, month_branch, day_branch, hour_stem, hour_branch`. **SEE TRAP.**
- `bazi.luck_pillars(birth, gender) -> list[dict]` — gender `"male"`/`"female"`.
  8 pillars, each with `stem, branch, stem/branch_index, *_element, animal,
  start_age, end_age, pillar`.
  Gold (male): starts age **3.7** (backward, Yin year stem + male):
  Ji Chou 3.7–13.7 / Wu Zi 13.7–23.7 / Ding Hai 23.7–33.7 /
  **Bing Xu 33.7–43.7** (age ~35) / Yi You 43.7–53.7 / Jia Shen 53.7–63.7 /
  Gui Wei 63.7–73.7 / Ren Wu 73.7–83.7.

## ten_gods() — FIXED 2026-09-06 (commit 01d7bac)

The engine previously inverted Direct/Indirect for all non-companion relations
(`_ten_god_for` returned Direct on SAME polarity). **Fixed in the engine** —
`ten_gods()` now returns standard values directly. Gold (DM Bing, Yang Fire):

- year_stem Xin: **Zheng Cai** · year_branch Wei: Shi Shen
- month_stem Geng: **Pian Cai** · month_branch Yin: Pian Yin
- day_branch Chen: Shang Guan
- hour_stem Ding: **Jie Cai** · hour_branch You: **Zheng Cai (Direct Wealth)**

Anchor check: `assert g['hour_stem']=='Jie Cai' and g['hour_branch']=='Zheng Cai'`.
If either fails again after an engine update, re-apply the standard rule:
Direct (Zheng) = OPPOSITE polarity for wealth/resource/output/power;
companion: same = Bi Jian, opposite = Jie Cai.

## Notes

- Branch polarity convention: engine treats each branch's polarity as its
  principal-qi parity via `STEM_YIN_YANG[(idx*5)%10]` (Yang branches = even
  index). Standard charts often key off the actual hidden principal stem.
- Day pillar: `(jdn+9)%10, (jdn+1)%12`; year rolls at Li Chun (~Feb 4);
  month stems via Five Tigers, hour stems via Five Rats; 23:00+ births use
  next day's day stem for the hour pillar.
- Readings must NEVER omit detail: report all four pillars, all 7 Ten Gods,
  element balance, and the full luck-pillar sequence with ages.
