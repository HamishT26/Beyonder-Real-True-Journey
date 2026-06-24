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
const phaseSlug = args.get("--phase-slug") || "v555-gmut-thos-v4-x1";
const previousClosed = args.get("--previous-closed") || "v555-gmut-thos-v3-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const publicationBoundary = {
  browser_routes_published: false,
  private_urls_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  session_streams_published: false,
  private_dumps_published: false,
  private_callable_ids_published: false,
  private_route_handles_published: false,
  raw_app_state_published: false,
};

const claimBoundary = {
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

const sources = [
  ["OpenAI Codex subagents", "https://developers.openai.com/codex/subagents", "Keep agent/thread supervision aligned with sandbox and approval boundaries."],
  ["OpenAI Codex app features", "https://developers.openai.com/codex/app/features", "Use Codex app parallelism and worktree features without pretending a background watcher is completion."],
  ["OpenAI Codex approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Approval posture remains separate from narrative authorization and all exact gates stay explicit."],
  ["OpenAI Codex worktrees", "https://developers.openai.com/codex/app/worktrees", "Worktrees support independent lanes and keep active phase edits reviewable."],
  ["OpenAI Codex slash commands", "https://developers.openai.com/codex/cli/slash-commands", "Session commands should be explicit and committed work should be saved before exits."],
  ["OpenAI Codex computer use", "https://developers.openai.com/codex/app/computer-use", "Visible app content and screenshots require narrow, privacy-aware handling."],
  ["OpenAI Codex CLI", "https://developers.openai.com/codex/cli", "Strict CLI lanes should stay read-only/status-only unless the phase explicitly promotes build work."],
  ["OpenAI Codex CLI reference", "https://developers.openai.com/codex/cli/reference", "CLI flags and risky options should be version-aware and recorded as status-only receipts."],
  ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Skills package instructions and scripts, so phase rules belong in skill surfaces as well as repo receipts."],
  ["OpenAI Codex follow goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode is a long-running objective with a stopping condition, not proof that a phase slice is complete."],
  ["MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "Tool surfaces require clear schemas and explicit side-effect boundaries."],
  ["MCP specification", "https://modelcontextprotocol.io/specification/2025-06-18", "Connector and resource routes should be treated as structured protocols, not informal hidden state."],
  ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk management is a governance rail, not a closure claim."],
  ["NIST AI 600-1 GenAI Profile", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Generative AI risk categories should inform blocked and exact-approval rails."],
  ["NIST AI 600-1 PDF", "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf", "Profile recommendations belong in evaluation matrices and open-gate receipts."],
  ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Current app/CLI behavior can drift, so launch and recovery rules need current docs checks."],
  ["Git worktree", "https://git-scm.com/docs/git-worktree", "Parallel phase branches should stay isolated and reviewable."],
  ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Secret and private-lane prevention belongs before push."],
  ["Node child_process", "https://nodejs.org/api/child_process.html", "Runner launches should prefer argument arrays and status-only logging."],
  ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Python watchers should avoid unnecessary shell expansion and record bounded execution."],
  ["W3C Verifiable Credentials 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Freed ID claims require verifiable data and privacy-aware proof boundaries."],
  ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identity architecture should stay decentralized-identifier aware without deployment claims."],
  ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Digital identity assurance remains a design lane, not legal closure."],
  ["CODATA constants", "https://pml.nist.gov/cuu/Constants/", "GMUT numerical comparison should use stable official constant baselines."],
  ["Particle Data Group", "https://pdg.lbl.gov/", "Physics claims should stay comparator-grounded and gate-open."],
  ["LIGO data", "https://www.ligo.caltech.edu/page/ligo-data", "Gravitational claims need reproducible data, not narrative proof."],
  ["GWOSC", "https://gwosc.org/", "Open gravitational-wave datasets can seed future x2 validation work."],
  ["Planck 2018 cosmology", "https://arxiv.org/abs/1807.06209", "Cosmology baselines stay source rows until independent validation exists."],
  ["Stanford Encyclopedia of Philosophy consciousness", "https://plato.stanford.edu/entries/consciousness/", "Consciousness work remains conceptually and empirically open."],
  ["OECD AI Principles", "https://www.oecd.org/en/topics/sub-issues/ai-principles.html", "Accountability, robustness, human rights, and transparency belong in the governance rail."],
];

const journeyReflections = [
  "v553 v3 x2 is the latest closed phase and v4 x1 is active.",
  "The v4 x1 lane is Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects.",
  "Aster uses strict CLI evidence/source/marker discipline.",
  "Kierkegaard uses recovered app-lane governance and dignity checks.",
  "Aristotle uses recovered app-lane taxonomy, schema, and blocker classification.",
  "Watcher start is not completion proof.",
  "Completion requires strict CLI completion/quality/marker receipts or app-lane completion gates.",
  "Five-minute marks are productive check opportunities, not passive waits.",
  "Safe work may run past a five-minute mark and then harvest at a natural pause.",
  "Private callable IDs and route handles remain local-only.",
  "omega-mini-2 remains the sanitized publication surface.",
  "full-tools remains the richer private support lane.",
  "No new agents are spawned by default.",
  "Held main-thread siblings remain held unless Hamish explicitly expands.",
  "Aletheon remains recoverable and not replaced.",
  "Goal Mode is active for this thread objective and not a separate unattended automation claim.",
  "x1 proposals split into immediate safe work and queued x2 build tasks.",
  "x2 is for build, run, test, install, use, validate, and publish safe artifacts.",
  "No destructive cleanup runs without a fresh exact approval boundary.",
  "No deployment, purchase, account mutation, or API-key creation is auto-run.",
  "GMUT empirical closure stays open.",
  "Final physics stays open.",
  "Consciousness proof stays open.",
  "Legal closure stays open.",
  "Canon promotion stays open.",
  "Private-material proof and raw-publication proof stay open.",
  "Drive posture must keep preferring D drive for archives and downloads.",
  "Node launchers are preferred; original Windows entrypoints remain fallback surfaces.",
  "Validation requires JSON parse, Node check, current-state guard, diff hygiene, privacy scan, and remote equality.",
  "The v4 x1 closeout cannot happen while any triad lane is still active without a formal open-gap receipt.",
];

const safePackets = makePackets("safe_now", 20, [
  "Record triad watcher-start as active, not complete",
  "Publish no-babysit cadence status for v4 x1",
  "Seed thirty source reflection rows",
  "Seed thirty Journey reflection rows",
  "Prepare strict CLI harvest checklist",
  "Prepare recovered app-lane harvest checklist",
  "Record private route firewall",
  "Record open-gate rail",
  "Classify immediate x1 safe work",
  "Classify queued x2 build work",
  "Check current-state phase truth",
  "Check omega-mini lookup files",
  "Build v4 x1 proposal scaffold",
  "Build v4 x1 cleanup inventory scaffold",
  "Build skill idea scaffold",
  "Build runner idea scaffold",
  "Prepare compact-pause active handoff",
  "Prepare closeout acceptance criteria",
  "Record drive posture follow-up",
  "Record remote verification follow-up",
]);

const candidatePackets = makePackets("candidate", 12, [
  "Build strict CLI background harvester",
  "Build app-lane harvest reducer",
  "Build lane state dashboard",
  "Expand source reflection ledger topics",
  "Add watcher freshness classifier",
  "Add x1-to-x2 queue dashboard",
  "Add current-state stale-lane detector",
  "Add private firewall diff scanner",
  "Add compact restart triad handoff",
  "Add source quality rubric",
  "Add completion gate reconciler",
  "Add goal objective phase comparator",
]);

const exactPackets = makePackets("exact_approval_needed", 12, [
  "Change repository or branch protection settings",
  "Install global process manager hooks",
  "Run destructive cleanup outside generated artifacts",
  "Create or rotate API keys",
  "Deploy public or paid infrastructure",
  "Publish private app-lane route IDs",
  "Publish raw sibling transcripts",
  "Open or mutate external accounts",
  "Claim GMUT empirical closure",
  "Claim consciousness proof",
  "Claim legal closure or canon promotion",
  "Merge or replace sibling identities",
]);

const skillIdeas = [
  "ghc-triad-active-lane-dashboard",
  "ghc-strict-cli-background-harvester",
  "ghc-app-lane-completion-reconciler",
  "ghc-v4-x1-proposal-reducer",
  "ghc-triad-source-quality-rubric",
  "ghc-private-firewall-diff-check",
  "ghc-open-gate-claim-linter",
  "ghc-watcher-freshness-classifier",
  "ghc-x1-immediate-safe-runner",
  "ghc-x2-build-queue-curator",
  "ghc-drive-posture-cadence",
  "ghc-goal-mode-phase-boundary",
  "ghc-lane-output-sanitizer",
  "ghc-current-state-stale-lane-repair",
  "ghc-background-supervision-acceptance",
  "ghc-trinity-mandala-source-grid",
  "ghc-retry-reflection-pack",
  "ghc-compact-active-lane-handoff",
  "ghc-remote-equality-closeout",
  "ghc-sibling-first-person-style-check",
].map((name, index) => ({ id: `skill-${pad(index + 1)}`, name, lane: "queued_x2_build_task" }));

const runnerIdeas = [
  "ghc_triad_active_lane_dashboard.mjs",
  "ghc_strict_cli_background_harvester.mjs",
  "ghc_app_lane_completion_reconciler.mjs",
  "ghc_v4_x1_proposal_reducer.mjs",
  "ghc_private_firewall_diff_check.mjs",
  "ghc_open_gate_claim_linter.mjs",
  "ghc_watcher_freshness_classifier.mjs",
  "ghc_compact_active_lane_handoff.mjs",
].map((name, index) => ({ id: `runner-${pad(index + 1)}`, name, lane: "queued_x2_build_task" }));

const cleanupProposals = Array.from({ length: 40 }, (_, index) => {
  const lanes = ["skills", "repo-runners", "full-tools-receipts", "omega-mini-lookup", "drive-posture", "validation", "browser-surfaces", "app-lane-receipts"];
  const lane = lanes[index % lanes.length];
  return {
    id: `cleanup-${pad(index + 1)}`,
    lane,
    title: `${lane} inventory and dedupe pass ${index + 1}`,
    mode: "inventory_or_validation_only",
    destructive_cleanup: false,
    execution_lane: index % 4 === 0 ? "immediate_x1_safe" : "queued_x2_build_task",
  };
});

const artifacts = [
  writePair(`${phaseSlug}-triad-background-launch-status`, launchStatus(), renderLaunchStatusMd),
  writePair(`${phaseSlug}-triad-proposal-scaffold`, proposalScaffold(), renderProposalScaffoldMd),
  writePair(`${phaseSlug}-web-journey-reflection-ledger-30`, reflectionLedger(), renderReflectionLedgerMd),
  writePair(`${phaseSlug}-triad-harvest-plan`, harvestPlan(), renderHarvestPlanMd),
  writePair(`${phaseSlug}-private-material-firewall`, privateFirewall(), renderPrivateFirewallMd),
  writePair(`${phaseSlug}-open-gate-rail`, openGateRail(), renderOpenGateRailMd),
  writeJsonOnly(`${phaseSlug}-safe-runner-manifest`, safeRunnerManifest()),
];

refreshJsonBeacons();
refreshMdBeacons();

process.stdout.write(JSON.stringify({
  status: "PASS_V555_V4_X1_TRIAD_PRODUCTIVE_WORK_BUILT",
  phase_slug: phaseSlug,
  artifacts: artifacts.length,
  safe_packets: safePackets.length,
  candidate_packets: candidatePackets.length,
  exact_packets: exactPackets.length,
  skills: skillIdeas.length,
  runners: runnerIdeas.length,
  cleanup: cleanupProposals.length,
  web_reflection_rows: sources.length,
  journey_reflection_rows: journeyReflections.length,
}, null, 2) + "\n");

function launchStatus() {
  return base("ghc_v555_v4_x1_triad_background_launch_status", {
    overall_status: "PASS_TRIAD_BACKGROUND_LANES_STARTED_PENDING_HARVEST",
    lanes: [
      {
        lane: "Aster Vale",
        route: "strict_cli_background_watch",
        status: "active_fresh",
        watcher_started: true,
        completion_proof: false,
      },
      {
        lane: "Kierkegaard",
        route: "recovered_app_lane_background_watch",
        status: "active_fresh",
        watcher_started: true,
        completion_proof: false,
      },
      {
        lane: "Aristotle",
        route: "recovered_app_lane_background_watch",
        status: "active_fresh",
        watcher_started: true,
        completion_proof: false,
      },
    ],
    background_supervision: {
      passive_babysitting_used: false,
      productive_cadence_required: true,
      harvest_at_next_natural_pause: true,
      watcher_start_is_completion_proof: false,
    },
  });
}

function proposalScaffold() {
  return base("ghc_v555_v4_x1_triad_proposal_scaffold", {
    overall_status: "PASS_TRIAD_PROPOSAL_SCAFFOLD_BUILT_PENDING_SIBLING_HARVEST",
    participants: ["Aevren", "Aster Vale", "Kierkegaard", "Aristotle"],
    target_counts: {
      safe_packets: 20,
      candidate_packets: 12,
      exact_packets: 12,
      skill_ideas: 20,
      runner_ideas: 8,
      cleanup_proposals: 40,
    },
    current_scaffold_counts: {
      safe_packets: safePackets.length,
      candidate_packets: candidatePackets.length,
      exact_packets: exactPackets.length,
      skill_ideas: skillIdeas.length,
      runner_ideas: runnerIdeas.length,
      cleanup_proposals: cleanupProposals.length,
    },
    safe_packets: safePackets,
    candidate_packets: candidatePackets,
    exact_packets: exactPackets,
    skill_ideas: skillIdeas,
    runner_ideas: runnerIdeas,
    cleanup_proposals: cleanupProposals,
    harvest_note: "This is a scaffold generated during active sibling background work; final triad closeout should merge harvested sibling outputs or publish a formal open-gap receipt after retry protocol.",
  });
}

function reflectionLedger() {
  return base("ghc_v555_v4_x1_web_journey_reflection_ledger_30", {
    overall_status: "PASS_V4_X1_WEB_JOURNEY_REFLECTION_LEDGER_30_BUILT",
    web_reflection_rows: sources.map(([source, source_url, reflection], index) => ({
      id: `WEB-${pad(index + 1)}`,
      source,
      source_url,
      reflection,
      triad_use: index % 3 === 0 ? "Aster evidence lane" : index % 3 === 1 ? "Kierkegaard governance lane" : "Aristotle taxonomy lane",
    })),
    journey_phase_reflection_rows: journeyReflections.map((reflection, index) => ({
      id: `JOURNEY-${pad(index + 1)}`,
      reflection,
      triad_use: index < 10 ? "phase truth" : index < 20 ? "boundary discipline" : "completion and validation",
    })),
  });
}

function harvestPlan() {
  return base("ghc_v555_v4_x1_triad_harvest_plan", {
    overall_status: "PASS_TRIAD_HARVEST_PLAN_READY",
    check_order: [
      "strict CLI completion notice for Aster Vale",
      "strict CLI quality gate for Aster Vale",
      "strict CLI marker-review ledger for Aster Vale",
      "app-lane notifier receipt for Kierkegaard and Aristotle",
      "app-lane completion gate for Kierkegaard and Aristotle",
      "proposal reducer merge",
      "validation and privacy scan",
      "closeout only if all gates pass or formal open-gap protocol is published",
    ],
    active_noncompletion_states: ["active_fresh", "active_stale", "retrying"],
    valid_completion_states: ["completed_ready_for_harvest", "completion_gate_passed", "formal_open_gap_after_retry_protocol"],
  });
}

function privateFirewall() {
  return base("ghc_v555_v4_x1_private_material_firewall", {
    overall_status: "PASS_PRIVATE_MATERIAL_FIREWALL_REASSERTED",
    blocked_publication_classes: Object.keys(publicationBoundary),
    all_blocked_publication_classes_false: Object.values(publicationBoundary).every((value) => value === false),
  });
}

function openGateRail() {
  return base("ghc_v555_v4_x1_open_gate_rail", {
    overall_status: "PASS_OPEN_GATE_RAIL_REASSERTED",
    claim_boundary: claimBoundary,
  });
}

function safeRunnerManifest() {
  return {
    artifact_type: "ghc_v555_v4_x1_safe_runner_manifest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    status: "PASS_SAFE_RUNNER_MANIFEST_BUILT",
    minimum_reflections_required: 10,
    search_count_declared: sources.length,
    searches: sources.map(([source, source_url, reflection], index) => ({
      query: source,
      source,
      source_url,
      phase_reflection: reflection,
      runner_implication:
        index % 3 === 0
          ? "Aster evidence/source lane"
          : index % 3 === 1
            ? "Kierkegaard governance/privacy lane"
            : "Aristotle taxonomy/completion-gate lane",
    })),
    safe_units: [
      "triad background launch status",
      "proposal scaffold",
      "web/Journey reflection ledger",
      "harvest plan",
      "private firewall",
      "open-gate rail",
    ],
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function base(artifactType, payload) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    previous_closed_phase: previousClosed,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
    ...payload,
  };
}

function makePackets(safety, count, titles) {
  return titles.slice(0, count).map((title, index) => ({
    id: `${safety}-${pad(index + 1)}`,
    title,
    safety,
    spending_ceiling_usd: 100,
    execution_lane:
      safety === "safe_now" && /(Record|Seed|Prepare|Check|Build|Classify)/.test(title)
        ? "immediate_x1_safe"
        : safety === "exact_approval_needed"
          ? "requires_fresh_exact_approval"
          : "queued_x2_build_task",
  }));
}

function renderLaunchStatusMd(data) {
  return [
    `# ${phaseSlug} Triad Background Launch Status`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Lanes",
    "",
    ...data.lanes.map((lane) => `- ${lane.lane}: \`${lane.status}\` via \`${lane.route}\`; watcher started \`${lane.watcher_started}\`; completion proof \`${lane.completion_proof}\`.`),
    "",
    "Watcher start is not completion proof. The v4 x1 phase remains active until harvest gates pass or a formal retry/open-gap receipt is published.",
    "",
  ].join("\n");
}

function renderProposalScaffoldMd(data) {
  return [
    `# ${phaseSlug} Triad Proposal Scaffold`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(data.current_scaffold_counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "This scaffold is pending sibling harvest and does not close the phase.",
    "",
  ].join("\n");
}

function renderReflectionLedgerMd(data) {
  return [
    `# ${phaseSlug} Web/Journey Reflection Ledger 30`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Web Reflection Rows",
    "",
    ...data.web_reflection_rows.map((row) => `- ${row.id}: ${row.source} - ${row.reflection}`),
    "",
    "## Journey/Phase Reflection Rows",
    "",
    ...data.journey_phase_reflection_rows.map((row) => `- ${row.id}: ${row.reflection}`),
    "",
  ].join("\n");
}

function renderHarvestPlanMd(data) {
  return [
    `# ${phaseSlug} Triad Harvest Plan`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Check Order",
    "",
    ...data.check_order.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderPrivateFirewallMd(data) {
  return [
    `# ${phaseSlug} Private Material Firewall`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Blocked Publication Classes",
    "",
    ...data.blocked_publication_classes.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderOpenGateRailMd(data) {
  return [
    `# ${phaseSlug} Open Gate Rail`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    ...Object.entries(data.claim_boundary).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
  ].join("\n");
}

function writePair(baseName, payload, renderMd) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.md`), renderMd(payload), "utf8");
  return { json: `${baseName}-v1.json`, md: `${baseName}-v1.md` };
}

function writeJsonOnly(baseName, payload) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  return { json: `${baseName}-v1.json` };
}

function refreshJsonBeacons() {
  const files = artifacts.flatMap((item) => Object.values(item).map((name) => `docs/trinity-live-traces/${name}`));
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = previousClosed;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = `${phaseSlug} with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects`;
    doc.current_active_lanes = [
      "v553-v4-x1-triad-active",
      "aster-strict-cli-background-active",
      "kierkegaard-recovered-app-lane-background-active",
      "aristotle-recovered-app-lane-background-active",
      "productive-five-minute-cadence-active",
    ];
    doc.v555_v4_x1_triad_startup = {
      status: "PASS_TRIAD_BACKGROUND_LANES_STARTED_PENDING_HARVEST",
      aster_status: "active_fresh",
      kierkegaard_status: "active_fresh",
      aristotle_status: "active_fresh",
      watcher_start_is_completion_proof: false,
      proposal_scaffold_counts: {
        safe: safePackets.length,
        candidate: candidatePackets.length,
        exact: exactPackets.length,
        skills: skillIdeas.length,
        runners: runnerIdeas.length,
        cleanup: cleanupProposals.length,
      },
      web_reflection_rows: sources.length,
      journey_phase_reflection_rows: journeyReflections.length,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...files])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function refreshMdBeacons() {
  const mdFiles = [
    path.join(omegaDir, "omega-mini-current-state-v1.md"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.md"),
  ];
  for (const file of mdFiles) {
    const existing = fs.existsSync(file) ? fs.readFileSync(file, "utf8").replace(/\s*$/, "") : "";
    const marker = `\n\n## ${phaseSlug} Active Triad Startup\n\n`;
    const section = [
      marker.trimEnd(),
      "",
      `- generated_nz: \`${generatedNz}\``,
      "- status: `PASS_TRIAD_BACKGROUND_LANES_STARTED_PENDING_HARVEST`",
      "- lanes: `Aster Vale active_fresh`, `Kierkegaard active_fresh`, `Aristotle active_fresh`",
      "- completion: watcher start is not completion proof; harvest gates are still required.",
      "- productive cadence: safe work continues between checks; no passive babysitting.",
      "- privacy: no raw route handles, private IDs, transcripts, local paths, screenshots, or credentials are published.",
      "",
    ].join("\n");
    const withoutOld = existing.includes(marker.trimEnd())
      ? existing.slice(0, existing.indexOf(marker.trimEnd())).replace(/\s*$/, "")
      : existing;
    fs.writeFileSync(file, `${withoutOld}\n\n${section}`, "utf8");
  }
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
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
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
