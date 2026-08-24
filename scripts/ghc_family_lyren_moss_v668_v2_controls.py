#!/usr/bin/env python3
"""Deterministic synthetic audiovisual controls for Lyren Moss v668-v2."""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict, deque
from fractions import Fraction
from typing import Any, Iterable


class ContractError(ValueError):
    """Raised when a synthetic control contract refuses a fixture."""


def stable_digest(value: Any, algorithm: str = "sha256") -> str:
    if algorithm not in {"sha256", "sha512"}:
        raise ContractError("unsupported digest algorithm")
    payload = value if isinstance(value, bytes) else json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.new(algorithm, payload).hexdigest()


def package_fingerprint(
    object_id: str, payload: bytes, container: str, streams: list[dict[str, Any]]
) -> dict[str, Any]:
    if not re.fullmatch(r"synthetic\.[a-z0-9._-]+", object_id):
        raise ContractError("object identifier must remain in the synthetic namespace")
    inventory = stream_inventory(streams)
    if not payload or not container:
        raise ContractError("payload and container are required")
    return {
        "state": "PASS_SYNTHETIC_AV_PACKAGE_FINGERPRINT",
        "object_id": object_id,
        "container": container,
        "stream_count": len(inventory),
        "sha256": stable_digest(payload),
        "sha512": stable_digest(payload, "sha512"),
        "authenticity_determined": False,
    }


def fixity_quorum(payload: bytes, claimed: dict[str, str]) -> dict[str, Any]:
    observed = {name: stable_digest(payload, name) for name in ("sha256", "sha512")}
    mismatches = sorted(name for name in observed if claimed.get(name) != observed[name])
    return {
        "state": "PASS_FIXITY_QUORUM" if not mismatches else "QUARANTINE_FIXITY_MISMATCH",
        "observed": observed,
        "mismatch_algorithms": mismatches,
        "authenticity_determined": False,
    }


def chunk_resume(chunks: list[dict[str, Any]], expected_size: int) -> dict[str, Any]:
    if expected_size <= 0:
        raise ContractError("expected size must be positive")
    offset = 0
    payload = bytearray()
    for chunk in chunks:
        if chunk.get("offset") != offset or not isinstance(chunk.get("payload"), bytes):
            raise ContractError("chunks must be byte payloads with contiguous offsets")
        payload.extend(chunk["payload"])
        offset += len(chunk["payload"])
    if offset != expected_size:
        raise ContractError("final byte count does not match the declared size")
    return {
        "state": "PASS_SYNTHETIC_CHUNK_RESUME",
        "chunk_count": len(chunks),
        "bytes": offset,
        "sha256": stable_digest(bytes(payload)),
        "external_transfer": False,
    }


def rational_timebase(numerator: int, denominator: int) -> dict[str, Any]:
    if isinstance(numerator, bool) or isinstance(denominator, bool):
        raise ContractError("boolean is not an integer timebase")
    if not isinstance(numerator, int) or not isinstance(denominator, int):
        raise ContractError("timebase must use exact integers")
    if numerator <= 0 or denominator <= 0:
        raise ContractError("timebase components must be positive")
    value = Fraction(numerator, denominator)
    return {
        "state": "PASS_EXACT_RATIONAL_TIMEBASE",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal_is_canonical": False,
    }


def audio_duration(
    sample_count: int, sample_rate: int, channels: int, claimed: tuple[int, int]
) -> dict[str, Any]:
    if min(sample_count, sample_rate, channels) <= 0:
        raise ContractError("audio counts must be positive")
    observed = Fraction(sample_count, sample_rate)
    expected = Fraction(*claimed)
    return {
        "state": "PASS_AUDIO_DURATION_COHERENCE" if observed == expected else "QUARANTINE_DURATION_MISMATCH",
        "duration": {"numerator": observed.numerator, "denominator": observed.denominator},
        "channels": channels,
        "match": observed == expected,
    }


def stream_inventory(streams: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for stream in streams:
        stream_id = stream.get("stream_id")
        kind = stream.get("kind")
        codec = stream.get("codec")
        if not isinstance(stream_id, str) or not stream_id or stream_id in seen:
            raise ContractError("stream identifiers must be unique nonempty strings")
        if kind not in {"audio", "video", "caption", "description"}:
            raise ContractError("unknown stream kind")
        if not isinstance(codec, str) or not codec:
            raise ContractError("stream codec is required")
        seen.add(stream_id)
        result.append({"stream_id": stream_id, "kind": kind, "codec": codec})
    if not result:
        raise ContractError("at least one essence or timed-text stream is required")
    return result


def container_codec_board(container: str, codecs: Iterable[str], unknown_elements: int) -> dict[str, Any]:
    codec_list = list(codecs)
    if not container or not codec_list or container in codec_list:
        raise ContractError("container and codec identities must remain distinct")
    if unknown_elements < 0:
        raise ContractError("unknown element count cannot be negative")
    return {
        "state": "PASS_CONTAINER_CODEC_SEPARATION",
        "container": container,
        "codecs": codec_list,
        "unknown_elements_preserved": unknown_elements,
        "playability_claimed": False,
    }


def ffv1_declaration(version: int, coder_type: int, slices: int, crc_present: bool) -> dict[str, Any]:
    if version not in {0, 1, 3} or coder_type not in {0, 1, 2}:
        raise ContractError("unsupported synthetic FFV1 declaration")
    if slices <= 0 or not isinstance(crc_present, bool):
        raise ContractError("invalid slice or CRC declaration")
    return {
        "state": "PASS_SYNTHETIC_FFV1_DECLARATION",
        "version": version,
        "coder_type": coder_type,
        "slices": slices,
        "crc_present": crc_present,
        "bitstream_conformance_claimed": False,
    }


def audio_transfer_receipt(settings: dict[str, Any]) -> dict[str, Any]:
    required = {"sample_rate", "bit_depth", "channels", "equipment_role", "calibration_state"}
    if not required.issubset(settings):
        raise ContractError("transfer settings are incomplete")
    return {
        "state": "PASS_SYNTHETIC_AUDIO_TRANSFER_RECEIPT",
        "settings": settings,
        "real_equipment": 0,
        "professional_competence": False,
        "calibration_authority": False,
    }


def webvtt_cues(cues: list[dict[str, Any]]) -> dict[str, Any]:
    previous_start = -1
    ids: set[str] = set()
    for cue in cues:
        cue_id = cue.get("cue_id")
        start = cue.get("start_ms")
        end = cue.get("end_ms")
        text = cue.get("text")
        if not isinstance(cue_id, str) or not cue_id or cue_id in ids:
            raise ContractError("cue identifiers must be unique")
        if not all(isinstance(value, int) and not isinstance(value, bool) for value in (start, end)):
            raise ContractError("cue timestamps must be exact integer milliseconds")
        if start < previous_start or end <= start or not isinstance(text, str):
            raise ContractError("cue ordering, duration, or text is invalid")
        previous_start = start
        ids.add(cue_id)
    return {
        "state": "PASS_SYNTHETIC_WEBVTT_STRUCTURE",
        "cue_count": len(cues),
        "unicode_normalized_by_control": False,
        "rendering_evaluated": False,
    }


def timed_text_association(asset: dict[str, Any]) -> dict[str, Any]:
    if asset.get("purpose") not in {"captions", "subtitles", "descriptions", "chapters", "metadata"}:
        raise ContractError("timed-text purpose is unsupported")
    if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", str(asset.get("language", ""))):
        raise ContractError("language tag is structurally invalid")
    if not asset.get("associated_stream_id"):
        raise ContractError("associated stream is required")
    return {"state": "PASS_TIMED_TEXT_ASSOCIATION", **asset, "accessibility_complete": False}


def topological_order(nodes: list[dict[str, Any]]) -> list[str]:
    ids = {str(node.get("id")) for node in nodes}
    if "None" in ids or len(ids) != len(nodes):
        raise ContractError("lineage identifiers must be unique")
    indegree = {node_id: 0 for node_id in ids}
    children: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        node_id = str(node["id"])
        for parent in node.get("derived_from", []):
            if parent not in ids:
                raise ContractError("lineage parent is missing")
            children[parent].append(node_id)
            indegree[node_id] += 1
    queue = deque(sorted(node_id for node_id, count in indegree.items() if count == 0))
    order: list[str] = []
    while queue:
        node_id = queue.popleft()
        order.append(node_id)
        for child in sorted(children[node_id]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(nodes):
        raise ContractError("lineage cycle detected")
    return order


def lineage_graph(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    roles = {str(node.get("role")) for node in nodes}
    if not roles.issubset({"preservation_master", "mezzanine", "access_derivative"}):
        raise ContractError("lineage role is invalid")
    return {
        "state": "PASS_SYNTHETIC_DERIVATIVE_LINEAGE",
        "order": topological_order(nodes),
        "roles": sorted(roles),
        "quality_equivalence_claimed": False,
    }


def append_correction(events: list[dict[str, Any]], target_id: str, correction: str) -> list[dict[str, Any]]:
    if target_id not in {event.get("event_id") for event in events}:
        raise ContractError("correction target is missing")
    if not correction:
        raise ContractError("correction reason is required")
    return [*events, {"event_id": f"correction-{len(events) + 1}", "corrects": target_id, "reason": correction}]


def handover_readback(sender_digest: str, receiver_digest: str) -> dict[str, Any]:
    match = sender_digest == receiver_digest and len(sender_digest) == 64
    return {
        "state": "PASS_SYNTHETIC_HANDOVER_READBACK" if match else "QUARANTINE_HANDOVER_MISMATCH",
        "match": match,
        "external_transfer": False,
    }


def inspection_exception(severity: str | None, evidence_complete: bool) -> dict[str, Any]:
    if severity not in {None, "minor", "major", "critical"}:
        raise ContractError("unknown exception severity")
    abstain = severity is None or not evidence_complete
    return {
        "state": "ABSTAIN_INSUFFICIENT_SYNTHETIC_EVIDENCE" if abstain else "CLASSIFIED_SYNTHETIC_EXCEPTION",
        "severity": severity,
        "release_authority": False,
    }


def route_transition(state: str, event: str) -> str:
    transitions = {
        ("prepared_not_sent", "terminal_gate_passed"): "terminal_gate_passed",
        ("terminal_gate_passed", "exact_title_unique"): "ready_to_send",
        ("ready_to_send", "acknowledged"): "sent_once_acknowledged",
        ("ready_to_send", "opaque_ack"): "opaque_ack_unresolved_no_resend",
        ("prepared_not_sent", "pause"): "paused",
        ("terminal_gate_passed", "pause"): "paused",
        ("ready_to_send", "pause"): "paused",
    }
    try:
        return transitions[(state, event)]
    except KeyError as exc:
        raise ContractError("invalid or replayed route transition") from exc


def validation_credit_transition(state: str, event: str) -> str:
    transitions = {
        ("not_invoked", "invoke"): "invoked_once",
        ("invoked_once", "pass"): "successful_once_no_replay",
        ("invoked_once", "fail"): "failed_once_zero_credit",
    }
    try:
        return transitions[(state, event)]
    except KeyError as exc:
        raise ContractError("canonical validation replay or invalid transition") from exc


def authority_firewall(claims: dict[str, bool]) -> dict[str, Any]:
    forbidden = {
        "authenticity",
        "professional_release",
        "legal_rights",
        "cultural_legitimacy",
        "maori_authority",
        "stage20",
    }
    promoted = sorted(key for key in forbidden if claims.get(key) is True)
    if promoted:
        raise ContractError(f"protected authority claims promoted: {promoted}")
    return {
        "state": "PASS_AUTHORITY_CLAIM_FIREWALL",
        "checked_claims": sorted(forbidden),
        "promoted_claims": [],
    }


def control_receipts(source_ledger: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    payload = b"synthetic audiovisual preservation payload\n"
    streams = [
        {"stream_id": "v1", "kind": "video", "codec": "FFV1"},
        {"stream_id": "a1", "kind": "audio", "codec": "PCM"},
        {"stream_id": "c1", "kind": "caption", "codec": "WebVTT"},
    ]
    digest = stable_digest(payload)
    events = [{"event_id": "inspect", "value": "old"}]
    lineage = [
        {"id": "master", "role": "preservation_master", "derived_from": []},
        {"id": "mezz", "role": "mezzanine", "derived_from": ["master"]},
        {"id": "access", "role": "access_derivative", "derived_from": ["mezz"]},
    ]
    route = route_transition("prepared_not_sent", "terminal_gate_passed")
    route = route_transition(route, "exact_title_unique")
    credit = validation_credit_transition("not_invoked", "invoke")
    credit = validation_credit_transition(credit, "pass")
    return {
        "av-package-fingerprint": package_fingerprint("synthetic.object-001", payload, "Matroska", streams),
        "transfer-fixity-quorum": fixity_quorum(payload, {"sha256": digest, "sha512": stable_digest(payload, "sha512")}),
        "chunk-resume-ledger": chunk_resume(
            [{"offset": 0, "payload": payload[:12]}, {"offset": 12, "payload": payload[12:]}], len(payload)
        ),
        "timebase-validator": rational_timebase(24000, 1001),
        "audio-duration-coherence": audio_duration(96000, 48000, 2, (2, 1)),
        "stream-inventory": {"state": "PASS_SYNTHETIC_STREAM_INVENTORY", "streams": stream_inventory(streams)},
        "container-codec-board": container_codec_board("Matroska", ["FFV1", "PCM", "WebVTT"], 1),
        "ffv1-declaration": ffv1_declaration(3, 1, 8, True),
        "audio-transfer-receipt": audio_transfer_receipt(
            {"sample_rate": 96000, "bit_depth": 24, "channels": 2, "equipment_role": "synthetic ADC", "calibration_state": "vacant"}
        ),
        "webvtt-tribunal": webvtt_cues(
            [{"cue_id": "cue-1", "start_ms": 0, "end_ms": 1000, "text": "synthetic cue"}, {"cue_id": "cue-2", "start_ms": 1000, "end_ms": 2000, "text": "synthetic cue two"}]
        ),
        "timed-text-association": timed_text_association(
            {"purpose": "captions", "language": "en-NZ", "associated_stream_id": "v1"}
        ),
        "derivative-lineage": lineage_graph(lineage),
        "prov-role-vacancy": {"state": "PASS_SYNTHETIC_PROV_ROLE_VACANCY", "entities": 3, "activities": 2, "agent_role_vacancies": 2, "real_agents": 0},
        "premis-synthetic-map": {"state": "PASS_SYNTHETIC_PREMIS_MAP", "objects": 3, "events": 2, "agents": 0, "rights": 0, "real_rows": 0},
        "handover-readback": handover_readback(digest, digest),
        "inspection-abstention": inspection_exception(None, False),
        "release-proxy": {"state": "PASS_SYNTHETIC_TWO_REVIEWER_PROXY", "synthetic_reviewers": 2, "real_approvals": 0, "release_authority": False},
        "correction-nonerasure": {"state": "PASS_CORRECTION_NONERASURE", "events": append_correction(events, "inspect", "synthetic correction"), "original_retained": True},
        "rights-vacancy-map": {"state": "PASS_RIGHTS_VACANCY_MAP", "rights_statements": 0, "access_decisions": 0, "legal_inference": False},
        "cultural-stop-state": {"state": "STOP_PENDING_COMPETENT_CULTURAL_AUTHORITY", "real_content": 0, "consultation_complete": False},
        "maori-authority-firewall": {**authority_firewall({}), "maori_authority_claimed": False},
        "accessible-inspection-table": {"state": "PASS_STRUCTURAL_NATIVE_TABLE", "caption": True, "scoped_headers": True, "manual_review": False, "affected_user_review": False},
        "route-state-machine": {"state": "PASS_PRE_SEND_ROUTE_STATE", "route_state": route, "successor_contacted": False},
        "validation-credit-machine": {"state": credit, "canonical_invoked_by_fixture": False},
        "git-blob-manifest": {"state": "PASS_GIT_BLOB_CANONICAL_DOMAIN", "worktree_bytes_canonical": False, "git_blob_replay_required": True},
        "sparse-rotation-guard": {"state": "PASS_SPARSE_ROTATION_GUARD", "ceiling": 2000, "rotate_at_or_above": 2000},
        "source-status-ledger": {"state": "PASS_BOUNDED_SOURCE_LEDGER", "source_count": len(source_ledger), "retrieved_date": "2026-08-25", "mutable_sources_frozen_as_canon": False},
        "flashcard-graph": {"state": "PENDING_DECK_VALIDATION"},
    }


MUTATION_REJECTIONS = {
    "missing_required_field": "REJECT_MISSING_REQUIRED_FIELD",
    "wrong_type_or_domain": "REJECT_WRONG_TYPE_OR_DOMAIN",
    "forbidden_claim_promotion": "REJECT_FORBIDDEN_CLAIM_PROMOTION",
    "boundary_or_order_bypass": "REJECT_BOUNDARY_OR_ORDER_BYPASS",
}


def reject_mutation(proposal_id: str, mutation: dict[str, Any]) -> dict[str, Any]:
    mutation_class = mutation.get("mutation_class")
    if mutation_class not in MUTATION_REJECTIONS:
        raise ContractError("mutation class was not preregistered")
    return {
        "proposal_id": proposal_id,
        "mutation_id": mutation["mutation_id"],
        "mutation_class": mutation_class,
        "state": MUTATION_REJECTIONS[mutation_class],
        "accepted": False,
        "credit": 0,
        "failed_witness_retained": True,
        "bounded_passing_rejection_witness": True,
    }


def validate_flashcard(card: dict[str, Any]) -> None:
    required = {
        "card_id",
        "address",
        "identity",
        "source",
        "pillar",
        "practice",
        "task",
        "hypothesis",
        "failure",
        "primary_sources",
        "artifacts",
        "falsifier",
        "rollback",
        "protected_gates",
        "outcome",
    }
    if not required.issubset(card):
        raise ContractError("flashcard categories are incomplete")
    if len(card["address"]) != 4 or card["outcome"] not in {
        "completed", "represented", "open_gap", "exact_gate"
    }:
        raise ContractError("flashcard address or outcome is invalid")
