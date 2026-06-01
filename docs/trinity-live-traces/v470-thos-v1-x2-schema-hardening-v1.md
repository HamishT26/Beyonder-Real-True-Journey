# v470 THOS v1 x2 Schema Hardening

Classification: `evidence`

The x2 schema rule is deliberately conservative: a THOS row can pass shape, fail as a blocker, or remain an open gap. It cannot pass runtime execution by implication.

## Status Values

| Status | Meaning |
| --- | --- |
| `PASS_SHAPE_ONLY` | Structurally complete and inside the allowed policy. It proves no runtime behavior. |
| `FAIL_BLOCKER` | Contains forbidden mutation, destructive action, credential exposure, unapproved git action, connector write, or overclaim. |
| `OPEN_GAP` | Incomplete, ambiguous, unknown, or lacking source authority. |

## Schema Families

| Schema | Required field idea |
| --- | --- |
| Command surface | id, pattern, class, mutation level, approval, advisory allowance, blocker, source authority |
| Plugin/MCP/skill boundary | id, type, capability, credential surface, network effect, policy, approval, authority |
| Cleanup candidate | id, target, class, reason, risk, approval, rollback, retention |
| Retention row | artifact, phase, type, retention class, source authority, credential flag, publishability, quarantine reason |
| THOS check result | check id, predicate, target, status, severity, evidence, blocked claims, GMUT gate effect |

## Fail Conditions

Rows fail closed if they allow destructive action, connector writes, raw-material publication, credential exposure, uncurated advisory promotion, THOS-to-GMUT validation import, or any GMUT gate effect other than `none_open_not_tested`.
