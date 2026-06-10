# v470 THOS v6 x4 Corrupt-Byte Rehearsal

This artifact records a tempdir-only corruption rehearsal. A copied artifact was modified outside the repo, the copied manifest still held the original checksum, and `scripts/thos_phase_manifest.py --verify-manifest` failed closed.

## Result

- Expected status: `FAIL_BLOCKER`.
- Actual status: `FAIL_BLOCKER`.
- Exit code: `1`.
- Failure code: `checksum_mismatch`.
- Curated repo mutation: `false`.
- Connector write: `false`.

## Boundary

The temp path is intentionally not preserved in the curated artifact. This is integrity-routing evidence only; it is not a safety proof or GMUT validation.
