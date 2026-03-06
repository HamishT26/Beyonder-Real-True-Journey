# Trinity API Source Manifest Validation

- generated_utc: `2026-03-06T12:53:31+00:00`
- overall_status: **PASS**
- manifest_path: `docs/trinity-api-source-manifest-v1.json`
- query_pack_path: `docs/trinity-api-query-pack-v1.json`
- api_count: `7`

## Checks
| check | status | detail |
|---|---|---|
| manifest_header | PASS | ok |
| api_schema | PASS | ok |
| query_pack | PASS | ok |
| cache_target_coverage | PASS | ok |

## API roster
| api_id | pillar | cache_artifact | refresh_script | enabled_by_default |
|---|---|---|---|---|
| arxiv | mind | `docs/trinity-api-cache/mind-signals-latest.json` | `scripts/mind_theory_signal_refresh.py` | `False` |
| openalex | mind | `docs/trinity-api-cache/mind-signals-latest.json` | `scripts/mind_theory_signal_refresh.py` | `False` |
| crossref | body | `docs/trinity-api-cache/body-signals-latest.json` | `scripts/body_compute_signal_refresh.py` | `False` |
| github | body | `docs/trinity-api-cache/body-signals-latest.json` | `scripts/body_compute_signal_refresh.py` | `False` |
| worldbank | heart | `docs/trinity-api-cache/heart-signals-latest.json` | `scripts/heart_governance_signal_refresh.py` | `False` |
| oecd | heart | `docs/trinity-api-cache/heart-signals-latest.json` | `scripts/heart_governance_signal_refresh.py` | `False` |
| data_govt_nz | heart | `docs/trinity-api-cache/heart-signals-latest.json` | `scripts/heart_governance_signal_refresh.py` | `False` |
