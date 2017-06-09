# mdpExamples.py - MDP Examples
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from mdpProblem import MDP
#### Partying Decision Example ####

# States: Healthy Sick
# Actions: Relax Party

# trans[s][a][s'] gives P(s'|a,s)
#           Relax        Party
trans2 = (((0.95,0.05), (0.7, 0.3)),   # Healthy
          ((0.5,0.5),   (0.1, 0.9))    # Sick
        )

# reward[s][a] gives the expected reward of doing a in state s.
reward2 = ((7,10),(0,2))

healthy2 = MDP(['Healthy','Sick'], ['Relax','Party'], trans2, reward2, discount=0.8) 

## Tiny Game from Example 11.7 and Figure 11.8 of Poole and Mackworth, 2010 #

# actions        up                right          upC             left
transt = (((0.1,0.1,0.8,0,0,0), (0,1,0,0,0,0), (0,0,1,0,0,0), (1,0,0,0,0,0)), #s0
         ((0.1,0.1,0,0.8,0,0), (0,1,0,0,0,0), (0,0,0,1,0,0), (1,0,0,0,0,0)),  #s1
         ((0,0,0.1,0.1,0.8,0), (0,0,0,1,0,0), (0,0,0,0,1,0), (0,0,1,0,0,0)),  #s2
         ((0,0,0.1,0.1,0,0.8), (0,0,0,1,0,0), (0,0,0,0,0,1), (0,0,1,0,0,0)),  #s3
         ((0.1,0,0,0,0.8,0.1), (0,0,0,0,0,1), (0,0,0,0,1,0), (1,0,0,0,0,0)),  #s4
         ((0,0,0,0,0.1,0.9),   (0,0,0,0,0,1), (0,0,0,0,0,1), (0,0,0,0,1,0)) ) #s5

# actions     up  rt  upC  left
rewardt = ((-0.1,  0,  -1,   -1),   #s0
           (-0.1, -1,  -2,    0),   #s1
           (-10,   0,  -1, -100),   #s2
           (-0.1, -1,  -1,    0),   #s3
           (-1,    0,  -2,   10),   #s4
           (-1,   -1,  -2,    0))   #s5

mdpt = MDP(['s0','s1','s2','s3','s4','s5'],   # states
           ['up', 'right', 'upC', 'left'],    # actions
           transt, rewardt, discount=0.9)

def trace(mdp,numiter):
    print("Q values are shown as",[[st+"_"+ac for ac in mdp.actions] for st in mdp.states])
    print("One step lookahead Q-values:")
    print(mdp.q(mdp.v0))
    print("Values are for the states:", mdp.states)
    print("One step lookahead values:")
    print(mdp.vi(mdp.v0,1))
    print("Two step lookahead Q-values:")
    print(mdp.q(mdp.vi(mdp.v0,1)))
    print("Two step lookahead values:")
    print(mdp.vi(mdp.v0,2))
    vfin = mdp.vi(mdp.v0,numiter)
    print("After",numiter,"iterations, values:")
    print(vfin)
    print("After",numiter,"iterations, Q-values:")
    print(mdp.q(vfin))
    print("After",numiter,"iterations, Policy:", 
           [st+"->"+mdp.actions[act] for (st,act) in zip(mdp.states ,mdp.policy(vfin))])

# Try the following:
# trace(healthy2,10)

