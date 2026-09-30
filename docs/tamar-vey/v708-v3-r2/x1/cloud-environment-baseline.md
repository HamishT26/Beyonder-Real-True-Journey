# Managed-cloud baseline

This baseline is derived from the existing cloud task's attributable closeout and
the user-supplied screenshots. It is not a fresh runtime probe from the local
Tamar task.

- Repository: `HamishT26/Beyonder-Real-True-Journey`, main branch checkout.
- Prepared Python environment: `/workspace/.venv-beyonder`.
- Declared requirements plus separately identified `cryptography==50.0.1`.
- Writable cache selectors: `MPLCONFIGDIR` and `PIP_CACHE_DIR` below `/workspace/.cache/beyonder`.
- Representative service: V56 enterprise control-plane dashboard on localhost
  port 8560; prior bounded HTTP check returned 200 and the process was stopped.
- Reported quick result after dependency recovery: 37/38.
- Reported standard result: 1,126/1,155.
- Remaining failures were classified by the cloud task as stale evidence/gates
  plus two code defects, not missing environment dependencies.
- The environment configuration was shown as published. A later draft or current
  runtime state must be probed inside a managed cloud task before reuse.

Open boundaries:

- The local Tamar task cannot infer current secret readiness, network policy,
  cloud root, environment drift, or a running service from this closeout.
- The D: drive and private local GHC Family Laboratory do not exist at the same
  paths in the managed Linux environment.
- Cloud results require content-addressed export/import receipts and local
  quarantine before they can enter canonical custody.
