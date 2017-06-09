# searchAStar.py - A* and related searchers
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import heapq        # part of the Python standard library
from searchProblem import Path

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
        heapq.heappush(self.frontierpq,(value, -self.frontier_index, path))

    def pop(self):
        """returns and removes the path of the frontier with minimum value.
        Note that [2] extracts the path from the triple on the queue.
        """
        return heapq.heappop(self.frontierpq)[2] 

    def count(self,val):
        """returns the number of elements of the frontier with value=val"""
        return sum(1 for e in self.frontierpq if e[0]==val)

    def __repr__(self):
        """string representation of the frontier"""
        return str([(n,c,str(p)) for (n,c,p) in self.frontierpq])

from utilities import Displayable

class Searcher(Displayable):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    """

    def __init__(self, problem, method='astar'):
        """creates a searcher from a problem
        method is 'astar' or 'best-first' or 'lowest-cost-first'
        """
        self.problem = problem
        self.method = method  # not used
        self.frontier = Frontier()
        self.num_expanded = 0
        for node in problem.start_nodes():
            self.add_to_frontier(Path(node))
        self.display(3,"Frontier:",self.frontier)
    
    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost"""
        if self.method=='astar':
            value = path.cost+self.problem.heuristic(path.end())
        else:
            assert False, "unknown method "+str(self.method)
        self.frontier.add(path, value)

    def search(self):
        """returns (next) path from an element of problem's start nodes
        to a goal node. 
        Returns None if no path exists.
        """
        while not self.frontier.empty():
            path = self.frontier.pop()
            self.display(2, "Expanding:",path,"(cost:",path.cost,")")
            self.num_expanded += 1
            if self.problem.is_goal(path.end()):    # solution found
                self.display(1, self.num_expanded, "paths have been expanded and",
                            len(self.frontier.frontierpq), "nodes remain in the frontier")
                self.solution = path   # store the solution found
                return path
            else:
                neighs = self.problem.neighbors(path.end())
                for arc in neighs:
                    self.add_to_frontier(Path(path,arc))
                self.display(3,"Frontier:",self.frontier)
        self.display(1,"No (more) solutions. Total of",
                     self.frontier.frontier_index,"paths expanded.")

import searchProblem 
def test(SearchClass):
    print("Testing problem 1:")
    schr1 = SearchClass(searchProblem.problem1)
    path1 = schr1.search()
    print("Path found: ",path1)
    assert list(path1.nodes()) == ['g','d','c','b','a'], "Shortest path not found in problem1"
    print("Passed unit test")

if __name__ == "__main__":
    test(Searcher)

# example queries:
# searcher1 = Searcher(searchProblem.acyclic_delivery_problem)
# searcher1.search()  # find first path
# searcher1.search()  # find next path
# searcher2 = Searcher(searchProblem.cyclic_delivery_problem)
# searcher2.search()  # find first path
# searcher2.search()  # find next path

