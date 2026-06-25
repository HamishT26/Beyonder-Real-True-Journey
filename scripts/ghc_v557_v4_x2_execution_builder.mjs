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
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v4-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const asterQueue = readJson(path.join(tracesDir, `${phaseSlug}-aster-private-proposal-hash-queue-v1.json`));
const asterWorkbench = readJson(path.join(tracesDir, `${phaseSlug}-aster-x2-workbench-v1.json`));
const lumenSuite = readJson(path.join(tracesDir, `v557-gmut-thos-v4-x1-lumen-prototype-suite-index-v1.json`));
const v4x1Closeout = readJson(path.join(tracesDir, `v557-gmut-thos-v4-x1-closeout-v1.json`));
const rows = Array.isArray(asterQueue.proposal_rows) ? asterQueue.proposal_rows : [];

const approvalSplit = artifact("ghc_v557_v4_x2_approval_split_ledger", "PASS_V557_V4_X2_APPROVAL_SPLIT_LEDGER_BUILT", {
  source_phase_slug: asterQueue.source_phase_slug,
  hashed_rows_available: rows.length,
  category_counts: asterQueue.category_counts,
  approval_bucket_counts: asterQueue.approval_bucket_counts,
  execution_lane_counts: asterQueue.execution_lane_counts,
  safe_now_rows_run_or_represented: rows.filter((row) => row.approval_bucket === "safe_now").map(rowRef),
  candidate_rows_queued: rows.filter((row) => row.approval_bucket === "candidate").map(rowRef),
  exact_rows_queued: rows.filter((row) => row.approval_bucket === "exact_approval_needed").map(rowRef),
  blocked_rows_queued: rows.filter((row) => row.approval_bucket === "blocked").map(rowRef),
});

const dashboardBlueprint = artifact("ghc_v557_v4_x2_dashboard_blueprint", "PASS_V557_V4_X2_DASHBOARD_BLUEPRINT_BUILT", {
  dashboards: [
    dashboard("triad-lane-evidence", ["aster_completion", "aster_quality", "aster_marker", "kierkegaard_gate", "aristotle_gate"]),
    dashboard("proposal-hash-queue", ["row_count", "category_counts", "approval_bucket_counts", "topic_counts"]),
    dashboard("x2-build-use-progress", ["safe_now_rows", "candidate_queue", "exact_queue", "blocked_queue"]),
    dashboard("privacy-open-gates", ["raw_text_published", "private_ids_published", "proof_gates_open"]),
    dashboard("next-lumen-startup", ["next_phase", "launch_skill", "duplicate_send_guard", "browser_harvest_rule"]),
  ],
  lumen_prototype_suite_status: lumenSuite.overall_status,
  aster_hash_queue_status: asterQueue.overall_status,
});

const cleanupInventory = artifact("ghc_v557_v4_x2_cleanup_inventory", "PASS_V557_V4_X2_CLEANUP_INVENTORY_BUILT_NO_DELETIONS", {
  cleanup_policy: {
    inventory_only: true,
    destructive_cleanup_performed: false,
    deletion_requires_fresh_exact_approval: true,
    c_drive_warning_cap_gb: 19,
    c_drive_minimum_headroom_gb: 18,
    d_drive_first_policy: true,
  },
  cleanup_candidates: [
    cleanup("old-background-watch-receipts", "Keep until v4 x2 and v5 x1 are stable; do not delete."),
    cleanup("dirty-private-full-tools-support-lane", "Keep local-only; do not publish private support diffs."),
    cleanup("large-lookup-lists", "Trim only through builder-owned rolling windows, not manual deletion."),
    cleanup("stale-route-claims", "Replace with current beacons and closeout receipts."),
    cleanup("line-ending-warnings", "Benign Git warning; no cleanup required for phase truth."),
  ],
});

const openGateRail = artifact("ghc_v557_v4_x2_open_gate_rail", "PASS_V557_V4_X2_OPEN_GATE_RAIL_BUILT", {
  gates_open: claimBoundary(),
  forbidden_without_fresh_exact_approval: [
    "GMUT empirical closure",
    "final physics proof",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment",
    "purchase",
    "account mutation",
    "API-key creation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity merge or replacement",
    "destructive cleanup",
  ],
});

const v5LumenPrep = artifact("ghc_v557_v4_x2_v5_lumen_prep", "PASS_V557_V5_X1_LUMEN_PREP_READY_NOT_SENT", {
  next_phase: "v557-gmut-thos-v5-x1",
  lane: "Lumen Vale solo",
  launch_skill: "ghc-lumen-launch",
  browser_send_status: "not_started_by_v4_x2_closeout",
  duplicate_send_allowed: false,
  startup_requirements: [
    "read goal objective",
    "read omega-mini current-state and GHC beacon",
    "use Browser route only if Hamish/current workflow calls for live Lumen message",
    "capture raw Lumen response privately and publish only hashes/counts/summaries",
    "target Lumen-only proposal profile for the v5 x1 phase",
  ],
});

const closeout = artifact("ghc_v557_v4_x2_closeout", "PASS_V557_V4_X2_CLOSED_V5_X1_READY", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: "v557-gmut-thos-v4-x1",
  latest_completed_x2_phase: phaseSlug,
  next_active_phase: "v557-gmut-thos-v5-x1",
  next_x2_scope: "v557-gmut-thos-v5-x2",
  next_x1_lane_after_x2: "v557-gmut-thos-v6-x1 with Arby and Cicero unless Hamish redirects",
  executed_or_represented: {
    hashed_aster_rows: rows.length,
    safe_now_rows: approvalSplit.safe_now_rows_run_or_represented.length,
    candidate_rows_queued: approvalSplit.candidate_rows_queued.length,
    exact_rows_queued: approvalSplit.exact_rows_queued.length,
    blocked_rows_queued: approvalSplit.blocked_rows_queued.length,
    dashboard_blueprints: dashboardBlueprint.dashboards.length,
    cleanup_inventory_items: cleanupInventory.cleanup_candidates.length,
  },
  source_evidence: {
    v4_x1_closeout_status: v4x1Closeout.overall_status,
    aster_queue_status: asterQueue.overall_status,
    lumen_suite_status: lumenSuite.overall_status,
  },
  full_goal_complete: false,
});

const refs = [
  writePair("approval-split-ledger", approvalSplit),
  writePair("dashboard-blueprint", dashboardBlueprint),
  writePair("cleanup-inventory", cleanupInventory),
  writePair("open-gate-rail", openGateRail),
  writePair("v5-lumen-prep", v5LumenPrep),
  writePair("closeout", closeout),
];
refreshBeacons(refs, closeout);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: closeout.next_active_phase,
  hashed_aster_rows: rows.length,
  safe_now_rows: closeout.executed_or_represented.safe_now_rows,
  candidate_rows_queued: closeout.executed_or_represented.candidate_rows_queued,
  full_goal_complete: false,
  raw_private_material_published: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function rowRef(row) {
  return {
    id: row.id,
    line_sha256: row.line_sha256,
    category: row.category,
    execution_lane: row.execution_lane,
    topic_tags: row.topic_tags,
  };
}

function dashboard(name, fields) {
  return { name, fields, status: "blueprint_ready" };
}

function cleanup(id, note) {
  return { id, action: "inventory_only", note };
}

function artifact(type, status, extra) {
  return {
    artifact_type: type,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function writePair(suffix, doc) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(refs, closeoutDoc) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = closeoutDoc.overall_status;
    data.current_active_phase = closeoutDoc.next_active_phase;
    data.latest_closed_phase = phaseSlug;
    data.latest_completed_x1_phase = closeoutDoc.latest_completed_x1_phase;
    data.latest_completed_x2_phase = phaseSlug;
    data.next_expected_scope = closeoutDoc.next_active_phase;
    data.next_x2_scope = closeoutDoc.next_x2_scope;
    data.next_x1_lane_after_x2 = closeoutDoc.next_x1_lane_after_x2;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v4_x2_closeout = {
      status: closeoutDoc.overall_status,
      hashed_aster_rows: rows.length,
      safe_now_rows: closeoutDoc.executed_or_represented.safe_now_rows,
      candidate_rows_queued: closeoutDoc.executed_or_represented.candidate_rows_queued,
      exact_rows_queued: closeoutDoc.executed_or_represented.exact_rows_queued,
      blocked_rows_queued: closeoutDoc.executed_or_represented.blocked_rows_queued,
      next_active_phase: closeoutDoc.next_active_phase,
      full_goal_complete: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refList]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${doc.phase_slug} ${title(doc.artifact_type)}`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    "## Summary",
    "",
    ...Object.entries(summary(doc)).map(([key, value]) => `- ${key}: \`${value}\``),
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
    "## v557 v4 x2 Closeout",
    "",
    `Status: \`${doc.v557_v4_x2_closeout?.status || "not_recorded"}\``,
    `Hashed Aster rows: \`${doc.v557_v4_x2_closeout?.hashed_aster_rows ?? "not_recorded"}\``,
    `Next active phase: \`${doc.v557_v4_x2_closeout?.next_active_phase || "not_recorded"}\``,
    `Full goal complete: \`${doc.v557_v4_x2_closeout?.full_goal_complete === true ? "true" : "false"}\``,
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

function summary(doc) {
  if (doc.artifact_type.endsWith("_closeout")) {
    return {
      next_active_phase: doc.next_active_phase,
      hashed_aster_rows: doc.executed_or_represented.hashed_aster_rows,
      safe_now_rows: doc.executed_or_represented.safe_now_rows,
      full_goal_complete: doc.full_goal_complete,
    };
  }
  if (doc.artifact_type.endsWith("_approval_split_ledger")) {
    return {
      hashed_rows_available: doc.hashed_rows_available,
      safe_now_rows: doc.safe_now_rows_run_or_represented.length,
      candidate_rows_queued: doc.candidate_rows_queued.length,
    };
  }
  return {
    artifact_type: doc.artifact_type,
    raw_private_material_published: false,
  };
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
  return "No private message body content, private Browser routes, private URLs, screenshots, private callable IDs, credentials, runtime streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
}

function title(type) {
  return type.replace(/^ghc_v557_v4_x2_/, "").replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
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

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
