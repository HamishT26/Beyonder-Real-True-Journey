# Catalogue schema

Each capability card must contain:

- `card_id`: stable family-current identifier.
- `name` and `kind`: human name plus one of `skill`, `runner`, `command`, `method`, or `workflow`.
- `source_path` and `sha256`: repository-relative provenance and exact content digest.
- `status`: `current`, `compatibility`, `historical`, or `candidate`.
- `evidence_state`: `observed`, `validated`, `preferred`, or `exact_gate`.
- `owner_scope`: the bounded owner or family scope; never identity continuity.
- `triggers`: normalized selection terms.
- `caller_paths`: repository-relative observed callers, possibly empty.
- `rollback`: additive rollback or recovery text.
- `protected_gates`: boundaries that selection must not erase.

Validation rejects absolute paths, duplicate identifiers, unknown enum values, missing rollback, and missing protected gates. Collision analysis is advisory and must not silently choose between overlapping cards. Promotion readiness requires a valid catalogue, a validated evidence state, at least one bounded caller or smoke witness, a rollback statement, and an additive installation plan.
