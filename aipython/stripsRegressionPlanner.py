# stripsRegressionPlanner.py - Regression Planner with STRIPS actions
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from searchProblem import Arc, Search_problem

class Subgoal(object):
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

class Regression_STRIPS(Search_problem):
    """A search problem where:
    * a node is a goal to be achieved, represented by a set of propositions.
    * the dynamics are specified by the STRIPS representation of actions
    """

    def __init__(self, planning_problem, heur=lambda s,g:0):
        """creates a regression seach space from a planning problem.
        heur(state,goal) is a heuristic function; 
           an underestimate of the cost from state to goal, where
           both state and goals are feature:value dictionaries
        """
        self.prob_domain = planning_problem.prob_domain
        self.top_goal = Subgoal(planning_problem.goal)
        self.initial_state = planning_problem.initial_state
        self.heur = heur

    def is_goal(self, subgoal):
        """if subgoal is true in the initial state, a path has been found"""
        goal_asst = subgoal.assignment
        return all((g in self.initial_state) and (self.initial_state[g]==goal_asst[g])
                   for g in goal_asst)

    def start_nodes(self):
        """the list of start nodes consists of the top-level goal"""
        return [self.top_goal]

    def neighbors(self,subgoal):
        """returns a list of the arcs for the neighbors of subgoal in this problem"""
        cost = 1
        goal_asst = subgoal.assignment
        return [ Arc(subgoal,self.weakest_precond(act,goal_asst),cost,act)
                 for act in self.prob_domain.actions
                 if self.possible(act,goal_asst)]

    def possible(self,act,goal_asst):
        """True if act is possible to achieve goal_asst.

        the action achieves an element of the effects and
        the action doesn't delete something that needs to be achieved and
        the precoditions are consistent with other subgoals that need to be achieved
        """
        effects = self.prob_domain.strips_map[act].effects
        preconds = self.prob_domain.strips_map[act].preconditions
        return ( any(goal_asst[prop]==effects[prop]
                    for prop in effects if prop in goal_asst) 
                and all(goal_asst[prop]==effects[prop]
                        for prop in effects if prop in goal_asst)
                and all(goal_asst[prop]==preconds[prop]
                        for prop in preconds if prop not in effects and prop in goal_asst)
                )

    def weakest_precond(self,act,goal_asst):
        """returns the subgoal that must be true so goal_asst holds after act"""
        new_asst = self.prob_domain.strips_map[act].preconditions.copy()
        for g in goal_asst:
            if g not in self.prob_domain.strips_map[act].effects:
                new_asst[g] = goal_asst[g]
        return Subgoal(new_asst)

    def heuristic(self,subgoal):
        """in the regression planner a node is a subgoal.
        the heuristic is an (under)estimate of the cost of going from the initial state to subgoal.
        """
        return self.heur(self.initial_state, subgoal.assignment)

from searchBranchAndBound import DF_branch_and_bound
from searchAStar import Searcher
from searchMPP import SearcherMPP 
from stripsProblem import problem0, problem1, problem2 

# Searcher(Regression_STRIPS(problem0)).search()  #A*
# SearcherMPP(Regression_STRIPS(problem0)).search()   #A* with MPP
# DF_branch_and_bound(Regression_STRIPS(problem0),10).search() #B&B

