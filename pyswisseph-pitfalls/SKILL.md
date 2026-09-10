---
name: pyswisseph-pitfalls
description: "Use when building or debugging astrology engines with pyswisseph. Silent-failure API pitfalls, sidereal mode traps, ephemeris setup."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [astrology, swisseph, pyswisseph, ephemeris, python, pitfalls]
    category: astrology
    related_skills: [astrologica]
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

## 7. Sidereal mode — the REAL trap is the hidden global mode, not "corruption"

RESOLVED 2026-09-10 by direct measurement (repro + full evidence:
`references/sidereal-mode-resolved.md`). Two archived copies of this note contradicted
each other; the measurement settles it.

**FALSE (do not repeat):** "`set_sid_mode()` persists in C state and silently applies the
ayanamsa correction to `calc_ut()` even when `FLG_SIDEREAL` is not in the flags."
Measured: tropical Sun is `326.541235` before any sidereal call, after `get_ayanamsa()`,
and after `set_sid_mode(SIDM_LAHIRI)` — **identical to 9 decimal places**. Without
`FLG_SIDEREAL` nothing is corrected. If your tropical values are ~24° off, the bug is in
your own subtraction, not the library.

**TRUE — the actual silent failure:** the sidereal mode is process-global state and the
library default is **not Lahiri**.

- `swe.get_ayanamsa(jd)` returns the ayanamsa of *whatever mode is currently set*. Called
  before any `set_sid_mode()`, it returned **24.616322°** for 1991-02-15 — wrong by
  0.883° (~53 arc-min) versus Lahiri's 23.733115°. No error, no warning.
- `FLG_SIDEREAL` also silently uses the current mode: switching to `SIDM_RAMAN` shifted
  the result by **86.78 arc-min** with no exception.

**Safe pattern (use this):**

```python
flags = swe.FLG_SWIEPH | swe.FLG_SPEED     # NEVER add FLG_SIDEREAL
tropical = swe.calc_ut(jd, pid, flags)[0][0]
swe.set_sid_mode(swe.SIDM_LAHIRI)          # ALWAYS set the mode explicitly first
ay = swe.get_ayanamsa(jd)                  # then read it
sidereal = (tropical - ay) % 360.0         # then subtract manually
```

**Also do not reorder the last two steps.** `get_ayanamsa()` before `set_sid_mode()` is
the whole bug. And note the two approaches are not bit-identical: at 1991-02-15 the
direct `FLG_SIDEREAL` path differed from `tropical - get_ayanamsa()` by ~16 arc-sec, so
do not chase a 16" discrepancy against a published reference — it is expected, not a bug.

**Never read tropical values as sidereal.** This caused a multi-day bug in sweph-astrology
where Astro Seek comparisons were wrong because the code assumed tropical when Astro Seek
showed sidereal. When a source has "Sidereal: Ayanamsa 23°44' (Lahiri)" enabled, ALL its
displayed positions are already sidereal.

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

pyswisseph has no lunar-calendar converter. Working approach (used in sweph-astrology's `astro` CLI and `astrologica/lunar.py`): lunar day = days since last new moon + 1; lunar month = new moons since the month containing the winter solstice (month 11); leap month = first month after month 11 containing no principal solar term (中气， Sun crossing every other 30° multiple from 270°). Find new moons by walking the Sun–Moon elongation `(moon-sun) % 360` back in 0.25-day steps until it wraps >360→small, then bisect on `elong(mid) > 180`. **Round new-moon AND solar-term instants to whole China civil days (Asia/Shanghai, UTC+8) before classifying** — classifying by raw instants picks the wrong leap month in edge years (two events falling on the same UTC day can split across a China-day boundary). Sanity checks: 1991-02-15 → lunar M1 D1 (CNY was Feb 15, 1991); 2023-04-01 → month 2, leap=True; 2025 has leap month 6, not 7.

## 11. Entry-point scripts with uv venvs

`uv`-created venvs have no `pip` — install a project's `[project.scripts]` entry point with `uv pip install -e . --python .venv/bin/python`. The console script then appears in `.venv/bin/`.

## 12. Fix the engine, don't document a workaround — and check the tests

When a live-verification pass (your own or a subagent's) finds a systematic wrong-value
pattern in the engine, FIX the code rather than baking a "recompute it yourself"
workaround into the skill. A workaround in a skill is a patch waiting to happen and
rots when the bug is later fixed. Before fixing, grep the test tree for the SYMBOL —
existing tests often encode the buggy convention and their docstrings may even assert
it as correct; correct those tests to the standard rule, don't preserve them.
(Example: ten_gods() returned Direct on SAME polarity for all non-companion relations;
two tests asserted the inverted names and were fixed alongside the one-line engine
change.)

## 13. Verify after a parallel subagent fan-out on a shared repo

When extending the engine by dispatching several subagents in parallel against the SAME
git repo, never trust any child's final "N tests green" as the tree's state — parallel
children interleave commits and can leave a transiently-broken tree (test-count drift, a
failure from another agent's half-finished work) that only resolves once the last child
finishes. After the batch, run `.venv/bin/python -m pytest tests/ -q` and `git status`
yourself, re-smoke-test each new function's claimed gold value, and `git push` (children
commit but do not always push — `git status -sb` shows the ahead count). Give each child
one independent invariant/oracle check (e.g. SAV total = 337; Sun-in-Leo sthana bala >
Sun-in-Aquarius; solar arc ≈ 1°/year) so wrong OUTPUT is caught, not just wrong code.

**The same distrust applies to a child's ANALYSIS, not just its test counts.** A fan-out that
reports "40% of this tree is duplicated", "these two files are verbatim copies", or "each module
defers to the other" is making measurable claims — measure them before acting. In one audit the
children reported 40% duplication (true figure 3.4%), called two independently-worded documents
"verbatim" (zero shared sentences), and described a one-way pointer as a circular dependency (the
reverse reference did not exist). Only their *quoted file:line evidence* survived checking; every
derived number was inflated. Default assumption: a child's counts are estimates dressed as
measurements.

**Shape the fan-out as a MIXTURE, not N copies.** Several generalist children reading the same
material converge on the same answer and then confirm each other's errors — agent consensus is not
corroboration. Give each child a different lens *and* a different method: an adversarial verifier
told to ATTACK the previous round's claims, a quantitative pass that measures what the others only
assert, a wider-scope scout that searches outside the agreed boundary, a simulation pass that tests
the result against real usage, and a history archaeologist that mines what a snapshot comparison
cannot see. Expect the adversarial lens to refute you — if a "verification" round found nothing
wrong, it was not adversarial enough to be worth its cost.

**Measuring a text corpus: count lines, and exclude frontmatter.** "How much of this is
duplicated" is answerable exactly, and estimating it is how you get it wrong by 10x. Measure
at LINE level — whole-file and whole-paragraph similarity both undercount badly, because the
same line repeated inside two differently-worded paragraphs never forms a matching block (one
pass reported 0.1% duplication for a tree where grep had already proven seven identical
constructors). Then strip YAML frontmatter and report it separately: metadata lines
(`category:`, `version:`, `author:`) dominate raw duplicate counts and are noise. Classify
matches as code-fence vs prose and report the two separately — code that drifts breaks things,
prose that drifts merely reads oddly.

## 14. Treat every "known limitation" caveat as possibly-stale documentation

A caveat in a skill or docstring may describe a bug that was already fixed while the
caveat was never deleted — repeating it poisons later readings and prompts agents to
"work around" correct code. Before propagating any caveat, re-verify it against ground
truth (reference PDF, independent calculator, published table). If the values already
match, DELETE the caveat and add the regression test + naming layer instead. Never
accept "it was never broken" from a subagent either — pull the ground-truth artifact
yourself; a caveat removed without verification is whitewashing, a caveat kept after
verification passes is rot.

## 15. Never invent traditional-system tables

When implementing tables from a divination/astrology tradition (sihua, dasha orders,
compatibility matrices), web-research the authoritative source FIRST and implement only
what actually exists in the tradition. Task premises about "which tables exist" can be
wrong (e.g. Zi Wei sihua is stem-keyed only — there is no year-branch 四化 table in any
published source); inventing one produces authoritative-looking wrong output that tests
can't catch because the test fixtures came from the same invention. If the requested
table doesn't exist, say so and implement the real system instead.

**The same rule governs COPYING a table, not just inventing one.** A table found in an
archive, an older draft, or another model's write-up looks authoritative precisely because
it is formatted as reference data — and it can carry two errors at once that nothing in
your tree will catch. Before merging such a table, verify each row against independent
published sources. Expect a wrong *name* and a non-standard *formation rule* to travel
together, and treat agent consensus as no evidence: several subagents reading the same
wrong table will all recommend merging it verbatim.

## 16. Probe boundary inputs before calling an engine robust

An all-green suite from happy-path fixtures says nothing about edge inputs. Before
declaring a computation engine finished, run an adversarial sweep: polar latitudes
(Placidus is undefined above ±66.6° — need a fallback house system), garbage date
strings (raw `int()` ValueError instead of a clear message), out-of-range indices
(nakshatra outside 0–26 → raw KeyError), boundary longitudes (exact gate/cusp edges),
southern hemisphere, leap days, ephemeris range extremes (1900/2100), and string-vs-
datetime argument confusion. Each fix gets a regression test so the sweep is one command
next time.

## 17. Anchor day/night searches to LOCAL midnight, not UT midnight

When searching `swe.rise_trans` (or any daily event) for "today" at a birth location,
anchor the search at local midnight (00:00 in the birth timezone → JD), not JD-of-
UT-midnight. At far-east longitudes the UT-midnight anchor falls on the previous local
evening, so the rise/set bracket skips a local day and classifies a noon birth as
night with an absurd (30h+) span. Same rule for anything keyed to "the birth day"
solar-wise: convert to the birth tz first.

## 18. A bisection that never tightens both bounds converges to the scan grid

When root-finding a crossing (ingress, station, lunation) inside a coarse step scan,
the bisection must move BOTH bracket ends inward; a predicate like
`abs(lon-hi) < abs(lon-lo)` that only ever replaces one end converges to the original
step midpoint, silently quantizing every event time to the scan grid (12h steps →
events reported at 00:00/12:00 exactly). Regression-check against a published instant
(e.g. a solstice/equinox to the minute) — internal consistency won't catch it.

## 19. The lunar node has TWO modes — check which one a reference used

`swe.TRUE_NODE` and `swe.MEAN_NODE` are different bodies, not synonyms, and they can
differ by **up to ~1.4°** (at 1991-02-15 18:45 CET: true = 297.869°, mean = 296.713°,
a gap of 69.4 arc-min). A published node that "doesn't match" is usually the other mode,
not a bug — but an unexplained 1°+ node discrepancy will otherwise sit in a project for
months (this one did).

**Which to use:** classical Jyotish uses the **MEAN** node for Rahu/Ketu (always); modern
Western software usually defaults to TRUE. Make it an explicit parameter rather than a
buried constant, and print/record which mode produced a result — see
`astrologica.core.NODE_MODES` / `compute_positions(..., node="mean"|"true")`, which
defaults to `mean`.

**Ketu is not a separate body** — it is `Rahu + 180°` with the latitude negated, and it
inherits whatever node mode Rahu used. If you switch modes for Rahu, recompute Ketu.

**Corollary — derive aspects from the positions you display.** If your CLI prints
positions using a configurable mode but computes aspects from a second, independent
`compute_positions()` call with default options, the aspect table silently disagrees with
the position table under any non-default flag. Pass the computed positions into the
aspect function instead of recomputing.

## 20. Know your oracle's display resolution before chasing a small delta

The residual between your engine and a reference site is not all error — some of it
is the site's **display convention**. Do not assume the site has ONE convention:
measured 2026-09-10, astro-seek displays the *same* Lahiri ayanamsa as
`23°43'` on its ayanamsa comparison table (**truncated**) and `23°44'` on its chart
header (**rounded**). The underlying value is 23.733115° = 23°43.9869', i.e.
0.8 arc-seconds below the arcminute boundary — the sharpest possible test case, and
**both readings are correct**.

So establish the convention **per page**, not per site. Chasing a 1 arc-minute
delta as if it were a bug wastes hours; ignoring it blindly hides a real error
underneath.

The tell is the **sign of the residual**. Against a floored oracle, your values should sit
consistently just ABOVE the published ones, by less than one display unit. A residual that
flips sign, or exceeds one display unit, is a genuine disagreement.

Method, in order:

1. Establish that **page's** unit of display and its rounding direction (whole
   arc-minute? truncated or rounded? arc-second? decimal degrees?). Match the
   comparison like-for-like before computing any delta.
2. Set tolerance from that unit plus the input differences you know about (coordinate
   rounding, time precision) — and write the reason in the test, as a comment.
3. Assert the **structural** property, not just a width: e.g. `0 <= ours - theirs < 1'`.
   A wide symmetric band (`abs(delta) < 2'`) passes on a floored oracle whether or not
   your mode is right.
4. Only then treat a violation as a real defect.

Also compare **whole extra systems**, not one chart. An oracle that exposes an ayanamsa
selector validates five code paths at once; re-asserting one chart validates one. The
five-system astro-seek check caught that Lahiri-vs-Raman is an 86' gap — big enough that
a mode mixup can never hide inside a rounding tolerance.

### The corollary that matters most

A cross-check is only worth something if the two sides are **actually independent**. A
reference that shares your library, your ephemeris, or your ayanamsa setting will agree
with you while both are wrong. Before trusting agreement, ask what the two sides share —
in the case that motivated this rule, two "independent" sources agreed on a lunar node
because both silently used the true node, and the check certified a 69' error.

## 21. Validate lookup indices with ValueError, never modulo-wrap

Traditional-system table lookups (`idx % 10`, `idx % 12`, `idx % 27`) turn an invalid
index into plausible-looking garbage — `sihua_for_stem(10)` returned stem-0's row
without a whisper. Range-check every index argument at function entry
(`if not 0 <= idx <= 9: raise ValueError(...)`) so bad input is loud, even when a
wrapping caller "would have worked".

## 22. A green suite calibrated on a wrong anchor verifies nothing

An all-green suite with a *tight* tolerance can be certifying the wrong chart. If the
fixture's INPUT is wrong (wrong birth time, wrong coordinates, wrong tz handling), every
expected value derived from that input is wrong in the same direction — so the suite
passes, and the tight tolerance is exactly what makes it look rigorous. Symptom: the
tests agree with each other and with the docs, but disagree with reality.

Distinct from §16: that is about missing coverage; this is about a wrong baseline.

Before trusting a reference suite, attack its anchor: re-derive the fixture from a source
independent of your own code path (a different calculator, a published report, a second
export by the same service with known settings) and assert against THAT. Cross-check a
value that falls out of two independent paths — e.g. tropical longitude and local
sidereal time must both move consistently when the input time moves. A leftover
inconsistency between two derivations is the tell that you are on the wrong anchor.

Hardening that follows: assert the input INTERPRETATION explicitly (one test naming the
local time and the UT it equals), widen the tolerance only where rounding justifies it and
say so in a comment, and prefer relational assertions over absolute ones —
`sidereal == tropical - ayanamsa`, `Ketu == Rahu + 180`, `len(pos) == N`. A relation fails
loudly when the anchor drifts; an absolute value silently re-ratifies it.

**After fixing the anchor, sweep the whole tree for that LITERAL before calling it done.**
The file where a wrong fixture value surfaces is rarely the only one carrying it. Grep for
the literal itself (the time string, the coordinate pair, the constant) rather than for the
symbol — a symbol grep finds the API surface, not the bad value repeated across fixtures.
A tree with one corrected module and several stale ones is WORSE than a uniformly wrong
one: the corrected module makes the suite look maintained while its siblings keep certifying
the old baseline, so the next reader trusts a partially-repaired reference set.

## 23. A CLI positional sharing a parent parser's option name is silently dead

`add_parser("transits", parents=[common])` plus `add_argument("date")` puts the positional
into the SAME `args.date` dest as the parent's `--date` flag. The option handler then reads
the positional's value, concludes a date was supplied, and errors on the missing
latitude — so a documented subcommand fails 100% of the time while looking perfectly
correct in `--help`. Neither the parser nor `--help` warns you.

Give every positional a dest no option uses (`when`, not `date`), and add a regression
test that invokes each subcommand WITH its positional argument. A subcommand that only
ever gets tested bare will keep this bug indefinitely.

## 24. A stated value and a stated delta can silently disagree

Reference data written into a skill, docstring or report often pairs an absolute value with a
difference from another value. Nothing recomputes that pair, so a single mistyped digit survives
review indefinitely and *reads* as verified. Real case: the true node was written as `298.869°`
beside `mean 296.713°` and a claimed `1.1565°` gap — but 298.869 − 296.713 = 2.156. The gap was
right and the value was a typo for `297.869°`.

Rule: whenever you save two arithmetically related numbers, compute the relation first, and
re-derive the pair from the engine rather than from your memory of what it printed. An internally
inconsistent pair is worse than a missing number — a reader (or an adversarial pass) will find the
contradiction long before anyone finds the correct value. The same check catches unit slips
(deg vs arc-min, arc-sec vs arc-min) that no test exercises.

## 25. Verify the SETTINGS, not just the maths

The calculation is accurate to under an arc-second; a wrong mode is measured in degrees.
Verification effort therefore belongs on configuration, not on the ephemeris. Three rules,
with the measurements behind them, are in `references/verifying-output.md` — read it before
calling any chart "verified":

- **Two sources that share a setting are one source.** A "cross-check" where both paths used
  the same node/ayanamsa/house mode agrees perfectly and proves nothing — and the agreement
  manufactures confidence. List the axes a check could vary and confirm the two paths differ
  on the one under test.
- **Every published number carries its mode** (node, ayanamsa, house system, ephemeris files,
  time source) on the same line as the value, or it is not a result.
- **A component flagged as broken still poisons the total you publish.** Recompute with and
  without it, or drop the ranking; never ship a derived ordering built on a sum you have
  annotated as corrupt.

Error budget, measured: ephemeris < 1 arc-sec · coordinates rounded to the arc-minute
0.1 arc-min · **birth time off by 1 minute = 11 arc-min of Ascendant** · true vs mean node
69 arc-min · ayanamsa choice up to 87 arc-min · birth time off by 1 hour ≈ 11°. Do not
"improve" the astronomy; it is not the limiting factor.
