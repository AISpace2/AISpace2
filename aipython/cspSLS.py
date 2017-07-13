# cspSLS.py - Stochastic Local Search for Solving CSPs
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from cspProblem import CSP, Constraint
from searchProblem import Arc, Search_problem
from utilities import Displayable
import random
import heapq

class SLSearcher(Displayable):
    """A search problem directly from the CSP..

    A node is a variable:value dictionary"""
    def __init__(self, csp):
        self.csp = csp
        self.variables_to_select = {var for var in self.csp.variables 
                                    if len(self.csp.domains[var]) > 1}
        # Create assignment and conflicts set
        self.current_assignment = None # this will trigger a random restart
        self.number_of_steps = 1  #number of steps after the initialization

    def restart(self):
        """creates a new total assignment and the conflict set
        """
        self.current_assignment = {var:random_sample(dom) for 
                                   (var,dom) in self.csp.domains.items()}
        self.display(2,"Initial assignment",self.current_assignment)
        self.conflicts = set()
        for con in self.csp.constraints:
            if not con.holds(self.current_assignment):
                self.conflicts.add(con)
        self.display(2,"Number of conflicts",len(self.conflicts))
        self.variable_pq = None

    def search(self,max_steps, prob_best=1.0, prob_anycon=1.0):
        """
        returns the number of steps or None if these is no solution
        if there is a solution, it can be found in self.current_assignment
        """
        if self.current_assignment is None:
            self.restart()
            self.number_of_steps += 1
            if not self.conflicts:
                return self.number_of_steps
        if prob_best > 0:  # we need to maintain a variable priority queue
            return self.search_with_var_pq(max_steps, prob_best, prob_anycon)
        else:
            return self.search_with_any_conflict(max_steps, prob_anycon)

    def search_with_any_conflict(self, max_steps, prob_anycon=1.0):
        """Searches with the any_conflict heuristic.
        This relies on just maintaining the set of conflicts; 
        it does not maintain a priority queue
        """
        self.variable_pq = None   # we are not maintaining the priority queue.
                                  # This ensures it is regenerated if needed.
        for i in range(max_steps):
            self.number_of_steps +=1
            if  random.random() < prob_anycon:
                con = random_sample(self.conflicts)  # pick random conflict
                var = random_sample(con.scope)   # pick variable in conflict
            else:
                var = random_sample(self.variables_to_select)
            if len(self.csp.domains[var]) > 1:
                val = random_sample(self.csp.domains[var] -
                                    {self.current_assignment[var]})
                self.display(2,"Assigning",var,"=",val)
                self.current_assignment[var]=val
                for varcon in self.csp.var_to_const[var]:
                    if varcon.holds(self.current_assignment):
                        if varcon in self.conflicts:
                            self.conflicts.remove(varcon)
                    else:
                        if varcon not in self.conflicts:
                            self.conflicts.add(varcon)
                self.display(2,"Number of conflicts",len(self.conflicts))
            if not self.conflicts:
                self.display(1,"Solution found",self.current_assignment,
                                 "in", self.number_of_steps,"steps")
                return self.number_of_steps
        self.display(1,"No solution in",self.number_of_steps,"steps",
                    len(self.conflicts),"conflicts remain")
        return None

    def search_with_var_pq(self,max_steps, prob_best=1.0, prob_anycon=1.0):
        """search with a priority queue of variables.
        This is used to select a variable with the most conflicts.
        """
        if not self.variable_pq:
            self.create_pq()
        pick_best_or_con = prob_best + prob_anycon
        for i in range(max_steps):
            self.number_of_steps +=1
            randnum = random.random()
            ## Pick a variable
            if randnum < prob_best: # pick best variable
                var,oldval = self.variable_pq.top()
            elif randnum < pick_best_or_con:  # pick a variable in a conflict
                con = random_sample(self.conflicts)
                var = random_sample(con.scope)
            else:  #pick any variable that can be selected
                var = random_sample(self.variables_to_select)
            if len(self.csp.domains[var]) > 1:   # var has other values
                ## Pick a value
                val = random_sample(self.csp.domains[var] - 
                                    {self.current_assignment[var]})
                self.display(2,"Assigning",var,val)
                ## Update the priority queue
                var_differential = {}
                self.current_assignment[var]=val
                for varcon in self.csp.var_to_const[var]:
                    self.display(3,"Checking",varcon)
                    if varcon.holds(self.current_assignment):
                        if varcon in self.conflicts:  #was incons, now consis
                            self.display(3,"Became consistent",varcon)
                            self.conflicts.remove(varcon)
                            for v in varcon.scope: # v is in one fewer conflicts
                                var_differential[v] = var_differential.get(v,0)-1
                    else:
                        if varcon not in self.conflicts: # was consis, not now
                            self.display(3,"Became inconsistent",varcon)
                            self.conflicts.add(varcon)
                            for v in varcon.scope:  # v is in one more conflicts
                                var_differential[v] = var_differential.get(v,0)+1
                self.variable_pq.update_each_priority(var_differential)
                self.display(2,"Number of conflicts",len(self.conflicts))
            if not self.conflicts:  #no conflicts, so solution found
                self.display(1,"Solution found",self.current_assignment,"in",
                             self.number_of_steps,"steps")
                return self.number_of_steps
        self.display(1,"No solution in",self.number_of_steps,"steps",
                    len(self.conflicts),"conflicts remain")
        return None

    def create_pq(self):
        """Create the variable to number-of-conflicts priority queue.
        This is needed to select the variable in the most conflicts.
        
        The value of a variable in the priority queue is the negative of the
        number of conflicts the variable appears in.
        """
        self.variable_pq = Updatable_priority_queue()
        var_to_number_conflicts = {}
        for con in self.conflicts:
            for var in con.scope:
                var_to_number_conflicts[var] = var_to_number_conflicts.get(var,0)+1
        for var,num in var_to_number_conflicts.items():
            if num>0:
                self.variable_pq.add(var,-num)
        
def random_sample(st):
    """selects a random element from set st"""
    return random.sample(st,1)[0]

class Updatable_priority_queue(object):
    """A priority queue where the values can be updated.
    Elements with the same value are ordered randomly.
    
    This code is based on the ideas described in 
    http://docs.python.org/3.3/library/heapq.html
    It could probably be done more efficiently by
    shuffling the modified element in the heap.
    """
    def __init__(self):
        self.pq = []   # priority queue of [val,rand,elt] triples
        self.elt_map = {}  # map from elt to [val,rand,elt] triple in pq
        self.REMOVED = "*removed*"  # a string that won't be a legal element
        self.max_size=0

    def add(self,elt,val):
        """adds elt to the priority queue with priority=val.
        """
        assert val <= 0,val
        assert elt not in self.elt_map, elt
        new_triple = [val, random.random(),elt]
        heapq.heappush(self.pq, new_triple)
        self.elt_map[elt] = new_triple

    def remove(self,elt):
        """remove the element from the priority queue"""
        if elt in self.elt_map:
            self.elt_map[elt][2] = self.REMOVED
            del self.elt_map[elt]

    def update_each_priority(self,update_dict):
        """update values in the priority queue by subtracting the values in
        update_dict from the priority of those elements in priority queue.
        """
        for elt,incr in update_dict.items():
            if incr != 0:
                newval = self.elt_map.get(elt,[0])[0] - incr
                assert newval <= 0, str(elt)+":"+str(newval+incr)+"-"+str(incr)
                self.remove(elt)
                if newval != 0:
                    self.add(elt,newval)
                
    def pop(self):
        """Removes and returns the (elt,value) pair with minimal value.
        If the priority queue is empty, IndexError is raised.
        """
        self.max_size = max(self.max_size, len(self.pq))  # keep statistics
        triple = heapq.heappop(self.pq)
        while triple[2] == self.REMOVED:
            triple = heapq.heappop(self.pq)
        del self.elt_map[triple[2]]
        return triple[2], triple[0]  # elt, value

    def top(self):
        """Returns the (elt,value) pair with minimal value, without removing it.
        If the priority queue is empty, IndexError is raised.
        """
        self.max_size = max(self.max_size, len(self.pq))  # keep statistics
        triple = self.pq[0]
        while triple[2] == self.REMOVED:
            heapq.heappop(self.pq)
            triple = self.pq[0]
        return triple[2], triple[0]  # elt, value

    def empty(self):
        """returns True iff the priority queue is empty"""
        return all(triple[2] == self.REMOVED for triple in self.pq)

import matplotlib.pyplot as plt

class Runtime_distribution(object):
    def __init__(self, csp, xscale='log'):
        """Sets up plotting for csp
        xscale is either 'linear' or 'log'
        """
        self.csp = csp
        plt.ion()
        plt.xlabel("Number of Steps")
        plt.ylabel("Cumulative Number of Runs")
        plt.xscale(xscale)  # Makes a 'log' or 'linear' scale

    def plot_run(self,num_runs=100,max_steps=1000, prob_best=1.0, prob_anycon=1.0):
        stats = []
        SLSearcher.max_display_level, temp_mdl = 0, SLSearcher.max_display_level # no display
        for i in range(num_runs):
            searcher = SLSearcher(self.csp)
            num_steps = searcher.search(max_steps, prob_best, prob_anycon)
            if num_steps:
                stats.append(num_steps)
        stats.sort()
        if prob_best >= 1.0:
            label = "P(best)=1.0"
        else:
            p_ac =  min(prob_anycon, 1-prob_best)
            label = "P(best)=%.2f, P(ac)=%.2f" % (prob_best, p_ac)
        plt.plot(stats,range(len(stats)),label=label)
        plt.legend(loc="upper left")
        #plt.draw()
        SLSearcher.max_display_level= temp_mdl  #restore display

from cspExamples import test
def sls_solver(csp,prob_best=0.7):
    """stochastic local searcher"""
    se0 = SLSearcher(csp)
    se0.search(1000,prob_best)
    return se0.current_assignment
def any_conflict_solver(csp):
    """stochastic local searcher (any-conflict)"""
    return sls_solver(csp,0)

if __name__ == "__main__":
    test(sls_solver) 
    test(any_conflict_solver)
    
from cspExamples import csp1, csp2, crossword1

## Test Solving CSPs with Search:
#se1 = SLSearcher(csp1); print(se1.search(100))
#se2 = SLSearcher(csp2); print(se2.search(1000,1.0)) # greedy
#se2 = SLSearcher(csp2); print(se2.search(1000,0))  # any_conflict
#se2 = SLSearcher(csp2); print(se2.search(1000,0.7)) # 70% greedy; 30% any_conflict
#SLSearcher.max_display_level=2  #more detailed display
#se3 = SLSearcher(crossword1); print(se3.search(100),0.7)
#p = Runtime_distribution(csp2)
#p.plot_run(100,1000,0)
#p.plot_run(100,1000,1.0)
#p.plot_run(100,1000,0.7)

