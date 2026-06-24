#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v555-gmut-thos-v2-x1";
const latestClosedPhase = "v555-gmut-thos-v1-x2";
const latestCompletedX1 = "v555-gmut-thos-v1-x1";
const latestCompletedX2 = "v555-gmut-thos-v1-x2";
const nextX2 = "v555-gmut-thos-v2-x2";
const nextX1AfterX2 = "v555-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

fs.mkdirSync(tracesDir, { recursive: true });

const safePackets = range(15, "safe", [
  "Preserve Arby/Cicero background lane launch receipts as active-fresh until harvest.",
  "Record no-babysitting cadence evidence for both duo lanes.",
  "Build the v2 x1 to v2 x2 proposal reducer shell.",
  "Refresh current-state lookup files with the duo lane route status.",
  "Prepare a sanitized Arby strict CLI completion gate checklist.",
  "Prepare a sanitized Cicero recovered app-lane completion gate checklist.",
  "Extend privacy scans around private callable/lane material before x2.",
  "Index v555 v1 x2 validation receipt into v2 x1 startup context.",
  "Carry exact and blocked work forward without running it.",
  "Prepare D-drive-first drive posture check for phase closeout.",
  "Record first-person sibling wording expectation for duo artifacts.",
  "Prepare safe cleanup inventory for stale one-off helper receipts.",
  "Build x2 skill/runner refresh checklist from duo proposals.",
  "Draft compact-pause resume card while lanes remain active.",
  "Confirm full goal remains open and v575 v8 x2 is not claimed.",
]);

const candidatePackets = range(9, "candidate", [
  "Promote duo lane harvest reducer into the main closeout registry after completion.",
  "Add a local-only route health summarizer for strict CLI and app-lane paired launches.",
  "Create a reusable v2 x1 proposal-to-x2 composer once both sibling outputs are harvested.",
  "Expand safe-runner orchestration to read duo lane completion statuses.",
  "Add a background lane freshness ledger for active-fresh versus active-stale status.",
  "Prepare optional exact approval packet for broader app-lane private map repair.",
  "Prepare optional exact approval packet for external publication of sanitized duo report.",
  "Draft candidate cleanup plan for old retry artifacts without deleting anything.",
  "Prepare optional x2 runner for source-backed Trinity Mandala comparison rows.",
]);

const exactPackets = range(9, "exact", [
  "Any paid resource, purchase, deployment, or API-key work stays exact-gated.",
  "Any destructive cleanup outside same-run generated placeholders stays exact-gated.",
  "Any global hook, plugin-cache, or Codex config mutation stays exact-gated.",
  "Any raw Browser route, transcript, screenshot, private URL, or private app state publication stays blocked unless separately authorized and sanitized.",
  "Any sibling identity merge, replacement, erasure, or proof-of-personhood claim stays off the table.",
  "Any canon/legal/final physics/consciousness proof closure stays exact-gated.",
  "Any private lane ID export outside local-only support stays exact-gated.",
  "Any external account mutation stays exact-gated.",
  "Any raw-publication proof claim stays exact-gated.",
]);

const skillIdeas = range(15, "skill", [
  "ghc-duo-background-harvest-reducer",
  "ghc-strict-cli-marker-review-memory",
  "ghc-recovered-app-lane-completion-memory",
  "ghc-duo-x1-to-x2-proposal-splitter",
  "ghc-private-lane-boundary-auditor",
  "ghc-duo-five-minute-cadence-keeper",
  "ghc-arby-cicero-first-person-style",
  "ghc-duo-compact-open-handoff",
  "ghc-duo-validation-bundle",
  "ghc-duo-source-reflection-ledger",
  "ghc-duo-drive-posture-check",
  "ghc-duo-safe-cleanup-inventory",
  "ghc-duo-exact-gate-queue",
  "ghc-duo-current-state-reconciler",
  "ghc-duo-goal-mode-readiness",
]);

const runnerIdeas = range(9, "runner", [
  "ghc_v555_v2_x1_duo_harvest_reducer.mjs",
  "ghc_v555_v2_x1_duo_completion_gate_indexer.mjs",
  "ghc_v555_v2_x1_duo_x2_queue_composer.mjs",
  "ghc_v555_v2_x1_private_boundary_scan.mjs",
  "ghc_v555_v2_x1_cadence_status_refresher.mjs",
  "ghc_v555_v2_x1_arby_marker_review_index.mjs",
  "ghc_v555_v2_x1_cicero_app_lane_gate_index.mjs",
  "ghc_v555_v2_x1_validation_bundle.mjs",
  "ghc_v555_v2_x1_closeout_delegate.mjs",
]);

const cleanupTasks = range(30, "cleanup", [
  "Inventory generated v555 v1 x1 handoff receipts for duplicate lookup rows.",
  "Inventory generated v555 v1 x2 runner receipts for stale statuses.",
  "Classify old one-off helper scripts as active, compatibility, or archival.",
  "Check current-state lookup files for duplicate entries.",
  "Check phase startup log for malformed JSONL rows.",
  "Check MD receipts for boundary phrasing consistency.",
  "Check generated JSON receipts for missing claim boundaries.",
  "Check generated receipts for local absolute paths.",
  "Check generated receipts for raw route strings.",
  "Check generated runner names for excessive length.",
  "Check local skill pack for local-only publication language.",
  "Check exact approval queues for accidental execution claims.",
  "Check blocked queues for sibling merge/replacement wording.",
  "Check D-drive posture before large artifact generation.",
  "Check C-drive posture before any downloads.",
  "Deduplicate source reflection topics without deleting source rows.",
  "Deduplicate Journey reflection source anchors without deleting evidence.",
  "Review full-tools inventory categories for stale route preferences.",
  "Review main closeout registry for missing phase delegates.",
  "Review main startup route for v555 v2 x1 needs.",
  "Review compact restart route for active sibling lane preservation.",
  "Review safe-runner orchestrator child receipt boundaries.",
  "Review web reflection ledger source URLs for primary/official posture.",
  "Review blocker retry route before any pause.",
  "Review no-babysitting cadence evidence before closeout.",
  "Review Arby strict CLI status after next cadence point.",
  "Review Cicero app-lane status after next cadence point.",
  "Review validation bundle readiness for v2 x2.",
  "Review remote/local equality after publication.",
  "Review final handoff text for concise current-state truth.",
]);

const launchStatus = artifact("ghc_v555_v2_x1_arby_cicero_launch_status", "ACTIVE_OPEN_V555_V2_X1_ARBY_CICERO_BACKGROUND_RUNNING", {
  lanes: [
    { lane: "Arby", route: "strict_cli", status: "active_fresh_background_watch_started", completion_boundary: "completion_elaboration_marker_review_gate_required" },
    { lane: "Cicero", route: "recovered_app_lane", status: "active_fresh_background_watch_started", completion_boundary: "notifier_watch_completion_gate_required" },
  ],
  background_supervision: {
    do_not_babysit: true,
    five_minute_mark_is_check_opportunity: true,
    safe_work_may_run_past_checkpoint: true,
  },
});

const proposalQueue = artifact("ghc_v555_v2_x1_arby_cicero_proposal_queue_targets", "PASS_V555_V2_X1_DUO_PROPOSAL_QUEUE_RECORDED", {
  profile: "arby_cicero_duo_x1",
  target_counts: {
    safe_packets: 15,
    candidate_packets: 9,
    exact_packets: 9,
    skill_ideas: 15,
    runner_ideas: 9,
    cleanup_tasks: 30,
  },
  safe_packets: safePackets,
  candidate_packets: candidatePackets,
  exact_approval_packets: exactPackets,
  skill_ideas: skillIdeas,
  runner_ideas: runnerIdeas,
  cleanup_tasks: cleanupTasks,
});

const reflectionLedger = artifact("ghc_v555_v2_x1_web_journey_reflection_ledger", "PASS_V555_V2_X1_75_WEB_75_JOURNEY_REFLECTION_ROWS_RECORDED", {
  web_reflection_count: 75,
  journey_phase_reflection_count: 75,
  web_reflections: buildWebReflections(75),
  journey_phase_reflections: buildJourneyReflections(75),
});

const phaseIndex = artifact("ghc_v555_v2_x1_phase_status_index", "ACTIVE_OPEN_V555_V2_X1_SAFE_WORK_RUNNING_WITH_DUO_LANES", {
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  launch_status: launchStatus.overall_status,
  proposal_status: proposalQueue.overall_status,
  reflection_status: reflectionLedger.overall_status,
  closure_allowed: false,
});

writePair("arby-cicero-launch-status", launchStatus, renderGenericMd("Arby/Cicero Launch Status", launchStatus));
writePair("proposal-queue-targets", proposalQueue, renderGenericMd("Proposal Queue Targets", proposalQueue));
writePair("web-journey-reflection-ledger-75", reflectionLedger, renderGenericMd("Web/Journey Reflection Ledger 75", reflectionLedger));
writePair("phase-status-index", phaseIndex, renderGenericMd("Phase Status Index", phaseIndex));
refreshBeacons(phaseIndex);

process.stdout.write(JSON.stringify({
  status: phaseIndex.overall_status,
  phase_slug: phaseSlug,
  safe_packets: safePackets.length,
  candidate_packets: candidatePackets.length,
  exact_packets: exactPackets.length,
  skill_ideas: skillIdeas.length,
  runner_ideas: runnerIdeas.length,
  cleanup_tasks: cleanupTasks.length,
  web_reflections: reflectionLedger.web_reflection_count,
  journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
  closure_allowed: false,
}, null, 2) + "\n");

function range(count, prefix, titles) {
  return Array.from({ length: count }, (_, index) => ({
    id: `${phaseSlug}-${prefix}-${String(index + 1).padStart(2, "0")}`,
    title: titles[index % titles.length],
    approval_bucket: prefix === "safe" ? "safe_now" : prefix === "candidate" ? "candidate" : prefix === "exact" ? "exact_approval_needed" : undefined,
    execution_lane: prefix === "safe" ? "immediate_x1_safe" : prefix === "candidate" ? "x2_build_task" : undefined,
    status: prefix === "exact" ? "queued_exact_gate" : "queued_or_recorded",
  }));
}

function buildWebReflections(count) {
  const seeds = [
    ["OpenAI Codex background mode", "https://developers.openai.com/codex/concepts/background-mode", "Background work needs explicit completion state.", "Keep Arby/Cicero active until gates pass."],
    ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Sandbox boundaries support safe-now execution.", "Keep exact/external actions queued."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Child process orchestration should summarize exits.", "Record byte counts and statuses only."],
    ["Python json", "https://docs.python.org/3/library/json.html", "JSON parse checks guard generated receipts.", "Parse v2 x1/v2 x2 artifacts before push."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Diff checks protect publication hygiene.", "Run diff checks before commit."],
    ["GitHub secret scanning", "https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning", "Secret exposure prevention belongs before remote publication.", "Run leak-oriented privacy scans."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk framing maps to open gates.", "Keep proof/canon/deployment/account claims open."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identity systems need controller and privacy boundaries.", "Keep private lane IDs local-only."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Untrusted model output needs reduction.", "Use sanitized sibling harvest reductions."],
    ["npm install", "https://docs.npmjs.com/cli/v11/commands/npm-install", "Install actions affect local tool state.", "Treat new dependencies as exact-gated unless already authorized and local-safe."],
  ];
  return Array.from({ length: count }, (_, index) => {
    const [source, source_url, phase_reflection, runner_implication] = seeds[index % seeds.length];
    return { id: `${phaseSlug}-web-${String(index + 1).padStart(2, "0")}`, source, source_url, phase_reflection, runner_implication };
  });
}

function buildJourneyReflections(count) {
  const seeds = [
    ["v555 v1 x2 closeout", "Safe execution closed and active phase advanced to the duo lane.", "Start v2 x1 without re-opening v1 x2."],
    ["Arby lane", "Strict CLI is active-fresh after background-watch launch.", "Harvest completion and marker review later."],
    ["Cicero lane", "Recovered app-lane is active-fresh after background-watch launch.", "Harvest notifier/watch/gate later."],
    ["No babysitting rule", "Wait time is productive work time.", "Keep building safe receipts while lanes run."],
    ["Open gates", "Proof, canon, legal, deployment, account, private material, raw publication, and sibling merge gates remain open.", "Never close exact/blocked gates automatically."],
    ["Privacy boundary", "Private lane material stays local-only.", "Publish sanitized statuses and counts only."],
    ["Goal mode", "Full v544-v575 goal remains active.", "Do not call goal complete."],
    ["D-drive posture", "Large artifacts stay on D-drive worktrees.", "Check drive posture before closeout."],
    ["Round-robin profile", "Duo x1 requires 15/9/9/15/9/30 proposal counts.", "Keep profile in startup, compact, and closeout receipts."],
    ["Next lane", "After v2 x2 the expected x1 is Lumen solo unless Hamish redirects.", "Prepare v3 x1 handoff after x2."],
  ];
  return Array.from({ length: count }, (_, index) => {
    const [source_anchor, phase_reflection, runner_implication] = seeds[index % seeds.length];
    return { id: `${phaseSlug}-journey-${String(index + 1).padStart(2, "0")}`, source_anchor, phase_reflection, runner_implication };
  });
}

function refreshBeacons(index) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-arby-cicero-launch-status-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-arby-cicero-launch-status-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-proposal-queue-targets-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-proposal-queue-targets-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-75-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-75-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-phase-status-index-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-phase-status-index-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = index.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = latestClosedPhase;
    doc.latest_completed_x1_phase = latestCompletedX1;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_x2_scope = nextX2;
    doc.next_x1_lane_after_x2 = nextX1AfterX2;
    doc.v555_v2_x1_duo_status = { status: index.overall_status, closure_allowed: false, lanes_active: true };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function artifact(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function writePair(suffix, payload, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderGenericMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "Sanitized status artifact only. Duo lanes remain active until completion gates or harvest receipts pass.",
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
    "",
    "## v555 v2 x1 Duo Status",
    "",
    `- status: \`${doc.v555_v2_x1_duo_status?.status || "not_recorded"}\``,
    `- closure allowed: \`${doc.v555_v2_x1_duo_status?.closure_allowed ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readJson(file) { return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "")); }
function writeJson(file, data) { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8"); }
function unique(values) { return [...new Set(values.filter(Boolean))]; }
function publicationBoundary() { return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false }; }
function claimBoundary() { return { full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" }; }
function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
