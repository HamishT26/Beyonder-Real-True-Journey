# GHC Family workflow plan schema

## Request

The runner accepts UTF-8 JSON with this top-level shape:

```json
{
  "schema": "ghc.family.workflow-plan.request.v1",
  "plan_id": "sanitized-stable-label",
  "owner": "Relational owner name",
  "identity_boundary": "Relational working language only; no continuity or authority claim.",
  "route": {
    "cycle_order": ["Seat A", "Seat B"],
    "phase_assignments": [
      {"phase": "v649-v7", "seat": "Seat A"},
      {"phase": "v649-v8", "seat": "Seat B"}
    ],
    "normalization": {
      "start_phase": "v649-v7",
      "start_seat": "Seat A",
      "entry_count": 2
    },
    "future_identity_placeholders": []
  },
  "requirements": {
    "core_proposal_minimum": 20,
    "safe_candidate_task_cap": 1000,
    "skill_minimum": 10,
    "runner_minimum": 10,
    "document_word_cap": 100000,
    "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": true},
    "commit_cap": {"x1": 3, "x2": 3, "total": 6},
    "validation": {
      "canonical_pass_minimum": 1,
      "replay_policy": "skip_when_first_passes",
      "isolate_failures_before_broader_rerun": true,
      "privacy_scan_required": true,
      "manifest_required": true,
      "remote_equality_required": true
    },
    "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
    "messaging": {
      "codex_route": "existing_task_only_after_terminal_gate",
      "cross_platform": "user_mediated_file_relay_only"
    },
    "environment": {"windows_sandbox_hyper_v": "deferred"},
    "closeout": {"all_authorized_safe_candidate_prototypes_resolved": true}
  },
  "truth": {
    "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
    "independent_reproduction_claimed": false,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "protected_boundaries": ["empirical", "participant", "legal", "cultural", "production"]
  },
  "observed_failures": []
}
```

Unknown fields are preserved in the candidate request. Required fields fail closed when absent or malformed.

Live plans may choose any document cap from 1 through 100,000 words, a file-backed baton range whose minimum is at least 8,000 and maximum is at most 100,000 words, and commit caps no greater than six x1, six x2, and twelve total commits. These are ceilings, not completion quotas. A one-off special continuation may use the twelve-commit ceiling while ordinary phases declare a smaller cap such as three x1, three x2, and six total.

## Phase labels

The machine-readable phase label is `vN-vS`, where `N` is a positive integer and `S` is 1 through 8. Sequential normalization increments `S`; after `vN-v8`, it continues at `v(N+1)-v1`.

The declared `cycle_order` is rotated so `start_seat` owns `start_phase`. The runner emits `entry_count` sequential candidate assignments. The candidate is advisory whenever it differs from submitted ownership or numbering.

## Issue fields

Every issue contains:

- `issue_id`: deterministic sequence within one audit;
- `severity`: `error`, `warning`, or `info`;
- `code`: stable machine label;
- `truth_label`: normally `open_gap` or `exact_gate` for unresolved items;
- `message`: sanitized explanation;
- `recovery`: smallest safe next action;
- `protected_gates`: non-empty list.

Errors make the audit exit `2`. Warnings do not fail structural validation but remain visible.

## Output truth

`workflow-plan-refinement.json` reports:

- the submitted route assignments;
- the candidate sequential route;
- whether confirmation is required;
- policy checks;
- issue counts;
- a sanitized candidate request;
- a boundary statement.

`valid: true` means only that the sanitized plan is structurally consistent with its declared rules. It is not phase activation, scientific validation, permission to mutate, or proof of delivery.

## Privacy exclusions

Request and output artifacts must exclude raw task/thread identifiers, URI-like private routes, credentials, secrets, transcripts, screenshots, session streams, private callable identifiers, private app state, private absolute local paths, and real protected participant or beneficiary data. The output directory may be local, but its absolute value is never copied into generated artifacts.

## Failure and witness handling

When the runner exits `2`, keep the emitted issue artifacts and record a Method Flow fail witness before retrying. Rerun the smallest corrected request. A later pass does not erase the original issue, failed invocation, or negative. Same-owner validation is not independent reproduction.
