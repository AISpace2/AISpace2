# rlQLearner.py - Q Learning
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import random
from utilities import Displayable, argmax, flip

class RL_agent(Displayable):
    """An RL_Agent 
    has percepts (s, r) for some state s and real reward r
    """

class Q_learner(RL_agent):
    """A Q-learning agent has
    belief-state consisting of
        state is the previous state
        q is a {(state,action):value} dict
        visits is a {(state,action):n} dict.  n is how many times action was done in state
        acc_rewards is the accumulated reward

    it observes (s, r) for some world-state s and real reward r
    """

    def __init__(self, env, discount, explore=0.1, fixed_alpha=True, alpha=0.2,
                 alpha_fun=lambda k:1/k,
                 qinit=0, label="Q_learner"):
        """env is the environment to interact with.
        discount is the discount factor
        explore is the proportion of time the agent will explore
        fixed_alpha specifies whether alpha is fixed or varies with the number of visits
        alpha is the weight of new experiences compared to old experiences
        alpha_fun is a function that computes alpha from the number of visits
        qinit is the initial value of the Q's
        label is the label for plotting
        """
        RL_agent.__init__(self)
        self.env = env
        self.actions = env.actions
        self.discount = discount
        self.explore = explore
        self.fixed_alpha = fixed_alpha
        self.alpha = alpha
        self.alpha_fun = alpha_fun
        self.qinit = qinit
        self.label = label
        self.restart()

    def restart(self):
        """make the agent relearn, and reset the accumulated rewards
        """
        self.acc_rewards = 0
        self.state = self.env.state
        self.q = {}
        self.visits = {}

    def do(self,num_steps=100):
        """do num_steps of interaction with the environment"""
        self.display(2,"s\ta\tr\ts'\tQ")
        alpha = self.alpha
        for i in range(num_steps):
            action = self.select_action(self.state)
            next_state,reward = self.env.do(action)
            if not self.fixed_alpha:
                k = self.visits[(self.state, action)] = self.visits.get((self.state, action),0)+1
                alpha = self.alpha_fun(k)
            self.q[(self.state, action)] = (
                (1-alpha) * self.q.get((self.state, action),self.qinit)
                + alpha * (reward + self.discount
                                    * max(self.q.get((next_state, next_act),self.qinit)
                                          for next_act in self.actions)))
            self.display(2,self.state, action, reward, next_state, 
                         self.q[(self.state, action)], sep='\t')
            self.state = next_state
            self.acc_rewards += reward

    def select_action(self, state):
        """returns an action to carry out for the current agent
        given the state, and the q-function
        """
        if flip(self.explore):
            return random.choice(self.actions)
        else:
            return argmax((next_act, self.q.get((state, next_act),self.qinit))
                                  for next_act in self.actions)

