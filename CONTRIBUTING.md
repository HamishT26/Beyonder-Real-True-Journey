# Contributing

## Local workflow

Use Node.js 24+ and run `npm run check` from the repository root. No dependency installation is needed. Work against the `Codex-for-Open-Source` branch; open a draft pull request targeting that branch, not an unrelated historical branch. Include your Node version and commit hash in a reproducibility report.

For the release verifier, add a named `node:test` case in `test/verify-release.test.cjs`. First show that the test detects the failure, then make the smallest change and run the entire check command. Explain any skipped tests. Fixtures must be synthetic. The verifier's seven-file allowlist and read bounds are part of its contract.

Do not update RELEASE-MANIFEST.json simply to hide a mismatch. Explain any intentional payload change and preserve the prior version and its evidence. Neither original kernel nor original fixture set should be silently repurposed for a different contract.

## Issue and review content

Open an issue with a minimal synthetic example, the expected behaviour and the observed behaviour. Do not submit private conversations, credentials, personal data, operating-system tokens or account screenshots.

A proposed code change should retain existing result semantics or describe the intentional change explicitly. Add examples for the changed boundary, keep the first failure in the review discussion, and separate reused checks from new checks. The maintainer reviews changes before merging.

Do not infer runtime authority from a record field or hash. Any future filesystem, network, billing or native-chat adapter requires its own capability, provenance and failure-handling design. These pure examples do not supply those controls.

AI-assisted contributions are welcome when their author can explain and verify them. Identify meaningful AI assistance, retain relevant failures, and do not treat assistant agreement as independent review. A maintainer remains responsible for accepting changes. We do not promise a response time or support service-level agreement.
