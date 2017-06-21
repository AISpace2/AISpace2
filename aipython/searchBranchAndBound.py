# searchBranchAndBound.py - Branch and Bound Search
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from searchProblem import Path
from utilities import Displayable

class DF_branch_and_bound(Displayable):
    """returns a branch and bound searcher for a problem.    
    An optimal path with cost less than bound can be found by calling search()
    """
    def __init__(self, problem, bound=float("inf")):
        """creates a searcher than can be used with search() to find an optimal path.
        bound gives the initial bound. By default this is infinite - meaning there
        is no initial pruning due to depth bound
        """
        self.problem = problem
        self.best_path = None
        self.bound = bound

    def search(self):
        """returns an optimal solution to a problem with cost less than bound.
        returns None if there is no solution with cost less than bound."""
        self.number_expanded=0
        frontier = [Path(node) for node in reversed(self.problem.start_nodes())]
        while frontier:
            path = frontier.pop()
            if path.cost+self.problem.heuristic(path.end()) < self.bound:
                self.display(3,"Expanding:",path,"cost:",path.cost)
                self.number_expanded += 1
                if self.problem.is_goal(path.end()):
                    self.best_path = path
                    self.bound = path.cost
                    self.display(2,"New best path:",path," cost:",path.cost)
                frontier += reversed([Path(path, arc)
                                      for arc in self.problem.neighbors(path.end())])
        self.display(1,"Number of nodes expanded:",self.number_expanded)
        self.solution = self.best_path
        return self.best_path
        
from searchAStar import test
if __name__ == "__main__":
    test(DF_branch_and_bound)

# Example queries:
# import searchProblem 
# searcherb1 = DF_branch_and_bound(searchProblem.acyclic_delivery_problem)
# print(searcherb1.search())        # find optimal path
# searcherb2 = DF_branch_and_bound(searchProblem.cyclic_delivery_problem, bound=100)
# print(searcherb2.search())        # find optimal path

