---
name: ghc-family-chess-castling-en-passant
description: Validate synthetic castling-right and en-passant record tokens. Use for fen_castling and fen_en_passant fixtures with canonical ordering and explicit absence markers.
---

# GHC Family Chess Castling and En Passant

Invoke `scripts/ghc_family_chess_record_skill.py FIXTURE.json`. Only `fen_castling` and `fen_en_passant` are in scope.

Accept canonical `KQkq` subsets or `-`, and en-passant targets on ranks 3 or 6 or `-`. Reject duplicates, noncanonical order, other ranks, and extra fields. Preserve adverse receipts as failed witnesses.

This is a syntax and obligation guard, not proof that a capture or castling move is legal or occurred. It confers no game, competition, rating, professional, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, independent, consciousness, Theory-of-Everything, or Stage 20 claim. Use additive rollback only.
