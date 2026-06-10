# v470 THOS v2 x2 Template Validation Schema

This artifact defines a local THOS validator contract for the v2 x1 template family. It is a schema and policy scaffold only.

## Status Model

- `PASS_SHAPE_ONLY`: the target has the required shape; this is not runtime success.
- `FAIL_BLOCKER`: the target violates a safety, authority, retention, approval, or claim-boundary rule.
- `OPEN_GAP`: the target needs evidence or definition before it can be checked.
- `NOT_RUN`: the check is defined but not executed.

Generic `PASS` is forbidden because it collapses shape, runtime, authority, and safety into one overclaim-prone word.

## Required Global Fields

- `artifact`
- `phase`
- `classification`
- `template_or_checks`
- `claim_ceiling`
- `gmut_gate_effect`

`gmut_gate_effect` must equal `none_open_not_tested`.

## Core Invariants

- Advisory lanes cannot claim execution, cleanup, publication, connector writes, or external mutation.
- Write-capable surfaces require explicit separate approval.
- Raw logs, session JSONL, screenshots, and credential-bearing material are not publishable current-phase artifacts.
- Journey and Solas material can only be `journey_context_not_canon`.
- THOS validation cannot close any GMUT gate.

## GMUT Gate Carry

All six gates remain open: null recovery, dimensional/SI consistency, conservation or exchange law, baseline recovery, fifth-force/equivalence constraints, and consciousness measurement bridge.
