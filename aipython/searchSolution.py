# searchSolution.py - solution to Assignment 1
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from searchAStar import Searcher
from searchProblem import Path

class Searcher_prunes(Searcher):
    def __init__(self,problem,pruning=None,method='astar',max_expanded=10000):
        """max_expanded is a bound on the number of paths expanded (to prevent infinite computation)"""
        self.method = method
        self.max_expanded = max_expanded
        self.pruning = pruning
        Searcher.__init__(self,problem,method)
        if self.pruning == 'mpp':
            self.explored = set()

    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost"""
        if self.method=="astar":
            value = path.cost+self.problem.heuristic(path.end())
        if self.method=="best":
            value = self.problem.heuristic(path.end())
        if self.method=="least-cost":
            value = path.cost        
        self.frontier.add(path,value)

        
    def search(self):
        """returns next path from an element of problem's start nodes
        to a goal node. 
        Returns None if no path exists.
        """
        if self.pruning == 'mpp':
            while not self.frontier.empty():
                path = self.frontier.pop()
                if path.end() not in self.explored:
                    self.display(2, "Expanding: ",path,"(cost:",path.cost,")")
                    self.explored.add(path.end())
                    self.num_expanded += 1
                    if self.problem.is_goal(path.end()):
                        self.display(1, self.num_expanded, "paths have been expanded and",
                            len(self.frontier.frontierpq), "paths remain in the frontier")
                        return path
                    else:
                        neighs = self.problem.neighbors(path.end())
                        for arc in neighs:
                            self.add_to_frontier(Path(path,arc))
                        self.display(3,"Frontier:",self.frontier)
        elif self.pruning == 'cycle':
            while not self.frontier.empty():
                path = self.frontier.pop()
                if path.end() not in path.initial_nodes():  # new part for cycle pruning
                    self.display(2, "Expanding: ",path,"(cost:",path.cost,")")
                    self.num_expanded += 1
                    if self.problem.is_goal(path.end()):
                        self.display(1, self.num_expanded, "paths have been expanded and",
                            len(self.frontier.frontierpq), "paths remain in the frontier")
                        return path
                    else:
                        neighs = self.problem.neighbors(path.end())
                        for arc in neighs:
                            self.add_to_frontier(Path(path,arc))
                        self.display(3,"Frontier:",self.frontier)

        else:  # no pruning
            while not self.frontier.empty() and self.num_expanded < self.max_expanded:
                path = self.frontier.pop()
                self.display(2, "Expanding: ",path,"(cost:",path.cost,")")
                self.num_expanded += 1
                if self.problem.is_goal(path.end()):
                    self.display(1, self.num_expanded, "paths have been expanded and",
                            len(self.frontier.frontierpq), "paths remain in the frontier")
                    return path
                else:
                    neighs = self.problem.neighbors(path.end())
                    for arc in neighs:
                        self.add_to_frontier(Path(path,arc))
                    self.display(3,"Frontier:",self.frontier)
            
        self.display(1,"Total of", self.frontier.frontier_index,"paths expanded.")

import searchProblem

def show_combinations(problem,name):
    print('\n******',name)
    for pruning in [None,'cycle','mpp']:
        for method in ['astar','best','least-cost']:
            s = Searcher_prunes(problem, pruning=pruning,method=method)
            s.max_display_level=0
            path = s.search()
            if path:
                print(method,"with",pruning,"expanded",s.num_expanded,"paths")
            else:
                print(method,"with",pruning,"did not find a solution with",s.num_expanded,"paths expanded")

if __name__ == "__main__":
    show_combinations(searchProblem.cyclic_delivery_problem,"Cyclic Delivery Problem")

