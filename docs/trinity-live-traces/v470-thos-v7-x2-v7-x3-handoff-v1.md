# v470 THOS v7 x2 to v7 x3 Handoff

Next expected phase: `v470_THOS_v7_x3`

## Carry Forward

- Decide whether assertion reports should become mandatory inside `scripts/thos_publication_guard.py`.
- Add curated duplicate canonical, malformed visualization, tuple mismatch, and digest mismatch assertion fixtures.
- Keep renderer migration blocked until report assertions remain green.
- Keep all connector writes and destructive cleanup unperformed without explicit named-target approval.
- Keep all six GMUT gates open.

## Boundary

v7 x2 is THOS local assertion hardening only. It does not certify platform safety, authorize connector writes, validate GMUT, or move any GMUT gate.
