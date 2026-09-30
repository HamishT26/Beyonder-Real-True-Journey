import crypto from "node:crypto";

export const ALLOWED_OPERATIONS = new Set([
  "validate",
  "simulate",
  "summarize",
  "render_static",
]);

export const PROHIBITED_KEY_PATTERN =
  /(token|secret|password|credential|api[_-]?key|private[_-]?task|thread[_-]?id|transcript|session[_-]?stream)/i;

export function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalize(value[key])]),
    );
  }
  return value;
}

export function canonicalJson(value) {
  return JSON.stringify(canonicalize(value));
}

export function sha256Value(value) {
  return crypto
    .createHash("sha256")
    .update(canonicalJson(value), "utf8")
    .digest("hex");
}

function visitKeys(value, path = "$", hits = []) {
  if (Array.isArray(value)) {
    value.forEach((entry, index) =>
      visitKeys(entry, `${path}[${index}]`, hits),
    );
    return hits;
  }
  if (!value || typeof value !== "object") return hits;
  for (const [key, child] of Object.entries(value)) {
    if (PROHIBITED_KEY_PATTERN.test(key)) hits.push(`${path}.${key}`);
    visitKeys(child, `${path}.${key}`, hits);
  }
  return hits;
}

function relativeSafePath(path) {
  return (
    typeof path === "string" &&
    path.length > 0 &&
    !path.startsWith("/") &&
    !/^[a-zA-Z]:[\\/]/.test(path) &&
    !path.split(/[\\/]/).includes("..")
  );
}

export function validateCapsule(capsule) {
  const errors = [];
  if (!capsule || typeof capsule !== "object" || Array.isArray(capsule)) {
    return { ok: false, errors: ["capsule must be an object"] };
  }
  if (capsule.schema_version !== "ghc.nexus.capsule.v1")
    errors.push("schema_version");
  if (!/^[0-9a-f]{40}$/i.test(capsule.source_commit ?? ""))
    errors.push("source_commit");
  if (!/^[0-9a-f]{64}$/i.test(capsule.source_manifest_sha256 ?? "")) {
    errors.push("source_manifest_sha256");
  }
  if (!["public", "internal_sanitized"].includes(capsule.classification)) {
    errors.push("classification");
  }
  const created = Date.parse(capsule.created_at ?? "");
  const expires = Date.parse(capsule.expires_at ?? "");
  if (!Number.isFinite(created)) errors.push("created_at");
  if (!Number.isFinite(expires) || expires <= created)
    errors.push("expires_at");
  if (
    !Number.isFinite(capsule.max_cost_usd) ||
    capsule.max_cost_usd < 0 ||
    capsule.max_cost_usd > 50
  ) {
    errors.push("max_cost_usd");
  }
  if (!Array.isArray(capsule.operations) || capsule.operations.length === 0) {
    errors.push("operations");
  } else if (
    capsule.operations.some((operation) => !ALLOWED_OPERATIONS.has(operation))
  ) {
    errors.push("operations_allowlist");
  }
  if (!Array.isArray(capsule.files) || capsule.files.length === 0) {
    errors.push("files");
  } else {
    for (const file of capsule.files) {
      if (!relativeSafePath(file?.path)) errors.push("file_path");
      if (!/^[0-9a-f]{64}$/i.test(file?.sha256 ?? ""))
        errors.push("file_sha256");
      if (!Number.isInteger(file?.bytes) || file.bytes < 0)
        errors.push("file_bytes");
    }
  }
  const authority = capsule.authority_claims;
  if (!authority || typeof authority !== "object") {
    errors.push("authority_claims");
  } else if (Object.values(authority).some((value) => value !== false)) {
    errors.push("authority_nonpromotion");
  }
  const prohibited = visitKeys(capsule);
  if (prohibited.length) errors.push(`prohibited_keys:${prohibited.join(",")}`);
  return { ok: errors.length === 0, errors: [...new Set(errors)] };
}

export function nextPhase(version, slot) {
  if (
    !Number.isInteger(version) ||
    !Number.isInteger(slot) ||
    slot < 1 ||
    slot > 8
  ) {
    throw new Error("invalid phase coordinate");
  }
  return slot === 8
    ? { version: version + 1, slot: 1 }
    : { version, slot: slot + 1 };
}

export function projectRoster(input, endpoint = { version: 725, slot: 8 }) {
  const cycle = input?.cycle;
  if (!Array.isArray(cycle) || cycle.length === 0)
    throw new Error("cycle required");
  const expectedPositions = cycle.map((entry) => entry.position);
  if (new Set(expectedPositions).size !== cycle.length)
    throw new Error("duplicate cycle position");
  if (cycle.some((entry, index) => entry.position !== index + 1)) {
    throw new Error("cycle positions must be contiguous and ordered");
  }
  if (
    cycle.some((entry) => /^New ChatGPT\/Codex Dot sibling/.test(entry.owner))
  ) {
    throw new Error("uninstantiated Dot placeholder entered executable cycle");
  }
  const startIndex = cycle.findIndex(
    (entry) => entry.owner === input.effective_cursor.next_numbered_owner,
  );
  if (startIndex < 0) throw new Error("next owner missing from cycle");

  let version = 708;
  let slot = 4;
  let cycleIndex = startIndex;
  const rows = [];
  while (
    version < endpoint.version ||
    (version === endpoint.version && slot <= endpoint.slot)
  ) {
    const entry = cycle[cycleIndex];
    rows.push({
      sequence: rows.length + 1,
      owner: entry.owner,
      environment: entry.environment,
      phase: `v${version}-v${slot}`,
      cycle_position: entry.position,
      state: "prospective_projection_only",
    });
    if (version === endpoint.version && slot === endpoint.slot) break;
    ({ version, slot } = nextPhase(version, slot));
    cycleIndex = (cycleIndex + 1) % cycle.length;
  }
  return {
    schema: "ghc.local-cloud-roster.projection.v1",
    source_schema: input.schema,
    start: rows[0],
    endpoint: rows.at(-1),
    row_count: rows.length,
    expected_historical_endpoint: "Eiren Kestrel v725-v8",
    endpoint_conflict: rows.at(-1).owner !== "Eiren Kestrel",
    projection_is_not_activation: true,
    rows,
  };
}

export function privilegeMatrix() {
  return {
    schema: "ghc.privilege.non-equivalence.v1",
    dimensions: [
      {
        id: "app_mode",
        observed: "full_access",
        grants: ["tool_capability"],
        does_not_grant: ["windows_admin", "cloud_root"],
      },
      {
        id: "sandbox_mode",
        observed: "danger-full-access",
        grants: ["filesystem_capability"],
        does_not_grant: ["windows_admin", "external_authority"],
      },
      {
        id: "windows_sandbox",
        observed: "elevated",
        grants: ["configured_elevated_sandbox"],
        does_not_grant: ["proof_of_child_process_token"],
      },
      {
        id: "windows_process_token",
        observed: "not_probed",
        grants: [],
        does_not_grant: ["inferred_admin"],
      },
      {
        id: "managed_cloud",
        observed: "separate_linux_runtime",
        grants: ["configured_cloud_runtime"],
        does_not_grant: ["local_d_drive_access", "windows_admin"],
      },
    ],
    all_equivalent: false,
  };
}

export function buildModels() {
  const seeds = [
    ["local-canonical", 1, 5, 5, 1, "completed"],
    ["sanitized-export", 2, 4, 5, 2, "completed"],
    ["cloud-validation", 5, 3, 4, 3, "represented"],
    ["quarantined-return", 3, 4, 5, 2, "completed"],
    ["direct-cloud-merge", 5, 1, 1, 5, "exact_gate"],
    ["expired-capsule", 4, 2, 4, 4, "open_gap"],
    ["secret-bearing-export", 4, 1, 1, 5, "exact_gate"],
    ["equal-output-different-provenance", 3, 2, 4, 4, "represented"],
    ["unresolved-dot-placeholder", 2, 2, 5, 5, "exact_gate"],
    ["saelin-cloud-startup", 5, 3, 4, 3, "represented"],
    ["local-config-audit", 1, 5, 5, 1, "completed"],
    ["cloud-drift-detected", 5, 4, 4, 3, "open_gap"],
    ["provider-spend-zero", 4, 4, 5, 2, "completed"],
    ["journey-analogy-firewall", 1, 4, 5, 4, "completed"],
    ["stage20-promotion", 5, 1, 1, 5, "exact_gate"],
  ];
  return seeds.map(
    (
      [id, locality, evidence, reversibility, authorityGap, disposition],
      index,
    ) => ({
      id: `M${String(index + 1).padStart(2, "0")}`,
      label: id,
      coordinates: {
        locality,
        evidence,
        reversibility,
        authority_gap: authorityGap,
      },
      disposition,
      physical_claim: false,
      production_claim: false,
    }),
  );
}
