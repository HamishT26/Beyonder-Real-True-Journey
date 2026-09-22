---
name: ghc-family-git-blob-byte-domain
description: Keep immutable Git-blob, normalized-LF, index, and materialized-checkout byte domains explicit when building manifests and lifecycle evidence.
---

# GHC Family Git Blob Byte Domain

Use this skill when a phase hashes files, replays manifests, validates immutable x1 or evidence commits, or compares a sparse checkout with Git history.

1. Declare the byte domain for every digest: raw Git blob, normalized-LF Git blob, index blob, or checkout bytes.
2. Use `git show <commit>:<path>` or `git cat-file --batch` for immutable commit evidence; do not silently substitute materialized checkout bytes.
3. Record line-ending normalization explicitly and apply it identically at build and replay time.
4. Preserve manifest self-exclusions and prove their arithmetic separately.
5. Validate immutable lifecycle assertions in the correct commit context; a later worktree must not stand in for an earlier tree.
6. After timeouts or partial output, audit process, lock, filesystem, Git, and receipt state before retrying.

A matching manifest establishes bounded byte parity only. It does not establish semantic correctness, independent reproduction, security completeness, or external authority.
