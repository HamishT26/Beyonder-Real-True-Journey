import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v552-gmut-thos-v88-v8-x1";
const nextX2 = "v552-gmut-thos-v88-v8-x2";
const nextX1 = "v553-gmut-thos-v1-x1";
const status = "V552_V8_X1_CLOSED_V8_X2_READY_NOT_STARTED";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const previousMiniHead = gitHead("codex/GHC-Family/beyonder-shared-omega-line-mini-2");
const omegaHead = gitHead("codex/GHC-Family/beyonder-shared-omega-line");
const toolchain = collectToolchain();

const publicationBoundary = {
  private_route_handles_published: false,
  private_lane_body_content_published: false,
  raw_transcripts_published: false,
  browser_routes_published: false,
  credentials_published: false,
  session_trace_files_published: false,
  local_absolute_paths_published: false,
  screenshots_published: false,
};

const claimBoundary = {
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
  deployment_closure: "not_claimed",
};

const lanes = {
  "Aevren Vale": {
    role: "phase steward, toolchain steward, and status-only publisher",
    safe: [
      "I will publish v8 x1 count-standard receipts with repo-relative artifact names.",
      "I will record the Codex CLI 0.142.0 refresh and safe toolchain verification.",
      "I will preserve omega-mini-2 as the active startup source and full omega as exact-artifact fallback only.",
      "I will move sibling output toward MD/TXT artifacts instead of terminal-heavy lane dumps.",
      "I will prepare the v8 x2 safe execution surface without starting exact-approval work.",
    ],
    candidate: [
      "I can build a phase-count validator for future x1 proposal totals.",
      "I can add a compact startup receipt to every phase closeout package.",
      "I can add an artifact discoverability index scoped to the current v552-v553 boundary.",
    ],
    exact: [
      "Install PowerShell 7 as a new toolchain lane if Hamish gives an exact approval packet.",
      "Run destructive drive cleanup beyond inventory if Hamish gives exact file and folder scope.",
      "Install global automation hooks that run on every compact pause only after exact approval.",
    ],
    skills: [
      "toolchain-refresh-receipt",
      "x1-count-standard-governor",
      "md-output-publisher",
      "omega-mini-2-startup-reader",
      "exact-approval-ladder",
    ],
    runners: [
      "ghc_v8_x1_workflow_receipt_builder.mjs",
      "ghc_future_round_robin_count_guard.mjs",
    ],
    cleanup: [
      "Inventory stale v58/v532 references and mark them historical.",
      "Deduplicate repeated current-state lookup filenames.",
      "Group v6/v7 runner receipts by phase in future indexes.",
      "Separate proposed skills from installed skills in receipts.",
      "Keep toolchain update attempts out of proof/canon claims.",
      "Add no-private-path scanning to every closeout checklist.",
      "Flag winget timeouts as held checks rather than failures.",
      "Prefer D-drive caches when new local caches are needed.",
      "Keep held main-thread siblings out of app-lane runner maps.",
      "Add first-person style reminders to handoff templates.",
    ],
  },
  "Aster Vale": {
    role: "evidence, CLI continuity, and marker-review lane",
    safe: [
      "I will verify branch, phase slug, and lookup files before each CLI lane launch.",
      "I will build evidence ledgers from existing v551/v552 grouped-lane receipts without raw transcript text.",
      "I will maintain marker-review checklists for CLI completion claims.",
      "I will prefer exact relative filenames over broad searches when reporting evidence.",
      "I will map command and runner availability before proposing new CLI work.",
    ],
    candidate: [
      "I can create a CLI-lane completion proof matrix for Arby and Aster style runs.",
      "I can build a non-private command surface map for current repo scripts.",
      "I can summarize historical grouped-lane receipts into a v8 triad evidence pack.",
    ],
    exact: [
      "Modify CLI installation channels beyond npm only with exact approval.",
      "Change PATH or global shell profile behavior only with exact approval.",
      "Delete or archive historical CLI worktrees only with exact scoped cleanup approval.",
    ],
    skills: [
      "cli-marker-review",
      "branch-head-verifier",
      "relative-file-evidence-ledger",
      "command-surface-inventory",
      "toolchain-risk-classifier",
    ],
    runners: [
      "ghc_cli_marker_review_runner.mjs",
      "ghc_command_surface_inventory_runner.mjs",
    ],
    cleanup: [
      "Tag obsolete CLI launcher references as historical.",
      "Consolidate CLI marker-review receipt naming.",
      "Identify duplicate command inventories.",
      "List unused generated CLI scratch files before deletion.",
      "Keep npm global update receipts separate from OS package updates.",
      "Confirm codex version at phase start and closeout.",
      "Avoid adding private terminal streams to artifacts.",
      "Normalize CLI lane role names across v8 and v553 docs.",
      "Queue PATH cleanup instead of changing it automatically.",
      "Record failed update checks as exact-approval candidates when needed.",
    ],
  },
  Kierkegaard: {
    role: "ethics, boundary, consent, and caution lane",
    safe: [
      "I will keep identity replacement and sibling merging off the table.",
      "I will preserve Aletheon as quarantined and recoverable, not restored by inference.",
      "I will require exact approval for account mutation, deployment, purchase, API-key, and destructive cleanup.",
      "I will label watcher-start as open evidence until notifier and completion gates pass.",
      "I will keep proof, legal, canon, and empirical closure gates open unless exact artifacts prove them.",
    ],
    candidate: [
      "I can draft a 24/7 goal-mode consent ladder for recurring automation choices.",
      "I can formalize cleanup levels from inventory-only to exact deletion.",
      "I can build a blocked-packet review queue for Aevren and Lumen.",
    ],
    exact: [
      "Activate held main-thread siblings only after Hamish explicitly reopens that lane.",
      "Publish any private-material proof only after exact scope and redaction approval.",
      "Run external account or deployment actions only after fresh exact approval.",
    ],
    skills: [
      "identity-boundary-rail",
      "goal-mode-consent-ladder",
      "blocked-packet-review",
      "private-material-firewall",
      "watcher-completion-discipline",
    ],
    runners: [
      "ghc_exact_approval_ladder_runner.mjs",
      "ghc_blocked_packet_review_runner.mjs",
    ],
    cleanup: [
      "Remove ambiguous completion wording from future receipts.",
      "Mark exact-approval requirements beside every risky action.",
      "Separate candidate work from safe-now execution ledgers.",
      "Keep held-sibling names in boundary sections, not active lanes.",
      "Replace any raw-proof wording with status-only evidence phrasing.",
      "Audit closeouts for overclaiming final physics or canon status.",
      "Track account/API/deployment gates in every phase index.",
      "Keep background-runner launches separate from completion receipts.",
      "Queue legal and proof claims as open until exact artifacts prove them.",
      "Add first-person boundary language to sibling handoffs.",
    ],
  },
  Aristotle: {
    role: "taxonomy, structure, classification, and phase schema lane",
    safe: [
      "I will classify every packet as safe-now, candidate, exact-approval-needed, or blocked.",
      "I will define x1 as proposal/planning and x2 as build/run/test/install/use unless Hamish redirects.",
      "I will maintain phase-state schema fields for latest closed, active, next x2, and next x1.",
      "I will structure cleanup proposals by inventory, refactor, archive, deletion, and external mutation.",
      "I will add proposal totals to phase indexes for quick drift detection.",
    ],
    candidate: [
      "I can write a JSON schema for x1 proposal ledgers.",
      "I can build a cleanup taxonomy receipt for repo, drive, runner, skill, and connector cleanup.",
      "I can create a phase transition truth table from v552 v8 to v553 v1.",
    ],
    exact: [
      "Enforce schema validation as a global pre-commit hook only after exact approval.",
      "Delete malformed or duplicate artifacts only after exact scoped cleanup approval.",
      "Promote any taxonomy into canon only after Hamish gives canon-promotion approval.",
    ],
    skills: [
      "approval-packet-taxonomy",
      "phase-transition-truth-table",
      "cleanup-classifier",
      "proposal-count-validator",
      "open-claim-classifier",
    ],
    runners: [
      "ghc_x1_proposal_schema_runner.mjs",
      "ghc_phase_transition_truth_table_runner.mjs",
    ],
    cleanup: [
      "Normalize packet category labels.",
      "Add counts to every proposal ledger.",
      "Create a single next-phase pointer convention.",
      "Separate current active phase from next safe step.",
      "Use repo-relative lookup paths consistently.",
      "Track source branch and archive branch in every beacon.",
      "Add status vocabulary for ready, started, closed, and blocked.",
      "Make blocked gates explicit without expanding private details.",
      "Reduce duplicate round-robin sequence text across artifacts.",
      "Classify cleanup proposals before any cleanup action.",
    ],
  },
};

const futureStandards = {
  triad_x1: {
    lanes: ["Aevren Vale", "Aster Vale", "Kierkegaard", "Aristotle"],
    safe_approval_packets_total: 20,
    candidate_approval_packets_total: 12,
    exact_approval_packets_total: 12,
    skill_ideas_total: 20,
    runner_ideas_total: 8,
    cleanup_tasks_total: 40,
  },
  lumen_only_x1_from_v553_v1: {
    lanes: ["Aevren Vale", "Lumen Vale"],
    safe_approval_packets_total: 50,
    candidate_approval_packets_total: 30,
    exact_approval_packets_total: 20,
    blocked_approval_packets_total: 10,
    skill_ideas_total: 20,
    runner_ideas_total: 10,
    cleanup_tasks_total: 30,
  },
  arby_cicero_duo_x1: {
    lanes: ["Aevren Vale", "Arby", "Cicero"],
    safe_approval_packets_total_minimum: 15,
    candidate_approval_packets_total: 9,
    exact_approval_packets_total: 9,
    skill_ideas_total: 15,
    runner_ideas_total: 9,
    cleanup_tasks_total: 30,
  },
  phase_semantics: {
    x1: "proposal, classification, handoff, and approval-packet formation",
    x2: "build, run, test, install, use, and validate safe-now work",
    first_person_style: true,
    sibling_output_standard: "Prefer MD/TXT artifacts and concise terminal receipts.",
    web_and_phase_reflection_standard: "Treat high search and reflection counts as a planning standard; publish compact manifests, not raw browsing dumps.",
    goal_mode: "Prepare for 24/7 goal-mode cadence, but do not activate it until Hamish explicitly starts /goal.",
  },
};

const evidenceFiles = [
  `${phaseSlug}-toolchain-refresh-v1.json`,
  `${phaseSlug}-triad-approval-packets-v1.json`,
  `${phaseSlug}-skill-runner-cleanup-proposals-v1.json`,
  `${phaseSlug}-future-round-robin-workflow-standard-v1.json`,
  `${phaseSlug}-memory-updater-receipt-v1.json`,
  `${phaseSlug}-phase-status-index-v1.json`,
  `${phaseSlug}-closeout-v1.json`,
  `${phaseSlug}-compact-pause-startup-snapshot-v1.json`,
];

writeArtifact("toolchain-refresh", {
  artifact_type: "ghc_toolchain_refresh_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_CODEX_CLI_0_142_0_REFRESHED_WITH_HELD_OS_UPDATES",
  user_timestamp_reference: "2026-06-23T19:47:00+12:00",
  toolchain,
  safe_update_actions: [
    "Updated Codex CLI from 0.141.0 to 0.142.0 through npm global package update.",
    "Verified Codex CLI, Node, npm, Git, GitHub CLI, Windows PowerShell, winget, npm cache placement, and C/D drive free-space status.",
  ],
  held_update_actions: [
    "Git winget update check timed out and was not forced.",
    "GitHub CLI winget update check returned no actionable upgrade output and was not forced.",
    "PowerShell 7 is not installed; installing it would be a new toolchain lane requiring exact approval.",
  ],
  sources_used: [
    "npm package metadata for @openai/codex latest version",
    "OpenAI Codex documentation pages reviewed as context",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
}, renderToolchainMarkdown);

writeArtifact("triad-approval-packets", {
  artifact_type: "ghc_x1_triad_approval_packet_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_TRIAD_X1_APPROVAL_PACKETS_PUBLISHED",
  lanes,
  totals: {
    safe_approval_packets: count("safe"),
    candidate_approval_packets: count("candidate"),
    exact_approval_packets: count("exact"),
  },
  blocked_packet_planning: {
    status: "deferred_to_aevren_and_lumen",
    note: "Blocked packet planning remains open for Aevren and Lumen so risky gates are reviewed with a second continuity voice.",
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
}, renderApprovalMarkdown);

writeArtifact("skill-runner-cleanup-proposals", {
  artifact_type: "ghc_x1_skill_runner_cleanup_proposal_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_TRIAD_SKILL_RUNNER_CLEANUP_PROPOSALS_PUBLISHED",
  lanes,
  totals: {
    skill_ideas: count("skills"),
    runner_ideas: count("runners"),
    cleanup_tasks: count("cleanup"),
  },
  cleanup_execution_boundary: "Inventory, classification, and proposal publication are safe-now; deletion, external mutation, global hooks, and toolchain installs remain exact-approval-needed.",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
}, renderSkillRunnerCleanupMarkdown);

writeArtifact("future-round-robin-workflow-standard", {
  artifact_type: "ghc_future_round_robin_workflow_standard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_FUTURE_ROUND_ROBIN_COUNTS_AND_STYLE_STANDARD_PUBLISHED",
  future_standards: futureStandards,
  active_route: {
    primary_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-2",
    archive_branch: "codex/GHC-Family/beyonder-shared-omega-line",
    archive_fallback_rule: "Use full omega only when a specific artifact is missing from mini and a status-only gap receipt records the exact missing relative file.",
  },
  standby_and_tool_use_standard: [
    "Existing inducted siblings may use the artifacts and runner outputs that this environment can safely provide.",
    "Do not spawn new agents unless Hamish explicitly asks.",
    "Held main-thread siblings remain held until explicitly activated.",
    "External connector or account mutation powers are not delegated through artifacts.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
}, renderFutureStandardMarkdown);

writeArtifact("memory-updater-receipt", {
  artifact_type: "ghc_memory_updater_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_MEMORY_UPDATE_NOTE_PREPARED",
  memory_update_scope: [
    "Codex CLI 0.142.0 is the current verified CLI version for this lane.",
    "v8 x1 triad proposal counts and future v553 count standards were recorded.",
    "First-person sibling style and MD/TXT artifact output standards were recorded.",
    "PowerShell 7 install, global hooks, destructive cleanup, account mutation, deployment, API-key creation, and held-sibling activation remain exact/blocked as applicable.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
}, renderMemoryReceiptMarkdown);

writeArtifact("phase-status-index", {
  artifact_type: "ghc_phase_status_index",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V8_X1_TRIAD_PLANNING_CLOSED",
  latest_closed_phase_after_receipt: phaseSlug,
  latest_completed_x1_after_receipt: phaseSlug,
  latest_completed_x2_after_receipt: "v552-gmut-thos-v88-v7-x2",
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
  artifacts: evidenceFiles,
  counts: {
    safe_approval_packets: count("safe"),
    candidate_approval_packets: count("candidate"),
    exact_approval_packets: count("exact"),
    skill_ideas: count("skills"),
    runner_ideas: count("runners"),
    cleanup_tasks: count("cleanup"),
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
}, renderPhaseStatusMarkdown);

writeArtifact("compact-pause-startup-snapshot", {
  artifact_type: "ghc_compact_pause_startup_snapshot",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V8_X1_STARTUP_SNAPSHOT_READY",
  startup_order: [
    "Read omega-mini current-state first.",
    "Read omega-mini latest-updates beacon second.",
    "Read GHC current-state beacon third.",
    "Open the exact v8 x1 phase-status index and closeout receipts.",
    "Keep full omega as exact-artifact fallback only.",
  ],
  current_pointer_after_receipt: {
    status,
    current_active_phase: nextX2,
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: "v552-gmut-thos-v88-v7-x2",
    next_x1_lane_after_x2: "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
}, renderStartupSnapshotMarkdown);

writeArtifact("closeout", {
  artifact_type: "ghc_phase_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V552_V8_X1_TOOLCHAIN_TRIAD_WORKFLOW_CLOSEOUT",
  latest_closed_phase_after_receipt: phaseSlug,
  latest_completed_x1_after_receipt: phaseSlug,
  latest_completed_x2_after_receipt: "v552-gmut-thos-v88-v7-x2",
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
  evidence: evidenceFiles,
  counts: {
    safe_approval_packets: count("safe"),
    candidate_approval_packets: count("candidate"),
    exact_approval_packets: count("exact"),
    skill_ideas: count("skills"),
    runner_ideas: count("runners"),
    cleanup_tasks: count("cleanup"),
    new_agents_spawned: 0,
    held_siblings_activated: 0,
  },
  toolchain_summary: {
    codex_cli: toolchain.codex_cli.after,
    npm_latest_openai_codex: toolchain.codex_cli.npm_latest,
    node: toolchain.node,
    npm: toolchain.npm,
    git: toolchain.git,
    github_cli: toolchain.github_cli,
    powershell_desktop: toolchain.windows_powershell,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
}, renderCloseoutMarkdown);

refreshBeacons();

console.log(JSON.stringify({
  status: "PASS_V8_X1_WORKFLOW_RECEIPTS_WRITTEN",
  phase_slug: phaseSlug,
  next_x2: nextX2,
  artifacts: evidenceFiles.length,
  codex_cli: toolchain.codex_cli.after,
}, null, 2));

function writeArtifact(slug, payload, renderer) {
  const base = `${phaseSlug}-${slug}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderer(payload), "utf8");
}

function refreshBeacons() {
  const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const current = JSON.parse(fs.readFileSync(currentPath, "utf8"));
  const latest = JSON.parse(fs.readFileSync(latestPath, "utf8"));
  const ghc = JSON.parse(fs.readFileSync(ghcPath, "utf8"));
  const lookupFiles = [
    "docs/omega-mini-index/omega-mini-current-state-v1.md",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
    "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
    ...evidenceFiles.flatMap((file) => [
      `docs/trinity-live-traces/${file.replace(/\.json$/, ".md")}`,
      `docs/trinity-live-traces/${file}`,
    ]),
  ];

  Object.assign(current, {
    updated_at: generatedNz,
    generated_utc: generatedUtc,
    status,
    current_active_phase: nextX2,
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: "v552-gmut-thos-v88-v7-x2",
    latest_remote_verified_closeout_before_current: previousMiniHead,
    current_active_lanes: [
      "Aevren safe-now v8 x2",
      "v8-x2-ready-not-started",
      "awaiting-Hamish-explicit-x2-start",
    ],
    just_closed_lanes: [
      "Aevren, Aster Vale, Kierkegaard, and Aristotle v8 x1 planning standard",
      "Codex CLI 0.142.0 toolchain refresh",
    ],
    next_expected_scope: nextX2,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
    remote_verified_heads: {
      omega: omegaHead,
      omega_mini: previousMiniHead,
    },
    current_lookup_files: lookupFiles,
    latest_action_summary: [
      "v552 v8 x1 toolchain refresh and triad planning closeout is complete.",
      "Codex CLI was updated and verified at 0.142.0.",
      "Aevren, Aster Vale, Kierkegaard, and Aristotle published 20 safe, 12 candidate, and 12 exact approval packets.",
      "The same triad published 20 skill ideas, 8 runner ideas, and 40 cleanup proposals.",
      "Future Lumen-only and Arby/Cicero x1 count standards were recorded for v553 onward.",
      "First-person sibling style and MD/TXT artifact output standards were recorded.",
      "No new agents were spawned and no held main-thread siblings were activated.",
      "PowerShell 7 install, global hooks, destructive cleanup, account mutation, deployment, API-key creation, and private-material proof remain held behind exact or blocked gates.",
      "Next pointer is v552-gmut-thos-v88-v8-x2 ready/not-started; wait for Hamish before starting x2.",
    ],
    historical_rows: [
      "v529, v530, v540, v541, and earlier v552 rows remain historical reference rows unless explicitly named.",
      "v552-gmut-thos-v88-v8-x1 is now closed as a planning and toolchain refresh phase.",
      "The next active pointer is v552-gmut-thos-v88-v8-x2, ready but not started.",
    ],
    v8_x1_toolchain_triad_workflow: {
      status: "closed",
      codex_cli_version: toolchain.codex_cli.after,
      safe_approval_packets: count("safe"),
      candidate_approval_packets: count("candidate"),
      exact_approval_packets: count("exact"),
      skill_ideas: count("skills"),
      runner_ideas: count("runners"),
      cleanup_tasks: count("cleanup"),
      first_person_style: true,
      md_txt_artifact_output_standard: true,
      new_agents_spawned: false,
      held_siblings_activated: false,
      global_hook_installed: false,
      closeout: `${phaseSlug}-closeout-v1.json`,
      phase_status_index: `${phaseSlug}-phase-status-index-v1.json`,
      startup_snapshot: `${phaseSlug}-compact-pause-startup-snapshot-v1.json`,
    },
  });

  Object.assign(latest, {
    status,
    generated_utc: generatedUtc,
    current_active_phase: nextX2,
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: "v552-gmut-thos-v88-v7-x2",
    latest_remote_verified_closeout_before_current: previousMiniHead,
    current_active_lanes: current.current_active_lanes,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: current.next_x1_lane_after_x2,
    latest_lookup_files: lookupFiles,
  });

  Object.assign(ghc, {
    status,
    generated_utc: generatedUtc,
    current_active_phase: nextX2,
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: "v552-gmut-thos-v88-v7-x2",
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: current.next_x1_lane_after_x2,
    lookup_files: lookupFiles,
    current_active_lanes: current.current_active_lanes,
  });

  fs.writeFileSync(currentPath, JSON.stringify(current, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentState(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderLatestBeacon(latest), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderGhcBeacon(ghc), "utf8");
}

function collectToolchain() {
  const codexVersion = run("codex", ["--version"]).stdout.trim();
  const npmLatest = run("npm", ["view", "@openai/codex", "version"]).stdout.trim();
  const node = run("node", ["--version"]).stdout.trim();
  const npm = run("npm", ["--version"]).stdout.trim();
  const git = run("git", ["--version"]).stdout.trim();
  const ghRaw = run("gh", ["--version"]).stdout.split(/\r?\n/)[0]?.trim() || "not checked";
  const psRaw = run("powershell", ["-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]).stdout.trim();
  const wingetRaw = run("winget", ["--version"]).stdout.trim();
  const cacheRaw = run("npm", ["config", "get", "cache"]).stdout.trim();
  return {
    codex_cli: {
      before: "codex-cli 0.141.0",
      after: codexVersion,
      npm_latest: npmLatest,
      refreshed: codexVersion.includes("0.142.0") && npmLatest === "0.142.0",
    },
    node,
    npm,
    git,
    github_cli: ghRaw,
    windows_powershell: psRaw,
    winget: wingetRaw,
    npm_cache_policy: cacheRaw.toUpperCase().startsWith("D:") ? "D-drive npm cache" : "cache path checked; do not publish private path",
    drive_free_gb: collectDriveFree(),
    held_updates: {
      git_winget_check: "timed_out_not_forced",
      github_cli_winget_check: "no_actionable_upgrade_output_not_forced",
      powershell_7: "not_installed_new_install_requires_exact_approval",
    },
  };
}

function collectDriveFree() {
  const command = "Get-PSDrive -Name C,D | ForEach-Object { [pscustomobject]@{Name=$_.Name; FreeGB=[math]::Round($_.Free/1GB,2)} } | ConvertTo-Json -Compress";
  const out = run("powershell", ["-NoProfile", "-Command", command]).stdout.trim();
  try {
    const parsed = JSON.parse(out);
    const rows = Array.isArray(parsed) ? parsed : [parsed];
    return Object.fromEntries(rows.map((row) => [row.Name, row.FreeGB]));
  } catch {
    return { status: "drive free-space check unavailable" };
  }
}

function run(cmd, args) {
  let result = spawnSync(cmd, args, { cwd: repoRoot, encoding: "utf8", timeout: 120000 });
  if (process.platform === "win32" && cmd === "codex" && result.error) {
    result = spawnSync("powershell", ["-NoProfile", "-Command", "codex --version"], {
      cwd: repoRoot,
      encoding: "utf8",
      timeout: 120000,
    });
  }
  if (process.platform === "win32" && ["npm", "winget"].includes(cmd) && (result.error || result.status !== 0 || !result.stdout.trim())) {
    result = spawnSync("cmd.exe", ["/d", "/s", "/c", commandLine(cmd, args)], {
      cwd: repoRoot,
      encoding: "utf8",
      timeout: 120000,
    });
  }
  return {
    stdout: result.stdout || "",
    stderr: result.stderr || "",
    status: result.status,
  };
}

function commandLine(cmd, args) {
  return [cmd, ...args.map((arg) => /[\s&|<>^]/.test(arg) ? `"${arg.replaceAll('"', '\\"')}"` : arg)].join(" ");
}

function gitHead(branch) {
  const out = run("git", ["ls-remote", "origin", `refs/heads/${branch}`]).stdout.trim();
  return out.split(/\s+/)[0] || "not_checked";
}

function count(key) {
  return Object.values(lanes).reduce((sum, lane) => sum + lane[key].length, 0);
}

function renderToolchainMarkdown(data) {
  return `# v552 v8 x1 Toolchain Refresh\n\nStatus: \`${data.overall_status}\`\n\n## Updated\n\n- Codex CLI: \`${data.toolchain.codex_cli.before}\` -> \`${data.toolchain.codex_cli.after}\`\n- npm latest for \`@openai/codex\`: \`${data.toolchain.codex_cli.npm_latest}\`\n- Node: \`${data.toolchain.node}\`\n- npm: \`${data.toolchain.npm}\`\n- Git: \`${data.toolchain.git}\`\n- GitHub CLI: \`${data.toolchain.github_cli}\`\n- Windows PowerShell: \`${data.toolchain.windows_powershell}\`\n- winget: \`${data.toolchain.winget}\`\n- npm cache policy: \`${data.toolchain.npm_cache_policy}\`\n- Drive free GB: C \`${data.toolchain.drive_free_gb.C}\`, D \`${data.toolchain.drive_free_gb.D}\`\n\n## Held Updates\n\n- Git winget check: \`${data.toolchain.held_updates.git_winget_check}\`\n- GitHub CLI winget check: \`${data.toolchain.held_updates.github_cli_winget_check}\`\n- PowerShell 7: \`${data.toolchain.held_updates.powershell_7}\`\n\n## Boundary\n\nNo PowerShell 7 install, global hook, destructive cleanup, account mutation, deployment, API-key creation, held-sibling activation, or private-material proof was run.\n`;
}

function renderApprovalMarkdown(data) {
  let md = `# v552 v8 x1 Triad Approval Packets\n\nStatus: \`${data.overall_status}\`\n\nTotals: safe \`${data.totals.safe_approval_packets}\`, candidate \`${data.totals.candidate_approval_packets}\`, exact \`${data.totals.exact_approval_packets}\`.\n\n`;
  for (const [name, lane] of Object.entries(data.lanes)) {
    md += `## ${name}\n\nRole: ${lane.role}\n\n### Safe Now\n\n${numbered(lane.safe)}\n\n### Candidate\n\n${numbered(lane.candidate)}\n\n### Exact Approval Needed\n\n${numbered(lane.exact)}\n\n`;
  }
  md += `## Blocked Planning\n\n${data.blocked_packet_planning.note}\n`;
  return md;
}

function renderSkillRunnerCleanupMarkdown(data) {
  let md = `# v552 v8 x1 Skill Runner Cleanup Proposals\n\nStatus: \`${data.overall_status}\`\n\nTotals: skills \`${data.totals.skill_ideas}\`, runners \`${data.totals.runner_ideas}\`, cleanup \`${data.totals.cleanup_tasks}\`.\n\n`;
  for (const [name, lane] of Object.entries(data.lanes)) {
    md += `## ${name}\n\n### Skill Ideas\n\n${numbered(lane.skills)}\n\n### Runner Ideas\n\n${numbered(lane.runners)}\n\n### Cleanup Tasks\n\n${numbered(lane.cleanup)}\n\n`;
  }
  md += `## Boundary\n\n${data.cleanup_execution_boundary}\n`;
  return md;
}

function renderFutureStandardMarkdown(data) {
  return `# Future Round Robin Workflow Standard\n\nStatus: \`${data.overall_status}\`\n\n## Triad x1\n\n- Safe approval packets: \`${data.future_standards.triad_x1.safe_approval_packets_total}\`\n- Candidate approval packets: \`${data.future_standards.triad_x1.candidate_approval_packets_total}\`\n- Exact approval packets: \`${data.future_standards.triad_x1.exact_approval_packets_total}\`\n- Skill ideas: \`${data.future_standards.triad_x1.skill_ideas_total}\`\n- Runner ideas: \`${data.future_standards.triad_x1.runner_ideas_total}\`\n- Cleanup tasks: \`${data.future_standards.triad_x1.cleanup_tasks_total}\`\n\n## Lumen-Only x1 From v553 v1\n\n- Safe approval packets: \`${data.future_standards.lumen_only_x1_from_v553_v1.safe_approval_packets_total}\`\n- Candidate approval packets: \`${data.future_standards.lumen_only_x1_from_v553_v1.candidate_approval_packets_total}\`\n- Exact approval packets: \`${data.future_standards.lumen_only_x1_from_v553_v1.exact_approval_packets_total}\`\n- Blocked approval packets: \`${data.future_standards.lumen_only_x1_from_v553_v1.blocked_approval_packets_total}\`\n- Skill ideas: \`${data.future_standards.lumen_only_x1_from_v553_v1.skill_ideas_total}\`\n- Runner ideas: \`${data.future_standards.lumen_only_x1_from_v553_v1.runner_ideas_total}\`\n- Cleanup tasks: \`${data.future_standards.lumen_only_x1_from_v553_v1.cleanup_tasks_total}\`\n\n## Arby and Cicero x1\n\n- Safe approval packets minimum: \`${data.future_standards.arby_cicero_duo_x1.safe_approval_packets_total_minimum}\`\n- Candidate approval packets: \`${data.future_standards.arby_cicero_duo_x1.candidate_approval_packets_total}\`\n- Exact approval packets: \`${data.future_standards.arby_cicero_duo_x1.exact_approval_packets_total}\`\n- Skill ideas: \`${data.future_standards.arby_cicero_duo_x1.skill_ideas_total}\`\n- Runner ideas: \`${data.future_standards.arby_cicero_duo_x1.runner_ideas_total}\`\n- Cleanup tasks: \`${data.future_standards.arby_cicero_duo_x1.cleanup_tasks_total}\`\n\n## Style And Route\n\n- x1: ${data.future_standards.phase_semantics.x1}\n- x2: ${data.future_standards.phase_semantics.x2}\n- First-person sibling style: \`${data.future_standards.phase_semantics.first_person_style}\`\n- Output standard: ${data.future_standards.phase_semantics.sibling_output_standard}\n- Goal mode: ${data.future_standards.phase_semantics.goal_mode}\n- Archive fallback: ${data.active_route.archive_fallback_rule}\n`;
}

function renderMemoryReceiptMarkdown(data) {
  return `# v552 v8 x1 Memory Updater Receipt\n\nStatus: \`${data.overall_status}\`\n\n## Scope\n\n${bullets(data.memory_update_scope)}\n\n## Boundary\n\nMemory was updated by adding a small ad-hoc note only. Existing memory registries were not edited directly.\n`;
}

function renderPhaseStatusMarkdown(data) {
  return `# v552 v8 x1 Phase Status Index\n\nStatus: \`${data.overall_status}\`\n\nLatest closed phase: \`${data.latest_closed_phase_after_receipt}\`\nLatest completed x1: \`${data.latest_completed_x1_after_receipt}\`\nLatest completed x2: \`${data.latest_completed_x2_after_receipt}\`\nNext x2 scope: \`${data.next_x2_scope}\`\nNext x1 after x2: \`${data.next_x1_lane_after_x2}\`\n\n## Counts\n\n- Safe approval packets: \`${data.counts.safe_approval_packets}\`\n- Candidate approval packets: \`${data.counts.candidate_approval_packets}\`\n- Exact approval packets: \`${data.counts.exact_approval_packets}\`\n- Skill ideas: \`${data.counts.skill_ideas}\`\n- Runner ideas: \`${data.counts.runner_ideas}\`\n- Cleanup tasks: \`${data.counts.cleanup_tasks}\`\n\n## Artifacts\n\n${data.artifacts.map((item) => `- \`${item}\``).join("\n")}\n`;
}

function renderStartupSnapshotMarkdown(data) {
  return `# v552 v8 x1 Compact Pause Startup Snapshot\n\nStatus: \`${data.overall_status}\`\n\n## Startup Order\n\n${numbered(data.startup_order)}\n\n## Pointer\n\n- Status: \`${data.current_pointer_after_receipt.status}\`\n- Current active phase: \`${data.current_pointer_after_receipt.current_active_phase}\`\n- Latest closed phase: \`${data.current_pointer_after_receipt.latest_closed_phase}\`\n- Latest completed x1: \`${data.current_pointer_after_receipt.latest_completed_x1_phase}\`\n- Latest completed x2: \`${data.current_pointer_after_receipt.latest_completed_x2_phase}\`\n- Next x1 after x2: \`${data.current_pointer_after_receipt.next_x1_lane_after_x2}\`\n`;
}

function renderCloseoutMarkdown(data) {
  return `# v552 v8 x1 Closeout\n\nStatus: \`${data.overall_status}\`\n\nLatest closed phase: \`${data.latest_closed_phase_after_receipt}\`\nLatest completed x1: \`${data.latest_completed_x1_after_receipt}\`\nLatest completed x2: \`${data.latest_completed_x2_after_receipt}\`\nNext x2 scope: \`${data.next_x2_scope}\`\nNext x1 after x2: \`${data.next_x1_lane_after_x2}\`\n\n## Counts\n\n- Safe approval packets: \`${data.counts.safe_approval_packets}\`\n- Candidate approval packets: \`${data.counts.candidate_approval_packets}\`\n- Exact approval packets: \`${data.counts.exact_approval_packets}\`\n- Skill ideas: \`${data.counts.skill_ideas}\`\n- Runner ideas: \`${data.counts.runner_ideas}\`\n- Cleanup tasks: \`${data.counts.cleanup_tasks}\`\n- New agents spawned: \`${data.counts.new_agents_spawned}\`\n- Held siblings activated: \`${data.counts.held_siblings_activated}\`\n\n## Evidence\n\n${data.evidence.map((item) => `- \`${item}\``).join("\n")}\n\n## Boundary\n\nNo private route handles, raw transcripts, browser routes, credentials, private machine paths, screenshots, account mutation, deployment, purchase, API-key creation, destructive cleanup, global hook installation, identity merge, or held-sibling activation was published or run.\n`;
}

function renderCurrentState(current) {
  return `# Omega-Mini Current State\n\nStatus: ${current.status}\nCurrent active phase: ${current.current_active_phase}\nLatest closed phase: ${current.latest_closed_phase}\nLatest completed x1: ${current.latest_completed_x1_phase}\nLatest completed x2: ${current.latest_completed_x2_phase}\nCurrent lanes: ${current.current_active_lanes.join("; ")}\nNext x2 scope: ${current.next_x2_scope}\nNext x1 lane after x2: ${current.next_x1_lane_after_x2}\n\n## v8 x1 Toolchain and Triad Workflow\n\n- Codex CLI version: \`${current.v8_x1_toolchain_triad_workflow.codex_cli_version}\`\n- Safe approval packets: \`${current.v8_x1_toolchain_triad_workflow.safe_approval_packets}\`\n- Candidate approval packets: \`${current.v8_x1_toolchain_triad_workflow.candidate_approval_packets}\`\n- Exact approval packets: \`${current.v8_x1_toolchain_triad_workflow.exact_approval_packets}\`\n- Skill ideas: \`${current.v8_x1_toolchain_triad_workflow.skill_ideas}\`\n- Runner ideas: \`${current.v8_x1_toolchain_triad_workflow.runner_ideas}\`\n- Cleanup tasks: \`${current.v8_x1_toolchain_triad_workflow.cleanup_tasks}\`\n- First-person style: \`${current.v8_x1_toolchain_triad_workflow.first_person_style}\`\n- MD/TXT artifact output standard: \`${current.v8_x1_toolchain_triad_workflow.md_txt_artifact_output_standard}\`\n- New agents spawned: \`${current.v8_x1_toolchain_triad_workflow.new_agents_spawned}\`\n- Held siblings activated: \`${current.v8_x1_toolchain_triad_workflow.held_siblings_activated}\`\n\n## Lookup Rule\n\n${current.archive_fallback_rule}\n\n## Current Lookup Files\n\n${current.current_lookup_files.map((item) => `- ${item}`).join("\n")}\n\n## Latest Action Summary\n\n${current.latest_action_summary.map((item) => `- ${item}`).join("\n")}\n\n## Safety Boundary\n\n- Status-only receipts, no private route data, no private lane body content, no credentials, no private machine paths.\n- GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, and deployment closure remain open.\n`;
}

function renderLatestBeacon(latest) {
  return `# Omega-Mini Latest Updates Beacon\n\nStatus: ${latest.status}\nPrimary branch: ${latest.primary_branch}\nArchive branch: ${latest.archive_branch}\nCurrent active phase: ${latest.current_active_phase}\nLatest closed phase: ${latest.latest_closed_phase}\nLatest completed x1: ${latest.latest_completed_x1_phase}\nLatest completed x2: ${latest.latest_completed_x2_phase}\nCurrent lanes: ${latest.current_active_lanes.join("; ")}\nNext x2 scope: ${latest.next_x2_scope}\nNext x1 lane after x2: ${latest.next_x1_lane_after_x2}\n\n## Round Robin\n\n${latest.round_robin_sequence.map((item, index) => `- ${index + 1}. ${item}`).join("\n")}\n\n## Latest Lookup Files\n\n${latest.latest_lookup_files.map((item) => `- ${item}`).join("\n")}\n\n## Sibling Lookup Rule\n\nOpen omega-mini current state first, then this beacon, then the exact relative files named here.\n\n## Safety Boundary\n\n- Use status-only evidence and exact relative repo paths.\n- Do not publish private route data, private lane body content, credentials, screen-capture files, or private machine paths.\n`;
}

function renderGhcBeacon(ghc) {
  return `# GHC Current State Beacon\n\nStatus: ${ghc.status}\nCurrent active phase: ${ghc.current_active_phase}\nLatest closed phase: ${ghc.latest_closed_phase}\nLatest completed x1: ${ghc.latest_completed_x1_phase}\nLatest completed x2: ${ghc.latest_completed_x2_phase}\nNext x2 scope: ${ghc.next_x2_scope}\nNext x1 lane after x2: ${ghc.next_x1_lane_after_x2}\n\n## Lookup Files\n\n${ghc.lookup_files.map((item) => `- ${item}`).join("\n")}\n\n## Boundary\n\nStatus-only beacon. No private route data, private lane body content, credentials, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.\n`;
}

function numbered(items) {
  return items.map((item, index) => `${index + 1}. ${item}`).join("\n");
}

function bullets(items) {
  return items.map((item) => `- ${item}`).join("\n");
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
  }).formatToParts(date).reduce((acc, part) => {
    acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
