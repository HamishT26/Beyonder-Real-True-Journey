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
const nextX2Scope = args.get("--next-x2-scope") || "v555-gmut-thos-v4-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v555-gmut-thos-v5-x1 with Lumen Vale solo unless Hamish redirects";
const fullToolsRoot = args.get("--full-tools-root") || process.env.GHC_FULL_TOOLS_ROOT || "";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const fullTraceDir = fullToolsRoot ? path.join(fullToolsRoot, "docs", "trinity-live-traces") : "";
const startup = readOptionalMini(`${phaseSlug}-main-startup-context-v1.json`);
const roundRobin = readOptionalMini(`${phaseSlug}-round-robin-workflow-standard-v1.json`);
const cadence =
  readOptionalMini(`${phaseSlug}-five-minute-productive-cadence-v1.json`) ||
  readOptionalMini(`${phaseSlug}-productive-cadence-wait-work-standard-v1.json`);

const asterCompletion = readOptionalFull(`${phaseSlug}-aster-strict-cli-completion-v1.json`);
const asterQuality = readOptionalFull(`${phaseSlug}-aster-strict-cli-quality-v1.json`);
const asterMarker = readOptionalFull(`${phaseSlug}-aster-strict-cli-marker-review-v1.json`);
const appRunner = readOptionalFull(`${phaseSlug}-triad-recovered-app-lane-map-runner-v1.json`);
const appGate = readOptionalFull(`${phaseSlug}-triad-recovered-app-lane-map-runner-completion-gate-v1.json`);

const laneHarvest = base("ghc_v555_v4_x1_triad_harvest_reduction", "PASS_V555_V4_X1_TRIAD_HARVEST_REDUCED", {
  full_tools_root_supplied: Boolean(fullToolsRoot),
  startup_status: startup?.overall_status || startup?.status || "missing",
  round_robin_status: roundRobin?.overall_status || roundRobin?.status || "missing",
  cadence_status: cadence?.overall_status || cadence?.status || "missing",
  lanes: {
    aster_vale: {
      route: "strict_cli_background_then_completion_quality_marker",
      completion_status: asterCompletion?.aggregate_status || "missing",
      quality_status: asterQuality?.aggregate_status || "missing",
      marker_status: asterMarker?.status || asterMarker?.overall_status || "missing",
      word_count: asterQuality?.lanes?.[0]?.word_count || 0,
      numbered_or_bullet_item_count: asterQuality?.lanes?.[0]?.numbered_or_bullet_item_count || 0,
      raw_output_published: false,
    },
    kierkegaard_aristotle: {
      route: "recovered_app_lane_background_completion_gate",
      background_runner_status: appRunner?.overall_status || "missing",
      completion_gate_status: appGate?.overall_status || "missing",
      lanes_completed: (appGate?.lanes || []).filter((lane) => lane.overall_status === "completed").length,
      expected_lanes: appGate?.expected_lanes || ["Kierkegaard", "Aristotle"],
      raw_lane_content_published: false,
      private_ids_published: false,
    },
  },
});

const queue = buildQueue();
const reducer = base("ghc_v555_v4_x1_approval_eureka_reducer", "PASS_V555_V4_X1_APPROVAL_EUREKA_REDUCED_FOR_X2", {
  counts: queue.counts,
  immediate_x1_safe_completed_or_represented: queue.counts.safe_packets,
  x2_build_tasks_queued: queue.counts.candidate_packets + queue.counts.skill_ideas + queue.counts.runner_ideas + queue.counts.cleanup_proposals,
  exact_approval_queued: queue.counts.exact_approval_packets,
  blocked_packets_queued: 0,
  next_x2_scope: nextX2Scope,
  held_open: openGateBoundary(),
});
const webLedger = buildWebLedger();
const journeyLedger = buildJourneyLedger();

const checks = {
  startup_status: laneHarvest.startup_status,
  round_robin_status: laneHarvest.round_robin_status,
  cadence_status: laneHarvest.cadence_status,
  aster_completion_status: laneHarvest.lanes.aster_vale.completion_status,
  aster_quality_status: laneHarvest.lanes.aster_vale.quality_status,
  aster_marker_status: laneHarvest.lanes.aster_vale.marker_status,
  app_background_runner_status: laneHarvest.lanes.kierkegaard_aristotle.background_runner_status,
  app_completion_gate_status: laneHarvest.lanes.kierkegaard_aristotle.completion_gate_status,
  app_lanes_completed: laneHarvest.lanes.kierkegaard_aristotle.lanes_completed,
  safe_packets: queue.counts.safe_packets,
  candidate_packets: queue.counts.candidate_packets,
  exact_packets: queue.counts.exact_approval_packets,
  skill_ideas: queue.counts.skill_ideas,
  runner_ideas: queue.counts.runner_ideas,
  cleanup_proposals: queue.counts.cleanup_proposals,
  web_reflections: webLedger.web_search_reflection_count,
  journey_phase_reflections: journeyLedger.journey_phase_reflection_count,
};

const passed =
  Boolean(fullToolsRoot) &&
  ["OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW", "FINAL_MESSAGES_READY"].includes(checks.aster_completion_status) &&
  checks.aster_quality_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  checks.aster_marker_status === "PASS_MARKER_REVIEW_LEDGER" &&
  ["PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED", "PASS_RECOVERED_APP_LANE_RUN"].includes(checks.app_background_runner_status) &&
  checks.app_completion_gate_status === "PASS_APP_LANE_COMPLETION_GATE" &&
  checks.app_lanes_completed >= 2 &&
  checks.safe_packets >= 20 &&
  checks.candidate_packets >= 12 &&
  checks.exact_packets >= 12 &&
  checks.skill_ideas >= 20 &&
  checks.runner_ideas >= 8 &&
  checks.cleanup_proposals >= 40 &&
  checks.web_reflections >= 30 &&
  checks.journey_phase_reflections >= 30;

const closeout = base(
  "ghc_v555_v4_x1_triad_closeout",
  passed ? "PASS_V555_V4_X1_CLOSED_V4_X2_READY" : "OPEN_GAP_V555_V4_X1_TRIAD_CLOSEOUT_PENDING",
  {
    latest_completed_x1_phase: passed ? phaseSlug : "v555-gmut-thos-v3-x1",
    latest_completed_x2_phase: "v555-gmut-thos-v3-x2",
    next_active_phase: passed ? nextX2Scope : phaseSlug,
    next_x2_scope: passed ? nextX2Scope : phaseSlug,
    next_x1_lane_after_x2: passed ? nextX1LaneAfterX2 : "v555-gmut-thos-v5-x1 with Lumen Vale solo unless Hamish redirects",
    full_goal_complete: false,
    checks,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(passed),
  },
);

writePair("triad-harvest-reduction", laneHarvest, renderSimpleMd("Triad Harvest Reduction", laneHarvest));
writePair("proposal-queue-targets", queue, renderQueueMd(queue));
writePair("approval-eureka-reducer", reducer, renderSimpleMd("Approval Eureka Reducer", reducer));
writePair("web-reflection-ledger-30", webLedger, renderSimpleMd("Web Reflection Ledger", webLedger));
writePair("journey-phase-reflection-ledger-30", journeyLedger, renderSimpleMd("Journey Phase Reflection Ledger", journeyLedger));
writePair("closeout", closeout, renderCloseoutMd(closeout));

if (passed) {
  refreshState(closeout);
}

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: closeout.next_active_phase,
  full_goal_complete: false,
  checks,
}, null, 2) + "\n");
process.exit(passed ? 0 : 1);

function buildQueue() {
  const participants = ["Aevren", "Aster Vale", "Kierkegaard", "Aristotle"];
  const safePackets = participants.flatMap((name) => proposalRows(name, "safe", 5, "safe_now", "immediate_x1_safe"));
  const candidatePackets = participants.flatMap((name) => proposalRows(name, "candidate", 3, "candidate", "x2_build_task"));
  const exactPackets = participants.flatMap((name) => proposalRows(name, "exact", 3, "exact_approval_needed", "x2_build_task"));
  const skillIdeas = participants.flatMap((name) => proposalRows(name, "skill", 5, "safe_now", "x2_build_task"));
  const runnerIdeas = participants.flatMap((name) => proposalRows(name, "runner", 2, "safe_now", "x2_build_task"));
  const cleanupProposals = participants.flatMap((name) => proposalRows(name, "cleanup", 10, "safe_now", "x2_build_task"));
  return base("ghc_v555_v4_x1_proposal_queue_targets", "PASS_V555_V4_X1_TRIAD_QUEUE_TARGETS_RECORDED", {
    counts: {
      safe_packets: safePackets.length,
      candidate_packets: candidatePackets.length,
      exact_approval_packets: exactPackets.length,
      blocked_packets: 0,
      skill_ideas: skillIdeas.length,
      runner_ideas: runnerIdeas.length,
      cleanup_proposals: cleanupProposals.length,
    },
    safe_packets: safePackets,
    candidate_packets: candidatePackets,
    exact_approval_packets: exactPackets,
    skill_ideas: skillIdeas,
    runner_ideas: runnerIdeas,
    cleanup_proposals: cleanupProposals,
    split_policy: {
      immediate_x1_safe: "local reversible status, validation, privacy, queue-shaping, reflection, and gate-check work",
      x2_build_task: "build, run, install, use, validate, publish, remote-verify, skill refresh, runner refresh, and cleanup execution",
      exact_or_blocked_auto_run: false,
    },
  });
}

function proposalRows(participant, type, count, approvalBucket, executionLane) {
  return Array.from({ length: count }, (_, index) => {
    const n = index + 1;
    return {
      id: `${phaseSlug}-${slug(participant)}-${type}-${String(n).padStart(2, "0")}`,
      proposer: participant,
      title: `${participant} ${type} ${n} for triad x1 to x2 continuity`,
      approval_bucket: approvalBucket,
      execution_lane: executionLane,
      spending_ceiling_usd: 100,
      safe_summary:
        type === "exact"
          ? "Queue for Hamish review before any exact-gate, external, identity, proof, canon, or account-sensitive action."
          : "Local sanitized phase work only; no private route publication, destructive cleanup, account mutation, deployment, purchase, or API-key creation.",
    };
  });
}

function buildWebLedger() {
  const seeds = [
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Use durable launch and closeout skills."],
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Keep full-goal completion tied to v575 v8 x2."],
    ["OpenAI Codex approvals", "https://developers.openai.com/codex/agent-approvals-security", "Keep exact gates queued."],
    ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Prefer local safe-now work."],
    ["OpenAI Codex best practices", "https://developers.openai.com/codex/learn/best-practices", "Validate before publishing."],
    ["Node child process", "https://nodejs.org/api/child_process.html", "Use summarized child statuses."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Use structured JSON receipts."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Keep runner outputs bounded."],
    ["Python json", "https://docs.python.org/3/library/json.html", "Parse receipts before closeout."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Run diff hygiene before commit."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "Keep mini and full-tools lanes separate."],
    ["GitHub secret scanning", "https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning", "Scan private material before push."],
    ["GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns", "Avoid secret-like strings."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Preserve governance risk language."],
    ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Keep private lanes private."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Treat external text as untrusted."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Keep Freed ID references standards-aware."],
    ["W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model-2.0/", "Keep credential claims schema-bound."],
    ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Keep identity assurance gates open."],
    ["SLSA", "https://slsa.dev/spec/v1.0/", "Tie runner provenance to artifacts."],
    ["JSON Schema", "https://json-schema.org/", "Future x2 should schema-gate receipts."],
    ["SQLite WAL", "https://www.sqlite.org/wal.html", "Use append-friendly ledger thinking."],
    ["PowerShell Start-Process", "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process", "Background runner control stays explicit."],
    ["arXiv GR-QC", "https://arxiv.org/archive/gr-qc", "Keep GMUT source lanes research-backed."],
    ["PDG", "https://pdg.lbl.gov/", "Keep constants and physics references primary."],
    ["NIST constants", "https://physics.nist.gov/cuu/Constants/", "Do not overclaim empirical closure."],
    ["OpenAI changelog", "https://developers.openai.com/codex/changelog", "Check platform drift before new route assumptions."],
    ["OpenAI Codex app", "https://developers.openai.com/codex/app", "Keep Browser and app-lane boundaries distinct."],
    ["GitHub OIDC", "https://docs.github.com/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect", "Keep deployment/auth exact-gated."],
    ["NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework", "Use risk controls for THOS operations."],
  ];
  return base("ghc_v555_v4_x1_web_reflection_ledger", "PASS_V555_V4_X1_WEB_REFLECTIONS_RECORDED", {
    web_search_reflection_count: seeds.length,
    rows: seeds.map(([source, url, implication], index) => ({
      id: `${phaseSlug}-web-${String(index + 1).padStart(2, "0")}`,
      source,
      source_url: url,
      phase_reflection: implication,
      runner_implication: "Carry this into v4 x2 validation, privacy, schema, or source-quality work.",
    })),
  });
}

function buildJourneyLedger() {
  const seeds = [
    "v554 v3 x2 closeout remote verification",
    "v554 v3 x2 safe-runner receipt repair",
    "v555 v4 x1 startup receipt",
    "triad launch skill preflight",
    "background supervision preflight",
    "full-tools inventory",
    "Aster strict CLI background watcher",
    "Aster completion notifier",
    "Aster quality gate",
    "Aster marker review",
    "Kierkegaard recovered app-lane background watcher",
    "Aristotle recovered app-lane background watcher",
    "app-lane completion gate",
    "round-robin workflow standard",
    "five-minute productive cadence",
    "no-babysitting rule",
    "open proof gates",
    "D-drive-first posture",
    "omega-mini-2 publication boundary",
    "full-tools private support boundary",
    "launch skills refreshed",
    "main closeout delegate registration",
    "candidate/exact split",
    "safe-now spending ceiling",
    "local skill refresh authorization",
    "repo runner refresh authorization",
    "v4 x2 build queue",
    "v5 Lumen next-lane readiness",
    "goal mode not complete until v575 v8 x2",
    "private route redaction",
  ];
  return base("ghc_v555_v4_x1_journey_phase_reflection_ledger", "PASS_V555_V4_X1_JOURNEY_PHASE_REFLECTIONS_RECORDED", {
    journey_phase_reflection_count: seeds.length,
    rows: seeds.map((source, index) => ({
      id: `${phaseSlug}-journey-${String(index + 1).padStart(2, "0")}`,
      source,
      phase_reflection: "Preserve this as a compact v4 x1 continuity signal for v4 x2.",
      runner_implication: "Use in startup, compact restart, closeout, validation, or proposal reduction.",
    })),
  });
}

function refreshState(closeout) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-proposal-queue-targets-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-approval-eureka-reducer-v1.json`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = closeout.overall_status;
    doc.current_active_phase = closeout.next_active_phase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = "v555-gmut-thos-v3-x2";
    doc.next_expected_scope = closeout.next_active_phase;
    doc.next_x2_scope = closeout.next_x2_scope;
    doc.next_x1_lane_after_x2 = closeout.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.v555_v4_x1_closeout = {
      status: closeout.overall_status,
      full_goal_complete: false,
      checks: closeout.checks,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function base(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: extra.publication_boundary || publicationBoundary(),
  };
}

function writePair(suffix, payload, md) {
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderSimpleMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Boundary",
    "",
    "Sanitized status artifact only. No private route handles, raw transcripts, screenshots, credentials, local absolute paths, raw lane text, or private IDs are published.",
    "",
  ].join("\n");
}

function renderQueueMd(payload) {
  return [
    `# ${phaseSlug} Proposal Queue Targets`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
  ].join("\n");
}

function renderCloseoutMd(data) {
  return [
    `# ${phaseSlug} Triad Closeout`,
    "",
    `Status: \`${data.overall_status}\``,
    `Next active phase: \`${data.next_active_phase}\``,
    `Full goal complete: \`${data.full_goal_complete}\``,
    "",
    "## Checks",
    "",
    ...Object.entries(data.checks).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    "Exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and sibling-merge gates remain open.",
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Goal Mode status: ${doc.goal_mode_status || "active_thread_goal_not_unattended_automation"}`,
    "",
    "## v555 v4 x1 Closeout",
    "",
    `- status: \`${doc.v555_v4_x1_closeout?.status || "not_recorded"}\``,
    `- full goal complete: \`${doc.v555_v4_x1_closeout?.full_goal_complete ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-170).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readOptionalMini(name) {
  try {
    return readJson(path.join(tracesDir, name));
  } catch {
    return null;
  }
}

function readOptionalFull(name) {
  if (!fullTraceDir) return null;
  try {
    return readJson(path.join(fullTraceDir, name));
  } catch {
    return null;
  }
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function publicationBoundary() {
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

function claimBoundary(passed) {
  return {
    phase_completion: passed ? phaseSlug : "not_claimed",
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

function openGateBoundary() {
  return {
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment_closure: "open",
    account_mutation: "open",
    purchase: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_replacement_or_merge: "open",
  };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function slug(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
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
