# rlQTest.py - RL Q Tester
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from rlProblem import Healthy_env
from rlQLearner import Q_learner
from rlPlot import plot_rl

env = Healthy_env()
ag = Q_learner(env, 0.7)
ag_opt = Q_learner(env, 0.7, qinit=100, label="optimistic" ) # optimistic agent
ag_exp_l = Q_learner(env, 0.7, explore=0.01, label="less explore")
ag_exp_m = Q_learner(env, 0.7, explore=0.5, label="more explore")
ag_disc = Q_learner(env, 0.9, qinit=100, label="disc 0.9")
ag_va = Q_learner(env, 0.7, qinit=100,fixed_alpha=False,alpha_fun=lambda k:10/(9+k),label="alpha=10/(9+k)")

# ag.max_display_level = 2
# ag.do(20)
# ag.q    # get the learned q-values
# ag.max_display_level = 1
# ag.do(1000)
# ag.q    # get the learned q-values
# plot_rl(ag,yplot="Average")
# plot_rl(ag_opt,yplot="Average")
# plot_rl(ag_exp_l,yplot="Average") 
# plot_rl(ag_exp_m,yplot="Average")
# plot_rl(ag_disc,yplot="Average")
# plot_rl(ag_va,yplot="Average")

from mdpExamples import mdpt
from rlProblem import Env_from_MDP
envt = Env_from_MDP(mdpt)
agt = Q_learner(envt, 0.8)
# agt.do(20)

from rlSimpleEnv import Simple_game_env
senv = Simple_game_env()
sag1 = Q_learner(senv,0.9,explore=0.2,fixed_alpha=True,alpha=0.1)
# plot_rl(sag1,steps_explore=100000,steps_exploit=100000,label="alpha="+str(sag1.alpha))
sag2 = Q_learner(senv,0.9,explore=0.2,fixed_alpha=False)
# plot_rl(sag2,steps_explore=100000,steps_exploit=100000,label="alpha=1/k")
sag3 = Q_learner(senv,0.9,explore=0.2,fixed_alpha=False,alpha_fun=lambda k:10/(9+k))
# plot_rl(sag3,steps_explore=100000,steps_exploit=100000,label="alpha=10/(9+k)")

