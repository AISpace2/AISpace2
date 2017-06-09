# rlPlot.py - RL Plotter
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import matplotlib.pyplot as plt

def plot_rl(ag, label=None, yplot='Total', step_size=None, 
            steps_explore=1000, steps_exploit=1000, xscale='linear'):
    """
    plots the agent ag
    label is the label for the plot
    yplot is 'Average' or 'Total'
    step_size is the number of steps between each point plotted
    steps_explore is the number of steps the agent spends exploring
    steps_exploit is the number of steps the agent spends exploiting
    xscale is 'log' or 'linear'

    returns total reward when exploring, total reward when exploiting
    """
    assert yplot in ['Average','Total']
    if step_size is None:
        step_size = max(1,(steps_explore+steps_exploit)//500)
    if label is None:
        label = ag.label
    ag.max_display_level,old_mdl =  1,ag.max_display_level
    plt.ion()
    plt.xscale(xscale)
    plt.xlabel("step")
    plt.ylabel(yplot+" reward")
    steps = []         # steps
    rewards = []       # return
    ag.restart()
    step = 0
    while step < steps_explore:
        ag.do(step_size)
        step += step_size
        steps.append(step)
        if yplot == "Average":
            rewards.append(ag.acc_rewards/step)
        else:
            rewards.append(ag.acc_rewards)
    acc_rewards_exploring = ag.acc_rewards
    ag.explore,explore_save = 0,ag.explore
    while step < steps_explore+steps_exploit:
        ag.do(step_size)
        step += step_size
        steps.append(step)
        if yplot == "Average":
            rewards.append(ag.acc_rewards/step)
        else:
            rewards.append(ag.acc_rewards)
    plt.plot(steps,rewards,label=label)
    plt.legend(loc="upper left")
    plt.draw()
    ag.max_display_level = old_mdl 
    ag.explore=explore_save 
    return acc_rewards_exploring, ag.acc_rewards-acc_rewards_exploring

