---
name: ghc-family-restricted-content-minimization
description: Fail closed on synthetic sensitive-content fields while reserving disclosure, access, remedy, legal, cultural, and Maori-authority decisions.
---

# GHC Family Restricted Content Minimization

Use this skill when a zero-record schema includes personal names, sensitive locations, access restrictions, sacred or culturally sensitive content, redaction, takedown, or remedy fields.

Require every payload value to be null or synthetic, minimize linkability, refuse disclosure by default, preserve challenge and remediation placeholders, and name the competent affected and Maori authorities as external decision owners. Reject real content, a unilateral access decision, cultural interpretation, legal conclusion, remedy award, consent claim, or substituted Maori authority.

Passing proves only that the synthetic firewall failed closed.
