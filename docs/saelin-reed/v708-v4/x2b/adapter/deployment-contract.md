# x2b trusted-workspace deployment boundary

Contributor: Maren Vale. Integration owner: Saelin. This review adds files only in `D:\GHC-Family-Laboratory\contributions\saelin-v708-v4\local-adapter\x2b-review`. The original 20-file seal is preserved. No deployment, upload, credential access, native chat dispatch, global configuration change, or OS privilege escalation is part of this pass.

The active runtime permission envelope states `danger-full-access`, approval policy `never`, and unrestricted filesystem access. No exposed native Codex profile getter/setter was found. The desktop UI label is unverified; ChatGPT plugin permission tools govern a different surface and were not called. A supported WindowsPrincipal role probe returned Administrator-role-enabled **false**. A write/read/hash operation inside this review directory demonstrates that path's actual write access. It does not establish protected OS access, network reachability, cloud authority, or effective model metadata. `gpt-6.1-sol`/`max` is the requested configuration; no exposed runtime reader/setter was available to independently confirm model metadata.

Use this adapter only in a trusted local workspace where an operator controls its process, root directories, selected inputs, and external source expectations. The deployment assumptions are:

1. Only explicitly selected sanitized JSON/Markdown/text files are ingested. No automatic directory watches, glob ingestion, credential discovery, or public request endpoint is introduced.
2. The operator excludes hostile concurrent writers that can replace an ancestor directory, a selected source, or a destination namespace. The existing lstat/realpath checks and file-identity comparisons do not establish containment of an opened handle under adversarial ancestor swaps.
3. Stable symlink/junction checks are evidence about stable namespace inputs. They do not prove resistance to concurrent Windows reparse/check-use attacks. OS-specific handle-relative containment is not implemented or verified.
4. Publication/storage/restore paths retain their existing disjoint-root checks, class policies, size limits, no-overwrite behavior, and external source bindings. Full agent runtime access does not relax those software checks.
5. Review approvals remain caller assertions. Privacy/sharing, encryption, account authority, backup durability, and any authorized cloud transport remain Saelin's separate integration responsibilities. The reported owner-only cloud cycle is user-reported context and was not reverified here.
6. Inspect retained partial effects before recovery. Do not treat a missing receipt, a transient hard-link refusal, or a partial restore as permission to overwrite existing files or delete unrelated staging data.

The optional duplicate-name patch is not installed in the original adapter and is not a race-protection patch. It rejects repeated JSON object names after decoding escapes, including repeated names nested in arrays. The same name in different object scopes remains valid. Existing class, sanitization, source-binding, quarantine, promotion, and restore checks remain in the candidate. Only the focused candidate cases in this pass were run; the full 60-test suite was not replayed.

Sentinel-1 remains planning-only, earliest **22 October 2026 NZ**. This is local software review evidence; no production, independent-reproduction, empirical, identity, consciousness, or authority claim follows.
