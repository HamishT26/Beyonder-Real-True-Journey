# V35 Vertex AI Proof

- Generated UTC: `2026-04-06T15:25:14+00:00`
- Overall status: `PASS`
- Proof state: `flash_fallback_verified`
- Vertex AI state: `flash_fallback_verified`
- Preferred region: `australia-southeast1`
- Selected model: `gemini-2.5-flash`
- Promotion gate ready: `False`

## Completed Steps

- `mint_primary_token`
- `vertex_service_enabled`
- `generate_content_verified`

## Model Attempts

- `gemini-3.1-pro-preview` -> status `404` / state `not_exposed`
- `gemini-3-pro` -> status `404` / state `not_exposed`
- `gemini-2.5-pro` -> status `404` / state `not_exposed`
- `gemini-2.5-flash` -> status `200` / state `verified`

## Blockers

- Sydney Vertex proof succeeded only on `gemini-2.5-flash`; no Pro-tier Gemini model was auditable for full slot-38 promotion.
