---
name: ghc-family-outbox-lifecycle-proof
description: Evaluate receipt_reduce, outbox_chain, product_reachability, checkpoint_replay. Use for bounded recovery-commons records with explicit evidence ceilings.
---

# ghc-family-outbox-lifecycle-proof

Use the current family-index workflow and the newest direct user authorization. This merged skill supports four specific pure operations: receipt_reduce, outbox_chain, product_reachability, checkpoint_replay. It does not send messages, start tasks, reset models or inspect private task history.

The public runner is under the D family global-tools root at family-recovery-commons/runners/outbox-lifecycle-proof.txt. Its evaluate({operation,input}) interface returns {ok,error,value,authority:false}. Reject an operation outside this group. Inputs are JSON records with closed keys, bounded arrays, safe integer quantities and explicit missingness.

For a request file, use Node with the CommonJS text entrypoint and call the exported main function: node --input-type=commonjs -e "require(process.argv[1]).main(process.argv[2])" <runner.txt> <request.json>. Keep request and output files on D. The same pure interface is used by the local browser workbench.

After an accepted or unresolved submission, retain its latch. A local view reset does not authorize resending. Digest chains and model counterexamples support inspection but do not prove live delivery.

The merge retains four local guides and 3 local runner callers, totaling 7 source units. The source closure and checks are recorded in the Saelin v691-v4-r2 x2 promotion receipt. All original callers remain available. Rollback is additive: retain these sources and select a verified prior caller for its original contract; do not overwrite unrelated skills or erase negative evidence.

Same-owner bounded software only. No consciousness, personhood, professional qualification, physical GMUT confirmation, production identity, independent reproduction, public authority or Maori authority is established. NOT_READY_FOR_STAGE_20.
