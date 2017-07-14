# cspSearch.py - Representations of a Search Problem from a CSP.
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from cspProblem import CSP, Constraint
from searchProblem import Arc, Search_problem
from utilities import dict_union

class Search_from_CSP(Search_problem):
    """A search problem directly from the CSP.

    A node is a variable:value dictionary"""
    def __init__(self, csp, variable_order=None):
        self.csp=csp
        if variable_order:
            assert set(variable_order) == set(csp.variables)
            assert len(variable_order) == len(csp.variables)
            self.variables = variable_order
        else:
            self.variables = list(csp.variables)

    def is_goal(self, node):
        return len(node)==len(self.csp.variables)
    
    def start_nodes(self):
        return [{}]
    
    def neighbor_nodes(self, node):
        """iterator over the neighboring nodes of node"""
        var = self.variables[len(node)] # the next variable
        for val in self.csp.domains[var]:
            new_env = dict_union(node,{var:val})  #dictionary union
            if self.csp.consistent(new_env):
                yield new_env

from cspExamples import csp1,csp2,test
from searchDepthFirst import Depth_first_search

def dfs_solver(csp):
    """depth-first search"""
    return Depth_first_search(Search_from_CSP(csp)).search()

if __name__ == "__main__":
    test(dfs_solver)

## Test Solving CSPs with Search:
searcher1 = Depth_first_search(Search_from_CSP(csp1))
#print(searcher1.search())  # get next solution
searcher2 = Depth_first_search(Search_from_CSP(csp2))
#print(searcher2.search())  # get next solution

