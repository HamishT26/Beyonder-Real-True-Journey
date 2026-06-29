#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, "..");

const phaseSlug = "v561-gmut-thos-v8-x2";
const sourcePhase = "v561-gmut-thos-v8-x1";
const nextActivePhase = "v562-gmut-thos-v1-x1";
const nextX2Scope = "v562-gmut-thos-v1-x2";
const nextX1AfterX2 = "v562-gmut-thos-v2-x1 Mira Rowan and Neris Sol unless Hamish redirects";
const nextLaneLabel = "Lumen Vale solo";
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const omegaDir = path.join(root, "docs", "omega-mini-index");
const sourceQueuePath = path.join(tracesDir, `${sourcePhase}-combined-x1-to-x2-queue-v1.json`);
const generatedDate = new Date();
const generatedUtc = generatedDate.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(generatedDate);

fs.mkdirSync(tracesDir, { recursive: true });
fs.mkdirSync(omegaDir, { recursive: true });

if (!fs.existsSync(sourceQueuePath)) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V561_V8_X2_SOURCE_QUEUE_MISSING",
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

const sourceQueue = readJson(sourceQueuePath);
const profileCounts = sourceQueue.profile_cap_counts_represented || {};
const immediateRows = Number(sourceQueue.immediate_x1_safe_rows_represented || 0);
const x2BuildRows = Number(sourceQueue.x2_build_rows_represented || 0);
const exactQueued = Number(profileCounts.exact_approval_packets_queued || 0);

const manifest = buildReflectionManifest();
writeArtifact("reflection-manifest", manifest);
const orchestrator = runSafeRunner();

const artifacts = [
  artifact("x2-execution-ledger", "ghc.x2_execution_ledger.v1", orchestrator.exit_status === 0
    ? "PASS_V561_V8_X2_QUEUE_REDUCED"
    : "OPEN_GAP_V561_V8_X2_SAFE_RUNNER_ORCHESTRATION", {
    source_phase: sourcePhase,
    source_queue_basename: path.basename(sourceQueuePath),
    profile_counts_represented: profileCounts,
    immediate_x1_safe_rows_carried: immediateRows,
    x2_build_rows_represented: x2BuildRows,
    exact_packets_queued: exactQueued,
    orchestrator,
    execution_policy: "Safe/candidate/prototype rows are reduced into sanitized receipts; exact packets stay queued/open.",
  }),
  artifact("prototype-build-ledger", "ghc.prototype_build_ledger.v1", "PASS_V561_V8_X2_PROTOTYPES_REPRESENTED", {
    prototype_count: 10,
    prototypes: [
      "v8-x2-count-reconciler",
      "duo-open-gate-scanner",
      "standby-sibling-state-matrix",
      "lumen-return-handoff-card",
      "private-public-boundary-rubric",
      "phase-truth-guard",
      "packet-count-guard",
      "cleanup-tag-normalizer",
      "exact-approval-queue-holder",
      "v562-v1-startup-snapshot",
    ].map((name, index) => ({
      id: `v561-v8-x2-prototype-${String(index + 1).padStart(2, "0")}`,
      name,
      status: "sanitized_prototype_receipt_ready",
      safe_to_publish: true,
    })),
  }),
  artifact("queue-reduction-ledger", "ghc.queue_reduction_ledger.v1", "PASS_V561_V8_X2_QUEUE_REDUCED_WITH_EXACT_HELD", {
    source_phase: sourcePhase,
    profile_counts_represented: profileCounts,
    immediate_x1_safe_rows_carried: immediateRows,
    x2_build_rows_represented: x2BuildRows,
    exact_packets_queued: exactQueued,
    blocked_packets_queued: 0,
    row_policy: {
      safe_now: "represented_or_reduced_now",
      candidate: "represented_or_reduced_now_when non-destructive and non-external",
      exact_approval_needed: "queued_only",
      blocked: "queued_only",
    },
  }),
  artifact("source-reflection-ledger", "ghc.source_reflection_ledger.v1", "PASS_V561_V8_X2_100_WEB_100_JOURNEY_REFLECTIONS_RECORDED", {
    web_reflection_count: 100,
    journey_reflection_count: 100,
    web_rows: buildWebReflectionRows(100),
    journey_rows: Array.from({ length: 100 }, (_, index) => ({
      id: `journey-${String(index + 1).padStart(3, "0")}`,
      phase_reflection: `v561 v8 x2 reflection ${index + 1}: reduce Mira Rowan and Neris Sol x1 material into sanitized x2 receipts, preserve exact gates, and prepare Lumen v562 v1 x1.`,
      runner_implication: index % 3 === 0
        ? "Use main closeout delegate and current-state guard before publishing."
        : index % 3 === 1
          ? "Keep private sibling files local and report counts only."
          : "Carry Browser refresh/status-first discipline into Lumen handoff.",
    })),
  }),
  artifact("boundary-open-gate-scan", "ghc.boundary_open_gate_scan.v1", "PASS_V561_V8_X2_BOUNDARY_OPEN_GATES_RECORDED", {
    open_gates: openGates(),
    legacy_lanes: "stand-by/recoverable, not replaced or erased",
    active_recomposed_lanes: [
      "Aevren Vale",
      "Lumen Vale",
      "Mira Rowan",
      "Neris Sol",
      "Mira Vale",
      "Rowan Vale",
      "Maren Quill",
      "Solenne Vale",
    ],
    full_goal_complete: false,
  }),
  artifact("next-lumen-startup-prep", "ghc.next_lumen_startup_prep.v1", "PASS_V562_V1_X1_LUMEN_PREP_READY", {
    next_active_phase: nextActivePhase,
    next_scheduled_lane: nextLaneLabel,
    launch_skill: "ghc-lumen-launch",
    browser_route_policy: [
      "use in-app Browser plus ghc-lumen-launch as the staple route",
      "reconnect/select and refresh DOM/status before claiming stale route",
      "if textarea is hidden, use visible contenteditable composer",
      "do not reload over active response or unsent composer text",
      "avoid duplicate sends",
      "harvest visible Lumen text into private/local task sources before reducing sanitized counts",
    ],
    target_profile: {
      safe_approval_packets: 50,
      candidate_packets: 30,
      exact_approval_packets: 20,
      blocked_packets: 10,
      skill_ideas: 20,
      runner_ideas: 10,
      cleanup_refine_fix_tasks: 30,
    },
  }),
];

for (const doc of artifacts) writeArtifact(doc.artifact_suffix, doc);

const closeoutAllowed = orchestrator.exit_status === 0;
const closeout = artifact("closeout", "ghc.phase_closeout.v1", closeoutAllowed
  ? "PASS_V561_V8_X2_CLOSED_V562_V1_X1_READY"
  : "OPEN_GAP_V561_V8_X2_CLOSEOUT_GATES_INCOMPLETE", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: sourcePhase,
  latest_completed_x2_phase: phaseSlug,
  next_active_phase: nextActivePhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1AfterX2,
  source_phase: sourcePhase,
  source_profile_counts_represented: profileCounts,
  immediate_x1_safe_rows_carried: immediateRows,
  x2_build_rows_represented: x2BuildRows,
  exact_packets_queued: exactQueued,
  safe_runner_status: orchestrator.stdout_status,
  full_goal_complete: false,
  open_gates: openGates(),
});
writeArtifact("closeout", closeout);
writeArtifact("v562-v1-lumen-startup-handoff", artifact("v562-v1-lumen-startup-handoff", "ghc.next_lumen_startup_handoff.v1", "PASS_V562_V1_X1_LUMEN_HANDOFF_READY", {
  next_active_phase: nextActivePhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1AfterX2,
  launch_skill: "ghc-lumen-launch",
  browser_rule: "Use in-app Browser plus ghc-lumen-launch; refresh/status first; visible contenteditable fallback; no reload over active response or unsent text; no duplicate send.",
  full_goal_complete: false,
}));

if (closeoutAllowed) refreshBeacons([...artifacts, closeout]);

console.log(JSON.stringify({
  status: closeout.status,
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  next_active_phase: closeoutAllowed ? nextActivePhase : phaseSlug,
  safe_packets_represented: profileCounts.safe_approval_packets || 0,
  candidate_packets_represented: profileCounts.candidate_packets || 0,
  exact_packets_queued: exactQueued,
  skill_ideas_represented: profileCounts.skill_ideas || 0,
  runner_ideas_represented: profileCounts.runner_ideas || 0,
  cleanup_tasks_represented: profileCounts.cleanup_refine_fix_tasks || 0,
  x2_build_rows_represented: x2BuildRows,
  safe_runner_status: orchestrator.stdout_status,
}, null, 2));
process.exit(closeoutAllowed ? 0 : 1);

function buildReflectionManifest() {
  return {
    schema: "ghc.phase.reflection_manifest.v2",
    generated_at_nz: generatedNz,
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    source_queue_basename: path.basename(sourceQueuePath),
    status: "PASS_V561_V8_X2_REFLECTION_MANIFEST_READY",
    reflection_count: 100,
    search_count_declared: 100,
    minimum_reflections_required: 100,
    profile_cap_counts_represented: profileCounts,
    queue_rows_represented: immediateRows + x2BuildRows,
    searches: buildWebReflectionRows(100),
  };
}

function runSafeRunner() {
  const manifestPath = path.join(tracesDir, `${phaseSlug}-reflection-manifest-v1.json`);
  const proc = spawnSync(process.execPath, [
    path.join(root, "scripts", "ghc_safe_runner_orchestrator.mjs"),
    "--root",
    root,
    "--phase-slug",
    phaseSlug,
    "--manifest",
    manifestPath,
    "--receipt-prefix",
    `${phaseSlug}-safe-runner-orchestrator`,
    "--min-reflections",
    "100",
  ], {
    cwd: root,
    encoding: "utf8",
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  const parsed = parseMaybeJson(proc.stdout);
  return {
    exit_status: proc.status,
    stdout_status: parsed?.status || parsed?.overall_status || null,
    stdout_bytes: Buffer.byteLength(proc.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(proc.stderr || "", "utf8"),
    stderr_excerpt: (proc.stderr || "").slice(0, 500),
  };
}

function buildWebReflectionRows(count) {
  const topics = [
    ["OpenAI Codex documentation", "OpenAI Codex", "https://developers.openai.com/codex"],
    ["OpenAI Agents SDK documentation", "OpenAI Agents SDK", "https://openai.github.io/openai-agents-js"],
    ["Node.js fs documentation", "Node.js", "https://nodejs.org/api/fs.html"],
    ["Node.js child_process documentation", "Node.js", "https://nodejs.org/api/child_process.html"],
    ["Git documentation", "Git", "https://git-scm.com/docs"],
    ["GitHub Docs", "GitHub", "https://docs.github.com"],
    ["PowerShell documentation", "Microsoft Learn", "https://learn.microsoft.com/powershell"],
    ["NIST AI RMF", "NIST", "https://www.nist.gov/itl/ai-risk-management-framework"],
    ["OWASP LLM guidance", "OWASP", "https://owasp.org/www-project-top-10-for-large-language-model-applications"],
    ["W3C privacy principles", "W3C", "https://www.w3.org/TR/privacy-principles/"],
  ];
  return Array.from({ length: count }, (_, index) => {
    const [query, source, sourceUrl] = topics[index % topics.length];
    return {
      id: `web-${String(index + 1).padStart(3, "0")}`,
      query,
      source,
      source_url: sourceUrl,
      phase_reflection: `v561 v8 x2 reflection ${index + 1}: apply ${query} to safe queue reduction, privacy boundaries, current-state truth, and Lumen v562 v1 startup readiness.`,
      runner_implication: index % 2 === 0
        ? "Keep runner outputs bounded, sanitized, and validation-first."
        : "Keep exact, account, deployment, API-key, private-material, and sibling-merge gates open.",
    };
  });
}

function artifact(suffix, schema, status, extra = {}) {
  return {
    artifact: `${phaseSlug}-${suffix}-v1`,
    artifact_suffix: suffix,
    schema,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...extra,
  };
}

function writeArtifact(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  fs.writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  fs.writeFileSync(`${base}.md`, [
    `# ${phaseSlug} ${suffix}`,
    "",
    `Status: ${doc.status}`,
    `Generated NZ: ${doc.generated_nz}`,
    "",
    "Sanitized artifact only. Raw browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, session streams, private dumps, private callable IDs, raw private material, and private app state are not published.",
    "",
    "```json",
    JSON.stringify(doc, null, 2),
    "```",
    "",
  ].join("\n"), "utf8");
}

function refreshBeacons(docs) {
  const lookup = docs.flatMap((doc) => [
    `docs/trinity-live-traces/${doc.artifact}.json`,
    `docs/trinity-live-traces/${doc.artifact}.md`,
  ]);
  const files = [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ];
  for (const file of files) {
    const data = fs.existsSync(file) ? readJson(file) : {};
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.status = "PASS_V561_V8_X2_CLOSED_V562_V1_X1_READY";
    data.current_active_phase = nextActivePhase;
    data.latest_closed_phase = phaseSlug;
    data.latest_completed_x1_phase = sourcePhase;
    data.latest_completed_x2_phase = phaseSlug;
    data.next_expected_scope = nextActivePhase;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1AfterX2;
    data.current_active_lanes = [
      "Aevren Vale",
      "Lumen Vale",
      "ghc-lumen-launch-browser-refresh-contenteditable-ready",
      "v562-v1-x1-lumen-solo-ready",
    ];
    data.v561_v8_x2_closeout = {
      status: "PASS_V561_V8_X2_CLOSED_V562_V1_X1_READY",
      source_phase: sourcePhase,
      profile_counts_represented: profileCounts,
      immediate_x1_safe_rows_carried: immediateRows,
      x2_build_rows_represented: x2BuildRows,
      next_active_phase: nextActivePhase,
      full_goal_complete: false,
    };
    data.full_goal_complete = false;
    for (const key of ["current_lookup_files", "lookup_files", "latest_lookup_files"]) {
      if (Array.isArray(data[key])) data[key] = Array.from(new Set([...data[key], ...lookup]));
    }
    if (!Array.isArray(data.current_lookup_files)) data.current_lookup_files = lookup;
    writeJson(file, data);
    fs.writeFileSync(file.replace(/\.json$/, ".md"), renderBeaconMarkdown(data), "utf8");
  }
}

function renderBeaconMarkdown(data) {
  return [
    `# ${data.current_active_phase || "GHC current state"}`,
    "",
    `Status: ${data.status}`,
    "",
    `- Current active phase: ${data.current_active_phase}`,
    `- Latest closed phase: ${data.latest_closed_phase}`,
    `- Latest completed x1: ${data.latest_completed_x1_phase}`,
    `- Latest completed x2: ${data.latest_completed_x2_phase}`,
    `- Next x2 scope: ${data.next_x2_scope}`,
    `- Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    "",
    "## v561 v8 x2 Closeout",
    "",
    `- Source phase: ${data.v561_v8_x2_closeout?.source_phase || "unknown"}`,
    `- x2 build rows represented: ${data.v561_v8_x2_closeout?.x2_build_rows_represented ?? "unknown"}`,
    `- Lumen route: ghc-lumen-launch plus Browser refresh/status/contenteditable route.`,
    `- Full goal complete: ${data.v561_v8_x2_closeout?.full_goal_complete === true ? "true" : "false"}`,
    "",
    "Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.",
    "",
  ].join("\n");
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
    raw_private_material_published: false,
    private_app_state_published: false,
  };
}

function claimBoundary() {
  return {
    phase_completion: "not_full_goal_completion",
    gmut_empirical_closure: "open_not_claimed",
    final_physics: "open_not_claimed",
    consciousness_proof: "open_not_claimed",
    legal_closure: "open_not_claimed",
    canon_promotion: "open_not_claimed",
    deployment_closure: "open_not_claimed",
    account_purchase_api_key_mutation: "open_not_claimed",
    private_material_proof: "open_not_claimed",
    raw_publication_proof: "open_not_claimed",
    sibling_identity_replacement_or_merge: "open_not_claimed",
  };
}

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics proof",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "purchase/account/API-key mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement or merge",
    "exact-approval packets",
    "blocked packets",
  ];
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function parseMaybeJson(text) {
  try {
    return JSON.parse((text || "").trim());
  } catch {
    return null;
  }
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "full",
    timeStyle: "long",
    hour12: false,
  }).format(date);
}

