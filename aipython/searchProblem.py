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
        return "\n".join("".join(str(["{} ({})".format(p, n) for (n, c, p) in self.frontierpq])).split("\\n"))

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
            return (str(self.initial) + "\n   --" + str(self.arc.action)
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
    positions={'g': (60, 483), 'd': (229, 110), 'a': (919, 385), 'b': (659, 60), 'c': (489, 436)})

search_simple2 = Search_problem_from_explicit_graph(
    {'a', 'b', 'c', 'd', 'e', 'g', 'h', 'j'},
    [Arc('a', 'b', 1), Arc('b', 'c', 3), Arc('b', 'd', 1), Arc(
        'd', 'e', 3), Arc('d', 'g', 1), Arc('a', 'h', 3), Arc('h', 'j', 1)],
    start='a',
    goals={'g'})

search_edgeless = Search_problem_from_explicit_graph(
    {'a', 'b', 'c', 'd', 'e', 'g', 'h', 'j'},
    [],
    start='g',
    goals={'k', 'g'})

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
    }
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
    }
)
