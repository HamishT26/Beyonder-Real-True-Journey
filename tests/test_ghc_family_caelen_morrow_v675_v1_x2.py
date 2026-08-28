from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess  # nosec B404 - controlled local Git probes only
import unittest
from collections import Counter
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

ROOT = Path(__file__).resolve().parents[1]


def resolve_git_executable() -> str:
    candidate = shutil.which("git")
    if candidate is None:
        raise RuntimeError("git executable is required")
    return candidate


GIT_EXE = resolve_git_executable()
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v675-v1"
X1_COMMIT = "4d8bb1d7d956883a51a0e543cc3b2fd74b6305b6"
SOURCE_FINAL = "47ba7b0149713f60729f18f5a36ef78c331ce35f"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
EXPECTED_METHOD_COUNT = 225
EXPECTED_STATE_EVENTS = EXPECTED_METHOD_COUNT * 3
EXPECTED_WITNESSES = EXPECTED_METHOD_COUNT * 2
NO_FAILURES_REWRITTEN = int(False)


def load(relative: str) -> dict:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    return subprocess.run(  # nosec B603 - executable and arguments are owner-controlled Git probes
        [GIT_EXE, *args], cwd=ROOT, check=True, capture_output=True
    ).stdout


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def commit_blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def import_path(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path.name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCaelenMorrowV675V1X2Evidence(unittest.TestCase):
    def test_01_exact_immutable_x1_gate(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD").decode().strip(), X1_COMMIT)
        self.assertEqual(git("rev-parse", f"{X1_COMMIT}^").decode().strip(), SOURCE_FINAL)
        self.assertEqual(len(git("rev-list", f"{SOURCE_FINAL}..{X1_COMMIT}").decode().splitlines()), 1)
        x1_tree = git("ls-tree", "-r", "--name-only", X1_COMMIT).decode().splitlines()
        current_owner = [p for p in x1_tree if p.startswith("docs/caelen-morrow/v675-v1/")]
        self.assertTrue(current_owner)
        self.assertFalse(any("/x2/" in f"/{path}/" for path in current_owner))
        self.assertFalse(any("_x2.py" in path for path in x1_tree if "caelen_morrow_v675_v1" in path))

    def test_02_immutable_x1_manifest_replays_at_x1(self) -> None:
        manifest = json.loads(
            commit_blob(
                X1_COMMIT, "docs/caelen-morrow/v675-v1/validation/x1-manifest.json"
            ).decode("utf-8")
        )
        self.assertEqual(manifest["entry_count"], 23)
        for row in manifest["entries"]:
            blob = commit_blob(X1_COMMIT, row["path"])
            self.assertEqual(len(blob), row["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"])

    def test_03_four_label_proposal_evidence(self) -> None:
        ledger = load("x2/proposal-ledger-evidence.json")
        rows = ledger["rows"]
        self.assertEqual(len(rows), 40)
        self.assertEqual(Counter(row["observed_outcome"] for row in rows), Counter(OUTCOMES))
        self.assertEqual(ledger["proposal_chain_before"], 7030)
        self.assertEqual(ledger["proposal_chain_after"], 7070)
        for index, row in enumerate(rows, 1):
            self.assertEqual(row["proposal_id"], f"CM6751-N{index:03d}")
            self.assertEqual(row["expected_outcome"], row["observed_outcome"])
            self.assertIn(row["observed_outcome"], OUTCOMES)
            self.assertEqual(row["rejecting_mutations"], 4)
            self.assertEqual(row["external_actions"], 0)
            self.assertFalse(row["authority_conferred"])

    def test_04_all_preregistered_mutations_reject_and_remain_zero_credit(self) -> None:
        receipt = load("x2/mutation-receipt.json")
        self.assertEqual(receipt["preregistered"], 160)
        self.assertEqual(receipt["executed"], 160)
        self.assertEqual(receipt["rejected"], 160)
        self.assertEqual(receipt["accepted"], 0)
        self.assertEqual(len(receipt["rows"]), 160)
        self.assertEqual(Counter(row["mutation_type"] for row in receipt["rows"]), Counter({
            "missing_hypothesis": 40,
            "missing_protected_gates": 40,
            "invalid_outcome_label": 40,
            "external_action_promotion": 40,
        }))
        for row in receipt["rows"]:
            self.assertTrue(row["preregistered"])
            self.assertTrue(row["executed"])
            self.assertTrue(row["rejected"])
            self.assertEqual(row["result"], "fail")
            self.assertEqual(row["completion_credit"], 0)
            self.assertTrue(row["recovery_preserves_failure"])

    def test_05_positive_controls_and_vacancy_controls(self) -> None:
        ledger = load("x2/proposal-ledger-evidence.json")
        positive = [row for row in ledger["rows"] if row["positive_control"] is not None]
        absent = [row for row in ledger["rows"] if row["positive_control"] is None]
        self.assertEqual(len(positive), 36)
        self.assertEqual(len(absent), 4)
        for row in positive:
            control = row["positive_control"]
            self.assertTrue(control["accepted"])
            self.assertEqual(control["external_actions"], 0)
            self.assertTrue(control["evidence"]["synthetic"])
            self.assertEqual(control["evidence"]["real_people"], 0)
            self.assertEqual(control["evidence"]["real_objects"], 0)
            self.assertEqual(control["evidence"]["real_measurements"], 0)
            self.assertFalse(control["evidence"]["authority_conferred"])
        self.assertEqual(Counter(row["observed_outcome"] for row in absent), Counter({"open_gap": 2, "exact_gate": 2}))

    def test_06_gap_and_gate_register_is_additive(self) -> None:
        register = load("x2/open-exact-gate-register-evidence.json")
        self.assertEqual(register["source_open_gaps"], 328)
        self.assertEqual(register["source_exact_gates"], 321)
        self.assertEqual(len(register["new_open_gap_ids"]), 2)
        self.assertEqual(len(register["new_exact_gate_ids"]), 2)
        self.assertEqual(register["effective_open_gaps"], 330)
        self.assertEqual(register["effective_exact_gates"], 323)
        self.assertEqual(register["closed_without_exact_evidence"], 0)
        self.assertEqual(register["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_07_portfolio_execution_stays_inside_frozen_scope(self) -> None:
        portfolio = load("x2/portfolio-outcome.json")
        self.assertEqual(portfolio["executed_counts"], {
            "candidates": 30,
            "clean_fix_refine": 60,
            "runners": 10,
            "safe_now": 60,
            "skills": 20,
            "tools": 3,
        })
        self.assertEqual(portfolio["exact_approval_executed"], 0)
        self.assertEqual(portfolio["blocked_executed"], 0)
        self.assertEqual(portfolio["successor_recommendation_credit"], 0)
        self.assertEqual(portfolio["inherited_completion_credit"], 0)
        self.assertEqual(portfolio["external_actions"], 0)
        self.assertFalse(portfolio["authority_conferred"])
        for key in ("exact_approval", "blocked"):
            self.assertTrue(all(row["execution_count"] == 0 for row in portfolio["rows"][key]))
        for key in ("successor_skills", "successor_runners", "successor_clean_fix_refine"):
            self.assertTrue(all(row["completion_credit"] == 0 for row in portfolio["rows"][key]))

    def test_08_method_flow_preserves_all_failures(self) -> None:
        flow = load("x2/method-flow-evidence.json")
        witness_document = load("x2/method-flow-witnesses-evidence.json")
        witnesses = witness_document["rows"]
        negatives = load("x2/retained-negative-register-evidence.json")
        self.assertEqual(len(flow["methods"]), EXPECTED_METHOD_COUNT)
        self.assertEqual(len(flow["recommendations"]), EXPECTED_METHOD_COUNT)
        self.assertEqual(len(flow["state_events"]), EXPECTED_STATE_EVENTS)
        self.assertEqual(flow["witness_document"], "x2/method-flow-witnesses-evidence.json")
        self.assertEqual(flow["witness_count"], EXPECTED_WITNESSES)
        self.assertEqual(witness_document["row_count"], EXPECTED_WITNESSES)
        self.assertEqual(len(witnesses), EXPECTED_WITNESSES)
        self.assertEqual(len(flow["negative_rows"]), EXPECTED_METHOD_COUNT)
        self.assertEqual(
            Counter(row["result"] for row in witnesses),
            Counter({"fail": EXPECTED_METHOD_COUNT, "pass": EXPECTED_METHOD_COUNT}),
        )
        self.assertEqual(negatives["row_count"], EXPECTED_METHOD_COUNT)
        self.assertEqual(negatives["failures_rewritten_as_pass"], NO_FAILURES_REWRITTEN)
        for row in flow["negative_rows"]:
            self.assertEqual(row["result"], "fail")
            self.assertEqual(row["completion_credit"], 0)
            self.assertTrue(row["recovery_preserves_failure"])
        for row in witnesses:
            self.assertTrue(row["same_owner_only"])
            self.assertFalse(row["independent_reproduction"])

    def test_09_skills_are_local_validated_and_smoke_used(self) -> None:
        receipt = load("x2/skill-runner-tool-evidence.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["official_quick_validation"]["passed"], 20)
        self.assertEqual(receipt["skills"]["passed"], 20)
        self.assertEqual(receipt["runners"]["passed"], 10)
        self.assertEqual(receipt["tools"]["passed"], 3)
        self.assertEqual(receipt["global_installations"], 0)
        self.assertEqual(receipt["external_actions"], 0)
        for row in receipt["skills"]["rows"]:
            self.assertEqual(row["quick_validate"], "pass")
            self.assertEqual(row["accepting_smoke"], "pass")
            self.assertEqual(row["rejecting_smoke"], "rejected_as_expected")
            self.assertFalse(row["global_installation"])

    def test_10_runner_and_tool_receipts_are_substantive(self) -> None:
        receipt = load("x2/skill-runner-tool-evidence.json")
        self.assertEqual(len(receipt["runners"]["rows"]), 10)
        self.assertEqual(len(receipt["tools"]["rows"]), 3)
        for row in receipt["runners"]["rows"]:
            self.assertEqual(row["accepting_smoke"], "pass")
            self.assertEqual(row["rejecting_smoke"], "rejected_as_expected")
            self.assertEqual(row["external_actions"], 0)
            self.assertFalse(row["authority_conferred"])
        self.assertTrue(all(row["accepting_smoke"] for row in receipt["tools"]["rows"]))
        self.assertTrue(all(row["rejecting_smoke_rejected"] for row in receipt["tools"]["rows"]))

    def test_11_flashcards_are_content_addressed_four_tier_graph(self) -> None:
        deck = load("x2/flashcards/deck.json")
        graph = load("x2/flashcards/graph.json")
        sections = load("x2/flashcards/section-manifest.json")
        self.assertEqual(deck["card_count"], 80)
        self.assertEqual(deck["tiers"], 4)
        self.assertEqual(deck["sections"], 13)
        self.assertEqual(len({row["card_id"] for row in deck["cards"]}), 80)
        self.assertEqual(len({row["content_sha256"] for row in deck["cards"]}), 80)
        for row in deck["cards"]:
            core = {key: value for key, value in row.items() if key != "content_sha256"}
            digest = hashlib.sha256(json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            self.assertEqual(digest, row["content_sha256"])
            self.assertEqual(row["external_actions"], 0)
            self.assertFalse(row["authority_conferred"])
        self.assertFalse(deck["cache_benefit_claimed"])
        self.assertFalse(deck["identity_continuity_claimed"])
        self.assertFalse(deck["cognitive_benefit_claimed"])
        self.assertEqual(graph["node_count"], 80)
        self.assertEqual(graph["edge_count"], 79)
        self.assertEqual(sections["section_count"], 13)

    def test_12_environment_and_source_adapter_are_nonmutating(self) -> None:
        environment = load("x2/environment-version-receipt.json")
        adapter = load("x2/adapter/canada-cci-cane-chair-zero-row.json")
        self.assertTrue(environment["version_checks_only"])
        self.assertEqual(environment["installations"], 0)
        self.assertEqual(environment["updates"], 0)
        self.assertFalse(environment["desktop_updated"])
        self.assertFalse(environment["elevation"])
        self.assertFalse(environment["windows_features_changed"])
        self.assertFalse(environment["reboot"])
        self.assertFalse(adapter["transport_enabled"])
        self.assertEqual(adapter["network_calls"], 0)
        self.assertEqual(adapter["downloads"], 0)
        self.assertEqual(adapter["rows"], 0)
        self.assertEqual(adapter["media"], 0)
        self.assertEqual(adapter["professional_claims"], 0)

    def test_13_html_and_all_evidence_json_are_structurally_accessible_and_parse(self) -> None:
        html = (OWNER_ROOT / "x2" / "accessible-evidence-report.html").read_text(encoding="utf-8")
        for token in ('<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope=\'row\'', 'NOT READY FOR STAGE 20'):
            self.assertIn(token, html)
        self.assertIn("manual", html.lower())
        self.assertIn("affected-user", html)
        json_paths = sorted((OWNER_ROOT / "x2").rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 50)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_14_privacy_scan_has_no_confirmed_hit(self) -> None:
        privacy = load("validation/evidence-staged-privacy.json")
        self.assertEqual(len(privacy["pattern_classes"]), 5)
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(privacy["confirmed_hits"], [])
        self.assertEqual(privacy["decode_issues"], [])

    def test_15_manifest_and_staged_review_replay(self) -> None:
        manifest = load("validation/evidence-manifest.json")
        review = load("validation/evidence-staged-review.json")
        staged = set(git("diff", "--cached", "--name-only", "--diff-filter=ACMR", X1_COMMIT).decode().splitlines())
        declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
        self.assertEqual(declared, staged)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            blob = staged_blob(row["path"])
            self.assertEqual(len(blob), row["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"])
        self.assertTrue(review["valid"])
        self.assertTrue(review["allowed_owner_scope"])
        self.assertEqual(review["non_additive_paths"], [])
        self.assertEqual(review["manifest_issues"], [])
        self.assertEqual(review["exact_blocked_executed"], 0)

    def test_16_all_evidence_paths_are_additive_and_within_caps(self) -> None:
        name_status = git("diff", "--cached", "--name-status", X1_COMMIT).decode().splitlines()
        self.assertTrue(name_status)
        self.assertTrue(all(row.startswith("A\t") for row in name_status))
        owner_files = [path for path in OWNER_ROOT.rglob("*") if path.is_file()]
        changed_scripts = [ROOT / row.split("\t", 1)[1] for row in name_status if row.split("\t", 1)[1].startswith(("scripts/", "tests/"))]
        all_files = owner_files + changed_scripts
        self.assertLessEqual(len(all_files), 2000)
        for path in all_files:
            if path.suffix.lower() in {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)


class TestCaelenMorrowV675V1PropertyGuards(unittest.TestCase):
    @given(st.integers(min_value=1, max_value=1000))
    def test_nonzero_external_action_always_rejects_contract(self, action_count: int) -> None:
        module = import_path(ROOT / "scripts" / "ghc_family_caelen_morrow_v675_v1_contract.py")
        proposal = load("x1/new-proposal-freeze.json")["rows"][0]
        mutated = dict(proposal)
        mutated["external_actions"] = action_count
        self.assertFalse(module.validate(mutated)["accepted"])

    @given(st.text(min_size=1).filter(lambda value: value not in OUTCOMES))
    def test_unknown_outcome_label_always_rejects_contract(self, label: str) -> None:
        module = import_path(ROOT / "scripts" / "ghc_family_caelen_morrow_v675_v1_contract.py")
        proposal = load("x1/new-proposal-freeze.json")["rows"][0]
        mutated = dict(proposal)
        mutated["expected_disposition"] = label
        self.assertFalse(module.validate(mutated)["accepted"])


if __name__ == "__main__":
    unittest.main()
