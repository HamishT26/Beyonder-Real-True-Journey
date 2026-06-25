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
  route_tried: "recovered_app_lane_natural_pause_probe_without_duplicate_notify",
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
    "Preserved mini-6 as the sanitized publication lane and full-tools-5 as the richer private support lane.",
    "Ran a process-local, natural-pause recovered app-lane probe for Kierkegaard and Aristotle without publishing private route material.",
    "Confirmed recovered handles were available while the completion gate remained open.",
    "Ran the retry reflection protocol with current web/source context and Journey/phase continuity rows.",
    "Prepared a sanitized retry receipt and support-lane mirror for remote verification.",
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
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Version and feature claims should be checked against current release notes.", "Keep toolchain receipts current before long phase work."],
    ["OpenAI Codex releases", "https://github.com/openai/codex/releases", "CLI update requests need live verification.", "Record the exact local version observed."],
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode work should preserve active objectives without premature closure.", "Do not mark the persistent goal complete before v575 v8 x2."],
    ["OpenAI Codex goals cookbook", "https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex", "Long-running goals benefit from compact continuation receipts.", "Keep startup, compact, and closeout builders aligned."],
    ["OpenAI Codex prompting", "https://developers.openai.com/codex/prompting", "Precise instructions and boundaries reduce drift in tool-heavy loops.", "Refresh launch and retry skills when rules change."],
    ["OpenAI Codex app commands", "https://developers.openai.com/codex/app/commands", "App command surfaces can change during updates.", "Verify routes instead of relying on stale UI memory."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Background process starts require explicit completion evidence.", "Use watcher plus gate receipts."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Generated artifacts should use structured file operations.", "Prefer bounded JSON/MD receipts over raw dumps."],
    ["PowerShell Start-Process", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process", "Detached local helpers require clear window/background policy.", "Keep sibling runners backgrounded and harvest later."],
    ["PowerShell Get-Process", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-process", "Process checks should be status-only and scoped.", "Avoid babysitting lanes while productive cadence work runs."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "Worktree rotation must preserve clean branch provenance.", "Rotate to mini/full-tools successors only from clean heads."],
    ["GitHub branches", "https://docs.github.com/articles/about-branches", "Branch growth needs clear naming and publication boundaries.", "Use mini-N for sanitized load and full-tools-N for private support."],
    ["Playwright locators", "https://playwright.dev/docs/locators", "Browser automation should target stable controls rather than brittle screenshots.", "Keep main-thread handoffs evidence-based."],
    ["JSON Schema validation", "https://json-schema.org/draft/2020-12/json-schema-validation", "Receipts should be parseable before publication.", "Validate JSON before commit."],
    ["OpenSSF Scorecard", "https://github.com/ossf/scorecard", "Security posture should be treated as measurable and open-ended.", "Queue broad security automation behind exact approval gates."],
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
    ["omega-mini-6 current state", "mini-6 is the active sanitized lane for current publication.", "Publish only sanitized phase truth."],
    ["full-tools-5 support lane", "full-tools-5 is the richer private support lane for app-lane probes.", "Keep private route material local-only."],
    ["v557 v7 x2 closeout", "v8 x1 triad readiness is the current lane.", "Do not skip triad."],
    ["last-three Lumen proposal suite", "Grand Trinity Matrix and prototype lanes were reduced into safe public receipts.", "Use proposal suites as build backlog without raw transcript publication."],
    ["v8 x1 preflight", "Triad preflight passed and completion requires gates.", "Watcher start is not closure."],
    ["Aster harvest", "Aster passed strict CLI gates.", "Aster can feed x2 reduction."],
    ["App-lane probe 4", "Kierkegaard and Aristotle recovered handles were found, but completion gate remains open.", "Continue retry/cadence work without phase closeout."],
    ["Open gates", "Proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and merge gates remain open.", "Keep exact/blocked queued."],
    ["Worktree rotation policy", "Move to mini-N/full-tools-N successors when current worktrees get heavy, from clean verified heads only.", "Record rotation receipts before using successor lanes."],
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
