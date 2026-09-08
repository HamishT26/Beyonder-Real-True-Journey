---
name: ghc-family-chess-pgn-header-movetext
description: Validate bounded synthetic PGN header-list and movetext-token records. Use for pgn_headers and pgn_movetext fixtures with duplicate and terminal-result guards.
---

# GHC Family Chess PGN Header and Movetext

Run `scripts/ghc_family_chess_record_skill.py FIXTURE.json`. This skill accepts only `pgn_headers` and `pgn_movetext`.

Positive headers are unique string pairs. Positive movetext has exactly one terminal result marker. Reject duplicate names, malformed pairs, misplaced results, missing results, extra fields, or a non-allowlisted operation. Preserve the full rejecting envelope.

This bounded record projection does not authenticate a game, player, result, archive, ownership, rights state, rating, tournament decision, professional practice, cultural or Maori authority, privacy/accessibility completeness, independent reproduction, consciousness, Theory-of-Everything, or Stage 20. Rollback must preserve inherited evidence.
