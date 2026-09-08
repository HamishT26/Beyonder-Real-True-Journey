---
name: ghc-family-chess-record-fixity-provenance
description: Project bounded synthetic chess-record fixity and provenance vacancies. Use for chess_record_fixity and chess_record_provenance fixtures without claiming authenticity or publication authority.
---

# GHC Family Chess Record Fixity and Provenance

Run `scripts/ghc_family_chess_record_skill.py FIXTURE.json`. The exact allowlist is `chess_record_fixity` and `chess_record_provenance`.

Fixity produces raw and CRLF-to-LF digests while explicitly refusing authenticity. Provenance accepts only a synthetic `observed: false` record and either exposes missing source fields or preserves declared/unknown rights and absent/declared review. Reject real-observation claims, malformed digests, expanded states, unknown fields, and other operations.

Digests do not authenticate content, authorship, ownership, consent, legality, cultural legitimacy, Maori authority, publication permission, privacy/accessibility completeness, independent reproduction, professional custody, empirical truth, consciousness, Theory of Everything, or Stage 20. Preserve all failed fixtures and use reversible additive rollback.
