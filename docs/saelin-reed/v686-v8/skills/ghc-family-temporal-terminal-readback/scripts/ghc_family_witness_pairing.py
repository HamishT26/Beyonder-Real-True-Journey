"""Validate witness pairings, dependency graphs, and bounded case coverage."""
import re
import networkx as nx
from ghc_family_contract_oracle import main, require


def labels(items, code):
    require(type(items) is list and all(type(x) is str and x for x in items), code)
    return items


def witness_pair(value):
    if type(value) is not dict or set(value) != {'failure', 'correction'}:
        return False
    failure, correction = value['failure'], value['correction']
    if type(failure) is not dict or type(correction) is not dict:
        return False
    if set(failure) != {'id', 'criterion', 'passed'} or set(correction) != {'id', 'criterion', 'passed', 'corrects'}:
        return False
    return bool(all(type(x) is str and x for x in (failure['id'], failure['criterion'], correction['id'], correction['criterion'], correction['corrects']))
                and failure['passed'] is False and correction['passed'] is True
                and failure['id'] != correction['id']
                and failure['criterion'] == correction['criterion']
                and correction['corrects'] == failure['id'])


def acyclic_order(value):
    require(type(value) is dict and set(value) == {'nodes', 'edges'}, 'GRAPH_FIELDS_REQUIRED')
    nodes = labels(value['nodes'], 'INVALID_NODES')
    require(len(nodes) == len(set(nodes)), 'INVALID_NODES')
    edges = value['edges']
    require(type(edges) is list, 'INVALID_EDGES')
    seen = set()
    for edge in edges:
        require(type(edge) is list and len(edge) == 2
                and all(type(x) is str for x in edge), 'INVALID_EDGES')
        require(all(x in nodes for x in edge), 'UNKNOWN_NODE')
        require(tuple(edge) not in seen, 'DUPLICATE_EDGE')
        seen.add(tuple(edge))
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    require(nx.is_directed_acyclic_graph(graph), 'CYCLIC_GRAPH')
    return list(nx.lexicographical_topological_sort(graph))


def expectation_coverage(value):
    require(type(value) is dict and set(value) == {'criteria', 'cases'}, 'COVERAGE_FIELDS_REQUIRED')
    criteria = labels(value['criteria'], 'INVALID_CRITERIA')
    require(len(criteria) == len(set(criteria)), 'INVALID_CRITERIA')
    require(type(value['cases']) is list, 'INVALID_CASES')
    seen = set()
    for row in value['cases']:
        require(type(row) is dict and set(row) == {'criterion', 'polarity'}, 'INVALID_CASES')
        require(type(row['criterion']) is str and row['criterion'] in criteria, 'UNKNOWN_CRITERION')
        require(row['polarity'] in ('positive', 'adverse'), 'INVALID_POLARITY')
        pair = (row['criterion'], row['polarity'])
        require(pair not in seen, 'DUPLICATE_CASE_LINK')
        seen.add(pair)
    return {'missing_positive': sorted(c for c in criteria if (c, 'positive') not in seen),
            'missing_adverse': sorted(c for c in criteria if (c, 'adverse') not in seen)}


def witness_content_groups(value):
    require(type(value) is list, 'INVALID_WITNESS')
    groups, seen = {}, set()
    for row in value:
        require(type(row) is dict and set(row) == {'id', 'digest'}
                and type(row['id']) is str and row['id'], 'INVALID_WITNESS')
        require(row['id'] not in seen, 'DUPLICATE_WITNESS')
        seen.add(row['id'])
        require(type(row['digest']) is str and re.fullmatch('[0-9a-f]{64}', row['digest']), 'INVALID_DIGEST')
        groups.setdefault(row['digest'], []).append(row['id'])
    return {'groups': [{'digest': d, 'ids': sorted(groups[d])} for d in sorted(groups)],
            'unique_contents': len(groups), 'independent_reproductions': 0}


OPERATIONS = {fn.__name__: fn for fn in
              (witness_pair, acyclic_order, expectation_coverage, witness_content_groups)}

if __name__ == '__main__':
    main(OPERATIONS)
