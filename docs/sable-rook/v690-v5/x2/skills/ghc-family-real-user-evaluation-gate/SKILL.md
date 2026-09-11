---
name: ghc-family-real-user-evaluation-gate
description: Keep participant and assistive-technology evidence absent when no real evaluation occurred. Use only for bounded synthetic real_user_evaluation_gate review; do not invoke for real participant, professional, production, legal, cultural, Maori-authority, identity, accessibility-complete, or Stage 20 decisions.
---

# Real-user accessibility evaluation gate

Use [the accepting fixture](references/accepting.json) and require refusal of [the rejecting fixture](references/rejecting.json).

1. Preserve the exact finite input and case token.
2. Emit a closed ok/error/value envelope and keep the source unchanged.
3. Check zero participants stays visible; manual and affected-user review remains reserved.
4. Retain invalid subjects at zero original success credit.
5. Reserve manual, assistive-technology, affected-user, legal, cultural, Maori-authority, production, and Stage 20 decisions.

A structural pass is same-owner software evidence only and is not complete accessibility, privacy, security, recourse, or authority evidence.
