# GHC Family Method Flow State

- Phase: v646-gmut-thos-v7-x1-x2
- Owner: Eiren Kestrel
- Methods: 4
- Passing witnesses: 3
- Failed witnesses retained: 4

## Preferred methods

### V6467-M01 — Resolve frozen proposal collection from declared schema keys

- Trigger: inherited JSON index; unknown proposal collection field; PowerShell ConvertFrom-Json; partial output after runtime error
- Method: Inspect and record the frozen-index top-level keys first, then select the declared proposal collection by exact schema field and fail explicitly if it is absent.
- Recurrence guard: Never let a later successful PowerShell expression mask an earlier schema-access error; inspect declared keys and check every native or runtime failure before credit.
- Rollback: Give the partial probe zero novelty-audit credit, retain the null-array error, and rerun only the smallest key-first read-only query.
- Witnesses: V6467-M01-W-F, V6467-M01-W-P

### V6467-M02 — Serialize PowerShell loop results after explicit accumulation

- Trigger: PowerShell foreach loop; structured result objects; JSON serialization; read-only novelty audit
- Method: Accumulate PowerShell loop results in an explicit array and pipe that completed array to ConvertTo-Json after the loop.
- Recurrence guard: PowerShell loops that feed serialization must assign to an explicit results array; parser failures receive no downstream evidence credit.
- Rollback: Retain the parser failure, award zero novelty-search credit, and rerun only the corrected read-only loop.
- Witnesses: V6467-M02-W-F, V6467-M02-W-P

### V6467-M03 — Split login-shell startup from bounded filesystem and compiler probes

- Trigger: Windows PowerShell login shell; large Git worktree; short wrapper deadline; filesystem or compiler inspection
- Method: Disable login-shell initialization for bounded probes, use an already responsive neutral working directory, address the target by absolute path, and separate existence, content, and compilation checks.
- Recurrence guard: Do not retry an identical timed-out login-shell inspection; change one causal dimension, split the probe, and preserve the original timeout as a failed witness.
- Rollback: Award no inspection or compilation credit to either timeout and retain both wrapper expirations before using the bounded recovery.
- Witnesses: V6467-M03-W-F, V6467-M03-W-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
