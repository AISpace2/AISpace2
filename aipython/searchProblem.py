# searchProblem.py - representations of search problems
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en


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
    [Arc('a', 'b', 1), Arc('a', 'c', 3), Arc('b', 'c', 1), Arc('b', 'd', 3), Arc('c', 'd', 1), Arc('c', 'g', 3), Arc('d', 'g', 1)],
    start='a',
    goals={'g'},
    positions={'g': (60, 483), 'd': (229, 110), 'a': (919, 385), 'b': (659, 60), 'c': (489, 436)})

search_simple2 = Search_problem_from_explicit_graph(
    {'a', 'b', 'c', 'd', 'e', 'g', 'h', 'j'},
    [Arc('a', 'b', 1), Arc('b', 'c', 3), Arc('b', 'd', 1), Arc('d', 'e', 3), Arc('d', 'g', 1), Arc('a', 'h', 3), Arc('h', 'j', 1)],
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

sample_tree_graph = Search_problem_from_explicit_graph({'S','N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','G',},
                 [Arc('S','N1',9.9),
                 Arc('N1','N3',11.9),
                  Arc('N3','N7',9.6),
                  Arc('N1','N4',9.1),
                 Arc('N4','N8',8.7),
                 Arc('S','N2',10.6),
                 Arc('N2','N5',9.1),
                 Arc('N5','N9',8.6),
                 Arc('N5','G',8.8),
                 Arc('N2','N6',12.8),
                 Arc('N6','N10',8.5),],
                     start='S',
                goals={'G'},
                 hmap ={'S':26.0,'N1':25.1,'N2':16.4,'N3':27.6,'N4':18.1,'N5':8.8,'N6':8.5,'N7':28.0,'N8':18.7,'N9':10,'N10':6.5,'G':0,},
                    positions={
"S": (278,50),
"N5": (307,186),
"N9": (255,247),
"G": (349,247),
"N10": (442,240),
"N6": (424,156),
"N2": (372,111),
"N1": (147,99),
"N3": (62,156),
"N7": (38,226),
"N4": (183,166),
"N8": (142,236)})

extend_tree_graph = Search_problem_from_explicit_graph(
    nodes={'N2', 'N3', 'N20', 'N1', 'S', 'N11', 'N18', 'N10', 'N8', 'N19', 'N13', 'N15', 'N4', 'N17', 'N14', 'N9', 'N16', 'N12', 'N6', 'N5', 'N7', 'G'},
    arcs=[Arc('N1', 'N3', 11.9), Arc('N1', 'N4', 9.1), Arc('N2', 'N6', 12.8), Arc('N2', 'N5', 9.1), Arc('S', 'N1', 9.9), Arc('S', 'N2', 10.6), Arc('N5', 'N9', 8.6), Arc('N5', 'N10', 2.0), Arc('N4', 'N8', 8.7), Arc('N3', 'N7', 16.6), Arc('N9', 'N13', 4.0), Arc('N9', 'N14', 5.0), Arc('N14', 'N18', 3.0), Arc('N14', 'G', 4.0), Arc('N6', 'N12', 2.0), Arc('N12', 'N16', 6.0), Arc('N6', 'N11', 8.0), Arc('N11', 'N15', 8.0), Arc('N15', 'N19', 10.0), Arc('N7', 'N20', 2.0), Arc('N13', 'N17', 6.0)],
    start='S',
    goals={'G'},
    hmap={'N1': 27.1, 'N2': 18.4, 'N3': 30.2, 'N4': 28.9, 'N6': 10.5, 'N5': 14.8, 'N18': 0.0, 'S': 30.0, 'N9': 8.0, 'N10': 14.5, 'N8': 30.0, 'N7': 32.0, 'N13': 15.0, 'N14': 0.0, 'G': 0.0, 'N15': 14.0, 'N16': 13.0, 'N12': 14.9, 'N11': 14.0, 'N19': 17.0, 'N20': 33.0, 'N17': 10.0},
    positions={'N1': (7723.0767, 5182.8604), 'N2': (7867.8647, 5163.451), 'N3': (7584.081, 5286.368), 'N4': (7747.4663, 5295.6665), 'N6': (8075.205, 5266.595), 'N5': (7895.591, 5276.804), 'N18': (7905.7705, 5590.145), 'S': (7797.393, 5079.8394), 'N9': (7858.6997, 5388.454), 'N10': (7982.9863, 5382.1826), 'N8': (7724.952, 5387.6284), 'N7': (7546.7407, 5379.1914), 'N13': (7796.918, 5492.031), 'N14': (7954.2715, 5479.5015), 'G': (8014.078, 5585.455), 'N15': (8122.802, 5475.834), 'N16': (8268.428, 5473.6763), 'N12': (8254.093, 5352.59), 'N11': (8106.6533, 5366.197), 'N19': (8128.3945, 5585.9844), 'N20': (7545.5723, 5478.4287), 'N17': (7800.804, 5590.161)})

cyclic_graph_example = Search_problem_from_explicit_graph(
    nodes={'Node 6', 'Node 2', 'Node 7', 'Node 4', 'Node 5', 'Node 3', 'Node 0', 'Node 1'},
    arcs=[Arc('Node 0', 'Node 2', 11.8), Arc('Node 0', 'Node 3', 11.7), Arc('Node 1', 'Node 3', 11.9), Arc('Node 1', 'Node 4', 12.1), Arc('Node 2', 'Node 5', 11.4), Arc('Node 3', 'Node 2', 14.4), Arc('Node 3', 'Node 4', 15.4), Arc('Node 4', 'Node 6', 11.3), Arc('Node 5', 'Node 3', 11.4), Arc('Node 5', 'Node 7', 11.9), Arc('Node 6', 'Node 3', 11.7), Arc('Node 6', 'Node 7', 12.2)],
    start='Node 1',
    goals={'Node 7'},
    hmap={'Node 0': 28.4, 'Node 1': 28.3, 'Node 2': 23.3, 'Node 3': 18.1, 'Node 4': 23.6, 'Node 5': 11.9, 'Node 6': 12.2, 'Node 7': 0.0},
    positions={'Node 0': (7781.7725, 5041.314), 'Node 1': (7985.3047, 5042.698), 'Node 2': (7680.699, 5170.079), 'Node 3': (7880.077, 5170.079), 'Node 4': (8093.301, 5170.079), 'Node 5': (7780.388, 5293.3057), 'Node 6': (7990.843, 5289.152), 'Node 7': (7884.231, 5420.686)})

vancouver_neighbour = Search_problem_from_explicit_graph(
    nodes={'DT', 'KD', 'JB', 'UBC', 'SRY', 'BBY', 'MP', 'SP', 'KB', 'AP', 'RM'},
    arcs=[Arc('UBC', 'JB', 3.0), Arc('UBC', 'KD', 3.0), Arc('DT', 'SP', 2.0), Arc('JB', 'KB', 4.0), Arc('KD', 'JB', 4.0), Arc('KD', 'MP', 3.0), Arc('KB', 'DT', 2.0), Arc('KB', 'BBY', 6.0), Arc('MP', 'KB', 4.0), Arc('MP', 'BBY', 5.0), Arc('MP', 'RM', 3.0), Arc('RM', 'AP', 3.0), Arc('RM', 'SRY', 21.0), Arc('SRY', 'BBY', 22.0)],
    start='UBC',
    goals={'SP'},
    hmap={'UBC': 5.0, 'SP': 0.0, 'DT': 2.0, 'JB': 3.0, 'KD': 6.0, 'KB': 3.0, 'MP': 7.0, 'BBY': 8.0, 'AP': 8.0, 'RM': 9.0, 'SRY': 29.0},
    positions={'UBC': (7742.247, 5153.922), 'SP': (7811.536, 5038.2285), 'DT': (7875.7397, 5038.864), 'JB': (7808.358, 5116.417), 'KD': (7815.35, 5202.8696), 'KB': (7889.7246, 5113.874), 'MP': (7936.765, 5209.862), 'BBY': (8018.132, 5164.093), 'AP': (7821.0713, 5293.7715), 'RM': (7913.245, 5293.7715), 'SRY': (8032.753, 5289.9575)})

misleading_heuristic = Search_problem_from_explicit_graph(
    nodes={'Node 6', 'Node 2', 'Node 10', 'Node 8', 'Node 7', 'Node 4', 'Node 5', 'Node 3', 'Node 0', 'Node 1', 'Node 11', 'Node 9'},
    arcs=[Arc('Node 0', 'Node 1', 7.1), Arc('Node 0', 'Node 6', 11.5), Arc('Node 0', 'Node 10', 12.0), Arc('Node 1', 'Node 2', 6.9), Arc('Node 2', 'Node 3', 9.4), Arc('Node 3', 'Node 4', 7.9), Arc('Node 4', 'Node 5', 9.2), Arc('Node 5', 'Node 2', 11.9), Arc('Node 6', 'Node 7', 25.5), Arc('Node 6', 'Node 9', 8.4), Arc('Node 7', 'Node 8', 18.4), Arc('Node 10', 'Node 11', 9.1)],
    start='Node 0',
    goals={'Node 8'},
    hmap={'Node 0': 28.9, 'Node 1': 23.7, 'Node 2': 17.0, 'Node 3': 10.0, 'Node 4': 15.0, 'Node 5': 21.1, 'Node 6': 34.2, 'Node 7': 18.4, 'Node 8': 0.0, 'Node 9': 36.4, 'Node 10': 29.0, 'Node 11': 34.4},
    positions={'Node 0': (7851.313, 5094.2427), 'Node 1': (7830.8735, 5144.2056), 'Node 2': (7845.257, 5194.1685), 'Node 3': (7907.332, 5228.234), 'Node 4': (7960.3228, 5200.9814), 'Node 5': (7920.201, 5144.2056), 'Node 6': (7764.257, 5091.9717), 'Node 7': (7774.855, 5285.01), 'Node 8': (7912.631, 5303.935), 'Node 9': (7810.4346, 5048.065), 'Node 10': (7941.3975, 5085.9155), 'Node 11': (8005.7437, 5060.934)})

multiple_path_pruning_demo = Search_problem_from_explicit_graph(
    nodes={'Node 6', 'Node 2', 'Node 8', 'Node 7', 'Node 4', 'Node 5', 'Node 3', 'Node 0', 'Node 1'},
    arcs=[Arc('Node 0', 'Node 1', 1.0), Arc('Node 0', 'Node 3', 1.0), Arc('Node 0', 'Node 4', 1.0), Arc('Node 1', 'Node 2', 1.0), Arc('Node 1', 'Node 4', 1.0), Arc('Node 2', 'Node 5', 1.0), Arc('Node 2', 'Node 4', 1.0), Arc('Node 3', 'Node 6', 1.0), Arc('Node 3', 'Node 4', 1.0), Arc('Node 4', 'Node 7', 1.0), Arc('Node 4', 'Node 5', 1.0), Arc('Node 4', 'Node 6', 1.0), Arc('Node 4', 'Node 8', 1.0), Arc('Node 5', 'Node 8', 1.0), Arc('Node 6', 'Node 7', 1.0), Arc('Node 7', 'Node 8', 1.0)],
    start='Node 0',
    goals={'Node 8'},
    hmap={'Node 0': 0.0, 'Node 1': 0.0, 'Node 2': 0.0, 'Node 3': 0.0, 'Node 4': 0.0, 'Node 5': 0.0, 'Node 6': 0.0, 'Node 7': 0.0, 'Node 8': 0.0},
    positions={'Node 0': (7742.419, 5048.3457), 'Node 1': (7741.0083, 5172.4736), 'Node 2': (7742.419, 5303.6543), 'Node 3': (7886.295, 5048.3457), 'Node 4': (7887.705, 5172.4736), 'Node 5': (7889.1157, 5303.6543), 'Node 6': (8030.1704, 5048.3457), 'Node 7': (8031.581, 5173.8843), 'Node 8': (8032.9917, 5303.6543)})

robot_acyclic = Search_problem_from_explicit_graph(
    nodes={'c3', 'c2', 'o111', 'storage', 'o125', 'b1', 'r123', 'o103', 'c1', 'b4', 'b3', 'ts', 'b2', 'o123', 'o119', 'mail', 'o109'},
    arcs=[Arc('ts', 'mail', 6.0), Arc('o103', 'ts', 8.0), Arc('o103', 'b3', 4.0), Arc('b3', 'b4', 7.0), Arc('b3', 'b1', 4.0), Arc('b1', 'c2', 3.0), Arc('c2', 'c1', 4.0), Arc('c2', 'c3', 6.0), Arc('c1', 'c3', 8.0), Arc('b1', 'b2', 6.0), Arc('b2', 'b4', 3.0), Arc('o123', 'r123', 4.0), Arc('o123', 'o125', 4.0), Arc('o119', 'o123', 9.0), Arc('o103', 'o109', 12.0), Arc('b4', 'o109', 7.0), Arc('o109', 'o111', 4.0), Arc('o109', 'o119', 16.0), Arc('o119', 'storage', 7.0)],
    start='o103',
    goals={'r123'},
    hmap={'mail': 26.0, 'ts': 23.0, 'o103': 21.0, 'o111': 27.0, 'c1': 6.0, 'b4': 18.0, 'b3': 17.0, 'b1': 13.0, 'c2': 10.0, 'c3': 12.0, 'b2': 15.0, 'o123': 4.0, 'r123': 0.0, 'o125': 6.0, 'o119': 11.0, 'o109': 24.0, 'storage': 12.0},
    positions={'mail': (7742.061, 5304.6924), 'ts': (7787.5283, 5304.6924), 'o103': (7846.0737, 5304.6924), 'o111': (8027.939, 5304.6924), 'c1': (7846.0737, 5138.397), 'b4': (7917.0767, 5251.1284), 'b3': (7846.795, 5255.093), 'b1': (7846.795, 5211.858), 'c2': (7845.714, 5178.716), 'c3': (7916.092, 5179.797), 'b2': (7917.437, 5215.462), 'o123': (7848.018, 5107.4697), 'r123': (7849.099, 5060.263), 'o125': (7798.637, 5104.5864), 'o119': (7962.2134, 5107.1094), 'o109': (7976.267, 5303.9717), 'storage': (8020.1587, 5047.308)})

robot_cyclic = Search_problem_from_explicit_graph(
    nodes={'c3', 'c2', 'o111', 'storage', 'o125', 'b1', 'r123', 'o103', 'c1', 'b4', 'b3', 'ts', 'b2', 'o123', 'o119', 'mail', 'o109'},
    arcs=[Arc('ts', 'mail', 6.0), Arc('o103', 'ts', 8.0), Arc('o103', 'b3', 4.0), Arc('b3', 'b4', 7.0), Arc('b3', 'b1', 4.0), Arc('b1', 'c2', 3.0), Arc('c2', 'c1', 4.0), Arc('c2', 'c3', 6.0), Arc('c1', 'c3', 8.0), Arc('b1', 'b2', 6.0), Arc('b2', 'b4', 3.0), Arc('o123', 'r123', 4.0), Arc('o123', 'o125', 4.0), Arc('o119', 'o123', 9.0), Arc('o103', 'o109', 12.0), Arc('b4', 'o109', 7.0), Arc('o109', 'o111', 4.0), Arc('o109', 'o119', 16.0), Arc('o119', 'storage', 7.0), Arc('o125', 'o123', 4.0), Arc('r123', 'o123', 4.0), Arc('o123', 'o119', 9.0), Arc('storage', 'o119', 7.0), Arc('o119', 'o109', 16.0), Arc('o111', 'o109', 4.0), Arc('o109', 'o103', 12.0), Arc('ts', 'o103', 8.0), Arc('mail', 'ts', 6.0), Arc('b4', 'b3', 7.0), Arc('b4', 'b2', 3.0), Arc('b2', 'b1', 6.0), Arc('b1', 'b3', 4.0), Arc('c3', 'c2', 6.0), Arc('c1', 'c2', 4.0), Arc('c3', 'c1', 8.0)],
    start='o103',
    goals={'r123'},
    hmap={'mail': 26.0, 'ts': 23.0, 'o103': 21.0, 'o111': 27.0, 'c1': 6.0, 'b4': 18.0, 'b3': 17.0, 'b1': 13.0, 'c2': 10.0, 'c3': 12.0, 'b2': 15.0, 'o123': 4.0, 'r123': 0.0, 'o125': 6.0, 'o119': 11.0, 'o109': 24.0, 'storage': 12.0},
    positions={'mail': (7742.033, 5304.7173), 'ts': (7787.509, 5304.7173), 'o103': (7846.066, 5304.7173), 'o111': (8027.9663, 5304.7173), 'c1': (7846.066, 5138.3896), 'b4': (7917.082, 5251.1436), 'b3': (7846.787, 5255.108), 'b1': (7846.787, 5211.8647), 'c2': (7845.706, 5178.716), 'c3': (7916.098, 5179.798), 'b2': (7917.4424, 5215.4697), 'o123': (7848.0103, 5107.4565), 'r123': (7849.092, 5060.24), 'o125': (7798.6196, 5104.573), 'o119': (7962.228, 5107.096), 'o109': (7976.284, 5303.9966), 'storage': (8020.1846, 5047.283)})

module_4_graph = Search_problem_from_explicit_graph(
    nodes={'k', 'l', 'j', 'a', 'g', 'h', 'd', 's', 'e', 'i', 'c', 'f', 'b'},
    arcs=[Arc('s', 'a', 2.0), Arc('s', 'c', 1.0), Arc('s', 'k', 2.0), Arc('a', 'b', 2.0), Arc('c', 'd', 1.0), Arc('d', 'e', 1.0), Arc('e', 'f', 1.0), Arc('f', 'g', 1.0), Arc('b', 'h', 2.0), Arc('b', 'g', 3.0), Arc('h', 'i', 2.0), Arc('i', 'j', 1.0), Arc('i', 'g', 5.0), Arc('k', 'l', 1.0)],
    start='s',
    goals={'g'},
    hmap={'s': 4.0, 'a': 2.0, 'g': 0.0, 'c': 4.0, 'd': 3.0, 'e': 2.0, 'f': 1.0, 'b': 3.0, 'h': 4.0, 'i': 5.0, 'j': 6.0, 'k': 5.0, 'l': 6.0},
    positions={'s': (7894.0034, 5096.527), 'a': (7897.657, 5169.6055), 'g': (7890.9585, 5248.1655), 'c': (7940.8955, 5119.6685), 'd': (7949.4214, 5156.817), 'e': (7953.0757, 5193.3564), 'f': (7935.4146, 5226.8506), 'b': (7834.3223, 5190.3115), 'h': (7796.565, 5228.6777), 'i': (7784.994, 5265.826), 'j': (7777.686, 5304.1924), 'k': (7967.6914, 5077.039), 'l': (7996.314, 5047.8076)})

module_5_graph = Search_problem_from_explicit_graph(
    nodes={'tw', 'bg', 'mv', 'cp', 'gb', 'hi', 'fg', 'uv', 'rs', 'ab', 're', 'fv', 'mi'},
    arcs=[Arc('mi', 'uv', 18.3), Arc('mi', 'fg', 10.7), Arc('mi', 'hi', 9.5), Arc('mi', 'mv', 18.3), Arc('fg', 'hi', 12.3), Arc('fg', 'mi', 10.7), Arc('hi', 'fg', 12.3), Arc('hi', 'mi', 9.5), Arc('mv', 'mi', 18.3), Arc('mv', 'tw', 13.1), Arc('mv', 'gb', 9.5), Arc('tw', 'fv', 13.2), Arc('tw', 'mv', 13.1), Arc('tw', 'gb', 9.6), Arc('fv', 'cp', 8.5), Arc('fv', 'tw', 13.2), Arc('cp', 'fv', 8.5), Arc('gb', 'mv', 9.5), Arc('gb', 'tw', 9.6), Arc('gb', 'bg', 4.7), Arc('uv', 'mi', 18.3), Arc('uv', 'rs', 21.3), Arc('rs', 'ab', 8.8), Arc('rs', 'uv', 21.3), Arc('ab', 're', 12.1), Arc('ab', 'rs', 8.8), Arc('re', 'ab', 12.1), Arc('bg', 'gb', 4.7)],
    start='mi',
    goals={'cp'},
    hmap={'mi': 6.2, 'fg': 15.5, 'hi': 15.4, 'mv': 15.3, 'tw': 16.2, 'fv': 8.5, 'cp': 0.0, 'gb': 7.4, 'uv': 14.8, 'rs': 20.0, 'ab': 27.4, 're': 27.1, 'bg': 6.4},
    positions={'mi': (7855.3726, 5105.905), 'fg': (7787.803, 5104.6416), 'hi': (7840.8486, 5047.8076), 'mv': (7970.9355, 5102.1157), 'tw': (7970.3037, 5184.841), 'fv': (7886.9473, 5189.261), 'cp': (7880.6323, 5136.2163), 'gb': (7926.731, 5142.5312), 'uv': (7840.8486, 5220.836), 'rs': (7975.356, 5220.204), 'ab': (7984.197, 5275.144), 're': (7913.4697, 5304.1924), 'bg': (7915.3643, 5115.377)})

bicycle_courier_acyclic = Search_problem_from_explicit_graph(
    nodes={'mo', 'slb', 'sec', 'bp', 'ch', 'ase', 'ls', 'trp', 'al', 'bb', 'fs', 'ws', 'p27', 'rp', 'nyse', 'wtc', 'ac'},
    arcs=[Arc('al', 'wtc', 1.0), Arc('mo', 'al', 2.0), Arc('mo', 'ls', 5.0), Arc('mo', 'ws', 2.0), Arc('mo', 'ch', 1.0), Arc('ch', 'fs', 2.0), Arc('ch', 'ac', 4.0), Arc('ch', 'trp', 3.0), Arc('trp', 'bb', 5.0), Arc('wtc', 'ls', 1.0), Arc('ls', 'sec', 2.0), Arc('ws', 'fs', 2.0), Arc('ws', 'sec', 7.0), Arc('ws', 'nyse', 2.0), Arc('ws', 'ac', 4.0), Arc('ac', 'trp', 3.0), Arc('ac', 'nyse', 1.0), Arc('ac', 'p27', 9.0), Arc('ase', 'slb', 1.0), Arc('ase', 'rp', 1.0), Arc('sec', 'ase', 1.0), Arc('sec', 'bp', 3.0), Arc('sec', 'nyse', 1.0), Arc('nyse', 'bp', 5.0)],
    start='mo',
    goals={'nyse'},
    hmap={'al': 0.0, 'mo': 0.0, 'ch': 0.0, 'trp': 0.0, 'bb': 0.0, 'wtc': 0.0, 'ls': 0.0, 'fs': 0.0, 'ws': 0.0, 'ac': 0.0, 'p27': 0.0, 'slb': 0.0, 'ase': 0.0, 'rp': 0.0, 'sec': 0.0, 'bp': 0.0, 'nyse': 0.0},
    positions={'al': (7680.5317, 5048.8813), 'mo': (7769.275, 5048.8813), 'ch': (7867.612, 5048.8813), 'trp': (7979.54, 5048.8813), 'bb': (8079.4756, 5048.8813), 'wtc': (7680.5317, 5132.8276), 'ls': (7769.275, 5132.8276), 'fs': (7867.612, 5116.838), 'ws': (7867.612, 5179.9976), 'ac': (7979.54, 5138.4243), 'p27': (8091.468, 5182.396), 'slb': (7735.6963, 5193.589), 'ase': (7735.6963, 5274.337), 'rp': (7682.131, 5274.337), 'sec': (7809.249, 5245.555), 'bp': (7869.2104, 5303.1187), 'nyse': (7930.771, 5245.555)})

bicycle_courier_cyclic = Search_problem_from_explicit_graph(
    nodes={'mo', 'slb', 'sec', 'bp', 'ch', 'ase', 'ls', 'trp', 'al', 'bb', 'fs', 'ws', 'p27', 'rp', 'nyse', 'wtc', 'ac'},
    arcs=[Arc('al', 'wtc', 1.0), Arc('mo', 'al', 2.0), Arc('mo', 'ls', 5.0), Arc('mo', 'ws', 2.0), Arc('mo', 'ch', 1.0), Arc('ch', 'fs', 2.0), Arc('ch', 'ac', 4.0), Arc('ch', 'trp', 3.0), Arc('trp', 'bb', 5.0), Arc('trp', 'mo', 1.0), Arc('bb', 'bb', 2.0), Arc('wtc', 'ls', 1.0), Arc('ls', 'sec', 2.0), Arc('ws', 'fs', 2.0), Arc('ws', 'sec', 7.0), Arc('ws', 'nyse', 2.0), Arc('ws', 'ac', 4.0), Arc('ac', 'trp', 3.0), Arc('ac', 'nyse', 3.0), Arc('ac', 'p27', 9.0), Arc('slb', 'sec', 6.0), Arc('slb', 'slb', 1.0), Arc('ase', 'slb', 1.0), Arc('ase', 'rp', 1.0), Arc('sec', 'ase', 1.0), Arc('sec', 'bp', 3.0), Arc('sec', 'nyse', 1.0), Arc('nyse', 'bp', 5.0), Arc('nyse', 'ac', 1.0)],
    start='mo',
    goals={'p27'},
    hmap={'al': 0.0, 'mo': 0.0, 'ch': 0.0, 'trp': 0.0, 'bb': 0.0, 'wtc': 0.0, 'ls': 0.0, 'fs': 0.0, 'ws': 0.0, 'ac': 0.0, 'p27': 0.0, 'slb': 0.0, 'ase': 0.0, 'rp': 0.0, 'sec': 0.0, 'bp': 0.0, 'nyse': 0.0},
    positions={'al': (7683.0405, 5052.013), 'mo': (7777.0176, 5048.854), 'ch': (7867.836, 5064.6484), 'trp': (7979.1875, 5048.854), 'bb': (8077.1133, 5052.013), 'wtc': (7683.0405, 5134.934), 'ls': (7770.6997, 5134.934), 'fs': (7867.836, 5119.1396), 'ws': (7867.836, 5181.5283), 'ac': (7978.398, 5140.4624), 'p27': (8088.9595, 5183.8975), 'slb': (7737.5312, 5194.9536), 'ase': (7737.5312, 5274.716), 'rp': (7684.6196, 5274.716), 'sec': (7810.186, 5246.2856), 'bp': (7869.4155, 5303.146), 'nyse': (7930.2246, 5246.2856)})
