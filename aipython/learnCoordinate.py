# learnCoordinate.py - Learning to Coordinate
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Learner

soccer =  [[(-0.6,0.6),(-0.3,0.3)],[(-0.2,0.2),(-0.9,0.9)]]]
football = [[(2,1),(0,0)],[(0,0),(1,2)]]
prisoners_game = [[(100,100),(0,1100)],[(1100,0),(1000,1000)]]]

class Policy_hill_climbing(Learner):
    def __init__(self,game)

