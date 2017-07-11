import uuid

def search_problem_to_json(problem):
    """Converts a Search_problem into a JSON representation.

    The search problem must be defined explicitly.

    When using this function with a Dict traitlet for Jupyter widgets,
    this dictionary will automatically be converted into JSON for the client side.
    Therefore, you don't need to convert the return value into a string,
    synchronize the string with a traitlet, then convert it to JSON on the client.

    Args:
        csp (aipython.searchProblem.Search_problem): 
            The search problem instance to convert to a dictionary.

    Returns:
        (dict):
            A dictionary representing the search graph that can be easily converted into JSON.
    """
    nodes = []
    edges = []
    node_map = {n: str(uuid.uuid4()) for n in problem.nodes}

    for n in problem.nodes:
        h = 0
        if n in problem.hmap:
            h = problem.hmap[n]
        
        node_to_add = {'name': str(n), 'id': node_map[n], 'h': h}
        if n in problem.starts:
            node_to_add['type'] = 'search:start'
        elif n in problem.goals:
            node_to_add['type'] = 'search:goal'

        else:
            node_to_add['type'] = 'search:regular'

        nodes.append(node_to_add)

    for arc in problem.arcs:
        new_edge = {'id': str(uuid.uuid4()), 'source': node_map[arc.from_node], 'target': node_map[arc.to_node]}
        edges.append(new_edge)

    return {'nodes': nodes, 'edges': edges}
