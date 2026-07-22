#!/usr/bin/env python3
"""Build ten thin family-current v651-v6 runner entrypoints."""

from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
GROUPS = {
    "ghc_family_numerical_verification_board.py": ["non-normal-pseudospectrum", "constraint-residual-attribution", "buckingham-pi"],
    "ghc_family_discrete_adjoint_dot_test.py": ["discrete-adjoint-dot-product", "jacobian-coloring", "metamorphic-coordinate-invariance"],
    "ghc_family_dae_event_gate.py": ["dae-index-drift", "event-localization", "stiffness-solver-contract"],
    "ghc_family_richardson_range_gate.py": ["richardson-asymptotic-range", "conservation-projection", "shadow-hamiltonian"],
    "ghc_family_work_precision_frontier.py": ["work-precision-frontier", "emulator-convex-hull", "model-discrepancy-separator"],
    "ghc_family_mixed_precision_escalation.py": ["mixed-precision-escalation", "backward-error-modified-equation", "blind-likelihood-lockfile"],
    "ghc_family_thos_runtime_boundaries.py": ["thos-cancellation-propagation", "thos-priority-inversion", "thos-resource-lifetime", "thos-trace-parentage", "thos-repeatability-classifier"],
    "ghc_family_freed_id_key_boundaries.py": ["freed-id-key-custody", "freed-id-compromise-blast-radius"],
    "ghc_family_consequential_model_ledger.py": ["cbr-contestation-chain", "cbr-explanation-provenance", "cbr-model-redress-authority"],
    "ghc_family_claim_retraction_protocol.py": ["evidence-minimal-cut", "claim-retraction-trigger"],
}


TEMPLATE = '''#!/usr/bin/env python3
"""Family-current bounded delegate for Elaren v651-v6."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v651_v6_runtime import REPO, run_group


SURFACES = {surfaces!r}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = run_group(SURFACES)
    if args.output:
        target = REPO / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8", newline="\\n")
    print(json.dumps({{"runner": Path(__file__).name, "surfaces": len(SURFACES), "valid": payload["valid"], "output": args.output}}, sort_keys=True))


if __name__ == "__main__":
    main()
'''


def main() -> None:
    rows = []
    all_surfaces = set()
    for name, surfaces in GROUPS.items():
        target = SCRIPTS / name
        target.write_text(TEMPLATE.format(surfaces=surfaces), encoding="utf-8", newline="\n")
        rows.append({"name": name, "path": f"scripts/{name}", "surfaces": surfaces, "family_current": True, "compatibility_delegate": True})
        all_surfaces.update(surfaces)
    receipt = {"schema": "ghc.family.v651-v6.runner-build.v1", "runner_count": len(rows), "surface_coverage_count": len(all_surfaces), "runners": rows, "unified_runtime": "scripts/ghc_family_v651_v6_runtime.py", "independent_implementations_claimed": False, "valid": len(rows) == 10 and len(all_surfaces) == 30}
    target = REPO / "docs/elaren-kestrel/v651-v6/tooling/runner-build-receipt.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runners": len(rows), "surface_coverage": len(all_surfaces), "valid": receipt["valid"]}))


if __name__ == "__main__":
    main()
