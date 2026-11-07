# Reproduce this release

Use Node.js 24 or newer and npm. No npm install, account, key, cloud subscription or administrator access is required.

```sh
git clone --single-branch --branch Codex-for-Open-Source https://github.com/HamishT26/Beyonder-Real-True-Journey.git
cd Beyonder-Real-True-Journey
npm run check
```

Record `git rev-parse HEAD` and `node --version` with your result. A branch name moves; a commit hash identifies the snapshot you checked. Check a known commit from a trusted channel if authenticity matters.

## What runs

1. `npm run verify` reads RELEASE-MANIFEST.json and hashes seven fixed evidence files. Success is `{ "ok": true, "checked": 7, "errors": [] }` with exit 0. Other outcomes exit 1.
2. `npm test` exercises the verifier against synthetic temporary directories, including malformed manifests, missing files, changed bytes, oversized data and symlinks. Tests create and remove only their own temporary directories. Some hosts cannot create symlinks; those cases are explicitly skipped there rather than reported as passed.
3. `npm run examples` executes the preserved 22 expected-field cases on kernels.cjs and the 14 full-output cases on kernels-x2.cjs. Both check input immutability. They are different suites with different comparison scopes, not 36 independent scientific experiments.

The verifier accepts exactly seven distinct manifest entries: both kernels, both fixture sets, both convenience checkers and EVIDENCE.json. It rejects extra manifest fields or names, duplicates, missing entries, malformed digests and invalid sizes before reading payloads. Manifest reads are capped at 16,384 bytes; individual evidence files at 1,048,576 bytes. Files must be ordinary files, not directories or ordinary symlinks. Errors expose only fixed basenames and error categories.

`checked` counts successfully read payloads, not matching hashes. A result may therefore have `checked: 7` and `ok: false`. A manifest error has `checked: 0`. The CLI checks its own directory, independent of your current working directory. It does not accept arbitrary paths from command-line arguments.

## Trust and scope

A manifest can be modified alongside the files. A match proves byte agreement, not trusted authorship, safety, licence ownership, physical truth or correct human authorization. The verifier is not a signature verifier, malicious-filesystem sandbox or general archive extractor. Use a stable, trusted local checkout. Parent-directory links, concurrent hostile writers and platform-wide isolation are outside its security guarantee. It does not hash unrelated checkout files or documentation.

The public kernels assume parsed JSON-compatible data in a trusted process. Do not pass live objects with getters or prototypes from untrusted code and expect isolation. The index copies summary strings and does not redact them.

## Historical versus current checks

EVIDENCE.json is retained byte-for-byte as a historical receipt. Its publication-time statements remain historical. VERIFICATION.md records the newer maintainer verification separately. Repeating the examples confirms the same public behaviour in another run; it does not manufacture additional novelty or research credit.

GitHub Actions runs the same command with read-only repository permissions, pinned action revisions, no model calls and no deployment. Inspect the run for your exact commit. A workflow file is not proof that CI has run or passed.

## Updating evidence later

Intentional changes to frozen payloads require a separately reviewed version, changed expectations where justified, and a new evidence record. Never silently refresh hashes to make an unexplained mismatch disappear. Preserve the prior failure and investigate it first.
