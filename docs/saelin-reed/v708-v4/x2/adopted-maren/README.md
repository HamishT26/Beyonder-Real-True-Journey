# Saelin v708-v4 local memory/evidence adapter

Contributor: **Maren Vale**. Role: local evidence custodian. Hope: make provenance easier to check while keeping memory and secrets within their declared boundaries.

This is dependency-free, synchronous Node.js software for selected, sanitized UTF-8 JSON, Markdown, and text records. It prepares local artifacts and makes no network calls. It does not synchronize drives, upload to GitHub/cloud, mount a private Journey Space, or certify content as public. Saelin owns integration. Future Sentinel-1 remains planning-only, earliest **22 October 2026, Pacific/Auckland**.

## Classification and custody

| Class | Local payload | GitHub preparation | Private cloud preparation |
| --- | --- | --- | --- |
| `public-evidence` | Allowed after selection, binding, attestation, and checks | Allowed | Allowed |
| `private-memory` | Allowed after the same checks | Rejected | Allowed |
| `secret-local` | No payload: references/metadata only | Rejected | Rejected |

Each class has separate record storage. Public/private bytes with identical SHA-256 addresses are stored in separate object directories and are not linked together. Secret references have no object directory and cannot be restored as credential material. Do not pass actual credentials to any API; use an invented opaque reference ID and benign metadata.

The caller supplies a complete externally held source expectation: `sourceId`, `version`, relative source `path`, lowercase SHA-256, and exact byte count. A payload digest checks bytes; it does not prove provenance, consent, authority, or truth. Transfer/restore expectations also pin record ID, classification, and logical path. Keep these expectations separately from an incoming capsule.

## API

Import `openAdapter`, `bindingFor`, and optionally `AdapterError` from `src/local-evidence-adapter.mjs`. There are no npm packages or installation steps. Node.js 24.18.0 on Windows was used for the recorded tests; other platforms/versions are not freshly verified.

```js
import { openAdapter, bindingFor } from './src/local-evidence-adapter.mjs';

const adapter = openAdapter({
  allowedRoot: '/absolute/path/to/explicit-selected-inputs',
  storeRoot: '/absolute/path/to/local-custody-store',
});

// externallyPinnedBinding must already describe this exact sanitized file.
const record = adapter.ingest({
  sourcePath: 'observation.json',
  logicalPath: 'notes/observation.json',
  classification: 'public-evidence',
  sanitized: true,
  expectedSource: externallyPinnedBinding,
});

const records = [{ recordId: record.recordId, classification: record.classification }];
// Keep this binding as a separate trusted input for a recipient.
const expectedSources = [bindingFor(record)];
const prepared = adapter.prepareExport({ records, expectedSources, destination: 'github' });
// prepared.bundlePath is a local JSON artifact. Preparation is not delivery.
```

`recordSecretReference({referenceId,sourceId,version,kind,purpose,logicalPath,sanitized:true})` accepts exactly those fields. `referenceId`, `sourceId`, `version`, and `kind` use short portable identifiers. `purpose` is benign text up to 512 characters. It never accepts a credential path or opens an underlying secret file.

For transfer, explicitly place one prepared JSON artifact in a receiver's allowed root through the separately authorized local integration process. Then:

```js
const staged = receiver.quarantineImport({
  sourcePath: 'capsule.json', expectedSources, expectedDestination: 'github',
});
// Review the exact digest/artifact and bindings before setting this attestation.
const promoted = receiver.promote({
  quarantineDigest: staged.quarantineDigest,
  expectedSources,
  expectedDestination: 'github',
  approval: { reviewed: true, reviewerId: 'local-reviewer', quarantineDigest: staged.quarantineDigest },
});
const restored = receiver.restore({
  records,
  expectedSources,
  destinationRoot: '/absolute/path/to/existing-local-restore-directory',
});
```

The API checks the review attestation and its digest binding. It cannot authenticate a human reviewer. Test approvals are synthetic demonstrations, not evidence of real human review or authority.

`getRecord({recordId,classification})` loads and verifies an immutable record. The receiver must promote quarantined records before they become available through active record storage. Quarantine and promotion both validate the caller's external source expectations and intended export destination.

## Storage and failure behavior

- Objects: `objects/{public-evidence|private-memory}/{payload-sha256}.blob`.
- Records: `records/{classification}/{record-id}.json`; record IDs hash canonical record content excluding `recordId`.
- Prepared bundles: `prepared/{bundle-sha256}.json`.
- Quarantine: `quarantine/{canonical-bundle-sha256}.json`. Incoming whitespace/property ordering is canonicalized; this digest describes the canonical bytes, not necessarily the transport file's raw bytes.
- Promotion receipts: `promotions/{quarantine-sha256}.json`, written after the selected objects and records.

Canonical JSON uses recursively sorted object keys, unchanged array order, and no whitespace. Bundles embed exact payload bytes as canonical base64. There are no timestamps in object/record/bundle addresses.

Writes use exclusive random staging files, file fsync, and a no-replace hard-link publication step. A byte-identical existing object/record is accepted without rewriting it. Different bytes at an existing address cause rejection. Staging cleanup unlinks only the exact file created by that operation; there is no recursive adapter cleanup. A filesystem without hard-link publication fails closed.

Restore preflights the full selected set, rejects existing destinations, and verifies every newly written file against exact byte count and SHA-256. Paths are checked for case-insensitive aliases and file/directory prefix conflicts. Existing restore files are never overwritten, even if their bytes match. An OS failure after preflight can leave a partial restore; review retained files and choose a fresh destination before retrying. Promotion is append-only and idempotent per record, not a multi-file transaction: an interrupted operation may leave verified objects/records without a final promotion receipt. Quarantine remains retained. Review that state before deciding how to resume.

Defaults are 1 MiB per payload, 16 MiB per bundle, and 64 selected records. Optional integer limits are bounded to 16 MiB, 64 MiB, and 256 respectively. Safe paths use `/` between portable ASCII segments; absolute/drive/UNC paths, traversal, backslashes, ADS, encoded traversal, globs, Windows device names, trailing dots/spaces, and empty segments are rejected. Allowed/store/restore roots must be absolute local directories with disjoint custody/input/output boundaries.

Every ancestor is checked with `lstat` and native `realpath`; linked roots, linked ancestors, common Windows junctions/symlinks, reparse escapes, and hard-linked selected files are rejected. Reads bind pre-open/open/post-read filesystem identity and bound allocation by file size.

## Validation and retained evidence

Run `node tools/run-tests.mjs your-unique-lowercase-label` from this directory. It runs the 60 named tests sequentially, writes an append-only JSON receipt under `evidence/`, and retains a unique `.test-sandbox-*` directory within this contribution. An optional third argument selects a test-name regex for a focused check; only a complete, unfiltered passing run supplies final acceptance. A repeated evidence label is rejected. All test material is synthetic; no real private user memory or credential is used. Tests assert exact bytes, directory effects, unchanged stores after rejected requests, and unchanged outside targets. No sandbox is recursively deleted. One adversarial test removes an empty directory only after verifying its exact test containment, then replaces it with a controlled junction.

`test-result.json` summarizes the final run and all retained earlier attempts. `failures.md` preserves the baseline absence, the discovered path-prefix defect, and the broader secret-key filter gap without giving a failed attempt acceptance credit. `artifact-manifest.json` seals the reviewable files with hashes and byte counts; it excludes itself and disposable synthetic sandbox trees.

`node tools/verify-artifacts.mjs` independently rereads the sealed files, checks path containment and exact hashes/byte counts, and confirms that the final passing receipt names the current source/test bytes. It writes nothing. The manifest itself has a separately reported SHA-256; pin that digest separately if authenticity of the seal matters.

## Practical limits

This is reviewable local software evidence, not production, identity, consciousness, empirical-validation, independent-reproduction, or authority proof. The current suite verifies one Windows/Node environment. It exercises file symlinks and directory junctions but does not exhaust every Windows reparse tag or every filesystem.

Sanitization is an explicit caller attestation plus conservative filename/key/token/UTF-8 checks. The scanner is intentionally restrictive and is not a complete DLP system: unknown, encoded, split, or novel credential forms and ordinary sensitive personal information require upstream sanitization and review. Private cloud bundles are plaintext base64 JSON; the adapter provides no encryption, ACL management, reviewer authentication, signature verification, or backup durability guarantee. SHA-256 integrity is not authenticity.

The filesystem boundary assumes no hostile actor concurrently rewrites ancestor directories. Portable Node APIs cannot fully close directory replacement races without OS-specific handle-relative operations. Exclusive publication prevents overwrites, but parent checks are not a proof against an adversarial same-user race. File fsync is requested; directory fsync is best-effort where Windows/platform APIs reject it. Crash/power-loss durability, concurrency stress, fault injection, and live uploads are not demonstrated by this suite.
