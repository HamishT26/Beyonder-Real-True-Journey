# v468A THOS v2 x1 Phase Manifest Schema

Prepared: 2026-06-01T23:16:00+12:00.

This fixture defines the minimum fields for future THOS phase manifests: phase, domain, x-pass, NZ start time, baseline commit, claim locks, mutation class, source class, and next phase.

The important behavior is that mutation class must be explicit. A phase can plan connector or destructive work, but it cannot quietly perform it. The manifest also carries the inherited GMUT locks: all six gates remain `OPEN_NOT_TESTED`, `B_Psi` remains quarantined or demoted, `V(Psi)` remains symbolic only, and Journey/Solas context remains non-canon.
