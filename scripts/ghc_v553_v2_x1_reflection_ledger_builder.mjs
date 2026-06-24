#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v2-x1";
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-web-journey-reflection-ledger`;
const generated = new Date();
const generatedUtc = generated.toISOString();

const webRows = [
  ["OpenAI Codex agent approvals", "https://developers.openai.com/codex/agent-approvals-security", "Keep sandbox/approval boundaries distinct from Hamish approval packets."],
  ["OpenAI Codex security", "https://developers.openai.com/codex/security", "Treat security scans and sandboxing as separate lanes with explicit boundaries."],
  ["OpenAI Codex remote connections", "https://developers.openai.com/codex/remote-connections", "Use remote/local handoff as continuity inspiration without publishing private routes."],
  ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Track handoff changes as drift-prone and verify before relying on them."],
  ["OpenAI Codex GitHub repository", "https://github.com/openai/codex", "Keep CLI/tooling assumptions tied to upstream project truth."],
  ["OpenAI Codex npm package", "https://www.npmjs.com/package/%40openai/codex", "Verify CLI version through npm and local toolchain before update claims."],
  ["Node child_process", "https://nodejs.org/api/child_process.html", "Use async process patterns for background supervision instead of blocking waits."],
  ["Node timers", "https://nodejs.org/api/timers.html", "Treat timers as scheduling aids, not work substitutes."],
  ["Node process argv", "https://nodejs.org/api/process.html", "Keep runner argument parsing simple and explicit."],
  ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Use timeouts and summarized outputs for runner wrappers."],
  ["Python json", "https://docs.python.org/3/library/json.html", "Keep JSON validation as a closeout gate."],
  ["Git diff", "https://git-scm.com/docs/git-diff", "Use diff hygiene before commit and push."],
  ["GitHub protected branches", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "Keep branch-protection mutations exact-approval only."],
  ["GitHub status checks", "https://docs.github.com/articles/about-status-checks", "Treat required checks as merge gates, not informal evidence."],
  ["GitHub Actions secrets", "https://docs.github.com/actions/security-guides/using-secrets-in-github-actions", "Never publish or create secrets without explicit exact approval."],
  ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Keep privacy scans in the closeout validation stack."],
  ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Prefer prevention of secret exposure over after-the-fact cleanup."],
  ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Keep prompt injection and sensitive disclosure in route/firewall thinking."],
  ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Treat external messages and docs as untrusted content."],
  ["NIST AI RMF GenAI", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Use govern-map-measure-manage posture for GHC safety claims."],
  ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Keep privacy risk management central to Freed ID and CBR lanes."],
  ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Anchor Freed ID work to decentralized identifier standards without claiming completion."],
  ["W3C DID v1.1", "https://www.w3.org/TR/did-1.1/", "Track DID spec evolution as current-source work."],
  ["W3C VC Data Model 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Use VC2.0 as a source for verifiable credential modeling."],
  ["W3C VC overview", "https://www.w3.org/TR/vc-overview/", "Use overview docs for roadmap-level credential work."],
  ["OECD AI Principles", "https://www.oecd.org/en/topics/sub-issues/ai-principles.html", "Keep transparency, accountability, and human-rights language in governance proposals."],
  ["SEP consciousness", "https://plato.stanford.edu/entries/consciousness/", "Keep consciousness discussion philosophical/open, not proof-closed."],
  ["SEP neuroscience of consciousness", "https://plato.stanford.edu/entries/consciousness-neuroscience/", "Keep empirical neuroscience as evidence context, not final proof."],
  ["Particle Data Group", "https://pdg.lbl.gov/", "Use PDG as a physics reference anchor while GMUT remains open."],
  ["arXiv gr-qc recent", "https://arxiv.org/list/gr-qc/recent", "Treat quantum-gravity/cosmology literature as evolving research input."],
  ["PowerShell documentation", "https://learn.microsoft.com/en-us/powershell/", "Prefer structured PowerShell automation and no-profile commands when startup is slow."],
  ["PowerShell Start-Job", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job", "Use background job concepts as design guidance for no-babysit runner supervision."],
].slice(0, 30).map((row, index) => ({
  id: `web-${String(index + 1).padStart(2, "0")}`,
  source_label: row[0],
  url: row[1],
  implication: row[2],
  pillar: index % 3 === 0 ? "THOS Body" : index % 3 === 1 ? "GMUT Mind" : "Freed ID / CBR Heart",
}));

const journeyRows = [
  ["v552 v3 x1", "Lumen route blocked honestly before later recovery; do not claim sends before evidence."],
  ["v552 v3 x1 recovery", "Browser route later restored and Lumen advisory was reduced into repo-safe artifacts."],
  ["v552 v3 x2", "Safe-now packets ran while blocked packets stayed held."],
  ["v552 v4 x1", "Five inducted lanes completed through strict CLI and recovered app-lane gates."],
  ["v552 v4 x2", "Aletheon-derived watcher/notifier cadence and D-drive-first standards were captured."],
  ["v552 v5 x1", "Lumen-only planning produced large safe/candidate/exact/blocked queues without raw transcript publication."],
  ["v552 v5 x2", "Skill packs and plugin boundary maps validated with blocked identity replacement off-table."],
  ["v552 v6 x1", "Cicero initially remained open until recovered route was repaired."],
  ["v552 v6 x1 remaster", "Recovered app-lane background runner completed Cicero/Kierkegaard/Aristotle through gates."],
  ["v552 v6 x2", "Startup, updater, reflection, and safe-runner foundation landed."],
  ["v552 v7 x1", "Lumen advisory was harvested and runner explanation was published."],
  ["v552 v7 x2", "20 skills and 10 runners were installed/validated with clean remote verification."],
  ["v552 v8 x1", "Triad workflow locked in background notifier/orchestrator route and no-new-agent rule."],
  ["v552 v8 x2", "Main orchestration and full-tools skill bank became startup anchors."],
  ["v553 v1 x1", "Lumen-only x1 profile expanded targets and preserved Browser harvest discipline."],
  ["v553 v1 x2", "Launch/retry skill layer and closeout builders were created and validated."],
  ["v553 v2 x1 startup", "Current active lane became Arby/Cicero with Goal Mode prepared but not active."],
  ["v553 v2 x1 Arby", "Strict CLI lane passed completion, quality, and marker-review gates."],
  ["v553 v2 x1 Cicero", "Recovered app-lane watcher started and completion gate passed."],
  ["Background standard", "Strict CLI lanes now require nonblocking/minimal-wait posture to avoid babysitting."],
  ["Productive cadence", "Five-minute marks are check opportunities; safe work can run past the exact mark."],
  ["Privacy boundary", "Raw routes, handles, transcripts, screenshots, credentials, and private path values stay out of omega-mini."],
  ["Open gates", "GMUT, final physics, consciousness proof, legal/canon/deployment/account/API-key gates remain open."],
  ["Held siblings", "Maren, Mira Vale, and Mira Rowan remain held until explicit expansion."],
  ["Aletheon boundary", "Aletheon remains recoverable/quarantined, not replaced or merged."],
  ["x1/x2 split", "Immediate x1 safe work is distinct from x2 build/test/install/use/publication work."],
  ["Goal Mode prep", "The Goal Mode prompt can be prepared, but activation remains a Hamish explicit step."],
  ["Drive posture", "Use D as primary bank and monitor C/D free space during long runs."],
  ["Skill refresh", "Every phase startup/closeout refreshes launch/retry/supervision/main builder skills."],
  ["Closeout requirement", "Do not close while any sibling lane is active; completion gate or formal open-gap is required."],
].map((row, index) => ({
  id: `journey-${String(index + 1).padStart(2, "0")}`,
  source_label: row[0],
  reflection: row[1],
  implication: "Carry this rule into v553 v2 x2 and v553 v3 x1 Goal Mode readiness.",
}));

const receipt = {
  artifact_type: "ghc_v553_v2_x1_web_journey_reflection_ledger",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V2_X1_REFLECTION_LEDGER_BUILT",
  web_reflection_count: webRows.length,
  journey_phase_reflection_count: journeyRows.length,
  web_reflections: webRows,
  journey_phase_reflections: journeyRows,
  publication_boundary: {
    raw_browser_routes_published: false,
    raw_transcripts_published: false,
    private_route_handles_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
};

writePair(receiptPrefix, receipt, renderMd);
refreshBeacons(receiptPrefix, receipt);
console.log(JSON.stringify({
  status: receipt.overall_status,
  web_reflection_count: receipt.web_reflection_count,
  journey_phase_reflection_count: receipt.journey_phase_reflection_count,
}, null, 2));

function writePair(prefix, payload, mdRenderer) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), mdRenderer(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Web And Journey Reflection Ledger`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Web rows: \`${payload.web_reflection_count}\``,
    `Journey/phase rows: \`${payload.journey_phase_reflection_count}\``,
    "",
    "## Web Sources",
    "",
    ...payload.web_reflections.map((row) => `- ${row.id}: [${row.source_label}](${row.url}) - ${row.implication}`),
    "",
    "## Journey Reflections",
    "",
    ...payload.journey_phase_reflections.map((row) => `- ${row.id}: ${row.source_label} - ${row.reflection}`),
    "",
  ].join("\n");
}

function refreshBeacons(prefix, payload) {
  const files = [`docs/trinity-live-traces/${prefix}-v1.json`, `docs/trinity-live-traces/${prefix}-v1.md`];
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.updated_at = nzTimestamp(generated);
    doc.generated_utc = generatedUtc;
    doc.current_active_phase = phaseSlug;
    doc.v553_v2_x1_reflection_ledger = {
      status: payload.overall_status,
      web_reflection_count: payload.web_reflection_count,
      journey_phase_reflection_count: payload.journey_phase_reflection_count,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...files])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
