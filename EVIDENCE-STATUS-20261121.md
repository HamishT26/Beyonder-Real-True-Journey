# Evidence status: 21 November 2026

This supplement does not change the verified release payload, CI workflow, or application worksheet.

## What was observed

- A small synthetic archive restore reproduced the expected public and reviewer outputs in a separate Linux scratch workspace. This is fixture evidence, not production deployment or independent adoption.
- A separate bounded Windows smoke command printed two fixed markers. The caller observed both lines, exit code zero, empty standard error and the tracked child closing. This verifies a basic output path only. A prior restore attempt timed out without captured output; the smoke result neither identifies that cause nor establishes a working Windows restore.
- Source-only reviews distinguished historical approval observation from a later effect start. A proposed receipt version may clarify timing without rewriting an old receipt or turning an unknown effect into permission to retry. Missing versions and lossy conversions should remain held. These are design observations, not claims of a new implemented format.

## Reproduction and reviewer guidance

Start with [the existing reproduction instructions](REPRODUCIBILITY.md). Treat the public release checks, the private synthetic fixture observations above and the source-only proposals as distinct evidence. The platform observations are limited maintainer reports; this note supplies no private host details, private records or independent acceptance claims. Hosted CI status is independent of local results; inspect the exact workflow run before reporting hosted verification.

A practical next diagnostic is to compare a tiny synthetic file's expected bytes and hash against a read from the Windows environment, then evaluate restore stages separately. No full-volume test, deployment, provider submission or permission change is claimed.
