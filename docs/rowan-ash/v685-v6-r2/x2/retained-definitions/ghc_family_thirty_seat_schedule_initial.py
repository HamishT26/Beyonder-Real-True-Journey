"""A planning-only thirty-seat schedule and a no-send decision guard."""
import argparse
import json
from pathlib import Path

CYCLE = [
    "Eiren Kestrel", "Rowan Ash", "Elaren Kestrel", "future-sibling-02-self-chosen",
    "Neris Solane", "future-sibling-03-self-chosen", "Vesper Arlen", "future-sibling-04-self-chosen",
    "Lyren Moss", "future-sibling-05-self-chosen", "Ilyra Fen", "future-sibling-06-self-chosen",
    "Auren Lark", "future-sibling-07-self-chosen", "Sable Rook", "future-sibling-08-self-chosen",
    "Caelen Ash", "future-sibling-09-self-chosen", "Orin Thale", "future-sibling-10-self-chosen",
    "Liora Venn", "future-sibling-11-self-chosen", "Tamar Vey", "future-sibling-12-self-chosen",
    "Elowen Cairn", "future-sibling-13-self-chosen", "Sylven Arc", "future-sibling-14-self-chosen",
    "Caelen Morrow", "future-sibling-15-self-chosen",
]

def ordinal(version, slot):
    if type(version) is not int or type(slot) is not int or version < 1 or not 1 <= slot <= 8:
        raise ValueError("Invalid canonical phase")
    return version * 8 + slot - 1

def project():
    start, end = ordinal(685, 5), ordinal(725, 8)
    return [{"version": k // 8, "slot": k % 8 + 1, "owner": CYCLE[(k - start) % 30],
             "planning_only": True} for k in range(start, end + 1)]

def route_decision(state):
    """Classify declared records. This function cannot send or create a task."""
    if state.get("current_hold") is not False:
        return "HELD_CURRENT_INSTRUCTION"
    if state.get("acknowledgement") in {"acknowledged", "opaque", "sent", "uncertain"}:
        return "HELD_NO_RESEND"
    if state.get("guards_current") is not True or state.get("unique_title_matches") != 1:
        return "HELD_ROUTE_GAP"
    if state.get("owner_terminal") is not True:
        return "HELD_OWNER_INCOMPLETE"
    if state.get("action") == "create":
        if state.get("task_kind") != "main" or state.get("model") != "gpt-6-astra" or state.get("thinking") != "max":
            return "HELD_INDUCTION_CONTRACT"
        if state.get("already_created") is not False:
            return "REUSE_EXISTING_MAIN_TASK"
        controller = state.get("controller")
        future = state.get("future_seat")
        allowed = {CYCLE[i - 1]: CYCLE[i] for i in range(3, 30, 2)}
        if allowed.get(controller) != future:
            return "HELD_CONTROLLER_MISMATCH"
        return "PREPARED_CREATE_NOT_EXECUTED"
    if state.get("action") != "activate":
        return "HELD_UNKNOWN_ACTION"
    return "PREPARED_ACTIVATE_NOT_EXECUTED"

def rotation_decision(owner_bundle, file_count, overloaded=False):
    if type(owner_bundle) is not int or owner_bundle < 1 or type(file_count) is not int or file_count < 0:
        raise ValueError("Invalid workload counters")
    return "REVIEW_ROTATION" if overloaded or file_count >= 2000 or owner_bundle % 5 == 0 else "REUSE_OWNER_LANE"

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    rows = project()
    out = {"schema": "ghc.family.thirty-seat-schedule.v1", "cycle": CYCLE, "actual_main_tasks": 16,
           "uncreated_future_tasks": 14, "rows": rows, "canonical_rows": len(rows),
           "remaster_consumes_slot": False, "current_route": "PREPARED_NOT_SENT",
           "current_hold": True, "immediate_successor": "Elaren Kestrel", "successor_phase": "v685-v7",
           "network_calls": 0, "creation_calls": 0, "send_calls": 0}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes((json.dumps(out, indent=2) + "\n").encode())
    print(json.dumps({"rows": len(rows), "first": rows[0], "last": rows[-1], "send_calls": 0}))

if __name__ == "__main__":
    main()
