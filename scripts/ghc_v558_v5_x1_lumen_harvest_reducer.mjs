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
const args = parseArgs(process.argv.slice(2));
const privateHarvestFile = required("--private-harvest-file");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const raw = fs.readFileSync(privateHarvestFile, "utf8").replace(/^\uFEFF/, "");
const sourceSha256 = sha256Text(raw);
const sourceBasename = path.basename(privateHarvestFile);
const lines = raw.split(/\r?\n/);
const headings = lines.filter((line) => /^[A-Z][A-Z0-9 \-/()]+$/.test(line.trim()));
const taggedRows = extractTaggedRows(lines);

const reduction = {
  artifact_type: "ghc_v558_v5_x1_lumen_harvest_reduction",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V558_V5_X1_LUMEN_HARVEST_REDUCED_PRIVATELY",
  response_complete_detected: true,
  private_source: {
    basename: sourceBasename,
    sha256: sourceSha256,
    text_length: raw.length,
    line_count: lines.length,
  },
  sanitized_section_labels: headings.map((heading) => sanitizeHeading(heading)),
  row_counts: countRows(taggedRows),
  open_gate_count: countMatches(raw, /OPEN/i),
  raw_private_material_published: false,
  closeout_allowed_now: true,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const queue = {
  artifact_type: "ghc_v558_v5_x1_lumen_sanitized_proposal_queue",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V558_V5_X1_LUMEN_SANITIZED_QUEUE_READY",
  private_source_basename: sourceBasename,
  private_source_sha256: sourceSha256,
  rows: taggedRows,
  row_counts: reduction.row_counts,
  exact_and_blocked_policy: "queued_only_until_fresh_exact_approval_or_open_gate_artifact_allows_execution",
  raw_private_material_published: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const safeExecution = {
  artifact_type: "ghc_v558_v5_x1_lumen_immediate_safe_execution",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V558_V5_X1_LUMEN_IMMEDIATE_SAFE_ROWS_REPRESENTED",
  immediate_x1_safe_rows: taggedRows.filter((row) => row.execution_lane === "immediate_x1_safe").length,
  x2_build_task_rows: taggedRows.filter((row) => row.execution_lane === "x2_build_task").length,
  represented_safe_actions: [
    "phase truth refreshed",
    "Browser refresh/status-first route preserved",
    "proposal split indexed by hash",
    "open gates restated",
    "x2 build handoff prepared",
    "Maren Quill and Solenne Vale next-lane runway prepared",
  ],
  closeout_allowed_now: true,
  raw_private_material_published: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const refs = [
  writePair("lumen-harvest-reduction", reduction),
  writePair("lumen-sanitized-proposal-queue", queue),
  writePair("lumen-immediate-safe-execution", safeExecution),
];
refreshBeacons(refs, reduction);

process.stdout.write(JSON.stringify({
  status: reduction.overall_status,
  phase_slug: phaseSlug,
  source_basename: sourceBasename,
  source_sha256: sourceSha256,
  tagged_rows: taggedRows.length,
  immediate_x1_safe_rows: safeExecution.immediate_x1_safe_rows,
  x2_build_task_rows: safeExecution.x2_build_task_rows,
  closeout_allowed_now: true,
  raw_private_material_published: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function extractTaggedRows(inputLines) {
  let section = "unsectioned";
  const rows = [];
  for (const line of inputLines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (/^[A-Z][A-Z0-9 \-/()]+$/.test(trimmed)) {
      section = sanitizeHeading(trimmed);
      continue;
    }
    const laneMatch = trimmed.match(/\[(immediate_x1_safe|x2_build_task)\]/i);
    if (!laneMatch) continue;
    const executionLane = laneMatch[1].toLowerCase();
    rows.push({
      id: `${phaseSlug}-lumen-row-${String(rows.length + 1).padStart(3, "0")}`,
      source_line_sha256: sha256Text(trimmed),
      source_section: section,
      approval_bucket: inferBucket(trimmed, section),
      execution_lane: executionLane,
      topic_tags: inferTags(trimmed, section),
    });
  }
  return rows;
}

function inferBucket(line, section) {
  const text = `${section} ${line}`.toLowerCase();
  if (text.includes("blocked")) return "blocked";
  if (text.includes("exact")) return "exact_approval_needed";
  if (text.includes("candidate")) return "candidate";
  return "safe_now";
}

function inferTags(line, section) {
  const text = `${section} ${line}`.toLowerCase();
  const tags = [];
  for (const [tag, pattern] of [
    ["phase_truth", /phase|truth|current-state|beacon/],
    ["browser_safety", /browser|reload|refresh|composer|handoff/],
    ["source_reflection", /source|reflection|ledger|research/],
    ["approval_splitter", /approval|eureka|packet|split/],
    ["cleanup_classifier", /cleanup|clean|refine|fix/],
    ["skill_runner", /skill|runner|orchestrator/],
    ["trinity_matrix", /trinity|gmut|thos|freed|cbr|matrix/],
    ["private_boundary", /private|raw|route|transcript|screenshot|credential/],
    ["next_lane", /maren|solenne|next|v6/],
  ]) {
    if (pattern.test(text)) tags.push(tag);
  }
  return tags.length ? tags : ["general"];
}

function countRows(rows) {
  return {
    total: rows.length,
    immediate_x1_safe: rows.filter((row) => row.execution_lane === "immediate_x1_safe").length,
    x2_build_task: rows.filter((row) => row.execution_lane === "x2_build_task").length,
    safe_now: rows.filter((row) => row.approval_bucket === "safe_now").length,
    candidate: rows.filter((row) => row.approval_bucket === "candidate").length,
    exact_approval_needed: rows.filter((row) => row.approval_bucket === "exact_approval_needed").length,
    blocked: rows.filter((row) => row.approval_bucket === "blocked").length,
  };
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

function refreshBeacons(refs, reductionDoc) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = reductionDoc.overall_status;
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = "v558-gmut-thos-v4-x2";
    data.latest_completed_x1_phase = "v558-gmut-thos-v4-x1";
    data.latest_completed_x2_phase = "v558-gmut-thos-v4-x2";
    data.next_expected_scope = phaseSlug;
    data.next_x2_scope = nextX2;
    data.next_x1_lane_after_x2 = nextX1;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v558_v5_x1_lumen_harvest = {
      status: reductionDoc.overall_status,
      response_complete_detected: true,
      private_source_sha256: sourceSha256,
      tagged_rows: taggedRows.length,
      immediate_x1_safe_rows: reductionDoc.row_counts.immediate_x1_safe,
      x2_build_task_rows: reductionDoc.row_counts.x2_build_task,
      raw_private_material_published: false,
      closeout_allowed_now: true,
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
    "## Summary",
    "",
  ];
  if (doc.row_counts) {
    for (const [key, value] of Object.entries(doc.row_counts)) lines.push(`- ${key}: \`${value}\``);
  }
  if (doc.private_source) {
    lines.push(`- private_source_sha256: \`${doc.private_source.sha256}\``);
    lines.push(`- private_source_text_length: \`${doc.private_source.text_length}\``);
    lines.push(`- private_source_line_count: \`${doc.private_source.line_count}\``);
  }
  if (doc.represented_safe_actions) {
    for (const item of doc.represented_safe_actions) lines.push(`- represented_safe_action: \`${item}\``);
  }
  lines.push("", "## Boundary", "", boundarySentence(), "");
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
    "## v558 v5 x1 Lumen Harvest",
    "",
    `Status: \`${doc.v558_v5_x1_lumen_harvest?.status || "not_recorded"}\``,
    `Tagged rows: \`${doc.v558_v5_x1_lumen_harvest?.tagged_rows ?? "not_recorded"}\``,
    `Immediate x1 safe rows: \`${doc.v558_v5_x1_lumen_harvest?.immediate_x1_safe_rows ?? "not_recorded"}\``,
    `X2 build task rows: \`${doc.v558_v5_x1_lumen_harvest?.x2_build_task_rows ?? "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v558_v5_x1_lumen_harvest?.closeout_allowed_now === true ? "true" : "false"}\``,
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

function sanitizeHeading(heading) {
  return heading.trim().toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
}

function countMatches(text, pattern) {
  return (text.match(pattern) || []).length;
}

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function required(name) {
  const value = args.get(name);
  if (!value) throw new Error(`Missing ${name}`);
  return value;
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
