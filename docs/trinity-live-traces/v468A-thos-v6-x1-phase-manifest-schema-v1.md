# v468A THOS v6 x1 Phase Manifest Schema

Prepared: 2026-06-01T23:55:52.2751923+12:00.

This artifact drafts a JSON Schema 2020-12 contract for THOS phase manifests. It captures the fields already enforced by `scripts/validate_thos_phase_manifest.py`: phase id, phase type, start time, live heads, drift, artifact list, blocked actions, validation chain, and THOS-to-GMUT boundary.

The schema is a contract draft, not the executable guard. The Python validator remains the current executable local guard.
