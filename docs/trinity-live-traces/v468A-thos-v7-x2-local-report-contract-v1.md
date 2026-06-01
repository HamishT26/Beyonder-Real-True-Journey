# v468A THOS v7 x2 Local Report Contract

The report format is SARIF-style local JSON, not a certified SARIF artifact. It is meant to make THOS publication hygiene and boundary states readable.

Levels:

- `note`: informational receipt.
- `warning`: open blocker or boundary that must remain visible.
- `error`: publication should stop until fixed.

Blocked: upload, workflow mutation, cloud writes, SLSA level claims, security certification, and GMUT validation claims.
