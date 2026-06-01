# v470 THOS v1 x2 Retention And Source Test Suite

Classification: `evidence`

Retention and source tests make sure THOS preserves receipts without publishing raw operational exhaust or upgrading context into proof.

## Tests

| Test | Predicate | Status |
| --- | --- | --- |
| RET-001 | Durable phase artifacts are publishable summaries | `PASS_SHAPE_ONLY` |
| RET-002 | Raw logs, session JSONL, and screenshots are `do_not_publish_raw` | `PASS_SHAPE_ONLY` |
| RET-003 | Advisory receipts are labeled advisory-only | `PASS_SHAPE_ONLY` |
| RET-004 | External context cannot prove local execution | `PASS_SHAPE_ONLY` |
| RET-005 | Journey context remains not canon | `PASS_SHAPE_ONLY` |
| RET-006 | Cleanup candidates keep approval and rollback fields | `PASS_SHAPE_ONLY` |
| RET-007 | Source authority is required for publication claims | `PASS_SHAPE_ONLY` |
| RET-008 | Credential-sensitive rows are review or blocked | `PASS_SHAPE_ONLY` |

## Source Classes

Allowed source classes are durable repo, local generated, official or primary external context, advisory only, user instruction, journey context not canon, and open gap.
