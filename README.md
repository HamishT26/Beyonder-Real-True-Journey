# GHC evidence utilities

Small, dependency-free JavaScript examples for inspectable agent-workflow records.

For maintainers who need a small, inspectable example of provenance boundaries and exact arithmetic, this branch provides runnable code, synthetic cases and explicit limitations. Start with [reproducibility](REPRODUCIBILITY.md), [verification](VERIFICATION.md), the [roadmap](ROADMAP.md), or the [Codex for Open Source application worksheet](APPLICATION.md).

This branch collects a narrow public contribution from the GHC project. It contains an owner-scoped visible-message index, exact decimal credit-observation arithmetic, and a finite Unique Games solver. Each function has an explicit input bound and returns data without network access, process creation or filesystem changes.

## Run the examples

Use Node.js 24 or later:

```sh
npm run check        # integrity verification, verifier tests, then public examples
node check.cjs       # preserved x1 version and expected-field examples
node check-x2.cjs    # versioned x2 module and full-output examples
```

No installation step is required. `verify-release.cjs` checks seven fixed evidence files against `RELEASE-MANIFEST.json`, with bounded reads and explicit failure results. Its tests use synthetic temporary directories. A manifest match establishes byte agreement, not authenticity. The GitHub Actions workflow runs the same checks with read-only permissions; see the run for the exact commit before treating CI as passed.

The checker compares the expected fields in 22 manually specified examples and verifies that inputs remain unchanged. For the three positive index examples, those assertions cover four top-level fields; they do not cover the complete returned records or trust notice. The source is compatible with CommonJS. No package installation, API key, account login, elevated permissions or cloud service is needed.

## What the functions establish

| Function | Result | Limit |
| --- | --- | --- |
| `index` | Ordered metadata and separately selected human-source identifiers | The caller supplies visibility, origin, hashes and verified identifiers. The function copies summary text and omits the owner from its output. It is not authentication, source-byte verification, a public serializer or automatic chat capture. |
| `budget` | Exact six-decimal differences and the phase-ceiling remainder after a closure buffer | `dispatchAllowance` describes the phase ceiling only and can exceed the latest observed account balance. It does not establish currently available credits, attribute account-wide use, or grant spending permission. |
| `uniqueGames` | Exact optimum and first lexicographic witness for at most 4,096 assignments | The accepted finite domain includes loops, repeated edges and empty edge sets. It differs from the simple bipartite domains of some theoretical reductions. Exhaustive finite search does not resolve P versus NP or prove a general approximation theorem. |

For example, baseline `10`, latest balance `1`, phase ceiling `100`, and zero buffer yield `dispatchAllowance: "91.000000"`: that is ceiling headroom, while the observed balance remains `1`. A caller needs separate fresh availability checks and authorization before spending. The index likewise requires external verification of source tuples and a separately reviewed serializer before any public disclosure.

Private source messages, account balances, local paths, credentials, launcher internals and native caches are excluded from this release. The fixtures are synthetic; no real account balance is included.

The broader GMUT and THOS research programmes remain exploratory. These utilities do not validate a physical unification theory, demonstrate consciousness, establish portable personal identity or create a production operating system.

## Versioned x2 decimal handling and coverage

`kernels-x2.cjs` adds exact decimal inputs with up to 12 fractional digits when every digit after the sixth is zero. Inputs remain bounded to 31 characters and 18 integer digits. Nonzero excess precision, whitespace, signs, exponents and trailing line terminators are rejected; outputs remain exact six-place microcredits. The preserved `kernels.cjs` retains the earlier input contract, so old examples continue to refer to their original version.

`cases-x2.json` contains 14 new synthetic examples: decimal boundaries, a full index-output assertion and finite Unique Games coverage. All 14 full results and 14 input-immutability assertions matched in one supervised execution of the exact x2 module. A draft parser was rejected during source review before execution because JavaScript `$` can match before a final newline; the released version checks the complete match. The public `check-x2.cjs` is a convenience checker for the same fixtures and was statically reviewed, not separately executed during publication. The earlier 22-case suite was not replayed against the x2 module.

The full index example deliberately shows that a synthetic marker survives projection. This demonstrates why a separately reviewed public serializer is still required. Budget ceiling headroom remains distinct from an available account balance.

## Evidence and maintenance

The internal predecessor implementation passed 22 frozen literal cases and 22 input-immutability assertions in one run. This public release retains the same kernel bytes and replaces one account-shaped fixture with a synthetic example. The additional public example was checked separately; it is not counted as 22 new scientific experiments.

See `EVIDENCE.json` for exact source hashes and verification scope. `RESEARCH.md` explains the related mathematical claims. Changes should include a concrete use case, relevant boundary examples and retained first failures.

This is an early contribution. Independent adoption, downstream use and sustained community maintenance have not been established. The Codex for Open Source application is prepared separately and has not been submitted.

The 3 November 2026 maintainer update preserves both kernels, both fixture sets, both convenience checkers and the historical EVIDENCE.json exactly. New verification results are recorded separately in VERIFICATION.md. Reproducibility reruns do not add research or scientific completion credit. The wider GHC programme is summarized only at a bounded level in ROADMAP.md; private operational records are not part of this branch.

## Licence

The new files in this branch snapshot are provided under the MIT licence. This licence does not relicense historical content reachable through earlier repository commits or third-party works linked from the documentation.
