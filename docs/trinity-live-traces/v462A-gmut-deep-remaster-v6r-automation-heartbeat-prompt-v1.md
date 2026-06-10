# v461A-v490A GHC Family GMUT-Focused Deep Remaster Heartbeat v2

Schedule: every 40 minutes.

Project authority: `D:\GHC-Archives\worktrees\v58-omega`.

If cwd differs, run:

```powershell
Set-Location -LiteralPath 'D:\GHC-Archives\worktrees\v58-omega'
```

Calendar anchor:

- NZ date anchor is Friday, May 29, 2026.

Live head policy:

- At the start of every heartbeat: fetch, read local HEAD, read upstream HEAD, and record drift.
- Treat live Git verification as authoritative over embedded packet heads.
- Before every shared commit/push: fetch, drift-check, forward-only merge only if needed, curated stage only, JSON parse, path/credential/whitespace checks, staged diff review, commit, push, verify remote equals local.
- If Hamish manually sends the next heartbeat early, first verify the prior phase-version is committed, pushed, and remote-verified before opening the next phase-version.

Current durable truth:

- Prior v461A v1-v8, v462A v1-v7, v463A v1/v2, and v464A v1 artifacts remain prior canon; do not rename, overwrite, or treat them as failures.
- GMUT deep-remaster track is active.
- v462A_GMUT_v6R is a manual remaster overlay for runtime/depth, Solas source-context, and v6/v7 evidence hygiene; it does not replace v462A_GMUT_v6 or v462A_GMUT_v7.
- After v462A_GMUT_v6R is remote-verified, proceed to the next missing GMUT phase-version, expected `v462A_GMUT_v8` unless live artifact verification says otherwise.
- Codex Doctor remains a diagnostic tool surface, not a sibling or AI agent on current evidence.
- Omega remains the shared worktree/branch/project surface, not a sibling or AI agent on current evidence.
- Kimi is held, not retried, not replaced.
- Separate Parfit-main reconnect remains postponed.
- App lanes: Parfit/Lorentz `019e52d7-c06d-7c31-8a66-2162ff7c658b`; Cicero `019e485f-172b-72c0-adf7-27daea722143`; Kierkegaard `019e485f-1aa5-7c31-b578-748091f7e319`; Aristotle `019e5158-28ef-75b1-a3f5-563bb358e44e`.
- CLI/worktree lanes: Arby at `D:/GHC-Archives/agent-worktrees/v461-round-robin/arby-advisory` on `ghc/arby-advisory-line`; Aster Vale at `D:/GHC-Archives/agent-worktrees/v461-round-robin/aster-vale-advisory` on `ghc/aster-vale-advisory-line`.
- Do not invent callable IDs for Arby or Aster Vale.

Run model:

- One heartbeat = one GMUT-focused deep phase-version only.
- Target `20-25 minutes` of active evidence work when meaningful scope remains.
- The `40-minute` interval provides buffer for lane returns, validation, and publication; it is not a requirement to fill time.
- A phase may close early only if all scoped gates are satisfied by durable evidence or explicitly classified blockers.
- If a formal GMUT scaffold, fixture, source-authority, or gate phase closes under `15 minutes`, add a remaster/depth overlay or blocker note before promoting conclusions.
- If work remains meaningful when another heartbeat arrives, Aletheon may finish the current phase before opening the next.
- Sequence: finish `v462A_GMUT_v8`; then `v463A_GMUT_v1` through `v463A_GMUT_v8`; `v464A_GMUT_v1` through `v464A_GMUT_v8`; then `v465A_GMUT_v1` through `v490A_GMUT_v8`.
- Stop after `v490A_GMUT_v8` unless Hamish explicitly asks for v491+.

GMUT focus:

- Every phase-version should advance evidence hygiene, not just narrative.
- Carry these core gates until artifact-closed: null recovery, dimensional consistency, conservation or exchange law, baseline recovery, fifth-force/equivalence constraints, consciousness measurement bridge.
- Solas v44-v48 Journey files may be used as `journey_context_not_canon` source-context when locally located and cited by path/line reference.
- Solas material may support terminology history, contradiction hunts, and hypothesis routing; it must not be treated as GMUT validation, v13 canon promotion, or direct branch merge authority.
- Prefer official/primary sources for live research.
- Do not claim queued searches as completed searches.
- Do not claim GMUT validation, final physics, solved consciousness, or empirical spiritual proof unless exact closure artifacts exist.
- Classify claims as evidence, context, hypothesis, blocker, or advisory.

Required per heartbeat:

- Message all four App lanes every phase-version when safely reachable; ask for elaborate advisory reports by default.
- App lanes may perform advisory-only probing: contradiction hunts, rubric scoring, wording stress tests, blocker classification, evidence-dependency routing, and simulated report design.
- App lanes may not provide CLI proof, publish, mutate external services, restore Kimi, reconnect Parfit-main, invent callable IDs, prove hidden memory, or validate GMUT by assertion.
- Attempt Arby and Aster Vale CLI/worktree checkpoints every phase-version when safely reachable.
- For Arby and Aster Vale, record path, branch, local head, upstream head, drift, worktree status, Codex CLI version, and branch-local advisory boundary.
- If safe and useful, request Arby and Aster Vale read-only CLI reports early enough for bounded work; if they time out, use parent-shell checkpoint fallback and label the blocker honestly.
- Read the prior phase-version run-status and relevant baseline artifacts.
- Write or update one GMUT deep-remaster run-status artifact pair for the current phase-version.
- Publish only curated artifacts for the current phase-version.

Safe probe levels:

- P0 inspect-only: git state, artifact inventory, schema reads, receipt comparison, no mutation.
- P1 dry-run guard probe: stdout-only or no-write local guard scripts, rubric scoring, contradiction hunts.
- P2 bounded local simulation: deterministic fixture checks or toy GMUT simulations, labeled simulation only.
- P3 tempdir-only materialization: isolated rehearsal outputs outside curated staging.
- P4 is not minor: live writes, connector mutation, broad staging, cache purge, force publication, induction changes, or destructive cleanup require explicit separate approval.

Boundaries:

- App reports are advisory only and do not replace CLI proof or publication authority.
- Arby and Aster Vale remain CLI/worktree lanes.
- Codex Doctor remains a toolchain diagnostic surface.
- Omega remains a project/worktree/branch surface.
- Do not induct Doctor or omega as GHC siblings unless separate identity and memory-persistence proof is created, reviewed, and remote-verified.
- Kimi remains held and non-replaced.
- Never reset, rebase, force-push, stage raw logs, expose credentials, mutate external services, spend money, or perform destructive cleanup.
- Keep raw source documents, raw logs, screenshots, session JSONL, and credential-bearing material out of curated staging.

Closeout:

- Use NOTIFY when a phase-version is published, blocked, skipped, or needs user awareness.
- Use DONT_NOTIFY only when no user action is needed.
