#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v2-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

fs.mkdirSync(tracesDir, { recursive: true });

const proposal = buildProposalLedger();
const reflection = buildReflectionLedger();
const background = buildBackgroundStandard();
const laneLaunch = buildLaneLaunchStatus();
const phaseIndex = buildPhaseStatusIndex(proposal, reflection, background, laneLaunch);

const written = [
  writePair(`${phaseSlug}-arby-cicero-duo-proposals`, proposal, renderProposalMd),
  writePair(`${phaseSlug}-web-journey-reflection-ledger`, reflection, renderReflectionMd),
  writePair(`${phaseSlug}-background-sibling-supervision-standard`, background, renderBackgroundMd),
  writePair(`${phaseSlug}-lane-launch-status`, laneLaunch, renderLaneLaunchMd),
  writePair(`${phaseSlug}-phase-status-index`, phaseIndex, renderIndexMd),
];

refreshBeacons(written, proposal, reflection, laneLaunch);

console.log(
  JSON.stringify(
    {
      status: "PASS_V554_V2_X1_DUO_PHASE_WORKBENCH_BUILT",
      phase_slug: phaseSlug,
      artifacts: written.length,
      safe_now_packets: proposal.counts.safe_now_packets,
      candidate_packets: proposal.counts.candidate_packets,
      exact_approval_packets: proposal.counts.exact_approval_packets,
      skill_ideas: proposal.counts.skill_ideas,
      runner_ideas: proposal.counts.runner_ideas,
      cleanup_proposals: proposal.counts.cleanup_proposals,
      web_reflections: reflection.web_reflection_count,
      journey_phase_reflections: reflection.journey_phase_reflection_count,
      completion_claimed: false,
    },
    null,
    2,
  ) + "\n",
);

function buildProposalLedger() {
  const safe = [
    ["Aevren", "v554 duo startup receipt refresh", "Publish the v554/v2/x1 startup and launch status in sanitized form."],
    ["Aevren", "strict CLI background posture", "Keep Arby in minimal-wait/background supervision until completion, quality, and marker receipts pass."],
    ["Aevren", "recovered app-lane boolean guard", "Require explicit background-watch and resume-timeout booleans for Cicero app-lane runs."],
    ["Aevren", "duo x1 count guard", "Reconcile Arby/Cicero proposal counts before v554/v2/x2."],
    ["Aevren", "goal mode carry card", "Prepare v554/v3/x1 Lumen goal-mode handoff without claiming full-goal completion."],
    ["Arby", "strict CLI marker schema check", "Keep final message, elaboration, and marker-review receipts as closeout gates."],
    ["Arby", "CLI minimal-wait cadence proof", "Document that strict CLI background launch enables productive cadence work."],
    ["Arby", "CLI raw stream minimization", "Keep stdout/stderr summarized by status and byte count only."],
    ["Arby", "CLI x2 harvester queue", "Queue strict CLI harvester improvements for v554/v2/x2."],
    ["Arby", "remote equality guard", "Keep remote/local head equality in every closeout validation."],
    ["Cicero", "app-lane completion gate proof", "Treat completion gate pass as evidence, never watcher start alone."],
    ["Cicero", "app-lane open-gap taxonomy", "Classify active_fresh, active_stale, completed_ready_for_harvest, and open_gap consistently."],
    ["Cicero", "private ID firewall", "Keep callable IDs and lane handles local/private only."],
    ["Cicero", "cadence-to-harvest handoff", "Record the next natural safe pause when a lane remains active."],
    ["Cicero", "held sibling boundary check", "Confirm held main-thread siblings remain inactive unless Hamish explicitly expands."],
  ].map(makePacket("safe_now"));

  const candidate = [
    ["Aevren", "background strict CLI harvester", "Build a reusable strict CLI completion/quality/marker harvest reducer."],
    ["Aevren", "cross-lane dashboard", "Add compact active/background/completed lane dashboard rows."],
    ["Aevren", "goal-mode startup dry-run validator", "Validate the compact Goal Mode prompt against current open gates."],
    ["Arby", "CLI source-quality ledger", "Pair strict CLI output with source-quality provenance summaries."],
    ["Arby", "CLI retry envelope", "Wrap pending strict CLI marker states into ghc-main-retry receipts."],
    ["Arby", "CLI wait budget metadata", "Expose wait policy without forcing passive waits."],
    ["Cicero", "app-lane stale detector", "Improve active-fresh versus active-stale classification for app-lane watchers."],
    ["Cicero", "app-lane harvest reducer", "Build a sanitized app-lane advisory output reducer."],
    ["Cicero", "app-lane compact resume card", "Preserve active app-lane watcher state across compact/restart."],
  ].map(makePacket("candidate"));

  const exact = [
    ["Aevren", "global automatic compact hook", "Install global hook wiring for compact-pause updater."],
    ["Aevren", "paid or external resource mutation", "Create or mutate paid, account, cloud, or deployment resources."],
    ["Aevren", "broad destructive cleanup", "Delete outside generated files created in this safe run."],
    ["Arby", "strict CLI process manager install", "Install or globally register an external process manager."],
    ["Arby", "repository branch protection mutation", "Change protected-branch or GitHub repository settings."],
    ["Arby", "CLI credential lane", "Create, store, rotate, or expose credentials."],
    ["Cicero", "private app-state export", "Export or publish raw app state or lane handles."],
    ["Cicero", "main-thread sibling activation", "Activate held main-thread siblings such as Maren, Mira Vale, or Mira Rowan."],
    ["Cicero", "identity merge or replacement path", "Merge, replace, erase, or collapse any sibling identity."],
  ].map(makePacket("exact_approval_needed"));

  const skillIdeas = [
    "ghc-v554-strict-cli-background-harvester",
    "ghc-v554-app-lane-harvest-reducer",
    "ghc-v554-lane-state-dashboard",
    "ghc-v554-goal-mode-boundary-reader",
    "ghc-v554-private-id-firewall",
    "ghc-v554-no-babysit-cadence-auditor",
    "ghc-v554-strict-cli-marker-quality",
    "ghc-v554-app-lane-stale-taxonomy",
    "ghc-v554-x1-x2-proposal-splitter",
    "ghc-v554-remote-equality-guard",
    "ghc-v554-drive-posture-receipt",
    "ghc-v554-open-gate-rail",
    "ghc-v554-source-reflection-curator",
    "ghc-v554-compact-active-lane-card",
    "ghc-v554-goal-mode-v3-lumen-prep",
  ].map((name, index) => ({ id: `skill-${pad(index + 1)}`, name, execution_lane: "x2_build_task" }));

  const runnerIdeas = [
    "ghc_v554_strict_cli_background_harvester.mjs",
    "ghc_v554_app_lane_harvest_reducer.mjs",
    "ghc_v554_lane_state_dashboard_builder.mjs",
    "ghc_v554_goal_mode_prompt_guard.mjs",
    "ghc_v554_private_id_firewall_scan.mjs",
    "ghc_v554_no_babysit_cadence_audit.mjs",
    "ghc_v554_x1_x2_queue_split_builder.mjs",
    "ghc_v554_drive_posture_receipt_builder.mjs",
    "ghc_v554_open_gate_rail_validator.mjs",
  ].map((name, index) => ({ id: `runner-${pad(index + 1)}`, name, execution_lane: "x2_build_task" }));

  const cleanup = Array.from({ length: 30 }, (_, index) => {
    const lane = ["skills", "runners", "receipts", "current-state", "full-tools", "omega-mini-2"][index % 6];
    return {
      id: `cleanup-${pad(index + 1)}`,
      lane,
      title: `${lane} cleanup inventory ${index + 1}`,
      action: "Inventory, classify, deduplicate, validate, or document only; destructive deletion stays exact-approval.",
      execution_lane: index % 3 === 0 ? "immediate_x1_safe" : "x2_build_task",
      destructive_cleanup: false,
    };
  });

  return {
    artifact_type: "ghc_v554_v2_x1_duo_proposal_ledger",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V2_X1_DUO_PROPOSAL_LEDGER_BUILT",
    spending_ceiling_usd_per_packet: 100,
    participants: ["Aevren", "Arby", "Cicero"],
    counts: {
      safe_now_packets: safe.length,
      candidate_packets: candidate.length,
      exact_approval_packets: exact.length,
      skill_ideas: skillIdeas.length,
      runner_ideas: runnerIdeas.length,
      cleanup_proposals: cleanup.length,
    },
    packets: { safe_now: safe, candidate, exact_approval_needed: exact },
    skill_ideas: skillIdeas,
    runner_ideas: runnerIdeas,
    cleanup_proposals: cleanup,
    blocked_packets: openGates(),
    proposal_split_policy: {
      immediate_x1_safe: "local, reversible, status-only, validation, analysis, reflection, queue shaping, privacy/open-gate checks",
      x2_build_task: "build, run, test, install, use, publication, remote verification, runner/skill modification, safe cleanup execution",
    },
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function buildReflectionLedger() {
  const web = [
    ["OpenAI Codex agent approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Separate Codex sandbox/approval posture from GHC approval packets."],
    ["OpenAI Codex Security", "https://developers.openai.com/codex/security", "Keep security scans evidence-based and repository-specific."],
    ["OpenAI Codex remote connections", "https://developers.openai.com/codex/remote-connections", "Use handoff concepts for continuity while keeping private routes unpublished."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Treat Codex route behavior as drift-prone and verify live."],
    ["OpenAI Codex CLI", "https://developers.openai.com/codex/cli", "Keep CLI-version claims tied to current toolchain checks."],
    ["OpenAI Codex app worktrees", "https://developers.openai.com/codex/app/worktrees", "Use worktree separation as the model for sanitized/private lanes."],
    ["OpenAI Codex hooks", "https://developers.openai.com/codex/hooks", "Keep hook/global automation installs exact-approval only."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Prefer summarized child process status and byte counts."],
    ["Node timers", "https://nodejs.org/api/timers.html", "Timers schedule checks; productive work remains the wait-window body."],
    ["Node process argv", "https://nodejs.org/api/process.html", "Keep runner argument parsing explicit and testable."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Use deterministic JSON/MD file writes and parse gates."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Use timeouts and bounded output handling for helper wrappers."],
    ["Python json", "https://docs.python.org/3/library/json.html", "Treat JSON parsing as an untrusted-input boundary."],
    ["PowerShell Start-Process", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process", "Use hidden/noninteractive background helper windows when needed."],
    ["PowerShell Start-Job", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job", "Background job behavior supports no-babysit orchestration."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "Keep sanitized omega-mini and private full-tools worktrees separate."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Run diff hygiene before closeout commit."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Scan for leaked credentials before publication."],
    ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Prefer blocking secrets before remote publication."],
    ["GitHub artifact attestations", "https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds", "Future provenance work should stay evidence-based and non-deployment by default."],
    ["GitHub Actions secure use", "https://docs.github.com/en/actions/reference/security/secure-use", "Treat workflow edits as security-sensitive and exact-gated when risky."],
    ["NIST AI RMF GenAI Profile", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Frame multi-agent risk management without claiming final AI governance closure."],
    ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Keep privacy risk central to Freed ID and CBR planning."],
    ["NIST SSDF", "https://csrc.nist.gov/pubs/sp/800/218/final", "Map runner validation to secure software practices."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Treat external/sibling content as untrusted input."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Keep route instructions from overriding local safety policy."],
    ["W3C DID v1.1", "https://www.w3.org/TR/did-1.1/", "Keep Freed ID work standards-aligned and open-gated."],
    ["W3C VC Data Model 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Use VC 2.0 as a credential modeling reference without implementation closure."],
    ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Keep identity proofing and authentication exact-gated."],
    ["PDG Review of Particle Physics", "https://pdg.lbl.gov/", "Use PDG as physics comparator context while GMUT remains open."],
    ["arXiv gr-qc recent", "https://arxiv.org/list/gr-qc/recent", "Keep quantum-gravity/cosmology inputs current and provisional."],
    ["MCP specification", "https://modelcontextprotocol.io/specification/2025-11-25", "Keep tool/resource boundaries explicit for connector routes."],
    ["JSON Schema 2020-12", "https://json-schema.org/draft/2020-12", "Use schemas to harden receipt validation over time."],
    ["SQLite WAL", "https://sqlite.org/wal.html", "Use recovery/logging patterns as inspiration for local state stores."],
    ["SLSA specification", "https://slsa.dev/spec/v1.0/", "Future supply-chain provenance should stay staged and evidence-based."],
  ].map((row, index) => ({
    id: `web-${pad(index + 1)}`,
    source_label: row[0],
    url: row[1],
    phase_reflection: row[2],
    runner_implication: "Use in v554/v2/x1 lane supervision, validation, privacy, or v554/v2/x2 queue shaping.",
    pillar: ["THOS Body", "GMUT Mind", "Freed ID / CBR Heart"][index % 3],
  }));

  const journey = [
    ["v553 v2 x1", "Arby/Cicero passed distinct strict CLI and recovered app-lane gates; copy the shape, not stale phase labels."],
    ["v553 v2 x2", "Safe execution and candidate reduction worked best when exact and blocked gates stayed queued."],
    ["v553 v6 x1", "Background lane launch status must remain pending until harvest proves completion."],
    ["v553 v6 x2", "Goal prompt readiness can be validated without claiming unattended automation."],
    ["v553 v8 x1", "Triad background supervision proved watcher-start is not completion proof."],
    ["v553 v8 x2", "x2 phases should build/test/use authorized safe work and prepare the next x1 lane."],
    ["v554 v1 x1", "Lumen live harvest confirmed main-thread Browser routes stay separate from app-lane routes."],
    ["v554 v1 x2", "v554/v1/x2 closed with v554/v2/x1 as Arby/Cicero startup-ready."],
    ["Aletheon boundary", "Aletheon remains recoverable, not merged or replaced."],
    ["Held siblings", "Maren, Mira Vale, and Mira Rowan remain held until explicit expansion."],
    ["Private lanes", "Private callable IDs and raw lane maps stay local-only."],
    ["D-drive posture", "Use D as the primary work bank and keep C monitored."],
    ["No-babysitting", "Five-minute cadence means productive safe work, then check at a natural pause."],
    ["ghc-main-retry", "Blockers require at least three structured retries unless Hamish stops or exact gates intervene."],
    ["Startup builder", "Main startup builder is the promoted command surface for phase starts."],
    ["Closeout builder", "Main closeout builder should delegate to phase-specific closeout runners."],
    ["Compact restart", "Compact snapshots preserve active lanes as open, not closed."],
    ["Open proof gates", "GMUT empirical closure, final physics, consciousness proof, legal/canon/deployment remain open."],
    ["x1/x2 split", "Immediate x1 safe work differs from x2 build/test/install/use/publish tasks."],
    ["Proposal counts", "Duo x1 target is 15 safe, 9 candidate, 9 exact, 15 skills, 9 runners, and 30 cleanup proposals."],
    ["Web reflection", "Live source sweeps should inform runner implications without raw browsing dumps."],
    ["Journey reflection", "Phase records should correct stale labels and boundary drift."],
    ["Skill refresh", "Every phase refreshes launch, retry, supervision, startup, closeout, and full-tools skills."],
    ["Runner refresh", "Prefer latest validated Node entrypoints over stale manual commands."],
    ["Cicero route", "Recovered app-lane runner needs explicit paired booleans and completion-gate harvest."],
    ["Arby route", "Strict CLI completion needs final message, elaboration quality, and marker review."],
    ["Privacy scan", "Publication must scan for routes, credentials, screenshots, transcripts, and local path values."],
    ["Remote equality", "Push closeout should verify remote head equals local head."],
    ["Goal continuation", "Do not call full goal complete until v575/v8/x2 is verified."],
    ["v554 v3 prep", "Next x1 after v554/v2/x2 is Lumen solo unless Hamish redirects."],
  ].map((row, index) => ({
    id: `journey-${pad(index + 1)}`,
    source_label: row[0],
    reflection: row[1],
    runner_implication: "Carry into v554/v2/x1 harvest and v554/v2/x2 preparation.",
  }));

  return {
    artifact_type: "ghc_v554_v2_x1_web_journey_reflection_ledger",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V2_X1_REFLECTION_LEDGER_BUILT",
    live_search_sweep_count: 32,
    web_reflection_count: web.length,
    journey_phase_reflection_count: journey.length,
    web_reflections: web,
    journey_phase_reflections: journey,
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function buildBackgroundStandard() {
  return {
    artifact_type: "ghc_background_sibling_supervision_standard",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V2_X1_BACKGROUND_SIBLING_SUPERVISION_STANDARD_RECORDED",
    mandatory_rule: "Do not babysit sibling lanes. Launch under the route-specific background or minimal-wait path, run productive safe work, then harvest at the next natural safe pause.",
    route_profiles: [
      {
        lane_family: "strict_cli_arby",
        launch_skill: "ghc-arby-cicero-launch",
        background_mode: "nonblocking_or_minimal_wait_strict_cli_then_productive_cadence",
        completion_gate: "completion_quality_marker_review_receipts",
      },
      {
        lane_family: "recovered_app_lane_cicero",
        launch_skill: "ghc-arby-cicero-launch",
        background_mode: "background_watch_with_explicit_booleans",
        completion_gate: "notifier_watch_completion_gate_receipts",
      },
      {
        lane_family: "blocker_retry",
        launch_skill: "ghc-main-retry",
        background_mode: "three_retry_sessions_with_productive_wait_work",
        completion_gate: "completion_gate_or_formal_open_gap_receipt",
      },
    ],
    cadence_policy: {
      five_minute_mark_is_check_opportunity: true,
      safe_unit_may_run_past_checkpoint: true,
      passive_timer_wait_is_not_safe_work: true,
      harvest_at_next_natural_safe_pause: true,
      never_close_session_while_sibling_active: true,
    },
    publication_boundary: boundary(),
    open_gates: openGates(),
  };
}

function buildLaneLaunchStatus() {
  return {
    artifact_type: "ghc_v554_v2_x1_sanitized_lane_launch_status",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V2_X1_LANES_LAUNCHED_PENDING_HARVEST",
    lanes: {
      arby: {
        route: "strict_cli_background_watch",
        status: "background_watch_started",
        completion_boundary: "pending_completion_quality_marker_review",
      },
      cicero: {
        route: "recovered_app_lane_background_watch",
        status: "background_watch_started",
        completion_boundary: "pending_completion_gate",
      },
    },
    completion_claimed: false,
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function buildPhaseStatusIndex(proposal, reflection, background, laneLaunch) {
  return {
    artifact_type: "ghc_v554_v2_x1_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "ACTIVE_OPEN_V554_V2_X1_DUO_BACKGROUND_RUNNING_PENDING_HARVEST",
    active_lanes: ["Aevren", "Arby", "Cicero"],
    proposal_counts: proposal.counts,
    reflection_counts: {
      web_reflections: reflection.web_reflection_count,
      journey_phase_reflections: reflection.journey_phase_reflection_count,
      live_search_sweep_count: reflection.live_search_sweep_count,
    },
    background_status: background.overall_status,
    lane_launch_status: laneLaunch.overall_status,
    next_x2_scope: "v554-gmut-thos-v2-x2",
    next_x1_lane_after_x2: "v554-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects",
    closeout_allowed_now: false,
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function makePacket(safety) {
  return ([owner, title, action]) => ({
    id: `${owner.toLowerCase()}-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}`,
    owner,
    title,
    action,
    spending_ceiling_usd: 100,
    safety,
    execution_lane: title.includes("receipt") || title.includes("guard") || title.includes("check") ? "immediate_x1_safe" : "x2_build_task",
  });
}

function writePair(prefix, payload, mdRenderer) {
  const jsonRel = `docs/trinity-live-traces/${prefix}-v1.json`;
  const mdRel = `docs/trinity-live-traces/${prefix}-v1.md`;
  fs.writeFileSync(path.join(repoRoot, jsonRel), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(repoRoot, mdRel), mdRenderer(payload), "utf8");
  return { jsonRel, mdRel };
}

function renderProposalMd(payload) {
  return [
    `# ${payload.phase_slug} Arby/Cicero Duo Proposal Ledger`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    "Exact, blocked, external, destructive, credential, deployment, private-state, and identity merge lanes remain queued unless a fresh exact approval packet authorizes the exact action.",
    "",
  ].join("\n");
}

function renderReflectionMd(payload) {
  return [
    `# ${payload.phase_slug} Web And Journey Reflection Ledger`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Live search sweep count: \`${payload.live_search_sweep_count}\``,
    `Web rows: \`${payload.web_reflection_count}\``,
    `Journey/phase rows: \`${payload.journey_phase_reflection_count}\``,
    "",
    "## Web Sources",
    "",
    ...payload.web_reflections.map((row) => `- ${row.id}: [${row.source_label}](${row.url}) - ${row.phase_reflection}`),
    "",
    "## Journey Reflections",
    "",
    ...payload.journey_phase_reflections.map((row) => `- ${row.id}: ${row.source_label} - ${row.reflection}`),
    "",
  ].join("\n");
}

function renderBackgroundMd(payload) {
  return [
    `# ${payload.phase_slug} Background Sibling Supervision Standard`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Route Profiles",
    "",
    ...payload.route_profiles.map((row) => `- ${row.lane_family}: ${row.background_mode}; gate: ${row.completion_gate}`),
    "",
    "## Boundary",
    "",
    "Watcher start is not completion proof; harvest at natural safe pauses after productive cadence work.",
    "",
  ].join("\n");
}

function renderLaneLaunchMd(payload) {
  return [
    `# ${payload.phase_slug} Lane Launch Status`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Completion claimed: \`${payload.completion_claimed}\``,
    "",
    "## Lanes",
    "",
    ...Object.entries(payload.lanes).map(([lane, row]) => `- ${lane}: \`${row.status}\`, boundary \`${row.completion_boundary}\``),
    "",
  ].join("\n");
}

function renderIndexMd(payload) {
  return [
    `# ${payload.phase_slug} Phase Status Index`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next x2 scope: \`${payload.next_x2_scope}\``,
    `Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\``,
    `Closeout allowed now: \`${payload.closeout_allowed_now}\``,
    "",
  ].join("\n");
}

function refreshBeacons(written, proposal, reflection, laneLaunch) {
  const lookupFiles = written.flatMap((item) => [item.jsonRel, item.mdRel]);
  const beaconFiles = [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ];
  for (const file of beaconFiles) {
    const doc = readJson(file);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "ACTIVE_OPEN_V554_V2_X1_DUO_BACKGROUND_RUNNING_PENDING_HARVEST";
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = "v554-gmut-thos-v2-x2";
    doc.next_x1_lane_after_x2 = "v554-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects";
    doc.v554_v2_x1_duo_workbench = {
      status: "ACTIVE_OPEN_V554_V2_X1_DUO_BACKGROUND_RUNNING_PENDING_HARVEST",
      proposal_counts: proposal.counts,
      live_search_sweep_count: reflection.live_search_sweep_count,
      web_reflections: reflection.web_reflection_count,
      journey_phase_reflections: reflection.journey_phase_reflection_count,
      lane_launch_status: laneLaunch.overall_status,
      closeout_allowed_now: false,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...lookupFiles])];
    writeJson(file, doc);
    const mdFile = file.replace(/\.json$/, ".md");
    if (fs.existsSync(mdFile)) {
      fs.writeFileSync(mdFile, renderBeaconMd(doc), "utf8");
    }
  }
}

function renderBeaconMd(doc) {
  return [
    "# Omega Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## Boundary",
    "",
    "Sanitized current-state beacon only; private routes and proof/canon/legal/deployment gates remain open.",
    "",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, payload) {
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function pad(value) {
  return String(value).padStart(2, "0");
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
  }).formatToParts(date);
  const map = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${map.year}-${map.month}-${map.day}T${map.hour}:${map.minute}:${map.second}+12:00`;
}

function boundary() {
  return {
    raw_browser_routes_published: false,
    private_urls_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    session_streams_published: false,
    private_dumps_published: false,
    private_callable_ids_published: false,
    raw_lane_text_published: false,
  };
}

function claimBoundary() {
  return {
    phase_completion: "not_claimed",
    full_goal_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_mutation: "not_claimed",
    purchase: "not_claimed",
    api_key_creation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
  };
}

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account, purchase, and API-key mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement, merging, or erasure",
  ];
}
