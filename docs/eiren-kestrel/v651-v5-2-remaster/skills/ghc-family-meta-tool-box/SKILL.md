---
name: ghc-family-meta-tool-box
description: Catalogue, validate, compare, and query GHC Family skills, runners, commands, methods, and workflows by trigger, lifecycle status, owner scope, evidence state, caller compatibility, and rollback. Use when selecting current reusable tools, preparing a handoff tool list, checking trigger collisions, evaluating a candidate global promotion, or preventing blind execution and bulk installation.
---

# GHC Family Meta Tool Box

## Purpose

Build a small evidence-bound catalogue before selecting reusable tools. Treat discovery as inventory, not execution or authorization. A catalogue entry is usable only within its recorded scope and never upgrades a candidate into production, scientific, legal, cultural, identity, privacy-complete, security-complete, accessibility-complete, or independent-reproduction evidence.

## Required workflow

1. Identify the repository root and the narrow phase or tool roots that are in scope.
2. Run `scripts/ghc_family_meta_tool_box.py build` with repository-relative inputs and outputs.
3. Run `validate` before using the catalogue.
4. Run `collisions`; keep unresolved trigger overlap visible.
5. Run `query` with the narrowest useful filters. Prefer `evidence_state=validated` and `status=current`, but do not invent either value.
6. Before global promotion, run `promotion` and require a passing validation receipt, caller evidence, rollback, owner attribution, and no destructive action.
7. Preserve failed validations and rejected mutations as Method Flow negatives.

## Commands

```powershell
python scripts/ghc_family_meta_tool_box.py build --repo . --phase-root docs/eiren-kestrel/v651-v5-2-remaster --output docs/eiren-kestrel/v651-v5-2-remaster/tooling/meta-tool-box/catalogue.json
python scripts/ghc_family_meta_tool_box.py validate --catalogue docs/eiren-kestrel/v651-v5-2-remaster/tooling/meta-tool-box/catalogue.json --output docs/eiren-kestrel/v651-v5-2-remaster/tooling/meta-tool-box/validation.json
python scripts/ghc_family_meta_tool_box.py collisions --catalogue docs/eiren-kestrel/v651-v5-2-remaster/tooling/meta-tool-box/catalogue.json --output docs/eiren-kestrel/v651-v5-2-remaster/tooling/meta-tool-box/collisions.json
python scripts/ghc_family_meta_tool_box.py query --catalogue docs/eiren-kestrel/v651-v5-2-remaster/tooling/meta-tool-box/catalogue.json --kind skill --status current --output docs/eiren-kestrel/v651-v5-2-remaster/tooling/meta-tool-box/query.json
```

Use `--trigger`, `--evidence-state`, and `--owner-scope` only when those filters are supported by the recorded card fields. A zero-result query is a valid refusal, not permission to broaden silently.

## Promotion boundary

Global promotion is additive and curated. Never bulk-install everything discovered. Never delete, rewrite, reset, force-push, weaken host security, enable a Windows feature, or install unrelated software through this skill. Promote one validated package at a time, preserve its source hash and rollback path, validate the installed copy, and retain any failed attempt at zero credit.

## Boundaries

Catalogue discovery never authorizes blind execution, bulk installation, destructive cleanup, sibling-lane mutation, production deployment, empirical or participant claims, professional decisions, legal or cultural decisions, Māori authority, identity continuity, consciousness or personhood claims, independent reproduction, AGI or ASI claims, Theory-of-Everything claims, or Stage 20 promotion.

## Collision and staleness rules

- Similar trigger tokens create a review issue; they do not select a winner.
- Historical or compatibility-labelled surfaces stay visible when callers remain.
- Absence of a caller is not proof that deletion is safe.
- A newer timestamp or larger version number is not evidence of quality.
- Same-owner validation under shared infrastructure is not independent reproduction.

## References

Read [references/catalogue-schema.md](references/catalogue-schema.md) when adding fields or building a compatible caller. Keep repository artifacts free of absolute private paths, private routes, raw task identifiers, credentials, transcripts, screenshots, and private application state.
