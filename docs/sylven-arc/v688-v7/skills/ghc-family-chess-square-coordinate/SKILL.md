---
name: ghc-family-chess-square-coordinate
description: Validate bounded synthetic chess-square coordinate records. Use for strict square_parse and square_name fixtures when exact field sets, reversible rejection, and non-authority boundaries matter.
---

# GHC Family Chess Square Coordinate

Use `scripts/ghc_family_chess_record_skill.py FIXTURE.json` for one JSON fixture. The only accepted operations are `square_parse` and `square_name`.

Require the complete evaluator envelope and exit code: zero means the fixture was accepted; two means it was deliberately rejected. For an accepting smoke, use a lowercase algebraic square such as `a1` or an integer index from 0 through 63. For an adverse smoke, add an unknown field or use an out-of-range index. Retain every adverse result; never rewrite it as completion credit.

This skill provides same-owner synthetic record evidence only. It does not establish a real chess position, lawful move, game result, rating, tournament ruling, professional authority, cultural or Maori authority, accessibility completeness, independent reproduction, consciousness or personhood, Theory of Everything, or Stage 20 readiness. Roll back by removing the additive package or restoring its hash-verified predecessor; do not mutate source evidence.
