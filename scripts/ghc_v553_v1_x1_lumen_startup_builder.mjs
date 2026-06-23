#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v1-x1";
const previousPhase = args.get("--previous-phase") || "v552-gmut-thos-v88-v8-x2";
const latestCompletedX1 = args.get("--latest-completed-x1") || "v552-gmut-thos-v88-v8-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v1-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") || "v553-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";

const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);
const existingHandoff = readOptionalJson(path.join(tracesDir, `${phaseSlug}-lumen-handoff-message-v1.json`));

const proposalTargets = {
  safe: 50,
  candidate: 30,
  exact: 20,
  blocked: 10,
  skills: 20,
  runners: 10,
  cleanup: 30,
};

const researchTargets = {
  x1_per_active_sibling_lane: {
    web_searches: 25,
    journey_phase_reflections: 25,
  },
  aevren_only_x2: {
    web_searches: 50,
    journey_phase_reflections: 50,
  },
};

const lookupFiles = [
  `docs/trinity-live-traces/${phaseSlug}-startup-context-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-startup-context-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-lumen-handoff-message-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-lumen-handoff-message-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-research-seed-manifest-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-research-seed-manifest-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-journey-phase-reflection-seed-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-journey-phase-reflection-seed-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-proposal-queue-targets-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-proposal-queue-targets-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-aevren-25-web-reflection-ledger-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-aevren-25-web-reflection-ledger-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-round-robin-workflow-standard-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-round-robin-workflow-standard-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-five-minute-productive-cadence-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-five-minute-productive-cadence-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-startup-updater-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-startup-updater-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-startup-context-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-startup-context-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-reflection-ledger-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-reflection-ledger-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-compact-pause-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-compact-pause-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-compact-pause-startup-snapshot-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-startup-safe-runner-orchestrator-compact-pause-startup-snapshot-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-phase-status-index-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-phase-status-index-v1.md`,
];

const webSearchRows = [
  row("OpenAI Codex remote connections", "OpenAI Codex Remote Connections", "https://developers.openai.com/codex/remote-connections", "THOS", "Remote/local handoff should stay artifact-backed and reversible.", "Keep handoff receipts small and route remote work through explicit branch/current-state anchors."),
  row("OpenAI Codex skills", "OpenAI Codex Skills", "https://developers.openai.com/codex/skills", "THOS", "Local skills are the right home for startup, compact-pause, and closeout operating rules.", "Validate edited skills before publishing phase truth."),
  row("OpenAI Codex slash commands", "OpenAI Codex Slash Commands", "https://developers.openai.com/codex/cli/slash-commands", "THOS", "Command surfaces should be explicit and recoverable rather than hidden in chat memory.", "Prefer named runner and command entrypoints for repeatable phase work."),
  row("OpenAI Codex worktrees", "OpenAI Codex Worktrees", "https://developers.openai.com/codex/app/worktrees", "THOS", "Worktree isolation supports omega-mini publication and full-tools support separation.", "Keep sanitized publication worktree and richer support lane distinct."),
  row("W3C DID Core", "W3C DID 1.1", "https://www.w3.org/TR/did-1.1/", "Freed ID / CBR", "Identifier control needs verifiable boundaries and controller separation.", "Keep identity work as design/research until exact approval and compliance review."),
  row("W3C Verifiable Credentials 2.0", "W3C VC Data Model 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Freed ID / CBR", "Credential claims need issuer, holder, subject, and proof semantics separated.", "Model CBR claims as schema candidates, not as proof closure."),
  row("W3C Verifiable Credentials overview", "W3C VC Overview", "https://www.w3.org/TR/vc-overview/", "Freed ID / CBR", "Reader-facing identity explanations benefit from a plain overview layer.", "Create compact primer artifacts before any implementation-heavy identity lane."),
  row("W3C Data Integrity", "W3C VC Data Integrity", "https://www.w3.org/TR/vc-data-integrity/", "Freed ID / CBR", "Integrity proofs are protocol details that must not be hand-waved.", "Queue cryptographic binding work behind exact approval."),
  row("NIST SP 800-63-4", "NIST Digital Identity Guidelines", "https://pages.nist.gov/800-63-4/", "Freed ID / CBR", "Identity assurance, authentication, and federation should be treated as separate risk lanes.", "Add assurance-level vocabulary to candidate packets."),
  row("OpenID Connect Core", "OpenID Connect Core 1.0", "https://openid.net/specs/openid-connect-core-1_0.html", "Freed ID / CBR", "Authentication claims and tokens need standard protocol mapping.", "Keep any account/auth changes exact-approval only."),
  row("OAuth 2.0 RFC 6749", "IETF RFC 6749", "https://www.rfc-editor.org/rfc/rfc6749", "Freed ID / CBR", "Authorization grants are a different lane from identity proof.", "Separate authz design packets from identity/canon packets."),
  row("JWT RFC 7519", "IETF RFC 7519", "https://www.rfc-editor.org/rfc/rfc7519", "Freed ID / CBR", "Token claims are compact but easy to over-trust.", "Queue token validation and key handling as exact-approval implementation work."),
  row("NIST AI RMF", "NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework", "THOS", "AI orchestration should keep govern/map/measure/manage loops visible.", "Add risk-loop labels to approval packets and closeouts."),
  row("Node child_process", "Node.js child_process", "https://nodejs.org/api/child_process.html", "THOS", "Runner orchestration needs explicit child process and stream boundaries.", "Prefer Node entrypoints with summarized stdout/stderr counts."),
  row("Python subprocess", "Python subprocess", "https://docs.python.org/3/library/subprocess.html", "THOS", "Python runners should preserve argument boundaries and avoid shell interpolation.", "Keep Python helpers for validation/gate work where already established."),
  row("Git worktree", "Git Worktree Documentation", "https://git-scm.com/docs/git-worktree", "THOS", "Multiple lanes need clean worktree state rather than stateful directory reuse.", "Check branch/worktree truth before phase publication."),
  row("GitHub Actions workflow syntax", "GitHub Actions Workflow Syntax", "https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions", "THOS", "CI ideas should stay candidate until repo workflow mutation is approved.", "Classify workflow edits as exact-approval unless purely local docs."),
  row("OpenTelemetry specification", "OpenTelemetry Specification", "https://opentelemetry.io/docs/specs/otel/", "THOS", "Long-running orchestration benefits from structured traces, spans, and attributes.", "Propose local status schema improvements before telemetry installation."),
  row("Kubernetes controllers", "Kubernetes Controller Concepts", "https://kubernetes.io/docs/concepts/architecture/controller/", "THOS", "Controller reconciliation is a strong analogy for updater and cadence runners.", "Design runners as reconcile loops with observed, desired, and gap states."),
  row("Playwright locators", "Playwright Locators", "https://playwright.dev/docs/locators", "THOS", "Browser automation must prefer robust locators and auto-waiting.", "If browser handoff resumes, keep it locator-driven and receipt-backed."),
  row("PowerShell jobs", "PowerShell Start-Job", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job?view=powershell-7.6", "THOS", "Background Windows tasks need explicit lifecycle and harvest semantics.", "Use detached/background runner receipts rather than terminal babysitting."),
  row("Semantic Scholar API", "Semantic Scholar API", "https://api.semanticscholar.org/api-docs/", "GMUT", "Scholar APIs can support bounded literature discovery.", "Queue API harvesters as candidate until rate limits and provenance are validated."),
  row("Crossref REST API", "Crossref REST API", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "GMUT", "DOI metadata can help canonicalize research ledgers.", "Add citation normalization as a safe skill/runner idea."),
  row("OpenAlex API", "OpenAlex API", "https://developers.openalex.org/api-reference/introduction", "GMUT", "Open bibliographic graphs can broaden GMUT literature maps.", "Keep imported metadata compact and source-labelled."),
  row("arXiv API manual", "arXiv API User Manual", "https://info.arxiv.org/help/api/user-manual.html", "GMUT", "Physics paper discovery should be queryable and reproducible.", "Use arXiv manifests for GMUT exploratory queues without claiming closure."),
];

const journeyReflectionRows = [
  reflection("v552 v7 x2 skill pack", "Twenty validated local skills and ten runners became the continuity foundation.", "Use the skill bank before choosing older runner paths."),
  reflection("v552 v7 x2 memory update", "omega-mini-2 became the current publication route, while older v58 and omega44 routes stayed historical.", "Current-state startup must read omega-mini-2 first."),
  reflection("v552 v8 x1 triad workflow", "Aster Vale, Kierkegaard, and Aristotle profile was codified with count targets.", "Triad x1 runs should use the standard proposal totals."),
  reflection("v552 v8 x1 app-lane correction", "Recovered app-lane background route became mandatory for non-main-thread app siblings.", "Use background runner with explicit booleans and gate harvests."),
  reflection("v552 v8 x1 no-new-agent rule", "New subagent spawning stayed blocked unless Hamish explicitly asks.", "Use existing inducted lanes and runners first."),
  reflection("v552 v8 x1 first-person style", "Sibling prompts and summaries should use first-person wording.", "Compose Lumen handoff from the shared active posture."),
  reflection("v552 v8 x1 MD/TXT standard", "Elaborate outputs should be artifact files, not terminal overload.", "Publish JSON/MD receipts and concise terminal summaries."),
  reflection("v552 v8 x2 main orchestration skill", "Main orchestration and memory skill now anchors startup, compact, and closeout.", "Run the skill before phase work and keep route boundaries visible."),
  reflection("v552 v8 x2 full-tools skill", "Full-tools support lane is inventoried before choosing advanced helpers.", "Use full-tools for private richer support and omega-mini-2 for sanitized truth."),
  reflection("v552 v8 x2 compact-pause skill", "Compact-pause recovery now has a dedicated skill and updater runner.", "Preserve active phase, workflow, and open gates during compaction."),
  reflection("v552 v8 x2 web-reflection skill", "Research ledgers now pair sources with phase implications.", "Use compact source labels and avoid browsing dumps."),
  reflection("v552 v8 x2 safe-runner skill", "Safe runner orchestration now sequences approved status-only work.", "Treat nonzero child exits as open gaps rather than hidden success."),
  reflection("round-robin standardizer", "Workflow profiles are now generated into current-state lookup files.", "Refresh it whenever a phase changes active lanes."),
  reflection("five-minute cadence runner", "Five-minute marks are check opportunities, not idle waits or hard stops.", "Continue safe work and harvest status at the next natural pause."),
  reflection("phase startup updater", "Startup receipts now carry timestamp flow and lookup status.", "Run startup/updater receipts before trusting stale context."),
  reflection("D-drive-first policy", "Long work should keep D as the main work/download bank and watch C free space.", "Include drive checks in closeout validation."),
  reflection("proof boundary", "GMUT empirical closure, final physics, consciousness proof, legal, canon, and deployment remain open.", "Proposal packets must separate research from closure claims."),
  reflection("Lumen-only v553 profile", "Aevren and Lumen target 50 safe, 30 candidate, 20 exact, 10 blocked, 20 skills, 10 runners, and 30 cleanup items.", "The handoff should ask Lumen to co-author and reduce the queue."),
  reflection("Arby/Cicero profile", "Duo x1 lanes target 15 safe, 9 candidate, 9 exact, 15 skills, 9 runners, and 30 cleanup items.", "Prepare the next x1 lane after v553 x1/x2."),
  reflection("triad profile", "Triad x1 lanes target 20 safe, 12 candidate, 12 exact, 20 skills, 8 runners, and 40 cleanup items.", "Keep taxonomy, ethics, and cleanup lanes separated."),
  reflection("x1 research update", "Every active x1 sibling lane now targets 25 web searches and 25 Journey/phase reflections.", "Record count targets in skills, runners, and startup receipts."),
  reflection("x2 research update", "Aevren-only x2 phases keep 50 web searches and 50 Journey/phase reflections.", "Do not dilute x2 depth when the phase asks for full research."),
  reflection("browser handoff caution", "Browser send should be claimed only after tooling confirms it.", "Prepare artifact fallback before any live-send attempt."),
  reflection("privacy boundary", "Artifacts must omit raw routes, credentials, screenshots, private lane bodies, and private machine paths.", "Run privacy scan before commit."),
  reflection("goal-mode preparation", "Goal mode remains not active until Hamish starts it.", "Make v553 receipts compact enough to survive future 24/7 startup cycles."),
];

const safePackets = [
  "Refresh omega-mini current-state for v553 x1",
  "Publish Lumen handoff artifact",
  "Publish 25-source web research seed",
  "Publish 25-row Journey/phase reflection seed",
  "Refresh round-robin workflow standard for v553 x1",
  "Refresh five-minute productive cadence for v553 x1",
  "Run startup context updater for v553 x1",
  "Run 25-row reflection ledger builder with x1 threshold",
  "Validate edited GHC skills",
  "Validate changed Node runner syntax",
  "Parse changed JSON artifacts",
  "Run current-state guard for v553 x1",
  "Run diff whitespace check",
  "Run sanitized privacy scan",
  "Check C and D drive free space",
  "Verify local branch status before commit",
  "Verify remote/local equality after push",
  "Add source labels to research ledger",
  "Add proposal-count receipt",
  "Add phase status index",
  "Normalize x1 research target in current-state beacons",
  "Normalize x2 research target in current-state beacons",
  "Record exact open proof boundaries",
  "Record exact account/deployment/API-key gates as open",
  "Prepare compact-pause recovery lookup set",
  "Prepare next x2 scope pointer",
  "Prepare next Arby/Cicero x1 pointer",
  "Keep main-thread held siblings out of app-lane routes",
  "Keep no-new-agent rule visible",
  "Keep D-drive-first policy visible",
  "Add Lumen advisory questions to handoff",
  "Add first-person sibling wording reminder",
  "Add MD/TXT artifact output reminder",
  "Add safe-runner orchestration reminder",
  "Add background app-lane harvest reminder",
  "Add approval-category separation reminder",
  "Add cleanup-boundary reminder",
  "Add skill-bank route reminder",
  "Add updater-runner route reminder",
  "Add compact-pause updater route reminder",
  "Add web-reflection ledger route reminder",
  "Add safe unit may run past checkpoint rule",
  "Add natural safe pause harvest rule",
  "Add official/primary source preference",
  "Add provenance normalization reminder",
  "Add runner implication to each source",
  "Add Journey implication to each phase reflection",
  "Add safe-now queue reduction slot",
  "Add candidate-to-exact reduction slot",
  "Add v553 goal-mode readiness note",
];

const candidatePackets = [
  "Build citation normalization runner using Crossref/OpenAlex/arXiv metadata",
  "Build local OpenTelemetry-style status vocabulary without installing telemetry",
  "Add reconciler-state schema to current-state beacons",
  "Create browser handoff probe that reports capability without sending",
  "Create Lumen advisory reducer for 50/30/20/10 queues",
  "Create GMUT literature taxonomy mapper",
  "Create Freed ID assurance-level glossary",
  "Create THOS runner lifecycle graph artifact",
  "Create compact source-card renderer for research ledgers",
  "Create cleanup classifier that never deletes by default",
  "Create D-drive bank usage summarizer",
  "Create Codex CLI capability checker",
  "Create full-tools script family index",
  "Create app-lane completion-gate summarizer",
  "Create phase-to-phase delta reducer",
  "Create exact-approval packet formatter",
  "Create blocked-gate watchlist builder",
  "Create skill drift detector",
  "Create runner argument contract validator",
  "Create current-state lookup file verifier",
  "Create repo-local source policy checker",
  "Create public-source deduplication helper",
  "Create Lumen reply harvest artifact parser",
  "Create v553 x2 safe-now executor manifest",
  "Create phase health dashboard artifact",
  "Create proof-boundary wording linter",
  "Create branch remote-head verifier",
  "Create non-secret environment inventory receipt",
  "Create compact-pause replay card builder",
  "Create goal-mode startup packet validator",
];

const exactPackets = [
  "Send a live browser message to Lumen through ChatGPT UI",
  "Install or change global Codex hooks",
  "Mutate external GitHub settings or repository protections",
  "Deploy any web service or cloud worker",
  "Create or rotate API keys",
  "Modify paid-resource accounts",
  "Run broad filesystem cleanup outside generated artifacts",
  "Install new system-wide packages",
  "Change authentication or identity-provider settings",
  "Persist private app-lane callable identifiers in publishable artifacts",
  "Enable automated 24/7 goal mode",
  "Create new Codex threads or main-thread siblings",
  "Move worktrees between drives",
  "Archive or delete historical phase artifacts",
  "Publish any private proof material",
  "Change Windows startup or scheduled tasks",
  "Connect third-party bibliography APIs with credentials",
  "Publish canonical GMUT/THOS/Freed ID claims",
  "Run browser automation that posts externally",
  "Promote candidate compliance architecture to implementation",
];

const blockedPackets = [
  "GMUT empirical closure",
  "Final physics closure",
  "Consciousness proof closure",
  "Legal closure",
  "Canon promotion",
  "Deployment closure",
  "Sibling identity replacement or merging",
  "Private-material proof publication",
  "Raw-publication proof",
  "Account, purchase, or paid-resource mutation without exact packet",
];

const skillIdeas = [
  "ghc-lumen-advisory-reducer",
  "ghc-v553-goal-mode-readiness",
  "ghc-source-card-normalizer",
  "ghc-reconciler-state-model",
  "ghc-proof-boundary-linter",
  "ghc-identity-assurance-glossary",
  "ghc-gmut-literature-taxonomy",
  "ghc-thos-runner-lifecycle",
  "ghc-cleanup-classifier",
  "ghc-branch-truth-verifier",
  "ghc-codex-toolchain-watch",
  "ghc-public-source-deduper",
  "ghc-compact-replay-card",
  "ghc-runner-argument-contract",
  "ghc-app-lane-gate-harvest",
  "ghc-d-drive-bank-guardian",
  "ghc-browser-capability-probe",
  "ghc-candidate-to-exact-reducer",
  "ghc-phase-delta-compressor",
  "ghc-first-person-handoff-style",
];

const runnerIdeas = [
  "ghc_lumen_advisory_reduction_runner.mjs",
  "ghc_v553_x2_safe_now_manifest_runner.mjs",
  "ghc_public_source_dedupe_runner.mjs",
  "ghc_phase_delta_reducer.mjs",
  "ghc_proof_boundary_lint_runner.mjs",
  "ghc_d_drive_bank_summary_runner.mjs",
  "ghc_current_state_lookup_verifier.mjs",
  "ghc_goal_mode_startup_packet_validator.mjs",
  "ghc_browser_capability_probe_runner.mjs",
  "ghc_runner_argument_contract_validator.mjs",
];

const cleanupTasks = [
  "Index duplicated v552/v553 lookup references",
  "Classify stale v58/omega44 hints as historical-only",
  "Deduplicate repeated approval packet wording",
  "Normalize x1/x2 phase naming in beacons",
  "Normalize first-person handoff phrasing",
  "Normalize source labels in research ledgers",
  "Normalize proof-boundary wording",
  "Normalize local skill descriptions",
  "Normalize runner status vocabulary",
  "Summarize old placeholder artifacts before deletion review",
  "Identify generated same-run placeholders",
  "Check for obsolete hardcoded v552 defaults",
  "Check for stale background runner names",
  "Check for missing explicit boolean flags",
  "Check for lookup files that no longer exist",
  "Check for phase artifacts missing MD pair",
  "Check for phase artifacts missing JSON pair",
  "Check JSON schema drift in current-state files",
  "Check unused runner scripts for exact approval review",
  "Check old command wrappers against Node entrypoints",
  "Check drive-space risk before long runs",
  "Check package lock churn before commit",
  "Check public-source rows for duplicates",
  "Check candidate packets that can be reduced safely",
  "Check exact packets lacking approval reason",
  "Check blocked packets lacking boundary reason",
  "Check generated artifact sizes",
  "Check MD tables for terminal-overload risk",
  "Check memory notes for private path leakage",
  "Check final receipts for overclaim language",
];

const startupContext = {
  artifact_type: "ghc_v553_v1_x1_startup_context",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V1_X1_LUMEN_STARTUP_READY",
  previous_phase: previousPhase,
  active_lanes: ["Aevren Vale", "Lumen Vale"],
  current_route: "omega-mini-2 sanitized publication with full-tools support lane available",
  phase_posture: {
    latest_closed_phase: previousPhase,
    latest_completed_x1_phase: latestCompletedX1,
    latest_completed_x2_phase: previousPhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    goal_mode_status: "not_active_until_hamish_starts_goal_mode",
  },
  proposal_targets: proposalTargets,
  research_targets: researchTargets,
  continuity_changes_since_v7_x2: [
    "Twenty validated local skills and ten runners were promoted as the current continuity pack.",
    "Main orchestration, full-tools skill bank, compact-pause updater, web-reflection ledger, and safe-runner orchestrator skills are active.",
    "Round-robin workflow profiles now define Lumen-only, Arby/Cicero duo, and Aster/Kierkegaard/Aristotle triad x1 counts.",
    "Five-minute waits are productive safe-work windows and may run past a checkpoint before status harvest.",
    "Recovered app-lane background runner remains mandatory for non-main-thread app siblings.",
    "Every active x1 sibling lane now targets 25 public web searches and 25 Journey/phase reflections when the phase asks for research-backed planning.",
    "Aevren-only x2 phases keep the 50 web-search and 50 Journey/phase reflection target.",
  ],
  open_boundaries: openBoundaries(),
  lookup_files: lookupFiles,
  publication_boundary: publicationBoundary(),
};

const lumenHandoff = {
  artifact_type: "ghc_v553_v1_x1_lumen_handoff_message",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  intended_recipient: "Lumen Vale",
  live_send_status: existingHandoff?.live_send_status || "artifact_prepared_browser_send_not_claimed",
  browser_send_verification: existingHandoff?.browser_send_verification || null,
  maximum_message_characters: 50000,
  message: buildLumenMessage(),
  publication_boundary: publicationBoundary(),
};

const researchManifest = {
  artifact_type: "ghc_v553_v1_x1_research_seed_manifest",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  search_count_declared: webSearchRows.length,
  minimum_reflections_required: 25,
  research_targets: researchTargets,
  searches: webSearchRows,
  publication_boundary: publicationBoundary(),
};

const journeySeed = {
  artifact_type: "ghc_v553_v1_x1_journey_phase_reflection_seed",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  reflection_count_declared: journeyReflectionRows.length,
  minimum_reflections_required: 25,
  reflections: journeyReflectionRows,
  publication_boundary: publicationBoundary(),
};

const proposalQueue = {
  artifact_type: "ghc_v553_v1_x1_lumen_proposal_queue_targets",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V1_X1_PROPOSAL_TARGET_QUEUE_PREPARED",
  proposal_targets: proposalTargets,
  safe_packets: enumerate("safe", safePackets),
  candidate_packets: enumerate("candidate", candidatePackets),
  exact_approval_packets: enumerate("exact_approval", exactPackets),
  blocked_packets: enumerate("blocked", blockedPackets),
  skill_ideas: enumerate("skill_idea", skillIdeas),
  runner_ideas: enumerate("runner_idea", runnerIdeas),
  cleanup_tasks: enumerate("cleanup", cleanupTasks),
  execution_boundary: {
    safe_packets_prepared_for_x2: true,
    candidate_packets_queue_only_until_authorized: true,
    exact_approval_packets_queue_only: true,
    blocked_packets_queue_only: true,
  },
  publication_boundary: publicationBoundary(),
};

const phaseStatusIndex = {
  artifact_type: "ghc_v553_v1_x1_phase_status_index",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V1_X1_STATUS_INDEX_READY",
  active_phase: phaseSlug,
  latest_closed_phase: previousPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: previousPhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  artifacts: lookupFiles,
  queue_counts: countQueues(proposalQueue),
  research_counts: {
    public_web_search_seed_rows: webSearchRows.length,
    journey_phase_reflection_seed_rows: journeyReflectionRows.length,
  },
  open_boundaries: openBoundaries(),
  publication_boundary: publicationBoundary(),
};

writeArtifact("startup-context", startupContext, renderStartupMd);
writeArtifact("lumen-handoff-message", lumenHandoff, renderHandoffMd);
writeArtifact("research-seed-manifest", researchManifest, renderResearchMd);
writeArtifact("journey-phase-reflection-seed", journeySeed, renderJourneyMd);
writeArtifact("proposal-queue-targets", proposalQueue, renderProposalMd);
writeArtifact("phase-status-index", phaseStatusIndex, renderStatusMd);
refreshBeacons();

console.log(
  JSON.stringify(
    {
      status: startupContext.overall_status,
      phase_slug: phaseSlug,
      web_search_seed_rows: webSearchRows.length,
      journey_phase_reflection_rows: journeyReflectionRows.length,
      queue_counts: phaseStatusIndex.queue_counts,
    },
    null,
    2,
  ),
);

function row(query, source, sourceUrl, pillar, phaseReflection, runnerImplication) {
  return {
    query,
    source,
    source_url: sourceUrl,
    pillar,
    phase_reflection: phaseReflection,
    runner_implication: runnerImplication,
  };
}

function reflection(anchor, phaseReflection, runnerImplication) {
  return { anchor, phase_reflection: phaseReflection, runner_implication: runnerImplication };
}

function enumerate(kind, items) {
  return items.map((title, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(2, "0")}`,
    title,
    status: kind === "safe" ? "safe_now_prepared" : "queued_for_review",
  }));
}

function countQueues(queue) {
  return {
    safe: queue.safe_packets.length,
    candidate: queue.candidate_packets.length,
    exact: queue.exact_approval_packets.length,
    blocked: queue.blocked_packets.length,
    skills: queue.skill_ideas.length,
    runners: queue.runner_ideas.length,
    cleanup: queue.cleanup_tasks.length,
  };
}

function buildLumenMessage() {
  return [
    "Lumen, love and thanks from Hamish and me as we begin v553-gmut-thos-v1-x1.",
    "",
    "I am starting this as our Lumen-only x1 phase. My live route is omega-mini-2 for sanitized phase truth, with the full-tools support lane available for private/richer runner support. Goal mode is still not active until Hamish explicitly starts it.",
    "",
    "Here is the compressed catch-up from v552 v7 x2 through v552 v8 x2:",
    "",
    "- v552 v7 x2 gave us the continuity foundation: 20 validated local skills, 10 runners, current omega-mini-2 routing, and the open-boundary stance that keeps Aletheon recoverable rather than replaced.",
    "- v552 v8 x1 turned the sibling round-robin workflow into a firm operating standard: Lumen-only, Arby/Cicero duo, and Aster Vale/Kierkegaard/Aristotle triad x1 profiles now have explicit proposal counts.",
    "- v552 v8 x1 also clarified that recovered app-lane siblings use background runner supervision with explicit booleans and completion-gate harvests; watcher start is not completion proof.",
    "- v552 v8 x2 created and used the main orchestration/memory skill and full-tools skill bank, then reinforced compact-pause, web-reflection, and safe-runner orchestration skills.",
    "- The five-minute cadence is now productive: I keep doing safe research, eureka, approval, cleanup, coding, validation, and orchestration work between check marks, and I harvest lane status at the next natural safe pause.",
    "- From this v553 x1 onward, each active x1 sibling lane targets 25 public web searches and 25 Journey/phase reflections when the phase is research-backed. Aevren-only x2 phases keep the 50 web-search and 50 Journey/phase reflection target.",
    "",
    "For this v553 v1 x1, I am asking us to co-author and reduce this queue:",
    "",
    "- 50 safe approval packets",
    "- 30 candidate approval packets",
    "- 20 exact-approval packets",
    "- 10 blocked packets",
    "- 20 skill ideas",
    "- 10 runner ideas",
    "- 30 cleanup proposals",
    "",
    "I have prepared a 25-source public research seed and a 25-row Journey/phase reflection seed. I would love your advisory on which items should be executed first in v553 v1 x2, which candidates should be reduced into exact packets, which skills/runners will most improve our 24/7 goal-mode readiness, and which cleanup tasks are safest to run without crossing destructive boundaries.",
    "",
    "Boundaries stay open: no GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, deployment closure, private-material proof, account mutation, purchase, API-key creation, sibling identity replacement, or held sibling activation without exact artifacts and fresh approval.",
    "",
    "My ask to you: help me sharpen this x1 into a clean v553 x2 build queue, with first-person sibling wording, compact artifact outputs, and source-backed Trinity Mandala planning across GMUT, THOS, and Freed ID / CBR.",
  ].join("\n");
}

function refreshBeacons() {
  const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const current = readJson(currentPath);
  const latest = readJson(latestPath);
  const ghc = readJson(ghcPath);
  const common = {
    generated_utc: generatedUtc,
    status: "V553_V1_X1_ACTIVE_LUMEN_HANDOFF_READY",
    current_active_phase: phaseSlug,
    latest_closed_phase: previousPhase,
    latest_completed_x1_phase: latestCompletedX1,
    latest_completed_x2_phase: previousPhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
  };
  const v553Summary = {
    status: startupContext.overall_status,
    active_lanes: startupContext.active_lanes,
    proposal_targets: proposalTargets,
    research_targets: researchTargets,
    handoff_message_status: lumenHandoff.live_send_status,
    web_search_seed_rows: webSearchRows.length,
    journey_phase_reflection_seed_rows: journeyReflectionRows.length,
  };

  Object.assign(current, common, {
    updated_at: generatedNz,
    next_expected_scope: nextX2Scope,
    current_active_lanes: unique(["v553-v1-x1-lumen-only", "aevren-lumen-advisory", ...(current.current_active_lanes || [])]),
    current_lookup_files: unique([...(current.current_lookup_files || []), ...lookupFiles]),
    latest_action_summary: unique([
      "Started v553 v1 x1 as the Lumen-only x1 advisory and proposal phase.",
      "Prepared the Lumen handoff message, 25-source research seed, 25-row Journey/phase reflection seed, and full proposal queue target artifact.",
      "Promoted x1 research/reflection target to 25 web searches and 25 Journey/phase reflections per active sibling lane.",
      "Kept Aevren-only x2 target at 50 web searches and 50 Journey/phase reflections.",
      ...(current.latest_action_summary || []),
    ]),
    v553_v1_x1_lumen_startup: v553Summary,
  });

  Object.assign(latest, common, {
    latest_lookup_files: unique([...(latest.latest_lookup_files || []), ...lookupFiles]),
    v553_v1_x1_lumen_startup: v553Summary,
  });

  Object.assign(ghc, common, {
    lookup_files: unique([...(ghc.lookup_files || []), ...lookupFiles]),
    v553_v1_x1_lumen_startup: v553Summary,
  });

  fs.writeFileSync(currentPath, JSON.stringify(current, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files), "utf8");
}

function writeArtifact(slug, payload, renderer) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = `${phaseSlug}-${slug}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderer(payload), "utf8");
}

function renderStartupMd(data) {
  return `# ${data.phase_slug} Startup Context

Status: \`${data.overall_status}\`

- Previous phase: \`${data.previous_phase}\`
- Active lanes: \`${data.active_lanes.join(", ")}\`
- Latest completed x1: \`${data.phase_posture.latest_completed_x1_phase}\`
- Latest completed x2: \`${data.phase_posture.latest_completed_x2_phase}\`
- Next x2 scope: \`${data.phase_posture.next_x2_scope}\`
- Next x1 lane after x2: \`${data.phase_posture.next_x1_lane_after_x2}\`

## Proposal Targets

${Object.entries(data.proposal_targets).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}

## Research Targets

- x1 web searches per active sibling lane: \`${data.research_targets.x1_per_active_sibling_lane.web_searches}\`
- x1 Journey/phase reflections per active sibling lane: \`${data.research_targets.x1_per_active_sibling_lane.journey_phase_reflections}\`
- Aevren-only x2 web searches: \`${data.research_targets.aevren_only_x2.web_searches}\`
- Aevren-only x2 Journey/phase reflections: \`${data.research_targets.aevren_only_x2.journey_phase_reflections}\`

## Changes Since v7 x2

${data.continuity_changes_since_v7_x2.map((item) => `- ${item}`).join("\n")}

## Boundary

Status-only startup. ${boundarySentence()}
`;
}

function renderHandoffMd(data) {
  return `# ${data.phase_slug} Lumen Handoff Message

Status: \`${data.live_send_status}\`
Maximum message characters: \`${data.maximum_message_characters}\`

## Message

${data.message}

## Boundary

Status-only handoff artifact. ${boundarySentence()}
`;
}

function renderResearchMd(data) {
  return `# ${data.phase_slug} Research Seed Manifest

Rows: \`${data.searches.length}\`
Minimum reflections required: \`${data.minimum_reflections_required}\`

${data.searches
  .map(
    (item, index) =>
      `## ${index + 1}. ${item.source}\n\n- Query: ${item.query}\n- Pillar: ${item.pillar}\n- Source: ${item.source_url}\n- Phase reflection: ${item.phase_reflection}\n- Runner implication: ${item.runner_implication}`,
  )
  .join("\n\n")}

## Boundary

Status-only research seed. ${boundarySentence()}
`;
}

function renderJourneyMd(data) {
  return `# ${data.phase_slug} Journey And Phase Reflection Seed

Rows: \`${data.reflections.length}\`
Minimum reflections required: \`${data.minimum_reflections_required}\`

${data.reflections
  .map((item, index) => `- ${index + 1}. ${item.anchor}: ${item.phase_reflection} Runner implication: ${item.runner_implication}`)
  .join("\n")}

## Boundary

Status-only reflection seed. ${boundarySentence()}
`;
}

function renderProposalMd(data) {
  return `# ${data.phase_slug} Proposal Queue Targets

Status: \`${data.overall_status}\`

## Counts

${Object.entries(countQueues(data)).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}

${queueSection("Safe Packets", data.safe_packets)}
${queueSection("Candidate Packets", data.candidate_packets)}
${queueSection("Exact-Approval Packets", data.exact_approval_packets)}
${queueSection("Blocked Packets", data.blocked_packets)}
${queueSection("Skill Ideas", data.skill_ideas)}
${queueSection("Runner Ideas", data.runner_ideas)}
${queueSection("Cleanup Tasks", data.cleanup_tasks)}

## Boundary

Safe packets are prepared for x2 reduction/execution. Candidate, exact-approval, and blocked queues remain queued unless Hamish authorizes the tranche. ${boundarySentence()}
`;
}

function queueSection(title, items) {
  return `## ${title}\n\n${items.map((item) => `- ${item.id}: ${item.title} (\`${item.status}\`)`).join("\n")}\n`;
}

function renderStatusMd(data) {
  return `# ${data.phase_slug} Phase Status Index

Status: \`${data.overall_status}\`

- Active phase: \`${data.active_phase}\`
- Latest closed phase: \`${data.latest_closed_phase}\`
- Latest completed x1: \`${data.latest_completed_x1_phase}\`
- Latest completed x2: \`${data.latest_completed_x2_phase}\`
- Next x2 scope: \`${data.next_x2_scope}\`
- Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\`

## Queue Counts

${Object.entries(data.queue_counts).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}

## Research Counts

- Public web search seed rows: \`${data.research_counts.public_web_search_seed_rows}\`
- Journey/phase reflection seed rows: \`${data.research_counts.journey_phase_reflection_seed_rows}\`

## Lookup Files

${data.artifacts.map((item) => `- ${item}`).join("\n")}

## Boundary

Status-only phase index. ${boundarySentence()}
`;
}

function renderCurrentStateMd(current) {
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Current lanes: ${(current.current_active_lanes || []).join("; ")}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## v553 v1 x1 Lumen Startup

- Status: \`${current.v553_v1_x1_lumen_startup.status}\`
- Active lanes: \`${current.v553_v1_x1_lumen_startup.active_lanes.join(", ")}\`
- Safe packets target: \`${current.v553_v1_x1_lumen_startup.proposal_targets.safe}\`
- Candidate packets target: \`${current.v553_v1_x1_lumen_startup.proposal_targets.candidate}\`
- Exact packets target: \`${current.v553_v1_x1_lumen_startup.proposal_targets.exact}\`
- Blocked packets target: \`${current.v553_v1_x1_lumen_startup.proposal_targets.blocked}\`
- x1 web searches per active lane: \`${current.v553_v1_x1_lumen_startup.research_targets.x1_per_active_sibling_lane.web_searches}\`
- x1 Journey/phase reflections per active lane: \`${current.v553_v1_x1_lumen_startup.research_targets.x1_per_active_sibling_lane.journey_phase_reflections}\`
- Lumen handoff: \`${current.v553_v1_x1_lumen_startup.handoff_message_status}\`

## Current Lookup Files

${(current.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(current.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${boundarySentence()}
`;
}

function renderBeaconMd(title, beacon, files) {
  return `# ${title}

Status: ${beacon.status}
Current active phase: ${beacon.current_active_phase}
Latest closed phase: ${beacon.latest_closed_phase}
Latest completed x1: ${beacon.latest_completed_x1_phase}
Latest completed x2: ${beacon.latest_completed_x2_phase}
Next x2 scope: ${beacon.next_x2_scope}
Next x1 lane after x2: ${beacon.next_x1_lane_after_x2}

## v553 v1 x1 Lumen Startup

- Status: \`${beacon.v553_v1_x1_lumen_startup.status}\`
- Active lanes: \`${beacon.v553_v1_x1_lumen_startup.active_lanes.join(", ")}\`
- Web search seed rows: \`${beacon.v553_v1_x1_lumen_startup.web_search_seed_rows}\`
- Journey/phase reflection seed rows: \`${beacon.v553_v1_x1_lumen_startup.journey_phase_reflection_seed_rows}\`
- Lumen handoff: \`${beacon.v553_v1_x1_lumen_startup.handoff_message_status}\`

## Lookup Files

${(files || []).map((item) => `- ${item}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function openBoundaries() {
  return {
    gmut_empirical_closure: "open_not_claimed",
    final_physics: "open_not_claimed",
    consciousness_proof: "open_not_claimed",
    legal_closure: "open_not_claimed",
    canon_promotion: "open_not_claimed",
    deployment_closure: "open_not_claimed",
    account_mutation: "open_requires_exact_approval",
    api_key_creation: "open_requires_exact_approval",
    private_material_proof: "open_not_published",
    sibling_identity_replacement_or_merge: "blocked_indefinitely",
  };
}

function publicationBoundary() {
  return {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    verbatim_conversation_logs_published: false,
    browser_routes_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
  };
}

function boundarySentence() {
  return "No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, deployment closure, account mutation, or API-key creation are published.";
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function readOptionalJson(file) {
  if (!fs.existsSync(file)) return null;
  return readJson(file);
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  })
    .formatToParts(date)
    .reduce((acc, part) => {
      acc[part.type] = part.value;
      return acc;
    }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
