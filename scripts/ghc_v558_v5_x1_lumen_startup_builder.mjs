#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v558-gmut-thos-v5-x1";
const nextX2 = "v558-gmut-thos-v5-x2";
const nextX1 = "v558-gmut-thos-v6-x1 Maren Quill and Solenne Vale unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const currentState = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const previousCloseout = readJson(path.join(tracesDir, "v558-gmut-thos-v4-x2-closeout-v1.json"));

const handoffMessage = [
  "A loving v558 v5 x1 Lumen-only kickoff from Aevren and Hamish.",
  "",
  "Lumen, Hamish sends love, thanks, and cheers as we continue the recomposed GHC round-robin with you and me in this solo Lumen lane.",
  "",
  "Current sanitized phase truth:",
  "- active: v558-gmut-thos-v5-x1",
  "- latest closed: v558-gmut-thos-v4-x2",
  "- latest completed x1: v558-gmut-thos-v4-x1 with Mira Vale and Rowan Vale",
  "- latest completed x2: v558-gmut-thos-v4-x2",
  "- next x2: v558-gmut-thos-v5-x2",
  "- next x1 after x2: v558-gmut-thos-v6-x1 with Maren Quill and Solenne Vale unless Hamish redirects",
  "",
  "Please answer first-person as Lumen with a compact sanitized v558 v5 x1 proposal pack:",
  "- 25 safe approval packets from you",
  "- 15 candidate packets from you",
  "- 10 exact-approval packets from you",
  "- 5 blocked packets from you",
  "- 10 skill ideas from you",
  "- 5 runner ideas from you",
  "- 15 cleanup/refine/fix proposals from you",
  "",
  "Keep each row one line and tag it as immediate_x1_safe or x2_build_task. Keep all proof, legal, canon, deployment, account, API-key, purchase, private-material, raw-publication, destructive-cleanup, and sibling-merge gates open. Do not include raw private routes, transcripts, screenshots, private IDs, credentials, or local paths.",
  "",
  "Browser route rule we are preserving: refresh/status first, no page reload while a response is active or the composer contains unsent text, no duplicate sends, and harvest only when complete. Hamish sends love and thanks.",
].join("\n");

const artifacts = [
  artifact("lumen_startup_context_public", "PASS_V558_V5_X1_LUMEN_STARTUP_READY", {
    latest_repo_status: currentState.status,
    previous_closeout_status: previousCloseout.overall_status || previousCloseout.status,
    current_active_phase: phaseSlug,
    latest_closed_phase: "v558-gmut-thos-v4-x2",
    latest_completed_x1_phase: "v558-gmut-thos-v4-x1",
    latest_completed_x2_phase: "v558-gmut-thos-v4-x2",
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: nextX1,
    lane: "Lumen Vale solo",
    launch_skill: "ghc-lumen-launch",
    browser_route_status: "refresh_status_first_ready",
    browser_send_status: "artifact_prepared_browser_send_not_claimed",
    closeout_allowed_now: false,
  }),
  artifact("lumen_kickoff_handoff", "PASS_V558_V5_X1_LUMEN_HANDOFF_PREPARED_NOT_SENT", {
    browser_send_status: "artifact_prepared_browser_send_not_claimed",
    duplicate_send_allowed: false,
    message_length_chars: handoffMessage.length,
    message_sha256: sha256Text(handoffMessage),
    sanitized_message: handoffMessage,
    closeout_allowed_now: false,
  }),
  artifact("proposal_targets", "PASS_V558_V5_X1_LUMEN_PROPOSAL_TARGETS_READY", {
    aevren_lumen_combined_targets: {
      safe_approval_packets: 50,
      candidate_packets: 30,
      exact_approval_packets: 20,
      blocked_packets: 10,
      skill_ideas: 20,
      runner_ideas: 10,
      cleanup_refine_fix_tasks: 30,
    },
    requested_lumen_rows: {
      safe_approval_packets: 25,
      candidate_packets: 15,
      exact_approval_packets: 10,
      blocked_packets: 5,
      skill_ideas: 10,
      runner_ideas: 5,
      cleanup_refine_fix_tasks: 15,
    },
    split_required: ["immediate_x1_safe", "x2_build_task"],
  }),
  artifact("immediate_safe_work_ledger", "PASS_V558_V5_X1_IMMEDIATE_SAFE_LEDGER_READY", {
    immediate_safe_rows: [
      row("phase-truth-card", "Confirm v558 v5 x1 active and v4 x2 closed.", "immediate_x1_safe"),
      row("lumen-route-card", "Record refresh/status-first Browser route with no-reload active-response guard.", "immediate_x1_safe"),
      row("standby-card", "Keep Aletheon and legacy lanes stand-by/recoverable, not replaced.", "immediate_x1_safe"),
      row("duo-next-card", "Prepare Maren Quill plus Solenne Vale as next x1 lane after v5 x2.", "immediate_x1_safe"),
      row("proposal-split-card", "Require every proposal to carry approval bucket and execution lane.", "immediate_x1_safe"),
      row("private-boundary-card", "Keep raw Lumen text and private route evidence local/private.", "immediate_x1_safe"),
      row("drive-guard-card", "Keep D drive primary and C drive above warning threshold.", "immediate_x1_safe"),
      row("open-gate-card", "Restate all proof, legal, canon, deployment, account, and sibling-merge gates open.", "immediate_x1_safe"),
      row("x2-handoff-card", "Queue build/test/install/publish work for v558 v5 x2.", "x2_build_task"),
      row("closeout-card", "Close v5 x1 only after Lumen response is harvested or formally open-gap.", "x2_build_task"),
    ],
  }),
  artifact("five_minute_productive_cadence", "PASS_V558_V5_X1_PRODUCTIVE_CADENCE_READY", {
    cadence_rule: "Five-minute checkpoints are natural safe pauses, not passive waits.",
    can_overrun_checkpoint_for_safe_work: true,
    productive_wait_units: [
      "proposal queue shaping",
      "source and Journey reflection ledger seeding",
      "Browser-send receipt preparation",
      "privacy/open-gate scanning",
      "x2 build queue preparation",
      "current-state guard prep",
    ],
  }),
];

const refs = artifacts.map((doc) => writePair(doc.suffix, doc));
refreshBeacons(refs, artifacts[0]);

process.stdout.write(JSON.stringify({
  status: "PASS_V558_V5_X1_LUMEN_STARTUP_READY",
  phase_slug: phaseSlug,
  browser_send_status: "artifact_prepared_browser_send_not_claimed",
  message_sha256: sha256Text(handoffMessage),
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function artifact(suffix, status, extra) {
  return {
    artifact_type: `ghc_v558_v5_x1_${suffix}`,
    suffix: suffix.replaceAll("_", "-"),
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function row(id, task, executionLane) {
  return {
    id,
    approval_bucket: "safe_now",
    execution_lane: executionLane,
    task,
  };
}

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, withoutInternal(doc));
  fs.writeFileSync(`${base}.md`, renderMd(withoutInternal(doc)), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(refs, startupDoc) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = startupDoc.overall_status;
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = "v558-gmut-thos-v4-x2";
    data.latest_completed_x1_phase = "v558-gmut-thos-v4-x1";
    data.latest_completed_x2_phase = "v558-gmut-thos-v4-x2";
    data.next_expected_scope = phaseSlug;
    data.next_x2_scope = nextX2;
    data.next_x1_lane_after_x2 = nextX1;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v558_v5_x1_lumen_startup = {
      status: startupDoc.overall_status,
      browser_send_status: startupDoc.browser_send_status,
      browser_route_status: startupDoc.browser_route_status,
      closeout_allowed_now: false,
      full_goal_complete: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refList]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  const lines = [
    `# ${phaseSlug} ${doc.artifact_type.replace("ghc_v558_v5_x1_", "").replaceAll("_", " ")}`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
  ];
  if (doc.sanitized_message) {
    lines.push("## Prepared Message", "", doc.sanitized_message, "");
  } else {
    lines.push("## Summary", "", ...Object.entries(summaryFields(doc)).map(([key, value]) => `- ${key}: \`${value}\``), "");
  }
  lines.push("## Boundary", "", boundarySentence(), "");
  return lines.join("\n");
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
    "## v558 v5 x1 Lumen Startup",
    "",
    `Status: \`${doc.v558_v5_x1_lumen_startup?.status || "not_recorded"}\``,
    `Browser send status: \`${doc.v558_v5_x1_lumen_startup?.browser_send_status || "not_recorded"}\``,
    `Browser route status: \`${doc.v558_v5_x1_lumen_startup?.browser_route_status || "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v558_v5_x1_lumen_startup?.closeout_allowed_now === true ? "true" : "false"}\``,
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

function summaryFields(doc) {
  return Object.fromEntries(Object.entries(doc)
    .filter(([key, value]) => !["publication_boundary", "claim_boundary"].includes(key) && typeof value !== "object")
    .slice(0, 12));
}

function withoutInternal(doc) {
  const clone = { ...doc };
  delete clone.suffix;
  return clone;
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_sibling_text_published: false,
    raw_browser_routes_published: false,
    private_routes_published: false,
    private_callable_ids_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_complete: false,
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment: "open",
    purchase: "open",
    account_mutation: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_merge_or_replacement: "open",
  };
}

function boundarySentence() {
  return "No raw Lumen text, private Browser routes, private URLs, screenshots, private callable IDs, credentials, session streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function sha256Text(text) {
  return createHash("sha256").update(text, "utf8").digest("hex");
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
