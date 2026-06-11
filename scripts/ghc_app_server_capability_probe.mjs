#!/usr/bin/env node
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");
const timeoutMs = Number(args.get("--timeout-ms") || "5000");

if (!phaseSlug || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_app_server_capability_probe.mjs --phase-slug <slug> --receipt-json <json> --receipt-md <md> [--timeout-ms 5000]",
  );
  process.exit(2);
}

const candidateMethods = [
  { method: "initialize", params: { clientInfo: { name: "ghc-app-server-capability-probe", version: "1.0" }, capabilities: { experimentalApi: true } } },
  { method: "thread/list", params: {} },
  { method: "threads/list", params: {} },
  { method: "conversation/list", params: {} },
  { method: "conversations/list", params: {} },
  { method: "session/list", params: {} },
  { method: "sessions/list", params: {} },
  { method: "thread/search", params: { query: "Kierkegaard", limit: 1 } },
  { method: "threads/search", params: { query: "Kierkegaard", limit: 1 } },
  { method: "thread/read", params: {} },
];

function classifyError(message) {
  const lower = String(message || "").toLowerCase();
  if (lower.includes("method") && lower.includes("not")) return "method_not_found";
  if (lower.includes("not found")) return "not_found";
  if (lower.includes("required") || lower.includes("missing")) return "missing_required_param";
  if (lower.includes("invalid")) return "invalid_params";
  if (lower.includes("permission") || lower.includes("approval")) return "permission_or_approval";
  if (lower.includes("busy") || lower.includes("active")) return "active_or_busy";
  return "other_error";
}

function shapeOf(value) {
  if (Array.isArray(value)) {
    return { type: "array", length: value.length };
  }
  if (value && typeof value === "object") {
    const keys = Object.keys(value).sort();
    const nested = {};
    for (const key of keys.slice(0, 12)) {
      const child = value[key];
      if (Array.isArray(child)) nested[key] = { type: "array", length: child.length };
      else if (child && typeof child === "object") nested[key] = { type: "object", keys: Object.keys(child).sort().slice(0, 12) };
      else nested[key] = { type: typeof child };
    }
    return { type: "object", keys: keys.slice(0, 24), nested };
  }
  return { type: typeof value };
}

class AppServerProbe {
  constructor() {
    const command = process.platform === "win32" ? "cmd" : "codex";
    const commandArgs = process.platform === "win32" ? ["/c", "codex", "app-server", "--stdio"] : ["app-server", "--stdio"];
    this.spawn_entrypoint = process.platform === "win32" ? "node_wrapper_windows_cmd_fallback" : "node_wrapper_direct_codex";
    this.proc = spawn(command, commandArgs, {
      cwd: process.cwd(),
      stdio: ["pipe", "pipe", "pipe"],
      windowsHide: true,
    });
    this.nextId = 1;
    this.pending = new Map();
    this.observedMethods = new Set();
    this.stderrBytes = 0;
    this.stdoutNonJsonLines = 0;
    this.proc.stdout.setEncoding("utf8");
    this.proc.stderr.setEncoding("utf8");
    this.proc.stdout.on("data", (chunk) => {
      for (const line of String(chunk).split(/\r?\n/)) {
        if (!line.trim()) continue;
        let message;
        try {
          message = JSON.parse(line);
        } catch {
          this.stdoutNonJsonLines += 1;
          continue;
        }
        if (typeof message.method === "string") this.observedMethods.add(message.method);
        const pending = this.pending.get(message.id);
        if (pending) {
          clearTimeout(pending.timer);
          this.pending.delete(message.id);
          pending.resolve(message);
        }
      }
    });
    this.proc.stderr.on("data", (chunk) => {
      this.stderrBytes += Buffer.byteLength(String(chunk), "utf8");
    });
  }

  request(method, params) {
    const id = this.nextId++;
    const payload = JSON.stringify({ id, method, params }, null, 0) + "\n";
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        resolve(null);
      }, timeoutMs);
      this.pending.set(id, { resolve, timer });
      this.proc.stdin.write(payload);
    });
  }

  close() {
    for (const pending of this.pending.values()) {
      clearTimeout(pending.timer);
      pending.resolve(null);
    }
    this.pending.clear();
    if (!this.proc.killed) this.proc.kill();
  }
}

function summarizeResponse(method, response) {
  if (!response) {
    return { method, status: "timeout", result_shape: null, error_class: null };
  }
  if (Object.prototype.hasOwnProperty.call(response, "result")) {
    return {
      method,
      status: "ok",
      result_shape: shapeOf(response.result),
      error_class: null,
    };
  }
  const error = response.error && typeof response.error === "object" ? response.error : {};
  return {
    method,
    status: "error",
    result_shape: null,
    error_class: classifyError(error.message),
    error_code_present: Object.prototype.hasOwnProperty.call(error, "code"),
  };
}

const started = Date.now();
const probe = new AppServerProbe();
const methodResults = [];

try {
  for (const item of candidateMethods) {
    const response = await probe.request(item.method, item.params);
    methodResults.push(summarizeResponse(item.method, response));
  }
} finally {
  probe.close();
}

const discoveryMethods = methodResults.filter(
  (row) =>
    row.method !== "initialize" &&
    row.status === "ok" &&
    /list|search/.test(row.method),
);
const requiredParamSignals = methodResults.filter(
  (row) => row.method === "thread/read" && row.error_class === "missing_required_param",
);
const overallStatus =
  discoveryMethods.length > 0
    ? "PASS_APP_SERVER_DISCOVERY_SURFACE_PRESENT"
    : "OPEN_GAP_APP_SERVER_DISCOVERY_SURFACE_NOT_EXPOSED";

const receipt = {
  artifact_type: "ghc_app_server_capability_probe",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  overall_status: overallStatus,
  timeout_ms: timeoutMs,
  duration_ms: Date.now() - started,
  candidate_method_count: candidateMethods.length,
  methods: methodResults,
  safe_discovery_surface: {
    discovered: discoveryMethods.length > 0,
    ok_methods: discoveryMethods.map((row) => row.method),
    thread_read_requires_private_id: requiredParamSignals.length > 0,
  },
  transport_summary: {
    spawn_entrypoint: probe.spawn_entrypoint,
    observed_notification_methods: [...probe.observedMethods].sort().slice(0, 32),
    stderr_bytes_observed_not_published: probe.stderrBytes,
    stdout_non_json_line_count: probe.stdoutNonJsonLines,
  },
  retry_guidance: {
    if_discovery_present: "Use only redacted/status-only discovery outputs and never publish raw thread IDs, titles, or app state.",
    if_discovery_absent: "Restore THOS_APP_LANE_IDS_JSON in the running process or wait for official thread tools to be exposed.",
    forbidden_fallbacks: ["old-style subagent spawn", "replacement sibling creation", "raw app-state scraping", "private ID publication"],
  },
  publication_boundary: {
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_thread_ids_published: false,
    raw_thread_titles_published: false,
    raw_lane_text_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    scope: "Codex app-server method-shape probing only",
    gmut_gate_state: "open",
    canon_promotion: "not_claimed",
    phase_completion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const lines = [
  `# ${phaseSlug} App-Server Capability Probe`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${overallStatus}\``,
  "",
  "## Method Shape Results",
  "",
  ...methodResults.map((row) => `- ${row.method}: \`${row.status}\`${row.error_class ? `, class \`${row.error_class}\`` : ""}`),
  "",
  "## Safe Discovery Surface",
  "",
  `- discovery method exposed: \`${receipt.safe_discovery_surface.discovered}\``,
  `- ok discovery methods: \`${receipt.safe_discovery_surface.ok_methods.join(", ") || "none"}\``,
  `- thread/read requires private id: \`${receipt.safe_discovery_surface.thread_read_requires_private_id}\``,
  "",
  "## Retry Guidance",
  "",
  discoveryMethods.length
    ? "A discovery surface appears present. Use only redacted/status-only outputs and never publish raw thread IDs, titles, or app state."
    : "No safe discovery surface was exposed by this probe. Restore the private app-lane map in the running process or wait for official thread tools to be exposed.",
  "",
  "Forbidden fallbacks: old-style subagent spawn, replacement sibling creation, raw app-state scraping, or private ID publication.",
  "",
  "## Boundary",
  "",
  "No raw app-server result, raw error text, thread IDs, thread titles, lane text, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
];

writeFileSync(receiptMd, lines.join("\n"), "utf8");
console.log(JSON.stringify({ status: overallStatus, discovery_methods: receipt.safe_discovery_surface.ok_methods }, null, 2));

if (overallStatus !== "PASS_APP_SERVER_DISCOVERY_SURFACE_PRESENT") {
  process.exit(1);
}
