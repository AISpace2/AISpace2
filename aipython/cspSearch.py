# cspSearch.py - Representations of a Search Problem from a CSP.
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from aipython.cspProblem import CSP, Constraint
from aipython.searchProblem import Arc, Search_problem
from aipython.utilities import dict_union

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
    
    def start_node(self):
        return {}
    
    def neighbors(self, node):
        """iterator over the neighboring nodes of node"""
        var = self.variables[len(node)] # the next variable
        res = []
        for val in self.csp.domains[var]:
            new_env = dict_union(node,{var:val})  #dictionary union
            if self.csp.consistent(new_env):
                res.append(Arc(node,new_env))
        return res

from aipython.cspExamples import simple_csp2,extended_csp,test
from aipython.searchGeneric import Searcher

def dfs_solver(csp):
    """depth-first search solver"""
    path = Searcher(Search_from_CSP(csp)).search()
    if path is not None:
        return path.end()
    else:
        return None

if __name__ == "__main__":
    test(dfs_solver)

## Test Solving CSPs with Search:
searcher1 = Searcher(Search_from_CSP(simple_csp2))
#print(searcher1.search())  # get next solution
searcher2 = Searcher(Search_from_CSP(extended_csp))
#print(searcher2.search())  # get next solution

