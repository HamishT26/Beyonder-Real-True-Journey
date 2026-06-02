# v470 THOS v4 x2 Plugin Refusal Matrix

Phase: `v470_THOS_v4_x2`

Default posture: read or inventory first; mutation requires named target and clear cost.

| Surface | Allowed Now | Refuse Without New Scope | Reason |
| --- | --- | --- | --- |
| Google Drive | Search/read metadata and content excerpts when relevant. | Create, import, batchUpdate, share, permission edit, delete, bulk move. | Drive writes persist externally and can expose private Journey or THOS content. |
| NVIDIA AI-Q/NIM/Dynamo | Read local skills and official docs. | Backend research call, deploy, Kubernetes change, NGC/NIM credential use, GPU job. | May spend resources, need credentials, or mutate infrastructure. |
| GitHub connector | Read/review metadata where needed. | Issue/PR/comment mutation, secret scanning config, SARIF upload, attestation workflow edits outside curated repo patch. | GitHub writes are public or durable project mutations. |
| Computer/Chrome | View or inspect when UI proof is necessary. | Automation changes, credential entry, app settings changes, destructive UI actions. | Desktop actions can have broad machine effects. |
| Documents/Presentations/Spreadsheets | Local artifact design and read-only route planning. | Native Google Doc/Slide/Sheet creation or content update. | External document writes require a named target and sharing/retention decision. |
| Google Calendar/Gmail | None unless scheduling or email task is explicit. | Create/update events, drafts, labels, sends, forwards. | Communication and scheduling mutations need explicit human intent. |

## Global Stop Rules

- Stop if cost is uncertain.
- Stop if target file, repo, document, calendar, or infrastructure is ambiguous.
- Stop if private, raw, or secret material would leave the local repo.
- Stop if action would create durable external state.
- Stop if action would make a public claim stronger than local evidence supports.
