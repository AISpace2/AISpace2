# rlProblem.py - Representations for Reinforcement Learning
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import random
from utilities import Displayable, flip

class RL_env(Displayable):
    def __init__(self,actions,state):
        self.actions = actions   # set of actions
        self.state = state       # initial state

    def do(self, action):
        """do action
        returns state,reward
        """
        raise NotImplementedError("RL_env.do")   # abstract method
        
class Healthy_env(RL_env):
    def __init__(self):
        RL_env.__init__(self,["party","relax"], "healthy")

    def do(self, action):
        """updates the state based on the agent doing action.
        returns state,reward
        """
        if self.state=="healthy":
            if action=="party":
                self.state = "healthy" if flip(0.7) else "sick"
                reward = 10
            else:  # action=="relax"
                self.state = "healthy" if flip(0.95) else "sick"
                reward = 7
        else:  # self.state=="sick"
            if action=="party":
                self.state = "healthy" if flip(0.1) else "sick"
                reward = 2
            else:
                self.state = "healthy" if flip(0.5) else "sick"
                reward = 0
        return self.state,reward

class Env_from_MDP(RL_env):
    def __init__(self, mdp):
        initial_state = mdp.states[0]
        RL_env.__init__(self,mdp.actions, initial_state)
        self.mdp = mdp
        self.action_index = {action:index for (index,action) in enumerate(mdp.actions)}
        self.state_index = {state:index for (index,state) in enumerate(mdp.states)}

    def do(self, action):
        """updates the state based on the agent doing action.
        returns state,reward
        """
        action_ind = self.action_index[action]
        state_ind = self.state_index[self.state]
        self.state = pick_from_dist(self.mdp.trans[state_ind][action_ind], self.mdp.states)
        reward = self.mdp.reward[state_ind][action_ind]
        return self.state, reward

def pick_from_dist(dist,values):
    """
    e.g. pick_from_dist([0.3,0.5,0.2],['a','b','c']) should pick 'a' with probability 0.3, etc.
    """
    ran = random.random()
    i=0
    while ran>dist[i]:
        ran -= dist[i]
        i += 1
    return values[i]

