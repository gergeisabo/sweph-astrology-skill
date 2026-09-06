---
name: ziwei
description: "Use when computing Zi Wei Dou Shu (Purple Star) charts, palaces, bureau, or sihua. Live-verified against the gold birth."
version: 1.0.0
metadata:
  hermes:
    tags: [ziwei, purple-star, chinese-astrology, lunar-calendar]
    category: astrology
    related_skills: [astrologica]
---

# Zi Wei Dou Shu — `astrologica.ziwei` + solar→lunar conversion

Run with `~/Projects/astrologica/.venv/bin/python`, cwd `~/Projects/astrologica`.
CLI: `.venv/bin/astro ziwei` (does the solar→lunar conversion itself).

## Setup + gold birth (verified 2026-09)

```python
from astrologica.core import BirthData
from astrologica.bazi import four_pillars
from astrologica.ziwei import ziwei_chart, BRANCHES
birth = BirthData("1991-02-15", "18:45:00", 48.2264, 22.0847,
                  tz="Europe/Budapest", place="Kisvárda")
p = four_pillars(birth)
ys, yb = p["year"]["stem_index"], p["year"]["branch_index"]      # 7, 7 = Xin Wei
hour_branch = p["hour"]["branch_index"]                          # 9 = You
chart = ziwei_chart(ys, yb, lunar_month, lunar_day, hour_branch)
```

## ziwei_chart signature (from source)

`ziwei_chart(year_stem: int, year_branch: int, month: int, day: int,
hour_branch: int) -> ZWPResult` — ALL ints/indices (Zi=0 … Hai=11;
Jia=0 … Gui=9). `month`/`day` are **LUNAR** month/day, NOT solar.
`ZWPResult`: `birth_branch, life_palace, body_palace, palaces
(dict branch_idx→palace name), star_placements (dict star→branch_idx),
element, bureau, sihua`.

## Solar→lunar conversion (as implemented in cli.py `cmd_ziwei`)

Uses Swiss Ephemeris (`new_moon_before`): walk back from target JD in 0.25-day
steps until sun–moon elongation wraps 360→0, then bisect (40 iterations).
- `target_jd = swe.julday(year, month, day, 12.0)` (noon UT).
- **Lunar day** = `int((target_jd - new_moon_before(target_jd + 0.01)) // 1) + 1`
  (days since last new moon + 1).
- **Lunar month** = new moons since the new moon in the **Jan 20–Feb 20
  window** (Chinese New Year rule): `round((nm_at_birth - first_nm)/29.530588)+1`,
  +12 if negative. If no window new moon found, falls back to solar month −1
  with a "(month approximate)" note.
- Gold: 1991-02-15 → last new moon 1991-02-14 (JD 2448302.23, also the
  CYY-window new moon) → **lunar M1 D1** — correct because the birth WAS
  Chinese New Year day 1991.

## Gold chart (verified live: `ziwei_chart(7, 7, 1, 1, 9)`)

- **Life palace: Si (index 5)** · Body palace: Hai (index 11).
- **Bureau: Water 2** (element "Water", ju=2).
- **Sihua** (year stem Xin): Lu=Ju Men, Quan=Tai Yang, Ke=Wen Qu,
  Ji=Wen Chang.
- Palaces: Life Si / Siblings Wu / Spouse Wei / Children Shen / Wealth You /
  Health Xu / Travel Hai / Friends Zi / Career Chou / Property Yin /
  Fortune Mao / Parents Chen.
- Life palace stars: **Lian Zhen + Tian Ma**. Others: Zi Wei+Tian Xiang+
  Wen Chang+Wen Qu Chou · Tian Liang+Tian Yue+Di Kong+Tian Xi Yin ·
  Qi Sha Mao · Zuo Fu Chen · Po Jun+Ling Xing Wei · Tian Tong+Tuo Luo+
  Di Jie+Hong Luan Shen · Tian Fu+Wu Qu+Lu Cun You · Tai Yang+Tai Yin+
  Qing Yang+You Bi Xu · Tan Lang Hai · Tian Ji+Ju Men Zi · Tian Kui+
  Huo Xing Wu.

## Caveats

- **Leap-month approximation**: lunar month is derived by counting new moons
  since the CYY-window new moon; in years with a leap month the computed
  month (and palace placement) can be off by one. The CLI prints a note when
  approximate. Gold birth is unaffected.
- Noon-UT target: for births soon after a late-UT new moon near midnight,
  the lunar day can be off by one vs local-date reckoning.
- 14 main stars + 16 minor stars placed; sihua is year-stem keyed only
  (no palace/branch sihua variants).
- Readings must NEVER omit detail: all 12 palaces, all star placements,
  bureau, and all four sihua.
