"""
Utilities for converting to and from a Python CSP (aipython.cspProblem.CSP) 
and a Graph<ICSPGraphNode, IGraphEdge> in JavaScript.
"""

import json
import uuid
from operator import lt

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

            The second dictionary is a domain map, where the keys are node names (strings), and values are
            the IDs (also strings) of the nodes in the resulting JSON. For example, `domainMap['A'] -> 'a6c!dv33'`.
            You can ignore this dictionary - it is provided for convenience.

            The third dictionary is a edge map, where the keys are a tuple of (node name, constraint instance).
            The values are the IDs (string) of the edge connecting them in the resulting JSON.
            For example, `edgeMap[('A', A_lt_B_constraint)] -> 'wer3jbvcs2'`.
            You can ignore this dictionary - it is provided for convenience.            
    """
    cspJSON = {'nodes': {}, 'edges': {}}

    # Maps variables to their IDs
    domainMap = {var: str(uuid.uuid4()) for var in csp.domains}

    # Maps (variable, constraint) to their corresponding arc IDs
    edgeMap = dict()

    for i, (var, value) in enumerate(csp.domains.items()):
        cspJSON['nodes'][domainMap[var]] = {
            'id': domainMap[var], 'name': var, 'type': 'csp:variable', 'idx': i, 'domain': list(value)}

    for (i, cons) in enumerate(csp.constraints):
        consId = str(uuid.uuid4())
        cspJSON['nodes'][consId] = {
            'id': consId, 'name': cons.__repr__(), 'type': 'csp:constraint', 'idx': i}

        link1Id = str(uuid.uuid4())
        link1 = {'id': link1Id,
                 'source': domainMap[cons.scope[0]], 'dest': consId}

        cspJSON['edges'][link1Id] = link1
        edgeMap[(cons.scope[0], cons)] = link1Id

        if len(cons.scope) == 2:
            consId2 = str(uuid.uuid4())
            link2Id = str(uuid.uuid4())
            link2 = {'id': link2Id,
                     'source': domainMap[cons.scope[1]], 'dest': consId}

            cspJSON['edges'][link2Id] = link2
            edgeMap[(cons.scope[1], cons)] = link2Id

    return (cspJSON, domainMap, edgeMap)


def csp_from_json(graphJSON):
    """Converts a CSP represented by a JSON dictionary into a Python CSP instance.

    Note that because a CSP doesn't use the concept of IDs, which the JSON graph representation does,
    IDs will be lost and will be different if you convert the result of this function back to JSON.

    Args:
        graphJSON (dict): A dictionary representing JSON to be converted into a CSP instance.

    Returns:
        (aipython.cspProblem.CSP):
             An instance of CSP that was converted from the provided JSON.
    """
    domains = {
        node['name']: set(node['domain'])
        for node in graphJSON['nodes'].values() if node['type'] == 'csp:variable'
    }

    constraints = []

    for node in graphJSON['nodes'].values():
        scope = []
        if node['type'] == 'csp:constraint':
            # Find the links with the target as this constraint
            for link in graphJSON['edges'].values():
                if link['dest'] == node['id']:
                    sourceNode = graphJSON['nodes'][link['source']]
                    scope.append(sourceNode['name'])
                elif link['source'] == node['id']:
                    sourceNode = graphJSON['nodes'][link['dest']]
                    scope.append(sourceNode['name'])

            if scope:
                constraints.append(Constraint(tuple(scope), lt))

    return CSP(domains, constraints)


def csp_to_python_code(csp):
    """Converts a CSP into Python code that, when executed, creates the CSP.

    Example:
        ::
            >>> csp_to_python_code(csp)
            'from aipython.cspProblem import CSP, Constraint\ncsp = CSP({"A": [1, 2, 3], "B": [1, 2, 3]}, Constraint(("A", "B"), lt))'

    Args:
        csp (aipython.cspProblem.CSP): The CSP instance to convert to Python code.

    Returns:
        (string):
            A string containing Python code. Executing this string will cause a CSP to be created.
    """
    constStrList = []
    for constraint in csp.constraints:
        constStrList.append(f"Constraint({constraint.scope}, {constraint.condition.__name__})")

    template = """from aipython.cspProblem import CSP, Constraint
from operator import lt
csp = CSP($domains, [$constraints])"""

    return template
