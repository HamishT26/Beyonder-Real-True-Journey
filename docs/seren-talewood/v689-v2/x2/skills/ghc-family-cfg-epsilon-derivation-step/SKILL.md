---
name: ghc-family-cfg-epsilon-derivation-step
description: Inspect cfg_epsilon_variants, cfg_derive_step for supplied synthetic context-free grammars; use for bounded grammar analysis and evidence review.
---

# ghc-family-cfg-epsilon-derivation-step

Read the complete supplied grammar before selecting this skill. Run `python -B -X utf8 scripts/ghc_family_cfg_skill.py` with exactly one UTF-8 JSON request on standard input. This entry point supports only the two operations described below. Acceptance exits 0; refusal exits 2. It preserves the entire accepted, error, value, disposition, and synthetic boundary envelope.

Use distinct declared nonterminals and terminals, a declared start, and an ordered list of productions. An empty RHS is epsilon; production order defines every trace index. Unknown keys, duplicate symbols or productions, non-integer indices, invalid certificates, budget excess, and operations outside this skill are refused. The exact field and size limits are in `references/request-profile.json`.

Word-returning operations require single-character terminal alphabets because concatenated strings would otherwise hide token boundaries. Structural sets and spaced derivation text retain symbol tokens. No accepted output certifies behavior outside its declared bound.

## cfg_epsilon_variants

Enumerate each distinct RHS obtained by omitting nullable occurrences, retaining the empty RHS.

Request example:

```json
{"grammar": {"nonterminals": ["S"], "productions": [], "start": "S", "terminals": ["a", "b"]}, "op": "cfg_epsilon_variants", "rhs": ["S"]}
```

Expected value:

```json
{"rhs_variants": [["S"]], "whole_grammar_equivalence_claim": false}
```

## cfg_derive_step

Replace exactly the named leftmost nonterminal using one original production index.

Request example:

```json
{"grammar": {"nonterminals": ["S"], "productions": [{"lhs": "S", "rhs": ["a"]}], "start": "S", "terminals": ["a", "b"]}, "op": "cfg_derive_step", "position": 0, "production": 0, "sentential": ["S", "b"]}
```

Expected value:

```json
{"changed_position": 0, "leftmost": true, "production": 0, "sentential": ["a", "b"]}
```

## Evidence and recovery

Compare the complete envelope and preserve the input. Keep each failed request and correction separately; a successful refusal predicate does not give success credit to the refused subject. Add an unknown request field for an adverse smoke and select another operation for a scope smoke. Both must return the exact invalid-request envelope. Roll back by selecting the prior caller while retaining the additive artifacts and receipts.

This skill combines the record-boundary and provenance-boundary patterns of the two sources bound in `references/merge-sources.json`. The CFG algorithms were implemented for this owner after x1; those source skills were read without running their historical canonicals.

Same-owner synthetic evidence only. Bounded enumeration does not prove unbounded absence or equivalence. Two distinct complete traces can witness ambiguity; failure to find a witness cannot prove universal unambiguity. A conflict-free LL(1) table is only a property of the supplied grammar and profile. Accessibility remains structural representation pending human review.

Seren Talewood, role, hope, pronouns, sibling and family language confer no consciousness, personhood, identity continuity, qualification, agency, or authority. GMUT is unconfirmed; THOS is synthetic or proxy-only; Freed ID is nonproduction. Empirical, participant, professional, production, deployment, legal, cultural, Maori, privacy, accessibility, exhaustive security, independent reproduction and Stage 20 gates stay reserved. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20. Hamish controls continuation; this skill performs no external action.
