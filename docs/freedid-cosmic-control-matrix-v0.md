# Freed ID + Cosmic Bill Control Matrix v0 (Heart Track)

Purpose: convert governance principles into auditable controls with explicit maturity and next verification steps.

Maturity scale:
- `draft` = principle is written, control wording incomplete.
- `specified` = control text exists with measurable criteria.
- `implemented` = at least one working artifact enforces part of the control.
- `verified` = implementation evidence and repeatable checks are present.

---

## Control matrix

| control_id | principle_anchor | control_statement | maturity | evidence_now | verification_test | gap_owner | next_action |
|---|---|---|---|---|---|---|---|
| GOV-001 | Self-sovereignty (`freed_id_spec.md`) | DID holders can create and manage identifiers without central unilateral override. | specified | Method flow is documented in DID method section; in-memory registry supports create/update/revoke paths. | Add unit tests proving only controller-signed updates are accepted (stub signatures acceptable in v0). | Aster | Add signature-check interface in registry and negative tests. |
| GOV-002 | Privacy by design (`freed_id_spec.md`) | Credential presentations must support minimum-disclosure behavior. | draft | Selective disclosure intent is documented; no implementation exists in current code. | Add presentation schema with redaction/selective-field policy and test fixtures. | Aster | Define `presentation_policy.md` and sample credential presentation payloads. |
| GOV-003 | Transparency and auditability (`freed_id_spec.md`, `Cosmic_bill_of_rights.md`) | Identity and governance actions must emit append-only audit records. | specified | Documentation requires append-only logs; current registry is in-memory only, no audit ledger persisted. | Implement local append-only JSONL audit log and verify immutability expectations in checks. | Aster | Add `freed_id_audit_log.py` with append-only writer and integrity hash chain. |
| GOV-004 | Right to recourse (`Cosmic_bill_of_rights.md`) | Disputed credential actions must be tracked with case IDs and status transitions. | draft | Dispute resolution is described conceptually; no case workflow artifact exists. | Introduce dispute-case schema and lifecycle states (`opened`, `review`, `resolved`). | Human + Aster | Add `docs/dispute-resolution-protocol-v0.md` and case template. |
| GOV-005 | Right to safety/security (`Cosmic_bill_of_rights.md`) | Registry operations must reject revoked identities for privileged actions. | implemented | `Freed_id_registry.py` blocks credential actions when DID is revoked. | Add automated tests for revoke-and-retry denial behavior. | Aster | Create `tests/test_freed_id_revocation.py` in future test harness cycle. |
| GOV-006 | Interoperability (`freed_id_spec.md`) | DID documents should conform to W3C DID Core field structure. | specified | `DIDDocument.to_dict()` includes DID context/id/controller/verification/service fields. | Validate generated documents against minimal DID Core schema contract. | Aster | Add schema validation utility and sample pass/fail fixtures. |
| GOV-007 | Accountability and responsible innovation (`Cosmic_bill_of_rights.md`) | Every governance control must map to an owner and measurable review cadence. | implemented | This control matrix assigns owners and next actions. | Run weekly maturity review; no control can stay `draft` > 2 review cycles without recorded reason. | Aster + Human Council | Add review log template and first dated review entry. |

---

## Current maturity snapshot

- `draft`: 2 controls (GOV-002, GOV-004)
- `specified`: 3 controls (GOV-001, GOV-003, GOV-006)
- `implemented`: 2 controls (GOV-005, GOV-007)
- `verified`: 0 controls

Interpretation: the Heart track now has a measurable control structure, but verification-grade enforcement remains the main gap.

---

## Promotion rule (anti-hallucination guardrail)

A control can only move upward in maturity when one of the following is added in-repo:
1. code artifact enforcing the control,
2. automated check/test output proving behavior,
3. dated review evidence with reproducible validation steps.

No maturity upgrade should be done by narrative assertion alone.
