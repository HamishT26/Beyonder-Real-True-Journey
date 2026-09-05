# Portable evidence capsules: Rowan Ash v685-v6

The owner-local checker turns a declared set of Git blobs or synthetic inputs into
inspectable byte and workflow evidence. It uses Python's standard library and
Git. It installs no package, contacts no task or external service, and performs
no Git mutation.

The frozen planning source is e3f97e0764cbbf0f5aa7d3a9f2ecf42bfb142b64. The
activation source is Eiren Kestrel final
74dd8f72cfc9d06d8c6c7370131a5baa61a66397. Eiren's one canonical remains invalid
at 23/24 with zero success credit and zero replay. Its separately retained
content-seal recovery is inherited context, not Rowan completion credit.

## Commands

Run from the owner repository:

```powershell
python scripts/ghc_family_evidence_capsule.py digest --file docs/rowan-ash/v685-v6/x1/README.md --domain raw_bytes_v1
python docs/rowan-ash/v685-v6/x2/runners/ghc_family_capsule_paths.py --input docs/rowan-ash/v685-v6/x2/fixtures/paths-accept.json
```

The engine also provides `seal` for a full immutable commit and an
explicit JSON array of repository-relative file paths, and `render` for a
new HTML report. Both require a new output filename and refuse to overwrite it.
Use `--help` to inspect the exact arguments.

The `check` command and ten thin command interfaces evaluate declared
synthetic models. They do not establish that supplied lifecycle or authority
statements are true. The terminal verifier separately reads actual Git objects,
the exact owner delta, and fresh remote state.

## Byte domains

- `raw_bytes_v1` hashes bytes without decoding or transformation.
- `raw_git_blob_v1` hashes immutable Git blob content, including binary
  content and any line endings actually stored in that blob.
- `utf8_crlf_to_lf_v1` validates UTF-8 and replaces CRLF pairs with LF.
  It preserves lone CR, trailing whitespace, a BOM, and final-newline absence.
  This is a specifically named transform, not a universal Git normalization rule.

Git can store LF while materializing CRLF in a checkout. The digest domain must
therefore be explicit at creation and verification. The blob reader consumes
Git's declared object size rather than line counts. These choices follow the
[Git attribute documentation](https://git-scm.com/docs/gitattributes) and
[Git object reader documentation](https://git-scm.com/docs/git-cat-file).

The portable filename profile is deliberately restrictive. It refuses parent
segments, absolute or drive paths, backslashes, control characters, non-NFC
spellings, case-fold collisions, common Windows aliases, and Git pattern
characters. The manifest uses a closed allowlist, regular-file modes, and
separately declared self-exclusions. A valid path is not permission to read
another owner lane.

JSON output is strict UTF-8, finite, sorted-key JSON. It is not claimed to be
RFC 8785 canonical JSON. SHA-256 establishes a bounded byte fingerprint, not
semantic correctness, authority, or production security.

## What was exercised

The initial 60 behavioral tests passed and retained 103 rejecting fixtures.
Code review subsequently found two gaps: Git pattern characters were accepted
by the initial path profile, and malformed nested input could escape the public
error envelope. Both operational failures were retained before correction.

Two focused regressions then passed, covering eight refused pattern characters
and one bounded malformed-input response. The original engine and test
definitions were reconstructed and matched their captured pre-correction
SHA-256 values. They remain in retained-definitions as data, with the initial
receipt and the separately named focused recovery.

Ten command interfaces passed one accepting and one rejecting smoke each.
Twenty local skill packages were initialized, read through EOF, structurally
validated, and used to review the corresponding acceptance and evidence rules.
They were not globally installed or independently forward-tested.

The Git integration read all 38 immutable owner x1 blobs. Sixty inherited
identity/title checks and changed-title refusals retain zero current completion
or novelty credit. No Eiren test suite or canonical aggregate was replayed.

## Evidence interpretation

The sixty core proposal records resolve to 48 completed bounded software
conditions, six represented report conditions, three open gaps, and three exact
gates. A held reservation may have a passing representation check while its
real-world action remains unexecuted.

The 67-card deck contains one relational owner anchor, three Trinity pillars,
three synthetic practices, and sixty task cards across thirteen sections.
It provides navigation and selective loading. It establishes no cache,
memory-continuity, identity-continuity, or performance claim.

The accessible report uses language metadata, semantic landmarks, table
captions and headers, explicit text outcomes, escaped content, and relative
links. Its structure checker is not a general HTML sanitizer. Manual browser,
assistive-technology, cognitive, language, and affected-user evaluation remains
reserved; complete accessibility and exhaustive security are not claimed.

The accumulated counts are record counts. They do not measure distinct
scientific findings, independent validations, or resolved authority questions.

## Continuation boundary

This task owns solo v685-v6 only. Its exact final and one owner-scoped canonical
result are recorded separately from the immutable x1 and x2 evidence.

Future siblings 02 through 15 remain planned and uncreated. Hamish retains
direct control of the announced v685-v6 (2) remaster. Elaren Kestrel v685-v7
remains prospective behind a fresh terminal instruction and route review.
This file is preparation and does not activate or contact any endpoint.

All names, roles, hopes, family language, Freed ID, CBR, and Trinity Mandala
language are relational working language only. GMUT remains a typed scalar-tensor
and EFT research-model family without empirical confirmation. THOS remains
synthetic or proxy-only without governed real arms and independent review.
Freed ID remains synthetic and nonproduction without live keys, proofs,
lifecycle, interoperability, review, recovery, and trust governance.

No professional, empirical, participant, production, deployment, legal, cultural,
affected-party, Maori-authority, privacy-complete, accessibility-complete,
exhaustive-security, independent-reproduction, AGI, ASI, consciousness,
personhood, Theory-of-Everything, proof, canon, or Stage 20 gate is closed.

Terminal verdict: NOT_READY_FOR_STAGE_20.
