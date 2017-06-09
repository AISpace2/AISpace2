# searchMPP.py - Searcher with multiple-path pruning
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from searchAStar import Searcher
from searchProblem import Path

class SearcherMPP(Searcher):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    """
    def __init__(self, problem, method='astar'):
        Searcher.__init__(self, problem, method)
        self.expanded = set()

    def search(self):
        """returns next path from an element of problem's start nodes
        to a goal node. 
        Returns None if no path exists.
        """
        while not self.frontier.empty():
            path = self.frontier.pop()
            if path.end() not in self.expanded:
                self.display(2, "Expanding: ",path,"(cost:",path.cost,")")
                self.expanded.add(path.end())
                self.num_expanded += 1
                if self.problem.is_goal(path.end()):
                    self.display(1, self.num_expanded, "nodes have been expanded and",
                            len(self.frontier.frontierpq), "nodes remain in the frontier")
                    self.solution = path   # store the solution found
                    return path
                else:
                    neighs = self.problem.neighbors(path.end())
                    for arc in neighs:
                        self.add_to_frontier(Path(path,arc))
                    self.display(3,"Frontier:",self.frontier)

from searchAStar import test
if __name__ == "__main__":
    test(SearcherMPP)

import searchProblem 
# searcherMPPcdp = SearcherMPP(searchProblem.cyclic_delivery_problem)
# print(searcherMPPcdp.search())  # find first path

