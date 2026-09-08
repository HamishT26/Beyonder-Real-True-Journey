---
name: ghc-family-chess-fen-structure
description: Validate bounded synthetic FEN board and six-field record structure. Use for fen_board and fen_record fixtures with strict fields, typed counters, and retained rejection evidence.
---

# GHC Family Chess FEN Structure

Run `scripts/ghc_family_chess_record_skill.py FIXTURE.json`. This package accepts only `fen_board` and `fen_record` operations.

An accepting fixture must encode exactly eight board ranks or exactly six FEN fields, respectively. An adverse fixture should use a rank-width mismatch, bad active colour, invalid counter, or unknown field. Record the full envelope and distinguish a rejected mutation from a tool failure.

The result is a synthetic structural projection, not validation of a real position, legality, provenance, tournament result, rating, professional decision, accessibility, privacy, legal or cultural status, Maori authority, independent review, Theory of Everything, or Stage 20. Rollback is additive package removal or hash-verified predecessor restoration only.
