# stripsHeuristic.py - Planner with Heursitic Function
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

def heuristic_fun(state,goal):
    """An (under)estimate of the cost of solving goal from state.
    Both state and goal are variable:value dictionaries.
    This heuristic is the maximum of
    - the distance to the goal location, if there is one
    - the distance to the coffee shop if the goal has SWC=False, node has SWC=True and RHC=False
    """
    return max(h1(state,goal),
               h2(state,goal))

def h1(state,goal):
    """ the distance to the goal location, if there is one"""
    if 'RLoc' in goal:
        return dist(state['RLoc'], goal['RLoc'])
    else:
        return 0

def h2(state,goal):
    """ the distance to the coffee shop plus getting coffee and delivering it
    if the goal has SWC=False, node has SWC=True and RHC=False
    """
    if 'SWC' in goal and goal['SWC']==False and state['SWC']==True and state['RHC']==False:
        return dist(state['RLoc'],'cs')+3
    else:
        return 0
        
def dist(loc1, loc2):
    """returns the distance from location loc1 to loc2
    """
    if loc1==loc2:
        return 0
    if {loc1,loc2} in [{'cs','lab'},{'mr','off'}]:
        return 2
    else:
        return 1

#####  Forward Planner #####
from searchAStar import Searcher
from searchMPP import SearcherMPP
from stripsForwardPlanner import Forward_STRIPS
from stripsProblem import problem0, problem1, problem2
thisproblem = problem1

print("\n***** FORWARD NO HEURISTIC")
print(SearcherMPP(Forward_STRIPS(thisproblem)).search())

print("\n***** FORWARD WITH HEURISTIC")
print(SearcherMPP(Forward_STRIPS(thisproblem,heuristic_fun)).search()) 

#####  Regression Planner
from stripsRegressionPlanner import Regression_STRIPS

print("\n***** REGRESSION NO HEURISTIC")
print(SearcherMPP(Regression_STRIPS(thisproblem)).search())

print("\n***** REGRESSION WITH HEURISTIC")
print(SearcherMPP(Regression_STRIPS(thisproblem,heuristic_fun)).search())

