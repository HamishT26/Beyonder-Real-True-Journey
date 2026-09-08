---
name: ghc-family-chess-san-pgn-tag
description: Validate bounded synthetic SAN-token and PGN-tag syntax. Use for san_token and pgn_tag fixtures where strict quoting and zero-execution parsing are required.
---

# GHC Family Chess SAN and PGN Tag

Pass one fixture to `scripts/ghc_family_chess_record_skill.py`. Only `san_token` and `pgn_tag` are allowed.

Use exact synthetic tokens and quoted tag-pair lines for accepting tests. Use malformed notation, bad quoting, escapes outside the profile, extra fields, or another operation for rejecting tests. A rejected fixture must remain a failed witness at zero completion credit.

The parser is not a full legality checker or archival, competition, professional, copyright, cultural, Maori-authority, privacy, accessibility, independent-review, empirical, consciousness, Theory-of-Everything, or Stage 20 authority. Removal or restoration is additive and hash checked.
