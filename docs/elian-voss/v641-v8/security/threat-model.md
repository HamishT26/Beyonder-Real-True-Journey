# V641-v8 bounded artifact threat model

The protected assets are the frozen x1 packet, evidence manifests, phase truth, retained negatives, privacy boundary, and owned Git lineage. The bounded adversary can replace a metadata fixture between check and use, swap a manifest, present a stale hash, or propose a link/reparse target outside the phase. Fixtures are inert descriptions: no real link is created and no unsafe target is dereferenced.

Trust boundaries are the owned worktree, Git index, detached snapshots, official source metadata, and the future external-executor packet. Controls are content hashing at use, canonical relative-path validation, no-follow policy, quarantine on mismatch, retained negatives, non-destructive restore, and complete revalidation before reopen. This is a bounded negative-test model, not an exhaustive security assessment.
