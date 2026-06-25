#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v4-x2";
const sourcePhaseSlug = args.get("--source-phase-slug") || "v557-gmut-thos-v4-x1";
const inputFile = args.get("--aster-final-message-input") || process.env.GHC_ASTER_FINAL_MESSAGE_INPUT;
const expectedHash = args.get("--expected-hash");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

if (!inputFile) {
  console.error("Missing --aster-final-message-input.");
  process.exit(2);
}

const raw = fs.readFileSync(inputFile, "utf8");
const sourceHash = sha256(raw);
if (expectedHash && sourceHash !== expectedHash) {
  console.error(JSON.stringify({ status: "HASH_MISMATCH", expectedHash, sourceHash }, null, 2));
  process.exit(1);
}

const rows = extractRows(raw);
const categoryCounts = countBy(rows.map((row) => row.category));
const approvalCounts = countBy(rows.map((row) => row.approval_bucket));
const executionCounts = countBy(rows.map((row) => row.execution_lane));
const topicCounts = countTopics(rows);

const queue = artifact("ghc_v557_v4_x2_aster_private_proposal_hash_queue", "PASS_ASTER_PRIVATE_PROPOSAL_HASH_QUEUE_BUILT", {
  source_phase_slug: sourcePhaseSlug,
  source_digest: {
    source_kind: "private_aster_strict_cli_final_message",
    source_sha256: sourceHash,
    source_bytes: Buffer.byteLength(raw, "utf8"),
    raw_text_published: false,
    input_path_published: false,
  },
  proposal_rows: rows,
  row_count: rows.length,
  category_counts: categoryCounts,
  approval_bucket_counts: approvalCounts,
  execution_lane_counts: executionCounts,
  topic_counts: topicCounts,
});

const x2Workbench = artifact("ghc_v557_v4_x2_aster_x2_workbench", "PASS_V557_V4_X2_ASTER_WORKBENCH_STARTED", {
  source_phase_slug: sourcePhaseSlug,
  input_queue_status: queue.overall_status,
  source_sha256: sourceHash,
  x2_build_use_scope: [
    workItem("phase-truth-and-closeout-reducer", "safe_now", "Use v4 x1 closeout evidence to guard v4 x2 phase truth."),
    workItem("strict-cli-proposal-digest", "safe_now", "Use Aster proposal hashes and category counts without raw output."),
    workItem("triad-dashboard-blueprint", "safe_now", "Combine Aster CLI evidence with Kierkegaard/Aristotle app-gate completion."),
    workItem("x2-approval-splitter", "safe_now", "Split hashed rows into safe, candidate, exact, and blocked work lanes."),
    workItem("x2-cleanup-inventory", "safe_now", "Classify cleanup as inventory-only unless exact approval is required."),
    workItem("x2-open-gate-rail", "safe_now", "Keep proof/canon/deployment/account gates open."),
    workItem("v5-lumen-prep", "safe_now", "Prepare next Lumen solo x1 after v4 x2 closes."),
  ],
  x2_counts: {
    hashed_rows_available: rows.length,
    safe_now_rows: approvalCounts.safe_now || 0,
    candidate_rows: approvalCounts.candidate || 0,
    exact_rows_queued: approvalCounts.exact_approval_needed || 0,
    blocked_rows_queued: approvalCounts.blocked || 0,
  },
  raw_text_published: false,
});

const refs = [
  writePair("aster-private-proposal-hash-queue", queue),
  writePair("aster-x2-workbench", x2Workbench),
];
refreshBeacons(refs, x2Workbench);

process.stdout.write(JSON.stringify({
  status: x2Workbench.overall_status,
  phase_slug: phaseSlug,
  source_phase_slug: sourcePhaseSlug,
  source_sha256: sourceHash,
  rows: rows.length,
  category_counts: categoryCounts,
  approval_bucket_counts: approvalCounts,
  raw_text_published: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function extractRows(text) {
  const lines = text.split(/\r?\n/);
  let category = "uncategorized";
  const rows = [];
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    const heading = normalizedHeading(trimmed);
    if (heading) {
      category = heading;
      continue;
    }
    if (!/^([-*]|\d+[.)])\s+/.test(trimmed)) continue;
    const compact = trimmed.replace(/^([-*]|\d+[.)])\s+/, "").trim();
    if (compact.length < 16) continue;
    const topicTags = inferTopicTags(compact);
    rows.push({
      id: `${phaseSlug}-aster-row-${String(rows.length + 1).padStart(3, "0")}`,
      source_phase_slug: sourcePhaseSlug,
      source_line_index: lines.indexOf(line) + 1,
      line_sha256: sha256(compact),
      category,
      approval_bucket: inferApprovalBucket(compact, category),
      execution_lane: inferExecutionLane(compact, category),
      topic_tags: topicTags,
    });
  }
  return rows;
}

function normalizedHeading(line) {
  const cleaned = line.replace(/^#+\s*/, "").trim();
  const upper = cleaned.toUpperCase();
  const known = [
    "COMMAND PROPOSALS",
    "EUREKA TASKS",
    "SKILL OR MICRO-WORKFLOW PROPOSALS",
    "SYSTEM EXPANSION PROPOSALS",
    "X2 BUILD PRIORITIES",
    "RISKS AND BLOCKERS",
  ];
  const found = known.find((item) => upper.startsWith(item));
  return found ? found.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "") : null;
}

function inferApprovalBucket(text, category) {
  const t = `${text} ${category}`.toLowerCase();
  if (/\bblocked\b|\brisk\b|\bmust not\b|\bwithout fresh\b/.test(t)) return "blocked";
  if (/\bexact\b|\bapproval\b|\bprivate id\b|\bapi key\b|\bdeploy\b|\bpurchase\b|\bdelete\b|\bdestructive\b/.test(t)) return "exact_approval_needed";
  if (/\bsafe\b|\binventory\b|\bhash\b|\bdigest\b|\bledger\b|\bdashboard\b|\breducer\b|\bvalidator\b|\bclassifier\b|\bguard\b|\bprototype\b/.test(t)) return "safe_now";
  return "candidate";
}

function inferExecutionLane(text, category) {
  const t = `${text} ${category}`.toLowerCase();
  if (/\bx2\b|\bbuild\b|\brun\b|\btest\b|\binstall\b|\buse\b|\bprototype\b|\bdashboard\b|\breducer\b|\bclassifier\b|\bvalidator\b|\bledger\b/.test(t)) {
    return "x2_build_task";
  }
  return "immediate_x1_safe";
}

function inferTopicTags(text) {
  const t = text.toLowerCase();
  const topics = {
    phase_truth: /\bphase\b|\btruth\b|\bcloseout\b|\bbeacon\b/,
    strict_cli: /\bcli\b|\bstrict\b|\bmarker\b|\bquality\b/,
    approval_splitter: /\bapproval\b|\beureka\b|\bpacket\b|\bsplit\b/,
    cleanup_classifier: /\bcleanup\b|\bdelete\b|\binventory\b|\brefine\b/,
    dashboard: /\bdashboard\b|\bmatrix\b|\bboard\b/,
    runner_skill: /\brunner\b|\bskill\b|\bworkflow\b|\bcommand\b/,
    privacy_gate: /\bprivate\b|\braw\b|\bcredential\b|\bsecret\b|\bpath\b/,
    source_reflection: /\bsource\b|\breflection\b|\bweb\b|\bjourney\b/,
    next_phase: /\bv5\b|\blumen\b|\bnext\b/,
  };
  return Object.entries(topics).filter(([, regex]) => regex.test(t)).map(([topic]) => topic);
}

function countTopics(rows) {
  const counts = {};
  for (const row of rows) {
    for (const topic of row.topic_tags) {
      counts[topic] = (counts[topic] || 0) + 1;
    }
  }
  return counts;
}

function workItem(id, bucket, purpose) {
  return { id, approval_bucket: bucket, purpose, status: "queued_or_started_safe_x2" };
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

function refreshBeacons(refs, doc) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = doc.overall_status;
    data.current_active_phase = phaseSlug;
    data.next_expected_scope = phaseSlug;
    data.latest_closed_phase = sourcePhaseSlug;
    data.latest_completed_x1_phase = sourcePhaseSlug;
    data.next_x2_scope = phaseSlug;
    data.next_x1_lane_after_x2 = "v557-gmut-thos-v5-x1 with Lumen Vale solo unless Hamish redirects";
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v4_x2_aster_private_reduction = {
      status: doc.overall_status,
      source_phase_slug: sourcePhaseSlug,
      source_sha256: sourceHash,
      hashed_rows_available: rows.length,
      raw_text_published: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refList]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  const lines = [
    `# ${doc.phase_slug} Aster Private Reduction`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    "## Summary",
    "",
    `- source phase: \`${doc.source_phase_slug || sourcePhaseSlug}\``,
    `- hashed rows: \`${doc.row_count || doc.x2_counts?.hashed_rows_available || 0}\``,
    `- raw text published: \`false\``,
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ];
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
    "## v557 v4 x2 Aster Private Reduction",
    "",
    `Status: \`${doc.v557_v4_x2_aster_private_reduction?.status || "not_recorded"}\``,
    `Hashed rows available: \`${doc.v557_v4_x2_aster_private_reduction?.hashed_rows_available ?? "not_recorded"}\``,
    `Raw text published: \`${doc.v557_v4_x2_aster_private_reduction?.raw_text_published === true ? "true" : "false"}\``,
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
    phase_completion_scope: "v557_v4_x2_private_safe_reduction_only",
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

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function countBy(values) {
  return values.reduce((acc, value) => {
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});
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
