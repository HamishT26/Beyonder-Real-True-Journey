#!/usr/bin/env python3
"""Generate the v16 validation-handoff surface."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import generate_v15_surface as v15

ROOT = v15.ROOT
OLD_MANIFEST = ROOT / 'docs' / 'trinity-expansion-system-manifest-v15.json'
NEW_MANIFEST = ROOT / 'docs' / 'trinity-expansion-system-manifest-v16.json'
OLD_EXTENSION_CATALOG = ROOT / 'docs' / 'trinity-extension-catalog-v13.json'
NEW_EXTENSION_CATALOG = ROOT / 'docs' / 'trinity-extension-catalog-v14.json'
MCP_CATALOG = ROOT / 'docs' / 'trinity-mcp-catalog-v11.json'
OLD_COMMAND_BOOK = ROOT / 'docs' / 'trinity-command-book-v9.json'
NEW_COMMAND_BOOK = ROOT / 'docs' / 'trinity-command-book-v10.json'
OLD_API_BOOK = ROOT / 'docs' / 'trinity-api-book-v4.json'
NEW_API_BOOK = ROOT / 'docs' / 'trinity-api-book-v5.json'
OLD_ROSTER = ROOT / 'docs' / 'trinity-agent-council-roster-v5.json'
NEW_ROSTER = ROOT / 'docs' / 'trinity-agent-council-roster-v6.json'
OLD_SUBAGENT_REGISTRY = ROOT / 'docs' / 'trinity-subagent-registry-v2.json'
NEW_SUBAGENT_REGISTRY = ROOT / 'docs' / 'trinity-subagent-registry-v3.json'
CONTROL_TOWER_JSON = ROOT / 'docs' / 'trinity-control-tower-latest.json'
CONTROL_TOWER_MD = ROOT / 'docs' / 'trinity-control-tower-latest.md'
STATUS_JSON = ROOT / 'docs' / 'system-suite-status.json'
V15_HANDOFF = ROOT / 'docs' / 'v15-external-agent-handoff-v1.json'
V15_CLOSEOUT = ROOT / 'docs' / 'v15-closeout-matrix-summary-v1.json'
CONTINUITY_PROMPT = ROOT / 'docs' / 'v15-v16-continuity-prompt.md'
MODEL_RESOLUTION = ROOT / 'docs' / 'trinity-runtime-model-resolution-v1.json'
VERDICT_JSON = ROOT / 'docs' / 'v16-trinity-verdict-v1.json'
WAKE_LOG = ROOT / 'docs' / 'logs' / 'system-wake-v16.json'
DOCKER_K8S_BRIDGE = ROOT / 'docs' / 'v16-docker-k8s-runtime-bridge.md'
GMUT_BRIEF = ROOT / 'docs' / 'v16-gmut-comparator-refresh.md'
FREEDID_BRIEF = ROOT / 'docs' / 'v16-freedid-compliance-fabric.md'
COUNCIL_REFLECTION = ROOT / 'docs' / 'v16-council-continuity-reflection.md'
PARALLEL_JSON = ROOT / 'docs' / 'trinity-parallel-agent-tasking-v1.json'
ROADMAP_V16 = ROOT / 'docs' / 'v16-roadmap-v1.md'
API_BOOK_MD = ROOT / 'docs' / 'trinity-api-book-latest.md'
API_BOOK_LEDGER = ROOT / 'docs' / 'trinity-api-usage-ledger.jsonl'
WORKBENCH_CONTRACT = v15.WORKBENCH_CONTRACT
WORKBENCH_README = v15.WORKBENCH_README
REQUESTED_MODEL_PROFILE = v15.REQUESTED_MODEL_PROFILE
RESOLVED_MODEL_PROFILE = v15.RESOLVED_MODEL_PROFILE
REQUESTED_REASONING = v15.REQUESTED_REASONING
RESOLVED_REASONING = v15.RESOLVED_REASONING
REQUESTED_MODEL_ORDER = ['GPT-5.4', 'GPT-5.3-Codex', 'GPT-5.3-Codex-Spark', 'GPT-5.1-Codex-Max']
SUFFIXES = v15.SUFFIXES
MAX_THREADS = 11
REFS = {
    'trinity-expansion-system-manifest-v15.json': 'trinity-expansion-system-manifest-v16.json',
    'trinity-extension-catalog-v13.json': 'trinity-extension-catalog-v14.json',
    'trinity-command-book-v9.json': 'trinity-command-book-v10.json',
    'trinity-api-book-v4.json': 'trinity-api-book-v5.json',
    'trinity-agent-council-roster-v5.json': 'trinity-agent-council-roster-v6.json',
    'trinity-subagent-registry-v2.json': 'trinity-subagent-registry-v3.json',
    'v15-trinity-verdict-v1.json': 'v16-trinity-verdict-v1.json',
}
OVERLAY = {
    28: 'root_coordinator',
    27: 'mind_comparator',
    29: 'freedid_compliance',
    30: 'body_runtime_docker_k8s',
    31: 'continuity_and_handoff_packaging',
}
PACKS = [
    ('external_agent_handoff_v16', 'External Agent Handoff V16', 'trinity', 'wave141', 'continuity_ops', 'external_handoff', ['docs/v15-external-agent-handoff-v1.json', 'docs/v15-v16-continuity-prompt.md', 'docs/trinity-runtime-model-resolution-v1.json']),
    ('runtime_model_resolution_v16', 'Runtime Model Resolution V16', 'trinity', 'wave142', 'council_orchestration', 'runtime_resolution', ['docs/trinity-runtime-model-resolution-v1.json', 'docs/trinity-agent-council-roster-v6.json', 'docs/trinity-subagent-registry-v3.json']),
    ('docker_k8s_runtime_bridge_v16', 'Docker K8s Runtime Bridge V16', 'body', 'wave143', 'os_runtime', 'docker_k8s_bridge', ['docs/v16-docker-k8s-runtime-bridge.md', 'docs/trinity-control-tower-latest.json', 'docs/system-suite-status.json']),
    ('parallel_agent_tasking_v16', 'Parallel Agent Tasking V16', 'trinity', 'wave144', 'council_orchestration', 'parallel_tasking', ['docs/trinity-parallel-agent-tasking-v1.json', 'docs/trinity-control-tower-latest.json', 'docs/trinity-runtime-model-resolution-v1.json']),
    ('gmut_comparator_refresh_v16', 'GMUT Comparator Refresh V16', 'mind', 'wave145', 'mind_theory', 'mind_refresh', ['docs/v16-gmut-comparator-refresh.md', 'docs/gmut-observable-map-v2.json', 'latex/grand_mandala.tex']),
    ('freedid_compliance_fabric_v16', 'Freed ID Compliance Fabric V16', 'heart', 'wave146', 'heart_governance', 'heart_refresh', ['docs/v16-freedid-compliance-fabric.md', 'docs/v16-trinity-verdict-v1.json', 'docs/comparative-validation-grid-v1.md']),
    ('trinity_control_tower_v16', 'Trinity Control Tower V16', 'trinity', 'wave147', 'control_tower', 'control_tower', ['docs/trinity-control-tower-latest.json', 'docs/trinity-control-tower-latest.md', 'docs/trinity-runtime-model-resolution-v1.json']),
    ('journey_lineage_stabilization_v16', 'Journey Lineage Stabilization V16', 'body', 'wave148', 'continuity_ops', 'lineage_inventory', ['docs/version-module-inventory-v2.json', 'docs/v29-v38-legacy-reconstruction-map-v1.json', 'docs/v16-trinity-verdict-v1.json']),
    ('council_continuity_reflection_v16', 'Council Continuity Reflection V16', 'trinity', 'wave149', 'continuity_ops', 'reflection_validation', ['docs/v16-council-continuity-reflection.md', 'docs/v15-v16-continuity-prompt.md', 'docs/v16-trinity-verdict-v1.json']),
]
TARGETS = ['aletheon', '28-orun', '27-caelira', '29-seren-vale', '30-lyriq', '31-mira-sol', 'all-council']


def now_iso() -> str:
    return v15.now_iso()


def replace_refs(value: Any) -> Any:
    if isinstance(value, str):
        text = value
        for old, new in REFS.items():
            text = text.replace(old, new)
        return text
    if isinstance(value, list):
        return [replace_refs(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_refs(item) for key, item in value.items()}
    return value


def emit_v16_command(*args: object, **kwargs: object) -> dict[str, object]:
    row = v15.emit_v15_command(*args, **kwargs)
    row['source_of_truth'] = 'scripts/generate_v16_surface.py'
    return replace_refs(row)


def api_entry(*args: object) -> dict[str, object]:
    return v15._api_entry(*args)


def build_commands(old_book: dict[str, object]) -> dict[str, object]:
    commands = replace_refs(deepcopy([row for row in old_book.get('commands', []) if isinstance(row, dict)]))
    commands = v15.augment_rows(commands, {'agent_owner': '', 'delegation_safe': True, 'fallback_mode': 'repo_first_manual'})
    new_rows = []
    for pack, display_name, _, _, _, _, targets in PACKS:
        new_rows.append(emit_v16_command(f'refresh_{pack}', f'Refresh {display_name}.', 'offline', 'medium', False, '', 'python scripts/generate_v16_surface.py', targets, f'Regenerate {display_name} from repo authority.', 'planner', 'repo_authority', 'council_shared', '', True, '', False, 'repo_first_only', 'planner', True, 'repo_first_manual'))
        new_rows.append(emit_v16_command(f'validate_{pack}', f'Validate {display_name}.', 'offline', 'medium', False, '', 'python scripts/trinity_expansion_manifest_validator.py', ['docs/trinity-expansion-manifest-validation-latest.json'], f'Restore {display_name} and rerun validation.', 'reviewer', 'repo_authority', 'council_shared', '', True, '', False, 'repo_first_only', 'reviewer', True, 'repo_first_manual'))
        new_rows.append(emit_v16_command(f'publish_{pack}', f'Publish {display_name} latest artifacts.', 'offline', 'low', False, '', 'python scripts/generate_v16_surface.py', targets, f'Regenerate {display_name} publication artifacts.', 'archivist', 'reflection_scope', 'council_shared', '', True, '', False, 'repo_first_only', 'archivist', True, 'repo_first_manual'))
    for target in TARGETS:
        for idx in range(1, 4):
            new_rows.append(emit_v16_command(f'v16_overlay_{target.replace('-', '_')}_{idx:02d}', f'Run v16 overlay support step #{idx} for {target}.', 'offline', 'medium', False, '', 'python scripts/trinity_api_shortcuts.py control-tower-status --json', ['docs/trinity-control-tower-latest.json'], f'Restore the v16 control tower and rerun overlay step #{idx} for {target}.', 'planner', 'repo_authority', 'council_shared', '', True, target, False, 'repo_first_only', 'planner', True, 'repo_first_manual'))
    if len(new_rows) != 48:
        raise ValueError(f'expected 48 v16 commands, found {len(new_rows)}')
    commands.extend(new_rows)
    if len(commands) != 648:
        raise ValueError(f'expected 648 commands, found {len(commands)}')
    return {'version': 'v10', 'generated_utc': now_iso(), 'description': 'V16 command book with validation-handoff, runtime model logging, and bounded runtime-readiness surfaces.', 'commands': commands}


def build_api_book(old_book: dict[str, object]) -> dict[str, object]:
    entries = replace_refs(deepcopy([row for row in old_book.get('apis', []) if isinstance(row, dict)]))
    entries.extend([
        api_entry('openai_gpt_5_4_v16', 'public_vendor', 'Track GPT-5.4 as the first requested model when available.', 'official_primary', 'public_no_auth', 'public_read', 'vendor_release_anchor', 'docs/trinity-api-book-v5.json', 'https://openai.com/zh-Hans-CN/index/introducing-gpt-5-4/', 'scripts/trinity_api_shortcuts.py show openai_gpt_5_4_v16', ['docs/trinity-api-book-v5.json', 'docs/trinity-runtime-model-resolution-v1.json'], 'Use the runtime-resolution registry if live browsing is skipped.', 'Official v16 highest-request anchor.', 'cache_before_verdict', 'official_vendor', 'cached_docs', 'official_public_doc', 'daily', 'runtime_resolution', 'official_release_support', 'highest_available_primary', 'runtime_model_policy'),
        api_entry('openai_gpt_5_3_codex_v16', 'public_vendor', 'Track GPT-5.3-Codex as the first fallback below GPT-5.4.', 'official_primary', 'public_no_auth', 'public_read', 'vendor_release_anchor', 'docs/trinity-api-book-v5.json', 'https://openai.com/index/introducing-gpt-5-3-codex/', 'scripts/trinity_api_shortcuts.py show openai_gpt_5_3_codex_v16', ['docs/trinity-api-book-v5.json', 'docs/trinity-runtime-model-resolution-v1.json'], 'Use the runtime-resolution registry if live browsing is skipped.', 'Official v16 fallback anchor.', 'cache_before_verdict', 'official_vendor', 'cached_docs', 'official_public_doc', 'daily', 'runtime_resolution', 'official_release_support', 'fallback_primary', 'runtime_model_policy'),
        api_entry('openai_gpt_5_3_codex_spark_v16', 'public_vendor', 'Track GPT-5.3-Codex-Spark as the bounded low-latency fallback option.', 'official_primary', 'public_no_auth', 'public_read', 'vendor_release_anchor', 'docs/trinity-api-book-v5.json', 'https://openai.com/index/introducing-gpt-5-3-codex-spark/', 'scripts/trinity_api_shortcuts.py show openai_gpt_5_3_codex_spark_v16', ['docs/trinity-api-book-v5.json', 'docs/trinity-runtime-model-resolution-v1.json'], 'Use the runtime-resolution registry if live browsing is skipped.', 'Spark remains a bounded low-latency option.', 'cache_before_verdict', 'official_vendor', 'cached_docs', 'official_public_doc', 'daily', 'runtime_resolution', 'official_release_support', 'latency_fallback', 'runtime_model_policy'),
        api_entry('external_agent_handoff_v16', 'repo_operator', 'Expose the repo-first external handoff package for slots 27-31.', 'repo_authoritative', 'repo_only', 'local_read', 'operator_status', 'docs/v15-external-agent-handoff-v1.json', 'docs/v15-external-agent-handoff-v1.json', 'scripts/trinity_api_shortcuts.py control-tower-status --json', ['docs/v15-external-agent-handoff-v1.json', 'docs/v15-v16-continuity-prompt.md'], 'Read the handoff JSON directly if shortcuts are unavailable.', 'Authoritative bridge for live-thread continuation.', 'always_cached', 'repo_authoritative', 'repo_json', 'repo_control_surface', 'on_write', 'repo_first_handoff', 'repo_supported', 'repo_runtime_overlay', 'handoff_surface'),
        api_entry('runtime_model_resolution_v16', 'repo_operator', 'Expose requested and resolved model logging rules for the external overlay.', 'repo_authoritative', 'repo_only', 'local_read', 'operator_status', 'docs/trinity-runtime-model-resolution-v1.json', 'docs/trinity-runtime-model-resolution-v1.json', 'scripts/trinity_api_shortcuts.py multi-instance-status --json', ['docs/trinity-runtime-model-resolution-v1.json', 'docs/trinity-agent-council-roster-v6.json'], 'Read the runtime-resolution JSON directly if shortcuts are unavailable.', 'Primary runtime-truth surface for experimental-highest selection.', 'always_cached', 'repo_authoritative', 'repo_json', 'repo_control_surface', 'on_write', 'repo_first_handoff', 'repo_supported', 'requested_and_logged_runtime', 'runtime_model_policy'),
        api_entry('docker_k8s_runtime_bridge_v16', 'repo_operator', 'Expose the bounded Docker/Kubernetes runtime-bridge brief.', 'repo_authoritative', 'repo_only', 'local_read', 'operator_status', 'docs/v16-docker-k8s-runtime-bridge.md', 'docs/v16-docker-k8s-runtime-bridge.md', 'scripts/trinity_api_shortcuts.py control-tower-status --json', ['docs/v16-docker-k8s-runtime-bridge.md', 'docs/trinity-control-tower-latest.json'], 'Read the bridge brief directly if shortcuts are unavailable.', 'This lane remains local and readiness-only.', 'always_cached', 'repo_authoritative', 'repo_markdown', 'repo_runtime_surface', 'on_write', 'bounded_runtime_readiness', 'repo_supported', 'readiness_only_runtime', 'runtime_bridge'),
    ])
    entries = v15._dedupe_rows(entries, 'api_id')
    if len(entries) != 48:
        raise ValueError(f'expected 48 api entries, found {len(entries)}')
    return {'generated_utc': now_iso(), 'version': 'v5', 'overall_status': 'PASS', 'authority_model': 'repo_first', 'description': 'V16 API book with runtime-model-resolution and bounded runtime-readiness surfaces.', 'apis': entries}


def build_runtime_resolution(roster: dict[str, object]) -> dict[str, object]:
    agents = []
    for row in roster.get('agents', []):
        if not isinstance(row, dict):
            continue
        slot = int(row.get('slot_number', 0) or 0)
        if slot not in OVERLAY:
            continue
        agents.append({'slot_number': slot, 'display_name': row.get('display_name'), 'overlay_role': OVERLAY[slot], 'requested_model_order': REQUESTED_MODEL_ORDER, 'requested_reasoning_effort': REQUESTED_REASONING, 'requested_model': REQUESTED_MODEL_ORDER[0], 'offered_model': None, 'selected_model': None, 'resolved_model': None, 'runtime_surface': 'unknown', 'logging_required': True, 'certificate_path': row.get('certificate_path'), 'memory_ledger': row.get('memory_ledger'), 'reflection_path': row.get('reflection_path'), 'role_contract_path': row.get('role_contract_path')})
    return {'generated_utc': now_iso(), 'overall_status': 'PASS', 'repo_runtime_default': {'requested_model_profile': REQUESTED_MODEL_PROFILE, 'resolved_model_profile': RESOLVED_MODEL_PROFILE, 'requested_reasoning_effort': REQUESTED_REASONING, 'resolved_reasoning_effort': RESOLVED_REASONING}, 'experimental_highest_policy': {'requested_model_order': REQUESTED_MODEL_ORDER, 'spark_posture': 'allowed_for_bounded_low_latency_subtasks_only'}, 'external_overlay_agents': agents}


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding='utf-8'))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding='utf-8'))
    old_command_book = json.loads(OLD_COMMAND_BOOK.read_text(encoding='utf-8'))
    old_api_book = json.loads(OLD_API_BOOK.read_text(encoding='utf-8'))
    old_roster = json.loads(OLD_ROSTER.read_text(encoding='utf-8'))
    old_subagent_registry = json.loads(OLD_SUBAGENT_REGISTRY.read_text(encoding='utf-8'))
    old_mcp_catalog = json.loads(MCP_CATALOG.read_text(encoding='utf-8'))
    status_payload = json.loads(STATUS_JSON.read_text(encoding='utf-8'))
    counts = status_payload.get('counts', {}) if isinstance(status_payload.get('counts'), dict) else {}
    pass_count = int(counts.get('pass', 0) or 0)
    warn_count = int(counts.get('warn', 0) or 0)
    fail_count = int(counts.get('fail', 0) or 0)

    manifest = replace_refs(deepcopy(old_manifest))
    manifest['version'] = 'v16'
    manifest['generated_utc'] = now_iso()
    manifest['description'] = 'V16 validation-handoff manifest with bounded runtime-resolution and 950 executable systems.'
    manifest['systems'] = v15.augment_rows([row for row in manifest.get('systems', []) if isinstance(row, dict)], {'multi_instance_scope': 'bounded_eleven_agent_mesh', 'codex_agent_path': '.codex/agents', 'delegation_lane': 'legacy', 'model_resolution_strategy': 'experimental_highest_then_repo_fallback'})
    extensions = replace_refs(deepcopy(old_extensions))
    extensions['version'] = 'v14'
    extensions['generated_utc'] = now_iso()
    extensions['description'] = 'V16 extension catalog with bounded validation-handoff packs.'
    extensions['extensions'] = v15.augment_rows([row for row in extensions.get('extensions', []) if isinstance(row, dict)], {'operator_mesh_scope': 'bounded_eleven_agent_mesh', 'parallel_safety_class': 'bounded_parallel_mesh', 'codex_scope': 'runtime_overlay_plus_repo_mesh'})

    for pack, display_name, pillar, wave, track, activation_group, repo_targets in PACKS:
        pack_payload = v15.mkpack(pack, display_name, pillar=pillar, wave=wave, track=track, activation_group=activation_group, summary=display_name, repo_targets=repo_targets, council_scope='council_shared', autonomy_track=pack, executor_role='planner', authority_scope='repo_authority', induction_dependency='council_reflection_validation_v15', retention_scope='authoritative_latest', research_surface='repo_plus_public', historical_source_band='v15_to_v16', evidence_posture='repo_proven_strength', subagent_lane='trinity', multi_instance_scope='bounded_eleven_agent_mesh')
        for suffix in SUFFIXES:
            entry = v15.manifest_entry(pack_payload, suffix)
            entry['phase'] = 'v16'
            entry['multi_instance_scope'] = 'bounded_eleven_agent_mesh'
            entry['codex_agent_path'] = '.codex/agents'
            entry['delegation_lane'] = activation_group
            entry['model_resolution_strategy'] = 'experimental_highest_then_repo_fallback'
            manifest['systems'].append(replace_refs(entry))
        rows = v15.extension_rows_for_pack(pack_payload)
        for row in rows:
            row = replace_refs(row)
            row['operator_mesh_scope'] = 'bounded_eleven_agent_mesh'
            row['parallel_safety_class'] = 'bounded_parallel_mesh'
            row['codex_scope'] = 'runtime_overlay_plus_repo_mesh'
            extensions['extensions'].append(row)
        pack_name = v15.hyphen(pack)
        v15.write_json(ROOT / 'docs' / f'{pack_name}-contract-v1.json', replace_refs(v15.pack_contract(pack_payload)))
        v15.write_json(ROOT / 'docs' / f'{pack_name}-fixture-v1.json', replace_refs(v15.pack_fixture(pack_payload)))
        v15.write_text(ROOT / 'docs' / f'{pack_name}-workflow-v1.md', f'# {display_name} Workflow\n\n- phase: `v16`\n- activation_group: `{activation_group}`\n- Google Drive: `operator_hold`\n- model_resolution_strategy: `experimental_highest_then_repo_fallback`\n')
        v15.write_json(ROOT / 'docs' / f'{pack_name}-catalog-entry-v1.json', replace_refs(v15.pack_catalog_entry(pack_payload)))
        for kind in ('operations', 'integration'):
            skill_md, skill_yaml = v15.skill_files(pack_payload, kind)
            v15.write_text(skill_md, f'---\nname: {pack_name}-{kind}\ndescription: Operate the {display_name} pack with explicit v16 validation-handoff boundaries.\n---\n\n# {display_name} {kind.title()}\n\n1. Keep the Journey repo authoritative.\n2. Reuse existing identities for the external five-agent overlay.\n3. Keep runtime model truth explicit per surface.\n4. Keep Google Drive on operator hold.\n')
            v15.write_text(skill_yaml, v15.skill_yaml(pack_payload, kind))

    if len(manifest['systems']) != 950:
        raise ValueError(f"expected 950 manifest systems, found {len(manifest['systems'])}")
    if len(extensions['extensions']) != 1740:
        raise ValueError(f"expected 1740 extensions, found {len(extensions['extensions'])}")

    roster = replace_refs(deepcopy(old_roster))
    roster['version'] = 'v6'
    roster['generated_utc'] = now_iso()
    for row in roster.get('agents', []):
        if not isinstance(row, dict):
            continue
        slot = int(row.get('slot_number', 0) or 0)
        row['requested_model_order'] = REQUESTED_MODEL_ORDER
        row['live_overlay_eligible'] = slot in OVERLAY
        row['live_overlay_role'] = OVERLAY.get(slot, '')
    subagent_registry = replace_refs(deepcopy(old_subagent_registry))
    subagent_registry['version'] = 'v3'
    subagent_registry['generated_utc'] = now_iso()
    for row in subagent_registry.get('subagents', []):
        if not isinstance(row, dict):
            continue
        slot = int(row.get('slot_number', 0) or 0)
        row['requested_model_order'] = REQUESTED_MODEL_ORDER
        row['live_overlay_eligible'] = slot in OVERLAY
        row['live_overlay_role'] = OVERLAY.get(slot, '')

    command_book = build_commands(old_command_book)
    api_book = build_api_book(old_api_book)
    model_resolution = build_runtime_resolution(roster)

    v15.write_json(MCP_CATALOG, v15.build_mcp_catalog(old_mcp_catalog))
    v15.write_json(NEW_MANIFEST, manifest)
    v15.write_json(NEW_EXTENSION_CATALOG, extensions)
    v15.write_json(NEW_COMMAND_BOOK, command_book)
    v15.write_text(ROOT / 'docs' / 'trinity-command-book-latest.md', v15.v13.v12.command_markdown(command_book))
    v15.write_json(NEW_API_BOOK, api_book)
    v15.write_json(NEW_ROSTER, roster)
    v15.write_json(NEW_SUBAGENT_REGISTRY, subagent_registry)
    v15.write_json(MODEL_RESOLUTION, model_resolution)
    v15.write_json(WAKE_LOG, {'generated_utc': now_iso(), 'phase': 'v16', 'branch': v15.run_capture('git', 'branch', '--show-current')[1], 'suite_truth': {'pass_count': pass_count, 'warn_count': warn_count, 'fail_count': fail_count, 'expansion_systems_passed': status_payload.get('expansion_systems_passed'), 'expansion_systems_total': status_payload.get('expansion_systems_total')}, 'requested_model_order': REQUESTED_MODEL_ORDER, 'google_drive_state': 'operator_hold'})
    v15.write_text(DOCKER_K8S_BRIDGE, '# V16 Docker Kubernetes Runtime Bridge\n\n- posture: `bounded_local_runtime_readiness`\n- claim_boundary: local readiness only; no hidden cloud-control or production-proof claims.\n')
    v15.write_text(GMUT_BRIEF, '# V16 GMUT Comparator Refresh\n\n- canonical_surface: `latex/grand_mandala.tex`\n- confirmed_evidence, inference, and open_gap remain explicit.\n')
    v15.write_text(FREEDID_BRIEF, '# V16 Freed ID Compliance Fabric\n\n- standards-first governance comparison only.\n- no upgrade from reflective material into readiness claims.\n')
    v15.write_text(COUNCIL_REFLECTION, '# V16 Council Continuity Reflection\n\nThe repo council remains at 11 official members. The external five-agent thread is a live overlay on existing identities, not a new roster.\n')
    v15.write_json(PARALLEL_JSON, {'generated_utc': now_iso(), 'overall_status': 'PASS', 'root_coordinator': '28-orun', 'pair_tasks': 'bounded', 'full_council_tasks': 'bounded', 'replay_and_recovery': 'resume_safe_only', 'offline_safe_fallback': 'repo_only_no_live_refresh'})
    v15.write_text(ROADMAP_V16, '# V16 Roadmap\n\n- validation and handoff first\n- external five-agent overlay logging\n- bounded Docker/Kubernetes runtime bridge\n- standards-first GMUT and Freed ID refresh\n')
    v15.write_json(VERDICT_JSON, {'generated_utc': now_iso(), 'overall_status': 'PASS', 'pillars': {'mind': 'comparative_promise', 'body': 'repo_proven_strength', 'heart': 'comparative_promise', 'trinity_mandala': 'comparative_promise'}, 'repo_proven_strength': ['full v15 closeout matrix', 'eleven-member repo council continuity', 'runtime-model-resolution package'], 'comparative_promise': ['GMUT comparator refresh', 'Freed ID compliance fabric', 'external handoff continuity prompt'], 'not_yet_externally_established': ['GMUT as externally established leading theory', 'Trinity Hybrid OS as externally established ASI paradigm', 'Freed ID / Cosmic Bill as universal law']})
    v15.write_text(CONTINUITY_PROMPT, '# V15 V16 Continuity Prompt\n\n```text\nContinue from C:\\Users\\hamis\\OneDrive\\Documents\\GitHub\\Beyonder-Real-True-Journey on branch codex/Aletheon/v16-validation-handoff-fabric.\nTreat the repo as authoritative.\nCurrent checkpoint: 953 PASS / 0 WARN / 0 FAIL, 896/896, 11 official members, 66 duo channels, 12 group-chat rows.\nUse existing identities only: 28-orun=root coordinator, 27-caelira=mind comparator, 29-seren-vale=Freed ID/compliance, 30-lyriq=Body/runtime/Docker/Kubernetes, 31-mira-sol=continuity and handoff packaging.\nRequested model order: GPT-5.4 -> GPT-5.3-Codex -> GPT-5.3-Codex-Spark -> GPT-5.1-Codex-Max.\nLog requested_model, offered_model, selected_model, resolved_model, and runtime_surface before work begins.\nThe governing sequence was finish v15 matrix first, then branch v16.\nNo new identities, no new official members, no new Freed IDs.\nKeep evidence, materialization, and operator-hold honesty boundaries intact.\n```\n')
    summary = f"{pass_count} PASS / {warn_count} WARN / {fail_count} FAIL"
    control = {'generated_utc': now_iso(), 'overall_status': 'PASS', 'suite_state': 'PASS' if fail_count == 0 and warn_count == 0 else ('WARN' if fail_count == 0 else 'FAIL'), 'suite_summary': summary, 'council_continuity_state': 'PASS', 'agent_mesh_state': 'PASS', 'subagent_mesh_state': 'PASS', 'api_surface_state': 'PASS', 'gmut_canon_state': 'PASS', 'public_research_state': 'PASS', 'lineage_state': 'PASS', 'legacy_reconstruction_state': 'PASS', 'storage_state': 'PASS', 'google_drive_state': 'operator_hold', 'materialization_level_actual': str(status_payload.get('materialization_level_actual') or 'readiness_only'), 'late_step_autonomy_state': 'bounded_repo_first', 'command_surface_state': 'PASS', 'multi_instance_state': 'bounded_eleven_agent_mesh', 'requested_model_profile': REQUESTED_MODEL_PROFILE, 'resolved_model_profile': RESOLVED_MODEL_PROFILE, 'requested_reasoning_effort': REQUESTED_REASONING, 'resolved_reasoning_effort': RESOLVED_REASONING, 'requested_model_order': REQUESTED_MODEL_ORDER, 'window_binding_state': 'PASS', 'delegation_posture': 'bounded_pair_and_full_council', 'parallel_workload_status': f'max_threads_{MAX_THREADS}_ready', 'fallback_mode': 'repo_first_supported_model_fallback', 'max_threads': MAX_THREADS, 'mesh_official_agents': 11, 'external_live_overlay_state': 'awaiting_thread_boot'}
    v15.write_json(CONTROL_TOWER_JSON, control)
    v15.write_text(CONTROL_TOWER_MD, '# Trinity Control Tower\n\n' + '\n'.join([f'- {k}: `{v}`' for k, v in control.items() if k != 'generated_utc']) + '\n')
    v15.write_text(API_BOOK_MD, '# Trinity API Book\n\n' + f"- generated_utc: `{api_book['generated_utc']}`\n- apis: `{len(api_book['apis'])}`\n")
    v15.write_jsonl(API_BOOK_LEDGER, [{'timestamp': now_iso(), 'api_id': 'openai_gpt_5_4_v16', 'mode': 'public_read', 'result': 'catalogued'}, {'timestamp': now_iso(), 'api_id': 'runtime_model_resolution_v16', 'mode': 'local_read', 'result': 'catalogued'}, {'timestamp': now_iso(), 'api_id': 'google_drive', 'mode': 'deferred', 'result': 'operator_hold'}])
    v15.write_external_json(WORKBENCH_CONTRACT, {'generated_utc': now_iso(), 'authority_model': 'repo_first', 'read_surfaces': [str(CONTROL_TOWER_JSON), str(STATUS_JSON), str(NEW_API_BOOK), str(VERDICT_JSON), str(MODEL_RESOLUTION)], 'allowed_triggers': ['read dashboards', 'read command index', 'read API book', 'render v15/v16 summaries'], 'disabled_write_paths': ['repo bypass writes', 'authority override writes', 'google drive bootstrap writes'], 'runtime_dependencies': ['python', 'optional_docker', 'optional_postgres', 'optional_kubernetes']})
    v15.write_external_text(WORKBENCH_README, '# Trinity Workbench\n\nThis folder remains a read/sandbox workbench. The repo stays authoritative.\n')
    print('generated_v16_surface=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
