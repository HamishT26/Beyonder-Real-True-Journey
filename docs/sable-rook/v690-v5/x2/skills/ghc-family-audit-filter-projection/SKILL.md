---
name: ghc-family-audit-filter-projection
description: Project declared audit rows through explicit status and pillar filters without mutating the source. Use only for bounded synthetic audit_filter_projection review; do not invoke for real participant, professional, production, legal, cultural, Maori-authority, identity, accessibility-complete, or Stage 20 decisions.
---

# Audit dashboard filter projection

Use [the accepting fixture](references/accepting.json) and require refusal of [the rejecting fixture](references/rejecting.json).

1. Preserve the exact finite input and case token.
2. Emit a closed ok/error/value envelope and keep the source unchanged.
3. Check visible rows satisfy both filters; source row order remains stable.
4. Retain invalid subjects at zero original success credit.
5. Reserve manual, assistive-technology, affected-user, legal, cultural, Maori-authority, production, and Stage 20 decisions.

A structural pass is same-owner software evidence only and is not complete accessibility, privacy, security, recourse, or authority evidence.
