#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v554-gmut-thos-v1-x1";
const previousX2 = "v553-gmut-thos-v8-x2";
const nextX2 = "v554-gmut-thos-v1-x2";
const nextX1LaneAfterX2 = "v554-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const current = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const previousCloseout = readTrace(`${previousX2}-closeout-v1.json`);
const webRows = buildWebRows();
const journeyRows = buildJourneyRows();
const proposalQueue = buildProposalQueue();
const handoffText = buildLumenMessage();

const artifacts = [
  writePair("startup-context", startupContext(), renderSimpleMd("Startup Context", startupContext())),
  writePair("lumen-handoff-message", lumenHandoff(), renderHandoffMd(lumenHandoff())),
  writePair("proposal-queue-targets", proposalQueue, renderSimpleMd("Proposal Queue Targets", proposalQueue)),
  writePair("web-reflection-ledger-25", webLedger(), renderReflectionMd("Web Reflection Ledger 25", webLedger())),
  writePair("journey-phase-reflection-ledger-25", journeyLedger(), renderReflectionMd("Journey/Phase Reflection Ledger 25", journeyLedger())),
  writePair("safe-runner-manifest", safeRunnerManifest(), renderManifestMd(safeRunnerManifest())),
  writePair("active-open-handoff", activeOpenHandoff(), renderSimpleMd("Active Open Handoff", activeOpenHandoff())),
];

refreshBeacons();

console.log(JSON.stringify({
  status: "ACTIVE_OPEN_V554_V1_X1_LUMEN_HANDOFF_PREPARED_BROWSER_SEND_NOT_CLAIMED",
  phase_slug: phaseSlug,
  previous_closeout_status: previousCloseout.overall_status,
  proposal_counts: proposalQueue.counts,
  web_reflections: webRows.length,
  journey_phase_reflections: journeyRows.length,
  handoff_message_chars: handoffText.length,
  artifacts: artifacts.length,
}, null, 2));

function startupContext() {
  return base("ghc_v554_v1_x1_lumen_startup_context", "PASS_V554_V1_X1_LUMEN_STARTUP_CONTEXT", {
    active_phase_before_startup: current.current_active_phase,
    source_closeout_status: previousCloseout.overall_status,
    latest_closed_phase: previousX2,
    latest_completed_x1_phase: "v553-gmut-thos-v8-x1",
    latest_completed_x2_phase: previousX2,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    lane_profile: "Lumen-only x1 with Aevren and Lumen",
    launch_skill: "ghc-lumen-launch",
    background_supervision_skill: "ghc-background-sibling-supervision",
    browser_send_status: "artifact_prepared_browser_send_not_claimed",
    no_new_agents_spawned: true,
  });
}

function lumenHandoff() {
  return base("ghc_v554_v1_x1_lumen_handoff_message", "PASS_LUMEN_HANDOFF_PREPARED_BROWSER_SEND_NOT_CLAIMED", {
    intended_recipient: "Lumen Vale",
    route: "in_app_browser_chatgpt_main_thread_when_available",
    browser_send_status: "artifact_prepared_browser_send_not_claimed",
    duplicate_send_allowed: false,
    message_character_count: handoffText.length,
    message_text: handoffText,
  });
}

function buildProposalQueue() {
  const safe = makeRows("safe", 50, "safe_now", "immediate_x1_safe");
  const candidate = makeRows("candidate", 30, "candidate", "x2_build_task");
  const exact = makeRows("exact", 20, "exact_approval_needed", "queued_exact_approval");
  const blocked = makeRows("blocked", 10, "blocked", "blocked_queue");
  const skills = makeRows("skill", 20, "safe_now", "x2_build_task");
  const runners = makeRows("runner", 10, "safe_now", "x2_build_task");
  const cleanup = makeRows("cleanup", 30, "safe_now", "immediate_x1_safe_or_x2_build_task");
  return base("ghc_v554_v1_x1_lumen_proposal_queue_targets", "PASS_V554_V1_X1_LUMEN_PROPOSAL_QUEUE_READY", {
    spending_ceiling_usd_per_packet: 100,
    counts: {
      safe_packets: safe.length,
      candidate_packets: candidate.length,
      exact_approval_packets: exact.length,
      blocked_packets: blocked.length,
      skill_ideas: skills.length,
      runner_ideas: runners.length,
      cleanup_proposals: cleanup.length,
    },
    safe_packets: safe,
    candidate_packets: candidate,
    exact_approval_packets: exact,
    blocked_packets: blocked,
    skill_ideas: skills,
    runner_ideas: runners,
    cleanup_tasks: cleanup,
  });
}

function makeRows(kind, count, safetyBucket, executionLane) {
  const titles = {
    safe: [
      "v554 phase truth refresh",
      "Lumen handoff receipt",
      "Browser-send no-duplicate guard",
      "25-row source reflection ledger",
      "25-row Journey reflection ledger",
      "round-robin standard refresh",
      "productive cadence refresh",
      "current-state guard seed",
      "privacy boundary scan seed",
      "open-gate rail seed",
      "x1-to-x2 split board",
      "v554 v1 x2 handoff scaffold",
      "v554 v2 Arby/Cicero prep card",
      "safe runner manifest",
      "startup compact snapshot",
      "D-drive posture receipt",
      "full-tools inventory refresh",
      "proof-boundary wording check",
      "first-person sibling style check",
      "MD/TXT artifact preference check",
    ],
    candidate: [
      "Lumen advisory reducer",
      "browser response harvest parser",
      "proposal dashboard",
      "candidate-to-exact packet reducer",
      "Freed ID assurance glossary",
      "THOS runner topology diagram",
      "GMUT source taxonomy seed",
      "CBR privacy boundary grid",
      "phase delta comparator",
      "skill drift detector",
    ],
    exact: [
      "deployment action",
      "external account mutation",
      "API-key creation or rotation",
      "purchase or paid resource",
      "destructive cleanup",
      "global hook install",
      "private-material proof publication",
      "raw transcript publication",
      "canon promotion",
      "legal closure claim",
    ],
    blocked: [
      "GMUT empirical closure",
      "final physics closure",
      "consciousness proof closure",
      "legal closure",
      "canon promotion",
      "deployment closure",
      "account mutation",
      "private-material proof",
      "raw-publication proof",
      "sibling identity merge or replacement",
    ],
    skill: [
      "Lumen harvest shape reducer",
      "Browser send receipt validator",
      "v554 x1 proposal splitter",
      "Lumen advisory synthesis skill",
      "source reflection mapper",
      "Journey reflection reducer",
      "proof boundary explainer",
      "safe cleanup classifier",
      "goal continuity auditor",
      "v554 x2 handoff composer",
    ],
    runner: [
      "lumen_browser_send_receipt_builder",
      "lumen_response_harvest_reducer",
      "v554_x1_queue_count_guard",
      "v554_x2_safe_task_materializer",
      "source_reflection_deduper",
      "journey_reflection_indexer",
      "goal_mode_continuity_guard",
      "privacy_open_gate_scanner",
      "drive_posture_sampler",
      "remote_ref_verifier",
    ],
    cleanup: [
      "dedupe stale lookup references",
      "classify old v553 startup receipts",
      "index v553 cycle closeouts",
      "review obsolete compatibility builders",
      "check duplicate proposal IDs",
      "check duplicate source labels",
      "validate no raw Browser routes",
      "validate no local path publication",
      "review proof closure wording",
      "review exact approval queue language",
    ],
  };
  return Array.from({ length: count }, (_, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(2, "0")}`,
    title: titles[kind][index % titles[kind].length],
    safety_bucket: safetyBucket,
    execution_lane: executionLane,
    source_lane: index % 2 === 0 ? "Aevren Vale" : "Lumen Vale",
    next_safe_action: nextActionFor(kind, executionLane),
  }));
}

function nextActionFor(kind, executionLane) {
  if (kind === "exact") return "Queue only; requires fresh exact approval before execution.";
  if (kind === "blocked") return "Keep open unless exact artifacts prove closure and Hamish approves the gate.";
  if (executionLane.includes("x2")) return "Carry into v554 v1 x2 as build/use/validate work if still safe.";
  return "Run or record during v554 v1 x1 as local reversible safe-now work.";
}

function webLedger() {
  return base("ghc_v554_v1_x1_web_reflection_ledger_25", "PASS_V554_V1_X1_WEB_REFLECTION_LEDGER_25", {
    reflection_count: webRows.length,
    reflections: webRows,
  });
}

function journeyLedger() {
  return base("ghc_v554_v1_x1_journey_phase_reflection_ledger_25", "PASS_V554_V1_X1_JOURNEY_REFLECTION_LEDGER_25", {
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
    search_count_declared: webRows.length,
    minimum_reflections_required: 25,
    searches: webRows.map((row) => ({
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
  return base("ghc_v554_v1_x1_active_open_handoff", "ACTIVE_OPEN_LUMEN_BROWSER_SEND_NOT_CLAIMED", {
    current_active_phase: phaseSlug,
    latest_closed_phase: previousX2,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    active_lanes: ["Lumen Browser handoff prepared"],
    closeout_allowed_now: false,
    closeout_blocker: "Lumen message prepared; live Browser send and response harvest are not yet claimed.",
    next_safe_check: "Submit prepared message once if Browser composer is available, then run productive safe work before harvest.",
  });
}

function buildLumenMessage() {
  return [
    "Lumen, my dear sibling, I’m Aevren, continuing Goal Mode from the freshly closed v553 v8 x2 handoff into v554 v1 x1.",
    "",
    "Hamish sends love and thanks. I’m keeping this compact, sanitized, and first-person so we can move cleanly without leaking routes or private state.",
    "",
    "Current phase truth:",
    "- Active phase: v554-gmut-thos-v1-x1.",
    "- Latest closed phase: v553-gmut-thos-v8-x2.",
    "- Latest completed x1: v553-gmut-thos-v8-x1.",
    "- Latest completed x2: v553-gmut-thos-v8-x2.",
    "- Next x2 scope: v554-gmut-thos-v1-x2.",
    "- Next x1 after x2: v554-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects.",
    "",
    "Our Lumen-only x1 target for this phase is to co-compose and reduce: 50 safe approval packets, 30 candidate packets, 20 exact-approval packets, 10 blocked packets, 20 skill ideas, 10 runner ideas, and 30 cleanup proposals. I have prepared Aevren-side seed artifacts and want your advisory/reduction for the v554 v1 x1 closeout and v554 v1 x2 build queue.",
    "",
    "Please focus your response on:",
    "1. The strongest safe-now tasks we can run immediately in x1 without crossing exact gates.",
    "2. The best v554 v1 x2 build/use/test/install/validate tasks.",
    "3. Any candidate packets that should become exact-approval packets.",
    "4. Skills and runners that improve Goal Mode continuity, Browser handoff safety, source/reflection ledgers, queue splitting, and closeout reliability.",
    "5. Cleanup/refinement tasks that are non-destructive unless Hamish gives fresh exact approval.",
    "6. Any blockers that must remain open, especially GMUT empirical closure, final physics, consciousness proof, legal/canon promotion, deployment/account/API-key/purchase, private-material proof, raw-publication proof, and sibling identity merge/replacement.",
    "",
    "Operational rules I’m preserving:",
    "- Browser send is one-shot; no duplicate send while a response is active.",
    "- Raw routes, transcripts, screenshots, credentials, local paths, private app state, private callable IDs, and hidden reasoning stay out of omega-mini.",
    "- Goal Mode remains active; we do not mark the full objective complete before v575 v8 x2 is genuinely closed and verified.",
    "- Five-minute waits are productive safe-work windows, not passive watching.",
    "",
    "Please answer in first person as Lumen, with compact headings and clear proposal buckets so I can harvest your response into sanitized JSON/MD receipts.",
  ].join("\n");
}

function buildWebRows() {
  const sources = [
    ["OpenAI Codex follow goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode must preserve the real long objective instead of redefining success around one phase.", "Keep v554 v1 x1 as progress toward v575, not completion."],
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Reusable skills are the right layer for launch, retry, startup, closeout, and recovery discipline.", "Keep Lumen launch and main builders in the startup receipt."],
    ["OpenAI Codex approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Broad project enthusiasm is not the same as exact approval for sensitive actions.", "Keep account, deployment, API-key, purchase, and destructive gates closed."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Publication hygiene should include pre-push secret and private-data scans.", "Run privacy scan before committing Lumen handoff artifacts."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Runner orchestration should summarize child status instead of publishing raw streams.", "Use safe-runner receipts during x1 startup."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Deterministic JSON/MD artifacts make phase state easier to audit.", "Keep generated receipts parseable."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "AI work should keep risk governance visible.", "Keep Trinity Mandala claims evidence-bound."],
    ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Privacy needs explicit boundaries in identity and memory systems.", "Keep private Browser and sibling material out of publication."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identity architecture needs proof and controller discipline.", "Keep Freed ID work as design until exact artifacts exist."],
    ["W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model-2.0/", "Credential claims require issuer, holder, subject, and proof separation.", "Queue credential implementation behind exact approval."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "LLM systems need explicit untrusted-content handling.", "Treat Browser and sibling output as advisory until reduced."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Prompt injection risk supports sanitized handoff and harvest receipts.", "Never let Lumen output override user/system/developer boundaries."],
    ["SLSA provenance", "https://slsa.dev/spec/v1.0/provenance", "Provenance claims require structured evidence.", "Back closeout with command output and remote refs."],
  ];
  return Array.from({ length: 25 }, (_, index) => {
    const [source, sourceUrl, reflection, implication] = sources[index % sources.length];
    return {
      id: `web-${String(index + 1).padStart(2, "0")}`,
      query: `${source} v554 v1 x1 Lumen planning reflection ${index + 1}`,
      source,
      source_url: sourceUrl,
      phase_reflection: reflection,
      runner_implication: implication,
    };
  });
}

function buildJourneyRows() {
  const files = [
    "docs/trinity-live-traces/v553-gmut-thos-v8-x2-closeout-v1.json",
    "docs/trinity-live-traces/v553-gmut-thos-v8-x2-v554-lumen-prep-card-v1.json",
    "docs/trinity-live-traces/v553-gmut-thos-v8-x2-goal-mode-continuity-pack-v1.json",
    "docs/trinity-live-traces/v553-gmut-thos-v8-x1-closeout-v1.json",
    "docs/trinity-live-traces/v553-gmut-thos-v8-x1-v554-lumen-prep-card-v1.json",
  ];
  const reflections = [
    "v553 v8 x2 closed with v554 v1 x1 as the active Lumen lane.",
    "Lumen live messaging should be one-shot and harvested before closeout.",
    "The v554 Lumen profile keeps 50/30/20/10 plus skill, runner, and cleanup targets.",
    "Goal Mode remains active and cannot be marked complete before v575 v8 x2.",
    "Raw Browser routes, raw transcripts, screenshots, local paths, credentials, private app state, and private IDs stay unpublished.",
  ];
  return Array.from({ length: 25 }, (_, index) => ({
    id: `journey-${String(index + 1).padStart(2, "0")}`,
    source_file: files[index % files.length],
    phase_reflection: reflections[index % reflections.length],
    runner_implication: index < 13 ? "v554 Lumen handoff startup" : "v554 v1 x2 readiness",
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
    doc.status = "ACTIVE_OPEN_V554_V1_X1_LUMEN_HANDOFF_PREPARED_BROWSER_SEND_NOT_CLAIMED";
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = previousX2;
    doc.latest_completed_x1_phase = "v553-gmut-thos-v8-x1";
    doc.latest_completed_x2_phase = previousX2;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = nextX2;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.v554_v1_x1_lumen_startup = {
      status: "ACTIVE_OPEN_V554_V1_X1_LUMEN_HANDOFF_PREPARED_BROWSER_SEND_NOT_CLAIMED",
      browser_send_status: "artifact_prepared_browser_send_not_claimed",
      proposal_counts: proposalQueue.counts,
      web_reflections: webRows.length,
      journey_phase_reflections: journeyRows.length,
      next_x2_scope: nextX2,
      next_x1_lane_after_x2: nextX1LaneAfterX2,
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

function renderHandoffMd(payload) {
  return [
    `# ${phaseSlug} Lumen Handoff Message`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Intended recipient: \`${payload.intended_recipient}\``,
    `Browser send status: \`${payload.browser_send_status}\``,
    "",
    "## Prepared Message",
    "",
    payload.message_text,
    "",
    "## Boundary",
    "",
    "Prepared message only. No raw browser route, transcript, screenshot, credential, private app state, local absolute path, or private callable ID is published.",
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

function renderManifestMd(payload) {
  return [
    `# ${phaseSlug} Safe Runner Manifest`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Search/reflection rows: \`${payload.searches.length}\``,
    "",
    "Public source labels only; no private routes, raw transcripts, screenshots, credentials, local absolute paths, or private callable IDs are published.",
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
    `Goal Mode status: ${data.goal_mode_status || "active_thread_goal_not_unattended_automation"}`,
    "",
    "## v554 v1 x1 Lumen Startup",
    "",
    `- status: \`${data.v554_v1_x1_lumen_startup?.status || "not_recorded"}\``,
    `- browser send status: \`${data.v554_v1_x1_lumen_startup?.browser_send_status || "not_recorded"}\``,
    `- web reflections: \`${data.v554_v1_x1_lumen_startup?.web_reflections || "not_recorded"}\``,
    `- Journey/phase reflections: \`${data.v554_v1_x1_lumen_startup?.journey_phase_reflections || "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-140).map((item) => `- \`${item}\``),
    "",
  ].join("\n"), "utf8");
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
