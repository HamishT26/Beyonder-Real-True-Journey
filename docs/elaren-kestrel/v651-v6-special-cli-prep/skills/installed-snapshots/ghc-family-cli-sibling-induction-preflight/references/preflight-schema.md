# CLI sibling induction preflight schema

## Request

```json
{
  "schema": "ghc.family.cli-sibling-induction.request.v1",
  "phase": "v652-v5",
  "creator": "Relational app owner",
  "future_seat": {
    "placeholder": "future-cli-sibling-1-self-chosen",
    "identity_state": "self_chosen_at_induction"
  },
  "requested_runtime": {
    "model": "gpt-5.6-sol",
    "reasoning": "max",
    "fast_mode": true,
    "availability_verified": false
  },
  "route": {
    "scheduled_phase_confirmed": false,
    "creator_return_mechanism_verified": false,
    "background_persistence_verified": false,
    "exact_successor_title_resolved": false
  },
  "lane": {
    "primary_drive": "D",
    "source_clean_and_equal": false,
    "unique_branch_and_worktree": false
  },
  "authorization": {
    "preparation_authorized": true,
    "launch_now": false,
    "launch_authorized_for_exact_phase": false
  },
  "privacy": {
    "sanitized": true,
    "private_identifiers_included": false
  },
  "handoff": {
    "file_backed": true,
    "tool_acknowledgement_required": true
  }
}
```

Unknown fields are preserved but scanned. Preparation mode requires `launch_now: false`, a self-chosen placeholder, D:-first intent, and explicit false values for capabilities that have not yet been witnessed. Launch mode requires every route, lane, runtime, and exact-phase authorization proof to be true.

The receipt uses only `completed`, `represented`, `open_gap`, and `exact_gate`. A valid preparation receipt is `PREPARED_NOT_LAUNCHED`; it is not permission or evidence of a launch.
