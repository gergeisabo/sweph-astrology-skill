# Verifying astrological output

How to check a chart, a report, or a claim about a chart so the check means something.
Read this before calling any astrological result "verified", and before trusting a
second source because it agrees.

---

## 1. Two sources that share a setting are one source

"Independently verified" is only meaningful if the paths differ in the thing being tested.
Two implementations that both default to the same hidden mode agree perfectly and prove
nothing about whether that mode is correct — and the perfect agreement manufactures the
confidence that stops anyone looking further.

Observed: a chart report asserted its web-service export and a recomputation in a
different library "agree to the minute on the Lagna and all nine grahas". They did — both
used the TRUE node. Another export for the same person quoted the MEAN node, 69 arc-min
away. Neither document stated the node mode, so the mismatch was invisible and the
agreement covered for it.

**Rule:** before calling a check independent, list the axes it could vary — ephemeris data
files, ayanamsa, node mode, house system, time source, coordinate precision — and confirm
the two paths actually differ on the axis under test. Differ on none ⇒ the check is a
tautology.

## 2. Every published number carries its mode, or it is not a result

A node, ayanamsa, house cusp, varga or dasha date with no stated mode is unverifiable and
unreproducible. Put the mode on the same line as the value, or in a header that provably
covers the block — never in a footnote three sections away. A value whose mode is unknown
should be reported as *unknown*, not silently defaulted and presented as fact.

## 3. The error budget is four orders of magnitude away from the maths

Measured on the gold chart. Rows are ordered by how far each source moves a position:

| source of error | effect |
|---|---|
| Swiss Ephemeris intrinsic (DE431, 1800–2400) | **< 1 arc-second** |
| coordinates rounded to the arc-minute | 0.1 arc-min |
| birth time off by 1 minute | **11 arc-min** of Ascendant |
| true vs mean node | **69 arc-min** |
| ayanamsa choice (Raman vs Lahiri) | **87 arc-min** |
| birth time off by 1 hour | **~11°** |

Read the first row against the rest. The calculation is ~1 arc-second and the configuration
is measured in degrees.

**Consequence:** effort spent chasing arc-seconds is wasted; effort spent removing *silent
default modes* pays back in degrees. Concretely — make every mode an explicit argument or
record it in the output, refuse to guess a birth time, and print the modes a result used.
Do not "improve" the astronomy; it is not the limiting factor and never was.

Corollary: a ~16 arc-second disagreement against a published reference is expected (method
difference between manual ayanamsa subtraction and `FLG_SIDEREAL`), not a bug. Do not spend
a session on it.

## 4. A component you know is broken poisons every derived total

When a report flags one strength component as suspect and then publishes totals and a
ranking built from those totals, the flag does not neutralise the error — it gives the
error cover.

Observed: a shadbala table listed Saturn's `cheshta` as 0 with a "known tool bug" note, then
ranked Saturn third. Recomputing with the correct value (60, the maximum):

```
cheshta=60 (correct):  471.26 virupas → ratio 1.571
cheshta=0  (the bug):  411.26 virupas → ratio 1.371
```

`1.371` is the number the report published, to three decimals. The published figure **was**
the bug, and the note had already told the reader to trust the ranking.

**Rule:** if a component is suspect, recompute with and without it, publish both, and mark
the ranking provisional — or drop the ranking. Never ship a derived ordering built on a sum
you have already annotated as corrupt.

Second-order rule: multi-variant measures (shadbala minimum values differ by author;
`cheshta`/`naisargika`/`ishta` are optional components) are only comparable between runs
that used the **same variant**. Two engines disagreeing on a ranking is not evidence either
is broken — it is evidence the variant was not stated. State it, then compare.

## 5. Verification checklist

- [ ] Every compared value has its mode stated on the same line or in a covering header
- [ ] The two paths differ on the axis under test (not just "they are different tools")
- [ ] Any value reported to the user is reproducible from the stated inputs alone
- [ ] Suspect components: figure recomputed both ways, or ranking marked provisional
- [ ] Multi-variant measures: the variant is named with the numbers
- [ ] Tolerance claims are earned — a ~16" gap vs a published reference is normal, not a bug
