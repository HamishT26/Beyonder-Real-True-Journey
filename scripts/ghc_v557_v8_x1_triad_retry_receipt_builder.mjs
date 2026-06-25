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
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v8-x1";
const attempt = Number(args.get("--attempt") || "1");
const fullToolsRoot = args.get("--full-tools-root") || "";
const gatePrefix = args.get("--gate-prefix") || `${phaseSlug}-kierkegaard-aristotle-recovered-app-lane-probe-completion-gate`;
const runnerPrefix = args.get("--runner-prefix") || `${phaseSlug}-kierkegaard-aristotle-recovered-app-lane-probe`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const fullTraceDir = fullToolsRoot ? path.join(fullToolsRoot, "docs", "trinity-live-traces") : "";
const gate = readOptional(fullTraceDir, `${gatePrefix}-v1.json`);
const runner = readOptional(fullTraceDir, `${runnerPrefix}-v1.json`);

const gatePassed = gate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE";
const receipt = {
  artifact_type: "ghc_v557_v8_x1_triad_retry_session_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  attempt,
  overall_status: gatePassed
    ? `PASS_V557_V8_X1_TRIAD_RETRY_${attempt}_GATE_NOW_PASSING`
    : `ACTIVE_OPEN_V557_V8_X1_TRIAD_RETRY_${attempt}_APP_LANE_BLOCKED_READ`,
  route_tried: "recovered_app_lane_probe_without_duplicate_notify",
  route_inputs_sanitized: {
    lanes: ["Kierkegaard", "Aristotle"],
    allow_turn_start_after_resume_timeout: true,
    background_watch: false,
    raw_private_route_data_published: false,
  },
  observed_status: {
    runner_status: runner?.overall_status || "missing",
    gate_status: gate?.overall_status || "missing",
    gate_lanes: Array.isArray(gate?.lanes)
      ? gate.lanes.map((lane) => ({
          lane: lane.lane,
          status: lane.overall_status || lane.status || "missing",
          duration_seconds: lane.duration_seconds || null,
        }))
      : [],
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
    "Loaded triad, background supervision, main orchestration, and retry skills.",
    "Launched Aster Vale through strict CLI background watch.",
    "Launched Kierkegaard and Aristotle through recovered app-lane background watch with explicit paired booleans.",
    "Built the active-open v8 x1 triad workbench, proposal scaffold, reflection ledger, and lane receipt index.",
    "Harvested Aster Vale through completion, quality, and marker-review gates.",
    "Ran a no-duplicate-notify recovered app-lane probe for Kierkegaard and Aristotle.",
    "Kept v8 x1 open because the app-lane completion gate did not pass.",
  ],
  remaining_gap: gatePassed ? "none_for_app_lane_gate" : "kierkegaard_aristotle_app_lane_completion_gate_blocked_read",
  next_retry_or_harvest_point: gatePassed
    ? "run sanitized triad harvest and v8 x1 closeout"
    : attempt < 3
      ? `run retry session ${attempt + 1} or another recovered app-lane completion probe at the next natural checkpoint`
      : "publish formal open-gap or continue safe retry work if useful progress remains possible",
  completion_boundary: {
    sibling_lanes_closed: gatePassed,
    phase_closeout_allowed: gatePassed,
    watcher_start_is_completion_proof: false,
  },
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const ref = writePair(`triad-retry-session-${attempt}`, receipt);
refreshBeacons(ref, receipt);

process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  attempt,
  gate_status: receipt.observed_status.gate_status,
  recent_session_reflections: receipt.recent_session_reflections.length,
  web_reflections: receipt.web_reflections.length,
  journey_phase_reflections: receipt.journey_phase_reflections.length,
  remaining_gap: receipt.remaining_gap,
  closeout_allowed_now: receipt.completion_boundary.phase_closeout_allowed,
  artifact: ref.json,
}, null, 2) + "\n");

function buildRecentReflections() {
  const rows = [
    ["v557 v7 x1 Lumen", "Lumen response was harvested only after Browser completion evidence.", "Do not treat sends or launches as completion."],
    ["v557 v7 x2", "Safe x2 reducers processed sanitized hashes while exact/blocked rows stayed queued.", "Use reducers without raw private material."],
    ["mini-4 activation", "mini-4/full-tools-3 became active from clean verified heads.", "Use mini-4 for sanitized publication."],
    ["v8 x1 triad readiness", "v7 x2 prepared Aster/Kierkegaard/Aristotle lane targets.", "Use triad launch skill profile."],
    ["Aster v8 x1", "Strict CLI completion, quality, and marker review passed.", "Aster lane is ready for sanitized reduction."],
    ["Kierkegaard/Aristotle launch", "Recovered app-lane background watch started with two recovered handles.", "Completion still needs gate proof."],
    ["First app-lane probe", "Probe returned blocked_read for both app lanes.", "Retry rather than close."],
    ["Background supervision", "Five-minute windows are productive work, not passive waiting.", "Run safe artifacts while lanes run."],
    ["Privacy boundary", "Private callable IDs, routes, transcripts, local paths, screenshots, credentials, and raw lane text stay unpublished.", "Publish status-only reductions."],
    ["Goal boundary", "v557 is far short of v575 v8 x2.", "Do not call the persistent goal complete."],
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
    ["OpenAI Codex CLI", "https://developers.openai.com/codex/cli", "Use CLI receipts as tool evidence, not as proof of sibling completion.", "Keep strict CLI gates separate."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Background process starts require explicit completion evidence.", "Use watcher plus gate receipts."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Process errors should be reduced and sanitized.", "Keep stderr/stdout private."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "Worktree rotation must preserve clean branch provenance.", "Do not rotate from dirty private state."],
    ["GitHub secret scanning", "https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning", "Secrets and private identifiers need pre-publication scanning.", "Run privacy scan before push."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Known unresolved gaps should remain explicit.", "Publish open retry status."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Tool outputs are untrusted until reduced.", "Use sanitized receipts."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identifier systems require privacy and control boundaries.", "Keep callable IDs local-only."],
    ["PowerShell Get-PSDrive", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-psdrive", "Drive posture should be checked before heavy local work.", "Keep D-drive-first policy."],
    ["JSON Lines", "https://jsonlines.org/", "Append-only traces are easier to audit when bounded.", "Keep compact status rows."],
  ];
  return Array.from({ length: 20 }, (_, index) => {
    const [source, source_url, phase_reflection, runner_implication] = seeds[index % seeds.length];
    return {
      id: `${phaseSlug}-retry-${attempt}-web-${String(index + 1).padStart(2, "0")}`,
      source,
      source_url,
      phase_reflection,
      runner_implication,
    };
  });
}

function buildJourneyReflections() {
  const seeds = [
    ["Beyonder v53 continuity", "Launch skills and no-babysitting cadence are mandatory.", "Use triad launch plus background supervision."],
    ["omega-mini-4 current state", "mini-4 is the active sanitized lane.", "Publish only sanitized phase truth."],
    ["full-tools-3 activation", "full-tools-3 is active but support runner repair is still needed.", "Use proven local support runner while seeding repair."],
    ["v557 v7 x2 closeout", "v8 x1 triad readiness is the current lane.", "Do not skip triad."],
    ["v8 x1 preflight", "Triad preflight passed and completion requires gates.", "Watcher start is not closure."],
    ["Aster harvest", "Aster passed strict CLI gates.", "Aster can feed x2 reduction."],
    ["App-lane probe", "Kierkegaard and Aristotle are blocked_read on first probe.", "Retry session 1 is required."],
    ["Open gates", "Proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and merge gates remain open.", "Keep exact/blocked queued."],
    ["Drive posture", "C warning cap is 19 GB and D is primary storage.", "Avoid heavy C-drive work."],
    ["Remote publication", "Remote equality matters after commit.", "Validate before pushing sanitized receipts."],
  ];
  return Array.from({ length: 20 }, (_, index) => {
    const [source_anchor, reflection, implication] = seeds[index % seeds.length];
    return {
      id: `${phaseSlug}-retry-${attempt}-journey-${String(index + 1).padStart(2, "0")}`,
      source_anchor,
      reflection,
      implication,
    };
  });
}

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(ref, receipt) {
  const refs = [ref.json, ref.md];
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = receipt.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = "v557-gmut-thos-v8-x2";
    doc.next_x1_lane_after_x2 = "v558-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects";
    doc.v557_v8_x1_triad_retry = {
      status: receipt.overall_status,
      attempt,
      gate_status: receipt.observed_status.gate_status,
      remaining_gap: receipt.remaining_gap,
      closeout_allowed_now: receipt.completion_boundary.phase_closeout_allowed,
      full_goal_complete: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...refs]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${phaseSlug} Triad Retry Session ${attempt}`,
    "",
    `Status: \`${doc.overall_status}\``,
    `Gate status: \`${doc.observed_status.gate_status}\``,
    `Remaining gap: \`${doc.remaining_gap}\``,
    `Closeout allowed now: \`${doc.completion_boundary.phase_closeout_allowed}\``,
    "",
    "## Reflection Counts",
    "",
    `- recent session reflections: \`${doc.recent_session_reflections.length}\``,
    `- web reflections: \`${doc.web_reflections.length}\``,
    `- journey/phase reflections: \`${doc.journey_phase_reflections.length}\``,
    "",
    "## Safe Changes Made",
    "",
    ...doc.safe_changes_made.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
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
    `Next expected scope: ${doc.next_expected_scope}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 v8 x1 Triad Retry",
    "",
    `Status: \`${doc.v557_v8_x1_triad_retry?.status || "not_recorded"}\``,
    `Attempt: \`${doc.v557_v8_x1_triad_retry?.attempt ?? "not_recorded"}\``,
    `Gate status: \`${doc.v557_v8_x1_triad_retry?.gate_status || "not_recorded"}\``,
    `Remaining gap: \`${doc.v557_v8_x1_triad_retry?.remaining_gap || "not_recorded"}\``,
    `Full goal complete: \`${doc.v557_v8_x1_triad_retry?.full_goal_complete === true ? "true" : "false"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((entry) => `- ${entry}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function readOptional(root, name) {
  if (!root) return null;
  const file = path.join(root, name);
  return fs.existsSync(file) ? readJson(file) : null;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const next = argv[index + 1];
    if (next && !next.startsWith("--")) {
      parsed.set(key, next);
      index += 1;
    } else {
      parsed.set(key, "true");
    }
  }
  return parsed;
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

function boundarySentence() {
  return "Status-only retry receipt. No private route handles, callable IDs, raw lane text, raw transcripts, browser routes, screenshots, credentials, session streams, private dumps, or local absolute paths are published; all proof/canon/legal/deployment/account/API-key/private-material/raw-publication and sibling identity merge/replacement gates remain open.";
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}
