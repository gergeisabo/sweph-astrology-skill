---
name: human-design
description: "Use when computing Human Design charts, type/authority/profile, transits, compatibility, or Rave Variables. Live-verified against the gold birth."
version: 1.0.0
metadata:
  hermes:
    tags: [human-design, bodygraph, rave-variables, incarnation-cross]
    category: astrology
    related_skills: [astrologica]
---

# Human Design — `astrologica.hd` + `astrologica.hd_ext`

Run with `~/Projects/astrologica/.venv/bin/python`, cwd `~/Projects/astrologica`.
CLI: `.venv/bin/astro hd`. Design = positions 88° of solar arc before birth
(`swe.solcross_ut`, precise).

## Setup + gold birth (verified 2026-09)

```python
from astrologica.core import BirthData
from astrologica import hd, hd_ext
birth = BirthData("1991-02-15", "18:45:00", 48.2264, 22.0847,
                  tz="Europe/Budapest", place="Kisvárda")
chart = hd.compute(birth)   # -> hd.HumanDesignChart
```

## hd.compute — HumanDesignChart fields (gold values verified live)

- `type` **Projector** · `strategy` **"Wait for invitation"** ·
  `authority` **"Self-Projected"** · `profile` **(3, 5)** → "3/5".
- `defined_centers` **{G, Throat}** · `defined_channels` **["1-8", "7-31"]**
  (single definition — both channels in one connected area).
- `incarnation_cross` **"30/29/14/8"** (P.Sun 30 / P.Earth 29 / D.Sun 14 /
  D.Earth 8) = Right Angle Cross of Contagion 1. Gold gates: P.Sun 30,
  D.Sun 14, P.Earth 29, D.Earth 8.
- `personality_gates` / `design_gates`: dict planet→gate; includes Earth =
  Sun+180°. `all_active_gates`: set union (gold: 22 gates).
- NEVER say type = "Pure Generator" for this chart — the gold PDF filename
  'PureGenerators' is a website name, not the type. Type is Projector.

## hd.gate_at_longitude(longitude) -> (gate, line)

Verified: `gate_at_longitude(326.5) -> (30, 3)`; `gate_at_longitude(224.0)
-> (1, 1)`. HD Earth gate = `gate_at_longitude((sun_lon + 180) % 360)` —
ALWAYS treat Earth as activated.

## hd_ext (all verified live)

- `hd_transits(birth, transit_date=None)` — gates/lines activated now (or at
  a datetime); returns `{"active_gates": {planet: (gate,line)}, "transit_date"}`.
- `hd_compatibility(birth1, birth2)` — person gates, `shared_gates`,
  `electromagnetic_gates` (symmetric difference), both types.
- `incarnation_cross(birth)` — 4-gate cross with named keys; Earth via wheel
  index +32 (correct method).
- `hd_circuitry(birth)` — Individual/Tribal/Collective gate counts +
  `dominant_circuit` (gold: Individual 19, Collective 17, Tribal 3).
- `design_date(birth)` — PRECISE: uses `hd._get_design_date`
  (`swe.solcross_ut` on natal Sun longitude − 88°) → gold **1990-11-21
  03:07:40 UTC**. Returns `design_date`, `design_time` and
  `days_before_birth` (~86.6, not 88 — the Sun's arc is not exactly 1°/day).
- `penta(charts)` — group bodygraph for a **list of 3–5** `BirthData`
  (raises `ValueError` otherwise). Returns `group_defined_centers` /
  `group_defined_channels` (UNION across members, channels normalised to
  `min-max`), `shared_gates` (INTERSECTION), `missing_gates` (1–64 minus
  union), and `group_dynamics` (interpretive center→tag labels, NOT a formal
  Penta/WA calc). Gold `penta([birth]*3)` → shared = all 22 gold gates,
  centers {G, Throat}, channels ["1-8","7-31"].
- `dream_rave(birth)` — Dream Rave core from the precise design instant
  (`_get_design_date`): design Sun/Moon/Earth (Earth = Sun+180°). Returns
  `dream_sun_gate`, `dream_moon_gate`, `dream_earth_gate`, `dream_gates`,
  `dream_channels` (complete channels among the 3 gates — rarely non-empty),
  `dream_centers` (centers TOUCHED by any dream gate, NOT full definition —
  a simplification; the real Dream Rave uses all design positions).
  Gold: Sun 14, Moon 58, Earth 8; channels []; centers {Root, Sacral, Throat}.
- `hologenetic_profile(birth)` — Gene Keys / Laveena Archers Hologenetic
  Profile, reduced to what the engine computes. Returns
  `role_gate`/`role_line` (Personality Earth = Sun+180° — TRUE HD math),
  `trajectory`/`trajectory_line` (Design Sun at design instant — TRUE HD
  math), and `mode` (INTERPRETIVE: canonical HD line-archetype name of the
  trajectory line — Investigator/Hermit/Martyr/Opportunist/Heretic/Role
  Model). Gold: role_gate 29 (line 3), trajectory 14 (line 5), mode
  **"Heretic"**.

## Rave Variables (sub-structure)

Six Variables, computed from Color/Tone within the gate. Sources:

| Variable     | Source                        |
|--------------|-------------------------------|
| Determination| Design Sun Color (+Tone → Left/Right qualifier) |
| Environment  | Design True-Node Color (+Tone → Left/Right qualifier) |
| Motivation   | Personality Sun Color         |
| Perspective  | Personality True-Node Color   |
| Sense        | Personality Sun Tone          |
| Cognition    | Design Sun Tone               |

Color/Tone are 1–6 (Line > Color > Tone: 0.9375° / 0.15625° / 0.026041667°).
TRUE NODE (`swe.TRUE_NODE`) is required for Environment/Perspective — the
mean node shifts the color. Tone 1–3 = Left, 4–6 = Right (arrow direction).

`hd.rave_variables(chart)` names all six via the IHDS maps. Gold birth
(1991-02-15 18:45 Kisvárda) — VERIFIED against an independent reference:

| Variable     | Gold name              | index                         |
|--------------|------------------------|-------------------------------|
| Determination| **Closed**             | color 2, tone 6 (Right)       |
| Environment  | **Mountains Active**   | color 4, tone 3 (Left)        |
| Motivation   | **Hope**               | color 2                       |
| Perspective  | **Wanting**            | color 4                       |
| Sense        | **Security**           | tone 1                        |
| Cognition    | **Touch**              | tone 6                        |

Naming maps (color 1–6): Determination
Appetite/Taste/Thirst/Touch/Sound/Light, with directional qualifiers (Taste
Left="Open", Right="Closed"); Environment
Caves/Markets/Kitchens/Mountains/Valleys/Shores (Mountains Left="Active",
Right="Passive"); Motivation Fear/Hope/Desire/Need/Guilt/Innocence;
Perspective Survival/Possibility/Power/Wanting/Probability/Personal; Sense
tones Security/Uncertainty/Action/Meditation/Judgment/Acceptance; Cognition
tones Smell/Taste/Outer vision/Inner vision/Feeling/Touch.

## Notes

- Gate wheel: 64 gates × 5.625°, Gate 41 starts ~302° tropical (+58° offset
  into IGING_WHEEL). Lines 1–6 per gate; profile = (P.Sun line, D.Sun line).
- Definition count: group defined channels into connected components
  (gold: one group → single definition).
- Readings must NEVER omit detail: every defined center, every channel, all
  22 active gates, all four cross gates, full Variables row.
