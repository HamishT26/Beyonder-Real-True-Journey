from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "tests" / "test_ghc_family_v646_v3_x1.py"
source = BASE.read_text(encoding="utf-8")
replacements = [
    ('self.assertEqual(payload["prior_frozen_proposal_count"], 410)', 'self.assertEqual(payload["prior_frozen_proposal_count"], 420)'),
    ('self.assertEqual(payload["frozen_chain_count_after_x1"], 420)', 'self.assertEqual(payload["frozen_chain_count_after_x1"], 430)'),
    ('test_semantic_novelty_audit_covers_all_410', 'test_semantic_novelty_audit_covers_all_420'),
    ('self.assertEqual(audit["prior_frozen_proposal_count"], 410)', 'self.assertEqual(audit["prior_frozen_proposal_count"], 420)'),
    ('safe_new_sable', 'safe_new_orin'),
    ('candidate_new_sable', 'candidate_new_orin'),
    ('self.assertEqual(len(sources["sources"]), 19)', 'self.assertEqual(len(sources["sources"]), 17)'),
    ('self.assertEqual(negatives["inherited_effective"], 2619)', 'self.assertEqual(negatives["inherited_effective"], 2704)'),
    ('self.assertEqual(negatives["new_x1_operational"], 5)', 'self.assertEqual(negatives["new_x1_operational"], 16)'),
    ('self.assertEqual(negatives["effective_after_x1"], 2694)', 'self.assertEqual(negatives["effective_after_x1"], 2790)'),
    ('self.assertEqual(gates["inherited_open_gaps"], 11)', 'self.assertEqual(gates["inherited_open_gaps"], 12)'),
    ('self.assertEqual(gates["inherited_exact_gates"], 12)', 'self.assertEqual(gates["inherited_exact_gates"], 13)'),
    ('self.assertEqual(method["method_count"], 4)', 'self.assertEqual(method["method_count"], 16)'),
    ('self.assertEqual(method["witness_count"], 9)', 'self.assertEqual(method["witness_count"], 32)'),
    ('V646V3X1Tests', 'V646V4X1Tests'),
    ('V6463', 'V6464'),
    ('v646-v3', 'v646-v4'),
    ('sable-rook', 'orin-thale'),
]
for old, new in replacements:
    source = source.replace(old, new)
exec(compile(source, str(BASE), "exec"), globals())
