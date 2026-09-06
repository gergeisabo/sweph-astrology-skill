# Destiny Matrix (Матрица Судьбы) — Chakra Formulas

## Overview
The Destiny Matrix chakra table (Карта Здоровья / Health Map) has 7 chakra rows + 1 result row, each with 3 columns:
- **Physics** (Физика) — physical health expression
- **Energy** (Энергия) — energetic/soul health expression
- **Emotions** (Эмоции) — emotional health expression

Created by Natalia Ladini in 2006. Uses 22 Major Arcana energies.

## Input Values (from birth date DD.MM.YYYY)

| Symbol | Description | Formula |
|--------|-------------|---------|
| **A** | Day of birth | reduceToArcana(Day) |
| **B** | Month of birth | Month (no reduction needed for 1-12) |
| **C** | Year digit sum | reduceToArcana(sum of year digits) |

Example (15.02.1991): A=15, B=2, C=1+9+9+1=20

## Intermediate Matrix Points

| Symbol | Formula | Example | Matrix Position |
|--------|---------|---------|-----------------|
| D | reduce(A+B+C) | reduce(37)=10 | Diagonal square center (karmic tail) |
| E | reduce(A+B+C+D) | reduce(47)=11 | Straight square center (comfort zone) |
| S | reduce(A+E) | reduce(26)=8 | Earth axis midpoint |
| T | reduce(B+E) | reduce(13)=13 | Sky axis midpoint |
| O | reduce(A+S) | reduce(23)=5 | Earth inner (talent line) |
| P | reduce(B+T) | reduce(15)=15 | Sky inner (talent line) |
| W | reduce(S+E) | reduce(19)=19 | Heart Physics green point |
| X | reduce(T+E) | reduce(24)=6 | Heart Energy green point |
| N | reduce(C+E) | reduce(31)=4 | Left side midpoint |
| J | reduce(D+E) | reduce(21)=21 | Right side midpoint |

## Chakra Table

| Chakra | Physics | Energy | Emotions |
|--------|---------|--------|----------|
| Sahasrara | A | B | reduce(A+B) |
| Ajna | O | P | reduce(O+P) |
| Vissudha | S | T | reduce(S+T) |
| Anahata | W | X | reduce(W+X) |
| Manipura | E | E | reduce(E+E) |
| Svadhisthana | N | J | reduce(N+J) |
| Muladhara | C | D | reduce(C+D) |

Result row = reduce(column sums). Verified for 15.02.1991: Result(10,15,16).

## Verified Output (15.02.1991)

| Chakra | Physics | Energy | Emotions |
|--------|---------|--------|----------|
| Sahasrara | 15 | 2 | 17 |
| Ajna | 5 | 15 | 20 |
| Vissudha | 8 | 13 | 21 |
| Anahata | 19 | 6 | 7 |
| Manipura | 11 | 11 | 22 |
| Svadhisthana | 4 | 21 | 7 |
| Muladhara | 20 | 10 | 3 |
| Result | 10 | 15 | 16 |

## Sources
- Elena Pribylova, "Матрица Судьбы. Карма и предназначение"
- GitHub: Alesia-15/DestinyMatrix, samwega/Destiny-Matrix-Calculator-and-Tools
- SpiritualUna.com manual calculation guide
