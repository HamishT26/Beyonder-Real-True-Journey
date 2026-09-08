---
name: ghc-family-chess-material-timeline
description: Validate synthetic chess material-count and halfmove-clock timeline records. Use for board_material and halfmove_timeline fixtures with typed nonnegative values.
---

# GHC Family Chess Material and Timeline

Use `scripts/ghc_family_chess_record_skill.py FIXTURE.json`. Only `board_material` and `halfmove_timeline` are accepted.

Material counts must use declared piece symbols and nonnegative integer counts. Timelines accept only quiet, pawn, and capture events from a nonnegative start. Reject booleans, negatives, unknown events or symbols, extra fields, or other operations. Treat rejections as retained evidence.

The values are conventional synthetic projections and do not establish position legality, game state, evaluation, material worth in every context, result, rating, tournament authority, professional advice, legal/cultural/Maori authority, privacy/accessibility completeness, independent evidence, consciousness, Theory of Everything, or Stage 20. Roll back additively.
