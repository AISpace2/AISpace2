# searchBranchAndBound.py - Branch and Bound Search
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from aipython.searchProblem import Path
from aipython.searchGeneric import Searcher
from aipython.utilities import Displayable
from aispace2.jupyter.search import visualize

class DF_branch_and_bound(Searcher):
    """returns a branch and bound searcher for a problem.    
    An optimal path with cost less than bound can be found by calling search()
    """
    def __init__(self, problem, bound=float("inf")):
        """creates a searcher than can be used with search() to find an optimal path.
        bound gives the initial bound. By default this is infinite - meaning there
        is no initial pruning due to depth bound
        """
        super().__init__(problem)
        self.best_path = None
        self.bound = bound

    @visualize
    def search(self):
        """returns an optimal solution to a problem with cost less than bound.
        returns None if there is no solution with cost less than bound."""
        self.frontier = [Path(self.problem.start_node())]
        self.num_expanded = 0
        while self.frontier:
            path = self.frontier.pop()
            if path.cost+self.problem.heuristic(path.end()) < self.bound:
                self.display(3,"Expanding:",path,"cost:",path.cost)
                self.num_expanded += 1
                if self.problem.is_goal(path.end()):
                    self.best_path = path
                    self.bound = path.cost
                    self.display(2,"New best path:",path," cost:",path.cost)
                else:
                    neighs = self.problem.neighbors(path.end())
                    self.display(3,"Neighbors are", neighs)
                    for arc in reversed(list(neighs)):
                        self.add_to_frontier(Path(path, arc))
                    self.display(3,"Frontier:",self.frontier)
        self.display(1,"Number of paths expanded:",self.num_expanded)
        self.solution = self.best_path
        return self.best_path
        
from aipython.searchGeneric import test
if __name__ == "__main__":
    test(DF_branch_and_bound)

# Example queries:
# import searchProblem 
# searcherb1 = DF_branch_and_bound(searchProblem.acyclic_delivery_problem)
# print(searcherb1.search())        # find optimal path
# searcherb2 = DF_branch_and_bound(searchProblem.cyclic_delivery_problem, bound=100)
# print(searcherb2.search())        # find optimal path

