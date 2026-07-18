# GHC Family Method Flow State

- Phase: v649-gmut-thos-v1-x1-x2
- Owner: Eiren Kestrel
- Methods: 7
- Passing witnesses: 7
- Failed witnesses retained: 7

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

### v6491-m03 — Optional decoder dependency refusal with structural fallback

- Trigger: A bounded format tribunal could use an optional decoder dependency.; The live phase forbids unrelated installation or environment widening.
- Method: Retain the missing dependency as a negative, perform no installation, and use a pure structural output/ratio-budget refusal fixture that explicitly earns no decoder or RFC-conformance credit.
- Recurrence guard: Probe optional modules once before implementation; when absent, do not install or repeatedly import them and downgrade the claimed evidence surface explicitly.
- Rollback: Remove any dependency-specific path, keep the import failure, and preserve a no-decoder boundary around the structural fixture.
- Witnesses: v6491-m03-wfail-01, v6491-m03-wpass-01

### v6491-m04 — Index reference search with concrete roots and include filters

- Trigger: A read-only search spans a skill entrypoint and its reference directory on Windows.; The intended selection includes all files under a known references directory.
- Method: Read the concrete skill file directly, enumerate the concrete references directory, and use -g filters when recursive filename selection is needed.
- Recurrence guard: Reject every rg command containing a wildcard in a path argument; use concrete roots, directory enumeration, or explicit -g include filters.
- Rollback: Discard the failed search result, retain error 123 as an operational negative, and rerun once against concrete paths.
- Witnesses: v6491-m04-wfail-01, v6491-m04-wpass-01

### v6491-m05 — Additive negative-total assertion synchronized with Method Flow

- Trigger: A phase test asserts the effective retained-negative total.; New Method Flow failures were added after the first evidence build.
- Method: Recompute the total from inherited, x1, synthetic, and x2 categories; update the builder and assertion together; rerun only the focused preflight.
- Recurrence guard: Before each focused test run, regenerate the retained-negative register after all newly recorded Method Flow failures and assert the category sum as well as the total.
- Rollback: Retain the failed focused run with zero canonical credit, restore category-consistent accounting, and rerun the bounded preflight only.
- Witnesses: v6491-m05-wfail-01, v6491-m05-wpass-01

### v6491-m06 — Exact validation-plan read without wildcard roots

- Trigger: A closeout preflight needs exact inherited validation exclusions.; Search scope spans a known phase plan and optionally version-filtered scripts.
- Method: Read the exact inherited final-validation-plan directly and use a concrete scripts root with -g only if supporting implementation lookup is still necessary.
- Recurrence guard: Run a pre-execution argument check that rejects wildcard characters in every rg root argument; exact known files must be read directly.
- Rollback: Discard the partial lookup, retain error 123, and perform one exact-file read for the authoritative exclusion list.
- Witnesses: v6491-m06-wfail-01, v6491-m06-wpass-01

### v6491-m07 — Repository-root import preflight for script-hosted suite runner

- Trigger: A Python runner stored under scripts imports repository test modules.; The runner is launched by file path rather than module mode.
- Method: Insert the resolved repository root into sys.path before importing test modules, then rerun only the plan-only selector.
- Recurrence guard: Every script-hosted test selector must assert that its repository root is present in sys.path before discovery and must provide a nonexecuting plan-only mode.
- Rollback: Retain the import failure with zero suite credit, amend only the launcher path, and rerun plan-only discovery without executing tests.
- Witnesses: v6491-m07-wfail-01, v6491-m07-wpass-01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
