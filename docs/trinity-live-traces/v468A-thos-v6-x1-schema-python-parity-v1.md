# v468A THOS v6 x1 Schema Python Parity

Prepared: 2026-06-01T23:55:52.2751923+12:00.

The schema and Python validator align on required fields, phase type, hash shape, drift shape, and THOS boundary values. The schema is stricter on extra fields. The Python validator is stronger on head equality, live Git comparison, artifact path existence, path containment, and forbidden overclaim linting.

Conclusion: use the schema as a contract and the Python validator as the executable guard.
