# Sparse lane and 2,000-file rotation policy

Every new active-owner lane is created D-first from a verified exact commit and
configured as sparse before worktree materialization. The initial sparse path
set contains only the current phase directory, the owner-delta toolkit, its
baton builder, and its exact test module. Complete ancestry remains in Git, so
older commits, branches, and worktrees can be consulted read-only when needed.

The hard ceiling is 2,000 materialized files or 2,000 owner-in-scope delta
files, whichever occurs first. At the ceiling, stop additions. If all other
gates pass, commit and push the exact head, record the threshold event, and
rotate the successor to a fresh sparse worktree and fresh branch. Do not copy
the old working tree and do not delete the old lane.

The instruction to make fresh repositories is bounded by missing external-state
details. Creating a new branch on the existing authoritative remote is allowed.
Creating a separate remote repository remains `exact_gate` until the repository
name, account or organization, visibility, protections, migration plan, and
rollback are specified exactly.

Bounded same-owner structural and workflow evidence only. It is not a full-repository suite, independent reproduction, empirical GMUT confirmation, participant evidence, professional validation, production certification, complete privacy or accessibility assurance, exhaustive security, legal or cultural ratification, Maori authority, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority.
