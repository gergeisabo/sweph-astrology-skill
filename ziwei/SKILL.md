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
from astrologica.lunar import solar_to_lunar
lunar_month, leap, lunar_day = solar_to_lunar(birth)              # (1, False, 1)
chart = ziwei_chart(ys, yb, lunar_month, lunar_day, hour_branch)
```

## ziwei_chart signature (from source)

`ziwei_chart(year_stem: int, year_branch: int, month: int, day: int,
hour_branch: int, sihua_kind: str = "year_stem", month_stem: int | None = None,
day_stem: int | None = None, hour_stem: int | None = None) -> ZWPResult` —
ALL ints/indices (Zi=0 … Hai=11; Jia=0 … Gui=9). `month`/`day` are **LUNAR**
month/day, NOT solar. `ZWPResult`: `birth_branch, life_palace, body_palace,
palaces (dict branch_idx→palace name), star_placements (dict star→branch_idx),
element, bureau, sihua, sihua_all`.

## Solar→lunar conversion — `astrologica.lunar.solar_to_lunar`

`from astrologica.lunar import solar_to_lunar`
`solar_to_lunar(birth) -> (month, leap_month, day)` — the CORRECT Chinese
lunisolar calendar (leap months + civil-day day reckoning); `cli.py cmd_ziwei`
uses it. Algorithm:

- Month boundaries = new-moon instants (Moon–Sun elongation 0 via Swiss
  Ephemeris), rounded to whole **China civil days** (Asia/Shanghai, UTC+8).
- Month 11 = the month containing the winter solstice (Sun longitude 270°,
  `swe.solcross_ut`).
- Principal solar terms (中气) = Sun crossing multiples of 30°:
  270, 300, 330, 0, …, 240 (12 terms, via `swe.solcross_ut`), rounded to China
  days. A month whose day-range contains NO 中气 is a **leap month** (repeats
  the previous month number, `leap=True`).
- Lunar day 1 = the China civil day containing the month's new moon;
  `day = (birth.date − new_moon_day).days + 1`.

The calendar is China-anchored (fixed worldwide): Chinese New Year 1991 was
15 Feb even though the new moon fell 14 Feb in European timezones.
- Gold 1991-02-15 → **lunar M1 D1, leap=False**.
- Leap example: 2023-04-01 → M2 leap=True (2023 had 闰二月, 03-22…04-19);
  2025-07-25 → M6 leap=True (闰六月).

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

## Four Transformations (四化) — four stem-keyed systems

Four Transformations are **stem-keyed by definition**: the single standard
十天干四化表 (Ten-Stem table, per 《紫微斗数全书》) is indexed by whichever
heavenly stem is in play. `ziwei_chart` exposes the four periods via
`sihua_kind` — `"year_stem"` (default, 生年四化), `"month_stem"` (流月四化),
`"day_stem"` (流日四化), `"hour_stem"` (流时四化). Pass the corresponding stem
(`month_stem`/`day_stem`/`hour_stem`) for the non-year kinds. `result.sihua`
holds the selected set; `result.sihua_all` holds every set whose stem is known.
There is **no branch-keyed (地支) table** — year-branch is not a sihua axis.

十天干四化表 (stem index 0=Jia … 9=Gui → Lu/Quan/Ke/Ji):

| 干 | Lu 化禄 | Quan 化权 | Ke 化科 | Ji 化忌 |
|---|---|---|---|---|
| 甲 Jia 0 | Lian Zhen | Po Jun | Wu Qu | Tai Yang |
| 乙 Yi 1 | Tian Ji | Tian Liang | Zi Wei | Tai Yin |
| 丙 Bing 2 | Tian Tong | Tian Ji | Wen Chang | Lian Zhen |
| 丁 Ding 3 | Tai Yin | Tian Tong | Tian Ji | Ju Men |
| 戊 Wu 4 | Tan Lang | Tai Yin | You Bi | Tian Ji |
| 己 Ji 5 | Wu Qu | Tan Lang | Tian Liang | Wen Qu |
| 庚 Geng 6 | Tai Yang | Wu Qu | Tai Yin | Tian Tong |
| 辛 Xin 7 | Ju Men | Tai Yang | Wen Qu | Wen Chang |
| 壬 Ren 8 | Tian Liang | Zi Wei | Zuo Fu | Wu Qu |
| 癸 Gui 9 | Po Jun | Ju Men | Tai Yin | Tan Lang |

Gold birth pillars → gold sihua sets (each = `sihua_for_stem(stem)`):

- **Year-stem** Xin 辛(7): Lu=Ju Men · Quan=Tai Yang · Ke=Wen Qu · Ji=Wen Chang.
- **Month-stem** Geng 庚(6): Lu=Tai Yang · Quan=Wu Qu · Ke=Tai Yin · Ji=Tian Tong.
- **Day-stem** Bing 丙(2): Lu=Tian Tong · Quan=Tian Ji · Ke=Wen Chang · Ji=Lian Zhen.
- **Hour-stem** Ding 丁(3): Lu=Tai Yin · Quan=Tian Tong · Ke=Tian Ji · Ji=Ju Men.
