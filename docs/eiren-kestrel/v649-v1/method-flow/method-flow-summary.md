# GHC Family Method Flow State

- Phase: v649-gmut-thos-v1-x1-x2
- Owner: Eiren Kestrel
- Methods: 2
- Passing witnesses: 2
- Failed witnesses retained: 2

## Preferred methods

### v6491-m01 — Windows directory-root search with explicit include filters

- Trigger: A recursive text or file search is running under Windows PowerShell.; The intended selection is a filename pattern within one or more known directory roots.
- Method: Pass real directory roots to the search tool and express filename selection through explicit include filters such as -g patterns.
- Recurrence guard: On Windows, never pass shell-style wildcard path components as directory arguments to rg; use concrete roots plus -g filters.
- Rollback: Discard the failed inventory, retain the error as an operational negative, and rerun once with concrete roots and explicit filters.
- Witnesses: v6491-m01-wfail-01, v6491-m01-wpass-01

### v6491-m02 — Compound staged stale-label audit with concrete roots

- Trigger: A staged audit searches owner documents plus phase-local scripts and tests.; Different file classes require include and exclusion filters without broad workspace enumeration.
- Method: Search only concrete owner, scripts, and tests roots; express file selection with -g include filters and exclude inherited frozen-index paths whose historical labels are intentional.
- Recurrence guard: Build compound rg audits from a concrete-root array and explicit -g filters; treat exit one as a zero-hit success only after checking the zero-line result.
- Rollback: Discard the failed stale-label conclusion, retain the wrapper failure, and rerun the bounded audit once with concrete roots and explicit filters.
- Witnesses: v6491-m02-wfail-01, v6491-m02-wpass-01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
