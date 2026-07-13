# Bounded v642-v2 threat model

## Scope

The scope is the Tamar-owned phase artifact pipeline: strict JSON and Markdown inputs, deterministic family builders, validators, normalized manifests, static report generation, privacy and raw-ID scanning, and non-destructive clean detached replay. Production services, live accounts, credentials, private data, networks, sibling branches, host configuration, deployment, and authority-bearing decisions are excluded.

## Threats and controls

Inputs are untrusted until duplicate-key, numeric-domain, Unicode-normalization, confusable-control, size, depth, object-count, path, provenance, and privacy checks pass. Parser disagreement fails closed. Absolute local paths, raw task or thread identifiers, private routes, transcripts, screenshots, credentials, and private app state are prohibited in public artifacts. Legal, cultural, Māori, identity, deployment, proof, private, destructive, shared-branch, and sibling-merge decisions never cross into the technical trust domain.

## Recovery and claim boundary

Recovery stops consumption, retains the vector, quarantines only owned output, restores a clean owned snapshot, tightens the smallest relevant bound, and reruns without elevation, destructive cleanup, host-security weakening, feature enablement, or reboot. This bounded battery is not exhaustive security, penetration testing, production hardening, deployment readiness, or proof that every novel secret encoding is impossible.
