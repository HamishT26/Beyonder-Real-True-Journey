# 09 Three package additions

Exactly three direct additions were installed from hash-verified wheels into a new isolated D environment: canonicaljson 2.0.0, frozendict 2.4.7, and cbor2 6.1.4. The environment contains exactly 3 distributions. Installation was offline from the frozen wheelhouse, dependency-free, hash-required, and did not change system Python, PATH, the npm prefix, plugin caches, Windows features, host security, accounts, credentials, or another owner environment.

All 3 positive smokes and 3 adverse smokes passed in the final composite. The initial aggregate receives zero success credit because its CBOR adverse byte decoded as a sentinel; only the corrected malformed-byte dependency was rerun. The dated OSV status is `COMPLETED_BOUNDED_SNAPSHOT` with 0 findings. That snapshot is not exhaustive security or future safety. Rollback selects retained tooling and preserves the environment and receipts without deletion.
