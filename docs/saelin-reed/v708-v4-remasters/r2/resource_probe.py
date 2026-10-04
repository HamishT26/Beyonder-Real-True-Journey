"""One bounded resource observation; no daemon, commands, identities or credentials."""
import argparse
import datetime
import json
import math
from pathlib import Path
import platform
import re
import sys
import time

import psutil

WATCHED = {'chatgpt.exe', 'codex.exe', 'node.exe', 'pwsh.exe', 'powershell.exe',
           'python.exe', 'chrome.exe', 'vmmemwsl', 'node', 'python3', 'pwsh', 'codex'}


def process_sample():
    rows, unavailable = {}, 0
    for process in psutil.process_iter(['pid', 'name', 'create_time']):
        if process.pid == 0:
            continue
        try:
            with process.oneshot():
                if not isinstance(process.info['create_time'], (int, float)) or not math.isfinite(process.info['create_time']):
                    unavailable += 1
                    continue
                name = (process.info['name'] or '').lower()
                group = name if name in WATCHED else 'other'
                cpu = process.cpu_times()
                sampled_at = time.perf_counter()
                rows[(process.pid, process.info['create_time'])] = {
                    'group': group, 'cpu': cpu.user + cpu.system,
                    'rss': process.memory_info().rss, 'sampled_at': sampled_at,
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            unavailable += 1
    return rows, unavailable


def cgroup_limits():
    result = {'cpu_quota': None, 'memory_max_bytes': None, 'memory_current_bytes': None,
              'scope': 'v2 standard paths only; absence is not proof of no other limits'}
    if sys.platform != 'linux':
        result['scope'] = 'not a Linux cgroup observation; Windows job limits unmeasured'
        return result
    for key, filename in [('memory_max_bytes', 'memory.max'), ('memory_current_bytes', 'memory.current')]:
        try:
            value = (Path('/sys/fs/cgroup') / filename).read_text().strip()
            result[key] = int(value) if value != 'max' else None
        except (OSError, ValueError):
            pass
    try:
        quota, period = Path('/sys/fs/cgroup/cpu.max').read_text().split()
        result['cpu_quota'] = int(quota) / int(period) if quota != 'max' and int(period) > 0 else None
    except (OSError, ValueError):
        pass
    return result


def aggregate_samples(before, after, logical):
    capacity = logical if type(logical) is int and logical > 0 else None
    groups = {}
    for identity, row in after.items():
        group = groups.setdefault(row['group'], {
            'process_count': 0, 'rss_sum_bytes': 0, 'matched_cpu_samples': 0,
            'cpu_seconds_observed': 0, 'cpu_core_equivalents_sum': 0,
            'new_processes_without_baseline': 0, 'invalid_counter_pairs': 0,
            'sample_intervals_seconds': [],
        })
        group['process_count'] += 1
        group['rss_sum_bytes'] += row['rss']
        if identity not in before:
            group['new_processes_without_baseline'] += 1
            continue
        previous = before[identity]
        interval = row['sampled_at'] - previous['sampled_at']
        delta = row['cpu'] - previous['cpu']
        if not math.isfinite(interval) or interval <= 0 or not math.isfinite(delta) or delta < 0:
            group['invalid_counter_pairs'] += 1
            continue
        group['matched_cpu_samples'] += 1
        group['cpu_seconds_observed'] += delta
        group['cpu_core_equivalents_sum'] += delta / interval
        group['sample_intervals_seconds'].append(interval)
    for group in groups.values():
        intervals = group.pop('sample_intervals_seconds')
        group['sample_interval_min_seconds'] = min(intervals) if intervals else None
        group['sample_interval_max_seconds'] = max(intervals) if intervals else None
        group['matched_process_cpu_percent_of_logical_capacity'] = (
            100 * group['cpu_core_equivalents_sum'] / capacity
            if capacity is not None and group['matched_cpu_samples'] else None)
    return groups, capacity


def main():
    entry = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=2)
    parser.add_argument('--label', default='bounded-observation',
                        choices=['bounded-observation', 'baseline', 'active-work', 'post-change', 'diagnostic'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not math.isfinite(args.seconds) or not 0.2 <= args.seconds <= 30:
        parser.error('seconds must be finite and between 0.2 and 30')
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', args.label):
        parser.error('label must be a short non-identifying token')
    if args.output.exists():
        parser.error('refusing to overwrite an observation')
    before, denied_before = process_sample()
    psutil.cpu_percent(interval=None)
    start = time.perf_counter()
    time.sleep(args.seconds)
    after, denied_after = process_sample()
    elapsed = time.perf_counter() - start
    system_percent = psutil.cpu_percent(interval=None)
    groups, logical = aggregate_samples(before, after, psutil.cpu_count())
    memory = psutil.virtual_memory()
    result = {
        'schema': 'ghc.bounded-resource-observation.v2',
        'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'label': args.label, 'platform': platform.system(), 'python': platform.python_version(),
        'psutil': psutil.__version__, 'requested_seconds': args.seconds, 'sleep_and_final_scan_seconds': elapsed,
        'time_to_serialization_seconds': time.perf_counter() - entry,
        'logical_cpu_count': logical, 'system_cpu_percent': system_percent,
        'physical_memory_bytes': memory.total, 'available_memory_bytes': memory.available,
        'cgroup': cgroup_limits(), 'groups': groups,
        'unavailable_process_samples': {'before': denied_before, 'after': denied_after},
        'exited_or_missing_processes': len(set(before) - set(after)),
        'cpu_scope': 'sum of per-process rates for matched surviving identities; each uses its own monotonic observation interval; not a simultaneous census',
        'scope': 'point-in-time observation; no scheduler, privilege, thermal or causal claim',
        'rss_note': 'summed process RSS can double-count shared pages and is not system memory consumption',
        'privacy': 'controlled label vocabulary; no host name, username, PID, executable path, command line, environment or connection endpoints emitted',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8', newline='\n') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps({'output_saved': True, 'elapsed_seconds': elapsed,
                      'system_cpu_percent': system_percent,
                      'available_memory_mib': round(memory.available / 1024**2),
                      'groups': len(groups), 'observation_only': True}))


if __name__ == '__main__':
    main()
