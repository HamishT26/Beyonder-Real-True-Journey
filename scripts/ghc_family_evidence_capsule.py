"""Portable evidence capsules for a bounded, explicitly declared owner scope.

Byte parity and structural checks do not establish authority or independent
reproduction. No command contacts a task, modifies Git history, or installs tools.
"""
from __future__ import annotations

import argparse
import codecs
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

DOMAINS = {"raw_bytes_v1", "raw_git_blob_v1", "utf8_crlf_to_lf_v1"}
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
SECTIONS = [
    "identity-and-corrigibility", "route-and-authority", "source-anchors",
    "x1-proposals", "trinity-pillars", "bounded-practices", "task-cards",
    "method-flow-and-negatives", "open-and-exact-gates", "validation-and-manifests",
    "wellbeing-and-workload", "successor-recommendations", "compact-baton-index",
]
BOUNDARY = (
    "Same-owner software evidence only. Manual browser, assistive-technology, "
    "cognitive, language, and affected-user accessibility evaluation remains "
    "reserved. No empirical, professional, production, independent-reproduction, "
    "identity, legal, cultural, Maori-authority, complete privacy or accessibility, "
    "exhaustive security, Theory-of-Everything, canon, or Stage 20 claim."
)


class CapsuleError(ValueError):
    """Stable public error codes avoid copying private paths into receipts."""


def need(condition, code):
    if not condition:
        raise CapsuleError(code)


def strict_json(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            need(k not in result, "duplicate_json_key")
            result[k] = v
        return result

    def constant(_):
        raise CapsuleError("nonfinite_json_number")

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CapsuleError("invalid_json_encoding_or_syntax") from exc


def json_bytes(value):
    try:
        return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                           indent=2, allow_nan=False) + "\n").encode("utf-8")
    except (ValueError, TypeError, UnicodeError) as exc:
        raise CapsuleError("unserializable_strict_json") from exc


def normalized_chunks(chunks, domain):
    need(domain in DOMAINS, "unknown_byte_domain")
    decoder = codecs.getincrementaldecoder("utf-8")("strict")
    pending = b""
    for chunk in chunks:
        need(type(chunk) is bytes, "nonbyte_chunk")
        if domain != "utf8_crlf_to_lf_v1":
            yield chunk
            continue
        try:
            decoder.decode(chunk, final=False)
        except UnicodeError as exc:
            raise CapsuleError("invalid_utf8_text_domain") from exc
        block = pending + chunk
        pending = b"\r" if block.endswith(b"\r") else b""
        if pending:
            block = block[:-1]
        yield block.replace(b"\r\n", b"\n")
    if domain == "utf8_crlf_to_lf_v1":
        try:
            decoder.decode(b"", final=True)
        except UnicodeError as exc:
            raise CapsuleError("invalid_utf8_text_domain") from exc
        if pending:
            yield pending


def digest_stream(chunks, domain):
    h = hashlib.sha256()
    size = 0
    for chunk in normalized_chunks(chunks, domain):
        h.update(chunk)
        size += len(chunk)
    return {"byte_domain": domain, "bytes": size, "sha256": h.hexdigest()}


def portable_path(value):
    need(isinstance(value, str) and bool(value), "empty_path")
    need(unicodedata.normalize("NFC", value) == value, "non_nfc_path")
    need("\\" not in value, "backslash_path")
    need(not any(ch in value for ch in '*?[]<>"|'), "pathspec_or_windows_character")
    need(not value.startswith("/") and ":" not in value, "absolute_or_drive_path")
    need(not any(ord(c) < 32 or ord(c) == 127 for c in value), "control_in_path")
    parts = value.split("/")
    need(all(p not in {"", ".", ".."} for p in parts), "dot_or_empty_segment")
    for part in parts:
        need(part == part.rstrip(" ."), "windows_trailing_alias")
        need(not re.fullmatch(r"(?i:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?",
                              part), "windows_device_alias")
    return value


def path_set(paths, ceiling=2000):
    need(type(ceiling) is int and 0 <= ceiling <= 2000, "invalid_file_ceiling")
    need(isinstance(paths, list) and len(paths) <= ceiling, "file_ceiling")
    checked = [portable_path(p) for p in paths]
    need(len(set(checked)) == len(checked), "duplicate_path")
    need(len({p.casefold() for p in checked}) == len(checked), "case_alias_collision")
    return set(checked)


def manifest_for(payloads, domain="raw_git_blob_v1", modes=None, exclusions=None):
    paths = path_set(list(payloads))
    modes = modes or {}
    exclusions = exclusions or []
    excluded = path_set(exclusions)
    need(not (paths & excluded), "hashed_exclusion_overlap")
    need(len(paths | excluded) <= 2000, "file_ceiling")
    entries = []
    for p in sorted(paths):
        mode = modes.get(p, "100644")
        need(mode in {"100644", "100755"}, "nonregular_mode")
        entries.append({"path": p, "mode": mode, **digest_stream([payloads[p]], domain)})
    return {"schema": "ghc.family.evidence-capsule.manifest.v1",
            "byte_domain": domain, "entries": entries, "entry_count": len(entries),
            "declared_self_exclusions": sorted(excluded)}


def verify_manifest(manifest, payloads, expected_paths, allowed_exclusions=None):
    need(isinstance(manifest, dict), "manifest_object_required")
    entries = manifest.get("entries")
    need(isinstance(entries, list), "manifest_entries_required")
    need(type(manifest.get("entry_count")) is int and
         manifest["entry_count"] == len(entries), "entry_count")
    expected = path_set(expected_paths)
    excluded = path_set(manifest.get("declared_self_exclusions", []))
    need(excluded == path_set(allowed_exclusions or []), "unapproved_exclusions")
    need(excluded <= expected, "excluded_path_not_expected")
    paths = path_set([e.get("path") for e in entries])
    need(paths == expected - excluded and paths == set(payloads), "manifest_path_set")
    need(not paths & excluded, "hashed_exclusion_overlap")
    need([e["path"] for e in entries] == sorted(paths), "manifest_order")
    domain = manifest.get("byte_domain")
    need(domain in DOMAINS, "unknown_byte_domain")
    for e in entries:
        need(e.get("mode") in {"100644", "100755"}, "nonregular_mode")
        need(e.get("byte_domain") == domain, "mixed_byte_domain")
        need(type(e.get("bytes")) is int and e["bytes"] >= 0, "invalid_byte_count")
        need(isinstance(e.get("sha256"), str) and
             re.fullmatch(r"[0-9a-f]{64}", e["sha256"]), "invalid_sha256")
        actual = digest_stream([payloads[e["path"]]], domain)
        need(actual["bytes"] == e["bytes"], "byte_count_mismatch")
        need(actual["sha256"] == e["sha256"], "digest_mismatch")
    return {"valid": True, "entry_count": len(entries), "byte_domain": domain}


def full_commit(value):
    need(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value),
         "full_commit_required")
    return value


def anchors(value):
    need(isinstance(value.get("owner"), str) and 0 < len(value["owner"]) <= 96,
         "owner_required")
    for key in ("source", "x1", "evidence", "final"):
        full_commit(value.get(key))
    return value


def validate_bindings(value):
    anchors(value)
    prefix = portable_path(value.get("scope_prefix"))
    parents = value.get("parents", {})
    for a, b in (("source", "x1"), ("x1", "evidence"), ("evidence", "final")):
        need(parents.get(value[b]) == [value[a]], "not_direct_single_parent")
    planning = path_set(value.get("planning_paths", []))
    need(bool(planning), "planning_paths_required")
    need(all(p.startswith(prefix + "/x1/") or
             p in {prefix + "/validation/x1-manifest.json",
                   prefix + "/validation/x1-precommit.json"}
             for p in planning), "implementation_in_x1")
    maps = value.get("planning_maps", {})
    first = maps.get("x1")
    need(isinstance(first, dict) and set(first) == planning, "planning_map_required")
    need(maps.get("evidence") == first and maps.get("final") == first,
         "planning_bytes_changed")
    delta = path_set(value.get("delta_paths", []))
    extra = path_set(value.get("extra_allowed_paths", []))
    need(bool(delta), "delta_paths_required")
    need(all(p.startswith(prefix + "/") or p in extra for p in delta),
         "outside_owner_scope")
    need(value.get("unchanged_history_scan") is False, "history_scan_forbidden")
    return {"valid": True, "planning_count": len(planning), "delta_count": len(delta)}


def validate_credit(row):
    need(type(row.get("inherited")) is bool, "inherited_boolean_required")
    need(row.get("outcome") in OUTCOMES, "invalid_outcome")
    need(row.get("independent_reproduction") is False, "independence_promotion")
    need(row.get("closed_gates") == [], "protected_gate_promotion")
    need(type(row.get("novelty_credit")) is int and row["novelty_credit"] in (0, 1),
         "novelty_credit")
    need(type(row.get("completion_credit")) is int and row["completion_credit"] in (0, 1),
         "completion_credit")
    if row.get("inherited") is True:
        need(row["novelty_credit"] == row["completion_credit"] == 0,
             "inherited_credit_promotion")
    credit = row.get("aggregate_success_credit", 0)
    need(type(credit) is int and credit in (0, 1), "aggregate_credit")
    if row.get("aggregate_state") != "valid":
        need(credit == 0, "failed_or_absent_aggregate_credit")
    if row.get("recovery_of") is not None:
        prior = row["recovery_of"]
        need(isinstance(prior, dict) and prior.get("state") == "invalid" and
             prior.get("success_credit") == 0 and bool(prior.get("negative_id")),
             "recovery_erases_failure")
        need(credit == 0, "recovery_promotes_aggregate")
    if row["outcome"] != "completed":
        need(row["completion_credit"] == 0, "noncompletion_credit")
    return {"valid": True, "outcome": row["outcome"]}


def unique_rows(rows, key):
    need(isinstance(rows, list), "record_list_required")
    need(all(isinstance(r, dict) for r in rows), "record_object_required")
    ids = [r.get(key) for r in rows]
    need(all(isinstance(x, str) and x for x in ids), "record_id_required")
    need(len(ids) == len(set(ids)), "duplicate_record_id")
    return dict(zip(ids, rows))


def validate_ledger(value):
    negatives = unique_rows(value.get("negatives"), "negative_id")
    witnesses = unique_rows(value.get("witnesses"), "witness_id")
    methods = unique_rows(value.get("methods"), "method_id")
    for n in negatives.values():
        need(n.get("success_credit") == 0, "negative_credit_promotion")
        if n.get("corrects") is not None:
            need(n["corrects"] in negatives and n["corrects"] != n["negative_id"],
                 "missing_correction_predecessor")
    for w in witnesses.values():
        need(w.get("result") in {"pass", "fail"}, "invalid_witness_result")
        links = w.get("retained_negative_ids")
        need(isinstance(links, list) and bool(links) and
             set(links) <= set(negatives), "orphan_witness")
        need(w.get("independent_reproduction") is False, "independence_promotion")
    for m in methods.values():
        ids = m.get("witness_ids", [])
        need(set(ids) <= set(witnesses), "missing_method_witness")
        if m.get("state") in {"validated", "preferred"}:
            need(any(witnesses[i]["result"] == "pass" for i in ids),
                 "promotion_without_pass")
    previous = value.get("previous", {})
    for name, key, current in (("negatives", "negative_id", negatives),
                               ("witnesses", "witness_id", witnesses),
                               ("methods", "method_id", methods)):
        for old in previous.get(name, []):
            need(old.get(key) in current and current[old[key]] == old,
                 "retained_record_changed_or_removed")
    totals = {"negatives": len(negatives),
              "failed_witnesses": sum(w["result"] == "fail" for w in witnesses.values()),
              "passing_witnesses": sum(w["result"] == "pass" for w in witnesses.values())}
    if "counts" in value:
        need(value["counts"] == totals, "ledger_count_mismatch")
    return {"valid": True, **totals}


def reserve_canonical(path, binding):
    anchors(binding)
    value = {"schema": "ghc.family.capsule.canonical-reservation.v1",
             "anchors": binding, "state": "RESERVED_ZERO_SUCCESS_CREDIT",
             "canonical_invocations": 1, "canonical_success_credit": 0,
             "replay_prohibited": True, "boundary": BOUNDARY}
    try:
        with Path(path).open("xb") as f:
            f.write(json_bytes(value))
    except FileExistsError as exc:
        raise CapsuleError("canonical_already_reserved") from exc
    return value


def finalize_canonical(path, checks):
    reservation = strict_json(Path(path).read_bytes())
    need(reservation.get("state") == "RESERVED_ZERO_SUCCESS_CREDIT",
         "invalid_reservation")
    anchors(reservation["anchors"])
    need(isinstance(checks, dict) and bool(checks) and
         all(isinstance(k, str) and type(v) is bool for k, v in checks.items()),
         "named_boolean_checks_required")
    valid = all(checks.values())
    result = {"schema": "ghc.family.capsule.canonical-result.v1",
              "anchors": reservation["anchors"], "checks": checks,
              "check_count": len(checks), "pass_count": sum(checks.values()),
              "failed_checks": [k for k, v in checks.items() if not v],
              "valid": valid, "status": "VALID" if valid else "INVALID",
              "canonical_success_credit": int(valid), "replay_count": 0,
              "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
              "boundary": BOUNDARY}
    result_path = Path(str(path) + ".result.json")
    try:
        with result_path.open("xb") as f:
            f.write(json_bytes(result))
    except FileExistsError as exc:
        raise CapsuleError("canonical_already_finalized") from exc
    return result


def validate_latch(value):
    anchors(value["anchors"])
    need(type(value.get("canonical_invocations")) is int and value["canonical_invocations"] == 1, "canonical_invocation_count")
    need(type(value.get("replay_count")) is int and value["replay_count"] == 0, "canonical_replay")
    need(type(value.get("complete")) is bool, "completion_boolean")
    checks = value.get("checks", {})
    need(isinstance(checks, dict) and
         all(type(v) is bool for v in checks.values()), "named_boolean_checks_required")
    expected = int(value["complete"] is True and bool(checks) and all(checks.values()))
    need(type(value.get("success_credit")) is int and value["success_credit"] == expected, "canonical_credit_mismatch")
    need(value.get("independent_reproduction") is False, "independence_promotion")
    return {"valid": True, "success_credit": expected}


def validate_deck(value):
    cards = unique_rows(value.get("cards"), "card_id")
    need(bool(cards), "empty_deck")
    roots = [c for c in cards.values() if c.get("tier") == 1]
    need(len(roots) == 1, "owner_anchor_count")
    for c in cards.values():
        tier = c.get("tier")
        need(type(tier) is int and 1 <= tier <= 4, "invalid_card_tier")
        parent_ids = c.get("parent_ids")
        need(isinstance(parent_ids, list), "parent_list_required")
        need(len(parent_ids) == (0 if tier == 1 else 1), "parent_count")
        for parent in parent_ids:
            need(parent in cards, "missing_card_parent")
            need(cards[parent].get("tier") == tier - 1, "tier_skip_or_cycle")
        need(c.get("outcome") in OUTCOMES, "invalid_outcome")
    done, active = set(), set()

    def visit(cid):
        need(cid not in active, "card_cycle")
        if cid in done:
            return
        active.add(cid)
        for parent in cards[cid]["parent_ids"]:
            visit(parent)
        active.remove(cid)
        done.add(cid)
    for cid in cards:
        visit(cid)
    stable, volatile = value.get("stable_prefix"), value.get("volatile_index")
    need(isinstance(stable, list) and isinstance(volatile, list), "deck_indices_required")
    need(len(stable + volatile) == len(set(stable + volatile)) and
         set(stable + volatile) == set(cards), "deck_index_partition")
    need(all(cards[c]["stability"] == "stable" and cards[c]["tier"] <= 2
             for c in stable), "volatile_in_stable_prefix")
    need(stable == [c["card_id"] for c in value["cards"] if c["stability"] == "stable"],
         "stable_prefix_order")
    need(value.get("sections") == SECTIONS, "baton_sections")
    return {"valid": True, "card_count": len(cards), "section_count": len(SECTIONS)}


def relative_link(value):
    need(isinstance(value, str), "link_required")
    parts = value.split("#")
    need(len(parts) <= 2, "invalid_fragment")
    portable_path(parts[0])
    if len(parts) == 2:
        need(bool(re.fullmatch(r"[A-Za-z0-9_-]+", parts[1])), "invalid_fragment")
    return value


def render_report(value):
    rows = value.get("rows", [])
    need(isinstance(rows, list), "report_rows")
    body = []
    for row in rows:
        need(row.get("outcome") in OUTCOMES, "invalid_outcome")
        body.append("<tr><th scope='row'>" + html.escape(str(row["title"])) +
                    "</th><td>" + html.escape(row["outcome"]) +
                    "</td><td>" + html.escape(str(row.get("detail", ""))) + "</td></tr>")
    links = "".join("<li><a href='" + html.escape(relative_link(x["path"]), quote=True) +
                    "'>" + html.escape(x["label"]) + "</a></li>" for x in value.get("links", []))
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Portable evidence capsule report</title>"
        "<style>body{font-family:system-ui;max-width:75rem;margin:2rem auto;padding:1rem;"
        "color:#18202b;background:#fff}table{border-collapse:collapse;width:100%}"
        "th,td{border:1px solid #788391;padding:.65rem;text-align:left;vertical-align:top}"
        "a{color:#0645ad}caption{text-align:left;font-weight:bold;padding:.6rem 0}</style>"
        "</head><body><header><h1>Portable evidence capsule report</h1></header>"
        "<main><p>" + html.escape(BOUNDARY) + "</p><p>NOT_READY_FOR_STAGE_20</p>"
        "<table><caption>Declared evidence outcomes</caption><thead><tr>"
        "<th scope='col'>Acceptance condition</th><th scope='col'>Outcome</th>"
        "<th scope='col'>Evidence and limits</th></tr></thead><tbody>" +
        "".join(body) + "</tbody></table><nav aria-label='Evidence files'><ul>" +
        links + "</ul></nav></main></body></html>\n"
    )


class ReportStructure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []
        self.headers = []
        self.lang = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "th":
            self.headers.append(a.get("scope"))
        for field in ("href", "src"):
            if field in a:
                self.links.append(a[field])

    def handle_data(self, data):
        self.text.append(data)


def validate_report(value):
    p = ReportStructure()
    p.feed(value)
    need(p.lang == "en", "report_language")
    need(all(t in p.tags for t in ("main", "h1", "caption", "thead", "tbody")),
         "report_landmarks")
    need("col" in p.headers and all(x in {"row", "col"} for x in p.headers),
         "report_table_headers")
    need("script" not in p.tags and "iframe" not in p.tags, "active_report_content")
    for link in p.links:
        relative_link(link)
    text = " ".join(p.text)
    need("NOT_READY_FOR_STAGE_20" in text and
         all(x in text for x in ("browser", "assistive-technology", "cognitive",
                                "language", "affected-user", "reserved")),
         "manual_review_reservation")
    return {"valid": True, "links": len(p.links), "manual_evaluation_complete": False}


def validate_reservations(value):
    rows = value.get("rows", [])
    need(len(rows) == 6, "reservation_count")
    need([r.get("outcome") for r in rows] == ["open_gap"] * 3 + ["exact_gate"] * 3,
         "reservation_outcomes")
    need(all(r.get("executed") is False and r.get("closed") is False for r in rows),
         "reservation_executed_or_closed")
    return {"valid": True, "open_gaps": 3, "exact_gates": 3}


def _git(repo, *args, input_bytes=None):
    r = subprocess.run(["git", "-C", str(repo), *args], input=input_bytes,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(r.returncode == 0, "git_read_failed")
    return r.stdout


def git_payloads(repo, revision, paths):
    full_commit(revision)
    targets = sorted(path_set(paths))
    need(bool(targets), "empty_git_allowlist")
    need(sum(len(p.encode("utf-8")) + 1 for p in targets) <= 20000,
         "git_argument_budget")
    tree = _git(repo, "ls-tree", "-z", revision, "--", *targets)
    modes = {}
    for record in tree.rstrip(b"\0").split(b"\0"):
        if not record:
            continue
        meta, p = record.split(b"\t", 1)
        mode, kind, oid = meta.decode("ascii").split()
        path = p.decode("utf-8")
        need(kind == "blob" and mode in {"100644", "100755"}, "nonregular_git_object")
        modes[path] = mode
    need(set(modes) == set(targets), "git_target_set")
    refs = "".join(revision + ":" + p + "\n" for p in targets).encode("utf-8")
    headers = _git(repo, "cat-file", "--batch-check", input_bytes=refs).splitlines()
    need(len(headers) == len(targets), "batch_header_count")
    total = 0
    for line in headers:
        parts = line.split()
        need(len(parts) == 3 and parts[1] == b"blob", "missing_git_blob")
        size = int(parts[2])
        need(0 <= size <= 8 * 1024 * 1024, "blob_size_budget")
        total += size
    need(total <= 64 * 1024 * 1024, "total_blob_budget")
    raw = _git(repo, "cat-file", "--batch", input_bytes=refs)
    offset, payloads = 0, {}
    for path, expected_header in zip(targets, headers):
        end = raw.find(b"\n", offset)
        need(end >= offset and raw[offset:end] == expected_header, "batch_header_mismatch")
        size = int(expected_header.split()[2])
        start = end + 1
        need(raw[start + size:start + size + 1] == b"\n", "batch_frame")
        payloads[path] = raw[start:start + size]
        need(len(payloads[path]) == size, "short_blob")
        offset = start + size + 1
    need(offset == len(raw), "trailing_batch_data")
    return payloads, modes


def check_group(group, value):
    need(isinstance(value, dict), "input_object_required")
    if group == "bytes":
        raw = bytes.fromhex(value["hex"])
        return digest_stream([raw], value["domain"])
    if group == "paths":
        return {"valid": True, "count": len(path_set(value["paths"]))}
    if group == "manifest":
        payloads = {k: bytes.fromhex(v) for k, v in value["payloads_hex"].items()}
        return verify_manifest(value["manifest"], payloads, value["expected_paths"],
                               value.get("allowed_exclusions", []))
    handlers = {"bindings": validate_bindings, "credit": validate_credit,
                "ledger": validate_ledger, "latch": validate_latch,
                "deck": validate_deck, "report": lambda v: validate_report(v["html"]),
                "reservations": validate_reservations}
    need(group in handlers, "unknown_group")
    return handlers[group](value)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    d = sub.add_parser("digest")
    d.add_argument("--file", required=True)
    d.add_argument("--domain", choices=sorted(DOMAINS), required=True)
    c = sub.add_parser("check")
    c.add_argument("--group", required=True)
    c.add_argument("--input", required=True)
    s = sub.add_parser("seal")
    s.add_argument("--repo", required=True)
    s.add_argument("--revision", required=True)
    s.add_argument("--allowlist", required=True)
    s.add_argument("--output", required=True)
    r = sub.add_parser("render")
    r.add_argument("--input", required=True)
    r.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "digest":
            with Path(args.file).open("rb") as f:
                result = digest_stream(iter(lambda: f.read(65536), b""), args.domain)
        elif args.command == "check":
            result = check_group(args.group, strict_json(Path(args.input).read_bytes()))
        elif args.command == "seal":
            paths = strict_json(Path(args.allowlist).read_bytes())
            payloads, modes = git_payloads(args.repo, args.revision, paths)
            result = manifest_for(payloads, modes=modes)
            with Path(args.output).open("xb") as f:
                f.write(json_bytes(result))
        else:
            document = render_report(strict_json(Path(args.input).read_bytes()))
            result = validate_report(document)
            with Path(args.output).open("xb") as f:
                f.write(document.encode("utf-8"))
        sys.stdout.buffer.write(json_bytes(result))
        return 0
    except (CapsuleError, OSError, KeyError, TypeError, ValueError, AttributeError, IndexError) as exc:
        code = str(exc) if isinstance(exc, CapsuleError) else type(exc).__name__
        sys.stdout.buffer.write(json_bytes({"valid": False, "error": code,
                                           "boundary": BOUNDARY}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
