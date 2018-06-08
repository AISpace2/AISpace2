import uuid
from string import Template

from aipython.searchProblem import Arc, Search_problem_from_explicit_graph


def search_problem_to_json(problem, widget_model=None):
    """Converts a Search_problem into a JSON representation.

    The search problem must be defined explicitly (i.e. instance of aipython.searchProblem.Search_problem_from_explicit_graph).
    If you would like to convert an implicitly defined search problem, use `implicit_to_explicit_search_problem()`.

    Args:
        problem (aipython.searchProblem.Search_problem_from_explicit_graph):
            The search problem instance to convert to a dictionary.
        widget_model: Instance of widget model passed by ipywidgets during conversion. Never used; you can ignore it.

    Returns:
        (dict or None):
            A dictionary representation of a search graph that can be easily converted into JSON. None if no problem was provided.
    """
    if not problem:
        return None

    nodes = []
    edges = []
    node_map = {str(n): str(hash(n)) for n in problem.nodes}

    for node in problem.nodes:
        h = 0
        if node in problem.hmap:
            h = problem.hmap[node]

        node_to_add = {'name': str(node), 'id': node_map[str(node)], 'h': h}
        if node == problem.start:
            node_to_add['type'] = 'search:start'
        elif node in problem.goals:
            node_to_add['type'] = 'search:goal'
        else:
            node_to_add['type'] = 'search:regular'

        if str(node) in problem.positions:
            position = problem.positions[str(node)]
            node_to_add['x'] = position[0]
            node_to_add['y'] = position[1]

        nodes.append(node_to_add)

    for arc in problem.arcs:
        edge_id = str(hash(arc))
        from_node = str(arc.from_node)
        to_node = str(arc.to_node)

        new_edge = {
            'id': edge_id,
            'name': arc.action,
            'source': node_map[from_node],
            'target': node_map[to_node],
            'cost': arc.cost
        }
        edges.append(new_edge)

    return {'nodes': nodes, 'edges': edges}


def generate_search_graph_mappings(problem):
    """Generate a ID mapping from a search problem for communicating with the frontend.

    Why is this useful? You want to tell the frontend to highlight a node or edge, for example.
    You aren't able to pass an instance directly to the frontend, because that node/edge instance is a Python object.
    Therefore, in order to tell the frontend which node/edge to highlight, you pass its ID instead.

    Args:
        problem (aipython.searchProblem.Search_problem_from_explicit_graph):
            The search problem instance to generate mappings for.

    Returns:
        (dict, dict):
            The first dictionary represents the node map. This is a mapping from a *string* representing the node
            to its corresponding ID. The keys are computed as `str(node)`.

            The second dictionary is an edge map. The keys are tuple of (from_node, to_node),
            and the values are the ID of the edge that connects those two nodes.
            Both from_node and to_node are string representation of the nodes, e.g. str(node)
    """
    node_map = {str(n): str(hash(n)) for n in problem.nodes}
    edge_map = {}

    for arc in problem.arcs:
        edge_id = str(hash(arc))
        from_node = str(arc.from_node)
        to_node = str(arc.to_node)

        edge_map[(from_node, to_node)] = edge_id

    return (node_map, edge_map)


def implicit_to_explicit_search_problem(implicit_problem):
    """Converts a non-explicit search problem into an explicit one.

    The intention is to take an initial implicit graph, turn it into an explicit graph,
    then proceed (e.g. by way of listening to `implicit_problem.neighbours()`) to fill in the graph.

    Arguments:
        implicit_problem (aipython.searchProblem.searchProblem):
            The implicitly defined search problem to convert.

    Returns:
        (aipython.searchproblem.Search_problem_from_explicit_graph):
            The explicit search problem. This only returns an explicit graph with the start node:
            there are no arcs nor goals. In the future, we could support "unrolling" of the implicit graph
            in order to create a more defined explicit graph.
    """
    start = str(implicit_problem.start_node())
    h = implicit_problem.heuristic(implicit_problem.start_node())
    return Search_problem_from_explicit_graph(
        set((start, )), [], start, set(), {start: h})


def json_to_search_problem(json, widget_model=None):
    """Converts a JSON representation of a search problem into an explicit graph.

    Args:
        json (dict):
            A dictionary that conforms to the interface IGraphJSON<ISearchGraphNode, IGraphEdgeJSON>
        widget_model: Instance of widget model passed by ipywidgets during conversion. Never used; you can ignore it.

    Returns:
        (aipython.searchProblem.Search_problem_from_explicit_graph or None):
            An explicit search problem represented by the provided JSON. None if no JSON was provided.
    """
    if not json:
        return None

    nodes = set()
    node_map = {}
    start = None
    goals = set()
    hmap = {}

    for node in json['nodes']:
        nodes.add(node['name'])
        node_map[node['id']] = node

        if node['type'] == 'search:start':
            start = node['name']
        elif node['type'] == 'search:goal':
            goals.add(node['name'])

        if node['h'] != 0:
            hmap[node['name']] = node['h']

    arcs = []
    for edge in json['edges']:
        cost = 0
        if 'cost' in edge:
            cost = edge['cost']
        arc = Arc(node_map[edge['source']]['name'],
                  node_map[edge['target']]['name'], cost)
        arcs.append(arc)

    return Search_problem_from_explicit_graph(nodes, arcs, start, goals, hmap)


def search_problem_to_python_code(problem):
    """Converts a JSON representation of a search problem into Python code.

    Example:
        ::
            >>> search_problem_to_python_code(csp)
            'from aipython.searchProblem import Search_problem_from_explicit_graph, Arc
            search_problem = Search_problem_from_explicit_graph({'a', 'b'}, [Arc('a', 'b', cost=5), 'a', {'b'}])'

    Args:
        problem (aipython.searchProblem.Search_problem_from_explicit_graph):
            The search problem to convert into code.

    Returns:
        (string):
            A string of Python code that, when executed, reconstructs the search problem given.
    """
    nodes = problem.nodes
    arcs = []
    for arc in problem.arcs:
        arcs.append("Arc({}, {}, cost={})".format(
            arc.from_node.__repr__(), arc.to_node.__repr__(), arc.cost))

    start = problem.start
    goals = problem.goals
    hmap = problem.hmap

    template = """from aipython.searchProblem import Search_problem_from_explicit_graph, Arc
search_problem = Search_problem_from_explicit_graph($nodes, [$arcs], $start, $goals, $hmap)"""
    return Template(template).substitute(
        nodes=nodes,
        arcs=', '.join(arcs),
        start=start.__repr__(),
        goals=goals,
        hmap=hmap)
