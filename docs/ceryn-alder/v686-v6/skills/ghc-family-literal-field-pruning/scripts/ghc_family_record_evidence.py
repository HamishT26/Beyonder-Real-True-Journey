"""Derived-record source coverage and explicit evidence/authority reservations."""
from ghc_family_record_selection import (
    ContractError, bounded_json, cli, fields, no, ok, require, text_list,
)

OPERATIONS = ('provenance_coverage','thos_migration_readback','gmut_record_gap','cbr_record_gate')
THOS = {
    'cutover_readback':'authorized_operator_execution',
    'rollback_rehearsal':'real_recovery_observation',
    'parallel_read_design':'live_matched_comparison',
    'capacity_margin_plan':'measured_capacity_under_load',
    'failure_notice_template':'affected_recipient_delivery',
    'validation_checkpoint':'competent_operational_acceptance',
    'change_freeze_record':'authorized_service_state',
    'archive_retention_plan':'retention_owner_decision',
    'dependency_pin_review':'production_review',
    'operator_handover_draft':'operator_acknowledgement',
}
GMUT = {
    'apparatus_record_trace':'independent_apparatus_observation',
    'calibration_matrix':'traceable_calibration_evidence',
    'unit_semantics':'validated_measurement_model',
    'sampling_frame':'observed_sampling_protocol',
    'missingness_process':'missingness_evidence',
    'measurement_covariance':'measured_uncertainty_covariance',
    'blind_comparator':'blind_matched_comparator',
    'causal_identification':'causal_identification_evidence',
    'external_reproduction':'independent_reproduction',
    'model_discrimination':'empirical_model_discrimination',
}
CBR = {
    'field_disclosure':'affected_party_consent',
    'record_correction':'competent_correction_authority',
    'retention_exception':'governance_authority',
    'credential_rebinding':'credential_owner_authority',
    'accessibility_acceptance':'affected_user_accessibility_review',
    'professional_signoff':'qualified_professional_review',
    'legal_interpretation':'competent_legal_authority',
    'maori_terminology':'maori_language_authority',
    'iwi_data_decision':'iwi_authority',
    'hapu_stewardship':'hapu_authority',
}


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation == 'provenance_coverage':
            fields(payload, ('outputs','links','declared_sources'))
            outputs,links,sources=payload['outputs'],payload['links'],payload['declared_sources']
            require(text_list(outputs) and text_list(sources) and type(links) is list, 'INVALID_COVERAGE_INPUT')
            require(len(outputs)==len(set(outputs)), 'DUPLICATE_OUTPUT')
            require(len(sources)==len(set(sources)), 'DUPLICATE_SOURCE')
            mapped={}
            for link in links:
                fields(link, ('output','sources'))
                require(type(link['output']) is str and text_list(link['sources']), 'INVALID_LINK')
                require(link['output'] not in mapped, 'DUPLICATE_LINK')
                mapped[link['output']]=link['sources']
            covered=sorted(o for o in outputs if mapped.get(o) and all(s in sources for s in mapped[o]))
            missing=sorted(set(outputs)-set(covered))
            orphan=sorted(set(mapped)-set(outputs))
            unknown=sorted({s for values in mapped.values() for s in values if s not in sources})
            return ok({'covered':covered,'uncovered':missing,'orphan_links':orphan,
                       'unknown_sources':unknown,'complete':not(missing or orphan or unknown)})
        if operation in ('thos_migration_readback','gmut_record_gap','cbr_record_gate'):
            fields(payload, ('topic',))
            topic=payload['topic']
            table={'thos_migration_readback':THOS,'gmut_record_gap':GMUT,'cbr_record_gate':CBR}[operation]
            require(type(topic) is str and topic in table, 'UNKNOWN_TOPIC')
            missing=table[topic]
            if operation == 'thos_migration_readback':
                return ok({'representation':topic,'execution_authorized':False,'production':False,'missing':[missing]})
            if operation == 'gmut_record_gap':
                return ok({'claim':topic,'empirical':False,'missing':[missing],'gate_open':True})
            return ok({'request':topic,'authorized':False,'required_authority':[missing],'gate_open':True})
        raise ContractError('UNKNOWN_OPERATION')
    except ContractError as exc:
        return no(str(exc))


if __name__ == '__main__':
    raise SystemExit(cli(evaluate))
