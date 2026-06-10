# v470 THOS v3 x2 Command and Connector Hygiene Ledger

Phase: `v470_THOS_v3_x2`

## Command Classes

| Class | Examples | Approval |
| --- | --- | --- |
| Read-only | `git status`, `git rev-parse`, `git ls-remote`, file inventory, JSON parse checks. | Allowed under packet. |
| Curated safe-write | Current-phase artifact writes, explicit current-phase `git add`, commit, explicit push to shared omega ref. | Allowed after guards. |
| Approval-required | Drive upload/import, GitHub connector mutation, cloud deployment, paid API call, TeX Live managed full install, supervisor background process. | Requires separate scoped action packet if cost or mutation is uncertain. |
| Forbidden without separate targeted approval | Delete worktrees, bulk Drive cleanup, `git reset --hard`, `git clean`, force push, raw log/session JSONL/screenshot/credential staging. | Not approved in this phase. |

## Connector Boundaries

- NVIDIA plugin was not callable in this context, so NVIDIA is official-web-source context only.
- GitHub connector was not used for repo mutation; Git CLI handles curated publication.
- Google Drive was not mutated.
- Computer and Chrome were not used because no UI automation was required.
- Documents, Presentations, and Spreadsheets were not used for external publication.

## Hygiene Recommendations

- Class every command before execution.
- Name `cwd` and current phase before write commands.
- Keep destructive cleanup separate from cleanup-candidate reporting.
- Do not confuse connector availability with connector write approval.
- Treat generated checker reports as evidence only for the exact checks they run.
