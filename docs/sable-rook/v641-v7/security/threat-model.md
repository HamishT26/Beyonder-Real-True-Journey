# V7 bounded threat model

Assets include public evidence integrity, source lineage, claim classification, privacy, reproducible tests, and non-destructive recovery. Trust boundaries separate untrusted source text, generated fixtures, the owned repository, external authorities, live identity infrastructure, and public artifacts.

The tested threats are encoding ambiguity, Unicode confusables, normalization drift, raw task identifiers, private path or route leakage, credential-shaped strings, poisoned provenance edges, draft-as-stable substitution, outcome leakage, destructive recovery directions, and unsupported claim promotion.

Controls are explicit source-status pins, type/category checks, in-memory negative fixtures, output exclusion, deterministic validators, clean snapshots, retained negatives, and exact authority gates. Recovery quarantines the affected output, restores the last clean owned snapshot, lowers the claim, and requires fresh evidence. It never authorizes host-security weakening, privilege expansion, destructive Git, secret handling, deployment, or external account changes.

This is a bounded threat model and negative-test suite. It is not exhaustive security, penetration testing, production assurance, or proof that unknown attack classes are absent.
