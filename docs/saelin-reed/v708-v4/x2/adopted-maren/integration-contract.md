# Integration contract: local adapter v1

Owner: Saelin-led v708-v4. Contributor: Maren Vale, local evidence custodian. Write scope: `D:\GHC-Family-Laboratory\contributions\saelin-v708-v4\local-adapter`. No network/upload, package installation, branch/config/skill mutation, sibling worktree mutation, or onward chat dispatch is part of this vertical.

| Operation | Required caller input | Observable result |
| --- | --- | --- |
| `openAdapter` | Absolute, disjoint local `allowedRoot`/`storeRoot`; optional bounded limits | Checked local custody layout; no source enumeration |
| `ingest` | One explicitly selected relative `sourcePath`, safe `logicalPath`, public/private class, `sanitized:true`, complete `expectedSource` | Verified exact-byte object and immutable record |
| `recordSecretReference` | Benign reference ID/source ID/version/kind/purpose/logical path and sanitized attestation | Secret-local metadata record only; no source file read or payload |
| `prepareExport` | Explicit `{recordId,classification}` list, exact external `expectedSources`, `github` or `private-cloud` | `PREPARED_LOCAL_ONLY` bundle path, digest, byte count, record IDs |
| `quarantineImport` | One selected JSON file, external expected sources, expected destination | `QUARANTINED` digest; no active objects/records |
| `promote` | Exact quarantine digest, fresh external expectations/destination, `{reviewed:true,reviewerId,quarantineDigest}` | Verified class-separated active records/objects; promotion receipt |
| `restore` | Selected record references, external expected sources, existing disjoint destination root | New files only; `RESTORED_VERIFIED` exact bytes/digests/path receipts |

`expectedSource = {sourceId,version,path,sha256,bytes}`. Each transfer/restore expectation is `{recordId,classification,logicalPath,source:expectedSource}`. Missing/extra/duplicate expectations or mismatched identity/version/path/class/digest/size are rejected. `bindingFor(record)` constructs that tuple; do not reconstruct authoritative expectations from an untrusted incoming bundle.

Export policy: GitHub accepts only public-evidence. Private cloud accepts public-evidence/private-memory. Secret-local is forbidden in every bundle and restore. No export destination implies authorization to publish; preparation/delivery/recipient completion remain separate.

All schemas reject unknown fields. Only sanitized UTF-8 `.json`, `.md`, `.txt` payloads are supported. JSON payloads must parse. All file/logical paths are relative portable ASCII paths inside a caller-selected local root. No globs or directory selection. Secret keys/recognized token patterns, unsafe paths, links/junction escapes, source hardlinks, oversized payloads/bundles, missing source bindings, inconsistent manifests/base64, collisions, and tampering are rejected with `AdapterError.code` without printing payloads.

Bundle format: `saelin-local-evidence-bundle/v1`, fields exactly `{format,destination,records,objects}`. An object is `{classification,sha256,bytes,data}` with canonical base64. Record format: `saelin-local-evidence-record/v1`. Record IDs hash canonical record content excluding `recordId`; bundle/quarantine digests hash canonical full-bundle UTF-8 bytes. Array order is preserved. Raw incoming file hash may differ from the canonical quarantine digest.

Quarantine is mandatory for incoming bundles. Promotion attestations are caller assertions, not authenticated human authority. Objects and records are never replaced through the adapter. Multi-file promotion/restore may retain partial effects after an OS interruption; check for the promotion receipt and review exact retained files. A normal validation failure is tested to precede store mutation; hash collisions encountered during later publication may retain earlier verified append-only writes.

Acceptance evidence is the final 60-test receipt, source/test hashes, artifact manifest, and retained failed-attempt receipts. It does not establish encryption, ACL/privacy enforcement, complete DLP, all reparse-tag behavior, hostile concurrent-directory-race safety, crash durability, other-platform operation, live upload, production readiness, empirical science, consciousness/personhood, or authority. The Space does not thereby mount this local drive. Sentinel-1 stays planning-only, earliest **22 October 2026 NZ**. Saelin owns further review, promotion, integration, and any separately authorized transport.
