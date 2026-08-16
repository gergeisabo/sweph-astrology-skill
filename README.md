# astrologica — Hermes Agent Skill

Hermes Agent skill for the [astrologica](https://github.com/gergeisabo/sweph-astrology) local astrology engine.

## What It Does

Gives Hermes Agent the ability to compute astrological charts and readings **fully locally** — no external API calls, no rate limits, no credits. Covers Western, Vedic, BaZi, Human Design, Zi Wei Dou Shu, Destiny Matrix, Mayan, Numerology, Tarot, and more.

## Prerequisites

- [astrologica](https://github.com/gergeisabo/sweph-astrology) installed at `~/Projects/astrologica`
- Python 3.11+ with pyswisseph (the engine's venv handles this)

## Install

```bash
hermes skills install gergeisabo/sweph-astrology-skill
```

Or manual:
```bash
git clone https://github.com/gergeisabo/sweph-astrology-skill /tmp/sweph-astrology-skill
cp -r /tmp/sweph-astrology-skill ~/.hermes/skills/astrology/astrologica
```

## Usage

Once installed, Hermes automatically loads the skill when you ask about astrology:

- "What's my natal chart?"
- "Calculate transits for next week"
- "Find muhurat for buying a car in September"
- "What are the eclipses in 2026?"
- "Compatibility between these two charts"

The skill tells Hermes how to import and use the astrologica Python library.

## Related

- [astrologica engine](https://github.com/gergeisabo/sweph-astrology) — the computation library
- [Swiss Ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm) — the astronomical engine underneath
