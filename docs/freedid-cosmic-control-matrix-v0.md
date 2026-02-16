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
| GOV-002 | Privacy by design (`freed_id_spec.md`) | Credential presentations must support minimum-disclosure behavior. | implemented | Added v0 policy scaffold (`docs/freedid-minimum-disclosure-policy-v0.md`) and reproducible verifier (`freed_id_min_disclosure_verifier.py`) with latest artifacts in `docs/heart-track-min-disclosure-latest.{json,md}` and timestamped run outputs under `docs/heart-track-runs/*-freedid-min-disclosure-check.{json,md}`. | Run `python3 freed_id_min_disclosure_verifier.py` and require PASS for required/forbidden/extra-field checks plus commitment binding. | Aster + Lumen | Promote to verified after integrating policy checks into live credential presentation flow (non-fixture path). |
| GOV-003 | Transparency and auditability (`freed_id_spec.md`, `Cosmic_bill_of_rights.md`) | Identity and governance actions must emit append-only audit records. | verified | Append-only audit ledger support now exists (`freed_id_audit_log.py`) and registry actions emit chained events (`Freed_id_registry.py` with `audit_ledger_path`). PASS artifacts: `docs/heart-track-auditability-latest.{json,md}` and timestamped `docs/heart-track-runs/*-freedid-auditability-check.{json,md}`. | Run `python3 freed_id_auditability_verifier.py` and require PASS for ledger existence, action sequence, and hash-chain integrity checks. | Aster + Lumen | Convert verifier checks into pytest suite once test harness standardization lands. |
| GOV-004 | Right to recourse (`Cosmic_bill_of_rights.md`) | Disputed credential actions must be tracked with case IDs and status transitions. | draft | Dispute resolution is described conceptually; no case workflow artifact exists. | Introduce dispute-case schema and lifecycle states (`opened`, `review`, `resolved`). | Human + Aster | Add `docs/dispute-resolution-protocol-v0.md` and case template. |
| GOV-005 | Right to safety/security (`Cosmic_bill_of_rights.md`) | Registry operations must reject revoked identities for privileged actions. | verified | `Freed_id_registry.py` blocks credential actions when DID is revoked; `freed_id_control_verifier.py` produced passing artifacts in `docs/heart-track-governance-latest.{json,md}` and `docs/heart-track-runs/20260213T123852Z-freedid-gov-check.{json,md}`. | Run `python3 freed_id_control_verifier.py` and require PASS across all checks. | Aster | Add pytest conversion for the same checks once a full test harness is standardized. |
| GOV-006 | Interoperability (`freed_id_spec.md`) | DID documents should conform to W3C DID Core field structure. | specified | `DIDDocument.to_dict()` includes DID context/id/controller/verification/service fields. | Validate generated documents against minimal DID Core schema contract. | Aster | Add schema validation utility and sample pass/fail fixtures. |
| GOV-007 | Accountability and responsible innovation (`Cosmic_bill_of_rights.md`) | Every governance control must map to an owner and measurable review cadence. | implemented | This control matrix assigns owners and next actions. | Run weekly maturity review; no control can stay `draft` > 2 review cycles without recorded reason. | Aster + Human Council | Add review log template and first dated review entry. |

---

## Current maturity snapshot

- `draft`: 1 control (GOV-004)
- `specified`: 2 controls (GOV-001, GOV-006)
- `implemented`: 2 controls (GOV-002, GOV-007)
- `verified`: 2 controls (GOV-003, GOV-005)

Interpretation: Heart track now has two verification-grade controls and one implemented privacy control; next gap is promoting GOV-002 from implemented to verified in non-fixture integration.

---

## Promotion rule (anti-hallucination guardrail)

A control can only move upward in maturity when one of the following is added in-repo:
1. code artifact enforcing the control,
2. automated check/test output proving behavior,
3. dated review evidence with reproducible validation steps.

No maturity upgrade should be done by narrative assertion alone.
