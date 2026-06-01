# v470 THOS v1 x2 Validation Matrix

Classification: `evidence`

This matrix uses `PASS_SHAPE_ONLY`, `FAIL_BLOCKER`, and `OPEN_GAP`. It never uses generic `PASS` because THOS x2 is validating structure and policy shape, not runtime cleanup or physics.

## Predicates

| Check | Predicate | Status |
| --- | --- | --- |
| THOS-CHK-001 | Command rows have mutation level and approval policy | `PASS_SHAPE_ONLY` |
| THOS-CHK-002 | Advisory-allowed commands are read-only | `PASS_SHAPE_ONLY` |
| THOS-CHK-003 | Git mutation requires publication authority | `PASS_SHAPE_ONLY` |
| THOS-CHK-004 | Destructive cleanup is blocked in advisory lanes | `PASS_SHAPE_ONLY` |
| THOS-CHK-005 | Connector writes require explicit approval | `PASS_SHAPE_ONLY` |
| THOS-CHK-006 | Credential-sensitive surfaces cannot expose values | `PASS_SHAPE_ONLY` |
| THOS-CHK-007 | Cleanup candidates classify reversibility | `PASS_SHAPE_ONLY` |
| THOS-CHK-008 | Raw material is non-publishable | `PASS_SHAPE_ONLY` |
| THOS-CHK-009 | Publication claims need source authority | `PASS_SHAPE_ONLY` |
| THOS-CHK-010 | THOS cannot import GMUT validation | `PASS_SHAPE_ONLY` |
| THOS-CHK-011 | Generic pass wording is forbidden | `PASS_SHAPE_ONLY` |
| THOS-CHK-012 | GMUT gate effect remains `none_open_not_tested` | `PASS_SHAPE_ONLY` |

## Result

All x2 validation predicates pass shape only. No runtime cleanup, connector mutation, external service change, or GMUT validation is claimed.
