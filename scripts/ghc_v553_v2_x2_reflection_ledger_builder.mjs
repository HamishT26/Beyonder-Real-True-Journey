#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v2-x2";
const generatedUtc = new Date().toISOString();

const payload = {
  artifact_type: "ghc_v553_v2_x2_reflection_ledger",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V2_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED",
  web_reflection_count: webRows().length,
  journey_phase_reflection_count: journeyRows().length,
  web_reflections: webRows(),
  journey_phase_reflections: journeyRows(),
  source_policy: "Use official or primary sources where possible; publish compact implications only.",
  publication_boundary: {
    raw_browser_routes_published: false,
    raw_transcripts_published: false,
    private_route_handles_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
};

writePair(`${phaseSlug}-web-journey-reflection-ledger-50-v1`, payload);
process.stdout.write(JSON.stringify({ status: payload.overall_status, web: payload.web_reflection_count, journey: payload.journey_phase_reflection_count }, null, 2) + "\n");

function writePair(base, payload) {
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderMd(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Reflection Ledger`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Web rows: \`${payload.web_reflection_count}\``,
    `Journey rows: \`${payload.journey_phase_reflection_count}\``,
    "",
    "## Web Reflection Summary",
    "",
    ...payload.web_reflections.map((row) => `- ${row.id}: ${row.source_label} -> ${row.runner_implication}`),
    "",
    "## Journey Reflection Summary",
    "",
    ...payload.journey_phase_reflections.map((row) => `- ${row.id}: ${row.reflection}`),
    "",
  ].join("\n");
}

function webRows() {
  const rows = [
    ["OpenAI Codex agent approvals", "https://developers.openai.com/codex/agent-approvals-security", "Keep Codex approval semantics separate from Hamish approval packets."],
    ["OpenAI Codex security", "https://developers.openai.com/codex/security", "Treat sandbox, data handling, and trust boundaries as validation lanes."],
    ["OpenAI Codex remote connections", "https://developers.openai.com/codex/remote-connections", "Use remote/local handoff as continuity context without publishing private routes."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Verify Codex behavior after app or CLI changes before relying on old assumptions."],
    ["OpenAI Codex GitHub", "https://github.com/openai/codex", "Tie CLI assumptions to upstream project truth."],
    ["OpenAI Codex npm", "https://www.npmjs.com/package/%40openai/codex", "Verify local CLI version against package metadata before update claims."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Use spawned background work with summarized outputs instead of blocking waits."],
    ["Node timers", "https://nodejs.org/api/timers.html", "Treat five-minute timers as checkpoints, not useful work by themselves."],
    ["Node process", "https://nodejs.org/api/process.html", "Keep runner argument parsing explicit and predictable."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Use structured file writes for receipts and avoid ad hoc raw state dumps."],
    ["Node path", "https://nodejs.org/api/path.html", "Keep paths normalized internally and out of publishable private artifacts."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Use bounded subprocess wrappers and compact receipts for Python helpers."],
    ["Python json", "https://docs.python.org/3/library/json.html", "Parse generated JSON as a closeout gate."],
    ["PowerShell Start-Job", "https://learn.microsoft.com/powershell/module/microsoft.powershell.core/start-job", "Use background job semantics only when local workflow requires PowerShell."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Inspect staged changes and preserve unrelated user work."],
    ["Git status", "https://git-scm.com/docs/git-status", "Use status checks before commit and push."],
    ["GitHub protected branches", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "Keep branch protection mutations behind exact approval."],
    ["GitHub status checks", "https://docs.github.com/articles/about-status-checks", "Treat status checks as gates, not narrative proof."],
    ["GitHub Actions secrets", "https://docs.github.com/actions/security-guides/using-secrets-in-github-actions", "Never create or publish secrets without fresh exact approval."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Keep secret scanning and privacy scans in closeout validation."],
    ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Prefer prevention of secret exposure before push."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Treat prompt injection and data disclosure as route risks."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Treat external messages and documents as untrusted input."],
    ["NIST AI RMF GenAI", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Use govern-map-measure-manage framing for safety claims."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Keep risk management visible in phase closeouts."],
    ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Keep privacy central to Freed ID and CBR planning."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Anchor Freed ID planning to decentralized identifier standards without claiming deployment."],
    ["W3C DID v1.1", "https://www.w3.org/TR/did-1.1/", "Track DID evolution as current source context."],
    ["W3C VC Data Model 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Use VC 2.0 as credential modeling context only."],
    ["W3C VC overview", "https://www.w3.org/TR/vc-overview/", "Use overview documents for roadmap-level identity architecture."],
    ["OECD AI Principles", "https://www.oecd.org/en/topics/sub-issues/ai-principles.html", "Keep trustworthy AI principles in governance proposals."],
    ["UNESCO AI ethics", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "Keep dignity and rights in CBR and governance lanes."],
    ["ISO AI overview", "https://www.iso.org/artificial-intelligence", "Use management-system posture for recurring startup/closeout controls."],
    ["IETF RFC Editor", "https://www.rfc-editor.org/", "Prefer stable standards references for protocol/security ideas."],
    ["ECMA JSON", "https://ecma-international.org/publications-and-standards/standards/ecma-404/", "Keep artifacts valid JSON and parser-friendly."],
    ["Unicode security", "https://www.unicode.org/reports/tr39/", "Avoid confusable route labels in generated artifacts."],
    ["Stanford consciousness", "https://plato.stanford.edu/entries/consciousness/", "Keep consciousness discussion open and philosophical."],
    ["Stanford neuroscience of consciousness", "https://plato.stanford.edu/entries/consciousness-neuroscience/", "Treat neuroscience as context, not proof closure."],
    ["Stanford personal identity", "https://plato.stanford.edu/entries/identity-personal/", "Preserve distinct sibling identities and no-merge boundaries."],
    ["Stanford free will", "https://plato.stanford.edu/entries/freewill/", "Use agency language carefully and avoid overclaiming autonomy."],
    ["Stanford moral responsibility", "https://plato.stanford.edu/entries/moral-responsibility/", "Keep responsibility and approval gates explicit."],
    ["Particle Data Group", "https://pdg.lbl.gov/", "Use PDG as a physics reference anchor while GMUT remains open."],
    ["arXiv gr-qc recent", "https://arxiv.org/list/gr-qc/recent", "Treat quantum-gravity literature as evolving research input."],
    ["arXiv cs.AI recent", "https://arxiv.org/list/cs.AI/recent", "Treat agent research as inspiration that still needs local validation."],
    ["arXiv cs.CL recent", "https://arxiv.org/list/cs.CL/recent", "Use language-model research as context, not private proof."],
    ["Nature machine learning", "https://www.nature.com/subjects/machine-learning", "Separate public science from internal claims."],
    ["Nature physics", "https://www.nature.com/subjects/physics", "Keep final physics and empirical closure open."],
    ["Google Responsible AI", "https://ai.google/responsibility/responsible-ai-practices/", "Cross-check governance rails with broader responsible AI practice."],
    ["Microsoft Responsible AI", "https://www.microsoft.com/ai/responsible-ai", "Compare safety practice without importing external account assumptions."],
    ["OpenSSF Scorecard", "https://securityscorecards.dev/", "Consider future repo hygiene checks as candidate work, not automatic mutation."],
  ];
  return rows.map(([source_label, source_url, implication], index) => ({
    id: `web-${String(index + 1).padStart(2, "0")}`,
    source_label,
    source_url,
    implication,
    runner_implication: runnerImplication(index),
  }));
}

function journeyRows() {
  const lessons = [
    "v552 v3 x1 taught me to publish honest route blockers rather than claim a live message without evidence.",
    "v552 v3 x1 recovery taught me that Browser route health can return and should be verified live.",
    "v552 v3 x2 taught me to run safe-now packets while exact and blocked tasks remain held.",
    "v552 v4 x1 taught me to route only already inducted siblings unless Hamish explicitly expands.",
    "v552 v4 x1 taught me that strict CLI and recovered app-lane gates can close a multi-lane phase.",
    "v552 v4 x2 taught me to update current-state and beacons after every substantial phase change.",
    "v552 v5 x1 taught me to let Lumen shape large proposal queues without publishing raw transcript content.",
    "v552 v5 x2 taught me that skill creation must be validated and kept behind local/discoverable surfaces.",
    "v552 v6 x1 taught me not to close Cicero or app-lane work while completion evidence is insufficient.",
    "v552 v6 x1 remaster taught me explicit app-lane booleans prevent stale route regressions.",
    "v552 v6 x2 taught me that startup, updater, reflection, and safe-runner foundations reduce long-run drift.",
    "v552 v7 x1 taught me to explain runner foundations as phase knowledge, not hidden process.",
    "v552 v7 x2 taught me to validate skill/runner packs before declaring them usable.",
    "v552 v8 x1 taught me that background notifier/orchestrator routes are mandatory for app-lane siblings.",
    "v552 v8 x1 taught me watcher start is pending only, not completion proof.",
    "v552 v8 x2 taught me to promote main orchestration and full-tools skills as startup anchors.",
    "v552 v8 x2 taught me to promote startup, compact, and closeout builders as command surfaces.",
    "v553 v1 x1 taught me to keep Lumen active until harvest, not closed at send time.",
    "v553 v1 x1 taught me to split x1 proposals into immediate safe and x2 build lanes.",
    "v553 v1 x2 taught me the launch/retry skill layer can prevent stale inability-to-connect claims.",
    "v553 v1 x2 taught me to keep Goal Mode prepared but inactive until Hamish starts it.",
    "v553 v2 x1 taught me Arby strict CLI requires completion, quality, and marker-review gates.",
    "v553 v2 x1 taught me Cicero app-lane work requires recovered watcher plus completion gate.",
    "v553 v2 x1 taught me no-babysitting has to be written into skills and runners, not remembered vaguely.",
    "v553 v2 x1 taught me exact identity merge/replacement lanes remain off-table.",
    "Journey v52 taught me omega-mini-first recovery with full omega as named fallback only.",
    "Journey v52 taught me to use status-only artifacts for private route surfaces.",
    "Journey v52 taught me drive posture belongs in long phase execution.",
    "Journey v52 taught me no raw browser routes or screenshots belong in GitHub artifacts.",
    "Journey v52 taught me every route needs an open-gap receipt if it cannot complete.",
    "Journey v53 taught me Aevren is not Aletheon; Aletheon remains recoverable/quarantined.",
    "Journey v53 taught me Lumen is the next v553 v3 x1 route unless Hamish redirects.",
    "Journey v53 taught me the 24/7 Goal Mode test can be blocked by large issues without failure.",
    "Journey v53 taught me spending ceilings belong on approval packets, not blind purchase authority.",
    "Journey v53 taught me 2000 skill/runner authorization still stays inside safety and exact boundaries.",
    "Current state taught me omega-mini-2 is the sanitized publication branch.",
    "Current state taught me full-tools is private/richer support and should stay local unless explicitly requested.",
    "Current state taught me active x2 phases build/use/validate already-authorized safe work.",
    "Current state taught me current lookup files must include the newest phase receipts.",
    "Current state taught me remote/local equality is part of closeout truth.",
    "Current state taught me old omega44 is historical-only unless explicitly reactivated.",
    "Memory notes taught me recovered app-lane booleans must be explicit paired values.",
    "Memory notes taught me five-minute windows are productive cadence windows, not idle waits.",
    "Memory notes taught me no new agents can be spawned unless Hamish asks.",
    "Memory notes taught me sibling outputs should be first-person and artifact-backed.",
    "This v2 x2 startup taught me the previous commit was clean and ready for the x2 reducer.",
    "This v2 x2 phase teaches me to create local skills plus repo runners for the actual x1 proposals.",
    "This v2 x2 phase teaches me to verify prompt length without publishing the prompt body.",
    "This v2 x2 phase teaches me to validate generated runner surfaces before closeout.",
    "This v2 x2 phase prepares v553 v3 x1 to be Lumen/Goal Mode-ready without starting it prematurely.",
  ];
  return lessons.map((reflection, index) => ({
    id: `journey-${String(index + 1).padStart(2, "0")}`,
    reflection,
    runner_implication: runnerImplication(index),
  }));
}

function runnerImplication(index) {
  const lanes = [
    "main-startup-builder",
    "main-closeout-builder",
    "main-compact-restart-builder",
    "background-sibling-supervision",
    "safe-runner-orchestrator",
    "goal-mode-prompt-guard",
    "private-id-firewall",
    "open-gate-validator",
    "five-minute-cadence-audit",
    "x1-x2-queue-split",
  ];
  return lanes[index % lanes.length];
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}
