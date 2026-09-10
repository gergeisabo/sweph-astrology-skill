---
name: astrology-readings
description: "Use when synthesizing a multi-system natal reading."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [astrology, natal, synthesis, wealth, human-design, bazi]
    category: astrology
    related_skills: [astrologica, destiny-matrix]
---

# Astrology readings (local engine)

Compute with `astrologica` (`~/Projects/astrologica/.venv/bin/astro` CLI, or the Python API). Ladini chakras with `destiny-matrix`. Then **synthesize the intersection**, not a dump of every system.

`astrologica` SKILL.md was reconciled with the code on 2026-09-06 (CLI, correct APIs) and re-verified 2026-09-10 (**517 tests**, not 276). The traps below are still worth reading.

## When to use

User asks what the stars say about money, purpose, timing, travel, alignment, or “read my chart” across Western / Vedic / HD / BaZi / Destiny Matrix.

## Gold birth (do not renegotiate)

- Local: **1991-02-15 18:45 Europe/Budapest** (CET). UT 17:45.
- Kisvárda 48.2264 N, 22.0847 E.
- Gold notes: `/mnt/hdd/00-obsidian/ASTROLOGY/BIRTH CHART DATA.md`
- HD gold PDF: `/mnt/hdd/00-obsidian/ASTROLOGY/PureGenerators_HumanDesign_Chart.pdf` — **PureGenerators is the website**, not the type.

`core.py` comments that say 17:45 CET and tropical Sun Aquarius 2° are wrong. Feb 15 Sun is ~26° Aquarius. Sidereal Sun ~2.81° Aquarius is the Lahiri value. **Birth time is local 18:45 CET = 17:45 UT** — feeding 17:45 as local shifts every house and the Lagna (Leo 13.23° instead of Leo 24.2°).

## Compute checklist

```python
birth = BirthData("1991-02-15", "18:45:00", 48.2264, 22.0847,
                  tz="Europe/Budapest", place="Kisvárda")
pos = compute_positions(birth)                 # tropical
houses = compute_houses(birth)                 # Placidus
sid = compute_positions(birth, sidereal=True)
wh = compute_houses(birth, system="whole_sign", sidereal=True)  # REQUIRED
```

- Houses: always `houses.house_of(lon)`. Iterate `pos.items()` (keys are Rahu/Ketu, not North Node).
- Vedic dasha: `vimshottari_dasha(birth, sid["Moon"].longitude)`.
- Yogas: `yogas(sid, wh, int(wh.ascendant // 30))` — `lagna_sign` required.
- Progressions: date string, not year int.
- Numerology: `full_profile(name, date_str)` — there is no `pythagorean()`.
- Night chart for this natal (`is_day=False`) for lots/ZR.
- HD: `from astrologica.hd import compute as hd_compute`. Gold PDF = engine: **Projector**, wait for invitation, Self-Projected, 3/5, channels 7–31 and 1–8, Cross of Contagion 1 (30/29|14/8).
- Destiny Matrix: `astro destiny` (CLI, added 2026-09-10) or `astrologica.destiny.compute(date_str)`. The engine's `destiny.py` was rewritten (commit 7976318) and **now computes the verified Ladini matrix itself** — do NOT hand-compute it and do NOT fall back to the old vault numbers. `destiny-matrix` remains the formula authority; verify against its `references/verified-1991-02-15-chakras.md` (A=15 Devil, center E=11 Justice, tail D=10 Wheel).
- BaZi pillars gold: Xin Wei / Geng Yin / **Bing Chen** / Ding You. Day Master **Bing Fire**. Hour Ding = Jie Cai on You Direct Wealth.
- `ten_gods()` was FIXED in the engine on 2026-09-06 (commit 01d7bac) and now returns **standard** Direct/Indirect polarity directly. **Do NOT re-apply the polarity rule on top of engine output — that double-corrects it.** Gold anchor: `hour_stem='Jie Cai'`, `hour_branch='Zheng Cai'`. If those ever fail after an engine change, only then re-apply: Direct = opposite yin/yang for wealth/resource/output/power.
- Luck pillars `luck_pillars(birth, "male")`. Age 35 = Bing Xu (~33.7–43.7), not the old vault Ding-Hai table.

## Do not reuse

- `OLD/Astrology/Gergely - Asztrológiai elemzés 2026-06-26.md` **BaZi is wrong** (Yi-You Day Master / Yin Wood). Same file Destiny center=Devil is wrong.
- Do not tell MoA or any model “HD type = Pure Generator.” The PDF filename will poison Generator-strategy advice.

## Synthesis method (this user)

User is non-technical. Wants **one pattern**, dos/don’ts, how to flow — not an encyclopedia and not a menu.

1. Compute all systems (facts only).
2. Hunt the **intersection**. If 3+ systems agree on the mechanism, that is the teaching. Drop poetic lanes that contradict.
3. Lead with the pattern in plain language. Tables are proof, not the answer — unless they asked for a full natal dump (then every point, Rx, `house_of()`).
4. Travel: this natal is a **WHEN** chart (Mars 9th, Gemini MC, Fortune 12th), not an ACG WHERE chart, unless they explicitly ask for lines. Engine `acg_lines` sweeps birth latitude only — too crude to pick cities.
5. “Wait for invitation” is not passivity: act on work **already on the table**.
6. Age-35 12th profection is **Leo / Sun**, not Mercury (do not take year-lord from Fortune in Virgo).

### Pattern already confirmed (2026-08-29)

Money and purpose are the same switch: **paid/recognized when a counterpart chooses him as the guide; leak is peers/Rob Wealth; do not initiate empire; Saturn–Mars from 2026-10-11 is the movement season.** Projector, not Generator. Keep the insurer contract; don’t split it with equals.

## MoA

If using MoA, feed **computed type (Projector)** and **Bing Fire**, never the PDF filename or the 2026-06-26 vault BaZi.
