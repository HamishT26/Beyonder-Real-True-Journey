"""Named evidence contracts with explicit accepted and adverse local fixtures.

Every result is a bounded local software check. Metadata rules do not verify the
world described by the metadata. No evaluation of code or network retrieval is used.
"""
import argparse
import copy
import hashlib
import json
import math
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from zoneinfo import ZoneInfo
from ghc_family_unit_fraction_witness import verify
from ghc_family_thirty_seat_schedule import CYCLE, project, route_decision, rotation_decision

RULES = []
def register(family, good, change, predicate, purpose):
    bad = copy.deepcopy(good)
    bad.update(change)
    index = sum(r["family"] == family for r in RULES)
    RULES.append({"family": family, "rule_index": index, "good": good, "bad": bad,
                  "predicate": predicate, "purpose": purpose})

def integer(n):
    return type(n) is int

def finite(n):
    return type(n) in (int, float) and math.isfinite(n)

def stamp(s):
    value = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("Timezone required")
    return value

def digest(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def acyclic(nodes, edges):
    if len(nodes) != len(set(nodes)) or any(a not in nodes or b not in nodes for a, b in edges):
        return False
    colors = {}
    def walk(node):
        if colors.get(node) == 1:
            return False
        if colors.get(node) == 2:
            return True
        colors[node] = 1
        for a, b in edges:
            if a == node and not walk(b):
                return False
        colors[node] = 2
        return True
    return all(walk(n) for n in nodes)

DIMS = {"m": [0, 1, 0], "s": [0, 0, 1], "kg": [1, 0, 0],
        "N": [1, 1, -2], "J": [1, 2, -2], "Pa": [1, -1, -2], "1": [0, 0, 0]}
register("units", {"unit": "J", "dimension": [1, 2, -2]}, {"unit": "N"},
         lambda d: DIMS[d["unit"]] == d["dimension"], "Compare declared dimensions against the unit dictionary")
register("units", {"force": "N", "energy": "J"}, {"energy": "N"},
         lambda d: DIMS[d["force"]] != DIMS[d["energy"]], "Do not conflate force with energy")
register("units", {"dimension": [0,0,0], "source_type": "Shannon_bits", "target_type": "Shannon_bits"}, {"target_type": "experience"},
         lambda d: d["dimension"] == [0,0,0] and d["source_type"] == d["target_type"], "Keep the semantic type of a dimensionless quantity")
register("units", {"a": [1,1,-2], "b": [0,1,0], "product": [1,2,-2]}, {"product": [1,1,-2]},
         lambda d: [a+b for a,b in zip(d["a"],d["b"], strict=True)] == d["product"], "Add exponents for multiplication")
register("units", {"a": [1,2,-2], "b": [0,3,0], "ratio": [1,-1,-2]}, {"ratio": [1,5,-2]},
         lambda d: [a-b for a,b in zip(d["a"],d["b"], strict=True)] == d["ratio"], "Subtract exponents for division")
register("units", {"dimension": [0,1,0], "power": 3, "result": [0,3,0]}, {"result": [0,1,0]},
         lambda d: [a*d["power"] for a in d["dimension"]] == d["result"], "Scale dimensions for powers")
register("units", {"celsius": 20, "kelvin": 293.15, "offset": 273.15}, {"offset": 0},
         lambda d: math.isclose(d["celsius"]+d["offset"], d["kelvin"], abs_tol=1e-9) and d["offset"] == 273.15, "Retain the affine temperature offset")
register("units", {"natural_units": True, "constants_set_to_one": ["c","hbar"], "conversion": "SI_to_natural_explicit"},
         {"conversion": ""}, lambda d: not d["natural_units"] or bool(d["constants_set_to_one"] and d["conversion"]), "Record conversion assumptions")
register("units", {"curvature": [0,-2,0], "stress": [1,-1,-2], "coupling": [-1,-1,2]},
         {"coupling": [0,0,0]}, lambda d: [a+b for a,b in zip(d["stress"],d["coupling"],strict=True)] == d["curvature"], "Require a dimensionally compatible coupling scale")
register("units", {"unit": "Pa"}, {"unit": "psyche_energy"},
         lambda d: d["unit"] in DIMS, "Reject unknown symbols rather than invent units")

register("uncertainty", {"u": 0.2}, {"u": -0.2}, lambda d: finite(d["u"]) and d["u"] >= 0, "Standard uncertainty is nonnegative")
register("uncertainty", {"matrix": [[1,.2],[.2,2]]}, {"matrix": [[1,.2],[.3,2]]},
         lambda d: d["matrix"][0][1] == d["matrix"][1][0], "Retain covariance symmetry")
register("uncertainty", {"matrix": [[1,.2],[.2,2]]}, {"matrix": [[1,2],[2,1]]},
         lambda d: d["matrix"][0][0]>=0 and d["matrix"][1][1]>=0 and d["matrix"][0][1]==d["matrix"][1][0] and d["matrix"][0][0]*d["matrix"][1][1]>=d["matrix"][0][1]**2, "Check the two-variable positive semidefinite condition")
register("uncertainty", {"rho": -.8}, {"rho": 1.2}, lambda d: finite(d["rho"]) and -1<=d["rho"]<=1, "Bound a correlation coefficient")
register("uncertainty", {"j": [2,3], "cov": [[1,.5],[.5,4]], "variance": 46},
         {"variance": 40}, lambda d: math.isclose(sum(d["j"][i]*d["cov"][i][j]*d["j"][j] for i in range(2) for j in range(2)),d["variance"]), "Include both cross covariance terms in propagation")
register("uncertainty", {"k": 2, "interpretation": "approximately_95_percent_normal_assumption"},
         {"interpretation": ""}, lambda d: finite(d["k"]) and d["k"]>0 and bool(d["interpretation"]), "Carry a coverage interpretation")
register("uncertainty", {"low": 1.2, "high": 1.8}, {"low": 2},
         lambda d: finite(d["low"]) and finite(d["high"]) and d["low"]<=d["high"], "Order interval endpoints")
register("uncertainty", {"dof": 9}, {"dof": 0}, lambda d: finite(d["dof"]) and d["dof"]>0, "Positive degrees of freedom")
register("uncertainty", {"u": 0, "exact_quantity": True}, {"exact_quantity": False},
         lambda d: d["u"]>0 or (d["u"]==0 and d["exact_quantity"] is True), "Zero uncertainty has a declared exact origin")
register("uncertainty", {"value": 1.23456, "rounded": 1.235, "uncertainty": .01},
         {"rounded": 1.2}, lambda d: d["uncertainty"]>0 and abs(d["value"]-d["rounded"])<=d["uncertainty"]/10, "Do not round away the uncertainty scale")

register("time", {"event": "2026-07-23T23:21:02Z"}, {"event": "2026-07-23T23:21:02"},
         lambda d: stamp(d["event"]).utcoffset() is not None, "Require an offset for an instant")
register("time", {"event": "2026-07-23T23:21:02Z", "retrieval": "2026-09-05T07:00:00Z"},
         {"retrieval": "2026-07-20T07:00:00Z"}, lambda d: stamp(d["event"])<=stamp(d["retrieval"]), "Retrieval cannot precede the source event in this record")
register("time", {"utc": "2026-07-23T23:21:02Z", "nz_date": "2026-07-24"},
         {"nz_date": "2026-07-23"}, lambda d: stamp(d["utc"]).astimezone(ZoneInfo("Pacific/Auckland")).date().isoformat()==d["nz_date"], "Derive the New Zealand calendar date")
register("time", {"expiry": "2026-09-06T00:00:00Z", "observed": "2026-09-05T00:00:00Z"},
         {"observed": "2026-09-07T00:00:00Z"}, lambda d: stamp(d["observed"])<stamp(d["expiry"]), "Check expiry against the stated observation")
register("time", {"start": 10.5, "end": 12.0}, {"end": 8.0},
         lambda d: finite(d["start"]) and finite(d["end"]) and d["end"]>=d["start"], "Elapsed intervals are nonnegative")
register("time", {"precision": "date", "source": "2026-09-05", "instant": None},
         {"instant": "2026-09-05T00:00:00Z"}, lambda d: d["precision"]!="date" or d["instant"] is None, "A date-only source does not supply an instant")
register("time", {"elapsed_clock": "monotonic", "elapsed_seconds": 2.3},
         {"elapsed_clock": "civil"}, lambda d: d["elapsed_clock"]=="monotonic" and d["elapsed_seconds"]>=0, "Use monotonic time for elapsed measurement")
register("time", {"source_deadline": None, "reported_deadline": None},
         {"reported_deadline": "2026-08-05"}, lambda d: d["reported_deadline"]==d["source_deadline"], "A blank deadline stays blank")
register("time", {"original": "2026-08-06T18:46:04Z", "correction": "2026-09-05T07:00:00Z"},
         {"correction": "2026-07-05T07:00:00Z"}, lambda d: stamp(d["correction"])>=stamp(d["original"]), "Preserve event order")
register("time", {"a": "2026-07-23T23:21:02Z", "b": "2026-07-24T11:21:02+12:00"},
         {"b": "2026-07-24T11:21:02Z"}, lambda d: stamp(d["a"])==stamp(d["b"]), "Offset conversion preserves the instant")

register("field", {"rank": 2, "indices": ["A","B"]}, {"indices": ["A"]},
         lambda d: integer(d["rank"]) and len(d["indices"])==d["rank"], "Declare tensor rank and indices")
register("field", {"components": [[1,2],[2,3]]}, {"components": [[1,2],[4,3]]},
         lambda d: d["components"][0][1]==d["components"][1][0], "Check symmetric component declarations")
register("field", {"alpha": 2, "d_alpha": 0, "xi": 3, "d_xi": 5, "derivative": 10},
         {"derivative": 16}, lambda d: d["d_alpha"]==0 and d["derivative"]==d["alpha"]*d["d_xi"], "Apply a constant-coupling product rule")
register("field", {"alpha": 2, "d_alpha": 7, "xi": 3, "d_xi": 5, "derivative": 31},
         {"derivative": 10}, lambda d: d["derivative"]==d["d_alpha"]*d["xi"]+d["alpha"]*d["d_xi"], "Retain the derivative of a variable coupling")
register("field", {"matter_exchange": 4, "reported_exchange": 4}, {"reported_exchange": 0},
         lambda d: d["matter_exchange"]==d["reported_exchange"], "Preserve nonzero matter exchange")
register("field", {"geometry": "flat_component_example", "claim": "flat_component_identity"},
         {"claim": "general_curved_covariance"}, lambda d: d["geometry"]=="flat_component_example" and d["claim"]=="flat_component_identity", "Do not promote flat derivatives")
register("field", {"omega_m": 0, "omega_r": 0, "alpha_xi": 0, "residual": 0},
         {"omega_m": 1}, lambda d: d["omega_m"]+d["omega_r"]-d["alpha_xi"]==d["residual"]==0, "Check the declared general relativity limit")
register("field", {"bridge_defined": False, "status": "open_gap"}, {"status": "empirically_validated"},
         lambda d: d["bridge_defined"] is False and d["status"]=="open_gap", "Undefined bridge terms retain the observable gap")
register("field", {"action_dimension": "energy_times_time", "dependencies": ["metric","matter","bridge"]},
         {"dependencies": []}, lambda d: d["action_dimension"]=="energy_times_time" and bool(d["dependencies"]), "Record action dimensions and field dependencies")
register("field", {"result": "consistency_identity", "evidence": "mathematical_local"},
         {"evidence": "empirical_confirmation"}, lambda d: d["result"]=="consistency_identity" and d["evidence"]=="mathematical_local", "Keep algebraic and empirical evidence distinct")

register("numeric", {"left": [1,3], "right": [2,6]}, {"right": [333333,1000000]},
         lambda d: Fraction(*d["left"])==Fraction(*d["right"]), "Use exact rational equality")
register("numeric", {"decimal_places": 50}, {"decimal_places": 0},
         lambda d: integer(d["decimal_places"]) and 15<=d["decimal_places"]<=1000, "Declare a bounded arbitrary precision")
register("numeric", {"relative": 1e-8, "absolute": 1e-12}, {"absolute": None},
         lambda d: finite(d["relative"]) and finite(d["absolute"]) and d["relative"]>=0 and d["absolute"]>0, "Pair relative tolerance with an absolute scale")
register("numeric", {"values": [1,2.5,0]}, {"values": [1,"Infinity"]},
         lambda d: all(finite(x) for x in d["values"]), "Reject nonfinite or nonnumeric values")
register("numeric", {"reference": [1,10], "observed": .1, "abs_tol": 1e-12}, {"observed": 0},
         lambda d: abs(float(Fraction(*d["reference"]))-d["observed"])<=d["abs_tol"], "Compare cancellation-sensitive results to an exact reference")
register("numeric", {"coefficients": [1,0,3], "derivative": [0,6]}, {"derivative": [0,3]},
         lambda d: [i*c for i,c in enumerate(d["coefficients"]) if i] == d["derivative"], "Differentiate the polynomial coefficient sequence")
register("numeric", {"measured": 8, "predicted": 5, "convention": "measured_minus_predicted", "residual": 3},
         {"residual": -3}, lambda d: d["convention"]=="measured_minus_predicted" and d["residual"]==d["measured"]-d["predicted"], "Retain the residual sign convention")
register("numeric", {"n": 8}, {"n": True},
         lambda d: integer(d["n"]) and d["n"]>0, "Reject booleans as integer domain values")
register("numeric", {"seeds": [4,4], "independent_reproductions": 0}, {"independent_reproductions": 2},
         lambda d: d["seeds"]==[4,4] and d["independent_reproductions"]==0, "Repeated seeded runs are not independent reproduction")
register("numeric", {"tested": [3,1000], "reported": [3,1000], "universal": False}, {"universal": True},
         lambda d: d["tested"]==d["reported"] and d["universal"] is False, "Report the actual finite range")

register("correspondence", {"message_type": "attendance_selection", "claim": "application_selected_to_attend"},
         {"claim": "scientific_theory_endorsed"}, lambda d: d["message_type"]=="attendance_selection" and d["claim"]=="application_selected_to_attend", "Bound an attendance claim")
register("correspondence", {"message_type": "registration_reminder", "attended": None}, {"attended": True},
         lambda d: d["message_type"]=="registration_reminder" and d["attended"] is None, "A reminder does not prove attendance")
register("correspondence", {"release_reason": "registration_unclaimed", "travel_reason_source": "user_report"},
         {"travel_reason_source": "email_verified"}, lambda d: d["release_reason"]=="registration_unclaimed" and d["travel_reason_source"]=="user_report", "Separate recorded release from attributed travel reason")
register("correspondence", {"scholarship_text": "not_offered", "scholarship_awarded": False}, {"scholarship_awarded": True},
         lambda d: d["scholarship_text"]=="not_offered" and d["scholarship_awarded"] is False, "Follow the explicit scholarship statement")
register("correspondence", {"cohort_evidence": None, "nz_unique": None}, {"nz_unique": True},
         lambda d: d["cohort_evidence"] is None and d["nz_unique"] is None, "Keep national uniqueness unestablished")
register("correspondence", {"review_record": None, "repository_review_confirmed": False}, {"repository_review_confirmed": True},
         lambda d: d["review_record"] is None and d["repository_review_confirmed"] is False, "Do not invent a repository review")
register("correspondence", {"support_acknowledged": True, "technical_endorsement": False}, {"technical_endorsement": True},
         lambda d: d["support_acknowledged"] is True and d["technical_endorsement"] is False, "Support acknowledgement retains its narrow meaning")
register("correspondence", {"channel": "community_digest", "evidence_class": "community_material"},
         {"evidence_class": "official_validation"}, lambda d: d["channel"]=="community_digest" and d["evidence_class"]=="community_material", "Classify community mail separately")
register("correspondence", {"shared_keys": ["subject","event_date","bounded_summary"]},
         {"shared_keys": ["subject","invitation_url"]}, lambda d: set(d["shared_keys"])<={"subject","event_date","bounded_summary"}, "Exclude private invitation routes")
register("correspondence", {"source_nz_date": "2026-07-24", "reported_nz_date": "2026-07-24"},
         {"reported_nz_date": "approximately_two_weeks_ago"}, lambda d: d["source_nz_date"]==d["reported_nz_date"], "Prefer verified dates to approximate recollection")

register("lifecycle", {"revision": "1"*40}, {"revision": "main"},
         lambda d: len(d["revision"])==40 and all(c in "0123456789abcdef" for c in d["revision"]), "Bind an immutable revision")
register("lifecycle", {"status": "retracted", "retained": True}, {"retained": False},
         lambda d: d["status"]!="retracted" or d["retained"] is True, "Retain retracted history")
register("lifecycle", {"correction": "b", "predecessor": "a", "retained_ids": ["a","b"]},
         {"retained_ids": ["b"]}, lambda d: d["predecessor"] in d["retained_ids"] and d["correction"] in d["retained_ids"], "Link correction and retained predecessor")
register("lifecycle", {"status": "superseded", "replacement": "new_revision"}, {"replacement": None},
         lambda d: d["status"]!="superseded" or bool(d["replacement"]), "Name a superseding replacement")
register("lifecycle", {"locator_works": False, "status": "open_gap"}, {"status": "completed"},
         lambda d: d["locator_works"] is False and d["status"]=="open_gap", "Keep broken source locations explicit")
register("lifecycle", {"archived": True, "event_date": "2026-01-14"}, {"event_date": None},
         lambda d: not d["archived"] or bool(d["event_date"]), "Retain historical dates")
register("lifecycle", {"source_claims": ["A","B"], "summary_claims": ["A"]}, {"summary_claims": ["A","C"]},
         lambda d: set(d["summary_claims"])<=set(d["source_claims"]), "A summary cannot add unsupported claims")
register("lifecycle", {"lines_read": [1,100], "entire_document": False}, {"entire_document": True},
         lambda d: d["lines_read"]==[1,100] and d["entire_document"] is False, "Preserve partial-read coverage")
register("lifecycle", {"source": "retained text", "cached_digest": digest("retained text")}, {"source": "changed text"},
         lambda d: digest(d["source"])==d["cached_digest"], "Invalidate changed source content")
register("lifecycle", {"source_status": "active", "checked_at": "2026-09-05T00:00:00Z", "reuse_at": "2026-09-05T01:00:00Z"},
         {"checked_at": "2026-08-01T00:00:00Z"}, lambda d: d["source_status"]=="active" and 0<=(stamp(d["reuse_at"])-stamp(d["checked_at"])).total_seconds()<=86400, "Bound the freshness of a source-status observation")

register("attribution", {"author": "Example Researcher", "publisher": "Example Journal", "roles_separate": True}, {"roles_separate": False},
         lambda d: bool(d["author"]) and bool(d["publisher"]) and d["roles_separate"] is True, "Record author and publisher roles")
register("attribution", {"institution_named": "Example Institute", "endorsement_record": None, "endorsed": False}, {"endorsed": True},
         lambda d: d["endorsement_record"] is None and d["endorsed"] is False, "Institution naming is not endorsement")
register("attribution", {"claim": "attributed proposition", "speaker": "historical speaker"}, {"speaker": ""},
         lambda d: bool(d["claim"]) and bool(d["speaker"]), "Keep the quoted speaker")
register("attribution", {"kind": "newsletter", "peer_review_receipt": None}, {"peer_review_receipt": "inferred_from_newsletter"},
         lambda d: d["kind"]=="newsletter" and d["peer_review_receipt"] is None, "A newsletter supplies no review receipt")
register("attribution", {"publication": "preprint", "result": "claim_pending_review"}, {"result": "accepted_proof"},
         lambda d: d["publication"]=="preprint" and d["result"]=="claim_pending_review", "Retain preprint status")
register("attribution", {"source": "Hamish report", "attributed": True}, {"attributed": False},
         lambda d: d["source"]=="Hamish report" and d["attributed"] is True, "Attribute user-reported details")
register("attribution", {"read_scope": "title_only", "evidence_class": "unassessed"}, {"evidence_class": "validated"},
         lambda d: d["read_scope"]=="title_only" and d["evidence_class"]=="unassessed", "Titles do not establish evidence quality")
register("attribution", {"source_type": "vocabulary", "observations": 0}, {"observations": 1},
         lambda d: d["source_type"]=="vocabulary" and d["observations"]==0, "A vocabulary is not an observation")
register("attribution", {"source_qualifier": "may", "translation_qualifier": "may"}, {"translation_qualifier": "certainly"},
         lambda d: d["source_qualifier"]==d["translation_qualifier"], "Retain uncertainty in translation")
register("attribution", {"citation_present": True, "source_support": False, "claim_supported": False}, {"claim_supported": True},
         lambda d: d["source_support"] is d["claim_supported"], "Check agreement rather than citation presence")

register("claims", {"class": "synthetic", "requested": "synthetic", "independent_record": None}, {"requested": "empirical"},
         lambda d: d["requested"]==d["class"], "No evidence-class promotion without another record")
register("claims", {"before": "represented", "after_formatting": "represented"}, {"after_formatting": "completed"},
         lambda d: d["before"]==d["after_formatting"], "Formatting preserves evidence authority")
register("claims", {"origin": "synthetic", "exported_class": "synthetic"}, {"exported_class": "observed_real"},
         lambda d: d["origin"]==d["exported_class"], "Export preserves synthetic provenance")
register("claims", {"parser_passed": True, "proposition_validated": False}, {"proposition_validated": True},
         lambda d: d["parser_passed"] is True and d["proposition_validated"] is False, "Parser success is not proposition validation")
register("claims", {"reviewer": "independent_reviewer", "owner": "owner", "record": "review_receipt"},
         {"reviewer": "owner"}, lambda d: d["reviewer"]!=d["owner"] and bool(d["record"]), "Require a distinct attributed reviewer and record")
register("claims", {"owner": "owner", "replay_owner": "owner", "independent": False}, {"independent": True},
         lambda d: d["owner"]==d["replay_owner"] and d["independent"] is False, "Same-owner replay remains attributed")
register("claims", {"software_passed": True, "personhood_established": False}, {"personhood_established": True},
         lambda d: d["software_passed"] is True and d["personhood_established"] is False, "Do not infer personhood from tests")
register("claims", {"observed": "fail", "reported": "fail", "success_credit": 0}, {"reported": "pass"},
         lambda d: d["observed"]==d["reported"] and d["success_credit"]==0, "Retain a failed result without success credit")
register("claims", {"supported": ["a","b"], "compound": ["a","b"]}, {"compound": ["a","b","c"]},
         lambda d: set(d["compound"])<=set(d["supported"]), "Expose unsupported compound subclaims")
register("claims", {"evidence": ["supports","contradicts"], "decision": "abstain"}, {"decision": "confirmed"},
         lambda d: not ({"supports","contradicts"}<=set(d["evidence"])) or d["decision"]=="abstain", "Conflicting evidence requires abstention")

register("graph", {"entity_type": "entity", "activity_type": "activity"}, {"activity_type": "entity"},
         lambda d: d["entity_type"]=="entity" and d["activity_type"]=="activity", "Separate provenance node types")
register("graph", {"derived": "new", "source": "old", "edge": ["new","old"]}, {"edge": ["old","new"]},
         lambda d: d["edge"]==[d["derived"],d["source"]], "Preserve derivation direction")
register("graph", {"nodes": ["a","b"], "edges": [["b","a"]]}, {"edges": [["b","c"]]},
         lambda d: all(a in d["nodes"] and b in d["nodes"] for a,b in d["edges"]), "Reject orphan references")
register("graph", {"nodes": ["a","b","c"], "edges": [["b","a"],["c","b"]]},
         {"edges": [["b","a"],["a","b"]]}, lambda d: acyclic(d["nodes"],d["edges"]), "Detect directed provenance cycles")
register("graph", {"digests": ["abc","abc","def"], "evidence_units": 2}, {"evidence_units": 3},
         lambda d: len(set(d["digests"]))==d["evidence_units"], "Equivalent copies do not multiply credit")
register("graph", {"context_loader": "offline_allowlist", "network_requests": 0}, {"context_loader": "default_network"},
         lambda d: d["context_loader"]=="offline_allowlist" and d["network_requests"]==0, "Declare offline JSON LD context loading")
register("graph", {"parse_argument": "data", "format": "turtle"}, {"parse_argument": "location"},
         lambda d: d["parse_argument"]=="data" and d["format"]=="turtle", "Parse inline RDF fixtures")
register("graph", {"imports": False, "javascript": False, "advanced": False}, {"imports": True},
         lambda d: all(d[k] is False for k in ["imports","javascript","advanced"]), "Keep the SHACL fixture execution profile bounded")
register("graph", {"number": 42, "canonical_domain": "JCS_safe_integer"}, {"number": 9007199254740992},
         lambda d: integer(d["number"]) and abs(d["number"])<=9007199254740991 and d["canonical_domain"]=="JCS_safe_integer", "Respect the declared JCS integer domain")
register("graph", {"label_type": "blank_node", "enduring_identity": False}, {"enduring_identity": True},
         lambda d: d["label_type"]=="blank_node" and d["enduring_identity"] is False, "Blank-node labels have no enduring identity claim")

register("preregister", {"frozen_at": 10, "execution_at": 20}, {"frozen_at": 30},
         lambda d: d["frozen_at"]<d["execution_at"], "Freeze the hypothesis before execution")
register("preregister", {"falsifier": "adverse_case_accepted", "results_seen": False}, {"falsifier": ""},
         lambda d: bool(d["falsifier"]) and d["results_seen"] is False, "Declare an adverse outcome before results")
register("preregister", {"primary": ["accuracy"], "secondary": ["latency"]}, {"secondary": ["accuracy"]},
         lambda d: bool(d["primary"]) and set(d["primary"]).isdisjoint(d["secondary"]), "Separate primary and secondary outcomes")
register("preregister", {"population": "synthetic contract fixtures"}, {"population": ""},
         lambda d: bool(d["population"].strip()), "Name the analysis population")
register("preregister", {"stopping_rule": "fixed_200_cases", "declared_before": True}, {"declared_before": False},
         lambda d: bool(d["stopping_rule"]) and d["declared_before"] is True, "Declare the stopping rule in advance")
register("preregister", {"exclusion_rule": "malformed_input", "defined_at": 10, "result_at": 20}, {"defined_at": 21},
         lambda d: bool(d["exclusion_rule"]) and d["defined_at"]<d["result_at"], "Do not select exclusions after results")
register("preregister", {"randomized": False, "blinded": False, "fields": ["randomized","blinded"]}, {"fields": ["randomized"]},
         lambda d: {"randomized","blinded"}<=set(d["fields"]), "Record randomization and blinding separately")
register("preregister", {"budget_a": [100,"tokens"], "budget_b": [100,"tokens"]}, {"budget_b": [100,"seconds"]},
         lambda d: d["budget_a"]==d["budget_b"], "Match quantity and resource unit")
register("preregister", {"original": "plan_a", "amendment": "plan_b", "retained": ["plan_a","plan_b"]}, {"retained": ["plan_b"]},
         lambda d: {d["original"],d["amendment"]}<=set(d["retained"]), "Preserve an amended protocol's original")
register("preregister", {"protocol_exists": True, "experiment_completed": False}, {"experiment_completed": True},
         lambda d: d["protocol_exists"] is True and d["experiment_completed"] is False, "A protocol is not an executed experiment")

register("sampling", {"n": 5}, {"n": 5.5}, lambda d: integer(d["n"]) and d["n"]>=0, "Nonnegative integer sample counts")
register("sampling", {"values": [1,None,3], "missing": 1}, {"missing": 0},
         lambda d: sum(x is None for x in d["values"])==d["missing"], "Count explicit missing observations")
register("sampling", {"ids": ["a","a","b"], "unique_n": 2}, {"unique_n": 3},
         lambda d: len(set(d["ids"]))==d["unique_n"], "Do not double count duplicate observations")
register("sampling", {"frame": ["synthetic"], "generalization": ["synthetic"]}, {"generalization": ["all_humans"]},
         lambda d: set(d["generalization"])<=set(d["frame"]), "Bound generalization to the sampling frame")
register("sampling", {"selection": "deterministic_fixture_selection"}, {"selection": ""},
         lambda d: bool(d["selection"]), "State the selection mechanism")
register("sampling", {"weights": [1,.5,0]}, {"weights": [1,-.5,0]},
         lambda d: all(finite(w) and w>=0 for w in d["weights"]), "Use finite nonnegative weights")
register("sampling", {"ids": ["a","b","c"], "clusters": ["x","x","y"]}, {"clusters": ["x","y"]},
         lambda d: len(d["ids"])==len(d["clusters"]) and all(d["clusters"]), "Preserve one cluster label per observation")
register("sampling", {"train": ["a","b"], "evaluation": ["c","d"]}, {"evaluation": ["b","d"]},
         lambda d: set(d["train"]).isdisjoint(d["evaluation"]), "Separate training and evaluation records")
register("sampling", {"participants": 8, "bootstrap_repeats": 500, "reported_participants": 8}, {"reported_participants": 500},
         lambda d: d["participants"]==d["reported_participants"], "Resampling creates no participants")
register("sampling", {"real_participants": 0, "real_study": "open_gap"}, {"real_study": "completed"},
         lambda d: d["real_participants"]==0 and d["real_study"]=="open_gap", "Retain the zero-real-participant gap")

register("comparison", {"a": {"p1": 2,"p2": 4}, "b": {"p1": 1,"p2": 3}}, {"b": {"p1": 1,"p3": 3}},
         lambda d: set(d["a"])==set(d["b"]), "Paired differences preserve pair identifiers")
register("comparison", {"design": "unpaired", "assumed_pairing": False}, {"assumed_pairing": True},
         lambda d: d["design"]=="unpaired" and d["assumed_pairing"] is False, "Do not assume pairs in an unpaired design")
register("comparison", {"effect": -.2, "scale": "mean_difference", "direction": "a_minus_b"}, {"scale": ""},
         lambda d: finite(d["effect"]) and bool(d["scale"] and d["direction"]), "An effect size has a scale and direction")
register("comparison", {"interval": [-.4,.1], "confidence": .95}, {"confidence": 95},
         lambda d: 0<d["confidence"]<1 and d["interval"][0]<=d["interval"][1], "Confidence is a probability with ordered bounds")
register("comparison", {"variance": 0, "standardized_effect": None}, {"standardized_effect": 3.0},
         lambda d: d["variance"]!=0 or d["standardized_effect"] is None, "Zero variance cannot silently produce a standardized effect")
register("comparison", {"a_unit": "tokens", "b_unit": "tokens"}, {"b_unit": "seconds"},
         lambda d: d["a_unit"]==d["b_unit"], "Match resource units")
register("comparison", {"baseline_at": 10, "comparison_at": 20}, {"baseline_at": 25},
         lambda d: d["baseline_at"]<d["comparison_at"], "Freeze a baseline before comparison")
register("comparison", {"control_present": False, "causal_comparison": "open_gap"}, {"causal_comparison": "confirmed"},
         lambda d: d["control_present"] is False and d["causal_comparison"]=="open_gap", "An omitted control remains a gap")
register("comparison", {"environment": "proxy", "real_superiority": False}, {"real_superiority": True},
         lambda d: d["environment"]=="proxy" and d["real_superiority"] is False, "Keep proxy results separate from real-arm superiority")
register("comparison", {"changed_assumptions": ["normality"], "reported_changes": ["normality"]}, {"reported_changes": []},
         lambda d: set(d["changed_assumptions"])<=set(d["reported_changes"]), "Report changed sensitivity assumptions")

def holm(p):
    n=len(p); order=sorted(range(n), key=lambda i:p[i]); out=[0.0]*n; last=0.0
    for j,i in enumerate(order):
        last=max(last,min(1.0,(n-j)*p[i]));out[i]=last
    return out

def bh(p):
    n=len(p); order=sorted(range(n), key=lambda i:p[i]);out=[0.0]*n;last=1.0
    for j in range(n-1,-1,-1):
        i=order[j];last=min(last,n*p[i]/(j+1));out[i]=min(1.0,last)
    return out

register("multiplicity", {"p": [.01,.3,1]}, {"p": [.01,1.3]},
         lambda d: all(finite(p) and 0<=p<=1 for p in d["p"]), "P values are in the unit interval")
register("multiplicity", {"family": ["h1","h2"], "tested": ["h1","h2"]}, {"family": ["h1"]},
         lambda d: set(d["tested"])<=set(d["family"]), "Declare the hypothesis family")
register("multiplicity", {"p": [.01,.04,.03], "adjusted": [.03,.06,.06]}, {"adjusted": [.01,.04,.03]},
         lambda d: all(math.isclose(a,b) for a,b in zip(holm(d["p"]),d["adjusted"],strict=True)), "Holm adjustment returns original hypothesis order")
register("multiplicity", {"p": [.04,.01,.03], "adjusted": [.04,.03,.04]}, {"adjusted": [.03,.04,.04]},
         lambda d: all(math.isclose(a,b) for a,b in zip(bh(d["p"]),d["adjusted"],strict=True)), "Benjamini Hochberg adjustment preserves identifiers")
register("multiplicity", {"planned_alpha": .05, "used_alpha": .05}, {"used_alpha": .1},
         lambda d: d["planned_alpha"]==d["used_alpha"], "Retain the planned threshold")
register("multiplicity", {"raw_label": "raw_p", "adjusted_label": "holm_p"}, {"adjusted_label": "raw_p"},
         lambda d: d["raw_label"]!=d["adjusted_label"], "Distinguish raw and adjusted outputs")
register("multiplicity", {"planned": False, "analysis_label": "exploratory"}, {"analysis_label": "confirmatory"},
         lambda d: d["planned"] is False and d["analysis_label"]=="exploratory", "Unplanned analyses remain exploratory")
register("multiplicity", {"optional_stopping": True, "disclosed": True}, {"disclosed": False},
         lambda d: not d["optional_stopping"] or d["disclosed"] is True, "Disclose optional stopping")
register("multiplicity", {"significance_language": True, "effect_size": .1}, {"effect_size": None},
         lambda d: not d["significance_language"] or finite(d["effect_size"]), "Accompany significance with an effect size")
register("multiplicity", {"p_below_alpha": True, "causality_established": False}, {"causality_established": True},
         lambda d: d["p_below_alpha"] is True and d["causality_established"] is False, "Significance alone establishes no causality")

register("counterexample", {"variant": "positive", "minimum_n": 2}, {"minimum_n": 1},
         lambda d: d["variant"]=="positive" and d["minimum_n"]==2, "State the positive denominator variant")
register("counterexample", {"variant": "distinct", "minimum_n": 3}, {"minimum_n": 2},
         lambda d: d["variant"]=="distinct" and d["minimum_n"]==3, "State the distinct denominator variant")
register("counterexample", {"n": 5, "denominators": [2,4,20]}, {"denominators": [2,4,-20]},
         lambda d: all(integer(x) and x>0 for x in d["denominators"]), "Positive integer denominators")
register("counterexample", {"denominators": [2,4,20]}, {"denominators": [3,3,3]},
         lambda d: len(d["denominators"])==3 and d["denominators"][0]<d["denominators"][1]<d["denominators"][2], "Test distinctness separately")
register("counterexample", {"n": 5, "denominators": [2,4,20]}, {"denominators": [2,4,21]},
         lambda d: verify(d["n"],d["denominators"]), "Exact rational equality and domain verification")
register("counterexample", {"tested": [3,1000], "universal": False}, {"universal": True},
         lambda d: d["tested"]==[3,1000] and d["universal"] is False, "A finite sweep is not a universal proof")
register("counterexample", {"k": 2, "n": 4, "ds": [2,3,6]}, {"k": 1,"n": 2,"ds": [1,2,2]},
         lambda d: integer(d["k"]) and d["k"]>=2 and d["n"]==2*d["k"] and d["ds"]==[d["k"],d["k"]+1,d["k"]*(d["k"]+1)] and verify(d["n"],d["ds"]), "Verify the known even family with k at least two")
register("counterexample", {"k": 3, "n": 9, "ds": [3,12,36]}, {"ds": [3,12,35]},
         lambda d: integer(d["k"]) and d["k"]>=1 and d["n"]==3*d["k"] and d["ds"]==[d["k"],4*d["k"],12*d["k"]] and verify(d["n"],d["ds"]), "Verify the known multiple of three family")
register("counterexample", {"timed_out": True, "status": "open_gap"}, {"status": "disproved"},
         lambda d: d["timed_out"] is True and d["status"]=="open_gap", "A timeout retains an unresolved result")
register("counterexample", {"proof_claim": True, "independent_review": None, "accepted_theorem": False}, {"accepted_theorem": True},
         lambda d: d["independent_review"] is None and d["accepted_theorem"] is False, "A proof claim is not an independently accepted theorem")

register("credential", {"type": "VerifiableCredential", "signature_verified": False, "reported": "structure_only"}, {"reported": "valid_trusted_credential"},
         lambda d: d["type"]=="VerifiableCredential" and d["signature_verified"] is False and d["reported"]=="structure_only", "Type and validity are different claims")
register("credential", {"issuer": "issuer_example", "subject": "subject_example", "issuer_role": "issuer_example"}, {"issuer_role": "subject_example"},
         lambda d: d["issuer_role"]==d["issuer"] and d["issuer"]!=d["subject"], "Retain issuer and subject roles")
register("credential", {"subject": "subject_example", "holder": None, "holder_inferred": False}, {"holder_inferred": True},
         lambda d: d["holder"] is None and d["holder_inferred"] is False, "Do not infer a holder from a subject")
register("credential", {"context": "offline_pinned_fixture", "retrievals": 0}, {"retrievals": 1},
         lambda d: d["context"]=="offline_pinned_fixture" and d["retrievals"]==0, "Pin contexts without network retrieval")
register("credential", {"proof_present": True, "verification_receipt": None, "verified": False}, {"verified": True},
         lambda d: d["verification_receipt"] is None and d["verified"] is False, "Proof presence is not signature verification")
register("credential", {"status": "unknown", "observed_at": "2026-09-05T00:00:00Z"}, {"observed_at": None},
         lambda d: stamp(d["observed_at"]).utcoffset() is not None, "Timestamp status observations")
register("credential", {"source_state": "suspended", "reported_state": "suspended"}, {"reported_state": "revoked"},
         lambda d: d["source_state"]==d["reported_state"], "Distinguish suspension and revocation")
register("credential", {"identifier": "synthetic_subject_example", "live_did": False}, {"live_did": True},
         lambda d: d["identifier"].startswith("synthetic_") and d["live_did"] is False, "A fixture identifier is not a live DID")
register("credential", {"protocol_exercised": False, "interop_proven": False}, {"interop_proven": True},
         lambda d: d["protocol_exercised"] is False and d["interop_proven"] is False, "Interoperability requires an exercised protocol")
register("credential", {"json_valid": True, "trust_authority": "exact_gate"}, {"trust_authority": "automatically_granted"},
         lambda d: d["json_valid"] is True and d["trust_authority"]=="exact_gate", "Keep trust governance separate")

register("privacy", {"shared_fields": ["date","summary"]}, {"shared_fields": ["date","mailbox_route"]},
         lambda d: set(d["shared_fields"])<={"date","summary","subject"}, "Exclude private mail routes")
register("privacy", {"redaction_scope": ["invitation_links"], "limitations": ["not_anonymization"]}, {"limitations": []},
         lambda d: bool(d["redaction_scope"]) and bool(d["limitations"]), "State redaction scope and limits")
register("privacy", {"digest_present": True, "anonymized": False}, {"anonymized": True},
         lambda d: d["digest_present"] is True and d["anonymized"] is False, "Hashing does not prove anonymization")
register("privacy", {"private_view": "local_only", "public_view": "bounded_summary"}, {"public_view": "private_raw_body"},
         lambda d: d["private_view"]=="local_only" and d["public_view"]=="bounded_summary", "Separate artifact views")
register("privacy", {"needed": ["date","summary"], "collected": ["date","summary"]}, {"collected": ["date","summary","account_number"]},
         lambda d: set(d["collected"])<=set(d["needed"]), "Minimize collected fields")
register("privacy", {"available": True, "consent_record": None, "consented": False}, {"consented": True},
         lambda d: d["consent_record"] is None and d["consented"] is False, "Availability is not consent")
register("privacy", {"file_owned": True, "cultural_authority": "unestablished"}, {"cultural_authority": "inferred"},
         lambda d: d["file_owned"] is True and d["cultural_authority"]=="unestablished", "File ownership does not establish cultural authority")
register("privacy", {"location": "scanner_definition", "payload_exposure": False}, {"payload_exposure": True},
         lambda d: d["location"]=="scanner_definition" and d["payload_exposure"] is False, "Distinguish scanner definitions from exposed payloads")
register("privacy", {"finding": "candidate_a", "correction": "false_positive", "retained": ["candidate_a"]}, {"retained": []},
         lambda d: d["finding"] in d["retained"] and d["correction"]=="false_positive", "Preserve corrected findings")
register("privacy", {"structure_audit": "pass", "affected_user_evaluation": "open_gap"}, {"affected_user_evaluation": "pass"},
         lambda d: d["structure_audit"]=="pass" and d["affected_user_evaluation"]=="open_gap", "Structural accessibility is not affected-user evaluation")

register("handoff", {"substantive_words": 10001}, {"substantive_words": 9999},
         lambda d: integer(d["substantive_words"]) and 10000<=d["substantive_words"]<=100000, "Respect the file-backed baton length range")
register("handoff", {"sections": list(range(13))}, {"sections": list(range(12))},
         lambda d: len(d["sections"])>=13 and len(set(d["sections"]))==len(d["sections"]), "Provide thirteen distinct navigable sections")
register("handoff", {"message_words": 90, "baton_in_message": False}, {"baton_in_message": True},
         lambda d: 1<=d["message_words"]<=300 and d["baton_in_message"] is False, "Keep future activation messages compact")
register("handoff", {"prepared": True, "send_receipt": None, "delivery": "PREPARED_NOT_SENT"}, {"delivery": "ACKNOWLEDGED"},
         lambda d: d["prepared"] is True and d["send_receipt"] is None and d["delivery"]=="PREPARED_NOT_SENT", "Preparation is not delivery")
register("handoff", {"successor": "Elaren Kestrel", "phase": "v685-v7"}, {"phase": "v685-v8"},
         lambda d: d["successor"]=="Elaren Kestrel" and d["phase"]=="v685-v7", "Name the immediate successor phase")
register("handoff", {"controller": "Elaren Kestrel", "future_seat": "future-sibling-02-self-chosen"}, {"controller": "Rowan Ash"},
         lambda d: d["controller"]=="Elaren Kestrel" and d["future_seat"]=="future-sibling-02-self-chosen", "Retain the next induction controller")
register("handoff", {"current_hold": True, "decision": "HELD_CURRENT_INSTRUCTION"}, {"decision": "SEND"},
         lambda d: route_decision(d)==d["decision"], "A current hold takes precedence")
register("handoff", {"acknowledgement": "opaque", "resend": False}, {"resend": True},
         lambda d: d["acknowledgement"]=="opaque" and d["resend"] is False, "Do not resend an opaque accepted call")
register("handoff", {"current_hold": False, "guards_current": False, "decision": "HELD_ROUTE_GAP"}, {"decision": "SEND"},
         lambda d: route_decision(d)==d["decision"], "Hold when current guards are unavailable")
register("handoff", {"working_name": "Rowan Ash", "identity_continuity_proven": False}, {"identity_continuity_proven": True},
         lambda d: bool(d["working_name"]) and d["identity_continuity_proven"] is False, "Working names do not prove continuity")

register("roster", {"cycle": CYCLE}, {"cycle": CYCLE[:-1]+[CYCLE[0]]},
         lambda d: len(d["cycle"])==30 and len(set(d["cycle"]))==30, "Thirty unique planning seats")
register("roster", {"actual_main_tasks": 16}, {"actual_main_tasks": 30},
         lambda d: d["actual_main_tasks"]==16, "Retain the observed existing main-task count")
register("roster", {"planned_total": 30, "actual": 16, "uncreated": 14}, {"uncreated": 0},
         lambda d: d["planned_total"]-d["actual"]==d["uncreated"]==14, "Fourteen future tasks are uncreated")
register("roster", {"future_name": None, "future_specialty": None}, {"future_name": "assigned_without_inductee"},
         lambda d: d["future_name"] is None and d["future_specialty"] is None, "Future identity attributes remain self chosen")
register("roster", {"after_685_8": [686,1]}, {"after_685_8": [685,9]},
         lambda d: d["after_685_8"]==[686,1], "Advance phase arithmetic through eight slots")
register("roster", {"remaster": "v685-v6-r2", "canonical_slots_consumed": 0}, {"canonical_slots_consumed": 1},
         lambda d: d["remaster"]=="v685-v6-r2" and d["canonical_slots_consumed"]==0, "The remaster consumes no canonical slot")
register("roster", {"incumbent": "Elaren Kestrel", "created_future_count": 1}, {"created_future_count": 2},
         lambda d: d["incumbent"] in CYCLE and integer(d["created_future_count"]) and 0<=d["created_future_count"]<=1, "One future seat per authorized incumbent")
register("roster", {"already_created": True, "next_action": "reuse"}, {"next_action": "create_duplicate"},
         lambda d: d["already_created"] is True and d["next_action"]=="reuse", "Reuse created tasks on later cycles")
register("roster", {"task_kind": "main", "model": "gpt-6-astra", "thinking": "max"}, {"task_kind": "collaboration_subagent"},
         lambda d: d["task_kind"]=="main" and d["model"]=="gpt-6-astra" and d["thinking"]=="max", "A subagent is not an induction main task")
register("roster", {"last": [725,8]}, {"last": [726,1]},
         lambda d: d["last"]==[project()[-1]["version"],project()[-1]["slot"]], "Stop the projected horizon at v725 v8")

register("runtime", {"owner_bundle": 2, "files": 500, "decision": "REUSE_OWNER_LANE"}, {"decision": "REVIEW_ROTATION"},
         lambda d: rotation_decision(d["owner_bundle"],d["files"])==d["decision"], "Reuse the second owner lane")
register("runtime", {"owner_bundle": 5, "files": 500, "decision": "REVIEW_ROTATION"}, {"decision": "REUSE_OWNER_LANE"},
         lambda d: rotation_decision(d["owner_bundle"],d["files"])==d["decision"], "Review rotation for every fifth owner bundle")
register("runtime", {"owner_bundle": 2, "files": 2000, "decision": "REVIEW_ROTATION"}, {"decision": "REUSE_OWNER_LANE"},
         lambda d: rotation_decision(d["owner_bundle"],d["files"])==d["decision"], "The materialized file ceiling overrides reuse")
register("runtime", {"source": "a"*40, "final": "b"*40, "scope": "source_to_final_delta"}, {"scope": "all_historical_lanes"},
         lambda d: len(d["source"])==len(d["final"])==40 and d["source"]!=d["final"] and d["scope"]=="source_to_final_delta", "Name the owner validation delta")
register("runtime", {"requested_owner": "Rowan Ash", "executed_owners": ["Rowan Ash"]}, {"executed_owners": ["Rowan Ash","Elaren Kestrel"]},
         lambda d: set(d["executed_owners"])=={d["requested_owner"]}, "Execute only the current owner delta")
register("runtime", {"sympy": "1.14.0", "mpmath": [1,3,0]}, {"mpmath": [1,4,1]},
         lambda d: d["sympy"]=="1.14.0" and (1,1,0)<=tuple(d["mpmath"])<(1,4,0), "Enforce the researched dependency interval")
register("runtime", {"artifact": "example wheel bytes", "sha256": digest("example wheel bytes")}, {"artifact": "changed wheel bytes"},
         lambda d: digest(d["artifact"])==d["sha256"], "Verify artifact fixity")
register("runtime", {"source_retained": True, "byte_parity": True, "rollback": "prior_package_pointer"}, {"rollback": ""},
         lambda d: d["source_retained"] is True and d["byte_parity"] is True and bool(d["rollback"]), "Retain compatibility and rollback during promotion")
register("runtime", {"success_count": 1, "requested_invocations": 1}, {"requested_invocations": 2},
         lambda d: d["success_count"]==1 and d["requested_invocations"]==1, "Do not replay a successful canonical receipt")
register("runtime", {"configured_context": 1000000, "retention_guaranteed": False}, {"retention_guaranteed": True},
         lambda d: d["configured_context"]==1000000 and d["retention_guaranteed"] is False, "A configured limit is not a retention guarantee")

def evaluate(family, rule_index, payload):
    if not isinstance(payload, dict) or type(rule_index) is not int:
        return False
    matches = [r for r in RULES if r["family"]==family and r["rule_index"]==rule_index]
    if len(matches)!=1:
        return False
    try:
        return matches[0]["predicate"](payload) is True
    except (KeyError, TypeError, ValueError, ArithmeticError, IndexError, AttributeError):
        return False

def exercise(families=None):
    rows = []
    for n,r in enumerate(RULES,1):
        if families and r["family"] not in families:
            continue
        good=evaluate(r["family"],r["rule_index"],r["good"])
        adverse=evaluate(r["family"],r["rule_index"],r["bad"])
        rows.append({"proposal_id":f"RA6856R2-N{n:03d}", "family":r["family"], "rule_index":r["rule_index"],
                     "purpose":r["purpose"], "accepted_fixture":r["good"], "adverse_fixture":r["bad"],
                     "accepted_observed":good, "adverse_observed":adverse, "pass":good and not adverse,
                     "scope":"same-owner local contract", "independent_reproduction":False,
                     "scientific_discovery_credit":0})
    return {"schema":"ghc.family.claim-evidence-lab.v1","status":"PASS" if all(r["pass"] for r in rows) and rows else "FAIL",
            "criteria":len(rows),"positive_checks":len(rows),"adverse_checks":len(rows),"rows":rows,
            "metadata_does_not_verify_underlying_world":True}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--families",nargs="*")
    a=ap.parse_args()
    out=exercise(set(a.families) if a.families else None)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes((json.dumps(out,indent=2,ensure_ascii=False)+"\n").encode("utf-8"))
    print(json.dumps({k:v for k,v in out.items() if k!="rows"}))
    return out["status"]!="PASS"

if __name__=="__main__":
    raise SystemExit(main())
