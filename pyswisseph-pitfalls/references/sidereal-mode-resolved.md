# Sidereal mode in pyswisseph — resolved by measurement (2026-09-10)

Two archived copies of the old note (`hermes-mac-archive/skills/astrology/`,
under `astrologica-local-engine/references/` and `astroway/references/`) contradicted
each other about `swe.set_sid_mode()`. Both were in the vault archive, mode 600,
manimix-owned. This file is the resolution. **Treat the two archived copies as
superseded wherever they disagree with this file.**

Reproduce with `scripts/sidereal_mode_probe.py` (in this skill).

## The claim under dispute

Archived copy A (`astrologica-local-engine`, the original):

> `swe.set_sid_mode()` PERSISTS in the Swiss Ephemeris library's internal C state. Once
> called (even indirectly via `swe.get_ayanamsa()`), ALL subsequent `calc_ut()` calls are
> affected — the library may silently apply the ayanamsa correction even when
> `FLG_SIDEREAL` is NOT in the flags.

Archived copy B (`astroway`) corrected it inline:

> The issue is NOT that `set_sid_mode` corrupts `calc_ut` without `FLG_SIDEREAL`. The
> issue is that using `FLG_SIDEREAL` applies the correction INSIDE the library, and if
> `set_sid_mode` was called with a DIFFERENT ayanamsa than expected, you get silently
> wrong results.

## Verdict: copy A is FALSE, copy B is TRUE — but B buries the real trap

Measured at JD for 1991-02-15 17:45 UT, tropical Sun (`FLG_SWIEPH | FLG_SPEED`, no
`FLG_SIDEREAL`):

| Library state | `calc_ut(SUN)` without `FLG_SIDEREAL` |
|---|---|
| pristine | `326.541235` |
| after `get_ayanamsa()` | `326.541235` |
| after `set_sid_mode(SIDM_LAHIRI)` | `326.541235` |
| after `set_sid_mode(SIDM_RAMAN)` | `326.541235` |

Identical to 9 decimal places in every state. **No silent correction happens without
`FLG_SIDEREAL`.** Copy A's root cause is wrong; do not repeat it.

## The real trap (what copy A was groping toward)

The sidereal mode is **process-global**, and the library default is **not Lahiri**:

- `swe.get_ayanamsa(jd)` called BEFORE any `set_sid_mode()` returned **24.616322°** for
  1991-02-15. Lahiri is **23.733115°**. Wrong by 0.883° ≈ 53 arc-min, silently.
- `FLG_SIDEREAL` with a non-Lahiri mode returned positions **86.78 arc-min** away from the
  Lahiri answer, silently.

So both `get_ayanamsa()` and `FLG_SIDEREAL` read a global that you may never have set.

## Also measured: the two approaches are NOT bit-identical

At 1991-02-15 the direct `FLG_SIDEREAL` path differed from
`tropical - get_ayanamsa(jd)` by **~16 arc-sec** (23.737732 vs 23.733115 implied
tropical offset). Consequence: **do not chase a ~16" discrepancy against a published
reference** — it is inherent to the method, not a bug in your code. (The archived notes
attributed this 16" to DE431-vs-DE441 ephemeris files; that is plausible but was never
proven, and the method difference alone accounts for it.)

## Consequence for the gold chart

When Astro Seek has "Sidereal chart: Ayanamsa 23°44' (Lahiri)" enabled, **every displayed
position on that page is already sidereal**. Reading them as tropical is the multi-day bug
that produced the confusion in the first place.

## What the archived copies ALSO got wrong

Both copies' cross-validation table is headed "Gergely (Kisvárda, 1991-02-15 **17:45 CET**)"
and lists a sidereal Sun of "Aquarius 2°45'42". 17:45 is the **UT** value; the local civil
time is 18:45 CET. The whole table was therefore generated for a chart one hour early.
Correct values at 18:45 local:

| | 17:45 as local (wrong) | 18:45 local (correct) |
|---|---|---|
| Sidereal Sun | Aquarius 2°45' | Aquarius 2°48' |
| Sidereal Lagna | Leo 13.23° | Leo 24.20° |
| Sade Sati | — | phase 3 active |

That bad anchor propagated into `tests/test_core_verify.py` and was only fixed 2026-09-10
(commit `435e5ce`). See the `astrologica` skill's birth-time trap section.
