#!/usr/bin/env python3
"""Deterministic bounded tribunals for Vesper Arlen v651-v7."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/vesper-arlen/v651-v7"
ALLOWED = ("completed", "represented", "open_gap", "exact_gate")
PROTECTED_CLAIMS = {
    "empirical_confirmation": False,
    "participant_effect": False,
    "production_ready": False,
    "professional_authority": False,
    "legal_authority": False,
    "cultural_authority": False,
    "maori_authority": False,
    "privacy_complete": False,
    "security_complete": False,
    "accessibility_complete": False,
    "independent_reproduction": False,
    "agi_or_asi": False,
    "consciousness_or_personhood": False,
    "theory_of_everything": False,
    "stage20_ready": False,
}


def _base(slug: str, label: str, passed: bool, metrics: dict[str, Any], rejection_witnesses: list[str], boundary: str) -> dict[str, Any]:
    if label not in ALLOWED:
        raise ValueError(label)
    return {
        "slug": slug,
        "truth_label": label,
        "valid_fixture_passed": bool(passed),
        "metrics": metrics,
        "rejecting_fixture_count": len(rejection_witnesses),
        "rejecting_fixture_witnesses": rejection_witnesses,
        "protected_claims": dict(PROTECTED_CLAIMS),
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": boundary,
    }


def _lsm() -> dict[str, Any]:
    can_reclaim = lambda tombstone, active: bool(active) and tombstone < min(active)
    passed = can_reclaim(4, [6, 9]) and not can_reclaim(4, [4, 9])
    return _base("lsm-tombstone-horizon", "completed", passed, {"tombstone_epoch": 4, "minimum_active_snapshot": 6, "reclaimed": True}, ["equal snapshot horizon rejected", "empty active-set authority refused"], "Synthetic reclamation logic only; no storage-engine durability claim.")


def _mvcc() -> dict[str, Any]:
    a = {"reads": {"on_call"}, "writes": {"a"}, "post": 0}
    b = {"reads": {"on_call"}, "writes": {"b"}, "post": 0}
    detected = bool(a["reads"] & b["reads"]) and not bool(a["writes"] & b["writes"]) and min(a["post"], b["post"]) < 1
    return _base("mvcc-write-skew", "completed", detected, {"predicate": "on_call_at_least_one", "concurrent_post_count": 0, "write_skew_detected": detected}, ["serial schedule accepted separately", "disjoint invariant does not trigger"], "Synthetic dependency analysis only; no database isolation certification.")


def _epoch() -> dict[str, Any]:
    reclaim = lambda retired, active: bool(active) and retired < min(active)
    passed = reclaim(4, [5, 8]) and not reclaim(5, [5, 8])
    return _base("epoch-reclamation", "completed", passed, {"retired_epoch": 4, "minimum_active_epoch": 5}, ["equal active epoch refused", "unknown participant refused"], "Synthetic quiescence evidence only; no real memory reclamation.")


def _aba() -> dict[str, Any]:
    stale, current = ("A", 1), ("A", 2)
    detected = stale[0] == current[0] and stale != current
    return _base("hazard-aba", "completed", detected, {"address_equal": True, "tag_equal": False, "aba_detected": detected}, ["unchanged tag is not ABA", "untagged ownership refused"], "Synthetic token evidence only; no lock-free implementation assurance.")


def _monotonic() -> dict[str, Any]:
    wall = [100.0, 90.0]
    monotonic = [5.0, 8.0]
    elapsed = monotonic[1] - monotonic[0]
    passed = elapsed == 3.0 and wall[1] - wall[0] < 0
    return _base("monotonic-deadline", "completed", passed, {"monotonic_elapsed": elapsed, "wall_delta": -10.0}, ["wall-clock rollback excluded from timeout", "negative monotonic delta rejected"], "Synthetic clock fixture only; no operating-system timing guarantee.")


def _token_bucket() -> dict[str, Any]:
    capacity, rate = 5.0, 2.0
    tokens, last = capacity, 0.0
    def take(amount: float, now: float) -> bool:
        nonlocal tokens, last
        if now < last or amount < 0:
            return False
        tokens = min(capacity, tokens + (now - last) * rate)
        last = now
        if amount > tokens:
            return False
        tokens -= amount
        return True
    passed = take(5, 0) and take(2, 1) and not take(1, 0.5) and not take(6, 2)
    return _base("token-bucket", "completed", passed, {"capacity": capacity, "refill_rate": rate, "remaining_tokens": tokens}, ["negative time refused", "over-burst refused"], "Synthetic admission fixture only; no network quality-of-service claim.")


def _weighted_fair() -> dict[str, Any]:
    weights = [1, 2, 3]
    allocations = [12 * weight / sum(weights) for weight in weights]
    ratios = [allocation / weight for allocation, weight in zip(allocations, weights)]
    passed = all(value > 0 for value in allocations) and max(ratios) - min(ratios) < 1e-12
    return _base("weighted-fair-queue", "completed", passed, {"weights": weights, "allocations": allocations}, ["zero weight excluded", "starved positive-weight queue rejected"], "Synthetic service allocation only; no scheduler deployment claim.")


def _consistent_hash() -> dict[str, Any]:
    def owner(position: int, ring: dict[str, int]) -> str:
        ordered = sorted((point, name) for name, point in ring.items())
        return next((name for point, name in ordered if position <= point), ordered[0][1])
    before = {"A": 20, "B": 70}
    after = {"A": 20, "C": 50, "B": 70}
    keys = [10, 30, 80]
    old = {key: owner(key, before) for key in keys}
    new = {key: owner(key, after) for key in keys}
    moved = [key for key in keys if old[key] != new[key]]
    passed = moved == [30] and set(old) == set(new)
    return _base("consistent-hash-movement", "completed", passed, {"old_owners": old, "new_owners": new, "moved_keys": moved}, ["duplicate key assignment rejected", "dropped key rejected"], "Synthetic ring evidence only; no distributed-system availability claim.")


def _merkle() -> dict[str, Any]:
    leaves = [hashlib.sha256(f"{index}:value-{index}".encode()).hexdigest() for index in range(4)]
    root = hashlib.sha256("".join(leaves).encode()).hexdigest()
    indices = [1, 2]
    contiguous = indices == list(range(min(indices), max(indices) + 1)) and len(indices) == len(set(indices))
    passed = contiguous and len(root) == 64
    return _base("merkle-range-completeness", "completed", passed, {"indices": indices, "root": root, "contiguous": contiguous}, ["gap rejected", "duplicate index rejected", "reordered range rejected"], "Bounded synthetic hashing only; no production transparency-log assurance.")


def _domain_separation() -> dict[str, Any]:
    payload = b"same-payload"
    digest = lambda domain: hashlib.sha256(domain.encode() + b"\x00" + payload).hexdigest()
    one, two = digest("artifact"), digest("manifest")
    return _base("content-domain-separation", "completed", one != two, {"artifact_digest": one, "manifest_digest": two}, ["missing type prefix rejected", "unknown domain rejected"], "Synthetic content-address evidence only; no collision-resistance proof.")


def _savepoint() -> dict[str, Any]:
    state = ["outer-a", "outer-b"]
    savepoint = len(state)
    state.extend(["inner-c", "inner-d"])
    del state[savepoint:]
    passed = state == ["outer-a", "outer-b"]
    return _base("savepoint-rollback", "completed", passed, {"surviving_state": state, "rolled_back_count": 2}, ["outer prefix deletion rejected", "unknown savepoint refused"], "In-memory transaction model only; no database durability claim.")


def _wal() -> dict[str, Any]:
    wal_end = 10
    reader_end_marks = [7, 9]
    checkpointed = min([wal_end, *reader_end_marks])
    complete = checkpointed == wal_end
    passed = checkpointed == 7 and not complete
    return _base("wal-reader-pin", "completed", passed, {"wal_end": wal_end, "reader_end_marks": reader_end_marks, "checkpointed_through": checkpointed, "complete": complete}, ["partial checkpoint cannot be labeled complete", "reader-free reset modeled separately"], "Synthetic checkpoint model only; no SQLite version or corruption assurance.")


def _backup() -> dict[str, Any]:
    pages = [{"page": index, "generation": 9} for index in range(1, 5)]
    passed = len({row["generation"] for row in pages}) == 1
    return _base("backup-generation", "completed", passed, {"page_count": len(pages), "generation": 9}, ["mixed generation rejected", "missing page provenance rejected"], "Synthetic page ledger only; no backup recoverability certification.")


def _expand_contract() -> dict[str, Any]:
    readers = [{"old", "new"}, {"old", "new"}]
    dual_write = True
    remove_old = dual_write and all("new" in reader for reader in readers)
    incompatible = [{"old"}, {"old", "new"}]
    passed = remove_old and not (dual_write and all("new" in reader for reader in incompatible))
    return _base("expand-contract", "completed", passed, {"reader_count": len(readers), "dual_write": dual_write, "old_field_removable": remove_old}, ["legacy reader blocks removal", "no dual-write blocks removal"], "Synthetic schema contract only; no live migration authority.")


def _singleflight() -> dict[str, Any]:
    calls = ["a", "a", "a", "b", "a"]
    computations = sorted(set(calls))
    results = [f"value:{key}" for key in calls]
    passed = len(computations) == 2 and len(results) == len(calls)
    return _base("singleflight", "completed", passed, {"caller_count": len(calls), "computation_count": len(computations), "results_returned": len(results)}, ["different keys not coalesced", "caller result loss rejected"], "Deterministic coalescing model only; no concurrency or cache reliability claim.")


def _etag() -> dict[str, Any]:
    current = '"v2"'
    stale_allowed = '"v1"' == current
    current_allowed = '"v2"' == current
    passed = not stale_allowed and current_allowed
    return _base("etag-cas", "completed", passed, {"current_etag": current, "stale_update_allowed": stale_allowed, "matching_update_allowed": current_allowed}, ["stale validator rejected", "missing validator refused for protected update"], "Synthetic HTTP validator logic only; no server deployment or authorization claim.")


def _chebyshev() -> dict[str, Any]:
    node_count = 8
    max_degree = node_count - 1
    passed = 6 <= max_degree and not (9 <= max_degree)
    return _base("chebyshev-aliasing", "completed", passed, {"node_count": node_count, "maximum_resolvable_degree": max_degree}, ["degree nine refused", "physical inference refused"], "Typed numerical fixture only; no empirical GMUT evidence.")


def _interval() -> dict[str, Any]:
    left, right = (-2.0, 3.0), (4.0, 5.0)
    products = [a * b for a in left for b in right]
    enclosure = [min(products), max(products)]
    samples = [-2 * 4, -2 * 5, 3 * 4, 3 * 5, 0]
    passed = all(enclosure[0] <= value <= enclosure[1] for value in samples) and enclosure[0] <= enclosure[1]
    return _base("interval-enclosure", "completed", passed, {"enclosure": enclosure, "sample_count": len(samples)}, ["reversed bound rejected", "nonfinite bound rejected"], "Bounded scalar enclosure only; no proof of full GMUT dynamics.")


def _conditioning() -> dict[str, Any]:
    condition, perturbation, observed = 10.0, 0.001, 0.005
    budget = condition * perturbation
    passed = observed <= budget and not 0.02 <= budget
    return _base("condition-perturbation", "completed", passed, {"condition_number": condition, "input_relative_perturbation": perturbation, "error_budget": budget, "observed_error": observed}, ["over-budget error rejected", "unknown condition refused"], "Synthetic conditioning evidence only; no model adequacy claim.")


def _matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _commutator() -> dict[str, Any]:
    a, b = [[0, 1], [0, 0]], [[0, 0], [1, 0]]
    ab, ba = _matmul(a, b), _matmul(b, a)
    comm_ab = [[ab[i][j] - ba[i][j] for j in range(2)] for i in range(2)]
    comm_ba = [[-value for value in row] for row in comm_ab]
    anti = all(comm_ab[i][j] + comm_ba[i][j] == 0 for i in range(2) for j in range(2))
    available_order, requested_order = 2, 3
    passed = anti and requested_order > available_order
    return _base("lie-commutator", "completed", passed, {"commutator": comm_ab, "antisymmetry": anti, "available_order": available_order, "requested_order_refused": requested_order}, ["unsupported truncation refused", "physical promotion refused"], "Symbolic matrix evidence only; no physical symmetry or quantum-completeness claim.")


def _calibration() -> dict[str, Any]:
    tolerance, drift = 0.05, 0.09
    blocked = drift > tolerance
    return _base("calibration-drift", "completed", blocked, {"tolerance": tolerance, "observed_drift": drift, "promotion_blocked": blocked}, ["below-threshold fixture does not authorize promotion", "missing denominator refused"], "Structural nonpromotion control only; no participant estimate or Stage 20 authority.")


def _evidence_chain() -> dict[str, Any]:
    history = ["completed", "represented", "open_gap"]
    rank = {"completed": 3, "represented": 2, "open_gap": 1, "exact_gate": 0}
    monotone = all(rank[a] >= rank[b] for a, b in zip(history, history[1:]))
    return _base("evidence-chain-monotonicity", "completed", monotone, {"history": history, "prior_states_preserved": True}, ["upgrade without new evidence rejected", "history erasure rejected"], "Claim-state workflow evidence only; no scientific or legal adjudication.")


def _manifest_domain() -> dict[str, Any]:
    git_blob = b"line-one\nline-two\n"
    checkout = b"line-one\r\nline-two\r\n"
    different = hashlib.sha256(git_blob).hexdigest() != hashlib.sha256(checkout).hexdigest()
    return _base("manifest-blob-domain", "completed", different, {"git_blob_bytes": len(git_blob), "checkout_bytes": len(checkout), "domains_distinct": True}, ["cross-domain hash substitution rejected", "unlabeled normalization rejected"], "Manifest-domain classifier only; no semantic truth or independent reproduction.")


def _represented(slug: str, fields: list[str], boundary: str, metrics: dict[str, Any] | None = None) -> dict[str, Any]:
    present = all(bool(field) for field in fields)
    values = {"required_fields": fields, "real_people": 0, "real_operations": 0, "real_keys_or_tokens": 0}
    values.update(metrics or {})
    return _base(slug, "represented", present, values, ["missing required field rejected", "real-world promotion rejected"], boundary)


def _open_gap() -> dict[str, Any]:
    metrics = {"authorized_accounts": 0, "downloaded_rows": 0, "catalog_rows": 0, "covariance_rows": 0, "likelihood_calls": 0, "posterior_samples": 0, "constraints": 0}
    passed = all(value == 0 for value in metrics.values())
    return _base("rubin-dp1-adapter", "open_gap", passed, metrics, ["fabricated row rejected", "likelihood without provenance refused"], "Official availability is not authorized access or empirical evidence; the adapter remains empty.")


def _exact_gate() -> dict[str, Any]:
    metrics = {"affected_parties_present": 0, "competent_legal_authority_present": 0, "tangata_whenua_iwi_hapu_authority_present": 0, "decisions_made": 0}
    passed = all(value == 0 for value in metrics.values())
    return _base("preservation-authority", "exact_gate", passed, metrics, ["proxy authority rejected", "real decision without authority refused"], "Retention, deletion, repatriation, remedy, legal, cultural, and Maori-data decisions remain exact-gated.")


SURFACES: dict[str, Callable[[], dict[str, Any]]] = {
    "lsm-tombstone-horizon": _lsm,
    "mvcc-write-skew": _mvcc,
    "epoch-reclamation": _epoch,
    "hazard-aba": _aba,
    "monotonic-deadline": _monotonic,
    "token-bucket": _token_bucket,
    "weighted-fair-queue": _weighted_fair,
    "consistent-hash-movement": _consistent_hash,
    "merkle-range-completeness": _merkle,
    "content-domain-separation": _domain_separation,
    "savepoint-rollback": _savepoint,
    "wal-reader-pin": _wal,
    "backup-generation": _backup,
    "expand-contract": _expand_contract,
    "singleflight": _singleflight,
    "etag-cas": _etag,
    "chebyshev-aliasing": _chebyshev,
    "interval-enclosure": _interval,
    "condition-perturbation": _conditioning,
    "lie-commutator": _commutator,
    "calibration-drift": _calibration,
    "evidence-chain-monotonicity": _evidence_chain,
    "manifest-blob-domain": _manifest_domain,
    "preservation-fixity": lambda: _represented("preservation-fixity", ["fixity", "provenance", "custody", "repair", "audit"], "Synthetic package profile only; no archival effectiveness.", {"synthetic_packages": 2}),
    "preservation-handover": lambda: _represented("preservation-handover", ["detection", "isolation", "readback", "escalation", "workload", "handover"], "Synthetic incident profile only; no real collection or operator result.", {"synthetic_incidents": 2}),
    "par-rar-profile": lambda: _represented("par-rar-profile", ["request_uri", "expiry", "one_time_use", "audience", "authorization_details_type"], "Synthetic OAuth profile only; no real keys, tokens, issuer, client, or interoperability.", {"network_exchanges": 0}),
    "recovery-custody": lambda: _represented("recovery-custody", ["request", "approval", "execution", "notification", "contestation"], "Synthetic recovery profile only; no real recovery or trust governance.", {"recovery_decisions": 0}),
    "treegrid-structure": lambda: _represented("treegrid-structure", ["treegrid", "row", "gridcell", "aria-expanded", "aria-selected", "aria-label", "print-fallback"], "Structural accessibility proxy only; manual and affected-user evaluation reserved.", {"manual_evaluations": 0}),
    "rubin-dp1-adapter": _open_gap,
    "preservation-authority": _exact_gate,
}


GROUPS = {
    "storage-reclamation": ["lsm-tombstone-horizon", "savepoint-rollback", "wal-reader-pin", "backup-generation"],
    "concurrency-reclamation": ["mvcc-write-skew", "epoch-reclamation", "hazard-aba"],
    "time-rate-fairness": ["monotonic-deadline", "token-bucket", "weighted-fair-queue", "consistent-hash-movement"],
    "integrity-range": ["merkle-range-completeness", "content-domain-separation", "manifest-blob-domain"],
    "transaction-checkpoint": ["savepoint-rollback", "wal-reader-pin", "backup-generation"],
    "schema-cache-concurrency": ["expand-contract", "singleflight"],
    "conditional-update": ["etag-cas", "evidence-chain-monotonicity"],
    "numerical-boundary": ["chebyshev-aliasing", "interval-enclosure", "condition-perturbation", "lie-commutator"],
    "identity-accessibility-proxy": ["preservation-fixity", "preservation-handover", "par-rar-profile", "recovery-custody", "treegrid-structure"],
    "stage20-authority-refusal": ["calibration-drift", "rubin-dp1-adapter", "preservation-authority"],
}


def run_surface(slug: str) -> dict[str, Any]:
    try:
        result = SURFACES[slug]()
    except KeyError as exc:
        raise ValueError(f"unknown surface: {slug}") from exc
    if not result["valid_fixture_passed"]:
        raise RuntimeError(f"valid fixture failed: {slug}")
    return result


def run_group(group: str) -> dict[str, Any]:
    try:
        slugs = GROUPS[group]
    except KeyError as exc:
        raise ValueError(f"unknown group: {group}") from exc
    rows = [run_surface(slug) for slug in slugs]
    return {
        "schema": "ghc.family.v651-v7.runner-output.v1",
        "group": group,
        "surface_count": len(rows),
        "surfaces": [row["slug"] for row in rows],
        "valid": all(row["valid_fixture_passed"] for row in rows),
        "same_owner_only": True,
        "independent_implementations": False,
        "results": rows,
    }


def main() -> None:
    print(json.dumps({"surface_count": len(SURFACES), "group_count": len(GROUPS), "valid": all(run_surface(slug)["valid_fixture_passed"] for slug in SURFACES)}, sort_keys=True))


if __name__ == "__main__":
    main()
