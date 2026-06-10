# v470 THOS v6 x3 Enum And Null Semantics

This artifact freezes the next useful semantic boundary for THOS export rows.

## Statuses

- `PASS_SHAPE_ONLY`: local shape, guard, or deterministic report structure passed only at the declared scope.
- `OPEN_GAP`: a scope, approval, proof, or artifact requirement remains open.
- `FAIL_BLOCKER`: a route is blocked until exact corrective evidence or approval exists.
- `NOT_RUN`: a check was declared but not executed.

## Reconciliation

Unexpected success is never approval. It is a boundary failure. Unexpected failure is not automatically a broken validator; it needs reconciliation. Reporting failure means the execution may have been acceptable but the export dropped required authority fields.

## Nulls

`null`, `unknown`, `not_applicable`, `missing`, and `empty_array` must stay distinct. The most important rule is simple: missing required provenance is a blocker or open gap, not a quiet null.
