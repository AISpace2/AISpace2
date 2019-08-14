# probGraphicalModels.py - Graphical Models and Belief Networks
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from .probFactors import Prob
from .probVariables import Variable
from .utilities import Displayable


class Graphical_model(object):
    """The class of graphical models.
    A graphical model consists of a set of variables and a set of factors.

    vars - a list of variables (name should be unique)
    factors - a list of factors
    positions - a dictionary that maps each variable's name into its (x,y)-position
    """

    def __init__(self, vars=None, factors=None, positions={}):
        self.variables = vars
        self.factors = factors
        self.positions = positions


class Belief_network(Graphical_model):
    """The class of belief networks."""

    def __init__(self, vars=None, factors=None, positions={}):
        """
        vars - a list of variables (name should be unique)
        factors - a list of factors
        positions - a dictionary that maps each variable's name into its (x,y)-position
        """
        Graphical_model.__init__(self, vars, factors, positions)

        assert all(isinstance(f, Prob) for f in factors) if factors else True


class Inference_method(Displayable):
    """The abstract class of graphical model inference methods"""

    def query(self, qvar, obs={}):
        raise NotImplementedError("Inference_method query")   # abstract method


bn_empty = Belief_network([], [])

boolean = [False, True]
A = Variable("A", boolean)
B = Variable("B", boolean)
C = Variable("C", boolean)

f_a = Prob(A, [], [0.4, 0.6])
f_b = Prob(B, [A], [0.9, 0.1, 0.2, 0.8])
f_c = Prob(C, [B], [0.5, 0.5, 0.3, 0.7])

bn1 = Belief_network([A, B, C], [f_a, f_b, f_c])

# Bayesian network report of leaving example from
# Poole and Mackworth, Artificial Intelligence, 2010 http://artint.info
# This is Example 6.10 (page 236) shown in Figure 6.1

Al = Variable("Alarm", boolean)
Fi = Variable("Fire", boolean)
Le = Variable("Leaving", boolean)
Re = Variable("Report", boolean)
Sm = Variable("Smoke", boolean)
Ta = Variable("Tamper", boolean)

f_ta = Prob(Ta, [], [0.98, 0.02])
f_fi = Prob(Fi, [], [0.99, 0.01])
f_sm = Prob(Sm, [Fi], [0.99, 0.01, 0.1, 0.9])
f_al = Prob(Al, [Fi, Ta], [0.9999, 0.0001, 0.15, 0.85, 0.01, 0.99, 0.5, 0.5])
f_lv = Prob(Le, [Al], [0.999, 0.001, 0.12, 0.88])
f_re = Prob(Re, [Le], [0.99, 0.01, 0.25, 0.75])

bn2 = Belief_network([Al, Fi, Le, Re, Sm, Ta], [f_ta, f_fi, f_sm, f_al, f_lv, f_re])

Season = Variable("Season", ["summer", "winter"])
Sprinkler = Variable("Sprinkler", ["on", "off"])
Rained = Variable("Rained", boolean)
Grass_wet = Variable("Grass wet", boolean)
Grass_shiny = Variable("Grass shiny", boolean)
Shoes_wet = Variable("Shoes wet", boolean)

f_season = Prob(Season, [], [0.5, 0.5])
f_sprinkler = Prob(Sprinkler, [Season], [0.9, 0.1, 0.05, 0.95])
f_rained = Prob(Rained, [Season], [0.7, 0.3, 0.2, 0.8])
f_wet = Prob(Grass_wet, [Sprinkler, Rained], [1, 0, 0.1, 0.9, 0.2, 0.8, 0.02, 0.98])
f_shiny = Prob(Grass_shiny, [Grass_wet], [0.95, 0.05, 0.3, 0.7])
f_shoes = Prob(Shoes_wet, [Grass_wet], [0.92, 0.08, 0.35, 0.65])

bn3 = Belief_network([Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet], [f_season, f_sprinkler, f_rained, f_wet, f_shiny, f_shoes])

# An example with domain length > 2

C100 = Variable("C100", ["c103", "c110", "c121"])
M200 = Variable("M200", ["m200", "m221"])
C200 = Variable("C200", ["c210", "c221"])
C300 = Variable("C300", ["c310", "c313", "c314", "c320"])

f_c100 = Prob(C100, [], [0.2, 0.4, 0.4])
f_m200 = Prob(M200, [], [0.5, 0.5])
f_c200 = Prob(C200, [C100], [0.5, 0.5, 0.8, 0.2, 0.2, 0.8])
f_c300 = Prob(C300, [C200, M200], [0.25, 0.25, 0.25, 0.25, 0.30, 0.30, 0.10, 0.30, 0.20, 0.20, 0.40, 0.20, 0.10, 0.10, 0.70, 0.10])

bn4 = Belief_network([C100, M200, C200, C300], [f_c100, f_m200, f_c200, f_c300])

report = Variable('report', ['T', 'F'])
tampering = Variable('tampering', ['T', 'F'])
alarm = Variable('alarm', ['T', 'F'])
fire = Variable('fire', ['T', 'F'])
smoke = Variable('smoke', ['T', 'F'])
leaving = Variable('leaving', ['T', 'F']) 
f_report = Prob(report,[leaving],[0.75,0.25,0.01,0.99])
f_tampering = Prob(tampering,[],[0.02,0.98])
f_alarm = Prob(alarm,[tampering,fire],[0.5,0.5,0.85,0.15,0.99,0.01,0.0,1.0])
f_fire = Prob(fire,[],[0.01,0.99])
f_smoke = Prob(smoke,[fire],[0.9,0.1,0.01,0.99])
f_leaving = Prob(leaving,[alarm],[0.88,0.12,0.0,1.0])
Fire_Alarm_Belief_Network = Belief_network(
    vars=[report,tampering,alarm,fire,smoke,leaving],
    factors=[f_report,f_tampering,f_alarm,f_fire,f_smoke,f_leaving],
    positions=[])
