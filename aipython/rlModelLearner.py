# rlModelLearner.py - Model-based Reinforcement Learner
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import random
from rlQLearner import RL_agent
from utilities import Displayable, argmax, flip

class Model_based_reinforcement_learner(RL_agent):
    """A Model-based reinforcement learner
    """

    def __init__(self, env, discount, explore=0.1, qinit=0, 
                   updates_per_step=10, label="MBR_learner"):
        """env is the environment to interact with.
        discount is the discount factor
        explore is the proportion of time the agent will explore
        qinit is the initial value of the Q's
        updates_per_step is the number of AVI updates per action
        label is the label for plotting
        """
        RL_agent.__init__(self)
        self.env = env
        self.actions = env.actions
        self.discount = discount
        self.explore = explore
        self.qinit = qinit
        self.updates_per_step = updates_per_step
        self.label = label
        self.restart()

    def restart(self):
        """make the agent relearn, and reset the accumulated rewards
        """
        self.acc_rewards = 0
        self.state = self.env.state
        self.q = {}             # {(st,action):q_value} map
        self.r = {}             # {(st,action):reward} map
        self.t = {}             # {(st,action,st_next):count} map
        self.visits = {}        # {(st,action):count} map
        self.res_states = {}    # {(st,action):set_of_states}  map
        self.visits_list = []   # list of (st,action)
        self.previous_action = None

    def do(self,num_steps=100):
        """do num_steps of interaction with the environment
        for each action, do updates_per_step iterations of asynchronous value iteration
        """
        for step in range(num_steps):
            pst = self.state     # previous state
            action = self.select_action(pst)
            self.state,reward = self.env.do(action)
            self.acc_rewards += reward
            self.t[(pst,action,self.state)] = self.t.get((pst, action,self.state),0)+1
            if (pst,action) in self.visits:
                self.visits[(pst,action)] += 1
                self.r[(pst,action)] += (reward-self.r[(pst,action)])/self.visits[(pst,action)]
                self.res_states[(pst,action)].add(self.state)
            else:
                self.visits[(pst,action)] = 1
                self.r[(pst,action)] = reward
                self.res_states[(pst,action)] = {self.state}
                self.visits_list.append((pst,action))
            st,act = pst,action      #initial state-action pair for AVI
            for update in range(self.updates_per_step):
                self.q[(st,act)] = self.r[(st,act)]+self.discount*(
                    sum(self.t[st,act,rst]/self.visits[st,act]*
                        max(self.q.get((rst,nact),self.qinit) for nact in self.actions)
                        for rst in self.res_states[(st,act)]))
                st,act = random.choice(self.visits_list)
                
    def select_action(self, state):
        """returns an action to carry out for the current agent
        given the state, and the q-function
        """
        if flip(self.explore):
            return random.choice(self.actions)
        else:
            return argmax((next_act, self.q.get((state, next_act),self.qinit))
                                  for next_act in self.actions)

from rlQTest import senv    # simple game environment
mbl1 = Model_based_reinforcement_learner(senv,0.9,updates_per_step=10)
# plot_rl(mbl1,steps_explore=100000,steps_exploit=100000,label="model-based(10)")
mbl2 = Model_based_reinforcement_learner(senv,0.9,updates_per_step=1)
# plot_rl(mbl2,steps_explore=100000,steps_exploit=100000,label="model-based(1)")

