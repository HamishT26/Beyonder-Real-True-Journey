# Evidence review methods: 19 November 2026

This note records a proposed maintenance contract for future GHC evidence tooling. It is documentation, not an additional runnable release. The public JavaScript utilities and the seven frozen payloads in `RELEASE-MANIFEST.json` retain their existing contracts.

The wider programme has produced privately retained candidate packages, reviews and corrections. Their source, test records and private coordination are not included here. This note does not ask a public reviewer to accept those private claims, and those totals are not evidence of public adoption. A future public implementation should include its own synthetic reproducer, source and tests.

## Separate the questions a review answers

An evidence consumer should report several results instead of compressing them into one green flag.

| Question | Evidence needed | What the result does not establish |
| --- | --- | --- |
| Did the bytes match? | Actual bounded reads, exact sizes and computed digests | Authorship, authorization or safety |
| Is the record well formed? | Versioned schema, exact types, required fields and bounded collections | Whether its claims are true |
| Does a source reference exist? | The pinned source and an unambiguous symbol or span | Correct implementation of the claimed behaviour |
| Was a particular case recorded? | A unique case identifier, attempt identifier and retained result | Independent execution or exhaustive coverage |
| Does a case support a requirement? | A reviewed requirement-to-case mapping and relevant observations | Every other requirement with a similar label |
| Is a release accepted? | An identified reviewer, agreed criteria and an explicit decision | Production, legal, scientific or cultural authority beyond that decision |

The existing branch verifier answers the first two questions for its narrow seven-file contract. It does not become a general evidence interpreter because a new document describes one. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for its actual trust assumptions.

## Capture individual case results at execution time

A future receipt should record the source revision, fixture identity, attempt identity, discovered case identifiers and each observed outcome. A requirement mapping should be frozen before execution or clearly labelled as a later interpretation.

A useful contract would distinguish:

- the number of selected cases;
- the number actually started;
- the number with retained terminal results;
- passes, failures, errors and skips;
- interrupted cases and unknown effects;
- cases omitted from selection;
- repeated evaluations of an existing case.

Zero failures is insufficient when no required case ran. A missing case is not a pass. A repeated passing run can support reproducibility without becoming a new contribution. Corrections, alternate formats and repeated assertions do not multiply the number of implemented requirements.

Preserve the first failing attempt and the exact source that produced it. If the final source differs, an old receipt's source mismatch is expected historical information; it should not silently disappear or be rewritten as though the earlier attempt ran the new source.

## Treat historical logs as supplementary evidence

An old text log may contain useful per-case output even when its machine-readable receipt contains only aggregate counts. A supplementary reader can associate a named result line with a pinned source reference and report the exact matching basis.

That supplementary interpretation should retain its own version and source pins. It must not rewrite the old receipt, manufacture fields that were never recorded, or imply a new execution. If a discovery loader reports only a flat module name, association with a uniquely named archived source member still does not independently prove Python import origin.

Ambiguous names, duplicate case identifiers, inconsistent denominators and unmatched references should remain visible. A stricter schema can expose a real evidence gap even when the old code had passing producer tests. Both observations can be retained without collapsing them into a single verdict.

## Bound file handling according to the threat model

For a future local POSIX reader, a useful design is to receive an explicitly trusted root, traverse relative components through directory descriptors, reject links under the declared policy, bound reads, and compare the opened object's identity before and after reading.

A final-component FIFO can block an ordinary read-only open before a later regular-file check runs. Where the platform supports it, a no-follow pre-open stat, a nonblocking open, and an opened-descriptor regular-file and identity check address that specific class. A test of such a failure should use a newly owned fixture and a terminable child with retained timeout, reap and stream-closure observations.

These are design requirements for a future candidate, not a claim that the current public verifier supplies hostile-filesystem containment. The existing verifier explicitly assumes a stable, trusted checkout. A local regular-file read is also not a hard real-time deadline guarantee. A malicious administrator, hostile mount, concurrent multi-tenant filesystem or distributed store needs separate analysis and evidence.

## Persist enough signed data to verify after reopening

A future signed review store should retain the canonical event bytes and signature, the relevant public key and policy revision, and the actual decision-source bytes or an independently trusted immutable reference. Reconstructing a decision after reopening should recheck the signatures and the exact source binding.

For a synthetic committee, quorum counting by distinct public keys avoids counting two aliases of the same key twice. It does not establish distinct natural persons: one person can control multiple keys. Conflict exclusions should apply to keys as well as display names.

A signed withdrawal or changed decision should be a new event with ordering and predecessor information. Preserve the earlier disagreement. An exact replay can be idempotent while a conflicting replay, sequence gap or wrong predecessor is rejected.

A local hash chain alone cannot detect deletion of a valid suffix from the only retained copy. An external checkpoint is needed for that threat. Digital signatures likewise do not establish the truth of a claim, meaningful consent, a person's identity or institutional authority.

## Make rights records explain their scope

A reuse request, retention review and permission grant are different records. Future tooling should retain the actor, purpose, source context, reason, time and the authority actually established for the operation. A request should not silently become authorization.

An output cannot consistently claim that the same field was both released and withheld in the same projection. This can be checked as a data-consistency rule. Passing that rule does not establish the legal or ethical adequacy of the disclosure.

Deleting a primary working copy does not establish deletion from registered backups. A withdrawal workflow should enumerate the inventory it actually inspected and retain unresolved copies. A document or status flag cannot substitute for observed enforcement.

## Use the Trinity Mandala as a review structure

For this contribution, the three pillars can organize concrete questions:

- **GMUT:** state assumptions, dimensions, derivations, observable predictions and falsifying evidence. Algebra and synthetic numerical examples do not establish empirical validation of a unification theory.
- **THOS:** make resource admission, execution, recovery, evidence custody and failure handling observable within an explicit environment.
- **Freed ID / CBR:** explain identity assumptions, purpose limits, conflicts, appeals, withdrawal and the authority that remains unestablished.

Sentinel can consume those records as a proposed orchestration and evaluation layer. A controller check is not a trained-model improvement. A deployment specification is not evidence that Docker or Kubernetes has been deployed. The dated [infrastructure note](INFRASTRUCTURE-STATUS-20261118.md) explains the proposed New Zealand context and its limits.

## Next public contribution

The most useful next step is a small, independently reproducible implementation of one of these contracts, with synthetic fixtures and an explicit compatibility decision. It should preserve the current release, add a versioned implementation where semantics change, retain its first failures, and show which requirement each case exercises.

Public reviewers should be able to run it without private messages, account access, paid inference or trust in a project-wide completion total. Independent use and external review remain necessary evidence for usefulness. This note creates no new deployment, acceptance, adoption or programme-selection claim.

Prepared with AI assistance from Aurenna Quill for maintainer review. The maintainer remains responsible for accepting and publishing changes.
