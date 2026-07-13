# Bounded v642-v1 threat model

## Scope

The scope is the Nima-owned phase artifact pipeline: structured JSON and Markdown inputs, deterministic builders, validators, hash manifests, static report generation, privacy scanning, and non-destructive clean-snapshot replay. It excludes production services, live credentials, user accounts, networks, sibling branches, host configuration, and deployment.

## Assets and trust boundaries

Assets are source lineage, x1 freeze integrity, retained negatives, claim classifications, official-source status labels, phase-scoped files, validator decisions, hash commitments, and remote equality receipts. Inputs are treated as untrusted until schema, size, depth, count, path, provenance, and privacy checks pass. Authority-bearing legal, cultural, identity, deployment, proof, and private decisions never cross into the technical trust domain.

## Bounded threats

The safe battery represents excessive decompression ratio, oversized declared expansion, nesting depth, object and key counts, duplicate-key ambiguity, oversized tokens, recursion, time or memory budgets, context laundering, raw task or thread identifiers, credential shapes, unsafe paths, and evidence-destroying recovery order. No dangerous payload is materialized. No privilege is expanded.

## Controls and recovery

Controls apply before consumption: strict ceilings, duplicate-key rejection, owned-path restriction, no link traversal, content hashes, retained vectors, phase privacy scans, and clean detached replay. Recovery stops processing, preserves the exact negative, quarantines only owned outputs, restores a clean owned snapshot, tightens the smallest relevant control, and reruns without elevation, destructive cleanup, host-security weakening, or reboot.

## Claim ceiling

Passing these fixtures is bounded defensive evidence only. It is not exhaustive security, penetration testing, cryptographic assurance, production hardening, deployment readiness, or a guarantee that unknown encodings and attacks cannot exist.
