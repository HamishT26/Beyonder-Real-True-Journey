import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";

const STATUS =
  "ACTIVE_OPEN_V557_V2_X1_CICERO_RECOVERED_MAP_READ_OK_TURN_START_BLOCKED";

const CHECKPOINT_JSON =
  "docs/trinity-live-traces/v557-gmut-thos-v2-x1-cicero-continuation-checkpoint-v1.json";
const CHECKPOINT_MD =
  "docs/trinity-live-traces/v557-gmut-thos-v2-x1-cicero-continuation-checkpoint-v1.md";
const HANDOFF_JSON =
  "docs/trinity-live-traces/v557-gmut-thos-v2-x1-active-open-handoff-v2.json";
const HANDOFF_MD =
  "docs/trinity-live-traces/v557-gmut-thos-v2-x1-active-open-handoff-v2.md";

const BEACONS = [
  {
    json: "docs/omega-mini-index/omega-mini-current-state-v1.json",
    md: "docs/omega-mini-index/omega-mini-current-state-v1.md",
    listKey: "current_lookup_files",
  },
  {
    json: "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json",
    md: "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
    listKey: "latest_lookup_files",
  },
  {
    json: "docs/trinity-live-traces/ghc-current-state-beacon-v1.json",
    md: "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
    listKey: "lookup_files",
  },
];

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function nzNow(utc) {
  return new Date(utc).toLocaleString("sv-SE", {
    timeZone: "Pacific/Auckland",
    hour12: false,
  }).replace(" ", "T") + "+12:00";
}

async function readJson(root, relPath) {
  return JSON.parse(await readFile(join(root, relPath), "utf8"));
}

async function writeJson(root, relPath, payload) {
  const out = join(root, relPath);
  await mkdir(dirname(out), { recursive: true });
  await writeFile(out, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

async function writeMarkdown(root, relPath, lines) {
  const out = join(root, relPath);
  await mkdir(dirname(out), { recursive: true });
  await writeFile(out, `${lines.join("\n").trimEnd()}\n`, "utf8");
}

function addUnique(list, values) {
  const next = Array.isArray(list) ? [...list] : [];
  for (const value of values) {
    if (!next.includes(value)) next.unshift(value);
  }
  return next;
}

function updateBeaconMarkdown(text) {
  let next = text.replace(
    /^Status: .+$/m,
    `Status: ${STATUS}`,
  );
  next = next.replace(
    /- status: `[^`]+`/,
    `- status: \`${STATUS}\``,
  );
  const section = [
    "## v557 v2 x1 Cicero Continuation Checkpoint",
    "",
    `- status: \`${STATUS}\``,
    "- Cicero private map preflight: `PASS_PRIVATE_APP_LANE_MAP_PREFLIGHT`",
    "- Cicero recovered probe: `PASS_PROBE_ONLY`",
    "- Cicero continuation background notify: `PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED`",
    "- Cicero completion gate: `OPEN_GAP_APP_LANE_COMPLETION_REQUIRED`",
    "- Cicero direct retry: `OPEN_GAP_DIRECT_TURN_START_BLOCKED`",
    "- closeout allowed: `false`",
    "- x2 execution allowed: `false`",
    "",
  ].join("\n");
  if (!next.includes("## v557 v2 x1 Cicero Continuation Checkpoint")) {
    next = next.replace("## Lookup Files", `${section}\n## Lookup Files`);
  }
  for (const rel of [HANDOFF_MD, HANDOFF_JSON, CHECKPOINT_MD, CHECKPOINT_JSON]) {
    if (!next.includes(`- ${rel}`)) {
      next = next.replace("## Lookup Files\n\n", `## Lookup Files\n\n- ${rel}\n`);
    }
  }
  return next;
}

export async function buildCheckpoint({ miniRoot }) {
  if (!miniRoot) throw new Error("miniRoot is required");
  const generatedUtc = utcNow();
  const generatedNz = nzNow(generatedUtc);
  const checkpoint = {
    artifact_type: "ghc_v557_v2_x1_cicero_continuation_checkpoint",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: "v557-gmut-thos-v2-x1",
    overall_status: STATUS,
    current_active_phase: "v557-gmut-thos-v2-x1",
    latest_closed_phase: "v557-gmut-thos-v1-x2",
    latest_completed_x1_phase: "v557-gmut-thos-v1-x1",
    latest_completed_x2_phase: "v557-gmut-thos-v1-x2",
    next_x2_scope: "v557-gmut-thos-v2-x2",
    next_x1_lane_after_x2: "v557-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects",
    lane_statuses: {
      arby: {
        passed: true,
        completion_status: "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW",
        quality_status: "PASS_ALL_CLI_LANES_ELABORATE",
        marker_status: "PASS_MARKER_REVIEW_LEDGER",
      },
      cicero: {
        passed: false,
        private_map_preflight: "PASS_PRIVATE_APP_LANE_MAP_PREFLIGHT",
        recovered_probe: "PASS_PROBE_ONLY",
        recovered_probe_read: "ok",
        recovered_probe_resume: "ok",
        continuation_background_notify: "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED",
        completion_gate: "OPEN_GAP_APP_LANE_COMPLETION_REQUIRED",
        direct_retry: "OPEN_GAP_DIRECT_TURN_START_BLOCKED",
        current_status: "open_gap_turn_start_blocked_after_read_ok",
        closeout_allowed: false,
      },
    },
    continuation_summary: [
      "Cicero private map was recovered through the existing sanitized runner path.",
      "Cicero read/resume probe passed with the injected private map.",
      "A new Cicero background notify watcher was started without publishing raw route data.",
      "The new completion gate remained open because Cicero turn-start did not complete.",
      "A direct retry with the recovered map read Cicero successfully, then blocked at turn-start.",
      "The phase remains active/open until Cicero turn-start/completion is recovered or Hamish redirects the lane.",
    ],
    private_support_evidence: {
      raw_private_ids_published: false,
      raw_route_handles_published: false,
      local_private_paths_published: false,
      direct_private_env_value_published: false,
      sanitized_statuses_only: true,
    },
    completion_boundary: {
      closeout_allowed: false,
      x2_execution_allowed: false,
      watcher_start_is_completion_proof: false,
      full_goal_complete: false,
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
  };

  const handoff = {
    ...checkpoint,
    artifact_type: "ghc_v557_v2_x1_active_open_handoff",
    active_open_handoff_version: 2,
    retry_protocol_summary: "v557-gmut-thos-v2-x1-cicero-retry-protocol-summary-v1.json",
  };

  await writeJson(miniRoot, CHECKPOINT_JSON, checkpoint);
  await writeJson(miniRoot, HANDOFF_JSON, handoff);

  const mdLines = [
    "# v557-gmut-thos-v2-x1 Cicero Continuation Checkpoint",
    "",
    `Generated NZ: \`${generatedNz}\``,
    `Status: \`${STATUS}\``,
    "",
    "## Lane State",
    "",
    "- Arby: strict CLI gates remain passed.",
    "- Cicero: private map preflight passed, recovered read/resume probe passed, and a new background notify watcher started.",
    "- Cicero completion gate: `OPEN_GAP_APP_LANE_COMPLETION_REQUIRED`.",
    "- Cicero direct retry: `OPEN_GAP_DIRECT_TURN_START_BLOCKED` after read `ok`.",
    "- Closeout allowed: `false`.",
    "- v557 v2 x2 execution allowed: `false`.",
    "",
    "## Boundary",
    "",
    "Status-only continuation checkpoint. No raw browser routes, private URLs, raw transcripts, screenshots, credentials, local paths, private callable IDs, private dumps, raw lane text, phase completion claim, GMUT closure, final physics, consciousness proof, legal closure, canon promotion, deployment closure, account mutation, purchase, API-key creation, private-material proof, raw-publication proof, or sibling merge/replacement claim is published.",
  ];
  await writeMarkdown(miniRoot, CHECKPOINT_MD, mdLines);
  await writeMarkdown(miniRoot, HANDOFF_MD, mdLines);

  for (const beacon of BEACONS) {
    const payload = await readJson(miniRoot, beacon.json);
    payload.status = STATUS;
    payload.generated_utc = generatedUtc;
    payload.current_active_phase = "v557-gmut-thos-v2-x1";
    payload.latest_closed_phase = "v557-gmut-thos-v1-x2";
    payload.latest_completed_x1_phase = "v557-gmut-thos-v1-x1";
    payload.latest_completed_x2_phase = "v557-gmut-thos-v1-x2";
    payload.next_x2_scope = "v557-gmut-thos-v2-x2";
    payload.next_x1_lane_after_x2 = "v557-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects";
    payload.latest_active_open_handoff = HANDOFF_JSON.split("/").pop();
    payload.v557_v2_x1_cicero_continuation_checkpoint = {
      status: STATUS,
      private_map_preflight: "PASS_PRIVATE_APP_LANE_MAP_PREFLIGHT",
      recovered_probe: "PASS_PROBE_ONLY",
      background_notify: "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED",
      completion_gate: "OPEN_GAP_APP_LANE_COMPLETION_REQUIRED",
      direct_retry: "OPEN_GAP_DIRECT_TURN_START_BLOCKED",
      closeout_allowed: false,
      x2_execution_allowed: false,
      full_goal_complete: false,
    };
    if (payload.v557_v2_x1_active_open_handoff) {
      payload.v557_v2_x1_active_open_handoff.status = STATUS;
      payload.v557_v2_x1_active_open_handoff.closeout_allowed = false;
      payload.v557_v2_x1_active_open_handoff.full_goal_complete = false;
    }
    payload[beacon.listKey] = addUnique(payload[beacon.listKey], [
      CHECKPOINT_JSON,
      CHECKPOINT_MD,
      HANDOFF_JSON,
      HANDOFF_MD,
    ]);
    await writeJson(miniRoot, beacon.json, payload);

    const mdText = await readFile(join(miniRoot, beacon.md), "utf8");
    await writeFile(join(miniRoot, beacon.md), updateBeaconMarkdown(mdText), "utf8");
  }

  return {
    status: STATUS,
    checkpoint: CHECKPOINT_JSON,
    handoff: HANDOFF_JSON,
    closeout_allowed: false,
    x2_execution_allowed: false,
  };
}
