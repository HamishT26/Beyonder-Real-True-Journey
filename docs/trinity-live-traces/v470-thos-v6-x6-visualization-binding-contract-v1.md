# v470 THOS v6 x6 Visualization Binding Contract

Phase: `v470_THOS_v6_x6`
Created NZ: `2026-06-02T17:13:52+12:00`

## Contract

Visualization data must project from canonical rows. It must not invent or define its own row universe. Each visualization row should carry enough identity to bind back to the active row-universe receipt: `row_id`, `family`, `status`, `surface`, `source_row_id`, `row_identity_digest`, and `row_content_digest`.

Rejected rows can be counted for operator awareness, but they must not be projected as canonical visualization rows.

## Open Gap

The earlier v6 x2 HTML still embeds row data. v6 x6 records the binding contract and externalized JSON requirement, but it does not rewrite that renderer. v6 x7 should either move the renderer onto external JSON or add executable orphan and multi-bind checks around the projection.

## Boundary

Visualization binding is local report-shaping infrastructure. It is not external dashboard authority, governance certification, safety proof, or GMUT validation.
