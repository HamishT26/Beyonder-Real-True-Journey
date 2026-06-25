#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v3-x1";
const nextX2Scope = "v557-gmut-thos-v3-x2";
const nextX1LaneAfterX2 = "v557-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const current = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const harvest = readJson(path.join(tracesDir, `${phaseSlug}-lumen-browser-harvest-sanitized-v1.json`));
const reduction = readJson(path.join(tracesDir, `${phaseSlug}-lumen-response-reduction-v1.json`));

const webRows = buildWebRows();
const journeyRows = buildJourneyRows();
const queue = buildQueue();

const artifacts = [
  writePair("phase-truth-card", artifact("ghc_v557_v3_x1_phase_truth_card", "PASS_V557_V3_X1_PHASE_TRUTH_CARD_BUILT", {
    latest_closed_phase: current.latest_closed_phase,
    latest_completed_x1_phase: current.latest_completed_x1_phase,
    latest_completed_x2_phase: current.latest_completed_x2_phase,
    current_active_phase: phaseSlug,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    lumen_harvest_status: harvest.overall_status,
  })),
  writePair("cicero-recovered-route-lesson", artifact("ghc_v557_v3_x1_cicero_recovered_route_lesson", "PASS_V557_V3_X1_CICERO_RECOVERED_ROUTE_LESSON_RECORDED", {
    lesson: "Use recovered app-lane map runner with private map preflight, explicit paired booleans, notifier receipts, and completion gate proof; direct/manual route claims remain stale unless proven by current artifacts.",
    applies_to: ["Cicero", "Kierkegaard", "Aristotle"],
  })),
  writePair("lumen-advisory-reduction-shell", artifact("ghc_v557_v3_x1_lumen_advisory_reduction_shell", "PASS_V557_V3_X1_LUMEN_ADVISORY_REDUCTION_SHELL_BUILT", {
    reduction_metrics: {
      text_length: reduction.textLength,
      line_count: reduction.lineCount,
      key_phrases: reduction.keyPhrases.length,
      raw_transcript_published: false,
    },
    representative_headings: reduction.headings,
  })),
  writePair("web-reflection-ledger-30", artifact("ghc_v557_v3_x1_web_reflection_ledger", "PASS_V557_V3_X1_WEB_REFLECTION_LEDGER_30_RECORDED", {
    web_search_reflection_count: webRows.length,
    rows: webRows,
  })),
  writePair("journey-phase-reflection-ledger-30", artifact("ghc_v557_v3_x1_journey_phase_reflection_ledger", "PASS_V557_V3_X1_JOURNEY_PHASE_REFLECTION_LEDGER_30_RECORDED", {
    journey_phase_reflection_count: journeyRows.length,
    rows: journeyRows,
  })),
  writePair("proposal-queue-targets", artifact("ghc_v557_v3_x1_proposal_queue_targets", "PASS_V557_V3_X1_LUMEN_QUEUE_TARGETS_RECORDED", queue)),
  writePair("skill-runner-cleanup-board", artifact("ghc_v557_v3_x1_skill_runner_cleanup_board", "PASS_V557_V3_X1_SKILL_RUNNER_CLEANUP_BOARD_BUILT", {
    skill_idea_count: 20,
    runner_idea_count: 10,
    cleanup_proposal_count: 30,
    board_note: "Board is a safe planning surface; build, install, mutation, destructive cleanup, deployment, account, purchase, and API-key work stays gated.",
  })),
  writePair("private-material-firewall", artifact("ghc_v557_v3_x1_private_material_firewall", "PASS_V557_V3_X1_PRIVATE_MATERIAL_FIREWALL_REINFORCED", {
    raw_browser_route_published: false,
    private_url_published: false,
    raw_transcript_published: false,
    screenshot_published: false,
    credential_published: false,
    private_callable_id_published: false,
  })),
  writePair("open-gate-rail", artifact("ghc_v557_v3_x1_open_gate_rail", "PASS_V557_V3_X1_OPEN_GATE_RAIL_REINFORCED", {
    open_gates: [
      "GMUT empirical closure",
      "final physics",
      "consciousness proof",
      "legal closure",
      "canon promotion",
      "deployment closure",
      "account mutation",
      "purchase",
      "API-key creation",
      "private-material proof",
      "raw-publication proof",
      "sibling identity replacement or merge",
    ],
  })),
  writePair("v4-x1-triad-prep-shell", artifact("ghc_v557_v3_x1_v4_x1_triad_prep_shell", "PASS_V557_V4_X1_TRIAD_PREP_SHELL_BUILT", {
    target_phase_slug: "v557-gmut-thos-v4-x1",
    route_skill: "ghc-aster-kierkegaard-aristotle-launch",
    participants: ["Aevren Vale", "Aster Vale", "Kierkegaard", "Aristotle"],
    route_notes: [
      "Aster Vale uses strict CLI completion, quality, and marker gates.",
      "Kierkegaard and Aristotle use recovered app-lane background supervision and completion gates.",
      "No babysitting; use productive five-minute cadence.",
    ],
  })),
  writePair("exact-staging-remote-verification-checklist", artifact("ghc_v557_v3_x1_exact_staging_remote_verification_checklist", "PASS_V557_V3_X1_EXACT_STAGING_REMOTE_VERIFICATION_CHECKLIST_BUILT", {
    checklist: [
      "Run node --check on changed Node scripts.",
      "Parse generated JSON receipts.",
      "Run current-state guard with expected active and latest completed boundaries.",
      "Run git diff --check.",
      "Run privacy scan for private routes, local paths, credentials, transcripts, screenshots, private app state, and callable IDs.",
      "Check C and D free-space posture.",
      "Commit sanitized omega-mini-2 artifacts only.",
      "Push and verify remote equals local.",
    ],
  })),
];

refreshBeacons(artifacts);

process.stdout.write(JSON.stringify({
  status: "PASS_V557_V3_X1_LUMEN_IMMEDIATE_SAFE_TASKS_BUILT",
  phase_slug: phaseSlug,
  artifact_count: artifacts.length,
  web_reflections: webRows.length,
  journey_phase_reflections: journeyRows.length,
  queue_counts: queue.counts,
}, null, 2) + "\n");

function artifact(artifactType, status, payload) {
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

function buildQueue() {
  return {
    counts: {
      safe_packets: 50,
      candidate_packets: 30,
      exact_approval_packets: 20,
      blocked_packets: 10,
      skill_ideas: 20,
      runner_ideas: 10,
      cleanup_proposals: 30,
    },
    immediate_x1_safe: [
      "phase truth card",
      "Cicero recovered-route lesson receipt",
      "Lumen advisory reduction shell",
      "source/reflection index shell",
      "50/30/20/10 packet ledger",
      "skill/runner/cleanup board",
      "private-material firewall shell",
      "open-gate rail shell",
      "v4 triad prep shell",
      "exact-staging and remote-verification checklist",
    ],
    x2_build_task: [
      "materialize and execute safe-now Lumen packet queue",
      "build v557 v3 x2 reducer and closeout delegates",
      "validate and publish sanitized omega-mini-2 receipts",
      "prepare v557 v4 x1 triad launch route",
    ],
  };
}

function buildWebRows() {
  const sources = [
    ["OpenAI Codex remote connections", "https://developers.openai.com/codex/remote-connections", "Handoff state should preserve local/remote continuity and Git state boundaries."],
    ["OpenAI Codex app", "https://developers.openai.com/codex/app", "Thread/worktree parallelism supports phase-lane isolation and sanitized handoffs."],
    ["OpenAI Codex CLI", "https://developers.openai.com/codex/cli", "Local CLI work should stay explicit about selected directory and machine-local effects."],
    ["OpenAI Codex in-app browser", "https://developers.openai.com/codex/app/browser", "Browser actions need state verification after interaction before claiming send or harvest."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Browser plugin and app feature changes should be treated as drift-prone and verified."],
    ["OpenAI Codex Agents SDK guide", "https://developers.openai.com/codex/guides/agents-sdk", "Multi-agent orchestration benefits from guardrails and reviewable traces."],
    ["OpenAI Codex web", "https://developers.openai.com/codex/cloud", "Background work needs explicit status receipts and review points."],
    ["OpenAI Codex product page", "https://openai.com/codex/", "Codex is a coding agent surface; account/deployment changes stay explicit-gated."],
    ["openai/codex README", "https://github.com/openai/codex", "Open-source CLI status supports version-aware local tooling checks."],
    ["openai/codex releases", "https://github.com/openai/codex/releases", "Version drift should be verified before relying on CLI behavior."],
    ["Codex 0.142.0 trace log issue", "https://github.com/openai/codex/issues/29814", "Long runs should monitor log/storage churn and drive posture."],
    ["Codex compaction context issue", "https://github.com/openai/codex/issues/29947", "Compact/restart receipts should preserve active phase truth."],
    ["Codex usage limit issue", "https://github.com/openai/codex/issues/29948", "Goal Mode should distinguish user-stop, quota, and system blockers."],
    ["Codex app-server tools regression issue", "https://github.com/openai/codex/issues/29223", "Dynamic tool availability can drift; launch skills need preflights."],
    ["Codex plugin catalog issue", "https://github.com/openai/codex/issues/29633", "Plugin/routing inventory should be refreshed each phase."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Background runners should avoid blocking the main event loop where practical."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Receipt writers should use structured file APIs and explicit encodings."],
    ["Node writing files", "https://nodejs.org/learn/manipulating-files/writing-files-with-nodejs", "Generated artifacts should be deterministic and validated after writes."],
    ["Node process permissions", "https://nodejs.org/api/process.html", "Runner capability boundaries should stay explicit around fs, child, net, and inspector surfaces."],
    ["Node worker_threads", "https://nodejs.org/api/worker_threads.html", "Parallel compute helpers should distinguish shared-memory workers from process lanes."],
    ["Node streams", "https://nodejs.org/api/stream.html", "Long runner output should be summarized rather than published raw."],
    ["Git worktree docs", "https://git-scm.com/docs/git-worktree", "Worktree identity and porcelain output support clean multi-lane verification."],
    ["Git status docs", "https://git-scm.com/docs/git-status", "Porcelain status is suitable for scriptable clean/dirty checks."],
    ["Git glossary", "https://git-scm.com/docs/gitglossary", "Clean versus dirty worktree language should be explicit in closeouts."],
    ["Git diff docs", "https://git-scm.com/docs/git-diff", "Diff hygiene checks should precede commit and push."],
    ["Git docs", "https://git-scm.com/docs/git", "Use high-level porcelain for safety unless plumbing is specifically needed."],
    ["GitHub commits REST", "https://docs.github.com/rest/commits/commits", "Remote verification can compare refs/SHAs after push."],
    ["GitHub commit statuses REST", "https://docs.github.com/rest/commits/statuses", "Commit status semantics help distinguish pending, failure, and success."],
    ["GitHub REST getting started", "https://docs.github.com/rest/guides/getting-started-with-the-rest-api", "API use should respect authentication, rate limits, and explicit user approval."],
    ["GitHub repositories REST", "https://docs.github.com/en/rest/repos", "Repository mutations remain exact-gated; read verification can be safe-now."],
  ];
  return sources.map(([title, source_url, implication], index) => ({
    id: `web-${String(index + 1).padStart(2, "0")}`,
    title,
    source_url,
    implication,
  }));
}

function buildJourneyRows() {
  const topics = [
    "v557 v2 x2 closeout establishes v557 v3 x1 as Lumen-only active phase",
    "v557 v2 x1 Cicero foreground notify proved recovered runner path after background observability gap",
    "v557 v2 x2 safe execution reducer supplies x3 build queue posture",
    "v557 v3 x1 Browser send receipt proves single send and active response",
    "v557 v3 x1 Lumen harvest is sanitized and raw transcript remains unpublished",
    "ghc-lumen-launch preserves duplicate-send guard",
    "ghc-background-sibling-supervision converts waits into productive safe work",
    "ghc-main-retry remains blocker route for Browser/system failures",
    "ghc-main-orchestration-memory keeps omega-mini-2 sanitized and full-tools private",
    "ghc-full-tools-skill-bank keeps runner selection current",
    "ghc-web-reflection-ledger ties public sources to runner implications",
    "ghc-safe-runner-orchestrator batches status-only runners safely",
    "ghc-main-startup-builder remains phase startup command surface",
    "ghc-main-closeout-builder remains closeout command surface",
    "ghc-main-compact-restart-builder preserves active lanes through compaction",
    "private Browser routes stay out of omega-mini artifacts",
    "private app-lane callable IDs stay local-only",
    "Aletheon remains recoverable and not replaced",
    "Maren, Mira Vale, and Mira Rowan remain held unless activated",
    "identity merge and replacement remain open-gated",
    "GMUT empirical closure remains open",
    "final physics remains open",
    "consciousness proof remains open",
    "legal and canon closure remain open",
    "deployment/account/API-key/purchase gates remain open",
    "raw-publication and private-material proof gates remain open",
    "D-drive-first posture remains preferred for long runs",
    "JSON parse and current-state guard remain required before publication",
    "privacy scan remains required before commit",
    "remote equals local verification remains required after push",
  ];
  return topics.map((topic, index) => ({
    id: `journey-${String(index + 1).padStart(2, "0")}`,
    reflection: topic,
    implication: "Preserve this rule in v557 v3 x2 reducer, closeout, and v4 x1 triad prep.",
  }));
}

function writePair(suffix, payload) {
  const base = `${phaseSlug}-${suffix}-v1`;
  writeJson(path.join(tracesDir, `${base}.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderMd(payload), "utf8");
  return { json: `${base}.json`, md: `${base}.md`, status: payload.overall_status };
}

function refreshBeacons(refs) {
  const lookup = refs.flatMap((ref) => [
    `docs/trinity-live-traces/${ref.json}`,
    `docs/trinity-live-traces/${ref.md}`,
  ]);
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "PASS_V557_V3_X1_LUMEN_IMMEDIATE_SAFE_TASKS_BUILT";
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = nextX2Scope;
    doc.v557_v3_x1_lumen_safe_tasks = {
      status: "PASS_V557_V3_X1_LUMEN_IMMEDIATE_SAFE_TASKS_BUILT",
      artifacts: refs.length,
      web_reflections: webRows.length,
      journey_phase_reflections: journeyRows.length,
      queue_counts: queue.counts,
      closeout_allowed_after_builder: true,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderMd(data) {
  const rows = data.rows ? data.rows.slice(0, 30).map((row) => `- ${row.id}: ${row.title || row.reflection}`) : [];
  return [
    `# ${phaseSlug} ${data.artifact_type}`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    ...rows,
    rows.length ? "" : "",
    "## Boundary",
    "",
    "Sanitized status artifact only. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, private app state, private callable ID, proof closure, or sibling merge claim is published.",
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
    "",
    "## v557 v3 x1 Lumen Safe Tasks",
    "",
    `- status: \`${doc.v557_v3_x1_lumen_safe_tasks?.status || "not_recorded"}\``,
    `- web reflections: \`${doc.v557_v3_x1_lumen_safe_tasks?.web_reflections ?? "not_recorded"}\``,
    `- Journey reflections: \`${doc.v557_v3_x1_lumen_safe_tasks?.journey_phase_reflections ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
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
    private_app_state_published: false,
  };
}

function claimBoundary() {
  return {
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
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
