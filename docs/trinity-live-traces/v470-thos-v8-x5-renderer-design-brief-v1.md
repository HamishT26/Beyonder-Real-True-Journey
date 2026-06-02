# v470 THOS v8 x5 Renderer Design Brief

Phase: `v470_THOS_v8_x5`

## Visualization Route

Analytical job: monitoring and guard reconciliation.

Artifact family: static local HTML dashboard table.

Primary route: use the Build Web Data Visualization router's lowest-risk path: a simple, truthful, directly labeled dashboard. The rendered artifact must make case ID, row status, guard status, guard decision, dominant reason, and required-code parity visible without hover.

Fallback route: plain JSON and Markdown artifact review remains authoritative if the HTML artifact is unavailable.

## Contract

The renderer consumes `docs/trinity-live-traces/v470-thos-v8-x4-renderer-preflight-v1.json`, specifically `renderer_rows`.

The local HTML artifact must preserve row count parity with the preflight, expose required labels, avoid forbidden claim wording, avoid credential-shaped content, and carry no connector/cloud/destructive operation.

## Boundary

This phase creates a local rendered artifact proof. It does not claim a final UI, production dashboard, connector write, cloud write, destructive cleanup result, publication authority change, GMUT validation, or GMUT gate closure.
