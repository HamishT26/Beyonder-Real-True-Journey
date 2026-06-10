# v470 THOS v4 x2 Checker Fixture Plan

Phase: `v470_THOS_v4_x2`

Fixture policy: document expected failures without staging forbidden raw material.

| Fixture | Simulated Input | Expected |
| --- | --- | --- |
| `outside_allowlist` | Current phase plus unrelated staged file. | `FAIL_BLOCKER staged_allowlist` |
| `raw_session_jsonl_path` | Path contains a session JSONL marker. | `FAIL_BLOCKER path_guard` |
| `screenshot_path` | Path contains a screenshot marker. | `FAIL_BLOCKER path_guard` |
| `secret_like_content` | Synthetic fake key pattern using fake placeholder only. | `FAIL_BLOCKER credential_guard` |
| `overclaim_assertion` | Redacted prohibited GMUT-overclaim token. | `FAIL_BLOCKER forbidden_claim_guard` |
| `generic_pass_status` | Row status is `PASS` instead of `PASS_SHAPE_ONLY`. | `FAIL_BLOCKER status_enum` |
| `trailing_whitespace` | Artifact line has trailing space. | `FAIL_BLOCKER trailing_whitespace` |
| `unreadable_git_drift` | Checker run outside git repo or without upstream. | `OPEN_GAP git_drift` |

## Next Step

Materialize synthetic fixtures in a tempdir or current-phase docs only. Do not stage raw forbidden material.
