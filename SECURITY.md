# Security scope

These utilities accept already parsed JSON-compatible data in a trusted local process. They are not network parsers, sandboxes, credential stores, access-control services or operating-system path validators.

An exposed service must enforce transport byte and depth limits before parsing, authenticate callers, authorize individual operations, and protect its own storage. The supplied `verifiedHumanIds` parameter is an external trust input; malicious callers can mislabel provenance.

For a suspected issue, share a minimal synthetic reproduction without real credentials or private records. Do not run intrusive tests against third-party services.
