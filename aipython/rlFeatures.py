# rlFeatures.py - Feature-based Reinforcement Learner
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

class SARSA_LFA_learner(RL_agent):
    """A SARSA_LFA learning agent has
    belief-state consisting of
        state is the previous state
        q is a {(state,action):value} dict
        visits is a {(state,action):n} dict.  n is how many times action was done in state
        acc_rewards is the accumulated reward

    it observes (s, r) for some world-state s and real reward r
    """
    def __init__(self, env, get_features, discount, explore=0.2, step_size=0.01,
                 winit=0, label="SARSA_LFA"):
        """env is the feature environment to interact with
        get_features is a function get_features(state,action) that returns the list of feature values
        discount is the discount factor
        explore is the proportion of time the agent will explore
        step_size is gradient descent step size
        winit is the initial value of the weights
        label is the label for plotting
        """
        RL_agent.__init__(self)
        self.env = env
        self.get_features = get_features
        self.actions = env.actions
        self.discount = discount
        self.explore = explore
        self.step_size = step_size
        self.winit = winit
        self.label = label
        self.restart()

    def restart(self):
        """make the agent relearn, and reset the accumulated rewards
        """
        self.acc_rewards = 0
        self.state = self.env.state
        self.features = self.get_features(self.state, list(self.env.actions)[0])
        self.weights = [self.winit for f in self.features]
        self.action = self.select_action(self.state)

    def do(self,num_steps=100):
        """do num_steps of interaction with the environment"""
        self.display(2,"s\ta\tr\ts'\tQ\tdelta")
        for i in range(num_steps):
            next_state,reward = self.env.do(self.action)
            self.acc_rewards += reward
            next_action = self.select_action(next_state)
            feature_values = self.get_features(self.state,self.action)
            oldQ = dot_product(self.weights, feature_values)
            nextQ = dot_product(self.weights, self.get_features(next_state,next_action))
            delta = reward + self.discount * nextQ - oldQ
            for i in range(len(self.weights)):
                self.weights[i] += self.step_size * delta * feature_values[i]
            self.display(2,self.state, self.action, reward, next_state,
                         dot_product(self.weights, feature_values), delta, sep='\t')
            self.state = next_state
            self.action = next_action

    def select_action(self, state):
        """returns an action to carry out for the current agent
        given the state, and the q-function.
        This implements an epsilon-greedy approach
        where self.explore is the probability of exploring.
        """
        if flip(self.explore):
            return random.choice(self.actions)
        else:
            return argmax((next_act, dot_product(self.weights,
                                                 self.get_features(state,next_act)))
                                  for next_act in self.actions)

    def show_actions(self,state=None):
        """prints the value for each action in a state.
        This may be useful for debugging.
        """
        if state is None:
            state = self.state
        for next_act in self.actions:
            print(next_act,dot_product(self.weights, self.get_features(state,next_act)))

def dot_product(l1,l2):
    return sum(e1*e2 for (e1,e2) in zip(l1,l2))


from rlQTest import senv    # simple game environment
from rlSimpleGameFeatures import get_features, simp_features
from rlPlot import plot_rl

fa1 = SARSA_LFA_learner(senv, get_features, 0.9, step_size=0.01)
#fa1.max_display_level = 2
#fa1.do(20)
#plot_rl(fa1,steps_explore=10000,steps_exploit=10000,label="SARSA_LFA(0.01)")
fas1 = SARSA_LFA_learner(senv, simp_features, 0.9, step_size=0.01)
#plot_rl(fas1,steps_explore=10000,steps_exploit=10000,label="SARSA_LFA(simp)")

