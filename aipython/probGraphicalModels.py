# probGraphicalModels.py - Graphical Models and Belief Networks
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

class Graphical_model(object):
    """The class of graphical models. 
    A graphical model consists of a set of variables and a set of factors.

    List vars is a list of variables
    List factors is a list of factors
    """
    def __init__(self,vars=None,factors=None):
        self.variables = vars
        self.factors = factors

class Belief_network(Graphical_model):
    """The class of belief networks."""

    def __init__(self,vars=None,factors=None):
        """vars is a list of variables
        factors is a list of factors. Here we assume that all of the factors are instances of Prob.
        """
        Graphical_model.__init__(self,vars,factors)
        assert all(isinstance(f,Prob) for f in factors) if factors else True

from utilities import Displayable

class Inference_method(Displayable):
    """The abstract class of graphical model inference methods"""
    def query(self,qvar,obs={}):
        raise NotImplementedError("Inference_method query")   # abstract method

from probVariables import Variable
from probFactors import Prob

boolean = [False, True]
A = Variable("A", boolean)
B = Variable("B", boolean)
C = Variable("C", boolean)

f_a = Prob(A,[],[0.4,0.6])
f_b = Prob(B,[A],[0.9,0.1,0.2,0.8])
f_c = Prob(C,[B],[0.5,0.5,0.3,0.7])

bn1 = Belief_network([A,B,C],[f_a,f_b,f_c])

# Bayesian network report of leaving example from 
# Poole and Mackworth, Artificial Intelligence, 2010 http://artint.info
# This is Example 6.10 (page 236) shown in Figure 6.1

Al = Variable("Alarm", boolean)
Fi = Variable("Fire", boolean)
Le = Variable("Leaving", boolean)
Re = Variable("Report", boolean)
Sm = Variable("Smoke", boolean)
Ta = Variable("Tamper", boolean)

f_ta = Prob(Ta,[],[0.98,0.02])
f_fi = Prob(Fi,[],[0.99,0.01])
f_sm = Prob(Sm,[Fi],[0.99,0.01,0.1,0.9])
f_al = Prob(Al,[Fi,Ta],[0.9999, 0.0001, 0.15, 0.85, 0.01, 0.99, 0.5, 0.5])
f_lv = Prob(Le,[Al],[0.999, 0.001, 0.12, 0.88])
f_re = Prob(Re,[Le],[0.99, 0.01, 0.25, 0.75])

bn2 = Belief_network([Al,Fi,Le,Re,Sm,Ta],[f_ta,f_fi,f_sm,f_al,f_lv,f_re])


Season = Variable("Season",["summer","winter"])
Sprinkler = Variable("Sprinkler",["on","off"])
Rained = Variable("Rained",boolean)
Grass_wet = Variable("Grass wet",boolean)
Grass_shiny = Variable("Grass shiny",boolean)
Shoes_wet = Variable("Shoes wet",boolean)

f_season = Prob(Season,[],[0.5,0.5])
f_sprinkler = Prob(Sprinkler,[Season],[0.9,0.1,0.05,0.95])
f_rained = Prob(Rained,[Season],[0.7,0.3,0.2,0.8])
f_wet = Prob(Grass_wet,[Sprinkler,Rained], [1,0,0.1,0.9,0.2,0.8,0.02,0.98])
f_shiny = Prob(Grass_shiny, [Grass_wet], [0.95,0.05,0.3,0.7])
f_shoes = Prob(Shoes_wet, [Grass_wet], [0.92,0.08,0.35,0.65])

bn3 = Belief_network([Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet],
               [f_season, f_sprinkler, f_rained, f_wet, f_shiny, f_shoes])
