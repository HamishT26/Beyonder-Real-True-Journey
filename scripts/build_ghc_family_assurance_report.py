#!/usr/bin/env python3
"""Extend the stable family evidence report with additive assurance surfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_ghc_family_evidence_report import build_report, esc


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_assurance_report(phase: Path) -> str:
    base = build_report(phase)
    minimal_support = load(phase / "provenance" / "minimal-support-sets.json")
    source_impact = load(phase / "provenance" / "source-change-impact.json")
    typed_contract = load(phase / "physics" / "typed-expression-contract.json")
    counterexamples = load(phase / "physics" / "assumption-counterexample-sweep.json")
    cross_solver = load(phase / "physics" / "cross-solver-envelope.json")
    real_data_gate = load(phase / "empirical" / "baseline-to-claim-gate.json")
    blindness = load(phase / "thos" / "blindness-sentinel-audit.json")
    trust_gate = load(phase / "freed-id" / "trust-resolution-gate.json")
    participation = load(phase / "cbr" / "participation-evidence-contract.json")
    package_manifest = load(phase / "security" / "canonical-package-manifest.json")
    perturbation_matrix = load(phase / "reproduction" / "perturbation-matrix.json")
    compression = load(phase / "stage20" / "claim-compression-audit.json")
    section = f"""
  <section aria-labelledby="assurance-title">
    <h2 id="assurance-title">2C. V5 evidence-assurance extensions</h2>
    <p>V5 adds support minimization and downstream change propagation, typed expression counterexamples, a frozen cross-solver tolerance envelope, real-data and cryptographic completion gates, blindness sentinels, participation refusal checks, canonical packaging, multi-snapshot repeatability, and claim-compression integrity. These are bounded local controls rather than external truth.</p>
    <div class="table-wrap"><table><caption>V5 bounded assurance checks and preserved limits</caption><thead><tr><th>Surface</th><th>Executed check</th><th>Preserved limit</th></tr></thead><tbody>
      <tr><th scope="row">Source support</th><td>{minimal_support['claim_count']} minimal-support rows and {source_impact['fixture_count']} change fixtures</td><td>Declared dependence, not epistemic independence</td></tr>
      <tr><th scope="row">Typed GMUT</th><td>{typed_contract['expression_count']} typed expressions and {counterexamples['fixture_count']} counterexamples</td><td>Formal accountability, not empirical confirmation</td></tr>
      <tr><th scope="row">Numerical cross-check</th><td>{len(cross_solver['solvers'])} solvers under tolerance {esc(cross_solver['frozen_tolerance'])}</td><td>Local proxy, not accuracy against nature</td></tr>
      <tr><th scope="row">Empirical gate</th><td>Claim allowed: {esc(real_data_gate['claim_allowed'])}</td><td>Real data, baseline, likelihood, and review absent</td></tr>
      <tr><th scope="row">THOS</th><td>{blindness['fixture_count']} blindness sentinels; {blindness['real_arm_output_count']} real outputs</td><td>No superiority, AGI, ASI, or consciousness claim</td></tr>
      <tr><th scope="row">Freed ID</th><td>Highest local state: {esc(trust_gate['highest_local_state'])}</td><td>Real keys, proofs, resolution, and trust governance absent</td></tr>
      <tr><th scope="row">Participation</th><td>Authorized affected-party participation: {esc(participation['authorized_affected_party_participation_present'])}</td><td>Legal, cultural, and Māori authority exact-gated</td></tr>
      <tr><th scope="row">Canonical package</th><td>{package_manifest['file_count']} selected files; paths unique: {esc(package_manifest['canonical_paths_unique'])}</td><td>Not exhaustive security or certification</td></tr>
      <tr><th scope="row">Repeatability</th><td>{perturbation_matrix['clean_snapshot_count']} clean comparison snapshots</td><td>Same-owner only, never independent reproduction</td></tr>
      <tr><th scope="row">Claim compression</th><td>{compression['fixture_count']} boundary-loss mutations rejected</td><td>Automated static checks, not full accessibility conformance</td></tr>
    </tbody></table></div>
  </section>

"""
    marker = '  <section aria-labelledby="mind-title">'
    if marker not in base:
        raise ValueError("stable report insertion point is absent")
    return base.replace(marker, section + marker, 1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    encoded = build_assurance_report(args.phase_dir.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded.rstrip() + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output.as_posix(), "static": True, "assurance_section": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
