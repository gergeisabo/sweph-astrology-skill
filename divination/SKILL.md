---
name: divination
description: "Use when drawing tarot, I Ching, runes, or geomancy. No birth data needed — oracle draws for questions, daily pulls, spreads."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [astrology, tarot, iching, runes, geomancy, divination, oracle]
    category: astrology
    related_skills: [astrologica]
---

# Divination — `astrologica.divination`

Hardcoded data, no external files, NO birth data of any kind. All draws accept
`seed: int | None` — pass a seed for reproducible readings (verified: same seed → same
draw), omit it for a true random draw.

```python
from astrologica import divination
# run with: ~/Projects/astrologica/.venv/bin/python, cwd ~/Projects/astrologica
```

## ⚠️ tarot_draw and runes_draw are GENERATORS

Wrap in `list(...)` or you get a generator, not results. For a *named* spread use
`tarot_spread(name, seed=42)` (below) instead of hand-labelling `tarot_draw`.

## Functions — verified live

| Call | Use when |
|---|---|
| `list(divination.tarot_draw(n=3, system='rider_waite', seed=42))` | daily pull (n=1) or spread (n≥3); decks: `rider_waite` (78), `marseille`, `lenormand` (36) |
| `divination.iching_throw_coins(seed=42)` | full coin cast: primary + resulting hexagram, changing_lines |
| `divination.iching_lookup(1)` | hexagram facts by number 1–64 (ValueError outside) |
| `divination.iching_by_question('Should I take the job?', seed=99)` | question-specific cast; same question text without seed is stable per process |
| `list(divination.runes_draw(n=3, system='elder_futhark', seed=42))` | rune draw; sets: `elder_futhark` (24), `younger_futhark` (16), `anglo_saxon_futhorc` (33) |
| `divination.geomancy_cast(seed=42)` | full chart: 4 mothers → daughters/nephews/witnesses/judge |
| `divination.geomancy_lookup('fortuna major')` | figure facts by name (title-cased match; ValueError on unknown) |
| `divination.tarot_spread('three_card', seed=42)` | named spread → `{spread, cards:[{..., meaning}]}`; names: `three_card` (Past/Present/Future), `celtic_cross` (10), `daily` (1), `relationship` (7). Hyphen/underscore interchangeable. ValueError on unknown |

## Gold draws — verified live (seed=42 unless noted)

- tarot 3-card rider_waite: Temperance (rev), The Empress (rev), King of Wands (rev)
- iching: primary 42 Increase 益, resulting 1 The Creative, changing lines [2,4,5]
- runes elder 3: Laguz upright, Ansuz reversed, Fehu reversed
- geomancy: mothers [Puella, Populus, Laetitia, Populus], judge **Populus** (favorable)
- tarot_spread three_card (seed=42): 3 cards, meanings Past/Present/Future (cards = same as tarot_draw(3))
- tarot_spread celtic_cross (seed=42): 10 cards ending in Outcome; reproducible per seed

## Choosing a tool

- Quick daily guidance → `tarot_draw(n=1)` or `runes_draw(n=1)`
- Multi-facet situation → `tarot_draw(n=3+)` or `geomancy_cast` (structured houses)
- A specific yes/no-or-advice question → `iching_by_question(q)`
- Looking up a card/hexagram/figure already mentioned → `*_lookup` (deterministic, no RNG)

Reversed cards/runes: `reversed` bool; rune `meaning` already flips to the reversed
sense; tarot keywords stay upright — interpret reversal yourself.
