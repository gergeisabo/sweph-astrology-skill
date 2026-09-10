# sweph-astrology-skill

Per-system Hermes Agent skills for the local [sweph-astrology](https://github.com/gergeisabo/sweph-astrology) (astrologica) engine. Every documented API call is live-verified against the gold birth.

## Skills

| Skill | Covers | CLI |
|---|---|---|
| `astrologica` | Routing hub: birth data, positions, houses, CLI, gold birth | `astro …` |
| `western-astrology` | Natal, aspects, transits, synastry, returns, profections, ACG | `astro natal/transits/timing/svg` |
| `vedic-astrology` | Sidereal charts, nakshatras, dashas, panchang, muhurat, ashtakavarga | `astro vedic` |
| `bazi` | Four Pillars, Ten Gods, luck pillars | `astro bazi` |
| `human-design` | Type/authority/profile, gates/channels, Rave Variables | `astro hd` |
| `ziwei` | Zi Wei Dou Shu palaces, bureau, sihua (solar→lunar built in) | `astro ziwei` |
| `mayan` | Tzolkin, Haab, Long Count, Dreamspell | `astro mayan` |
| `numerology` | Life path, soul urge, expression, chaldean/kabbalistic | `astro numerology` |
| `divination` | Tarot, I Ching, runes, geomancy (seeded) | — |
| `destiny-matrix` | Destiny Matrix (Ladini) chakras — authoritative | — |
| `pyswisseph-pitfalls` | Engine-building pitfalls | — |
| `astrology-readings` | Multi-system synthesis method | — |

Install each dir under `~/.hermes/skills/astrology/<name>/`.
