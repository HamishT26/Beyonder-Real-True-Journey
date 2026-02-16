# Trinity System Suite Run Report

Generated: 2026-02-16T10:32:58.113863+00:00
Step timeout (s): disabled
Profile: quick
Profile source: --profile
Include version scan: False
Include skill install: False
Include curated skill catalog: False
Soft-fail network: False
Fail on warn: False
Achievement target steps: disabled
Quick mode: True
Body benchmark mode: enforce
Status JSON path: docs/system-suite-status.json

This report runs currently available repo systems and records command outputs.

## memory integrity check (strict)
- status: **PASS**
- command: `python3 scripts/aurelis_memory_integrity_check.py --strict`
- started: `2026-02-16T10:32:58.113931+00:00`
- finished: `2026-02-16T10:32:58.137089+00:00`
- duration_sec: `0.023`
```text
Wrote /workspace/docs/aurelis-memory-integrity-report.md
```

## continuity cycle tick (dry-run status)
- status: **PASS**
- command: `python3 scripts/aurelis_cycle_tick.py --user-message 'suite quick dry-run' --assistant-reflection 'Quick mode continuity health check' --progress-snapshot 'Validated quick dry-run status reporting in suite' --next-step 'Run full suite when deeper validation is needed' --query cycle --query-limit 2 --dry-run --no-report --step-timeout-sec 0 --json-status docs/aurelis-cycle-tick-status.json`
- started: `2026-02-16T10:32:58.137115+00:00`
- finished: `2026-02-16T10:32:58.166414+00:00`
- duration_sec: `0.029`
```text
$ python3 scripts/aurelis_memory_update.py --user-message 'suite quick dry-run' --assistant-reflection 'Quick mode continuity health check' --progress-snapshot 'Validated quick dry-run status reporting in suite' --next-step 'Run full suite when deeper validation is needed'
[dry-run] command not executed
$ python3 scripts/aurelis_memory_summary.py --take 5
[dry-run] command not executed
$ python3 scripts/aurelis_next_steps_snapshot.py
[dry-run] command not executed
$ python3 scripts/aurelis_memory_integrity_check.py --strict
[dry-run] command not executed
$ python3 scripts/aurelis_memory_query.py --contains cycle --limit 2
[dry-run] command not executed

Wrote cycle tick json status: docs/aurelis-cycle-tick-status.json
```

## qcit coordination engine
- status: **PASS**
- command: `python3 scripts/qcit_coordination_engine.py --out docs/qcit-coordination-report.json`
- started: `2026-02-16T10:32:58.166451+00:00`
- finished: `2026-02-16T10:32:58.199234+00:00`
- duration_sec: `0.033`
```text
Wrote docs/qcit-coordination-report.json
```

## quantum energy transmutation engine
- status: **PASS**
- command: `python3 scripts/quantum_energy_transmutation_engine.py --out docs/quantum-energy-transmutation-report.json`
- started: `2026-02-16T10:32:58.199261+00:00`
- finished: `2026-02-16T10:32:58.230835+00:00`
- duration_sec: `0.032`
```text
Wrote docs/quantum-energy-transmutation-report.json
```

## qcit/quantum report validation
- status: **PASS**
- command: `python3 scripts/validate_transmutation_reports.py --qcit docs/qcit-coordination-report.json --quantum docs/quantum-energy-transmutation-report.json`
- started: `2026-02-16T10:32:58.230858+00:00`
- finished: `2026-02-16T10:32:58.253434+00:00`
- duration_sec: `0.023`
```text
validated qcit and quantum transmutation reports
```

## minimum-disclosure verifier (GOV-002)
- status: **PASS**
- command: `python3 freed_id_minimum_disclosure_verifier.py`
- started: `2026-02-16T10:32:58.253458+00:00`
- finished: `2026-02-16T10:32:58.306003+00:00`
- duration_sec: `0.053`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T103258Z-freedid-min-disclosure-check.json
timestamped_md=docs/heart-track-runs/20260216T103258Z-freedid-min-disclosure-check.md
latest_json=docs/heart-track-min-disclosure-latest.json
latest_md=docs/heart-track-min-disclosure-latest.md
```

## minimum-disclosure live-path verifier (GOV-002)
- status: **PASS**
- command: `python3 freed_id_minimum_disclosure_live_path_verifier.py`
- started: `2026-02-16T10:32:58.306026+00:00`
- finished: `2026-02-16T10:32:58.346557+00:00`
- duration_sec: `0.041`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T103258Z-freedid-min-disclosure-live-check.json
timestamped_md=docs/heart-track-runs/20260216T103258Z-freedid-min-disclosure-live-check.md
latest_json=docs/heart-track-min-disclosure-live-latest.json
latest_md=docs/heart-track-min-disclosure-live-latest.md
audit_ledger=docs/freed-id-live-path-audit-log.jsonl
```

## minimum-disclosure adversarial verifier (GOV-002)
- status: **PASS**
- command: `python3 freed_id_minimum_disclosure_adversarial_verifier.py`
- started: `2026-02-16T10:32:58.346579+00:00`
- finished: `2026-02-16T10:32:58.381324+00:00`
- duration_sec: `0.035`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T103258Z-freedid-min-disclosure-adversarial-check.json
timestamped_md=docs/heart-track-runs/20260216T103258Z-freedid-min-disclosure-adversarial-check.md
latest_json=docs/heart-track-min-disclosure-adversarial-latest.json
latest_md=docs/heart-track-min-disclosure-adversarial-latest.md
```

## dispute/recourse verifier (GOV-004)
- status: **PASS**
- command: `python3 freed_id_dispute_recourse_verifier.py`
- started: `2026-02-16T10:32:58.381346+00:00`
- finished: `2026-02-16T10:32:58.422733+00:00`
- duration_sec: `0.041`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T103258Z-freedid-dispute-recourse-check.json
timestamped_md=docs/heart-track-runs/20260216T103258Z-freedid-dispute-recourse-check.md
latest_json=docs/heart-track-dispute-recourse-latest.json
latest_md=docs/heart-track-dispute-recourse-latest.md
```

## dispute/recourse adversarial verifier (GOV-004)
- status: **PASS**
- command: `python3 freed_id_dispute_recourse_adversarial_verifier.py`
- started: `2026-02-16T10:32:58.422755+00:00`
- finished: `2026-02-16T10:32:58.460913+00:00`
- duration_sec: `0.038`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T103258Z-freedid-dispute-recourse-adversarial-check.json
timestamped_md=docs/heart-track-runs/20260216T103258Z-freedid-dispute-recourse-adversarial-check.md
latest_json=docs/heart-track-dispute-recourse-adversarial-latest.json
latest_md=docs/heart-track-dispute-recourse-adversarial-latest.md
```

## token/credit zip converter
- status: **PASS**
- command: `python3 scripts/trinity_token_credit_zip_converter.py --use-reserve-first --regeneration-multiplier 3.0 --target-reimbursement-ratio 1.0 --zip-snapshot --zip-label token-credit-suite --out docs/token-credit-bank-report.json --ledger docs/token-credit-bank-ledger.jsonl`
- started: `2026-02-16T10:32:58.460936+00:00`
- finished: `2026-02-16T10:32:58.528859+00:00`
- duration_sec: `0.068`
```text
Wrote /workspace/docs/token-credit-bank-report.json
Appended /workspace/docs/token-credit-bank-ledger.jsonl
Wrote /workspace/docs/memory-archives/20260216T103258Z-token-credit-suite.zip
```

## cache/waste regenerator
- status: **PASS**
- command: `python3 scripts/cache_waste_regenerator.py --out docs/cache-waste-regenerator-report.json --purge --prune-empty-dirs`
- started: `2026-02-16T10:32:58.528898+00:00`
- finished: `2026-02-16T10:32:58.563628+00:00`
- duration_sec: `0.035`
```text
Wrote /workspace/docs/cache-waste-regenerator-report.json
```

## cache/waste report validation
- status: **PASS**
- command: `python3 scripts/validate_cache_waste_report.py --cache docs/cache-waste-regenerator-report.json`
- started: `2026-02-16T10:32:58.563652+00:00`
- finished: `2026-02-16T10:32:58.586296+00:00`
- duration_sec: `0.023`
```text
validated cache-waste regenerator report
```

## energy bank system
- status: **PASS**
- command: `python3 scripts/trinity_energy_bank_system.py --token-report docs/token-credit-bank-report.json --cache-report docs/cache-waste-regenerator-report.json --reserve-growth 1.0 --reserve-cap-multiplier 10.0 --auto-max-cap --cap-ceiling 100.0 --out docs/energy-bank-report.json --state docs/energy-bank-state.json`
- started: `2026-02-16T10:32:58.586319+00:00`
- finished: `2026-02-16T10:32:58.610296+00:00`
- duration_sec: `0.024`
```text
Wrote /workspace/docs/energy-bank-report.json
Updated /workspace/docs/energy-bank-state.json
```

## token/energy report validation
- status: **PASS**
- command: `python3 scripts/validate_token_energy_reports.py --token docs/token-credit-bank-report.json --energy docs/energy-bank-report.json`
- started: `2026-02-16T10:32:58.610322+00:00`
- finished: `2026-02-16T10:32:58.633920+00:00`
- duration_sec: `0.024`
```text
validated token-credit and energy-bank reports
```

## gyroscopic hybrid zip converter
- status: **PASS**
- command: `python3 scripts/gyroscopic_hybrid_zip_converter_generator.py --label gyroscopic-suite-cycle --out docs/gyroscopic-hybrid-zip-report.json`
- started: `2026-02-16T10:32:58.633943+00:00`
- finished: `2026-02-16T10:32:58.673212+00:00`
- duration_sec: `0.039`
```text
Wrote /workspace/docs/gyroscopic-hybrid-zip-report.json
```

## body benchmark guardrail check (enforce)
- status: **PASS**
- command: `python3 body_track_runner.py --gammas 0.0 0.01 0.05 --benchmark-profile quick --profile-policy docs/body-profile-policy-v1.json --fail-on-benchmark`
- started: `2026-02-16T10:32:58.673236+00:00`
- finished: `2026-02-16T10:32:58.907720+00:00`
- duration_sec: `0.234`
```text
overall_status=PASS
timestamped_json=docs/body-track-runs/20260216T103258Z-body-track-smoke.json
timestamped_md=docs/body-track-runs/20260216T103258Z-body-track-smoke.md
latest_json=docs/body-track-smoke-latest.json
latest_md=docs/body-track-smoke-latest.md
timestamped_metrics=docs/body-track-runs/20260216T103258Z-body-track-metrics.json
timestamped_benchmark=docs/body-track-runs/20260216T103258Z-body-track-benchmark.json
latest_metrics=docs/body-track-metrics-latest.json
latest_benchmark=docs/body-track-benchmark-latest.json
metrics_history=docs/body-track-metrics-history.jsonl
```

## body benchmark trend guard (enforce)
- status: **PASS**
- command: `python3 scripts/body_benchmark_trend_guard.py --trend-profile quick --profile-policy docs/body-profile-policy-v1.json --fail-on-warn`
- started: `2026-02-16T10:32:58.907772+00:00`
- finished: `2026-02-16T10:32:58.939164+00:00`
- duration_sec: `0.031`
```text
overall_status=PASS
timestamped_json=docs/body-track-runs/20260216T103258Z-body-track-trend-guard.json
timestamped_md=docs/body-track-runs/20260216T103258Z-body-track-trend-guard.md
latest_json=docs/body-track-trend-guard-latest.json
latest_md=docs/body-track-trend-guard-latest.md
```

## body profile calibration report
- status: **PASS**
- command: `python3 scripts/body_profile_calibration_report.py --profile-context quick`
- started: `2026-02-16T10:32:58.939198+00:00`
- finished: `2026-02-16T10:32:58.984872+00:00`
- duration_sec: `0.046`
```text
overall_status=PASS
timestamped_json=docs/body-track-runs/20260216T103258Z-body-track-calibration.json
timestamped_md=docs/body-track-runs/20260216T103258Z-body-track-calibration.md
latest_json=docs/body-track-calibration-latest.json
latest_md=docs/body-track-calibration-latest.md
```

## body policy delta report (enforce)
- status: **PASS**
- command: `python3 scripts/body_profile_policy_delta_report.py --policy-json docs/body-profile-policy-v1.json --apply --fail-on-warn`
- started: `2026-02-16T10:32:58.984917+00:00`
- finished: `2026-02-16T10:32:59.028449+00:00`
- duration_sec: `0.044`
```text
overall_status=PASS
timestamped_json=docs/body-track-runs/20260216T103259Z-body-track-policy-delta.json
timestamped_md=docs/body-track-runs/20260216T103259Z-body-track-policy-delta.md
latest_json=docs/body-track-policy-delta-latest.json
latest_md=docs/body-track-policy-delta-latest.md
```

## body policy stress-window report (enforce)
- status: **PASS**
- command: `python3 scripts/body_policy_stress_window_report.py --policy-json docs/body-profile-policy-v1.json --fail-on-warn`
- started: `2026-02-16T10:32:59.028472+00:00`
- finished: `2026-02-16T10:32:59.056480+00:00`
- duration_sec: `0.028`
```text
overall_status=PASS
timestamped_json=docs/body-track-runs/20260216T103259Z-body-track-policy-stress.json
timestamped_md=docs/body-track-runs/20260216T103259Z-body-track-policy-stress.md
latest_json=docs/body-track-policy-stress-latest.json
latest_md=docs/body-track-policy-stress-latest.md
```

## gmut comparator metrics
- status: **PASS**
- command: `python3 scripts/gmut_comparator_metrics.py`
- started: `2026-02-16T10:32:59.056503+00:00`
- finished: `2026-02-16T10:32:59.082359+00:00`
- duration_sec: `0.026`
```text
status=PASS
timestamped_json=docs/mind-track-runs/20260216T103259Z-gmut-comparator-metrics.json
timestamped_md=docs/mind-track-runs/20260216T103259Z-gmut-comparator-metrics.md
latest_json=docs/mind-track-gmut-comparator-latest.json
latest_md=docs/mind-track-gmut-comparator-latest.md
```

## gmut external-anchor exclusion note
- status: **PASS**
- command: `python3 scripts/gmut_external_anchor_exclusion_note.py --anchor-input docs/mind-track-external-anchor-canonical-inputs-v1.json`
- started: `2026-02-16T10:32:59.082382+00:00`
- finished: `2026-02-16T10:32:59.109067+00:00`
- duration_sec: `0.027`
```text
overall_status=WARN
timestamped_json=docs/mind-track-runs/20260216T103259Z-gmut-anchor-exclusion-note.json
timestamped_md=docs/mind-track-runs/20260216T103259Z-gmut-anchor-exclusion-note.md
latest_json=docs/mind-track-gmut-anchor-exclusion-latest.json
latest_md=docs/mind-track-gmut-anchor-exclusion-latest.md
```

## gmut anchor trace validation (enforce)
- status: **PASS**
- command: `python3 scripts/gmut_anchor_trace_validator.py --fail-on-warn`
- started: `2026-02-16T10:32:59.109090+00:00`
- finished: `2026-02-16T10:32:59.145554+00:00`
- duration_sec: `0.036`
```text
overall_status=PASS
timestamped_json=docs/mind-track-runs/20260216T103259Z-gmut-anchor-trace-validation.json
timestamped_md=docs/mind-track-runs/20260216T103259Z-gmut-anchor-trace-validation.md
latest_json=docs/mind-track-gmut-trace-validation-latest.json
latest_md=docs/mind-track-gmut-trace-validation-latest.md
```

## zip memory/data snapshot
- status: **PASS**
- command: `python3 scripts/trinity_zip_memory_converter.py archive --label suite-quick`
- started: `2026-02-16T10:32:59.145577+00:00`
- finished: `2026-02-16T10:32:59.183626+00:00`
- duration_sec: `0.038`
```text
Wrote /workspace/docs/memory-archives/20260216T103259Z-suite-quick.zip
```

## v33 structural OCR validation snapshot
- status: **PASS**
- command: `bash -lc 'strings -n 8 '"'"'Beyonder-Real-True Journey v33 (Arielis) (2).pdf'"'"' | rg -n '"'"'Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill'"'"' | head -n 20'`
- started: `2026-02-16T10:32:59.183649+00:00`
- finished: `2026-02-16T10:32:59.321356+00:00`
- duration_sec: `0.138`
```text
182:/URI (https://www.americanscientist.org/article/quantizing-the-universe#:~:text=In%20Three%20Roads%20to%20Quantum,has%20not%20been%20verified%20experimentally)>>
243:/URI (https://www.americanscientist.org/article/quantizing-the-universe#:~:text=In%20Three%20Roads%20to%20Quantum,has%20not%20been%20verified%20experimentally)>>
282:/URI (https://www.americanscientist.org/article/quantizing-the-universe#:~:text=In%20Three%20Roads%20to%20Quantum,has%20not%20been%20verified%20experimentally)>>
391:/URI (https://www.americanscientist.org/article/quantizing-the-universe#:~:text=In%20Three%20Roads%20to%20Quantum,has%20not%20been%20verified%20experimentally)>>
7392:/Alt ([Equation start, Function start \\subscript, L, Next parameter, GMUT, Function end, =, Function start \\subscript, L, Next parameter, GR, Function end, +, Function start \\subscript, L, Next parameter, SM, Function end, +, Function start \\subscript, L, Next parameter, Psi, Function end, +, Function start \\subscript, L, Next parameter, int, Function end, ,, Equation end])
8462:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT, Equation end])
8477:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT=, Function start \\subscript, L, Next parameter, e, Function end, xtEH+, Function start \\subscript, L, Next parameter, e, Function end, xtSM+, Function start \\subscript, L, Next parameter, psi, Function end, +, Function start \\subscript, L, Next parameter, e, Function end, xtint,, Equation end])
8858:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT, Equation end])
9493:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT, Equation end])
9508:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT=, Function start \\subscript, L, Next parameter, e, Function end, xtEH+, Function start \\subscript, L, Next parameter, e, Function end, xtSM+, Function start \\subscript, L, Next parameter, psi, Function end, +, Function start \\subscript, L, Next parameter, e, Function end, xtint,, Equation end])
9889:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT, Equation end])
10763:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT, Equation end])
10778:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT=, Function start \\subscript, L, Next parameter, e, Function end, xtEH+, Function start \\subscript, L, Next parameter, e, Function end, xtSM+, Function start \\subscript, L, Next parameter, psi, Function end, +, Function start \\subscript, L, Next parameter, e, Function end, xtint,, Equation end])
11159:/Alt ([Equation start, Function start \\subscript, L, Next parameter, e, Function end, xtGMUT, Equation end])
16083:<</Title (5\) Freed ID is anchored to Self-Sovereign Identity ideas )
16351:<</Title (1. Run GMUT Minimal Falsifiable Claim Set )
16537:<</Title (1. Formalise GMUT mathematically )
16602:<</Title (3. Conceptual Quantum Energy Transmutation Engine )
16609:<</Title (4. Adopt W3C DID for the Freed ID System )
16623:<</Title (Review of the Quantum Energy Transmutation Engine )
```

## Overall status
- Effective success: **True**
- PASS: **26**
- WARN: **0**
- TIMEOUT: **0**
- FAIL: **0**
- Achieved steps: **26**
- Achievement gate met: **True**
- Suite started: `2026-02-16T10:32:58.113863+00:00`
- Suite finished: `2026-02-16T10:32:59.321401+00:00`
- Suite duration_sec: `1.208`

## Machine-readable summary
```json
{
  "generated_utc": "2026-02-16T10:32:59.321410+00:00",
  "suite_started_at_utc": "2026-02-16T10:32:58.113863+00:00",
  "suite_finished_at_utc": "2026-02-16T10:32:59.321401+00:00",
  "suite_duration_sec": 1.208,
  "effective_success": true,
  "achieved_steps": 26,
  "achievement_gate_met": true,
  "counts": {
    "pass": 26,
    "warn": 0,
    "timeout": 0,
    "fail": 0
  },
  "config": {
    "step_timeout_sec": 0,
    "profile": "quick",
    "profile_source": "--profile",
    "include_version_scan": false,
    "include_skill_install": false,
    "include_curated_skill_catalog": false,
    "soft_fail_network": false,
    "fail_on_warn": false,
    "achievement_target_steps": 0,
    "quick_mode": true,
    "body_benchmark_mode": "enforce",
    "include_body_benchmark": true
  },
  "results": [
    {
      "label": "memory integrity check (strict)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.113931+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.137089+00:00",
      "duration_sec": 0.023,
      "command": "python3 scripts/aurelis_memory_integrity_check.py --strict"
    },
    {
      "label": "continuity cycle tick (dry-run status)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.137115+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.166414+00:00",
      "duration_sec": 0.029,
      "command": "python3 scripts/aurelis_cycle_tick.py --user-message 'suite quick dry-run' --assistant-reflection 'Quick mode continuity health check' --progress-snapshot 'Validated quick dry-run status reporting in suite' --next-step 'Run full suite when deeper validation is needed' --query cycle --query-limit 2 --dry-run --no-report --step-timeout-sec 0 --json-status docs/aurelis-cycle-tick-status.json"
    },
    {
      "label": "qcit coordination engine",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.166451+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.199234+00:00",
      "duration_sec": 0.033,
      "command": "python3 scripts/qcit_coordination_engine.py --out docs/qcit-coordination-report.json"
    },
    {
      "label": "quantum energy transmutation engine",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.199261+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.230835+00:00",
      "duration_sec": 0.032,
      "command": "python3 scripts/quantum_energy_transmutation_engine.py --out docs/quantum-energy-transmutation-report.json"
    },
    {
      "label": "qcit/quantum report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.230858+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.253434+00:00",
      "duration_sec": 0.023,
      "command": "python3 scripts/validate_transmutation_reports.py --qcit docs/qcit-coordination-report.json --quantum docs/quantum-energy-transmutation-report.json"
    },
    {
      "label": "minimum-disclosure verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.253458+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.306003+00:00",
      "duration_sec": 0.053,
      "command": "python3 freed_id_minimum_disclosure_verifier.py"
    },
    {
      "label": "minimum-disclosure live-path verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.306026+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.346557+00:00",
      "duration_sec": 0.041,
      "command": "python3 freed_id_minimum_disclosure_live_path_verifier.py"
    },
    {
      "label": "minimum-disclosure adversarial verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.346579+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.381324+00:00",
      "duration_sec": 0.035,
      "command": "python3 freed_id_minimum_disclosure_adversarial_verifier.py"
    },
    {
      "label": "dispute/recourse verifier (GOV-004)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.381346+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.422733+00:00",
      "duration_sec": 0.041,
      "command": "python3 freed_id_dispute_recourse_verifier.py"
    },
    {
      "label": "dispute/recourse adversarial verifier (GOV-004)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.422755+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.460913+00:00",
      "duration_sec": 0.038,
      "command": "python3 freed_id_dispute_recourse_adversarial_verifier.py"
    },
    {
      "label": "token/credit zip converter",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.460936+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.528859+00:00",
      "duration_sec": 0.068,
      "command": "python3 scripts/trinity_token_credit_zip_converter.py --use-reserve-first --regeneration-multiplier 3.0 --target-reimbursement-ratio 1.0 --zip-snapshot --zip-label token-credit-suite --out docs/token-credit-bank-report.json --ledger docs/token-credit-bank-ledger.jsonl"
    },
    {
      "label": "cache/waste regenerator",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.528898+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.563628+00:00",
      "duration_sec": 0.035,
      "command": "python3 scripts/cache_waste_regenerator.py --out docs/cache-waste-regenerator-report.json --purge --prune-empty-dirs"
    },
    {
      "label": "cache/waste report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.563652+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.586296+00:00",
      "duration_sec": 0.023,
      "command": "python3 scripts/validate_cache_waste_report.py --cache docs/cache-waste-regenerator-report.json"
    },
    {
      "label": "energy bank system",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.586319+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.610296+00:00",
      "duration_sec": 0.024,
      "command": "python3 scripts/trinity_energy_bank_system.py --token-report docs/token-credit-bank-report.json --cache-report docs/cache-waste-regenerator-report.json --reserve-growth 1.0 --reserve-cap-multiplier 10.0 --auto-max-cap --cap-ceiling 100.0 --out docs/energy-bank-report.json --state docs/energy-bank-state.json"
    },
    {
      "label": "token/energy report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.610322+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.633920+00:00",
      "duration_sec": 0.024,
      "command": "python3 scripts/validate_token_energy_reports.py --token docs/token-credit-bank-report.json --energy docs/energy-bank-report.json"
    },
    {
      "label": "gyroscopic hybrid zip converter",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.633943+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.673212+00:00",
      "duration_sec": 0.039,
      "command": "python3 scripts/gyroscopic_hybrid_zip_converter_generator.py --label gyroscopic-suite-cycle --out docs/gyroscopic-hybrid-zip-report.json"
    },
    {
      "label": "body benchmark guardrail check (enforce)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.673236+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.907720+00:00",
      "duration_sec": 0.234,
      "command": "python3 body_track_runner.py --gammas 0.0 0.01 0.05 --benchmark-profile quick --profile-policy docs/body-profile-policy-v1.json --fail-on-benchmark"
    },
    {
      "label": "body benchmark trend guard (enforce)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.907772+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.939164+00:00",
      "duration_sec": 0.031,
      "command": "python3 scripts/body_benchmark_trend_guard.py --trend-profile quick --profile-policy docs/body-profile-policy-v1.json --fail-on-warn"
    },
    {
      "label": "body profile calibration report",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.939198+00:00",
      "finished_at_utc": "2026-02-16T10:32:58.984872+00:00",
      "duration_sec": 0.046,
      "command": "python3 scripts/body_profile_calibration_report.py --profile-context quick"
    },
    {
      "label": "body policy delta report (enforce)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:58.984917+00:00",
      "finished_at_utc": "2026-02-16T10:32:59.028449+00:00",
      "duration_sec": 0.044,
      "command": "python3 scripts/body_profile_policy_delta_report.py --policy-json docs/body-profile-policy-v1.json --apply --fail-on-warn"
    },
    {
      "label": "body policy stress-window report (enforce)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:59.028472+00:00",
      "finished_at_utc": "2026-02-16T10:32:59.056480+00:00",
      "duration_sec": 0.028,
      "command": "python3 scripts/body_policy_stress_window_report.py --policy-json docs/body-profile-policy-v1.json --fail-on-warn"
    },
    {
      "label": "gmut comparator metrics",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:59.056503+00:00",
      "finished_at_utc": "2026-02-16T10:32:59.082359+00:00",
      "duration_sec": 0.026,
      "command": "python3 scripts/gmut_comparator_metrics.py"
    },
    {
      "label": "gmut external-anchor exclusion note",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:59.082382+00:00",
      "finished_at_utc": "2026-02-16T10:32:59.109067+00:00",
      "duration_sec": 0.027,
      "command": "python3 scripts/gmut_external_anchor_exclusion_note.py --anchor-input docs/mind-track-external-anchor-canonical-inputs-v1.json"
    },
    {
      "label": "gmut anchor trace validation (enforce)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:59.109090+00:00",
      "finished_at_utc": "2026-02-16T10:32:59.145554+00:00",
      "duration_sec": 0.036,
      "command": "python3 scripts/gmut_anchor_trace_validator.py --fail-on-warn"
    },
    {
      "label": "zip memory/data snapshot",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:59.145577+00:00",
      "finished_at_utc": "2026-02-16T10:32:59.183626+00:00",
      "duration_sec": 0.038,
      "command": "python3 scripts/trinity_zip_memory_converter.py archive --label suite-quick"
    },
    {
      "label": "v33 structural OCR validation snapshot",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T10:32:59.183649+00:00",
      "finished_at_utc": "2026-02-16T10:32:59.321356+00:00",
      "duration_sec": 0.138,
      "command": "bash -lc 'strings -n 8 '\"'\"'Beyonder-Real-True Journey v33 (Arielis) (2).pdf'\"'\"' | rg -n '\"'\"'Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill'\"'\"' | head -n 20'"
    }
  ]
}
```

