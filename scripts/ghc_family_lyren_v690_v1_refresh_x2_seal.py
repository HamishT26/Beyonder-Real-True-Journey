"""Refresh the additive x2 tool catalogue, truth overlay, allowlist, and manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "docs/lyren-moss/v690-v1/x2"
SOURCE = "fbd8eb790f2f8bc9c507db0420bdd66d1ec05e2e"
GATES = [
    "empirical",
    "participants",
    "professional",
    "production",
    "legal-cultural-Maori-authority",
    "privacy-accessibility-security-completeness",
    "independent-reproduction",
    "AGI-ASI-consciousness-personhood",
    "Theory-of-Everything-Stage-20",
]


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    promotion_path = X2 / "tooling/global-promotion.json"
    promotion = load(promotion_path)
    if not promotion["passed"] or promotion["counts"] != {"skills": 5, "public_runners": 5, "dependency_modules": 2}:
        raise RuntimeError("global promotion receipt is not complete")

    catalogue_path = X2 / "meta-tool-catalogue.json"
    catalogue = load(catalogue_path)
    known = {row["card_id"] for row in catalogue["cards"]}
    for row in promotion["runners"]:
        card_id = "runner-global:" + row["name"]
        if card_id in known:
            continue
        catalogue["cards"].append(
            {
                "card_id": card_id,
                "kind": "runner",
                "name": row["name"],
                "status": "installed_additively",
                "source_path": Path(row["source"]).relative_to(ROOT).as_posix(),
                "installed_path": row["target"],
                "sha256": row["target_sha256"],
                "owner_scope": "Lyren Moss v690-v1 owner-only",
                "execution_authority": "owner_self_scoped_delta",
                "evidence_state": "validated",
                "repository_scan": False,
                "module_scan": True,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "source_commit": SOURCE,
                "final_commit": "external_after_final_commit",
                "rollback": "Stop selecting the additive runner and preserve its installation receipt.",
                "protected_gates": GATES,
            }
        )
    catalogue["cards"] = sorted(catalogue["cards"], key=lambda row: row["card_id"])
    catalogue["card_count"] = len(catalogue["cards"])
    catalogue["global_promotion"] = {
        "state": promotion["state"],
        "skills": 5,
        "public_runners": 5,
        "dependency_modules": 2,
        "no_overwrite": True,
    }
    write(catalogue_path, catalogue)

    truth_path = X2 / "phase-truth.json"
    truth = load(truth_path)
    truth["global_tools_promoted"] = promotion["state"]
    truth["post_validation_overlay"] = {
        "retained_negatives": 7,
        "methods": 1,
        "witnesses": 14,
        "failed_witnesses": 7,
        "passing_witnesses": 7,
    }
    truth["x2_effective"] = {
        "effective_negatives": 112,
        "methods": 14,
        "direct_witnesses": 459,
        "failed_witnesses": 112,
        "passing_witnesses": 347,
    }
    truth["cumulative_after_late_overlay"] = {
        "effective_negatives": 967,
        "methods": 80,
        "direct_witnesses": 2467,
        "failed_witnesses": 678,
        "passing_witnesses": 1789,
    }
    write(truth_path, truth)

    allowlist_path = X2 / "allowlist.json"
    manifest_path = X2 / "manifest.json"
    all_files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in X2.rglob("*")
        if path.is_file()
    )
    write(
        allowlist_path,
        {
            "owner": "Lyren Moss",
            "phase": "x2",
            "allowed_paths": all_files,
            "additive_only": True,
        },
    )
    entries = []
    for path in sorted(file for file in X2.rglob("*") if file.is_file() and file != manifest_path):
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": raw_sha256(path),
                "hash_domain": "raw_file_bytes",
            }
        )
    write(manifest_path, {"self_excluded": "manifest.json", "entry_count": len(entries), "entries": entries})
    print(json.dumps({"catalogue_cards": catalogue["card_count"], "manifest_entries": len(entries), "effective_negatives": 967}, sort_keys=True))


if __name__ == "__main__":
    main()
