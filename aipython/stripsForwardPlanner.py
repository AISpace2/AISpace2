# stripsForwardPlanner.py - Forward Planner with STRIPS actions
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from searchProblem import Arc, Search_problem
from stripsProblem import Strips, STRIPS_domain

class State(object):
    def __init__(self,assignment):
        self.assignment = assignment
        self.hash_value = None
    def __hash__(self):
        if self.hash_value is None:
            self.hash_value = hash(frozenset(self.assignment.items()))
        return self.hash_value
    def __eq__(self,st):
        return self.assignment == st.assignment
    def __str__(self):
        return str(self.assignment)
        
def zero(*args,**nargs):
    """always returns 0"""
    return 0

class Forward_STRIPS(Search_problem):
    """A search problem from a planning problem where:
    * a node is a state object.
    * the dynamics are specified by the STRIPS representation of actions
    """
    def __init__(self, planning_problem, heur=zero):
        """creates a forward seach space from a planning problem.
        heur(state,goal) is a heuristic function,
           an underestimate of the cost from state to goal, where
           both state and goals are feature:value dictionaries.
        """
        self.prob_domain = planning_problem.prob_domain
        self.initial_state = State(planning_problem.initial_state)
        self.goal = planning_problem.goal
        self.heur = heur

    def is_goal(self, state):
        """is True if node is a goal.

        Every goal feature has the same value in the state and the goal."""
        state_asst = state.assignment
        return all(prop in state_asst and state_asst[prop]==self.goal[prop]
                   for prop in self.goal)

    def start_nodes(self):
        """returns list of start nodes"""
        return [self.initial_state]

    def neighbors(self,state):
        """returns neighbors of state in this problem"""
        cost=1
        state_asst = state.assignment
        return [ Arc(state,self.effect(act,state_asst),cost,act)
                 for act in self.prob_domain.actions
                 if self.possible(act,state_asst)]

    def possible(self,act,state_asst):
        """True if act is possible in state.
        act is possible if all of its preconditions have the same value in the state"""
        preconds = self.prob_domain.strips_map[act].preconditions
        return all(pre in state_asst and state_asst[pre]==preconds[pre]
                   for pre in preconds)

    def effect(self,act,state_asst):
        """returns the state that is the effect of doing act given state_asst"""
        new_state_asst = self.prob_domain.strips_map[act].effects.copy()
        for prop in state_asst:
            if prop not in new_state_asst:
                new_state_asst[prop]=state_asst[prop]
        return State(new_state_asst)

    def heuristic(self,state):
        """in the forward planner a node is a state.
        the heuristic is an (under)estimate of the cost
        of going from the state to the top-level goal.
        """
        return self.heur(state.assignment, self.goal)

from searchBranchAndBound import DF_branch_and_bound
from searchAStar import Searcher
from searchMPP import SearcherMPP
from stripsProblem import problem0, problem1, problem2, blocks1, blocks2, blocks3

# Searcher(Forward_STRIPS(problem1)).search()  #A*
# SearcherMPP(Forward_STRIPS(problem1)).search()  #A* with MPP
# DF_branch_and_bound(Forward_STRIPS(problem1),10).search() #B&B
# To find more than one plan:
# s1 =Searcher(Forward_STRIPS(problem1))  #A*
# s1.search()  #find another plan

