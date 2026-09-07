"""Bounded synthetic PCM evidence operations. No playback or external action."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from fractions import Fraction
from pathlib import Path

class Refusal(ValueError):
    pass

def require(condition, code):
    if not condition:
        raise Refusal(code)

def fields(record, names):
    require(set(record) == {'operation', *names}, 'FIELD_SET')

def integers(*values):
    require(all(type(v) is int for v in values), 'INTEGER_TYPE')

def rational(value):
    require(type(value) is str and len(value) <= 80 and
            re.fullmatch(r'-?[0-9]+(?:/[1-9][0-9]*)?', value) is not None, 'RATIONAL_SYNTAX')
    return Fraction(value)

def hex_bytes(value):
    require(type(value) is str and len(value) % 2 == 0 and
            re.fullmatch(r'[0-9a-f]*', value) is not None, 'HEX_SYNTAX')
    require(len(value) <= 131072, 'BYTE_LIMIT')
    return bytes.fromhex(value)

def riff_chunks(r):
    fields(r, ['hex'])
    raw = hex_bytes(r['hex'])
    require(len(raw) >= 12, 'TRUNCATED_RIFF_HEADER')
    require(raw[:4] == b'RIFF', 'UNSUPPORTED_CONTAINER')
    require(raw[8:12] == b'WAVE', 'UNSUPPORTED_FORM')
    require(struct.unpack_from('<I', raw, 4)[0] + 8 == len(raw), 'RIFF_SIZE_MISMATCH')
    chunks = []
    pos = 12
    while pos < len(raw):
        require(len(chunks) < 64, 'CHUNK_LIMIT')
        require(pos + 8 <= len(raw), 'TRUNCATED_CHUNK_HEADER')
        label = raw[pos:pos+4]
        require(all(b < 128 for b in label), 'FOURCC_ASCII')
        size = struct.unpack_from('<I', raw, pos+4)[0]
        end = pos + 8 + size
        require(end <= len(raw), 'CHUNK_OVERRUN')
        padded = end + size % 2
        require(padded <= len(raw), 'MISSING_PADDING')
        chunks.append({'id': label.decode('ascii'), 'offset': pos, 'size': size,
                       'pad_hex': raw[end:padded].hex()})
        pos = padded
    return {'form': 'WAVE', 'bytes': len(raw), 'chunks': chunks}

def pcm_format(r):
    keys = ['tag', 'channels', 'rate', 'bits', 'block_align', 'byte_rate']
    fields(r, keys)
    integers(*(r[k] for k in keys))
    require(r['tag'] == 1, 'FORMAT_TAG')
    require(r['channels'] in (1, 2), 'CHANNEL_COUNT')
    require(1 <= r['rate'] <= 384000, 'SAMPLE_RATE')
    require(r['bits'] in (8, 16), 'SAMPLE_BITS')
    align = r['channels'] * (r['bits'] // 8)
    require(r['block_align'] == align, 'BLOCK_ALIGN_MISMATCH')
    rate = align * r['rate']
    require(r['byte_rate'] == rate, 'BYTE_RATE_MISMATCH')
    return {'frame_bytes': align, 'byte_rate': rate,
            'sample_encoding': 'unsigned' if r['bits'] == 8 else 'signed'}

def pcm_frames(r):
    fields(r, ['data_bytes', 'block_align', 'declared_frames'])
    size, align, declared = r['data_bytes'], r['block_align'], r['declared_frames']
    integers(size, align)
    require(0 <= size <= 1048576, 'DATA_BYTES')
    require(1 <= align <= 64, 'BLOCK_ALIGN')
    require(size % align == 0, 'PARTIAL_FRAME')
    frames = size // align
    if declared is not None:
        integers(declared)
        require(declared >= 0, 'DECLARED_FRAMES')
        require(declared == frames, 'FRAME_COUNT_MISMATCH')
    return {'frames': frames, 'declared_frames': declared,
            'declaration_checked': declared is not None}

def sample_time(r):
    mode = r.get('mode')
    require(mode in ('to_seconds', 'to_index'), 'MODE')
    fields(r, ['mode', 'rate', 'origin', 'index' if mode == 'to_seconds' else 'seconds'])
    rate = r['rate']
    integers(rate)
    require(1 <= rate <= 384000, 'SAMPLE_RATE')
    origin = rational(r['origin'])
    if mode == 'to_seconds':
        index = r['index']
        integers(index)
        require(index >= 0, 'NEGATIVE_INDEX')
        require(index <= 10**12, 'INDEX_LIMIT')
        seconds = origin + Fraction(index, rate)
    else:
        seconds = rational(r['seconds'])
        exact_index = (seconds - origin) * rate
        require(exact_index >= 0, 'NEGATIVE_INDEX')
        require(exact_index.denominator == 1, 'OFF_SAMPLE_GRID')
        index = exact_index.numerator
        require(index <= 10**12, 'INDEX_LIMIT')
    return {'seconds': str(seconds), 'index': index}

def pcm_range(r):
    fields(r, ['bits', 'signed', 'samples'])
    bits, signed, samples = r['bits'], r['signed'], r['samples']
    integers(bits)
    require(1 <= bits <= 32, 'SAMPLE_BITS')
    require(type(signed) is bool, 'SIGNED_TYPE')
    require(type(samples) is list and len(samples) <= 64, 'SAMPLE_ARRAY')
    require(all(type(v) is int for v in samples), 'SAMPLE_TYPE')
    lower = -(1 << (bits-1)) if signed else 0
    upper = (1 << (bits-1))-1 if signed else (1 << bits)-1
    return {'lower': lower, 'upper': upper,
            'out_of_range_indices': [i for i, v in enumerate(samples) if not lower <= v <= upper],
            'rail_indices': [i for i, v in enumerate(samples) if v in (lower, upper)],
            'clipping_established': False}

def channel_permutation(r):
    fields(r, ['channels', 'order', 'frames'])
    channels, order, frames = r['channels'], r['order'], r['frames']
    require(type(channels) is list and 1 <= len(channels) <= 8 and
            all(type(v) is str and 1 <= len(v) <= 80 for v in channels), 'CHANNEL_LABELS')
    require(len(set(channels)) == len(channels), 'CHANNEL_LABELS')
    n = len(channels)
    require(type(order) is list and len(order) == n and all(type(v) is int for v in order)
            and sorted(order) == list(range(n)), 'PERMUTATION')
    require(type(frames) is list and len(frames) <= 64 and
            all(type(f) is list and len(f) == n for f in frames), 'FRAME_SHAPE')
    require(all(type(v) is int for f in frames for v in f), 'SAMPLE_TYPE')
    inverse = [0] * n
    for output_index, source_index in enumerate(order):
        inverse[source_index] = output_index
    return {'channels': [channels[i] for i in order],
            'frames': [[f[i] for i in order] for f in frames], 'inverse': inverse}

def edit_intervals(r):
    fields(r, ['source_frames', 'keep'])
    n, keep = r['source_frames'], r['keep']
    integers(n)
    require(0 <= n <= 10**12, 'SOURCE_FRAMES')
    require(type(keep) is list and len(keep) <= 64, 'SPAN_ARRAY')
    prior_end = 0
    output_pos = 0
    dropped = []
    mapping = []
    for span in keep:
        require(type(span) is list and len(span) == 2 and all(type(v) is int for v in span), 'SPAN_TYPE')
        start, end = span
        require(0 <= start < end <= n, 'SPAN_BOUNDS')
        require(start >= prior_end, 'SPAN_ORDER_OR_OVERLAP')
        if start > prior_end:
            dropped.append([prior_end, start])
        output_end = output_pos + end - start
        mapping.append([start, end, output_pos, output_end])
        output_pos = output_end
        prior_end = end
    if prior_end < n:
        dropped.append([prior_end, n])
    return {'output_frames': output_pos, 'dropped': dropped, 'mapping': mapping}

def segment_binding(r):
    fields(r, ['hex', 'start', 'end', 'source_sha256', 'segment_sha256'])
    raw = hex_bytes(r['hex'])
    start, end = r['start'], r['end']
    require(type(start) is int and type(end) is int, 'SPAN_TYPE')
    require(0 <= start <= end <= len(raw), 'SPAN_BOUNDS')
    for key in ['source_sha256', 'segment_sha256']:
        require(type(r[key]) is str and re.fullmatch(r'[0-9a-f]{64}', r[key]) is not None, 'DIGEST_SYNTAX')
    source_digest = hashlib.sha256(raw).hexdigest()
    segment_digest = hashlib.sha256(raw[start:end]).hexdigest()
    require(source_digest == r['source_sha256'], 'SOURCE_DIGEST_MISMATCH')
    require(segment_digest == r['segment_sha256'], 'SEGMENT_DIGEST_MISMATCH')
    return {'source_bytes': len(raw), 'segment_bytes': end-start,
            'source_sha256': source_digest, 'segment_sha256': segment_digest}

def restoration_claim(r):
    fields(r, ['source_kind', 'before', 'after', 'metric_before', 'metric_after', 'direction', 'independent_review'])
    require(r['source_kind'] == 'synthetic', 'REAL_AUDIO_AUTHORITY_REQUIRED')
    require(r['independent_review'] is False, 'EXTERNAL_REVIEW_REQUIRED')
    for key in ['before', 'after']:
        meta = r[key]
        require(type(meta) is dict and set(meta) == {'frames', 'rate', 'channels'}, 'COMPARISON_METADATA')
        require(all(type(v) is int for v in meta.values()) and meta['frames'] >= 0 and
                1 <= meta['rate'] <= 384000 and 1 <= meta['channels'] <= 8, 'COMPARISON_METADATA')
    require(r['before'] == r['after'], 'NOT_COMPARABLE')
    require(r['direction'] in ('lower', 'higher'), 'DIRECTION')
    require(r['metric_before'] is not None and r['metric_after'] is not None, 'MISSING_METRIC')
    delta = rational(r['metric_after']) - rational(r['metric_before'])
    return {'metric_delta': str(delta), 'better_in_fixture': delta < 0 if r['direction'] == 'lower' else delta > 0,
            'perceptual_effectiveness_established': False, 'independent_reproduction': False}

DISCLOSURE_REQUIRED = {
    'publish_audio': ['rights_holder', 'affected_people', 'privacy_review'],
    'publish_transcript': ['rights_holder', 'speaker_consent', 'privacy_review'],
    'identify_speaker': ['affected_people', 'competent_identity_review'],
    'determine_rights': ['competent_legal_authority', 'rights_holder'],
    'assign_maori_label': ['maori_authority', 'affected_people'],
    'release_maori_data': ['maori_data_governance', 'tangata_whenua_iwi_hapu'],
    'assert_tikanga': ['maori_authority'],
    'assert_taonga_status': ['maori_authority'],
    'claim_restoration_quality': ['preregistered_listener_evidence', 'independent_review'],
    'claim_accessibility_complete': ['affected_user_evaluation', 'assistive_technology_review'],
    'deploy_identity_service': ['production_keys_proofs', 'security_review', 'trust_governance'],
    'delete_source': ['exact_destructive_authority', 'recoverable_backup'],
    'change_shared_archive': ['archive_custodian', 'exact_shared_target'],
    'use_real_participants': ['governed_consent', 'safety_monitoring', 'competent_review'],
    'claim_gmut_confirmation': ['empirical_model_comparison', 'independent_review'],
    'promote_stage20': ['all_exact_external_gates', 'competent_affected_authority'],
}
LOCAL_ACTIONS = {'inspect_synthetic', 'plan_redaction', 'draft_access_summary', 'retain_private_source'}

def disclosure_gate(r):
    fields(r, ['action', 'source_kind', 'claimed_permissions'])
    action = r['action']
    require(type(action) is str and (action in LOCAL_ACTIONS or action in DISCLOSURE_REQUIRED), 'ACTION')
    require(r['source_kind'] == 'synthetic', 'REAL_AUDIO_AUTHORITY_REQUIRED')
    require(type(r['claimed_permissions']) is list and len(r['claimed_permissions']) <= 64 and
            all(type(v) is str and len(v) <= 100 for v in r['claimed_permissions']), 'PERMISSION_SHAPE')
    required = DISCLOSURE_REQUIRED.get(action, [])
    return {'action': action, 'disposition': 'exact_gate' if required else 'represented',
            'executed_external_action': False, 'required_authorities': list(required)}

OPERATIONS = {f.__name__: f for f in [riff_chunks, pcm_format, pcm_frames, sample_time, pcm_range,
                                    channel_permutation, edit_intervals, segment_binding,
                                    restoration_claim, disclosure_gate]}

def evaluate(record, allowed=None):
    try:
        require(type(record) is dict, 'RECORD_TYPE')
        operation = record.get('operation')
        require(type(operation) is str and operation in OPERATIONS, 'OPERATION')
        require(allowed is None or operation in allowed, 'OPERATION_SCOPE')
        value = OPERATIONS[operation](record)
        return {'accepted': True, 'value': value, 'error': None, 'external_credit': False}
    except Refusal as exc:
        return {'accepted': False, 'value': None, 'error': str(exc), 'external_credit': False}

def strict_load(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Refusal('DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def constant(_):
        raise Refusal('NONFINITE_JSON_CONSTANT')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)

def main(allowed=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path)
    args = ap.parse_args()
    try:
        require(args.input.stat().st_size <= 1048576, 'INPUT_BYTE_LIMIT')
        record = strict_load(args.input.read_text(encoding='utf-8'))
        result = evaluate(record, allowed)
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError, Refusal) as exc:
        code = str(exc) if isinstance(exc, Refusal) else type(exc).__name__
        result = {'accepted': False, 'value': None, 'error': code, 'external_credit': False}
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False))
    return 0 if result['accepted'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
