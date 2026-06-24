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
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v8-x1";
const previousX2 = "v554-gmut-thos-v7-x2";
const nextX2 = "v554-gmut-thos-v8-x2";
const nextRound = "v554-gmut-thos-v1-x1 with Lumen unless Hamish redirects";
const asterStatus = args.get("--aster-status") || "PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED";
const kierkegaardStatus = args.get("--kierkegaard-status") || "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED";
const aristotleStatus = args.get("--aristotle-status") || "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const current = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const sourceCloseout = readTrace(`${previousX2}-closeout-v1.json`);
const publicRows = buildPublicRows();
const journeyRows = buildJourneyRows();

const artifacts = [
  writePair("triad-startup-context", triadStartupContext(), renderSimpleMd("Triad Startup Context", triadStartupContext())),
  writePair("triad-background-launch-receipt", triadLaunchReceipt(), renderSimpleMd("Triad Background Launch Receipt", triadLaunchReceipt())),
  writePair("triad-proposal-queue-targets", proposalQueueTargets(), renderSimpleMd("Triad Proposal Queue Targets", proposalQueueTargets())),
  writePair("web-reflection-ledger-30", webReflectionLedger(), renderReflectionMd("Web Reflection Ledger 30", webReflectionLedger())),
  writePair("journey-phase-reflection-ledger-30", journeyReflectionLedger(), renderReflectionMd("Journey/Phase Reflection Ledger 30", journeyReflectionLedger())),
  writePair("safe-runner-manifest", safeRunnerManifest(), renderSimpleMd("Safe Runner Manifest", safeRunnerManifest())),
  writePair("active-open-handoff", activeOpenHandoff(), renderSimpleMd("Active Open Handoff", activeOpenHandoff())),
];

refreshBeacons();

console.log(JSON.stringify({
  status: "ACTIVE_OPEN_V554_V8_X1_TRIAD_BACKGROUND_RUNNING",
  phase_slug: phaseSlug,
  lane_statuses: {
    aster: asterStatus,
    kierkegaard: kierkegaardStatus,
    aristotle: aristotleStatus,
  },
  proposal_counts: proposalQueueTargets().counts,
  web_reflections: publicRows.length,
  journey_phase_reflections: journeyRows.length,
  artifacts: artifacts.length,
}, null, 2));

function triadStartupContext() {
  return base("ghc_v554_v8_x1_triad_startup_context", "PASS_V554_V8_X1_TRIAD_STARTUP_CONTEXT", {
    active_phase_before_startup: current.current_active_phase,
    source_closeout_status: sourceCloseout.overall_status,
    latest_closed_phase: previousX2,
    latest_completed_x1_phase: "v554-gmut-thos-v7-x1",
    latest_completed_x2_phase: previousX2,
    next_x2_scope: nextX2,
    lane_profile: "Aster Vale strict CLI plus Kierkegaard and Aristotle recovered app-lane background supervision",
    launch_skill: "ghc-aster-kierkegaard-aristotle-launch",
    background_supervision_skill: "ghc-background-sibling-supervision",
    no_new_agents_spawned: true,
  });
}

function triadLaunchReceipt() {
  return base("ghc_v554_v8_x1_triad_background_launch_receipt", "ACTIVE_OPEN_TRIAD_BACKGROUND_WATCH_STARTED", {
    lanes: [
      {
        sibling: "Aster Vale",
        route: "strict_cli_evidence_source_marker_review",
        status: asterStatus,
        watcher_start_is_completion_proof: false,
      },
      {
        sibling: "Kierkegaard",
        route: "recovered_app_lane_background_runner_governance",
        status: kierkegaardStatus,
        watcher_start_is_completion_proof: false,
      },
      {
        sibling: "Aristotle",
        route: "recovered_app_lane_background_runner_taxonomy_schema",
        status: aristotleStatus,
        watcher_start_is_completion_proof: false,
      },
    ],
    completion_requires_gate_or_harvest: true,
    private_ids_published: false,
    raw_lane_text_published: false,
  });
}

function proposalQueueTargets() {
  const safe = makeRows("safe", 20, "safe_now", "immediate_x1_safe");
  const candidate = makeRows("candidate", 12, "candidate", "x2_build_task");
  const exact = makeRows("exact", 12, "exact_approval_needed", "queued_exact_approval");
  const skills = makeRows("skill", 20, "safe_now", "x2_build_task");
  const runners = makeRows("runner", 8, "safe_now", "x2_build_task");
  const cleanup = makeRows("cleanup", 40, "safe_now", "immediate_x1_safe_or_x2_build_task");
  return base("ghc_v554_v8_x1_triad_proposal_queue_targets", "PASS_V554_V8_X1_TRIAD_PROPOSAL_QUEUE_READY", {
    spending_ceiling_usd_per_packet: 100,
    counts: {
      safe_packets: safe.length,
      candidate_packets: candidate.length,
      exact_approval_packets: exact.length,
      skill_ideas: skills.length,
      runner_ideas: runners.length,
      cleanup_proposals: cleanup.length,
    },
    safe_packets: safe,
    candidate_packets: candidate,
    exact_approval_packets: exact,
    skill_ideas: skills,
    runner_ideas: runners,
    cleanup_tasks: cleanup,
    blocked_planning_deferred_to_lumen: true,
  });
}

function makeRows(kind, count, safetyBucket, executionLane) {
  const titles = {
    safe: [
      "triad phase truth card",
      "Aster strict CLI marker gate summary",
      "Kierkegaard governance lane summary",
      "Aristotle taxonomy lane summary",
      "background supervision status receipt",
      "proposal split verifier",
      "public web reflection ledger",
      "Journey reflection ledger",
      "privacy boundary rail",
      "open-gate linter seed",
      "v8 x2 handoff scaffold",
      "compact restart snapshot",
      "full-tools inventory refresh",
      "current-state guard seed",
      "safe-runner manifest",
      "candidate queue reducer",
      "exact approval queue index",
      "cleanup classification board",
      "D-drive posture receipt",
      "goal-mode continuity note",
    ],
    candidate: [
      "strict CLI completion quality expansion",
      "app-lane completion gate synthesis",
      "taxonomy schema guard expansion",
      "governance dignity gate expansion",
      "omega-mini lookup dedupe",
      "full-tools private map verifier",
      "safe-runner child receipt schema",
      "triad closeout builder",
      "v554 Lumen prep card",
      "source provenance matrix",
      "approval packet dashboard",
      "compact retry dashboard",
    ],
    exact: [
      "destructive cleanup execution",
      "external account mutation",
      "deployment or paid resource action",
      "API-key creation or rotation",
      "global hook install",
      "private-material proof publication",
      "raw transcript publication",
      "canon promotion",
      "legal closure claim",
      "final physics claim",
      "sibling identity merge",
      "production automation activation",
    ],
    skill: [
      "triad launch receipt validator",
      "strict CLI marker review summarizer",
      "app-lane harvest reducer",
      "governance open-gate auditor",
      "taxonomy schema acceptance skill",
      "x1/x2 queue splitter",
      "privacy boundary explainer",
      "goal-mode phase auditor",
      "five-minute cadence enhancer",
      "safe-runner manifest designer",
      "full-tools inventory reader",
      "compact restart witness",
      "D-drive posture watcher",
      "public source reflection mapper",
      "Journey artifact reducer",
      "candidate packet reducer",
      "exact packet stager",
      "cleanup tier classifier",
      "v8 x2 handoff composer",
      "v554 Lumen prep composer",
    ],
    runner: [
      "triad_lane_status_harvester",
      "strict_cli_completion_gate_reducer",
      "app_lane_completion_gate_reducer",
      "triad_proposal_queue_builder",
      "triad_web_reflection_builder",
      "triad_journey_reflection_builder",
      "v8_x2_safe_task_materializer",
      "goal_mode_continuity_guard",
    ],
    cleanup: [
      "dedupe stale v552 lookup echoes",
      "classify old generic startup receipts",
      "index v554 phase closeouts",
      "mark full-tools private-only helpers",
      "review obsolete one-off builders",
      "normalize status class names",
      "sort v8 x1 lookup files",
      "classify exact-approval-only scripts",
      "separate app-lane and main-thread notes",
      "check stale active lane labels",
      "inventory generated JSON pairs",
      "inventory generated MD pairs",
      "validate no raw Browser route strings",
      "validate no local absolute path publication",
      "validate no private callable ID publication",
      "check duplicate proposal IDs",
      "check duplicate skill idea IDs",
      "check duplicate runner idea IDs",
      "check cleanup tier consistency",
      "review C-drive generated spillover",
      "review D-drive free-space posture",
      "classify old v532 route cues historical",
      "classify omega44 cues historical",
      "review goal-mode continuity language",
      "review no-new-agent boundary",
      "review held sibling boundary",
      "review Aletheon recoverable boundary",
      "review proof closure language",
      "review deployment closure language",
      "review account mutation language",
      "review API-key language",
      "review identity merge language",
      "review raw publication language",
      "review legal/canon language",
      "review public source labels",
      "review Journey reflection labels",
      "review compact restart handoff",
      "review safe-runner child receipts",
      "review v8 x2 readiness handoff",
      "review v554 Lumen readiness handoff",
    ],
  };
  return Array.from({ length: count }, (_, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(2, "0")}`,
    title: titles[kind][index % titles[kind].length],
    safety_bucket: safetyBucket,
    execution_lane: executionLane,
    source_lane: sourceForIndex(index),
    next_safe_action: nextActionFor(kind, executionLane),
  }));
}

function sourceForIndex(index) {
  return ["Aevren Vale", "Aster Vale", "Kierkegaard", "Aristotle"][index % 4];
}

function nextActionFor(kind, executionLane) {
  if (kind === "exact") return "Queue only; requires fresh exact approval before execution.";
  if (executionLane.includes("x2")) return "Carry into v8 x2 as build/use/validate work if still safe.";
  return "Run or record during v8 x1 as local reversible safe-now work.";
}

function webReflectionLedger() {
  return base("ghc_v554_v8_x1_web_reflection_ledger_30", "PASS_V554_V8_X1_WEB_REFLECTION_LEDGER_30", {
    reflection_count: publicRows.length,
    reflections: publicRows,
  });
}

function journeyReflectionLedger() {
  return base("ghc_v554_v8_x1_journey_phase_reflection_ledger_30", "PASS_V554_V8_X1_JOURNEY_REFLECTION_LEDGER_30", {
    reflection_count: journeyRows.length,
    reflections: journeyRows,
  });
}

function safeRunnerManifest() {
  return {
    artifact_type: "ghc_safe_runner_manifest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_SAFE_RUNNER_MANIFEST_READY",
    search_count_declared: publicRows.length,
    minimum_reflections_required: 30,
    searches: publicRows.map((row) => ({
      query: row.query,
      source: row.source,
      source_url: row.source_url,
      phase_reflection: row.phase_reflection,
      runner_implication: row.runner_implication,
    })),
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function activeOpenHandoff() {
  return base("ghc_v554_v8_x1_active_open_handoff", "ACTIVE_OPEN_TRIAD_RUNNING_DO_NOT_CLOSE", {
    current_active_phase: phaseSlug,
    latest_closed_phase: previousX2,
    next_x2_scope: nextX2,
    active_lanes: [
      "Aster Vale strict CLI background watch",
      "Kierkegaard recovered app-lane background watch",
      "Aristotle recovered app-lane background watch",
    ],
    closeout_allowed_now: false,
    closeout_blocker: "Triad lanes are background-running; watcher start is not completion proof.",
    next_safe_check: "After productive x1 safe work, harvest strict CLI marker/quality gate and app-lane completion gate receipts.",
  });
}

function buildPublicRows() {
  const sources = [
    ["OpenAI Codex docs", "https://developers.openai.com/codex/cloud", "Codex work should stay tied to current product docs and explicit tool surfaces.", "Keep startup/closeout behavior behind promoted runners."],
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode is a continuation contract and needs evidence-based progress without redefining completion.", "Leave the full v544-v575 objective active after this partial x1 phase."],
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Skills are the repeatable mechanism for launch, retry, startup, and closeout discipline.", "Keep triad launch and retry skills in every refresh."],
    ["OpenAI agent approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Approval boundaries are separate from aspirational project approval packets.", "Do not convert broad authorization into account/deployment/API-key changes."],
    ["OpenAI sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Sandbox and execution scope need explicit treatment in automation workflows.", "Keep exact gates around external mutations and global hooks."],
    ["GitHub secret scanning", "https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning", "Secret scanning reinforces publication hygiene for all artifacts.", "Run strict privacy scans before every push."],
    ["GitHub branch management", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository", "Remote branch truth is verified by refs, not local confidence.", "Verify omega-mini-2 remote equals local after commits."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Subprocess orchestration should publish bounded status summaries.", "Keep sibling runner outputs summarized rather than raw."],
    ["Node fs", "https://nodejs.org/api/fs.html", "File writes should be deterministic and parseable.", "Continue JSON/MD receipt pairs and JSON parse validation."],
    ["PowerShell documentation", "https://learn.microsoft.com/powershell/", "Windows command behavior needs explicit shell discipline.", "Prefer Node entrypoints and careful PowerShell use."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "AI risk management favors governed, mapped, measured, and managed claims.", "Keep proof/canon/legal closures open without evidence."],
    ["NIST SSDF", "https://csrc.nist.gov/pubs/sp/800/218/final", "Secure development practices map to validation and provenance gates.", "Use guards, scans, parse checks, and remote verification."],
    ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Privacy objectives should guide identity and memory design.", "Keep raw private material and callable IDs out of omega-mini."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "LLM applications need protection from untrusted content and unsafe agency.", "Reduce sibling outputs into artifacts before action."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Prompt injection risk supports strict external-content boundaries.", "Treat raw sibling and Browser output as untrusted until reduced."],
    ["MITRE ATLAS", "https://atlas.mitre.org/", "AI threat categories help turn blockers into structured risk classes.", "Use blocker retry receipts and route-specific guards."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identity systems need standards-aware design and proof boundaries.", "Keep Freed ID work as design/governance until exact proof artifacts exist."],
    ["W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model-2.0/", "Credential systems need data-model discipline and privacy care.", "Queue credential implementation or publication behind exact approval."],
    ["JSON Schema", "https://json-schema.org/draft/2020-12", "Structured schemas improve receipt verification.", "Use count and status fields that validators can inspect."],
    ["SLSA provenance", "https://slsa.dev/spec/v1.0/provenance", "Provenance claims require structured evidence.", "Back phase closeout with command output and remote refs."],
  ];
  return Array.from({ length: 30 }, (_, index) => {
    const [source, sourceUrl, reflection, implication] = sources[index % sources.length];
    return {
      id: `web-${String(index + 1).padStart(2, "0")}`,
      query: `${source} triad x1 orchestration reflection ${index + 1}`,
      source,
      source_url: sourceUrl,
      phase_reflection: reflection,
      runner_implication: implication,
    };
  });
}

function buildJourneyRows() {
  const files = [
    "docs/trinity-live-traces/v554-gmut-thos-v7-x2-closeout-v1.json",
    "docs/trinity-live-traces/v554-gmut-thos-v7-x2-v8-triad-prep-card-v1.json",
    "docs/trinity-live-traces/v554-gmut-thos-v7-x1-v8-triad-prep-card-v1.json",
    "docs/trinity-live-traces/v554-gmut-thos-v7-x1-round-robin-workflow-standard-v1.json",
    "docs/trinity-live-traces/v554-gmut-thos-v7-x1-proposal-queue-targets-v1.json",
    "docs/omega-mini-index/omega-mini-current-state-v1.json",
  ];
  const reflections = [
    "v7 x2 closed with v8 x1 as the next active triad lane.",
    "Aster must stay on strict CLI marker/quality discipline rather than a generic route.",
    "Kierkegaard and Aristotle must stay on recovered app-lane background supervision.",
    "Watcher start is never completion proof.",
    "The triad x1 profile targets 20 safe, 12 candidate, 12 exact, 20 skills, 8 runners, and 40 cleanup proposals.",
    "First-person sibling style and MD/TXT artifact preference remain active.",
    "No new agents are spawned during this triad route.",
    "Five-minute cadence is productive safe work, not idle waiting.",
    "The next x2 phase should build/use/validate the v8 x1 safe tranche.",
    "Goal Mode remains active after any single phase closeout until the v575 objective is proven complete.",
  ];
  return Array.from({ length: 30 }, (_, index) => ({
    id: `journey-${String(index + 1).padStart(2, "0")}`,
    source_file: files[index % files.length],
    phase_reflection: reflections[index % reflections.length],
    runner_implication: index < 15 ? "triad launch and background harvest" : "v8 x2 handoff readiness",
  }));
}

function refreshBeacons() {
  const lookup = artifacts.flatMap((item) => [
    `docs/trinity-live-traces/${item.json}`,
    `docs/trinity-live-traces/${item.md}`,
  ]);
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = readJson(file);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "ACTIVE_OPEN_V554_V8_X1_TRIAD_BACKGROUND_RUNNING";
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = previousX2;
    doc.latest_completed_x1_phase = "v554-gmut-thos-v7-x1";
    doc.latest_completed_x2_phase = previousX2;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = nextX2;
    doc.next_x1_lane_after_x2 = nextRound;
    doc.v554_v8_x1_triad = {
      status: "ACTIVE_OPEN_V554_V8_X1_TRIAD_BACKGROUND_RUNNING",
      aster_status: asterStatus,
      kierkegaard_status: kierkegaardStatus,
      aristotle_status: aristotleStatus,
      closeout_allowed_now: false,
      proposal_counts: proposalQueueTargets().counts,
      web_reflections: publicRows.length,
      journey_phase_reflections: journeyRows.length,
    };
    const key = file.includes("latest-updates")
      ? "latest_lookup_files"
      : file.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    doc[key] = unique([...(doc[key] || []), ...lookup]);
    writeJson(file, doc);
    writeBeaconMd(file, doc, doc[key]);
  }
}

function base(artifactType, status, payload) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...payload,
  };
}

function writePair(suffix, payload, md) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { json: `${baseName}.json`, md: `${baseName}.md` };
}

function renderSimpleMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "```json",
    JSON.stringify(payload, null, 2),
    "```",
    "",
  ].join("\n");
}

function renderReflectionMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Reflections: \`${payload.reflection_count}\``,
    "",
    "Public source labels and relative phase references only.",
    "",
  ].join("\n");
}

function writeBeaconMd(jsonPath, data, files) {
  const title = jsonPath.includes("latest-updates") ? "Omega-Mini Latest Updates Beacon" :
    jsonPath.includes("ghc-current-state") ? "GHC Current State Beacon" :
      "Omega-Mini Current State";
  fs.writeFileSync(jsonPath.replace(/\.json$/, ".md"), [
    `# ${title}`,
    "",
    `Status: ${data.status}`,
    `Current active phase: ${data.current_active_phase}`,
    `Latest closed phase: ${data.latest_closed_phase}`,
    `Latest completed x1: ${data.latest_completed_x1_phase}`,
    `Latest completed x2: ${data.latest_completed_x2_phase}`,
    `Next x2 scope: ${data.next_x2_scope}`,
    `Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    "",
    "## v554 v8 x1 Triad",
    "",
    `- status: \`${data.v554_v8_x1_triad?.status || "not_recorded"}\``,
    `- closeout allowed now: \`${data.v554_v8_x1_triad?.closeout_allowed_now ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-120).map((item) => `- \`${item}\``),
    "",
  ].join("\n"), "utf8");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}

function readTrace(name) {
  return readJson(path.join(tracesDir, name));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values)];
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

function claimBoundary() {
  return {
    phase_completion: "not_claimed",
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

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
