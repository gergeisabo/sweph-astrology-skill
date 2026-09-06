---
name: destiny-matrix
description: "Use when computing the Destiny Matrix (Матрица судьбы / Ladini) chakra table, karmic tail, or arcana math. Authoritative formulas; note the engine's destiny.py is a different simpler grid."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [numerology, destiny-matrix, ladini, arcana, chakra, karmic-tail]
    category: astrology
    related_skills: [astrologica, numerology]
---

# Destiny Matrix (Ladini) — Formula Reference

Pure-math computation for esoteric/numerological systems. No API calls. Use alongside `astrologica` which handles astronomical calculations.

## When to Use

User asks for: destiny matrix chakra table, health map (карта здоровья), Ladini matrix computation, arcana reduction, numerology digit-sum computation, or any birth-date-based esoteric calculation where the formula is deterministic.

For planetary positions, houses, transits → use `astrologica` instead.

## Core Reduction: reduceToArcana(n)

The fundamental operation across all these systems. If n > 22, **repeatedly** sum digits until ≤ 22.

```python
def reduce_to_arcana(n: int) -> int:
    n = abs(int(n))
    while n > 22:
        n = sum(int(d) for d in str(n))
    return 22 if n == 0 else n
```

**PITFALL:** Some calculators use single-pass digit sum (`n % 10 + n // 10`) or modulo 22. These produce WRONG values for certain inputs. Example: `reduceToArcana(24)` must be 6 (2+4), NOT 2 (24 mod 22). Always use recursive digit-sum.

## System 1: Destiny Matrix Chakra Table (Ladini)

Full formula reference: `references/destiny-matrix-chakra-formulas.md`. Worked example for 15.02.1991: `references/verified-1991-02-15-chakras.md`.

### Quick Summary

Birth date DD.MM.YYYY → three base values:
- A = reduceToArcana(Day)
- B = Month (no reduction for 1-12)
- C = reduceToArcana(year digit sum)

Key intermediate points:
```
D = reduce(A + B + C)           # karmic tail
E = reduce(A + B + C + D)       # comfort zone
S = reduce(A + E)               T = reduce(B + E)
O = reduce(A + S)               P = reduce(B + T)
W = reduce(S + E)               X = reduce(T + E)
N = reduce(C + E)               J = reduce(D + E)
```

Chakra table (Physics, Energy, Emotions):
```
Sahasrara:      A,          B,          reduce(A+B)
Ajna:           O,          P,          reduce(O+P)
Vissudha:       S,          T,          reduce(S+T)
Anahata:        W,          X,          reduce(W+X)
Manipura:       E,          E,          reduce(E+E)
Svadhisthana:   N,          J,          reduce(N+J)
Muladhara:      C,          D,          reduce(C+D)
```

Result row = reduce(column sums). Verified against multiple online calculators for birth date 15.02.1991.

### Matrix Geometry

The octagram has two overlapping squares:
- **Diagonal square** (ромб): Day, Month, YearSum corners + center D
- **Straight square** (квадрат): center E, derived from D + corners

Physics = Earth (horizontal) axis values. Energy = Sky (vertical) axis values.
W, X = "green points" (зелёные точки) on talent/DRK lines for Anahata.

## System 2: Basic Numerology Reduction

```python
def life_path_number(day: int, month: int, year: int) -> int:
    """Reduce date components separately, then sum and reduce."""
    d = sum_digits(day)
    m = sum_digits(month)
    y = sum_digits(year)
    return sum_digits(d + m + y)

def sum_digits(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n
```

## Pitfalls

1. **Reduction method matters:** Recursive digit-sum until target threshold. Different thresholds for different systems (≤22 for arcana, ≤9 for numerology).
2. **Month is NOT reduced** in Destiny Matrix base values (January=1, ..., December=12). It's already ≤22.
3. **Year digit sum** is computed BEFORE reduction: 1991 → 1+9+9+1 = 20 (already ≤22, no further reduction).
4. **Different calculators, different results:** Open-source implementations vary in reduction method. The recursive digit-sum method matches the majority of Russian-language reference calculators.
5. **The Anahata "green points"** (W and X) are NOT simple midpoints — they're computed from S+E and T+E respectively, placing them on the talent/DRK lines.
6. **`astrologica.destiny.compute()` is a different, simpler grid.** It is not this Ladini chakra table. Do not mix them. For 15.02.1991 the verified Ladini center is E=11 Justice, karmic tail D=10 Wheel — not engine center Lovers / money Tower. An older vault reading (2026-06-26) that put Devil at center used the wrong formulas; do not reuse it.
