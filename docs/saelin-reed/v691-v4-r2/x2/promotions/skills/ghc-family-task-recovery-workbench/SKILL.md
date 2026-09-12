---
name: ghc-family-task-recovery-workbench
description: Evaluate exact_registry, control_precedence, history_evidence, recovery_plan. Use for bounded recovery-commons records with explicit evidence ceilings.
---

# ghc-family-task-recovery-workbench

Use the current family-index workflow and the newest direct user authorization. This merged skill supports four specific pure operations: exact_registry, control_precedence, history_evidence, recovery_plan. It does not send messages, start tasks, reset models or inspect private task history.

The public runner is under the D family global-tools root at family-recovery-commons/runners/task-recovery-workbench.txt. Its evaluate({operation,input}) interface returns {ok,error,value,authority:false}. Reject an operation outside this group. Inputs are JSON records with closed keys, bounded arrays, safe integer quantities and explicit missingness.

For a request file, use Node with the CommonJS text entrypoint and call the exported main function: node --input-type=commonjs -e "require(process.argv[1]).main(process.argv[2])" <runner.txt> <request.json>. Keep request and output files on D. The same pure interface is used by the local browser workbench.

Empty or partial history remains unknown. At a real terminal edge, inspect the exact native target and newest controls; recover through bounded supported reads while no submission is accepted. The companion family-recovery-commons/workflow-reviewer.txt reviews the v6 profile and route as data and never activates tasks.

The merge retains four local guides and 2 local runner callers, totaling 6 source units. The source closure and checks are recorded in the Saelin v691-v4-r2 x2 promotion receipt. All original callers remain available. Rollback is additive: retain these sources and select a verified prior caller for its original contract; do not overwrite unrelated skills or erase negative evidence.

Same-owner bounded software only. No consciousness, personhood, professional qualification, physical GMUT confirmation, production identity, independent reproduction, public authority or Maori authority is established. NOT_READY_FOR_STAGE_20.
