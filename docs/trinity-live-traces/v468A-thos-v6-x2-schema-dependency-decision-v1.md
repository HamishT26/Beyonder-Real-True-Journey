# v468A THOS v6 x2 Schema Dependency Decision

Local probe found `jsonschema=4.26.0`, `referencing=0.37.0`, and `jsonschema-specifications=2025.9.1`.

Decision: use the existing optional dependency for local fixture evidence only. Do not vendor a validator, install a package, alter a lockfile, or replace the project-specific Python publication validator.

Reason: JSON Schema can express the base THOS manifest shape, but the Python validator still owns live git equality, artifact-path existence, repo-root escape defense, remote publication checks, and forbidden-claim rules.
