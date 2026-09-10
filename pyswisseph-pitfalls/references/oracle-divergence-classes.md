# When an oracle and your engine disagree by design

Companion to §20 (display conventions), §25 (verify the settings) and §26 (divergence is not
always a bug). Worked tables behind the rule "check the convention before fixing the code".

## Varga (divisional) chart schemes

Gold chart, Lahiri sidereal, whole sign, mean node, 13 bodies per division (ASC + Sun..Pluto +
Rahu + Ketu). Our engine vs astro-seek's published D1–D144 table.

| Division | Our signs matching | Status |
|---|---|---|
| D1, D2, D3, D7, D9, D10, D12, D24, D60 | 13 / 13 each | agree |
| D4 | 4 / 13 | diverges |
| D16 | 5 / 13 | diverges |
| D20 | 2 / 13 | diverges |
| D27 | 1 / 13 | diverges |
| D30 | 7 / 13 | diverges |
| D40 | 0 / 13 | diverges |
| D45 | 3 / 13 | diverges |

135 / 195 body-checks agree overall. Note D24 and D60 agree — check the full supported list, not
the handful you remember being disputed, or you will report a phantom failure.

## Two mechanisms — do not treat them alike

**Whole-sign shift (D16, D20).** Every mismatching body shifts by exactly ±4 signs, keyed to the
**parity of its D1 sign**: odd D1 sign → −4, even D1 sign → +4 (offset measured as
oracle − ours). Same divisions, different starting sign. These are relabellings.

**Different boundaries (D4, D27, D30, D40, D45).** Per-body offsets *vary* — D40 produced −4,
−3, −2, −1 and +2 within a single chart. A varying offset means the divisions are cut
*differently*, so the two schemes disagree for most charts, not just by a shifted label.

Diagnostic: tabulate the offset per body and group by the D1 sign's parity. Constant → relabelling.
Scattered → different division rule.

## Engine contract to preserve

`varga_chart()` supports **1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60**. Anything
else must raise `ValueError` — verified against 5, 6, 8, 11, 81, 108, 144, 999 — rather than
falling through to a default branch and returning a plausible-looking wrong chart. Keep the
supported set matching the docstring: a stale list is how a supported division looks
unsupported (D4 was implemented but undocumented).

`varga_chart()` returns the varga **sign** (longitude snapped to 0° of that sign). Varga degrees
*within* the sign are not returned, so a published varga degree compares as `int(computed)`
against a truncating source.

## Shadbala: the minima constant

`shadbala()` returns `total_rupas` / `total_virupas` and holds **no minima table and no ratio**.
The minimum Rupas per planet is a separate declaration:

| Planet | Raman (*Graha and Bhava Balas*) | BPHS via modern calculators |
|---|---|---|
| Sun | **5** | **6.5** |
| Moon | 6 | 6 |
| Mars | 5 | 5 |
| Mercury | 7 | 7 |
| Jupiter | 6.5 | 6.5 |
| Venus | 5.5 | 5.5 |
| Saturn | 5 | 5 |

Only the Sun differs, and it alone reorders the ranking. Also note the cardinal rule from §22:
Sun and Moon have **cheshta bala = 0 by design** — a component that is zero because the classical
definition says so must not be "fixed", but it must also not be silently carried into a published
total without being recomputed both ways.

## Probing recipe

1. Compute positions with explicit settings: `compute_positions(birth, sidereal=True, node="mean")` and `compute_houses(..., system="whole_sign", sidereal=True)`; add the Ascendant as a pseudo-body at `houses.ascendant`.
2. For each candidate division, call `varga_chart(pos, n)` and map each body to `int(lon // 30) % 12`.
3. **Map engine keys to your oracle's labels explicitly** (`Rahu`→`RA`, `Ketu`→`KE`, Ascendant→`AS`). The varga dict is keyed by the engine's planet names, not your table's column headers — getting this wrong yields a uniform 0/N failure that reads as a total scheme mismatch.
4. Record the per-division match counts as a pinned test so a rule change is loud, not silent.
5. Compare **whole extra systems**, not one chart, when an oracle exposes a selector — one ayanamsa sweep validates several code paths at once.
