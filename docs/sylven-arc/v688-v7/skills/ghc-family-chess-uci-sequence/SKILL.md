---
name: ghc-family-chess-uci-sequence
description: Validate bounded synthetic UCI move-token and sequence records. Use for uci_move and uci_sequence fixtures without executing a game or chess engine.
---

# GHC Family Chess UCI Sequence

Run `scripts/ghc_family_chess_record_skill.py FIXTURE.json`. The allowlist is exactly `uci_move` and `uci_sequence`.

Accept coordinate tokens, optional lowercase promotion symbols, the explicit null marker, and lists no longer than the bounded profile permits. Reject malformed tokens, oversized sequences, unknown fields, and other operations. Capture both accepting and adverse smoke evidence.

Parsing does not prove move legality, execution, engine strength, game outcome, rating, tournament authority, participant evidence, deployment, professional competence, legal or cultural status, Maori authority, completeness, independent reproduction, consciousness, Theory of Everything, or Stage 20. Roll back without altering inherited artifacts.
