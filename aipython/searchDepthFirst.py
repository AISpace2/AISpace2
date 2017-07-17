# searchDepthFirst.py - Depth-first Search for finding goals using an explicit stack of iterators
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from searchProblem import Path
from utilities import Displayable

class Depth_first_search(Displayable):
    """returns a depth-first searcher for a problem.
   
    This uses a list of iterators of nodes. "top" is the top-level iterator.
    The frontier contains iterators that may be needed to solve the problem.
    """
    def __init__(self, problem, bound=100000):
        self.problem = problem
        self.bound = bound  # default bound unless overridden in search
        self.top = iter([self.problem.start_node()])
        self.frontier = []    # list of iterators that generare all unexplored paths
        self.num_expanded = 0 # number of paths expanded
        self.hit_depth_bound = False # true when some paths hit the depth-bound

    def search(self, bound = None):
        """finds a goal with number of arcs less than bound if there is one.
        returns None if there is no path to a goal"""
        if bound is None: bound = self.bound
        while True:
            try:
                node = next(self.top)   #current path
                self.num_expanded += 1
                if self.problem.is_goal(node):
                    self.display(1,"DFS found goal",node,"There were",
                               self.num_expanded,"paths expanded")
                    return node
                elif len(self.frontier) < bound:
                    self.frontier.append(self.top)
                    self.display(2,"DFS expanding node",node)
                    self.top = self.problem.neighbor_nodes(node)
                else:
                    self.hit_depth_bound = True
                    self.display(2,"DFS hit depth bound at node",node)
            except StopIteration:  #top has no more elements
                self.display(2,"popping off frontier")
                if self.frontier:
                    self.top = self.frontier.pop()
                else:
                    self.display(1,"No path found. There were",
                              self.num_expanded,"paths expanded")
                    return None

# example queries:
# from searchDepthFirst import Depth_first_search
# import searchProblem 
# searcher1 = Depth_first_search(searchProblem.acyclic_delivery_problem)
# print(searcher1.search())        # find next path
# searcher2 = Depth_first_search(searchProblem.problem2)
# print(searcher2.search())        # find next path
# searcher3 = Depth_first_search(searchProblem.cyclic_delivery_problem)
# s3=searcher3.search()       # find next path - will go forever(?)

