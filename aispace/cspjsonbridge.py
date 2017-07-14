"""
Utilities for converting to and from a Python CSP (aipython.cspProblem.CSP)
and a Graph<ICSPGraphNode, IGraphEdge> in JavaScript.
"""

import uuid
from operator import lt
from string import Template

from aipython.cspProblem import CSP, Constraint


def csp_to_json(csp):
    """Converts a Python CSP instance to a dictionary representable as JSON.

    When using this function with a Dict traitlet for Jupyter widgets,
    this dictionary will automatically be converted into JSON for the client side.
    Therefore, you don't need to convert the return value into a string,
    synchronize the string with a traitlet, then convert it to JSON on the client.

    Args:
        csp (aipython.cspProblem.CSP): The CSP instance to convert to a dictionary.

    Returns:
        (dict, dict, dict):
            The first dictionary returned represents the CSP that is representable in JSON.
            This means the dictionary has no references to object instances.
            This JSON should be immediately usable in creating a new CSP Graph in JavaScript.
            See the TypeScript definition of IGraphJSON for details of its shape.

            The second dictionary is a domain map, where the keys are node names (strings),
            and values are the IDs (also strings) of the nodes in the resulting JSON.
            For example, `domain_map['A'] -> 'a6c!dv33'`.
            You can ignore this dictionary - it is provided for convenience.

            The third dictionary is a edge map.
            The keys are a tuple of (node name, Constraint instance).
            The values are the IDs (string) of the edge connecting them in the resulting JSON.
            For example, `edge_map[('A', A_lt_B_constraint)] -> 'wer3jbvcs2'`.
            You can ignore this dictionary - it is provided for convenience.
    """
    csp_json = {'nodes': [], 'edges': []}

    # Maps variables to their IDs
    domain_map = {var: str(uuid.uuid4()) for var in csp.domains}

    # Maps (variable, constraint) to their corresponding arc IDs
    edge_map = {}

    for i, (var, value) in enumerate(csp.domains.items()):
        csp_json['nodes'].append({
            'id': domain_map[var],
            'name': var,
            'type':
            'csp:variable',
            'idx': i,
            'domain': list(value)
        })

    for (i, constraint) in enumerate(csp.constraints):
        constraint_id = str(uuid.uuid4())
        csp_json['nodes'].append({
            'id': constraint_id,
            'name': constraint.__repr__(),
            'type': 'csp:constraint',
            'idx': i
        })

        link1_id = str(uuid.uuid4())
        link1 = {
            'id': link1_id,
            'source': domain_map[constraint.scope[0]],
            'target': constraint_id
        }

        csp_json['edges'].append(link1)
        edge_map[(constraint.scope[0], constraint)] = link1_id

        if len(constraint.scope) == 2:
            link2_id = str(uuid.uuid4())
            link2 = {'id': link2_id,
                     'source': domain_map[constraint.scope[1]], 'target': constraint_id}

            csp_json['edges'].append(link2)
            edge_map[(constraint.scope[1], constraint)] = link2_id

    return (csp_json, domain_map, edge_map)


def csp_from_json(graph_json):
    """Converts a CSP represented by a JSON dictionary into a Python CSP instance.

    Note that because a CSP doesn't use the concept of IDs, unlike the JSON graph representation,
    IDs will be lost and will be different if you convert the result of this function back to JSON.

    Args:
        graph_json (dict): A dictionary representing JSON to be converted into a CSP instance.

    Returns:
        (aipython.cspProblem.CSP):
             An instance of CSP that was converted from the provided JSON.
    """
    domains = {
        node['name']: set(node['domain'])
        for node in graph_json['nodes'] if node['type'] == 'csp:variable'
    }

    constraints = []

    for node in graph_json['nodes']:
        scope = []
        if node['type'] == 'csp:constraint':
            # Find the links with the target as this constraint
            for link in graph_json['edges']:
                if link['target'] == node['id']:
                    source_node = next(
                        n for n in graph_json['nodes'] if n['id'] == link['source'])
                    scope.append(source_node['name'])
                elif link['source'] == node['id']:
                    source_node = next(
                        n for n in graph_json['nodes'] if n['id'] == link['target'])
                    scope.append(source_node['name'])

            if scope:
                constraints.append(Constraint(tuple(scope), lt))

    return CSP(domains, constraints)


def csp_to_python_code(csp):
    """Converts a CSP into Python code that, when executed, creates the CSP.

    Example:
        ::
            >>> csp_to_python_code(csp)
            'from aipython.cspProblem import CSP, Constraint
            csp = CSP({"A": [1, 2, 3], "B": [1, 2, 3]}, Constraint(("A", "B"), lt))'

    Args:
        csp (aipython.cspProblem.CSP): The CSP instance to convert to Python code.

    Returns:
        (string):
            A string containing Python code. Executing this string will cause a CSP to be created.
    """
    constraint_strings = []
    for constraint in csp.constraints:
        scope = constraint.scope
        name = constraint.condition.__name__
        constraint_strings.append("Constraint({}, {})".format(scope, name))

    template = """from aipython.cspProblem import CSP, Constraint
from operator import lt
csp = CSP($domains, [$constraints])"""

    return Template(template).substitute(domains=csp.domains,
                                         constraints=', '.join(constraint_strings))
