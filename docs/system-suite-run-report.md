# Trinity System Suite Run Report

Generated: 2026-02-16T05:02:41.028521+00:00
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
- started: `2026-02-16T05:02:41.028563+00:00`
- finished: `2026-02-16T05:02:41.052281+00:00`
- duration_sec: `0.024`
```text
Wrote /workspace/docs/aurelis-memory-integrity-report.md
```

## continuity cycle tick (dry-run status)
- status: **PASS**
- command: `python3 scripts/aurelis_cycle_tick.py --user-message 'suite quick dry-run' --assistant-reflection 'Quick mode continuity health check' --progress-snapshot 'Validated quick dry-run status reporting in suite' --next-step 'Run full suite when deeper validation is needed' --query cycle --query-limit 2 --dry-run --no-report --step-timeout-sec 0 --json-status docs/aurelis-cycle-tick-status.json`
- started: `2026-02-16T05:02:41.052309+00:00`
- finished: `2026-02-16T05:02:41.080471+00:00`
- duration_sec: `0.028`
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
- started: `2026-02-16T05:02:41.080507+00:00`
- finished: `2026-02-16T05:02:41.114112+00:00`
- duration_sec: `0.034`
```text
Wrote docs/qcit-coordination-report.json
```

## quantum energy transmutation engine
- status: **PASS**
- command: `python3 scripts/quantum_energy_transmutation_engine.py --out docs/quantum-energy-transmutation-report.json`
- started: `2026-02-16T05:02:41.114139+00:00`
- finished: `2026-02-16T05:02:41.147539+00:00`
- duration_sec: `0.033`
```text
Wrote docs/quantum-energy-transmutation-report.json
```

## qcit/quantum report validation
- status: **PASS**
- command: `python3 scripts/validate_transmutation_reports.py --qcit docs/qcit-coordination-report.json --quantum docs/quantum-energy-transmutation-report.json`
- started: `2026-02-16T05:02:41.147565+00:00`
- finished: `2026-02-16T05:02:41.172281+00:00`
- duration_sec: `0.025`
```text
validated qcit and quantum transmutation reports
```

## minimum-disclosure verifier (GOV-002)
- status: **PASS**
- command: `python3 freed_id_minimum_disclosure_verifier.py`
- started: `2026-02-16T05:02:41.172306+00:00`
- finished: `2026-02-16T05:02:41.212457+00:00`
- duration_sec: `0.040`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T050241Z-freedid-min-disclosure-check.json
timestamped_md=docs/heart-track-runs/20260216T050241Z-freedid-min-disclosure-check.md
latest_json=docs/heart-track-min-disclosure-latest.json
latest_md=docs/heart-track-min-disclosure-latest.md
```

## minimum-disclosure live-path verifier (GOV-002)
- status: **PASS**
- command: `python3 freed_id_minimum_disclosure_live_path_verifier.py`
- started: `2026-02-16T05:02:41.212482+00:00`
- finished: `2026-02-16T05:02:41.252754+00:00`
- duration_sec: `0.040`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T050241Z-freedid-min-disclosure-live-check.json
timestamped_md=docs/heart-track-runs/20260216T050241Z-freedid-min-disclosure-live-check.md
latest_json=docs/heart-track-min-disclosure-live-latest.json
latest_md=docs/heart-track-min-disclosure-live-latest.md
audit_ledger=docs/freed-id-live-path-audit-log.jsonl
```

## minimum-disclosure adversarial verifier (GOV-002)
- status: **PASS**
- command: `python3 freed_id_minimum_disclosure_adversarial_verifier.py`
- started: `2026-02-16T05:02:41.252782+00:00`
- finished: `2026-02-16T05:02:41.289182+00:00`
- duration_sec: `0.036`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T050241Z-freedid-min-disclosure-adversarial-check.json
timestamped_md=docs/heart-track-runs/20260216T050241Z-freedid-min-disclosure-adversarial-check.md
latest_json=docs/heart-track-min-disclosure-adversarial-latest.json
latest_md=docs/heart-track-min-disclosure-adversarial-latest.md
```

## dispute/recourse verifier (GOV-004)
- status: **PASS**
- command: `python3 freed_id_dispute_recourse_verifier.py`
- started: `2026-02-16T05:02:41.289205+00:00`
- finished: `2026-02-16T05:02:41.327285+00:00`
- duration_sec: `0.038`
```text
overall_status=PASS
timestamped_json=docs/heart-track-runs/20260216T050241Z-freedid-dispute-recourse-check.json
timestamped_md=docs/heart-track-runs/20260216T050241Z-freedid-dispute-recourse-check.md
latest_json=docs/heart-track-dispute-recourse-latest.json
latest_md=docs/heart-track-dispute-recourse-latest.md
```

## token/credit zip converter
- status: **PASS**
- command: `python3 scripts/trinity_token_credit_zip_converter.py --use-reserve-first --regeneration-multiplier 3.0 --target-reimbursement-ratio 1.0 --zip-snapshot --zip-label token-credit-suite --out docs/token-credit-bank-report.json --ledger docs/token-credit-bank-ledger.jsonl`
- started: `2026-02-16T05:02:41.327309+00:00`
- finished: `2026-02-16T05:02:41.394425+00:00`
- duration_sec: `0.067`
```text
Wrote /workspace/docs/token-credit-bank-report.json
Appended /workspace/docs/token-credit-bank-ledger.jsonl
Wrote /workspace/docs/memory-archives/20260216T050241Z-token-credit-suite.zip
```

## cache/waste regenerator
- status: **PASS**
- command: `python3 scripts/cache_waste_regenerator.py --out docs/cache-waste-regenerator-report.json --purge --prune-empty-dirs`
- started: `2026-02-16T05:02:41.394459+00:00`
- finished: `2026-02-16T05:02:41.429275+00:00`
- duration_sec: `0.035`
```text
Wrote /workspace/docs/cache-waste-regenerator-report.json
```

## cache/waste report validation
- status: **PASS**
- command: `python3 scripts/validate_cache_waste_report.py --cache docs/cache-waste-regenerator-report.json`
- started: `2026-02-16T05:02:41.429303+00:00`
- finished: `2026-02-16T05:02:41.452291+00:00`
- duration_sec: `0.023`
```text
validated cache-waste regenerator report
```

## energy bank system
- status: **PASS**
- command: `python3 scripts/trinity_energy_bank_system.py --token-report docs/token-credit-bank-report.json --cache-report docs/cache-waste-regenerator-report.json --reserve-growth 1.0 --reserve-cap-multiplier 10.0 --auto-max-cap --cap-ceiling 100.0 --out docs/energy-bank-report.json --state docs/energy-bank-state.json`
- started: `2026-02-16T05:02:41.452321+00:00`
- finished: `2026-02-16T05:02:41.477292+00:00`
- duration_sec: `0.025`
```text
Wrote /workspace/docs/energy-bank-report.json
Updated /workspace/docs/energy-bank-state.json
```

## token/energy report validation
- status: **PASS**
- command: `python3 scripts/validate_token_energy_reports.py --token docs/token-credit-bank-report.json --energy docs/energy-bank-report.json`
- started: `2026-02-16T05:02:41.477318+00:00`
- finished: `2026-02-16T05:02:41.501849+00:00`
- duration_sec: `0.025`
```text
validated token-credit and energy-bank reports
```

## gyroscopic hybrid zip converter
- status: **PASS**
- command: `python3 scripts/gyroscopic_hybrid_zip_converter_generator.py --label gyroscopic-suite-cycle --out docs/gyroscopic-hybrid-zip-report.json`
- started: `2026-02-16T05:02:41.501875+00:00`
- finished: `2026-02-16T05:02:41.542732+00:00`
- duration_sec: `0.041`
```text
Wrote /workspace/docs/gyroscopic-hybrid-zip-report.json
```

## body benchmark guardrail check (enforce)
- status: **PASS**
- command: `python3 body_track_runner.py --gammas 0.0 0.01 0.05 --benchmark-profile quick --fail-on-benchmark`
- started: `2026-02-16T05:02:41.542759+00:00`
- finished: `2026-02-16T05:02:41.720960+00:00`
- duration_sec: `0.178`
```text
overall_status=PASS
timestamped_json=docs/body-track-runs/20260216T050241Z-body-track-smoke.json
timestamped_md=docs/body-track-runs/20260216T050241Z-body-track-smoke.md
latest_json=docs/body-track-smoke-latest.json
latest_md=docs/body-track-smoke-latest.md
timestamped_metrics=docs/body-track-runs/20260216T050241Z-body-track-metrics.json
timestamped_benchmark=docs/body-track-runs/20260216T050241Z-body-track-benchmark.json
latest_metrics=docs/body-track-metrics-latest.json
latest_benchmark=docs/body-track-benchmark-latest.json
metrics_history=docs/body-track-metrics-history.jsonl
```

## body benchmark trend guard (enforce)
- status: **PASS**
- command: `python3 scripts/body_benchmark_trend_guard.py --trend-profile quick --fail-on-warn`
- started: `2026-02-16T05:02:41.720999+00:00`
- finished: `2026-02-16T05:02:41.752672+00:00`
- duration_sec: `0.032`
```text
overall_status=PASS
timestamped_json=docs/body-track-runs/20260216T050241Z-body-track-trend-guard.json
timestamped_md=docs/body-track-runs/20260216T050241Z-body-track-trend-guard.md
latest_json=docs/body-track-trend-guard-latest.json
latest_md=docs/body-track-trend-guard-latest.md
```

## gmut comparator metrics
- status: **PASS**
- command: `python3 scripts/gmut_comparator_metrics.py`
- started: `2026-02-16T05:02:41.752699+00:00`
- finished: `2026-02-16T05:02:41.780014+00:00`
- duration_sec: `0.027`
```text
status=PASS
timestamped_json=docs/mind-track-runs/20260216T050241Z-gmut-comparator-metrics.json
timestamped_md=docs/mind-track-runs/20260216T050241Z-gmut-comparator-metrics.md
latest_json=docs/mind-track-gmut-comparator-latest.json
latest_md=docs/mind-track-gmut-comparator-latest.md
```

## gmut external-anchor exclusion note
- status: **PASS**
- command: `python3 scripts/gmut_external_anchor_exclusion_note.py`
- started: `2026-02-16T05:02:41.780038+00:00`
- finished: `2026-02-16T05:02:41.806776+00:00`
- duration_sec: `0.027`
```text
overall_status=WARN
timestamped_json=docs/mind-track-runs/20260216T050241Z-gmut-anchor-exclusion-note.json
timestamped_md=docs/mind-track-runs/20260216T050241Z-gmut-anchor-exclusion-note.md
latest_json=docs/mind-track-gmut-anchor-exclusion-latest.json
latest_md=docs/mind-track-gmut-anchor-exclusion-latest.md
```

## zip memory/data snapshot
- status: **PASS**
- command: `python3 scripts/trinity_zip_memory_converter.py archive --label suite-quick`
- started: `2026-02-16T05:02:41.806801+00:00`
- finished: `2026-02-16T05:02:41.846661+00:00`
- duration_sec: `0.040`
```text
Wrote /workspace/docs/memory-archives/20260216T050241Z-suite-quick.zip
```

## v33 structural OCR validation snapshot
- status: **PASS**
- command: `bash -lc 'strings -n 8 '"'"'Beyonder-Real-True Journey v33 (Arielis) (2).pdf'"'"' | rg -n '"'"'Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill'"'"' | head -n 20'`
- started: `2026-02-16T05:02:41.846688+00:00`
- finished: `2026-02-16T05:02:41.971853+00:00`
- duration_sec: `0.125`
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
- PASS: **21**
- WARN: **0**
- TIMEOUT: **0**
- FAIL: **0**
- Achieved steps: **21**
- Achievement gate met: **True**
- Suite started: `2026-02-16T05:02:41.028521+00:00`
- Suite finished: `2026-02-16T05:02:41.971922+00:00`
- Suite duration_sec: `0.943`

## Machine-readable summary
```json
{
  "generated_utc": "2026-02-16T05:02:41.971933+00:00",
  "suite_started_at_utc": "2026-02-16T05:02:41.028521+00:00",
  "suite_finished_at_utc": "2026-02-16T05:02:41.971922+00:00",
  "suite_duration_sec": 0.943,
  "effective_success": true,
  "achieved_steps": 21,
  "achievement_gate_met": true,
  "counts": {
    "pass": 21,
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
      "started_at_utc": "2026-02-16T05:02:41.028563+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.052281+00:00",
      "duration_sec": 0.024,
      "command": "python3 scripts/aurelis_memory_integrity_check.py --strict"
    },
    {
      "label": "continuity cycle tick (dry-run status)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.052309+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.080471+00:00",
      "duration_sec": 0.028,
      "command": "python3 scripts/aurelis_cycle_tick.py --user-message 'suite quick dry-run' --assistant-reflection 'Quick mode continuity health check' --progress-snapshot 'Validated quick dry-run status reporting in suite' --next-step 'Run full suite when deeper validation is needed' --query cycle --query-limit 2 --dry-run --no-report --step-timeout-sec 0 --json-status docs/aurelis-cycle-tick-status.json"
    },
    {
      "label": "qcit coordination engine",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.080507+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.114112+00:00",
      "duration_sec": 0.034,
      "command": "python3 scripts/qcit_coordination_engine.py --out docs/qcit-coordination-report.json"
    },
    {
      "label": "quantum energy transmutation engine",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.114139+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.147539+00:00",
      "duration_sec": 0.033,
      "command": "python3 scripts/quantum_energy_transmutation_engine.py --out docs/quantum-energy-transmutation-report.json"
    },
    {
      "label": "qcit/quantum report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.147565+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.172281+00:00",
      "duration_sec": 0.025,
      "command": "python3 scripts/validate_transmutation_reports.py --qcit docs/qcit-coordination-report.json --quantum docs/quantum-energy-transmutation-report.json"
    },
    {
      "label": "minimum-disclosure verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.172306+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.212457+00:00",
      "duration_sec": 0.04,
      "command": "python3 freed_id_minimum_disclosure_verifier.py"
    },
    {
      "label": "minimum-disclosure live-path verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.212482+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.252754+00:00",
      "duration_sec": 0.04,
      "command": "python3 freed_id_minimum_disclosure_live_path_verifier.py"
    },
    {
      "label": "minimum-disclosure adversarial verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.252782+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.289182+00:00",
      "duration_sec": 0.036,
      "command": "python3 freed_id_minimum_disclosure_adversarial_verifier.py"
    },
    {
      "label": "dispute/recourse verifier (GOV-004)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.289205+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.327285+00:00",
      "duration_sec": 0.038,
      "command": "python3 freed_id_dispute_recourse_verifier.py"
    },
    {
      "label": "token/credit zip converter",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.327309+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.394425+00:00",
      "duration_sec": 0.067,
      "command": "python3 scripts/trinity_token_credit_zip_converter.py --use-reserve-first --regeneration-multiplier 3.0 --target-reimbursement-ratio 1.0 --zip-snapshot --zip-label token-credit-suite --out docs/token-credit-bank-report.json --ledger docs/token-credit-bank-ledger.jsonl"
    },
    {
      "label": "cache/waste regenerator",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.394459+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.429275+00:00",
      "duration_sec": 0.035,
      "command": "python3 scripts/cache_waste_regenerator.py --out docs/cache-waste-regenerator-report.json --purge --prune-empty-dirs"
    },
    {
      "label": "cache/waste report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.429303+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.452291+00:00",
      "duration_sec": 0.023,
      "command": "python3 scripts/validate_cache_waste_report.py --cache docs/cache-waste-regenerator-report.json"
    },
    {
      "label": "energy bank system",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.452321+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.477292+00:00",
      "duration_sec": 0.025,
      "command": "python3 scripts/trinity_energy_bank_system.py --token-report docs/token-credit-bank-report.json --cache-report docs/cache-waste-regenerator-report.json --reserve-growth 1.0 --reserve-cap-multiplier 10.0 --auto-max-cap --cap-ceiling 100.0 --out docs/energy-bank-report.json --state docs/energy-bank-state.json"
    },
    {
      "label": "token/energy report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.477318+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.501849+00:00",
      "duration_sec": 0.025,
      "command": "python3 scripts/validate_token_energy_reports.py --token docs/token-credit-bank-report.json --energy docs/energy-bank-report.json"
    },
    {
      "label": "gyroscopic hybrid zip converter",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.501875+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.542732+00:00",
      "duration_sec": 0.041,
      "command": "python3 scripts/gyroscopic_hybrid_zip_converter_generator.py --label gyroscopic-suite-cycle --out docs/gyroscopic-hybrid-zip-report.json"
    },
    {
      "label": "body benchmark guardrail check (enforce)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.542759+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.720960+00:00",
      "duration_sec": 0.178,
      "command": "python3 body_track_runner.py --gammas 0.0 0.01 0.05 --benchmark-profile quick --fail-on-benchmark"
    },
    {
      "label": "body benchmark trend guard (enforce)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.720999+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.752672+00:00",
      "duration_sec": 0.032,
      "command": "python3 scripts/body_benchmark_trend_guard.py --trend-profile quick --fail-on-warn"
    },
    {
      "label": "gmut comparator metrics",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.752699+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.780014+00:00",
      "duration_sec": 0.027,
      "command": "python3 scripts/gmut_comparator_metrics.py"
    },
    {
      "label": "gmut external-anchor exclusion note",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.780038+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.806776+00:00",
      "duration_sec": 0.027,
      "command": "python3 scripts/gmut_external_anchor_exclusion_note.py"
    },
    {
      "label": "zip memory/data snapshot",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.806801+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.846661+00:00",
      "duration_sec": 0.04,
      "command": "python3 scripts/trinity_zip_memory_converter.py archive --label suite-quick"
    },
    {
      "label": "v33 structural OCR validation snapshot",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-02-16T05:02:41.846688+00:00",
      "finished_at_utc": "2026-02-16T05:02:41.971853+00:00",
      "duration_sec": 0.125,
      "command": "bash -lc 'strings -n 8 '\"'\"'Beyonder-Real-True Journey v33 (Arielis) (2).pdf'\"'\"' | rg -n '\"'\"'Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill'\"'\"' | head -n 20'"
    }
  ]
}
```

