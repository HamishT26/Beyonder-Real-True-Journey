# Publication and partial-restore findings

The review models faults only in a dedicated synthetic directory under x2b-review. The deterministic in-process fs hooks invoke the real filesystem and are restored in `finally`. They are cooperative boundary fixtures, not hostile-concurrency, actual process-crash, or power-loss evidence. All injected failure states are retained, and no automatic cleanup or recursive deletion is performed.

## Publication hard-link lifetime

Immediately after exclusive `linkSync(stage, object)`, the object and stage have the same inode and link count 2. A cooperating duplicate ingest in that interval is rejected with `HARDLINK_REJECTED`. After staging unlink, the steady-state object has link count 1, its exact bytes verify, and its record can be loaded. A transient refusal is compatible with fail-closed no-overwrite behavior; it is not evidence that an object was corrupted.

A simulated staging-unlink failure with `EINTR` leaves both names linked to verified object bytes, with no record published. Retrying the same source is rejected with `HARDLINK_REJECTED`, and the store is unchanged. The receipt records both exact filenames, inode equality, digest, link count, and failure/refusal codes. This is a retained operational recovery limitation. The optional JSON patch does not change it.

If an authorized operator chooses to recover such a state, first quiesce cooperating writers and retain the failure receipt. Under the trusted-workspace assumption, check the exact known stage and object paths, all ancestors, object class, external source binding, byte count and SHA-256, matching device/inode, and expected link count. Only then consider unlinking that one known stage name and verifying that the object remains byte-identical at link count 1. Recheck the exact missing postcondition before retrying. This is a manual procedure for review, not an automatic janitor or proof against hostile concurrent replacement. Do not infer that arbitrary `.stage-*` names are disposable.

## Partial restore recovery

The second restore publication was deterministically failed with `EIO`. The adapter returned `ATOMIC_PUBLISH_FAILED`; one verified destination file remained. A full replay returned `DESTINATION_EXISTS`, preserving that file. Recovery with only the still-missing selected record and its externally held source tuple completed the restore, with both payload hashes verified and the first file's inode/mtime unchanged.

An operator can choose a new destination, as the original README describes, or use this demonstrated missing-only recovery: validate every retained selected file against its external digest/size; retain the failed attempt; derive an explicit missing-record selection; pass only those references and exact expectation tuples to restore. No overwrite, relocation, or deletion is needed. This requires a trusted namespace and explicit selection; it does not authorize replaying a failed aggregate or accepting unverified retained files.

## JSON duplicate-name boundary

The sealed adapter accepts `{"observation":"first","observation":"second"}` when its exact raw source binding matches. Raw payload bytes are preserved, while Node's parsed value is the final name occurrence. At bundle import, a shadowed escaped `format` name is accepted and omitted from canonical quarantine bytes even though source bindings match. No class-declassification or overwrite bypass was demonstrated. The material finding is ambiguous raw JSON semantics at the trust/review boundary.

The optional patch introduces a small dependency-free guard that rejects duplicate decoded names in each object scope before returning the native parsed value. It uses existing read limits and maps `DUPLICATE_JSON_NAME`/`STRUCTURE_LIMIT` to adapter error codes. Invalid syntax remains `INVALID_JSON`. Rejection is tested before store changes, and an ordinary candidate quarantine/promote/restore round trip is verified. It remains an optional, unapplied candidate for Saelin's review.
