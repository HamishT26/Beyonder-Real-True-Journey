# v468A THOS v5 x1 Validator Upgrade

Prepared: 2026-06-01T23:46:12.1314922+12:00.

The THOS phase-manifest validator now supports optional `--repo-root`, `--check-artifacts`, `--check-live-git`, `--upstream-ref`, and `--report-json` flags.

The new checks harden the validator from static manifest review toward live execution readiness while still avoiding staging, pushing, Drive mutation, cleanup, or GMUT validation claims.
