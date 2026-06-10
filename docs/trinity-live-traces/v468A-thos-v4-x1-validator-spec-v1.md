# v468A THOS v4 x1 Validator Spec

Prepared: 2026-06-01T23:34:16.7258617+12:00.

`scripts/validate_thos_phase_manifest.py` is a dry-run local checker for THOS phase manifests. It checks required fields, phase type, live head format and equality, drift, required lists, GMUT boundary text, remote-equality validation, THOS boundary state, and forbidden overclaim phrases.

The checker is intentionally narrow. It does not stage, commit, push, mutate Drive, delete files, or replace future JSON Schema validation.
