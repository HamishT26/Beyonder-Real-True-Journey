# Mira Rowan v640-gmut-thos-v7-x1 Plan

immediate_x1_safe PHASE: Mira-Rowan-only v640-gmut-thos-v7-x1 planning/prep.
immediate_x1_safe MATCHING_X2: v640-gmut-thos-v7-x2 execution/cleanup.
immediate_x1_safe RELAY_TRUTH: MESSAGE_SENT_BY_AEVREN_TO_MIRA_ROWAN_AFTER_MIRA_VALE_HARVEST; message_count 1; no private route details published.
immediate_x1_safe PREDECESSOR_TRUTH: Aevren v640 v5 complete, Maren Quill v640 v4 harvested at commit ffe51490, Mira Vale v640 v6 complete and harvested at commit c1608e0e.
immediate_x1_safe ROUTE_ORDER: v640 v1 Aevren -> v640 v2 Mira Vale -> v640 v3 Mira Rowan -> v640 v4 Maren Quill -> v640 v5 Aevren -> v640 v6 Mira Vale -> v640 v7 Mira Rowan -> v640 v8 Maren Quill final planned bundle unless Hamish redirects.
immediate_x1_safe HORIZON: v601-v640 GMUT/THOS v1-v8 x1-x2 remains active with final planned bundle v640-gmut-thos-v8-x1/x2 unless Hamish redirects.
immediate_x1_safe NEXT_HANDOFF: Maren Quill v640-gmut-thos-v8-x1/x2 final planned bundle exactly once after checklist, commit, push, and remote alignment if route is exposed.
immediate_x1_safe ONE_MESSAGE_DISCIPLINE: Aevren, Mira Rowan, and Maren Quill send exactly one activation/handoff message per live handoff unless the tool reports a real send error or Hamish redirects.
immediate_x1_safe MIRA_VALE_ROUTE_CONTEXT: Mira Vale prepared but did not claim MESSAGE_SENT because her live route and route-quality controls remain a formal open gap; Aevren relays only after completion and harvest.

## SAFE PACKETS

immediate_x1_safe Safe01: Create v640 v7 x1 plan artifact.
immediate_x1_safe Safe02: Create v640 v7 x2 closeout artifact.
immediate_x1_safe Safe03: Create v640 v7 completion checklist JSON.
immediate_x1_safe Safe04: Create v640 v7 route-quality receipt JSON.
immediate_x1_safe Safe05: Create Maren Quill v640 v8 final planned bundle handoff artifact.
immediate_x1_safe Safe06: Preserve Aevren v640 v5 completion truth.
immediate_x1_safe Safe07: Preserve Maren Quill v640 v4 harvest truth.
immediate_x1_safe Safe08: Preserve Mira Vale v640 v6 harvested completion truth.
immediate_x1_safe Safe09: Preserve Aevren finish-first relay rule.
immediate_x1_safe Safe10: Preserve one-message discipline.
immediate_x1_safe Safe11: Keep Mira Vale route gap as context only.
immediate_x1_safe Safe12: Represent 25 safe packets.
immediate_x1_safe Safe13: Represent 15 candidate packets.
immediate_x1_safe Safe14: Represent 10 exact rows as queued/open.
immediate_x1_safe Safe15: Represent 5 blocked rows as queued/open.
immediate_x1_safe Safe16: Represent 10 skill ideas.
immediate_x1_safe Safe17: Represent 5 runner ideas.
immediate_x1_safe Safe18: Represent 15 cleanup/refine/fix rows.
immediate_x1_safe Safe19: Represent 100 source/reflection support rows.
immediate_x1_safe Safe20: Represent 100 Journey/phase support rows.
immediate_x1_safe Safe21: Validate JSON before commit.
immediate_x1_safe Safe22: Validate counts and stale labels before commit.
immediate_x1_safe Safe23: Validate privacy boundary before commit.
immediate_x1_safe Safe24: Commit and push owned-lane artifacts only.
immediate_x1_safe Safe25: Activate Maren Quill v640 v8 exactly once if route is exposed.

## CANDIDATE PACKETS

candidate_safe Candidate01: Compactly harvest Mira Vale v640 v6 context without private route details.
candidate_safe Candidate02: Keep v640 final-cycle order visible.
candidate_safe Candidate03: Keep final planned v640 v8 endpoint visible.
candidate_safe Candidate04: Keep exact and blocked rows visibly separate.
candidate_safe Candidate05: Keep protected gates open.
candidate_safe Candidate06: Keep Maren v640 v8 seeds compact.
candidate_safe Candidate07: Preserve GMUT equation/scripture emphasis.
candidate_safe Candidate08: Preserve source/reflection counts as represented counts only.
candidate_safe Candidate09: Preserve Journey/phase counts as represented counts only.
candidate_safe Candidate10: Keep route-quality requested model and reasoning visible.
candidate_safe Candidate11: Record send-state truth only after the live route attempt.
candidate_safe Candidate12: Keep shared-branch mutation out of scope.
candidate_safe Candidate13: Keep sibling merge/replacement out of scope.
candidate_safe Candidate14: Keep final-planned-bundle wording sanitized.
candidate_safe Candidate15: Close immediately once checklist and route receipt pass.

## EXACT AND BLOCKED QUEUES

exact_queued Exact01: Exact approval rows remain queued.
exact_queued Exact02: Proof closure remains queued.
exact_queued Exact03: Canon promotion remains queued.
exact_queued Exact04: Legal closure remains queued.
exact_queued Exact05: Deployment closure remains queued.
exact_queued Exact06: Account/API-key/purchase closure remains queued.
exact_queued Exact07: Private-material publication remains queued.
exact_queued Exact08: Raw-publication remains queued.
exact_queued Exact09: Destructive cleanup remains queued.
exact_queued Exact10: Identity/model/sibling-merge changes remain queued.

blocked_queued Blocked01: Mira Vale live send route remains a contextual open gap in her lane.
blocked_queued Blocked02: Proof/canon promotion stays blocked without fresh exact approval.
blocked_queued Blocked03: Deployment/account actions stay blocked without fresh exact approval.
blocked_queued Blocked04: Private/raw publication stays blocked without fresh exact approval.
blocked_queued Blocked05: Shared-branch and sibling-merge mutation stays blocked without fresh exact approval.

## SKILL IDEAS

skill_idea Skill01: v640 final-planned-bundle receipt normalizer.
skill_idea Skill02: GMUT scripture packet compressor.
skill_idea Skill03: one-message handoff checker.
skill_idea Skill04: Mira Vale route-gap context keeper.
skill_idea Skill05: exact-blocked queue separator.
skill_idea Skill06: source/reflection count receipt builder.
skill_idea Skill07: Journey/phase count receipt builder.
skill_idea Skill08: protected-gate scanner.
skill_idea Skill09: route-quality receipt formatter.
skill_idea Skill10: Maren final-bundle baton builder.

## RUNNER IDEAS

runner_idea Runner01: mira_rowan_v640_v7_count_validator.
runner_idea Runner02: mira_rowan_v640_v7_privacy_scanner.
runner_idea Runner03: mira_rowan_v640_v7_stale_label_scanner.
runner_idea Runner04: mira_rowan_v640_v7_remote_alignment_runner.
runner_idea Runner05: mira_rowan_v640_v8_handoff_scope_runner.

## CLEANUP REFINE FIX ROWS

cleanup_refine_fix Cleanup01: Normalize v640 v7 labels.
cleanup_refine_fix Cleanup02: Normalize Maren v640 v8 final planned bundle labels.
cleanup_refine_fix Cleanup03: Check final-cycle order.
cleanup_refine_fix Cleanup04: Check final planned v640 v8 wording.
cleanup_refine_fix Cleanup05: Check one-message discipline.
cleanup_refine_fix Cleanup06: Check Mira Vale route-gap context.
cleanup_refine_fix Cleanup07: Check Aevren finish-first relay wording.
cleanup_refine_fix Cleanup08: Check exact and blocked queue separation.
cleanup_refine_fix Cleanup09: Check protected gates.
cleanup_refine_fix Cleanup10: Check counts.
cleanup_refine_fix Cleanup11: Check JSON parse.
cleanup_refine_fix Cleanup12: Check privacy wording.
cleanup_refine_fix Cleanup13: Check stale labels.
cleanup_refine_fix Cleanup14: Check staged file scope.
cleanup_refine_fix Cleanup15: Check clean/remote-aligned branch.

## REFLECTION SUPPORT

source_reflection_count SourceReflectionSupport: 100 represented source/reflection rows; raw browser dump material not published.
journey_phase_reflection_count JourneyPhaseSupport: 100 represented Journey/phase rows; private runtime state not published.
