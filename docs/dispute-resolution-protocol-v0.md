# Freed ID Dispute + Recourse Protocol v0 (GOV-004)

Purpose: define a minimal, auditable dispute workflow for credential actions so
recourse can be executed and verified reproducibly.

Status: implementation scaffold (v0).

---

## 1) Scope

This protocol covers disputes tied to a credential action in the Freed ID
registry, including issuance, revocation impacts, and presentation claims.

Each dispute must include:
- `case_id` (stable identifier),
- `subject_did`,
- `credential_id`,
- `reason`,
- status lifecycle history with timestamped transitions.

---

## 2) Lifecycle states

Primary states:
- `opened` — dispute created and acknowledged.
- `review` — case is being evaluated.
- `escalated` — additional authority/review tier requested.
- `resolved` — remediation decision completed.
- `dismissed` — case closed without remediation.
- `reopened` — recourse path invoked after `resolved`/`dismissed`.

Allowed transitions (v0):
- `opened -> review | dismissed`
- `review -> resolved | dismissed | escalated`
- `escalated -> review | resolved`
- `resolved -> reopened`
- `dismissed -> reopened`
- `reopened -> review`

Any transition not listed above is invalid and must be rejected by the workflow.

---

## 3) Recourse guarantees (v0 policy)

1. Every dispute receives a `case_id` and immutable transition history entries.
2. At least one reopen path exists from terminal outcomes (`resolved`/`dismissed`)
   to avoid irreversible dead ends.
3. Every transition records:
   - actor,
   - from/to status,
   - timestamp (`at_utc`),
   - note and optional evidence references.
4. Workflow checks must be replayable by automation, not narrative-only claims.

---

## 4) Data contract

Canonical schema artifact:
- `docs/freed-id-dispute-case-schema-v0.json`

Implementation scaffold:
- `freed_id_dispute_recourse.py`

Verification scaffold:
- `freed_id_dispute_recourse_verifier.py`

Verifier outputs:
- timestamped: `docs/heart-track-runs/*-freedid-dispute-recourse-check.{json,md}`
- latest: `docs/heart-track-dispute-recourse-latest.{json,md}`

---

## 5) Known gaps for v1

- Bind dispute transitions to signature/authorization checks (GOV-001 linkage).
- Add explicit SLA timers for acknowledgement and resolution windows.
- Add adversarial tests for replay, ordering, and tamper attempts.
