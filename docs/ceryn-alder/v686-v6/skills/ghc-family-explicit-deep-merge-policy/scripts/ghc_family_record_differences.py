"""Exact record differences, reversible patches, and byte bindings."""
import copy
import re
import dictdiffer
from deepdiff import DeepDiff
from ghc_family_record_selection import (
    ContractError, bounded_json, canonical, cli, digest, fields, no, ok, require,
)

OPERATIONS = ('record_delta', 'typed_difference', 'source_binding', 'rename_keys')


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation in ('record_delta', 'typed_difference'):
            fields(payload, ('before', 'after'))
            before, after = payload['before'], payload['after']
            if operation == 'typed_difference':
                differences = DeepDiff(before, after, ignore_order=False,
                                       threshold_to_diff_deeper=0)
                return ok({'equal':not bool(differences), 'change_types':sorted(differences)})
            require(type(before) is dict and type(after) is dict, 'MAPPING_REQUIRED')
            delta = list(dictdiffer.diff(before, after, tolerance=0))
            forward = dictdiffer.patch(delta, before, in_place=False)
            reverted = dictdiffer.revert(delta, forward, in_place=False)
            require(canonical(forward) == canonical(after)
                    and canonical(reverted) == canonical(before), 'NONREVERSIBLE_DIFF')
            return ok({'forward':forward, 'reverted':reverted, 'reversible':True})
        if operation == 'source_binding':
            fields(payload, ('document', 'declared_sha256'))
            declared = payload['declared_sha256']
            require(type(declared) is str and re.fullmatch('[0-9a-fA-F]{64}', declared), 'INVALID_DIGEST')
            return ok({'matches':digest(payload['document']) == declared.lower()})
        if operation == 'rename_keys':
            fields(payload, ('document', 'renames'))
            document, renames = payload['document'], payload['renames']
            require(type(document) is dict and type(renames) is dict, 'MAPPING_REQUIRED')
            require(all(type(v) is str for v in renames.values()), 'NON_TEXT_KEY')
            require(set(renames).issubset(document), 'MISSING_RENAME_SOURCE')
            destinations = [renames.get(k, k) for k in document]
            require(len(destinations) == len(set(destinations)), 'KEY_COLLISION')
            return ok({renames.get(k,k):copy.deepcopy(v) for k,v in document.items()})
        raise ContractError('UNKNOWN_OPERATION')
    except ContractError as exc:
        return no(str(exc))


if __name__ == '__main__':
    raise SystemExit(cli(evaluate))
