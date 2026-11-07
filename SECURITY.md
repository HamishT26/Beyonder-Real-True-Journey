# Security scope

The three kernel functions accept already parsed JSON-compatible data in a trusted local process. They are not network parsers, sandboxes, credential stores, access-control services or operating-system path validators.

An exposed service must enforce transport byte and depth limits before parsing, authenticate callers, authorize individual operations, and protect its own storage. The supplied `verifiedHumanIds` parameter is an external trust input; malicious callers can mislabel provenance.

For a suspected issue, share a minimal synthetic reproduction without real credentials or private records. Do not run intrusive tests against third-party services.

## Reporting

If GitHub's private vulnerability reporting is enabled for this repository, use its private reporting flow. Otherwise, open a minimal issue requesting a private contact route, without vulnerability details, private data or exploit material. Do not assume this file enables private reporting or that public issues are confidential. There is no security support SLA.

## Release verifier

The verifier reads only its fixed manifest name and seven fixed evidence basenames. It rejects unknown manifest entries, extra fields, duplicates, invalid sizes and malformed hashes. Reads are bounded, and ordinary symlink and nonregular payloads are rejected. It writes no release files and runs no kernel code.

This is not a hostile-filesystem sandbox. Parent-directory symlinks, concurrent privileged mutation, file authenticity and provider isolation remain outside its guarantee. A modified manifest can attest modified files. Obtain the intended commit from a trusted channel; hash equality alone is not publisher authentication.

The synthetic test harness writes only its own temporary test directories and removes them after each test. The public example runners execute local JavaScript. Review code before running an unfamiliar checkout. CI uses read-only repository permissions, no stored deployment credentials, and does not publish or deploy.
