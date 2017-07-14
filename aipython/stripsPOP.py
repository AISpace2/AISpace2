# stripsPOP.py - Partial-order Planner using STRIPS representation
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from searchProblem import Arc, Search_problem
import random

class Action_instance(object):
    next_index = 0
    def __init__(self,action,index=None):
        if index is None:
            index = Action_instance.next_index
            Action_instance.next_index += 1
        self.action = action
        self.index = index

    def __str__(self):
        return str(self.action)+"#"+str(self.index)

    __repr__ = __str__  # __repr__ function is the same as the __str__ function

class POP_node(object):
    """a (partial) partial-order plan. This is a node in the search space."""
    def __init__(self, actions, constraints, agenda, causal_links):
        """
        * actions is a set of action instances
        * constraints a set of (a0,a1) pairs, representing a0<a1,
          closed under transitivity
        * agenda list of (subgoal,action) pairs to be achieved, where
          subgoal is a (variable,value) pair
        * causal_links is a set of (a0,g,a1) triples,
          where ai are action instances, and g is a (variable,value) pair
        """
        self.actions = actions  # a set of action instances
        self.constraints = constraints  # a set of (a0,a1) pairs
        self.agenda = agenda    # list of (subgoal,action) pairs to be achieved
        self.causal_links = causal_links # set of (a0,g,a1) triples

    def __str__(self):
        return ("actions: "+str({str(a) for a in self.actions})+
                "\nconstraints: "+
                str({(str(a1),str(a2)) for (a1,a2) in self.constraints})+
                "\nagenda: "+
                str([(str(s),str(a)) for (s,a) in self.agenda])+
                "\ncausal_links:"+
                str({(str(a0),str(g),str(a2)) for (a0,g,a2) in self.causal_links})  )

    def extract_plan(self):
        """returns a total ordering of the action instances consistent
        with the constraints.
        raises IndexError if there is no choice.
        """
        sorted_acts = []
        other_acts = set(self.actions)
        while other_acts:
            a = random.choice([a for a in other_acts if
                     all(((a1,a) not in self.constraints) for a1 in other_acts)])
            sorted_acts.append(a)
            other_acts.remove(a) 
        return sorted_acts
                 
from utilities import Displayable

class POP_search_from_STRIPS(Search_problem, Displayable):
    def __init__(self,planning_problem):
        Search_problem.__init__(self)
        self.planning_problem = planning_problem
        self.start = Action_instance("start")
        self.finish = Action_instance("finish")

    def is_goal(self, node):
        return node.agenda == []
    
    def start_nodes(self):
        constraints = {(self.start, self.finish)}
        agenda = [(g, self.finish) for g in self.planning_problem.goal.items()]
        return [POP_node([self.start,self.finish], constraints, agenda, [] )]

    def neighbors(self, node):
        """enumerates the neighbors of node"""
        self.display(3,"finding neighbors of\n",node)
        if node.agenda:
            subgoal,act1 = node.agenda[0]
            self.display(2,"selecting",subgoal,"for",act1)
            new_agenda = node.agenda[1:]
            for act0 in node.actions:
                if (self.achieves(act0, subgoal) and 
                   self.possible((act0,act1),node.constraints)):
                    self.display(2,"  reusing",act0)
                    consts1 = self.add_constraint((act0,act1),node.constraints)
                    new_clink = (act0,subgoal,act1)
                    new_cls = node.causal_links + [new_clink]
                    for consts2 in self.protect_cl_for_actions(node.actions,consts1,new_clink):
                        yield Arc(node, 
                                  POP_node(node.actions,consts2,new_agenda,new_cls), 
                                  cost=0)
            for a0 in self.planning_problem.prob_domain.strips_map:  #a0 is an action
                if self.achieves(a0, subgoal):
                    #a0 acheieves subgoal
                    new_a = Action_instance(a0)
                    self.display(2,"  using new action",new_a)
                    new_actions = node.actions + [new_a]
                    consts1 = self.add_constraint((self.start,new_a),node.constraints)
                    consts2 = self.add_constraint((new_a,act1),consts1)
                    preconds = self.planning_problem.prob_domain.strips_map[a0].preconditions
                    new_agenda = new_agenda + [(pre,new_a) for pre in preconds.items()]
                    new_clink = (new_a,subgoal,act1)
                    new_cls = node.causal_links + [new_clink]
                    for consts3 in self.protect_all_cls(node.causal_links,new_a,consts2):
                        for consts4 in self.protect_cl_for_actions(node.actions,consts3,new_clink):
                            yield Arc(node,
                                      POP_node(new_actions,consts4,new_agenda,new_cls),
                                      cost=1)

    def protect_cl_for_actions(self, actions, constrs, clink):
        """yields constriants that extend constrs and
        protect causal link (a0, subgoal, a1)
        for each action in actions
        """
        if actions:
            a = actions[0]
            rem_actions = actions[1:]
            a0, subgoal, a1 = clink
            if a != a0 and a != a1 and self.deletes(a,subgoal):
                if self.possible((a,a0),constrs):
                    new_const = self.add_constraint((a,a0),constrs)
                    for e in self.protect_cl_for_actions(rem_actions,new_const,clink): yield e  # could be "yield from"
                if self.possible((a1,a),constrs):
                    new_const = self.add_constraint((a1,a),constrs)
                    for e in self.protect_cl_for_actions(rem_actions,new_const,clink): yield e
            else:
                for e in self.protect_cl_for_actions(rem_actions,constrs,clink): yield e
        else:
            yield constrs
               
    def protect_all_cls(self, clinks, act, constrs):
        """yields constraints that protect all causal links from act"""
        if clinks:
            (a0,cond,a1) = clinks[0]  # select a causal link
            rem_clinks = clinks[1:]   # remaining causal links
            if act != a0 and act != a1 and self.deletes(act,cond):
                if self.possible((act,a0),constrs):
                    new_const = self.add_constraint((act,a0),constrs)
                    for e in self.protect_all_cls(rem_clinks,act,new_const): yield e
                if self.possible((a1,act),constrs):
                    new_const = self.add_constraint((a1,act),constrs)
                    for e in self.protect_all_cls(rem_clinks,act,new_const): yield e
            else:
                for e in self.protect_all_cls(rem_clinks,act,constrs): yield e
        else:
            yield constrs

    def achieves(self,action,subgoal):
        var,val = subgoal
        return var in self.effects(action) and self.effects(action)[var] == val

    def deletes(self,action,subgoal):
        var,val = subgoal
        return var in self.effects(action) and self.effects(action)[var] != val
    
    def effects(self,action):
        """returns the variable:value dictionary of the effects of action.
        works for both actions and action instances"""
        if isinstance(action, Action_instance):
            action = action.action
        if action == "start":
            return self.planning_problem.initial_state
        elif action == "finish":
            return {}
        else:
            return self.planning_problem.prob_domain.strips_map[action].effects
        
    def add_constraint(self, pair, const):
        if pair in const:
            return const
        todo = [pair]
        newconst = const.copy()
        while todo:
            x0,x1 = todo.pop()
            newconst.add((x0,x1))
            for x,y in newconst:
                if x==x1 and (x0,y) not in newconst:
                    todo.append((x0,y))
                if y==x0 and (x,x1) not in newconst:
                    todo.append((x,x1))
        return newconst

    def possible(self,pair,constraint):
        (x,y) = pair
        return (y,x) not in constraint

from searchBranchAndBound import DF_branch_and_bound
from searchAStar import Searcher
from searchMPP import SearcherMPP 
from stripsProblem import problem0, problem1, problem2 

rplanning0 = POP_search_from_STRIPS(problem0)
rplanning1 = POP_search_from_STRIPS(problem1)
rplanning2 = POP_search_from_STRIPS(problem2)
searcher0 = DF_branch_and_bound(rplanning0,5)
searcher0a = Searcher(rplanning0)
searcher1 = DF_branch_and_bound(rplanning1,10)
searcher1a = Searcher(rplanning1)
searcher2 = DF_branch_and_bound(rplanning2,10)
searcher2a = Searcher(rplanning2)
# Try one of the following searchers
# a = searcher0.search()
# a = searcher0a.search()
# a.end().extract_plan()  # print a plan found
# a.end().constraints     # print the constraints
# Searcher.max_display_level = 0  # less detailed display
# DF_branch_and_bound.max_display_level = 0  # less detailed display
# a = searcher1.search()
# a = searcher1a.search()
# a = searcher2.search()
# a = searcher2a.search()

