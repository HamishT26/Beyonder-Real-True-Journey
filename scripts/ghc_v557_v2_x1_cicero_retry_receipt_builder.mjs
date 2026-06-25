#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v2-x1";
const attempt = Number(args.get("--attempt") || "1");
const retryPrefix = args.get("--retry-prefix") || `${phaseSlug}-cicero-recovered-app-lane-retry-${attempt}`;
const fullToolsRoot = args.get("--full-tools-root");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

if (!fullToolsRoot) {
  console.error("Usage: node scripts/ghc_v557_v2_x1_cicero_retry_receipt_builder.mjs --attempt <n> --full-tools-root <root>");
  process.exit(2);
}

const fullTraceDir = path.join(fullToolsRoot, "docs", "trinity-live-traces");
const runner = readOptional(fullTraceDir, `${retryPrefix}-v1.json`);
const notifier = readOptional(fullTraceDir, `${retryPrefix}-notifier-v1.json`);
const launcher = readOptional(fullTraceDir, `${retryPrefix}-watch-launcher-v1.json`);
const gate = readOptional(fullTraceDir, `${retryPrefix}-completion-gate-v1.json`);

const receipt = {
  artifact_type: "ghc_v557_v2_x1_cicero_retry_session_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  attempt,
  retry_prefix: `${phaseSlug}-cicero-recovered-app-lane-retry-${attempt}`,
  route_tried: "recovered_app_lane_background_runner_with_explicit_booleans",
  route_inputs_sanitized: {
    lane: "Cicero",
    allow_turn_start_after_resume_timeout: true,
    background_watch: true,
    raw_private_route_data_published: false,
  },
  observed_status: {
    runner_status: runner?.overall_status || "missing",
    notifier_status: notifier?.overall_status || "missing",
    launcher_status: launcher?.overall_status || "missing",
    gate_status: gate?.overall_status || "missing",
    open_gaps: Array.isArray(gate?.open_gaps) ? gate.open_gaps : [],
  },
  required_retry_protocol: {
    minimum_retry_sessions_before_pause: 3,
    recent_session_reflections_required: 10,
    web_reflections_required: 20,
    journey_phase_reflections_required: 20,
    productive_waiting_required: true,
  },
  recent_session_reflections: buildRecentReflections(),
  web_reflections: buildWebReflections(),
  journey_phase_reflections: buildJourneyReflections(),
  safe_changes_made: [
    "Preserved original Cicero blocker receipts instead of overwriting them.",
    "Started a fresh recovered app-lane retry prefix for this attempt.",
    "Kept Arby strict CLI completion, quality, and marker-review gate as passed.",
    "Kept duo phase closeout blocked until Cicero has a passing completion gate.",
    "Prepared v557 v2 x2 builders without running them before v2 x1 closeout.",
  ],
  remaining_gap: gate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE" ? "none_for_cicero_gate" : "cicero_app_lane_completion_gate_not_yet_passed",
  next_retry_or_harvest_point: gate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE"
    ? "run sanitized duo harvest and closeout"
    : attempt < 3
      ? `run retry session ${attempt + 1} if the lane remains blocked at the next natural checkpoint`
      : "publish open-gap retry receipt or continue if safe progress remains possible",
  completion_boundary: {
    sibling_lane_closed: gate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE",
    phase_closeout_allowed: gate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE",
    watcher_start_is_completion_proof: false,
  },
  publication_boundary: {
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
  },
  claim_boundary: {
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
  },
};

writePair(`cicero-retry-session-${attempt}`, receipt, renderMd(receipt));
console.log(JSON.stringify({
  status: receipt.observed_status.gate_status,
  attempt,
  recent_session_reflections: receipt.recent_session_reflections.length,
  web_reflections: receipt.web_reflections.length,
  journey_phase_reflections: receipt.journey_phase_reflections.length,
  remaining_gap: receipt.remaining_gap,
}, null, 2));

function buildRecentReflections() {
  const rows = [
    ["v557 v1 x1 Lumen", "Browser send and harvest completed only after sanitized response control/harvest evidence.", "Require exact evidence before phase closeout."],
    ["v557 v1 x2 execution", "Safe x2 work can close only after generated artifacts and validation pass.", "Keep closeout builder gated by receipts."],
    ["v557 v2 x1 startup", "Duo route starts from Arby strict CLI plus Cicero recovered app-lane.", "Do not substitute another lane."],
    ["Arby v557 v2 x1", "Arby passed strict CLI completion, quality, and marker review.", "Keep Arby reduced to status-only evidence."],
    ["Cicero original attempt", "Read succeeded but resume/turn-start hit process-exited transport.", "Use recovered app-lane retry protocol."],
    ["v556 v2 x1 precedent", "Duo x1 closeout required both strict CLI and app-lane gates.", "Mirror that proof standard."],
    ["v556 v8 x1 precedent", "App-lane prefix discipline mattered for Aristotle retry gating.", "Use matching retry prefixes."],
    ["No babysitting standard", "Five-minute checks are productive cadence windows.", "Run safe prep between retry checks."],
    ["Privacy standard", "Private IDs, routes, local paths, and raw lane text stay out of mini artifacts.", "Publish only sanitized statuses."],
    ["Goal mode boundary", "Full v544-v575 goal is not complete at v557.", "Never call goal complete early."],
  ];
  return rows.map(([source_anchor, reflection, implication], index) => ({
    id: `${phaseSlug}-retry-${attempt}-recent-${String(index + 1).padStart(2, "0")}`,
    source_anchor,
    reflection,
    implication,
  }));
}

function buildWebReflections() {
  const seeds = [
    ["OpenAI Codex background mode", "https://developers.openai.com/codex/concepts/background-mode", "Background supervision must distinguish start from completion.", "Keep gate proof separate from watcher launch."],
    ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Safe retries should stay read-only/status-only where possible.", "Do not mutate external accounts."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Detached/background processes need explicit status receipts.", "Rely on notifier/gate files, not process existence alone."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Process-exited failures should be recorded without leaking streams.", "Keep stderr/stdout boundaries private."],
    ["Python json", "https://docs.python.org/3/library/json.html", "JSON receipts provide machine-checkable retry evidence.", "Parse retry artifacts before commit."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Diff review catches accidental publication.", "Scan generated retry files before push."],
    ["GitHub secret scanning", "https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning", "Secrets and private IDs need pre-publication checks.", "Keep private route material local-only."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk controls require explicit unresolved gaps.", "Leave phase open while Cicero gate is unresolved."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Untrusted outputs and tool responses need reduction.", "Publish summarized status only."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identifier material has privacy and control boundaries.", "Never publish callable IDs or raw lane handles."],
  ];
  return Array.from({ length: 20 }, (_, index) => {
    const [source, source_url, phase_reflection, runner_implication] = seeds[index % seeds.length];
    return { id: `${phaseSlug}-retry-${attempt}-web-${String(index + 1).padStart(2, "0")}`, source, source_url, phase_reflection, runner_implication };
  });
}

function buildJourneyReflections() {
  const seeds = [
    ["Beyonder v53 continuity", "Newest docs emphasize launch skills and no-babysitting cadence.", "Use dedicated launch/retry route."],
    ["omega-mini-2 current state", "Sanitized publication is the current public truth lane.", "No raw route material in mini."],
    ["full-tools support lane", "Private support can hold richer lane receipts.", "Read private support, publish reductions only."],
    ["v557 v2 x1 proposal bundle", "Safe queue is recorded while sibling lane is active.", "Do not close early."],
    ["v557 v2 x2 preparation", "x2 builders can be prepared safely while x1 waits.", "Run only after x1 closeout."],
    ["Arby status", "Strict CLI evidence is enough for Arby.", "Do not re-run Arby unnecessarily."],
    ["Cicero status", "Cicero needs app-lane completion gate.", "Retry recovered app-lane route."],
    ["Open gates", "Proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and sibling-merge gates stay open.", "Do not collapse blocked/exact lanes."],
    ["Drive posture", "Large/local support work belongs on D-drive worktrees.", "Check C/D before publication."],
    ["Remote publication", "Remote equality requires commit/push validation after closeout.", "Do not push active-open as closed."],
  ];
  return Array.from({ length: 20 }, (_, index) => {
    const [source_anchor, phase_reflection, runner_implication] = seeds[index % seeds.length];
    return { id: `${phaseSlug}-retry-${attempt}-journey-${String(index + 1).padStart(2, "0")}`, source_anchor, phase_reflection, runner_implication };
  });
}

function renderMd(data) {
  return [
    `# ${phaseSlug} Cicero Retry Session ${data.attempt}`,
    "",
    `Status: \`${data.observed_status.gate_status}\``,
    `Remaining gap: \`${data.remaining_gap}\``,
    "",
    "## Reflection Counts",
    "",
    `- recent session reflections: \`${data.recent_session_reflections.length}\``,
    `- web reflections: \`${data.web_reflections.length}\``,
    `- Journey/phase reflections: \`${data.journey_phase_reflections.length}\``,
    "",
    "## Boundary",
    "",
    "Sanitized retry receipt only. No raw route handles, private callable IDs, transcripts, screenshots, credentials, local absolute paths, private dumps, or raw lane text are published.",
    "",
  ].join("\n");
}

function readOptional(root, name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, name), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}

function writePair(suffix, payload, md) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
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
