# searchProblem.py - representations of search problems
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import heapq


class Search_problem(object):
    """A search problem consists of:
    * a start node
    * a neighbors function that gives the neighbors of a node
    * a specification of a goal
    * a (optional) heuristic function.
    The methods must be overridden to define a search problem."""

    def start_node(self):
        """returns start node"""
        raise NotImplementedError("start_node")   # abstract method

    def is_goal(self, node):
        """is True if node is a goal"""
        raise NotImplementedError("is_goal")   # abstract method

    def neighbors(self, node):
        """returns a list of the arcs for the neighbors of node"""
        raise NotImplementedError("neighbors")   # abstract method

    def heuristic(self, n):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        return 0


class Arc(object):
    """An arc has a from_node and a to_node node and a (non-negative) cost"""

    def __init__(self, from_node, to_node, cost=1, action=None):
        assert cost >= 0, ("Cost cannot be negative for" +
                           str(from_node) + "->" + str(to_node) + ", cost: " + str(cost))
        self.from_node = from_node
        self.to_node = to_node
        self.action = action
        self.cost = cost

    def __repr__(self):
        """string representation of an arc"""
        if self.action:
            return str(self.from_node) + " --" + str(self.action) + "--> " + str(self.to_node)
        else:
            return str(self.from_node) + " --> " + str(self.to_node)


class Frontier(object):
    """A frontier consists of a priority queue (heap), frontierpq, of
        (value, index, path) triples, where
    * value is the value we want to minimize (e.g., path cost + h).
    * index is a unique index for each element
    * path is the path on the queue
    Note that the priority queue always returns the smallest element.
    """

    def __init__(self):
        """constructs the frontier, initially an empty priority queue
        """
        self.frontier_index = 0  # the number of items ever added to the frontier
        self.frontierpq = []  # the frontier priority queue

    def empty(self):
        """is True if the priority queue is empty"""
        return self.frontierpq == []

    def add(self, path, value):
        """add a path to the priority queue
        value is the value to be minimized"""
        self.frontier_index += 1    # get a new unique index
        heapq.heappush(self.frontierpq, (value, -self.frontier_index, path))

    def pop(self):
        """returns and removes the path of the frontier with minimum value.
        Note that [2] extracts the path from the triple on the queue.
        """
        return heapq.heappop(self.frontierpq)[2]

    def count(self, val):
        """returns the number of elements of the frontier with value=val"""
        return sum(1 for e in self.frontierpq if e[0] == val)

    def __repr__(self):
        """string representation of the frontier"""
        return "".join(str(["{} ({})".format(p, n) for (n, c, p) in self.frontierpq]))

    def __len__(self):
        return len(self.frontierpq)

    def __iter__(self):
        for (_, _, p) in self.frontierpq:
            yield p


class Search_problem_from_explicit_graph(Search_problem):
    """A search problem consists of:
    * a list or set of nodes
    * a list or set of arcs
    * a start node
    * a list or set of goal nodes
    * a dictionary that maps each node into its heuristic value
    * a dictionary that maps each node name into its (x,y)-position.
    (node names should be unique)
    """

    def __init__(self, nodes, arcs, start=None, goals=set(), hmap={}, positions={}):
        self.neighs = {}
        self.nodes = nodes
        for node in nodes:
            self.neighs[node] = []
        self.arcs = arcs
        for arc in arcs:
            self.neighs[arc.from_node].append(arc)
        self.start = start
        self.goals = goals
        self.hmap = hmap
        self.positions = positions

    def start_node(self):
        """returns start node"""
        return self.start

    def is_goal(self, node):
        """is True if node is a goal"""
        return node in self.goals

    def neighbors(self, node):
        """returns the neighbors of node"""
        return self.neighs[node]

    def heuristic(self, node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden in the hmap."""
        if node in self.hmap:
            return self.hmap[node]
        else:
            return 0

    def __repr__(self):
        """returns a string representation of the search problem"""
        res = ""
        for arc in self.arcs:
            res += str(arc) + ".  "
        return res

    def neighbor_nodes(self, node):
        """returns an iterator over the neighbors of node"""
        return (path.to_node for path in self.neighs[node])


class Path(object):
    """A path is either a node or a path followed by an arc"""

    def __init__(self, initial, arc=None):
        """initial is either a node (in which case arc is None) or
        a path (in which case arc is an object of type Arc)"""
        self.initial = initial
        self.arc = arc
        if arc is None:
            self.cost = 0
        else:
            self.cost = initial.cost + arc.cost

    def end(self):
        """returns the node at the end of the path"""
        if self.arc is None:
            return self.initial
        else:
            return self.arc.to_node

    def nodes(self):
        """enumerates the nodes for the path.
        This starts at the end and enumerates nodes in the path backwards."""
        current = self
        while current.arc is not None:
            yield current.arc.to_node
            current = current.initial
        yield current.initial

    def initial_nodes(self):
        """enumerates the nodes for the path before the end node.
        This starts at the end and enumerates nodes in the path backwards."""
        if self.arc is not None:
            for nd in self.initial.nodes():
                yield nd     # could be "yield from"

    def __repr__(self):
        """returns a string representation of a path"""
        if self.arc is None:
            return str(self.initial)
        elif self.arc.action:
            return (str(self.initial) + " --" + str(self.arc.action)
                    + "--> " + str(self.arc.to_node))
        else:
            return str(self.initial) + " --> " + str(self.arc.to_node)


search_empty = Search_problem_from_explicit_graph(
    {}, [], start=None, goals={})

search_simple1 = Search_problem_from_explicit_graph(
    {'a', 'b', 'c', 'd', 'g'},
    [Arc('a', 'b', 1), Arc('a', 'c', 3), Arc('b', 'c', 1), Arc(
        'b', 'd', 3), Arc('c', 'd', 1), Arc('c', 'g', 3), Arc('d', 'g', 1)],
    start='a',
    goals={'g'},
    positions={'g': (1, 2), 'd': (1, 1), 'a': (3, 2), 'b': (3, 1), 'c': (2, 2)})

search_simple2 = Search_problem_from_explicit_graph(
    {'a', 'b', 'c', 'd', 'e', 'g', 'h', 'j'},
    [Arc('a', 'b', 1), Arc('b', 'c', 3), Arc('b', 'd', 1), Arc(
        'd', 'e', 3), Arc('d', 'g', 1), Arc('a', 'h', 3), Arc('h', 'j', 1)],
    start='a',
    goals={'g'},
    positions={"h": (1,2),
                "e": (2,3),
                "a": (1,1),
                "j": (1,3),
                "c": (3,1),
                "g": (3,2),
                "b": (2,1),
                "d": (2,2)})

search_acyclic_delivery = Search_problem_from_explicit_graph(
    {'mail', 'ts', 'o103', 'o109', 'o111', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3',
     'o125', 'o123', 'o119', 'r123', 'storage'},
    [Arc('ts', 'mail', 6),
        Arc('o103', 'ts', 8),
        Arc('o103', 'b3', 4),
        Arc('o103', 'o109', 12),
        Arc('o109', 'o119', 16),
        Arc('o109', 'o111', 4),
        Arc('b1', 'c2', 3),
        Arc('b1', 'b2', 6),
        Arc('b2', 'b4', 3),
        Arc('b3', 'b1', 4),
        Arc('b3', 'b4', 7),
        Arc('b4', 'o109', 7),
        Arc('c1', 'c3', 8),
        Arc('c2', 'c3', 6),
        Arc('c2', 'c1', 4),
        Arc('o123', 'o125', 4),
        Arc('o123', 'r123', 4),
        Arc('o119', 'o123', 9),
        Arc('o119', 'storage', 7)],
    start='o103',
    goals={'r123'},
    hmap={
        'mail': 26,
        'ts': 23,
        'o103': 21,
        'o109': 24,
        'o111': 27,
        'o119': 11,
        'o123': 4,
        'o125': 6,
        'r123': 0,
        'b1': 13,
        'b2': 15,
        'b3': 17,
        'b4': 18,
        'c1': 6,
        'c2': 10,
        'c3': 12,
        'storage': 12
    },
    positions={
        "o103": (2,7),
        "b4": (3,6),
        "o123": (2,2),
        "o111": (4,7),
        "o119": (4,2),
        "c2": (2,4),
        "b1": (2,5),
        "ts": (1,7),
        "b3": (2,6),
        "o125": (1,2),
        "o109": (4,6),
        "r123": (2,1),
        "mail": (1,6),
        "c1": (2,3),
        "storage": (4,1),
        "b2": (3,5),
        "c3": (3,3)}
)

search_cyclic_delivery = Search_problem_from_explicit_graph(
    {'mail', 'ts', 'o103', 'o109', 'o111', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3',
     'o125', 'o123', 'o119', 'r123', 'storage'},
    [Arc('ts', 'mail', 6), Arc('mail', 'ts', 6),
        Arc('o103', 'ts', 8), Arc('ts', 'o103', 8),
        Arc('o103', 'b3', 4),
        Arc('o103', 'o109', 12), Arc('o109', 'o103', 12),
        Arc('o109', 'o119', 16), Arc('o119', 'o109', 16),
        Arc('o109', 'o111', 4), Arc('o111', 'o109', 4),
        Arc('b1', 'c2', 3),
        Arc('b1', 'b2', 6), Arc('b2', 'b1', 6),
        Arc('b2', 'b4', 3), Arc('b4', 'b2', 3),
        Arc('b3', 'b1', 4), Arc('b1', 'b3', 4),
        Arc('b3', 'b4', 7), Arc('b4', 'b3', 7),
        Arc('b4', 'o109', 7),
        Arc('c1', 'c3', 8), Arc('c3', 'c1', 8),
        Arc('c2', 'c3', 6), Arc('c3', 'c2', 6),
        Arc('c2', 'c1', 4), Arc('c1', 'c2', 4),
        Arc('o123', 'o125', 4), Arc('o125', 'o123', 4),
        Arc('o123', 'r123', 4), Arc('r123', 'o123', 4),
        Arc('o119', 'o123', 9), Arc('o123', 'o119', 9),
        Arc('o119', 'storage', 7), Arc('storage', 'o119', 7)],
    start='o103',
    goals={'r123'},
    hmap={
        'mail': 26,
        'ts': 23,
        'o103': 21,
        'o109': 24,
        'o111': 27,
        'o119': 11,
        'o123': 4,
        'o125': 6,
        'r123': 0,
        'b1': 13,
        'b2': 15,
        'b3': 17,
        'b4': 18,
        'c1': 6,
        'c2': 10,
        'c3': 12,
        'storage': 12
    },
    positions={
        "o103": (2,7),
        "b4": (3,6),
        "o123": (2,2),
        "o111": (4,7),
        "o119": (4,2),
        "c2": (2,4),
        "b1": (2,5),
        "ts": (1,7),
        "b3": (2,6),
        "o125": (1,2),
        "o109": (4,6),
        "r123": (2,1),
        "mail": (1,6),
        "c1": (2,3),
        "storage": (4,1),
        "b2": (3,5),
        "c3": (3,3)}
)

search_tree = Search_problem_from_explicit_graph(
    {'S', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10', 'G'},
    [Arc('S', 'N1', 9.9),
     Arc('N1', 'N3', 11.9),
     Arc('N3', 'N7', 9.6),
     Arc('N1', 'N4', 9.1),
     Arc('N4', 'N8', 8.7),
     Arc('S', 'N2', 10.6),
     Arc('N2', 'N5', 9.1),
     Arc('N5', 'N9', 8.6),
     Arc('N5', 'G', 8.8),
     Arc('N2', 'N6', 12.8),
     Arc('N6', 'N10', 8.5)],
    start='S',
    goals={'G'},
    hmap={'S': 26.0, 'N1': 25.1, 'N2': 16.4, 'N3': 27.6, 'N4': 18.1, 'N5': 8.8,
          'N6': 8.5, 'N7': 28.0, 'N8': 18.7, 'N9': 10, 'N10': 6.5, 'G': 0},
    positions={
        "N10": (758, 362),
        "S": (509, 56),
        "N1": (427, 175),
        "N2": (607, 169),
        "N5": (555, 266),
        "N6": (696, 264),
        "N4": (451, 263),
        "N3": (319, 264),
        "N7": (220, 365),
        "G": (641, 371),
        "N9": (506, 375),
        "N8": (376, 373)})

search_extended_tree = Search_problem_from_explicit_graph(
    nodes={'N2', 'N3', 'N20', 'N1', 'S', 'N11', 'N18', 'N10', 'N8', 'N19', 'N13',
           'N15', 'N4', 'N17', 'N14', 'N9', 'N16', 'N12', 'N6', 'N5', 'N7', 'G'},
    arcs=[Arc('N1', 'N3', 11.9), Arc('N1', 'N4', 9.1), Arc('N2', 'N6', 12.8), Arc('N2', 'N5', 9.1), Arc('S', 'N1', 9.9), Arc('S', 'N2', 10.6), Arc('N5', 'N9', 8.6), Arc('N5', 'N10', 2.0), Arc('N4', 'N8', 8.7), Arc('N3', 'N7', 16.6), Arc(
        'N9', 'N13', 4.0), Arc('N9', 'N14', 5.0), Arc('N14', 'N18', 3.0), Arc('N14', 'G', 4.0), Arc('N6', 'N12', 2.0), Arc('N12', 'N16', 6.0), Arc('N6', 'N11', 8.0), Arc('N11', 'N15', 8.0), Arc('N15', 'N19', 10.0), Arc('N7', 'N20', 2.0), Arc('N13', 'N17', 6.0)],
    start='S',
    goals={'G'},
    hmap={'N1': 27.1, 'N2': 18.4, 'N3': 30.2, 'N4': 28.9, 'N6': 10.5, 'N5': 14.8, 'N18': 0.0, 'S': 30.0, 'N9': 8.0, 'N10': 14.5, 'N8': 30.0,
          'N7': 32.0, 'N13': 15.0, 'N14': 0.0, 'G': 0.0, 'N15': 14.0, 'N16': 13.0, 'N12': 14.9, 'N11': 14.0, 'N19': 17.0, 'N20': 33.0, 'N17': 10.0},
    positions={
        "S": (424, 50),
        "N1": (363, 140),
        "N3": (375, 217),
        "N2": (495, 131),
        "N6": (487, 211),
        "N4": (235, 227),
        "N8": (158, 330),
        "N7": (298, 330),
        "N20": (273, 420),
        "N12": (434, 333),
        "N11": (558, 336),
        "N16": (410, 419),
        "N15": (567, 419),
        "N19": (506, 499),
        "N5": (612, 209),
        "N10": (669, 334),
        "N9": (828, 327),
        "N14": (748, 413),
        "N13": (892, 408),
        "N17": (907, 488),
        "N18": (797, 493),
        "G": (676, 495)})

search_cyclic = Search_problem_from_explicit_graph(
    nodes={'Node 6', 'Node 2', 'Node 7', 'Node 4',
           'Node 5', 'Node 3', 'Node 0', 'Node 1'},
    arcs=[Arc('Node 0', 'Node 2', 11.8), Arc('Node 0', 'Node 3', 11.7), Arc('Node 1', 'Node 3', 11.9), Arc('Node 1', 'Node 4', 12.1), Arc('Node 2', 'Node 5', 11.4), Arc('Node 3', 'Node 2', 14.4), Arc(
        'Node 3', 'Node 4', 15.4), Arc('Node 4', 'Node 6', 11.3), Arc('Node 5', 'Node 3', 11.4), Arc('Node 5', 'Node 7', 11.9), Arc('Node 6', 'Node 3', 11.7), Arc('Node 6', 'Node 7', 12.2)],
    start='Node 1',
    goals={'Node 7'},
    hmap={'Node 0': 28.4, 'Node 1': 28.3, 'Node 2': 23.3, 'Node 3': 18.1,
          'Node 4': 23.6, 'Node 5': 11.9, 'Node 6': 12.2, 'Node 7': 0.0},
    positions={
        "Node 3": (460, 266),
        "Node 1": (270, 275),
        "Node 4": (334, 407),
        "Node 6": (533, 383),
        "Node 5": (651, 208),
        "Node 0": (305, 166),
        "Node 7": (726, 322),
        "Node 2": (491, 126)})

search_vancouver_neighbour = Search_problem_from_explicit_graph(
    nodes={'DT', 'KD', 'JB', 'UBC', 'SRY',
           'BBY', 'MP', 'SP', 'KB', 'AP', 'RM'},
    arcs=[Arc('UBC', 'JB', 3.0), Arc('UBC', 'KD', 3.0), Arc('DT', 'SP', 2.0), Arc('JB', 'KB', 4.0), Arc('KD', 'JB', 4.0), Arc('KD', 'MP', 3.0), Arc('KB', 'DT', 2.0), Arc(
        'KB', 'BBY', 6.0), Arc('MP', 'KB', 4.0), Arc('MP', 'BBY', 5.0), Arc('MP', 'RM', 3.0), Arc('RM', 'AP', 3.0), Arc('RM', 'SRY', 21.0), Arc('SRY', 'BBY', 22.0)],
    start='UBC',
    goals={'SP'},
    hmap={'UBC': 5.0, 'SP': 0.0, 'DT': 2.0, 'JB': 3.0, 'KD': 6.0,
          'KB': 3.0, 'MP': 7.0, 'BBY': 8.0, 'AP': 8.0, 'RM': 9.0, 'SRY': 29.0},
    positions={'UBC': (7671.8306, 5213.067), 'SP': (7774.71, 5041.2866), 'DT': (7870.0386, 5042.2305), 'JB': (7769.9907, 5157.38), 'KD': (7780.373, 5285.743), 'KB': (7890.803, 5153.6045), 'MP': (7960.648, 5296.1255), 'BBY': (8081.4604, 5228.1685), 'AP': (7788.8677, 5420.7134), 'RM': (7925.7256, 5420.7134), 'SRY': (8103.169, 5415.0503)})

search_misleading_heuristic = Search_problem_from_explicit_graph(
    nodes={'Node 6', 'Node 2', 'Node 10', 'Node 8', 'Node 7', 'Node 4',
           'Node 5', 'Node 3', 'Node 0', 'Node 1', 'Node 11', 'Node 9'},
    arcs=[Arc('Node 0', 'Node 1', 7.1), Arc('Node 0', 'Node 6', 11.5), Arc('Node 0', 'Node 10', 12.0), Arc('Node 1', 'Node 2', 6.9), Arc('Node 2', 'Node 3', 9.4), Arc('Node 3', 'Node 4', 7.9), Arc(
        'Node 4', 'Node 5', 9.2), Arc('Node 5', 'Node 2', 11.9), Arc('Node 6', 'Node 7', 25.5), Arc('Node 6', 'Node 9', 8.4), Arc('Node 7', 'Node 8', 18.4), Arc('Node 10', 'Node 11', 9.1)],
    start='Node 0',
    goals={'Node 8'},
    hmap={'Node 0': 28.9, 'Node 1': 23.7, 'Node 2': 17.0, 'Node 3': 10.0, 'Node 4': 15.0, 'Node 5': 21.1, 'Node 6': 34.2, 'Node 7': 18.4, 'Node 8': 0.0, 'Node 9': 36.4, 'Node 10': 29.0, 'Node 11': 34.4})

search_multiple_path_pruning = Search_problem_from_explicit_graph(
    nodes={'Node 6', 'Node 2', 'Node 8', 'Node 7',
           'Node 4', 'Node 5', 'Node 3', 'Node 0', 'Node 1'},
    arcs=[Arc('Node 0', 'Node 1', 1.0), Arc('Node 0', 'Node 3', 1.0), Arc('Node 0', 'Node 4', 1.0), Arc('Node 1', 'Node 2', 1.0), Arc('Node 1', 'Node 4', 1.0), Arc('Node 2', 'Node 5', 1.0), Arc('Node 2', 'Node 4', 1.0), Arc('Node 3', 'Node 6', 1.0), Arc(
        'Node 3', 'Node 4', 1.0), Arc('Node 4', 'Node 7', 1.0), Arc('Node 4', 'Node 5', 1.0), Arc('Node 4', 'Node 6', 1.0), Arc('Node 4', 'Node 8', 1.0), Arc('Node 5', 'Node 8', 1.0), Arc('Node 6', 'Node 7', 1.0), Arc('Node 7', 'Node 8', 1.0)],
    start='Node 0',
    goals={'Node 8'},
    hmap={'Node 0': 0.0, 'Node 1': 0.0, 'Node 2': 0.0, 'Node 3': 0.0, 'Node 4': 0.0, 'Node 5': 0.0, 'Node 6': 0.0, 'Node 7': 0.0, 'Node 8': 0.0})

search_module_4_graph = Search_problem_from_explicit_graph(
    nodes={'k', 'l', 'j', 'a', 'g', 'h', 'd', 's', 'e', 'i', 'c', 'f', 'b'},
    arcs=[Arc('s', 'a', 2.0), Arc('s', 'c', 1.0), Arc('s', 'k', 2.0), Arc('a', 'b', 2.0), Arc('c', 'd', 1.0), Arc('d', 'e', 1.0), Arc('e', 'f', 1.0),
          Arc('f', 'g', 1.0), Arc('b', 'h', 2.0), Arc('b', 'g', 3.0), Arc('h', 'i', 2.0), Arc('i', 'j', 1.0), Arc('i', 'g', 5.0), Arc('k', 'l', 1.0)],
    start='s',
    goals={'g'},
    hmap={'s': 4.0, 'a': 2.0, 'g': 0.0, 'c': 4.0, 'd': 3.0, 'e': 2.0,
          'f': 1.0, 'b': 3.0, 'h': 4.0, 'i': 5.0, 'j': 6.0, 'k': 5.0, 'l': 6.0})

search_module_5_graph = Search_problem_from_explicit_graph(
    nodes={'tw', 'bg', 'mv', 'cp', 'gb', 'hi',
           'fg', 'uv', 'rs', 'ab', 're', 'fv', 'mi'},
    arcs=[Arc('mi', 'uv', 18.3), Arc('mi', 'fg', 10.7), Arc('mi', 'hi', 9.5), Arc('mi', 'mv', 18.3), Arc('fg', 'hi', 12.3), Arc('fg', 'mi', 10.7), Arc('hi', 'fg', 12.3), Arc('hi', 'mi', 9.5), Arc('mv', 'mi', 18.3), Arc('mv', 'tw', 13.1), Arc('mv', 'gb', 9.5), Arc('tw', 'fv', 13.2), Arc('tw', 'mv', 13.1), Arc('tw', 'gb', 9.6), Arc(
        'fv', 'cp', 8.5), Arc('fv', 'tw', 13.2), Arc('cp', 'fv', 8.5), Arc('gb', 'mv', 9.5), Arc('gb', 'tw', 9.6), Arc('gb', 'bg', 4.7), Arc('uv', 'mi', 18.3), Arc('uv', 'rs', 21.3), Arc('rs', 'ab', 8.8), Arc('rs', 'uv', 21.3), Arc('ab', 're', 12.1), Arc('ab', 'rs', 8.8), Arc('re', 'ab', 12.1), Arc('bg', 'gb', 4.7)],
    start='mi',
    goals={'cp'},
    hmap={'mi': 6.2, 'fg': 15.5, 'hi': 15.4, 'mv': 15.3, 'tw': 16.2, 'fv': 8.5,
          'cp': 0.0, 'gb': 7.4, 'uv': 14.8, 'rs': 20.0, 'ab': 27.4, 're': 27.1, 'bg': 6.4})

search_bicycle_courier_acyclic = Search_problem_from_explicit_graph(
    nodes={'mo', 'slb', 'sec', 'bp', 'ch', 'ase', 'ls', 'trp',
           'al', 'bb', 'fs', 'ws', 'p27', 'rp', 'nyse', 'wtc', 'ac'},
    arcs=[Arc('al', 'wtc', 1.0), Arc('mo', 'al', 2.0), Arc('mo', 'ls', 5.0), Arc('mo', 'ws', 2.0), Arc('mo', 'ch', 1.0), Arc('ch', 'fs', 2.0), Arc('ch', 'ac', 4.0), Arc('ch', 'trp', 3.0), Arc('trp', 'bb', 5.0), Arc('wtc', 'ls', 1.0), Arc('ls', 'sec', 2.0), Arc('ws', 'fs', 2.0), Arc(
        'ws', 'sec', 7.0), Arc('ws', 'nyse', 2.0), Arc('ws', 'ac', 4.0), Arc('ac', 'trp', 3.0), Arc('ac', 'nyse', 1.0), Arc('ac', 'p27', 9.0), Arc('ase', 'slb', 1.0), Arc('ase', 'rp', 1.0), Arc('sec', 'ase', 1.0), Arc('sec', 'bp', 3.0), Arc('sec', 'nyse', 1.0), Arc('nyse', 'bp', 5.0)],
    start='mo',
    goals={'nyse'},
    hmap={'al': 0.0, 'mo': 0.0, 'ch': 0.0, 'trp': 0.0, 'bb': 0.0, 'wtc': 0.0, 'ls': 0.0, 'fs': 0.0, 'ws': 0.0,
          'ac': 0.0, 'p27': 0.0, 'slb': 0.0, 'ase': 0.0, 'rp': 0.0, 'sec': 0.0, 'bp': 0.0, 'nyse': 0.0})

search_bicycle_courier_cyclic = Search_problem_from_explicit_graph(
    nodes={'mo', 'slb', 'sec', 'bp', 'ch', 'ase', 'ls', 'trp',
           'al', 'bb', 'fs', 'ws', 'p27', 'rp', 'nyse', 'wtc', 'ac'},
    arcs=[Arc('al', 'wtc', 1.0), Arc('mo', 'al', 2.0), Arc('mo', 'ls', 5.0), Arc('mo', 'ws', 2.0), Arc('mo', 'ch', 1.0), Arc('ch', 'fs', 2.0), Arc('ch', 'ac', 4.0), Arc('ch', 'trp', 3.0), Arc('trp', 'bb', 5.0), Arc('trp', 'mo', 1.0), Arc('bb', 'bb', 2.0), Arc('wtc', 'ls', 1.0), Arc('ls', 'sec', 2.0), Arc('ws', 'fs', 2.0), Arc('ws', 'sec', 7.0), Arc(
        'ws', 'nyse', 2.0), Arc('ws', 'ac', 4.0), Arc('ac', 'trp', 3.0), Arc('ac', 'nyse', 3.0), Arc('ac', 'p27', 9.0), Arc('slb', 'sec', 6.0), Arc('slb', 'slb', 1.0), Arc('ase', 'slb', 1.0), Arc('ase', 'rp', 1.0), Arc('sec', 'ase', 1.0), Arc('sec', 'bp', 3.0), Arc('sec', 'nyse', 1.0), Arc('nyse', 'bp', 5.0), Arc('nyse', 'ac', 1.0)],
    start='mo',
    goals={'p27'},
    hmap={'al': 0.0, 'mo': 0.0, 'ch': 0.0, 'trp': 0.0, 'bb': 0.0, 'wtc': 0.0, 'ls': 0.0, 'fs': 0.0, 'ws': 0.0,
          'ac': 0.0, 'p27': 0.0, 'slb': 0.0, 'ase': 0.0, 'rp': 0.0, 'sec': 0.0, 'bp': 0.0, 'nyse': 0.0})
