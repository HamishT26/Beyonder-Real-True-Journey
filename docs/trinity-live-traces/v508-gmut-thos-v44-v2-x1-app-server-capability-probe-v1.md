# v508-gmut-thos-v44-v2-x1 App-Server Capability Probe

Generated UTC: `2026-06-12T01:34:45Z`

Status: `OPEN_GAP_APP_SERVER_DISCOVERY_SURFACE_NOT_EXPOSED`

## Method Shape Results

- initialize: `timeout`
- thread/list: `timeout`
- threads/list: `error`, class `invalid_params`
- conversation/list: `error`, class `invalid_params`
- conversations/list: `error`, class `invalid_params`
- session/list: `error`, class `invalid_params`
- sessions/list: `error`, class `invalid_params`
- thread/search: `error`, class `missing_required_param`
- threads/search: `error`, class `invalid_params`
- thread/read: `error`, class `missing_required_param`

## Safe Discovery Surface

- discovery method exposed: `false`
- ok discovery methods: `none`
- thread/read requires private id: `true`

## Retry Guidance

No safe discovery surface was exposed by this probe. Restore the private app-lane map in the running process or wait for official thread tools to be exposed.

Forbidden fallbacks: old-style subagent spawn, replacement sibling creation, raw app-state scraping, or private ID publication.

## Boundary

No raw app-server result, raw error text, thread IDs, thread titles, lane text, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.
