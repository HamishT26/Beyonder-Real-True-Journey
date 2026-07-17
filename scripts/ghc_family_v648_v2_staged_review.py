#!/usr/bin/env python3
"""Exact Git-index staged review for Sylven Arc v648-v2 lifecycle commits."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "ghc_family_v648_v1_staged_review.py"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    replacements = [
        ("Tamar Vey", "Sylven Arc"),
        ("docs/tamar-vey/v648-v1/", "docs/sylven-arc/v648-v2/"),
        ("v648-v1", "v648-v2"),
        ("v648_v1", "v648_v2"),
        ("ghc_family_atomic_publication_tribunal.py", "ghc_family_advisory_lock_tribunal.py"),
        ("ghc_family_iyer_wald_obligations.py", "ghc_family_kms_obligations.py"),
        ("ghc_family_des_y3_zero_row.py", "ghc_family_lotss_dr2_zero_row.py"),
        ("ghc_family_crane_lift_handover.py", "ghc_family_machining_handover.py"),
        ("ghc_family_shared_signals_profile.py", "ghc_family_jarm_profile.py"),
        ("ghc_family_crane_incident_authority.py", "ghc_family_machining_authority.py"),
        ("ghc_family_cpio_newc_tribunal.py", "ghc_family_zstd_frame_tribunal.py"),
        ("ghc_family_accessible_name_audit.py", "ghc_family_progressbar_audit.py"),
        ("ghc_family_prigogine_domain.py", "ghc_family_gibbs_adsorption.py"),
        ("ghc_family_instrumental_variable_board.py", "ghc_family_synthetic_control_board.py"),
        ("args.review.relative_to(ROOT)", "args.review.resolve().relative_to(ROOT)"),
        ("args.manifest.relative_to(ROOT)", "args.manifest.resolve().relative_to(ROOT)"),
        ("args.privacy.relative_to(ROOT)", "args.privacy.resolve().relative_to(ROOT)"),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def main() -> int:
    namespace = {"__name__": "ghc_family_v648_v2_staged_review_template", "__file__": str(Path(__file__).resolve())}
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
