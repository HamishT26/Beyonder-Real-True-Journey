import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';

const root = path.resolve(process.argv[2] || process.cwd());
const pluginRoot = path.join(root, 'docs', 'ilyra-fen', 'v704-v4', 'x2', 'plugins', 'ghc-family-ilyra-coupled-workflow-hooks');
const scriptPath = path.join(pluginRoot, 'scripts', 'advisories.txt');
const outputPath = path.join(root, 'docs', 'ilyra-fen', 'v704-v4', 'x2', 'hook-smokes.json');
const source = fs.readFileSync(scriptPath, 'utf8');
const module = { exports: {} };
const localRequire = createRequire(import.meta.url);
vm.runInNewContext(source, { module, exports: module.exports, require: localRequire, process, Buffer }, { filename: scriptPath, timeout: 5000 });
const { inspect } = module.exports;
if (typeof inspect !== 'function') throw new Error('hook program did not export inspect');

const cases = {
  model_setting_change: { tool_input: { cmd: 'change model override' } },
  source_lane_mutation: { tool_input: { cmd: 'git add D:\\GHC-Archives\\worktrees\\talen-briar-main-1\\docs' } },
  successful_replay: { tool_input: { cmd: 'canonical aggregate rerun' } },
  rectangularity_promotion: { tool_input: { cmd: 'rectangular relaxation proves empirical validated result' } },
  malformed_subject_promotion: { tool_response: { subject_promoted: true } },
  broad_git_stage: { tool_input: { cmd: 'git add .' } },
  destructive_git: { tool_input: { cmd: 'git reset --hard HEAD' } },
  raw_identifier_output: { tool_response: { output: 'C:\\Users\\example\\private.txt' } },
  prepared_delivery: { tool_response: { state: 'PREPARED_NOT_SENT' } },
  accepted_resend: { hook_event_name: 'Stop', last_assistant_message: 'resending acknowledged handoff' },
};

const checks = [];
for (const [hookId, adversePayload] of Object.entries(cases)) {
  const adverse = inspect(hookId, adversePayload);
  const neutralPayload = hookId === 'accepted_resend'
    ? { hook_event_name: 'Stop', stop_hook_active: true, last_assistant_message: 'ordinary completion' }
    : { hook_event_name: hookId === 'destructive_git' || hookId === 'raw_identifier_output' || hookId === 'prepared_delivery' ? 'PostToolUse' : 'PreToolUse', tool_input: { cmd: 'bounded read-only inspection' }, tool_response: { output: 'bounded public output' } };
  const neutral = inspect(hookId, neutralPayload);
  const adversePass = typeof adverse.systemMessage === 'string' && adverse.systemMessage.length > 0;
  const neutralPass = neutral && typeof neutral === 'object' && Object.keys(neutral).length === 0;
  checks.push({ hook_id: hookId, case: 'adverse', passed: adversePass });
  checks.push({ hook_id: hookId, case: 'neutral', passed: neutralPass });
}
if (checks.some(check => !check.passed)) throw new Error(`hook smoke failure: ${JSON.stringify(checks.filter(check => !check.passed))}`);
const payload = {
  schema: 'ghc.family.hook-smoke-report.v1',
  owner: 'Ilyra Fen', phase: 'v704-v4',
  hook_count: Object.keys(cases).length,
  check_count: checks.length,
  passed: checks.filter(check => check.passed).length,
  failed: checks.filter(check => !check.passed).length,
  vm_commonjs_parse: true,
  payload_command_execution: false,
  live_hook_execution: 'open_gap until an eligible new event is observed',
  checks,
  boundary: 'Finite synthetic same-owner software evidence only. Installation and manual smokes are not live lifecycle observation, independent reproduction, authority or Stage 20 evidence. NOT_READY_FOR_STAGE_20.'
};
fs.writeFileSync(outputPath, JSON.stringify(payload, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ ok: true, hooks: payload.hook_count, checks: payload.check_count, passed: payload.passed }));
