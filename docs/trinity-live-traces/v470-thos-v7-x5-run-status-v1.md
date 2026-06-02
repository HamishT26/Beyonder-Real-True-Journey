# v470 THOS v7 x5 Run Status

Status: `PASS_SHAPE_ONLY`

Phase start: `2026-06-02T19:21:44+12:00`

## Result

v7 x5 adds `scripts/thos_assertion_manifest_regression.py`, a tempdir-only harness that invokes the real THOS publication guard against synthetic assertion manifest cases. It verifies one positive allow case and eleven expected refusal cases while preserving only a curated summary report.

The publication guard now also supports `--skip-git-drift` for isolated tempdir-only regression harnesses. Normal phase publication checks still run Git drift checks by default.

## Validation Highlights

- Tempdir-only regression harness passed 12 of 12 cases.
- Missing manifest, malformed manifest, path-list mismatch, absolute path, traversal path, missing artifact, expectation mismatch, boundary drift, coverage gap, stray assertion, and duplicate artifact ID cases all denied as expected.
- Temp roots were cleaned up and no synthetic temp fixture was curated.

## Boundary

No connector writes, cleanup authority, remote publication authority, platform safety certification, GMUT validation, or GMUT gate movement occurred.
