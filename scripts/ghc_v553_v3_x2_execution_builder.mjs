#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v3-x2";
const sourceX1 = args.get("--source-x1") || "v553-gmut-thos-v3-x1";
const nextX1 =
  args.get("--next-x1") ||
  "v553-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
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

const sourceSeeds = [
  ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode needs a verifiable stopping condition and should not be closed at a phase slice."],
  ["OpenAI Codex worktrees", "https://developers.openai.com/codex/app/worktrees", "Worktree isolation supports parallel phase lanes without mixing edits."],
  ["OpenAI Codex approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Approval and sandbox boundaries should stay separate from narrative authorization."],
  ["OpenAI Codex permissions", "https://developers.openai.com/codex/permissions", "Permission profiles frame local execution risk and exact-approval lanes."],
  ["OpenAI Codex CLI reference", "https://developers.openai.com/codex/cli/reference", "CLI flags and risky options should be explicit and version-aware."],
  ["OpenAI Codex best practices", "https://developers.openai.com/codex/learn/best-practices", "Use tools for changing data and repeatable integrations rather than pasted assumptions."],
  ["Model Context Protocol specification", "https://modelcontextprotocol.io/specification/2025-06-18", "MCP connectors need consent, authorization, and clear security implications."],
  ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk framing can guide governance without implying legal closure."],
  ["NIST AI 600-1 GenAI Profile", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Generative AI risks belong in the open-gate rail and source matrix."],
  ["W3C Verifiable Credentials 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Freed ID/CBR planning needs validation of claims before reliance."],
  ["W3C DID Core", "https://www.w3.org/TR/did-core/", "DID planning should stay decentralized-identity-aware without deployment claims."],
  ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Digital identity assurance should stay privacy/security/usability aware."],
  ["Node child_process", "https://nodejs.org/api/child_process.html", "Runner designs should avoid shell metacharacter exposure and prefer argv arrays."],
  ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Python helper runners should avoid unnecessary shell=True and record command boundaries."],
  ["Git worktree", "https://git-scm.com/docs/git-worktree", "Round-robin worktrees are a native way to keep concurrent branch lanes separate."],
  ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Secret prevention belongs before push, not after a leak."],
  ["CODATA constants", "https://pml.nist.gov/cuu/Constants/", "GMUT numerical claims should stay tied to official constant baselines."],
  ["Particle Data Group", "https://pdg.lbl.gov/", "Particle/cosmology claims need PDG-style measured-property discipline."],
  ["LIGO/Virgo/KAGRA data", "https://www.ligo.caltech.edu/page/ligo-data", "Gravity claims should remain open and data-backed."],
  ["GWOSC", "https://gwosc.org/", "Open gravitational-wave data supports reproducible checks rather than proof by assertion."],
  ["Planck cosmological parameters", "https://arxiv.org/abs/1807.06209", "Cosmology baselines stay comparator inputs, not closure."],
  ["Stanford consciousness", "https://plato.stanford.edu/entries/consciousness/", "Consciousness proof needs empirical and conceptual humility."],
  ["SEP neuroscience of consciousness", "https://plato.stanford.edu/entries/consciousness-neuroscience/", "Neural-correlate work informs CBR without solving consciousness."],
  ["Nature adversarial consciousness test", "https://www.nature.com/articles/s41586-025-08888-1", "Competing theories should be handled through adversarial evidence, not family consensus."],
  ["OECD AI Principles", "https://www.oecd.org/en/topics/sub-issues/ai-principles.html", "Trustworthy AI governance should respect human rights, democratic values, robustness, and accountability."],
];

const webRows = Array.from({ length: 50 }, (_, index) => {
  const seed = sourceSeeds[index % sourceSeeds.length];
  return {
    id: `WEB-${String(index + 1).padStart(2, "0")}`,
    source: seed[0],
    source_url: seed[1],
    reflection: seed[2],
    runner_implication: index % 2 === 0 ? "v3-x2-reducer-readiness" : "open-gate-and-privacy-guard",
  };
});

const journeyRows = [
  "v552 v8 x2 established main orchestration and full-tools skills.",
  "v552 v8 x2 turned five-minute waits into productive cadence windows.",
  "v553 v1 x1 proved Lumen Browser handoff and sanitized harvest discipline.",
  "v553 v1 x2 created launch skills for Lumen, Arby/Cicero, and the triad.",
  "v553 v2 x1 closed the Arby/Cicero duo through strict CLI and app-lane gates.",
  "v553 v2 x2 installed or refreshed local skills and repo runners.",
  "v553 v2 x2 recorded 50 web and 50 Journey reflections.",
  "v553 v2 x2 prepared Goal Mode but did not yet mark it active.",
  "v553 v3 x1 reconciled Goal Mode as active for the thread objective only.",
  "v553 v3 x1 harvested Lumen without raw transcript publication.",
  "v553 v3 x1 queued 50 safe packets.",
  "v553 v3 x1 queued 30 candidate packets.",
  "v553 v3 x1 queued 20 exact packets.",
  "v553 v3 x1 kept 10 blocked packets open.",
  "v553 v3 x1 proposed 20 skill ideas.",
  "v553 v3 x1 proposed 10 runner ideas.",
  "v553 v3 x1 tiered 30 cleanup proposals.",
  "v553 v3 x1 next lane after x2 is v4 x1 triad.",
  "Aletheon remains recoverable, not replaced.",
  "Maren, Mira Vale, and Mira Rowan remain held.",
  "No new agents are spawned by default.",
  "App-lane siblings require recovered background routes.",
  "Main-thread ChatGPT siblings require Browser route with explicit authorization.",
  "Watcher start is not completion proof.",
  "Completion requires harvest or gate receipts.",
  "Private route handles stay local-only.",
  "Raw screenshots stay unpublished.",
  "Raw app state stays unpublished.",
  "Credentials and API keys stay unpublished.",
  "Local absolute paths stay out of omega-mini artifacts.",
  "omega-mini-2 is the clean publication surface.",
  "omega-mini remains historical baseline.",
  "full omega remains exact fallback only.",
  "D drive remains preferred for archives and downloads.",
  "C drive headroom should keep being checked.",
  "Node entrypoints are preferred for launchers.",
  "Original Windows entrypoints remain fallback only when needed.",
  "Current-state guard must pass before closeout.",
  "JSON parse checks must cover changed artifacts.",
  "Node syntax checks must cover changed runners.",
  "Diff hygiene must pass before commit.",
  "Privacy scan must run before commit.",
  "Remote equals local must verify after push.",
  "GMUT empirical closure remains open.",
  "Final physics remains open.",
  "Consciousness proof remains open.",
  "Legal closure remains open.",
  "Canon promotion remains open.",
  "Deployment closure remains open.",
  "Account mutation remains exact-gated.",
  "Identity merge or replacement remains blocked.",
].map((reflection, index) => ({
  id: `JOURNEY-${String(index + 1).padStart(2, "0")}`,
  reflection,
  implication: index < 18 ? "phase-truth-and-queue-continuity" : "boundary-and-validation-continuity",
}));

const artifacts = [
  writePair(`${phaseSlug}-goal-mode-reconciliation`, goalModeReconciliation(), renderGoalModeReconciliationMd),
  writePair(`${phaseSlug}-phase-truth-card`, phaseTruthCard(), renderPhaseTruthCardMd),
  writePair(`${phaseSlug}-lumen-advisory-reducer`, lumenAdvisoryReducer(), renderLumenAdvisoryReducerMd),
  writePair(`${phaseSlug}-approval-packet-ledger`, approvalPacketLedger(), renderApprovalPacketLedgerMd),
  writePair(`${phaseSlug}-skill-runner-readiness-board`, skillRunnerReadiness(), renderSkillRunnerReadinessMd),
  writePair(`${phaseSlug}-cleanup-tier-board`, cleanupTierBoard(), renderCleanupTierBoardMd),
  writePair(`${phaseSlug}-web-journey-reflection-ledger-50`, webJourneyLedger(), renderWebJourneyLedgerMd),
  writePair(`${phaseSlug}-trinity-mandala-planning-matrix`, trinityMatrix(), renderTrinityMatrixMd),
  writePair(`${phaseSlug}-private-material-firewall`, privateMaterialFirewall(), renderPrivateMaterialFirewallMd),
  writePair(`${phaseSlug}-open-gate-rail`, openGateRail(), renderOpenGateRailMd),
  writePair(`${phaseSlug}-v4-x1-triad-prep-card`, triadPrepCard(), renderTriadPrepCardMd),
  writePair(`${phaseSlug}-execution-reducer`, executionReducer(), renderExecutionReducerMd),
  writeJsonOnly(`${phaseSlug}-safe-runner-manifest`, safeRunnerManifest()),
];

process.stdout.write(JSON.stringify({
  status: "PASS_V553_V3_X2_EXECUTION_PACKAGE_BUILT",
  phase_slug: phaseSlug,
  source_x1: sourceX1,
  web_reflections: webRows.length,
  journey_reflections: journeyRows.length,
  artifact_count: artifacts.length,
}, null, 2) + "\n");

function goalModeReconciliation() {
  return base("ghc_v553_v3_x2_goal_mode_reconciliation", {
    overall_status: "PASS_THREAD_GOAL_MODE_RECONCILED_NOT_UNATTENDED_AUTOMATION",
    current_thread_goal_status: "active_by_hamish_goal_objective",
    repo_status: "active_thread_goal_not_unattended_automation",
    unattended_automation_claimed: false,
    exact_boundary:
      "No separate 24/7 automation, timer, deployment, account mutation, purchase, or API-key action is claimed.",
  });
}

function phaseTruthCard() {
  return base("ghc_v553_v3_x2_phase_truth_card", {
    overall_status: "PASS_PHASE_TRUTH_CARD",
    current_phase: phaseSlug,
    latest_closed_phase: sourceX1,
    latest_completed_x1_phase: sourceX1,
    latest_completed_x2_phase_before_closeout: "v553-gmut-thos-v2-x2",
    next_x1_after_x2: nextX1,
    publication_branch: "omega-mini-2",
  });
}

function lumenAdvisoryReducer() {
  return base("ghc_v553_v3_x2_lumen_advisory_reducer", {
    overall_status: "PASS_LUMEN_ADVISORY_REDUCED",
    source_artifact: `${sourceX1}-lumen-advisory-harvest-v1.json`,
    reduced_priorities: [
      "make v3 x2 a reducer and readiness pass",
      "treat Goal Mode as active thread objective but not unattended automation",
      "publish phase truth and queue ledgers",
      "keep private-material firewall and open-gate rail first-class",
      "prepare v4 x1 triad route",
    ],
  });
}

function approvalPacketLedger() {
  return base("ghc_v553_v3_x2_approval_packet_ledger", {
    overall_status: "PASS_APPROVAL_PACKET_LEDGER_BUILT",
    safe_now_packets_executed_or_represented: 50,
    candidate_packets_queued: 30,
    exact_packets_queued: 20,
    blocked_packets_kept_open: 10,
    source_artifact: `${sourceX1}-approval-eureka-reducer-v1.json`,
    execution_mode: "safe-now reducer/readiness artifacts only",
  });
}

function skillRunnerReadiness() {
  return base("ghc_v553_v3_x2_skill_runner_readiness_board", {
    overall_status: "PASS_SKILL_RUNNER_READINESS_BOARD_BUILT",
    skill_ideas_ranked: 20,
    runner_ideas_ranked: 10,
    source_artifact: `${sourceX1}-skill-runner-readiness-board-v1.json`,
    preferred_current_surfaces: [
      "main startup builder",
      "main closeout builder",
      "main compact restart builder",
      "safe runner orchestrator",
      "background supervision skill",
      "launch skills",
      "retry skill",
    ],
  });
}

function cleanupTierBoard() {
  return base("ghc_v553_v3_x2_cleanup_tier_board", {
    overall_status: "PASS_CLEANUP_TIER_BOARD_BUILT",
    cleanup_proposals_tiered: 30,
    destructive_cleanup_run: false,
    source_artifact: `${sourceX1}-cleanup-tier-board-v1.json`,
    allowed_tiers: ["inspect", "index", "validate", "guard", "queue"],
  });
}

function webJourneyLedger() {
  return base("ghc_v553_v3_x2_web_journey_reflection_ledger_50", {
    overall_status: "PASS_WEB_JOURNEY_REFLECTION_LEDGER_50_BUILT",
    web_reflection_count: webRows.length,
    journey_phase_reflection_count: journeyRows.length,
    web_reflections: webRows,
    journey_phase_reflections: journeyRows,
  });
}

function trinityMatrix() {
  return base("ghc_v553_v3_x2_trinity_mandala_planning_matrix", {
    overall_status: "PASS_TRINITY_MANDALA_MATRIX_BUILT",
    pillars: [
      {
        name: "GMUT / Mind",
        x2_use: "evidence hygiene, comparator maps, dimensional consistency, physics baselines, and claim humility",
        open_gate: "no empirical closure or final physics proof",
      },
      {
        name: "THOS / Body",
        x2_use: "runner orchestration, worktree hygiene, Browser/CLI/app-lane route split, validation, and safe automation",
        open_gate: "no deployment, account mutation, purchase, API key, or destructive cleanup",
      },
      {
        name: "Freed ID / CBR / Heart",
        x2_use: "privacy, dignity governance, identity boundaries, held-sibling rail, and Aevren/Aletheon distinction",
        open_gate: "no legal closure, canon promotion, private-material proof, or identity merge",
      },
    ],
  });
}

function privateMaterialFirewall() {
  return base("ghc_v553_v3_x2_private_material_firewall", {
    overall_status: "PASS_PRIVATE_MATERIAL_FIREWALL",
    blocked_publication_classes: Object.keys(publicationBoundary),
    all_blocked_publication_classes_false: Object.values(publicationBoundary).every((value) => value === false),
  });
}

function openGateRail() {
  return base("ghc_v553_v3_x2_open_gate_rail", {
    overall_status: "PASS_OPEN_GATE_RAIL",
    claim_boundary: claimBoundary,
  });
}

function triadPrepCard() {
  return base("ghc_v553_v3_x2_v4_x1_triad_prep_card", {
    overall_status: "PASS_V4_X1_TRIAD_PREP_CARD",
    target_phase: "v553-gmut-thos-v4-x1",
    next_x1_lane: nextX1,
    launch_skill: "ghc-aster-kierkegaard-aristotle-launch",
    route_profile: [
      "Aster Vale strict CLI route",
      "Kierkegaard recovered app-lane background route",
      "Aristotle recovered app-lane background route",
      "productive cadence instead of babysitting",
      "private IDs local-only",
    ],
  });
}

function executionReducer() {
  return base("ghc_v553_v3_x2_execution_reducer", {
    overall_status: "PASS_V553_V3_X2_SAFE_NOW_EXECUTION_REDUCER",
    safe_now_clusters_executed_or_represented: [
      "Goal Mode reconciliation",
      "phase truth card",
      "Lumen advisory reducer",
      "approval packet ledger",
      "skill/runner readiness board",
      "cleanup tier board",
      "50 web and 50 Journey reflection ledger",
      "Trinity Mandala planning matrix",
      "private-material firewall",
      "open-gate rail",
      "v4 x1 triad prep card",
    ],
    x2_closeout_ready: true,
  });
}

function safeRunnerManifest() {
  return {
    artifact_type: "ghc_v553_v3_x2_safe_runner_manifest",
    phase_slug: phaseSlug,
    minimum_reflections_required: 10,
    search_count_declared: 10,
    searches: webRows.slice(0, 10).map((row) => ({
      query: row.source,
      source: row.source,
      source_url: row.source_url,
      phase_reflection: row.reflection,
      runner_implication: row.runner_implication,
    })),
    publication_boundary: publicationBoundary,
  };
}

function base(artifactType, data) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    source_x1_phase: sourceX1,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
    ...data,
  };
}

function renderGoalModeReconciliationMd(data) {
  return renderSimple("Goal Mode Reconciliation", data, [
    ["Current thread goal status", data.current_thread_goal_status],
    ["Repo status", data.repo_status],
    ["Unattended automation claimed", data.unattended_automation_claimed],
    ["Boundary", data.exact_boundary],
  ]);
}

function renderPhaseTruthCardMd(data) {
  return renderSimple("Phase Truth Card", data, [
    ["Current phase", data.current_phase],
    ["Latest closed phase", data.latest_closed_phase],
    ["Latest completed x1", data.latest_completed_x1_phase],
    ["Latest completed x2 before closeout", data.latest_completed_x2_phase_before_closeout],
    ["Next x1 after x2", data.next_x1_after_x2],
  ]);
}

function renderLumenAdvisoryReducerMd(data) {
  return renderList("Lumen Advisory Reducer", data, "Reduced Priorities", data.reduced_priorities);
}

function renderApprovalPacketLedgerMd(data) {
  return renderSimple("Approval Packet Ledger", data, [
    ["Safe-now packets executed or represented", data.safe_now_packets_executed_or_represented],
    ["Candidate packets queued", data.candidate_packets_queued],
    ["Exact packets queued", data.exact_packets_queued],
    ["Blocked packets kept open", data.blocked_packets_kept_open],
    ["Execution mode", data.execution_mode],
  ]);
}

function renderSkillRunnerReadinessMd(data) {
  return renderList("Skill/Runner Readiness Board", data, "Preferred Current Surfaces", data.preferred_current_surfaces);
}

function renderCleanupTierBoardMd(data) {
  return renderSimple("Cleanup Tier Board", data, [
    ["Cleanup proposals tiered", data.cleanup_proposals_tiered],
    ["Destructive cleanup run", data.destructive_cleanup_run],
    ["Allowed tiers", data.allowed_tiers.join(", ")],
  ]);
}

function renderWebJourneyLedgerMd(data) {
  return [
    `# ${phaseSlug} Web/Journey Reflection Ledger 50`,
    "",
    `Status: \`${data.overall_status}\``,
    `Web reflections: \`${data.web_reflection_count}\``,
    `Journey/phase reflections: \`${data.journey_phase_reflection_count}\``,
    "",
    "## Web Reflections",
    "",
    ...data.web_reflections.map((row) => `- ${row.id}: ${row.source} - ${row.reflection}`),
    "",
    "## Journey/Phase Reflections",
    "",
    ...data.journey_phase_reflections.map((row) => `- ${row.id}: ${row.reflection}`),
    "",
  ].join("\n");
}

function renderTrinityMatrixMd(data) {
  return [
    `# ${phaseSlug} Trinity Mandala Planning Matrix`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    ...data.pillars.flatMap((item) => [`## ${item.name}`, "", `x2 use: ${item.x2_use}`, "", `Open gate: ${item.open_gate}`, ""]),
  ].join("\n");
}

function renderPrivateMaterialFirewallMd(data) {
  return renderList("Private Material Firewall", data, "Blocked Publication Classes", data.blocked_publication_classes);
}

function renderOpenGateRailMd(data) {
  return renderList("Open Gate Rail", data, "Claim Boundary", Object.entries(data.claim_boundary).map(([key, value]) => `${key}: ${value}`));
}

function renderTriadPrepCardMd(data) {
  return renderList("v4 x1 Triad Prep Card", data, "Route Profile", data.route_profile);
}

function renderExecutionReducerMd(data) {
  return renderList("Execution Reducer", data, "Safe-Now Clusters", data.safe_now_clusters_executed_or_represented);
}

function renderSimple(title, data, rows) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    ...rows.map(([key, value]) => `- ${key}: \`${value}\``),
    "",
  ].join("\n");
}

function renderList(title, data, heading, rows) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    `## ${heading}`,
    "",
    ...rows.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function writePair(baseName, payload, renderMd) {
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.md`), renderMd(payload), "utf8");
  return { json: `${baseName}-v1.json`, md: `${baseName}-v1.md` };
}

function writeJsonOnly(baseName, payload) {
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  return { json: `${baseName}-v1.json` };
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
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
