# rlSimpleEnv.py - Simple game
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import random
from utilities import flip
from rlProblem import RL_env

class Simple_game_env(RL_env):
    xdim = 5
    ydim = 5

    vwalls = [(0,3), (0,4), (1,4)]  # vertical walls right of these locations
    hwalls = [] # not implemented
    crashed_reward = -1
    
    prize_locs = [(0,0), (0,4), (4,0), (4,4)]
    prize_apears_prob = 0.3
    prize_reward = 10

    monster_locs = [(0,1), (1,1), (2,3), (3,1), (4,2)]
    monster_appears_prob = 0.4
    monster_reward_when_damaged = -10
    repair_stations = [(1,4)]

    actions = ["up","down","left","right"]
    
    def __init__(self):
        # State:
        self.x = 2
        self.y = 2
        self.damaged = False
        self.prize = None
        # Statistics
        self.number_steps = 0
        self.total_reward = 0
        self.min_reward = 0
        self.min_step = 0
        self.zero_crossing = 0
        RL_env.__init__(self, Simple_game_env.actions,
                        (self.x, self.y, self.damaged, self.prize))
        self.display(2,"","Step","Tot Rew","Ave Rew",sep="\t")

    def do(self,action):
        """updates the state based on the agent doing action.
        returns state,reward
        """
        reward = 0.0
        # A prize can appear:
        if self.prize is None and flip(self.prize_apears_prob):
                self.prize = random.choice(self.prize_locs)
        # Actions can be noisy
        if flip(0.4):
            actual_direction = random.choice(self.actions)
        else:
            actual_direction = action
        # Modeling the actions given the actual direction
        if actual_direction == "right":
            if self.x==self.xdim-1 or (self.x,self.y) in self.vwalls:
                reward += self.crashed_reward
            else:
                self.x += 1
        elif actual_direction == "left":
            if self.x==0 or (self.x-1,self.y) in self.vwalls:
                reward += self.crashed_reward
            else:
                self.x += -1
        elif actual_direction == "up":
            if self.y==self.ydim-1:
                reward += self.crashed_reward
            else:
                self.y += 1
        elif actual_direction == "down":
            if self.y==0:
                reward += self.crashed_reward
            else:
                self.y += -1
        else:
            raise RuntimeError("unknown_direction "+str(direction))

        # Monsters
        if (self.x,self.y) in self.monster_locs and flip(self.monster_appears_prob):
            if self.damaged:
                reward += self.monster_reward_when_damaged
            else:
                self.damaged = True
        if (self.x,self.y) in self.repair_stations:
            self.damaged = False

        # Prizes
        if (self.x,self.y) == self.prize:
            reward += self.prize_reward
            self.prize = None

        # Statistics
        self.number_steps += 1
        self.total_reward += reward
        if self.total_reward < self.min_reward:
            self.min_reward = self.total_reward
            self.min_step = self.number_steps
        if self.total_reward>0 and reward>self.total_reward:
            self.zero_crossing = self.number_steps
        self.display(2,"",self.number_steps,self.total_reward,
                      self.total_reward/self.number_steps,sep="\t")

        return (self.x, self.y, self.damaged, self.prize), reward
        
