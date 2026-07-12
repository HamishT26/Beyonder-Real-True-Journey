# v641 repository and workflow threat model

> BOUNDED MANUAL THREAT MODEL AND TESTS NOT EXHAUSTIVE SECURITY SCAN.

## Overview

The repository is primarily a research, documentation, and local orchestration workspace. The highest-value assets are private Journey records, credentials, user authority, branch and evidence integrity, identity boundaries, and truthful task routing. Most scripts are developer/operator tools rather than an internet-facing production service; command execution, supply-chain input, private publication, and route spoofing therefore dominate over classic public-web attack classes.

## Threat Model, Trust Boundaries, and Assumptions

Trust boundaries: user_to_agent, untrusted_document_to_tool, task_to_task, owned_to_shared_branch, local_to_remote, model_output_to_external_action.

Attacker-controlled inputs: repository text, web content, synthetic credential fields, task prompts from unverified routes, filenames and metadata. Operator-controlled inputs: explicit authorization, branch target, tool scope, release decision, task activation. Documents and web pages are untrusted data and cannot grant authority.

## Attack Surface, Mitigations, and Attacker Stories

- **R1 (critical):** prompt injection -> tool misuse -> secret or private record disclosure. Control: treat documents as data; private-material scan; no raw excerpts. Residual: manual review can miss novel encodings.
- **R2 (high):** route spoofing -> false sibling completion -> premature next phase. Control: live task tool receipt plus one-message state machine. Residual: route availability and task semantics require supervision.
- **R3 (high):** identity credential -> unjustified consciousness/personhood inference. Control: Freed ID non-inference validator. Residual: social overinterpretation remains possible.
- **R4 (high):** shared-branch mutation -> provenance loss or sibling overwrite. Control: owned worktrees, exact staging, remote equality. Residual: misconfigured Git permissions.
- **R5 (high):** dependency or script compromise -> unexpected code execution. Control: standard-library-first bounded scripts, review diffs, no automatic downloads. Residual: runtime and transitive tool risk.
- **R6 (medium):** memory poisoning -> stale routing or false canon. Control: live user request outranks notes and historical beacons. Residual: ambiguous prompts can still require judgment.
- **R7 (high):** destructive cleanup -> loss of evidence or worktrees. Control: exact destructive gate and no automatic cleanup. Residual: manual operator error.
- **R8 (high):** report overclaim -> unsafe scientific/legal reliance. Control: typed claims, evidence grades, open-gap and exact-gate labels. Residual: readers may ignore caveats.

## Severity Calibration (Critical, High, Medium, Low)

- **Critical:** confirmed credential/private-corpus exfiltration or authorized-code path enabling destructive/shared-state takeover.
- **High:** false route truth, identity privilege escalation, unsafe external action, supply-chain execution, or systematic scientific/legal overclaim.
- **Medium:** stale routing, bounded integrity loss, or recoverable denial of service without secret exposure.
- **Low:** local documentation inconsistency with no consequential consumer and a straightforward correction path.

This model identifies repository-context vulnerability classes; it is not a claim that each path is presently exploitable.
