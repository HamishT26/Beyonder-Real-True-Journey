# v467A GMUT v6 x2 Evidence Contract Schema

Prepared: 2026-06-01T21:59:44+12:00

This is a design-only schema contract. It is not an executed fixture and does not claim a result.

## Core Contract

The evidence contract splits authored rows from derived lint reports. A literal row records what the artifact actually says. A derived lint report records whether that row is structurally admissible. The split is mandatory because a lint pass cannot become a physics result.

Required literal row fields include `row_id`, `GMUT_KEY`, source anchor, affected expression refs, provenance entity/activity/agent IDs, presence state, comparison type, unit system, dimension status, and locked `not_run/no_result` execution fields.

Required derived lint fields include lint rule ID, lint status, reason code, claim ceiling, blocked fields, and non-implications.

## Enumerations

Presence states distinguish supported, symbolic, quarantined, unsupported, expected absence, permitted absence, declared null, derived null, not comparable, and withheld conflict. Null states distinguish measured zero, modeled zero, assumed zero, no detected signal, not applicable, and not evaluated.

Comparison types include scalar, vector, tensor, operator, symbolic identity, interval, distribution, bounded empirical, null test, residual, and not comparable. Unit status is limited to natural units, SI, mixed declared, or unset blocker. Dimension status is limited to declared only, missing dependency, blocked, or not checked.

## Hard Refusals

Forbidden inference fields include observed result, matches expected, recovered, validated, gate closed, fixture executed, pass hygiene only, safe, compatible, proven, and canon promoted. Any such field blocks publication until corrected.

All six GMUT gates remain `OPEN_NOT_TESTED`.
