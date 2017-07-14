import uuid

from aipython.searchProblem import Arc, Search_problem_from_explicit_graph


def search_problem_to_json(problem):
    """Converts a Search_problem into a JSON representation.

    The search problem must be defined explicitly.

    When using this function with a Dict traitlet for Jupyter widgets,
    this dictionary will automatically be converted into JSON for the client side.
    Therefore, you don't need to convert the return value into a string,
    synchronize the string with a traitlet, then convert it to JSON on the client.

    Args:
        problem (aipython.searchProblem.Search_problem):
            The search problem instance to convert to a dictionary.

    Returns:
        (dict, dict, dict):
            The first dictionary represents the search graph that can be easily converted into JSON.

            The second dictionary represents the node map. This is a mapping from a node to
            the corresponding ID of the node.

            The third dictionary is an edge map. The keys are tuple of (from_node, to_node),
            and the values are the ID of th edge that connects those two nodes.
    """
    nodes = []
    edges = []
    node_map = {n: str(uuid.uuid4()) for n in problem.nodes}
    edge_map = {}

    for n in problem.nodes:
        h = 0
        if n in problem.hmap:
            h = problem.hmap[n]

        node_to_add = {'name': str(n), 'id': node_map[n], 'h': h}
        if n == problem.start:
            node_to_add['type'] = 'search:start'
        elif n in problem.goals:
            node_to_add['type'] = 'search:goal'

        else:
            node_to_add['type'] = 'search:regular'

        nodes.append(node_to_add)

    for arc in problem.arcs:
        edge_id = str(uuid.uuid4())
        new_edge = {'id': edge_id, 'source': node_map[arc.from_node],
                    'target': node_map[arc.to_node], 'cost': arc.cost}
        edge_map[(arc.from_node, arc.to_node)] = edge_id
        edges.append(new_edge)

    return ({'nodes': nodes, 'edges': edges}, node_map, edge_map)


def json_to_search_problem(json):
    nodes = set()
    node_map = {}
    start = None
    goals = set()

    for node in json['nodes']:
        nodes.add(node['name'])
        node_map[node['id']] = node

        if node['type'] == 'search:start':
            start = node['name']
        elif node['type'] == 'search:goal':
            goals.add(node['name'])

    arcs = []
    for edge in json['edges']:
        cost = 0
        if 'cost' in edge:
            cost = edge['cost']
        arc = Arc(node_map[edge['source']]['name'],
                  node_map[edge['target']]['name'], cost)
        arcs.append(arc)

    return Search_problem_from_explicit_graph(nodes, arcs, start, goals)
