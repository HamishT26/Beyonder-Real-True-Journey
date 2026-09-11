# Current novelty correction and two additional frozen cases

This fourteenth module is the controlling correction to the first prepared thirteen-module edition. The original edition and failed preflight are retained externally, and every original module file remains byte-for-byte unchanged. Earlier statements about 200 new records and the old totals describe that prepared epoch. The current corrected figures below supersede those interpretations prospectively.

The component preflight passed 34 of 35 checks and all 65 selected tests, but found only 198 distinct normalized request inputs among 200 original proposal records. MF6903R2-027 and MF6903R2-028 repeat the same dispatch input as MF6903R2-026. All three executions and their outcomes remain in the frozen x1 evidence. The two repeated records receive zero new novelty credit. Their existence is not concealed by a changed identifier or a rewritten plan.

Two additional conjunctions were defined and hash-bound before execution. They use the existing dispatch evaluator without changing its implementation. One combines an opaque accepted send with a later cleanliness failure and pause; the other combines an acknowledged send with a later uniqueness failure and pause. Both must remain terminal with may_submit=false. A later change in prerequisites cannot justify resending a previously accepted message.

There are now 202 retained core records and 200 distinct newly credited inputs. The retained execution dispositions are 192 completed and ten represented. After excluding the two repeated novelty records, the credited core dispositions remain 190 completed and ten represented. This is a count of bounded contract inputs within twenty operation families, not two hundred independent algorithms or scientific discoveries. Core safe executions total 202, candidate subjects and their guards total 202 each, and the eight other supplementary safe tasks remain separate. Total safe executions are 210.

## MF6903R2-201 — Opaque accepted delivery remains terminal after cleanliness and pause change

Exercise a previously unrepresented conjunction of accepted-send history and changed present prerequisites without enabling a resend.

The frozen request is:

```json
{
  "op": "dispatch_state",
  "payload": {
    "canonical": true,
    "clean": false,
    "unique": true,
    "guard": "pause",
    "send": "opaque_accepted"
  }
}
```

The full expected and observed envelope is:

```json
{
  "ok": true,
  "error": null,
  "value": {
    "state": "sent_opaque_no_resend",
    "may_submit": false
  }
}
```

The paired undeclared-authority subject was refused with unknown_field and retains zero original success credit. The actual input was unchanged. The definition digest is 46e9ce53f005449caf8623dcdcb286f0d4e2c434b1a76e7870b582dc7eda685a.

## MF6903R2-202 — Acknowledged delivery remains terminal after uniqueness and pause change

Exercise a previously unrepresented conjunction of accepted-send history and changed present prerequisites without enabling a resend.

The frozen request is:

```json
{
  "op": "dispatch_state",
  "payload": {
    "canonical": true,
    "clean": true,
    "unique": false,
    "guard": "pause",
    "send": "acknowledged"
  }
}
```

The full expected and observed envelope is:

```json
{
  "ok": true,
  "error": null,
  "value": {
    "state": "sent_acknowledged",
    "may_submit": false
  }
}
```

The paired undeclared-authority subject was refused with unknown_field and retains zero original success credit. The actual input was unchanged. The definition digest is 42da25db70fa3df9b77f4a27412d1683f8c59f32c0bb8151d80490c3c008a3c9.

## Corrected accounting

The two new safe/subject/guard triples add six direct witnesses. The retained preflight failure and focused uniqueness recovery add two more. Two method records describe the correction and its new conjunction cases. A third method retains an authoring-script parse failure and its focused syntax recovery, adding three more witnesses: two failed attempts and one passing trusted syntax check. The current owner totals are 52 methods and 1,084 direct witnesses: 259 failed and 825 passing, with 49 validated methods and three candidates.

All failed execution witnesses remain counted. For the effective unique-negative calculation only, the two repeated candidate subjects 027 and 028 are aliases of the identical subject 026 and are excluded once each. This gives 257 unique failed subjects plus thirty blocked packets, or 287 effective negatives. The earlier x2 total of 284 remains preserved at its own epoch. The inherited source totals are unchanged; current cumulative totals are 215 methods, 5,779 direct witnesses, 1,580 failed, 4,199 passing and 1,927 effective negatives.

The original 219-card x2 deck remains unchanged. Two new tier-four correction cards join it in final/current-deck-index.json, producing 221 current indexed cards. The two original repeated proposal cards remain visible, with zero new novelty eligibility in the current index. No earlier card is deleted or rehashed.

The failed aggregate preflight is not replayed. Focused checks cover the changed novelty, accounting, card, baton, content-seal, privacy and syntax surfaces. The 65-test inventory is preserved. The first exact-final canonical is still a separate terminal action after the new final is pushed and fresh equality passes. Actual canonical and Auren delivery results remain external.

This correction strengthens the source-faithful ledger by making a counted defect visible and repairing the actual uniqueness floor. It grants no independent reproduction, physical GMUT confirmation, identity continuity, consciousness, ASI or authority. NOT_READY_FOR_STAGE_20.
