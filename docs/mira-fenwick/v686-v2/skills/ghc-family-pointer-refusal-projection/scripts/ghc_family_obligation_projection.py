"""Keep absent real evidence and authority unresolved in synthetic obligation records."""
from ghc_family_evidence_selectors import Refusal,check_json,cli

def evaluate(operation,data):
    try:
        check_json(data)
        if operation!='obligation': raise Refusal('unknown_operation')
        if type(data) is not dict or set(data)!={'obligation','expected_disposition','evidence','authority','external_action'}: raise Refusal('invalid_obligation')
        if type(data['obligation']) is not str or not data['obligation'].strip(): raise Refusal('missing_obligation')
        if data['expected_disposition'] not in ('represented','open_gap','exact_gate'): raise Refusal('invalid_disposition')
        if data['evidence'] is not None or data['authority'] is not None or data['external_action'] is not False: raise Refusal('unsupported_promotion')
        return data['expected_disposition']
    except Refusal as exc: return {'error':str(exc)}

if __name__=='__main__': raise SystemExit(cli(evaluate))
