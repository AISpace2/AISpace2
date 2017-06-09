# mdpProblem.py - Representations for Markov Decision Processes
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from utilities import argmax

class MDP(object):
    def __init__(self, states, actions, trans, reward, discount):
        """states is a list or tuple of states.
        actions is a list or tuple of actions
        trans[s][a][s'] represents P(s'|a,s)
        reward[s][a] gives the expected reward of doing a in state s
        discount is a real in the range [0,1]
        """
        self.states = states
        self.actions = actions
        self.trans = trans
        self.reward = reward
        self.discount = discount
        self.v0 = [0 for s in states]  # initial value function
        
    def vi1(self,v):
         """carry out one iteration of value iteration and 
         returns a value function (a list of a value for each state).
         v is the previous value function.
         """
         return [max([self.reward[s][a]+self.discount*product(self.trans[s][a],v)
                      for a in range(len(self.actions))])
                 for s in range(len(self.states))]

    def vi(self,v0,n):
        """carries out n iterations of value iteration starting with value v0.

        Returns a value function
        """
        val = self.v0
        for i in range(n):
           val= self.vi1(val)
        return val

    def policy(self,v): 
         """returns an optimal policy assuming the next value function is v
            v is a list of values for each state
            returns a list of the indexes of optimal actions for each state
         """
         return [argmax(enumerate([self.reward[s][a]+self.discount*product(self.trans[s][a],v)
                                   for a in range(len(self.actions))]))
                 for s in range(len(self.states))]

    def q(self,v): 
        """returns the one-step-lookahead q-value assuming the next value function is v
        v is a list of values for each state
        returns a list of q values for each state. so that q[s][a] represents Q(s,a)
        """
        return [[self.reward[s][a]+self.discount*product(self.trans[s][a],v)
                  for a in range(len(self.actions))]
                 for s in range(len(self.states))]
    
def product(l1,l2):
    """returns the dot product of l1 and l2"""
    return sum([i1*i2 for (i1,i2) in zip(l1,l2)])

