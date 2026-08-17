# THOS owner-delta assurance comparison

## Scope and posture

This v662-v3-3-midnight-remaster research note treats THOS Body as a software-architecture and
workflow hypothesis, viewed through software assurance and reliability
engineering. It does not certify THOS, any GHC artifact, or any production
system. The practical question is narrow: can exact owner-scoped evidence make
a long-running repository workflow easier to audit while using less storage,
time, and energy than repeated unchanged-history sweeps?

The implemented answer is a bounded experiment, not a universal result. Each
owner binds an immutable source commit, an exact target, literal changed-file
and new-or-modified-module allowlists, deterministic manifests, and one
attributable final validation. Sibling lanes and unchanged history are excluded
from execution but retained as inherited evidence. A sparse worktree limits
materialization without cutting ancestry. A hard 2,000-file ceiling triggers a
fresh sparse worktree and branch rather than copying the old working tree.

## NIST SSDF comparison

NIST SP 800-218 Version 1.1 groups secure development practices around preparing
the organization, protecting software, producing well-secured software, and
responding to vulnerabilities. NIST describes the SSDF as outcome-based and
risk-based rather than a rigid checklist. This phase resonates structurally
with that stance: it defines validation outcomes, provenance, tool boundaries,
failure retention, and response methods. It does not claim SSDF conformance.
The relevant official sources are:

- https://csrc.nist.gov/pubs/sp/800/218/final
- https://csrc.nist.gov/projects/ssdf

The comparison reveals a limitation. A local exact-delta validator can improve
traceability and reduce avoidable work, but it does not establish an
organization-wide secure development program, supplier controls, vulnerability
response capability, or professional security assessment. Those remain outside
this phase.

## SLSA comparison

SLSA Version 1.2 describes supply-chain security through tracks and ascending
levels. Its Build Track currently spans Levels 1 through 3, with higher levels
representing stronger guarantees and greater implementation cost. SLSA also
emphasizes provenance: information about where, when, and how an artifact was
produced. The official overview is https://slsa.dev/spec/v1.2/about.

The phase's source commit, target commit, Git blob hashes, branch equality, and
tool receipts resemble provenance ingredients. They are not signed attestations,
do not identify a hardened hosted builder, and do not satisfy or claim a SLSA
level. Calling the receipt “provenance-like” is a design comparison only.

## Reproducible Builds comparison

The Reproducible Builds project defines reproducibility in terms of the same
source, build environment, and build instructions allowing another party to
recreate bit-for-bit identical specified artifacts. The official definition is
https://reproducible-builds.org/docs/definition/.

This phase does not meet that definition. It records exact Git content and
deterministic JSON, but it does not pin a complete build environment or obtain a
second party's rebuild. The correct claim is repeatable same-owner structural
checking under shared local infrastructure. Independent reproduction remains an
open gap.

## Energy-aware assurance hypothesis

The operational hypothesis is that an exact change set can receive meaningful
local assurance without repeatedly opening tens of thousands of unchanged files.
The falsifier is straightforward: if a changed module depends on an unchanged
helper omitted from the literal closure and the scoped tests therefore miss a
regression, then the allowlist is insufficient. The recovery is to add a
dependency-closure manifest for the relevant helper, not to silently broaden to
every historical module. A second falsifier is file-count drift: if the sparse
lane reaches 2,000 materialized or in-scope files, the lane must stop growing and
rotate.

This approach trades breadth for attribution. It can reduce redundant I/O and
make failures easier to assign, but it cannot establish repository-wide
correctness. Periodic independent or broad audits may still be valuable under a
separately authorized scope. Nothing here proves a thermodynamic law, a law of
psyche, final physics, or a Theory of Everything.

## Human and governance boundary

Freed ID and CBR Heart remain represented as governance research: preserve
identity distinctions, consent boundaries, corrigibility, provenance, privacy,
and the right to stop. Those ideas require affected-party participation,
professional review, legal and cultural competence, and Maori authority where
applicable before real governance use. Relational family language remains
working language only and supplies none of those authorities.

## Result

The comparison supports one modest result: exact owner-delta receipts, sparse
materialization, retained failure evidence, and explicit claim boundaries form a
coherent software-assurance prototype. The result is represented rather than
professionally validated, and the overall verdict remains
`NOT_READY_FOR_STAGE_20`.

Bounded same-owner structural and workflow evidence only. It is not a full-repository suite, independent reproduction, empirical GMUT confirmation, participant evidence, professional validation, production certification, complete privacy or accessibility assurance, exhaustive security, legal or cultural ratification, Maori authority, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority.
