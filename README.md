# GHC evidence utilities

Small, dependency-free JavaScript examples for inspectable agent-workflow records.

This branch collects a narrow public contribution from the GHC project. It contains an owner-scoped visible-message index, exact decimal credit-observation arithmetic, and a finite Unique Games solver. Each function has an explicit input bound and returns data without network access, process creation or filesystem changes.

## Run the examples

Use Node.js 24 or later:

```sh
node check.cjs
```

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

## Evidence and maintenance

The internal predecessor implementation passed 22 frozen literal cases and 22 input-immutability assertions in one run. This public release retains the same kernel bytes and replaces one account-shaped fixture with a synthetic example. The additional public example was checked separately; it is not counted as 22 new scientific experiments.

See `EVIDENCE.json` for exact source hashes and verification scope. `RESEARCH.md` explains the related mathematical claims. Changes should include a concrete use case, relevant boundary examples and retained first failures.

This is an early contribution. Independent adoption, downstream use and sustained community maintenance have not been established. The Codex for Open Source application is prepared separately and has not been submitted.

## Licence

The new files in this branch snapshot are provided under the MIT licence. This licence does not relicense historical content reachable through earlier repository commits or third-party works linked from the documentation.
