# Eiren Kestrel v663-v8 owner-delta threat model

## Overview

This model covers only Eiren's additive v663-v8 owner delta. It does not claim
repository-wide coverage, production assurance, exhaustive security, complete
privacy, complete accessibility, independent reproduction, or authority.

## Threat Model, Trust Boundaries, and Assumptions

Protected assets are the immutable Caelen source, x1 separation, proposal and
gate truth, owner-delta manifests, synthetic fixtures, failure retention,
privacy boundaries, and the one-shot canonical receipt. Trust boundaries exist
between the live activation and committed source, Git objects and sparse
checkout, x1 and x2, synthetic fixtures and real-world authority, local and
remote refs, and terminal route lookup and one acknowledged send. JSON, free
text, paths, refs, source versions, and future registry payloads are untrusted.

## Attack Surface, Mitigations, and Attacker Stories

- A malformed fixture may claim real rows or authority. Common root checks and
  eighty mutations fail closed.
- A graph may contain duplicate nodes, orphan edges, invalid sequences, or
  nonfinite coordinates. Typed validators reject each class.
- A report may use colour alone or omit structure. The contract requires
  landmarks and redundant noncolour state while reserving human evaluation.
- A source URL may be treated as proof. The ledger records vocabulary-only use,
  zero ingestion, and zero authority.
- A path may hide a collision or private material. Literal allowlists, NFC and
  case-fold review, index-blob hashes, and five-class scans fail closed.
- A success may be replayed to launder evidence. The final contract permits one
  successful canonical invocation and records post-success replay as false.
- A successor may be substituted or contacted early. Routing remains disabled
  until exact final, newest authority, exact-title uniqueness, reread, and
  acknowledgement all pass.

## Severity Calibration

Any route substitution, private-material disclosure, source/x1 rewrite, false
authority claim, or evidence promotion is critical and stops the phase. Manifest
or test mismatch is high and blocks sealing. Structural documentation defects
are medium until corrected. Cosmetic owner-local wording defects are low only
when they do not change a claim, gate, count, hash, or route.

Residual risks remain: incomplete human accessibility evaluation, incomplete
privacy and security review, dependency and host assumptions, no independent
team reproduction, no real practitioners or assets, and no legal, cultural,
affected-party, or Māori-authority decision.
