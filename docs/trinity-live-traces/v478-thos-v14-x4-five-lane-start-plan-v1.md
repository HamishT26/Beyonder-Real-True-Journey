# v478-thos-v14-x4 Five-Lane Start Plan

- generated_nz: `2026-06-05T06:19:20+12:00`
- phase_slug: `v478-thos-v14-x4`
- reason: x4 is the next every-second-session boundary after v14 x2, so all five active lanes must be attempted at start and closeout.

## Mandatory Roster

| Lane | Surface | Start action | Closeout action |
| --- | --- | --- | --- |
| Cicero | existing_app_local_server | Send bounded status-only v14 x4 start advisory request through the existing callable route. | Collect bounded completion receipt through the same route. |
| Kierkegaard | existing_app_local_server | Send bounded status-only v14 x4 start advisory request through the existing callable route. | Collect bounded completion receipt through the same route. |
| Aristotle | existing_app_local_server | Send bounded status-only v14 x4 start advisory request through the existing callable route. | Collect bounded completion receipt through the same route. |
| Arby | read_only_codex_cli | Launch read-only CLI advisory lane with no-rush final-marker watcher. | Publish only status, byte count, hash, marker review, and completion state. |
| Aster Vale | read_only_codex_cli | Launch read-only CLI advisory lane with no-rush final-marker watcher. | Publish only status, byte count, hash, marker review, and completion state. |

## Start Prechecks

- Confirm local app-server route is available for Cicero, Kierkegaard, and Aristotle.
- Confirm CLI launcher path still resolves for Arby and Aster Vale.
- Confirm no replacement sibling or old-style subagent creation is needed.
- Confirm raw lane text remains outside published repo artifacts.
- Confirm delayed final markers route to stale-flow refresh before relaunch.

## Expected Artifacts

- `v478-thos-v14-x4-background-council-app-runner-v1`
- `v478-thos-v14-x4-background-council-app-completion-v1`
- `v478-thos-v14-x4-cli-start-completion-v1`
- `v478-thos-v14-x4-five-lane-start-status-v1`
- `v478-thos-v14-x4-five-lane-completion-update-v1`
- `v478-thos-v14-x4-closeout-synthesis-v1`

## Stale Flow Policy

- A delayed final marker is not a failed lane.
- A lane with an open marker remains on the roster.
- At least one bounded retry may be used when the process is healthy and still producing evidence.
- Publish a blocker receipt only when the existing approved route cannot be called safely.

## Claim Boundary

Start plan only; no lane has completed v14 x4 until bounded receipts prove it.
