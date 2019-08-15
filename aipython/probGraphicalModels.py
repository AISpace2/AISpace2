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

Fever = Variable('Fever', ['T', 'F'])
Smokes = Variable('Smokes', ['T', 'F'])
Coughing = Variable('Coughing', ['T', 'F'])
Bronchitis = Variable('Bronchitis', ['T', 'F'])
Wheezing = Variable('Wheezing', ['T', 'F'])
Sore_Throat = Variable('Sore_Throat', ['T', 'F'])
Influenza = Variable('Influenza', ['T', 'F']) 
f_Fever = Prob(Fever,[Influenza],[0.9,0.1,0.05,0.95])
f_Smokes = Prob(Smokes,[],[0.2,0.8])
f_Coughing = Prob(Coughing,[Bronchitis],[0.8,0.2,0.07,0.93])
f_Bronchitis = Prob(Bronchitis,[Influenza,Smokes],[0.99,0.01,0.9,0.1,0.7,0.3,1.0E-4,0.9999])
f_Wheezing = Prob(Wheezing,[Bronchitis],[0.6,0.4,0.001,0.999])
f_Sore_Throat = Prob(Sore_Throat,[Influenza],[0.3,0.7,0.001,0.999])
f_Influenza = Prob(Influenza,[],[0.05,0.95])
Simple_Diagnostic_Example = Belief_network(
    vars=[Fever,Smokes,Coughing,Bronchitis,Wheezing,Sore_Throat,Influenza],
    factors=[f_Fever,f_Smokes,f_Coughing,f_Bronchitis,f_Wheezing,f_Sore_Throat,f_Influenza],
    positions=[])

B = Variable('B', ['T', 'F'])
A = Variable('A', ['T', 'F'])
C = Variable('C', ['T', 'F'])
E = Variable('E', ['T', 'F'])
D = Variable('D', ['T', 'F'])
F = Variable('F', ['T', 'F'])
G = Variable('G', ['T', 'F']) 
f_B = Prob(B,[],[0.7,0.3])
f_A = Prob(A,[B],[0.88,0.12,0.38,0.62])
f_C = Prob(C,[B,D],[0.93,0.07,0.33,0.67,0.53,0.47,0.83,0.17])
f_E = Prob(E,[],[0.91,0.09])
f_D = Prob(D,[E],[0.04,0.96,0.84,0.16])
f_F = Prob(F,[C],[0.45,0.55,0.85,0.15])
f_G = Prob(G,[F],[0.26,0.74,0.96,0.04])
Simple_graph = Belief_network(
    vars=[B,A,C,E,D,F,G],
    factors=[f_B,f_A,f_C,f_E,f_D,f_F,f_G],
    positions=[])

B = Variable('B', ['T', 'F'])
A = Variable('A', ['T', 'F'])
I = Variable('I', ['T', 'F'])
C = Variable('C', ['T', 'F'])
J = Variable('J', ['T', 'F'])
H = Variable('H', ['T', 'F'])
E = Variable('E', ['T', 'F'])
D = Variable('D', ['T', 'F'])
F = Variable('F', ['T', 'F'])
G = Variable('G', ['T', 'F']) 
f_B = Prob(B,[C],[0.9,0.1,0.4,0.6])
f_A = Prob(A,[B],[0.7,0.3,0.4,0.6])
f_I = Prob(I,[H],[0.8,0.2,0.1,0.9])
f_C = Prob(C,[],[0.5,0.5])
f_J = Prob(J,[],[0.3,0.7])
f_H = Prob(H,[G,J],[0.8,0.2,0.3,0.7,0.5,0.5,0.1,0.9])
f_E = Prob(E,[C],[0.7,0.3,0.2,0.8])
f_D = Prob(D,[B,E],[0.3,0.7,0.5,0.5,0.2,0.8,0.9,0.1])
f_F = Prob(F,[E,G],[0.9,0.1,0.2,0.8,0.4,0.6,0.7,0.3])
f_G = Prob(G,[],[0.2,0.8])
Conditional_Independence_Quiz = Belief_network(
    vars=[B,A,I,C,J,H,E,D,F,G],
    factors=[f_B,f_A,f_I,f_C,f_J,f_H,f_E,f_D,f_F,f_G],
    positions=[])

Spark_Plugs = Variable('Spark_Plugs', ['okay', 'too_wide', 'fouled'])
Distributer_OK = Variable('Distributer_OK', ['T', 'F'])
Alternator_OK = Variable('Alternator_OK', ['T', 'F'])
Starter_Motor_OK = Variable('Starter_Motor_OK', ['T', 'F'])
Car_Cranks = Variable('Car_Cranks', ['T', 'F'])
Battery_Voltage = Variable('Battery_Voltage', ['strong', 'weak', 'dead'])
Voltage_at_Plug = Variable('Voltage_at_Plug', ['strong', 'weak', 'dead'])
Air_Filter_Clean = Variable('Air_Filter_Clean', ['T', 'F'])
Charging_System_OK = Variable('Charging_System_OK', ['T', 'F'])
Spark_Quality = Variable('Spark_Quality', ['good', 'bad', 'very_bad'])
Air_System_OK = Variable('Air_System_OK', ['T', 'F'])
Headlights = Variable('Headlights', ['bright', 'dim', 'off'])
Main_Fuse_OK = Variable('Main_Fuse_OK', ['T', 'F'])
Starter_System_OK = Variable('Starter_System_OK', ['T', 'F'])
Spark_Adequate = Variable('Spark_Adequate', ['T', 'F'])
Car_Starts = Variable('Car_Starts', ['T', 'F'])
Spark_Timing = Variable('Spark_Timing', ['good', 'bad', 'very_bad'])
Battery_Age = Variable('Battery_Age', ['new', 'old', 'very_old'])
Fuel_System_OK = Variable('Fuel_System_OK', ['T', 'F']) 
f_Spark_Plugs = Prob(Spark_Plugs,[],[0.99,0.003,0.007])
f_Distributer_OK = Prob(Distributer_OK,[],[0.99,0.01])
f_Alternator_OK = Prob(Alternator_OK,[],[0.9997,3.0E-4])
f_Starter_Motor_OK = Prob(Starter_Motor_OK,[],[0.992,0.008])
f_Car_Cranks = Prob(Car_Cranks,[Starter_System_OK],[0.98,0.02,0.0,1.0])
f_Battery_Voltage = Prob(Battery_Voltage,[Charging_System_OK,Battery_Age],[0.999,8.0E-4,2.0E-4,0.99,0.008,0.002,0.6,0.3,0.1,0.8,0.15,0.05,0.05,0.3,0.65,0.002,0.1,0.898])
f_Voltage_at_Plug = Prob(Voltage_at_Plug,[Battery_Voltage,Main_Fuse_OK,Distributer_OK],[0.98,0.015,0.005,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.1,0.8,0.1,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0])
f_Air_Filter_Clean = Prob(Air_Filter_Clean,[],[0.9,0.1])
f_Charging_System_OK = Prob(Charging_System_OK,[Alternator_OK],[0.995,0.005,0.0,1.0])
f_Spark_Quality = Prob(Spark_Quality,[Voltage_at_Plug,Spark_Plugs],[1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0,0.2,0.8,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0])
f_Air_System_OK = Prob(Air_System_OK,[Air_Filter_Clean],[0.9,0.1,0.3,0.7])
f_Headlights = Prob(Headlights,[Voltage_at_Plug],[0.98,0.015,0.005,0.05,0.9,0.05,0.0,0.0,1.0])
f_Main_Fuse_OK = Prob(Main_Fuse_OK,[],[0.999,0.001])
f_Starter_System_OK = Prob(Starter_System_OK,[Battery_Voltage,Main_Fuse_OK,Starter_Motor_OK],[0.998,0.002,0.0,1.0,0.0,1.0,0.0,1.0,0.72,0.28,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_Spark_Adequate = Prob(Spark_Adequate,[Spark_Timing,Spark_Quality],[0.99,0.01,0.5,0.5,0.1,0.9,0.5,0.5,0.05,0.95,0.01,0.99,0.1,0.9,0.01,0.99,0.0,1.0])
f_Car_Starts = Prob(Car_Starts,[Car_Cranks,Fuel_System_OK,Air_System_OK,Spark_Adequate],[1.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_Spark_Timing = Prob(Spark_Timing,[Distributer_OK],[0.97,0.02,0.01,0.2,0.3,0.5])
f_Battery_Age = Prob(Battery_Age,[],[0.4,0.4,0.2])
f_Fuel_System_OK = Prob(Fuel_System_OK,[],[0.9,0.1])
Car_Starting_Problem = Belief_network(
    vars=[Spark_Plugs,Distributer_OK,Alternator_OK,Starter_Motor_OK,Car_Cranks,Battery_Voltage,Voltage_at_Plug,Air_Filter_Clean,Charging_System_OK,Spark_Quality,Air_System_OK,Headlights,Main_Fuse_OK,Starter_System_OK,Spark_Adequate,Car_Starts,Spark_Timing,Battery_Age,Fuel_System_OK],
    factors=[f_Spark_Plugs,f_Distributer_OK,f_Alternator_OK,f_Starter_Motor_OK,f_Car_Cranks,f_Battery_Voltage,f_Voltage_at_Plug,f_Air_Filter_Clean,f_Charging_System_OK,f_Spark_Quality,f_Air_System_OK,f_Headlights,f_Main_Fuse_OK,f_Starter_System_OK,f_Spark_Adequate,f_Car_Starts,f_Spark_Timing,f_Battery_Age,f_Fuel_System_OK],
    positions=[])

p1 = Variable('p1', ['T', 'F'])
w2 = Variable('w2', ['live', 'dead'])
w1 = Variable('w1', ['live', 'dead'])
cb1_st = Variable('cb1_st', ['on', 'off'])
l1_lit = Variable('l1_lit', ['T', 'F'])
cb2_st = Variable('cb2_st', ['on', 'off'])
s3_pos = Variable('s3_pos', ['up', 'down'])
w6 = Variable('w6', ['live', 'dead'])
l2_st = Variable('l2_st', ['ok', 'intermittent', 'broken'])
s2_pos = Variable('s2_pos', ['up', 'down'])
w3 = Variable('w3', ['live', 'dead'])
l1_st = Variable('l1_st', ['ok', 'intermittent', 'broken'])
s3_st = Variable('s3_st', ['ok', 'upside_down', 'short', 'intermittent', 'broken'])
outside_power = Variable('outside_power', ['on', 'off'])
s2_st = Variable('s2_st', ['ok', 'upside_down', 'short', 'intermittent', 'broken'])
w0 = Variable('w0', ['live', 'dead'])
l2_lit = Variable('l2_lit', ['T', 'F'])
w4 = Variable('w4', ['live', 'dead'])
s1_pos = Variable('s1_pos', ['up', 'down'])
p2 = Variable('p2', ['T', 'F'])
s1_st = Variable('s1_st', ['ok', 'upside_down', 'short', 'intermittent', 'broken']) 
f_p1 = Prob(p1,[w3],[1.0,0.0,0.0,1.0])
f_w2 = Prob(w2,[w3,s1_st,s1_pos],[0.0,1.0,1.0,0.0,1.0,0.0,0.0,1.0,0.4,0.6,0.4,0.6,0.2,0.8,0.2,0.8,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_w1 = Prob(w1,[w3,s1_st,s1_pos],[1.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,0.6,0.4,0.4,0.6,0.4,0.6,0.01,0.99,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_cb1_st = Prob(cb1_st,[],[0.999,0.001])
f_l1_lit = Prob(l1_lit,[w0,l1_st],[1.0,0.0,0.7,0.3,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_cb2_st = Prob(cb2_st,[],[0.999,0.001])
f_s3_pos = Prob(s3_pos,[],[0.8,0.2])
f_w6 = Prob(w6,[outside_power,cb2_st],[1.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_l2_st = Prob(l2_st,[],[0.9,0.03,0.07])
f_s2_pos = Prob(s2_pos,[],[0.5,0.5])
f_w3 = Prob(w3,[outside_power,cb1_st],[1.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_l1_st = Prob(l1_st,[],[0.9,0.07,0.03])
f_s3_st = Prob(s3_st,[],[0.9,0.01,0.04,0.03,0.02])
f_outside_power = Prob(outside_power,[],[0.98,0.02])
f_s2_st = Prob(s2_st,[],[0.9,0.01,0.04,0.03,0.02])
f_w0 = Prob(w0,[w1,w2,s2_st,s2_pos],[1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,0.8,0.2,0.8,0.2,0.4,0.6,0.4,0.6,0.0,1.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,0.4,0.6,0.4,0.6,0.2,0.8,0.2,0.8,0.0,1.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,0.0,0.0,1.0,0.4,0.6,0.4,0.6,0.2,0.8,0.2,0.8,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_l2_lit = Prob(l2_lit,[w4,l2_st],[1.0,0.0,0.6,0.4,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_w4 = Prob(w4,[w3,s3_pos,s3_st],[1.0,0.0,0.0,1.0,0.4,0.6,0.2,0.8,0.0,1.0,0.0,1.0,1.0,0.0,0.4,0.6,0.2,0.8,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_s1_pos = Prob(s1_pos,[],[0.5,0.5])
f_p2 = Prob(p2,[w6],[1.0,0.0,0.0,1.0])
f_s1_st = Prob(s1_st,[],[0.9,0.01,0.04,0.03,0.02])
Electrical_Diagnosis_Problem = Belief_network(
    vars=[p1,w2,w1,cb1_st,l1_lit,cb2_st,s3_pos,w6,l2_st,s2_pos,w3,l1_st,s3_st,outside_power,s2_st,w0,l2_lit,w4,s1_pos,p2,s1_st],
    factors=[f_p1,f_w2,f_w1,f_cb1_st,f_l1_lit,f_cb2_st,f_s3_pos,f_w6,f_l2_st,f_s2_pos,f_w3,f_l1_st,f_s3_st,f_outside_power,f_s2_st,f_w0,f_l2_lit,f_w4,f_s1_pos,f_p2,f_s1_st],
    positions=[])

PRESS = Variable('PRESS', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
SHUNT = Variable('SHUNT', ['NORMAL', 'HIGH'])
STROKEVOLUME = Variable('STROKEVOLUME', ['LOW', 'NORMAL', 'HIGH'])
FIO2 = Variable('FIO2', ['LOW', 'NORMAL'])
INTUBATION = Variable('INTUBATION', ['NORMAL', 'ESOPHAGEAL', 'ONESIDED'])
MINVOLSET = Variable('MINVOLSET', ['LOW', 'NORMAL', 'HIGH'])
HR = Variable('HR', ['LOW', 'NORMAL', 'HIGH'])
VENTTUBE = Variable('VENTTUBE', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
DISCONNECT = Variable('DISCONNECT', ['TRUE', 'FALSE'])
CO = Variable('CO', ['LOW', 'NORMAL', 'HIGH'])
PAP = Variable('PAP', ['LOW', 'NORMAL', 'HIGH'])
MINVOL = Variable('MINVOL', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
HYPOVOLEMIA = Variable('HYPOVOLEMIA', ['TRUE', 'FALSE'])
CVP = Variable('CVP', ['LOW', 'NORMAL', 'HIGH'])
PULMEMBOLUS = Variable('PULMEMBOLUS', ['TRUE', 'FALSE'])
ARTCO2 = Variable('ARTCO2', ['LOW', 'NORMAL', 'HIGH'])
HRBP = Variable('HRBP', ['LOW', 'NORMAL', 'HIGH'])
TPR = Variable('TPR', ['LOW', 'NORMAL', 'HIGH'])
INSUFFANESTH = Variable('INSUFFANESTH', ['TRUE', 'FALSE'])
VENTALV = Variable('VENTALV', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
HREKG = Variable('HREKG', ['LOW', 'NORMAL', 'HIGH'])
ANAPHYLAXIS = Variable('ANAPHYLAXIS', ['TRUE', 'FALSE'])
HRSAT = Variable('HRSAT', ['LOW', 'NORMAL', 'HIGH'])
EXPCO2 = Variable('EXPCO2', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
ERRCAUTER = Variable('ERRCAUTER', ['TRUE', 'FALSE'])
SAO2 = Variable('SAO2', ['LOW', 'NORMAL', 'HIGH'])
PVSAT = Variable('PVSAT', ['LOW', 'NORMAL', 'HIGH'])
LVFAILURE = Variable('LVFAILURE', ['TRUE', 'FALSE'])
BP = Variable('BP', ['LOW', 'NORMAL', 'HIGH'])
ERRLOWOUTPUT = Variable('ERRLOWOUTPUT', ['TRUE', 'FALSE'])
CATECHOL = Variable('CATECHOL', ['NORMAL', 'HIGH'])
PCWP = Variable('PCWP', ['LOW', 'NORMAL', 'HIGH'])
KINKEDTUBE = Variable('KINKEDTUBE', ['TRUE', 'FALSE'])
VENTMACH = Variable('VENTMACH', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
HISTORY = Variable('HISTORY', ['TRUE', 'FALSE'])
LVEDVOLUME = Variable('LVEDVOLUME', ['LOW', 'NORMAL', 'HIGH'])
VENTLUNG = Variable('VENTLUNG', ['ZERO', 'LOW', 'NORMAL', 'HIGH']) 
f_PRESS = Prob(PRESS,[KINKEDTUBE,INTUBATION,VENTTUBE],[0.97,0.01,0.01,0.01,0.01,0.3,0.49,0.2,0.01,0.01,0.08,0.9,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.01,0.29,0.3,0.4,0.01,0.01,0.08,0.9,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.4,0.58,0.01,0.01,0.2,0.75,0.04,0.01,0.2,0.7,0.09,0.01,0.97,0.01,0.01,0.01,0.1,0.84,0.05,0.01,0.05,0.25,0.25,0.45,0.01,0.15,0.25,0.59,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.01,0.9,0.08,0.01,0.01,0.01,0.38,0.6,0.01,0.01,0.01,0.97])
f_SHUNT = Prob(SHUNT,[PULMEMBOLUS,INTUBATION],[0.1,0.9,0.01,0.99,0.95,0.05,0.1,0.9,0.95,0.05,0.05,0.95])
f_STROKEVOLUME = Prob(STROKEVOLUME,[HYPOVOLEMIA,LVFAILURE],[0.98,0.01,0.01,0.95,0.04,0.01,0.5,0.49,0.01,0.05,0.9,0.05])
f_FIO2 = Prob(FIO2,[],[0.05,0.95])
f_INTUBATION = Prob(INTUBATION,[],[0.92,0.03,0.05])
f_MINVOLSET = Prob(MINVOLSET,[],[0.05,0.9,0.05])
f_HR = Prob(HR,[CATECHOL],[0.05,0.9,0.05,0.01,0.09,0.9])
f_VENTTUBE = Prob(VENTTUBE,[DISCONNECT,VENTMACH],[0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97])
f_DISCONNECT = Prob(DISCONNECT,[],[0.1,0.9])
f_CO = Prob(CO,[STROKEVOLUME,HR],[0.98,0.01,0.01,0.95,0.04,0.01,0.3,0.69,0.01,0.95,0.04,0.01,0.04,0.95,0.01,0.01,0.3,0.69,0.8,0.19,0.01,0.01,0.04,0.95,0.01,0.01,0.98])
f_PAP = Prob(PAP,[PULMEMBOLUS],[0.01,0.19,0.8,0.05,0.9,0.05])
f_MINVOL = Prob(MINVOL,[INTUBATION,VENTLUNG],[0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.6,0.38,0.01,0.01,0.5,0.48,0.01,0.01,0.5,0.48,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97])
f_HYPOVOLEMIA = Prob(HYPOVOLEMIA,[],[0.2,0.8])
f_CVP = Prob(CVP,[LVEDVOLUME],[0.95,0.04,0.01,0.04,0.95,0.01,0.01,0.29,0.7])
f_PULMEMBOLUS = Prob(PULMEMBOLUS,[],[0.01,0.99])
f_ARTCO2 = Prob(ARTCO2,[VENTALV],[0.01,0.01,0.98,0.01,0.01,0.98,0.04,0.92,0.04,0.9,0.09,0.01])
f_HRBP = Prob(HRBP,[ERRLOWOUTPUT,HR],[0.98,0.01,0.01,0.4,0.59,0.01,0.3,0.4,0.3,0.98,0.01,0.01,0.01,0.98,0.01,0.01,0.01,0.98])
f_TPR = Prob(TPR,[ANAPHYLAXIS],[0.98,0.01,0.01,0.3,0.4,0.3])
f_INSUFFANESTH = Prob(INSUFFANESTH,[],[0.1,0.9])
f_VENTALV = Prob(VENTALV,[INTUBATION,VENTLUNG],[0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.03,0.95,0.01,0.01,0.01,0.94,0.04,0.01,0.01,0.88,0.1,0.01])
f_HREKG = Prob(HREKG,[ERRCAUTER,HR],[0.33333334,0.33333333,0.33333333,0.33333334,0.33333333,0.33333333,0.33333334,0.33333333,0.33333333,0.98,0.01,0.01,0.01,0.98,0.01,0.01,0.01,0.98])
f_ANAPHYLAXIS = Prob(ANAPHYLAXIS,[],[0.01,0.99])
f_HRSAT = Prob(HRSAT,[ERRCAUTER,HR],[0.33333334,0.33333333,0.33333333,0.33333334,0.33333333,0.33333333,0.33333334,0.33333333,0.33333333,0.98,0.01,0.01,0.01,0.98,0.01,0.01,0.01,0.98])
f_EXPCO2 = Prob(EXPCO2,[VENTLUNG,ARTCO2],[0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97])
f_ERRCAUTER = Prob(ERRCAUTER,[],[0.1,0.9])
f_SAO2 = Prob(SAO2,[PVSAT,SHUNT],[0.98,0.01,0.01,0.01,0.98,0.01,0.01,0.01,0.98,0.98,0.01,0.01,0.98,0.01,0.01,0.69,0.3,0.01])
f_PVSAT = Prob(PVSAT,[FIO2,VENTALV],[1.0,0.0,0.0,0.99,0.01,0.0,0.95,0.04,0.01,0.95,0.04,0.01,1.0,0.0,0.0,0.95,0.04,0.01,0.01,0.95,0.04,0.01,0.01,0.98])
f_LVFAILURE = Prob(LVFAILURE,[],[0.05,0.95])
f_BP = Prob(BP,[TPR,CO],[0.98,0.01,0.01,0.98,0.01,0.01,0.3,0.6,0.1,0.98,0.01,0.01,0.1,0.85,0.05,0.05,0.4,0.55,0.9,0.09,0.01,0.05,0.2,0.75,0.01,0.09,0.9])
f_ERRLOWOUTPUT = Prob(ERRLOWOUTPUT,[],[0.05,0.95])
f_CATECHOL = Prob(CATECHOL,[INSUFFANESTH,TPR,SAO2,ARTCO2],[0.01,0.99,0.01,0.99,0.7,0.3,0.01,0.99,0.05,0.95,0.7,0.3,0.01,0.99,0.05,0.95,0.7,0.3,0.01,0.99,0.01,0.99,0.7,0.3,0.01,0.99,0.05,0.95,0.7,0.3,0.01,0.99,0.05,0.95,0.7,0.3,0.01,0.99,0.01,0.99,0.1,0.9,0.01,0.99,0.01,0.99,0.1,0.9,0.01,0.99,0.01,0.99,0.1,0.9,0.01,0.99,0.05,0.95,0.95,0.05,0.01,0.99,0.05,0.95,0.95,0.05,0.05,0.95,0.05,0.95,0.95,0.05,0.01,0.99,0.05,0.95,0.99,0.01,0.01,0.99,0.05,0.95,0.99,0.01,0.05,0.95,0.05,0.95,0.99,0.01,0.01,0.99,0.01,0.99,0.3,0.7,0.01,0.99,0.01,0.99,0.3,0.7,0.01,0.99,0.01,0.99,0.3,0.7])
f_PCWP = Prob(PCWP,[LVEDVOLUME],[0.95,0.04,0.01,0.04,0.95,0.01,0.01,0.04,0.95])
f_KINKEDTUBE = Prob(KINKEDTUBE,[],[0.04,0.96])
f_VENTMACH = Prob(VENTMACH,[MINVOLSET],[0.05,0.93,0.01,0.01,0.05,0.01,0.93,0.01,0.05,0.01,0.01,0.93])
f_HISTORY = Prob(HISTORY,[LVFAILURE],[0.9,0.1,0.01,0.99])
f_LVEDVOLUME = Prob(LVEDVOLUME,[HYPOVOLEMIA,LVFAILURE],[0.95,0.04,0.01,0.98,0.01,0.01,0.01,0.09,0.9,0.05,0.9,0.05])
f_VENTLUNG = Prob(VENTLUNG,[KINKEDTUBE,INTUBATION,VENTTUBE],[0.97,0.01,0.01,0.01,0.95,0.03,0.01,0.01,0.4,0.58,0.01,0.01,0.3,0.68,0.01,0.01,0.97,0.01,0.01,0.01,0.95,0.03,0.01,0.01,0.5,0.48,0.01,0.01,0.3,0.68,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97])
Diagnosis_Problem = Belief_network(
    vars=[PRESS,SHUNT,STROKEVOLUME,FIO2,INTUBATION,MINVOLSET,HR,VENTTUBE,DISCONNECT,CO,PAP,MINVOL,HYPOVOLEMIA,CVP,PULMEMBOLUS,ARTCO2,HRBP,TPR,INSUFFANESTH,VENTALV,HREKG,ANAPHYLAXIS,HRSAT,EXPCO2,ERRCAUTER,SAO2,PVSAT,LVFAILURE,BP,ERRLOWOUTPUT,CATECHOL,PCWP,KINKEDTUBE,VENTMACH,HISTORY,LVEDVOLUME,VENTLUNG],
    factors=[f_PRESS,f_SHUNT,f_STROKEVOLUME,f_FIO2,f_INTUBATION,f_MINVOLSET,f_HR,f_VENTTUBE,f_DISCONNECT,f_CO,f_PAP,f_MINVOL,f_HYPOVOLEMIA,f_CVP,f_PULMEMBOLUS,f_ARTCO2,f_HRBP,f_TPR,f_INSUFFANESTH,f_VENTALV,f_HREKG,f_ANAPHYLAXIS,f_HRSAT,f_EXPCO2,f_ERRCAUTER,f_SAO2,f_PVSAT,f_LVFAILURE,f_BP,f_ERRLOWOUTPUT,f_CATECHOL,f_PCWP,f_KINKEDTUBE,f_VENTMACH,f_HISTORY,f_LVEDVOLUME,f_VENTLUNG],
    positions=[])

ScnRelPlFcst = Variable('ScnRelPlFcst', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'])
AMInsWliScen = Variable('AMInsWliScen', ['LessUnstable', 'Average', 'MoreUnstable'])
SfcWndShfDis = Variable('SfcWndShfDis', ['DenvCyclone', 'E_W_N', 'E_W_S', 'MovingFtorOt', 'DryLine', 'None', 'Other'])
InsInMt = Variable('InsInMt', ['None', 'Weak', 'Strong'])
AMCINInScen = Variable('AMCINInScen', ['LessThanAve', 'Average', 'MoreThanAve'])
PlainsFcst = Variable('PlainsFcst', ['XNIL', 'SIG', 'SVR'])
CombClouds = Variable('CombClouds', ['Cloudy', 'PC', 'Clear'])
LIfr12ZDENSd = Variable('LIfr12ZDENSd', ['LIGt0', 'N1GtLIGt_4', 'N5GtLIGt_8', 'LILt_8'])
CombMoisture = Variable('CombMoisture', ['VeryWet', 'Wet', 'Neutral', 'Dry'])
AMInstabMt = Variable('AMInstabMt', ['None', 'Weak', 'Strong'])
CldShadeOth = Variable('CldShadeOth', ['Cloudy', 'PC', 'Clear'])
N0_7muVerMo = Variable('N0_7muVerMo', ['StrongUp', 'WeakUp', 'Neutral', 'Down'])
LLIW = Variable('LLIW', ['Unfavorable', 'Weak', 'Moderate', 'Strong'])
ScenRelAMIns = Variable('ScenRelAMIns', ['ABI', 'CDEJ', 'F', 'G', 'H', 'K'])
VISCloudCov = Variable('VISCloudCov', ['Cloudy', 'PC', 'Clear'])
ScenRelAMCIN = Variable('ScenRelAMCIN', ['AB', 'CThruK'])
MidLLapse = Variable('MidLLapse', ['CloseToDryAd', 'Steep', 'ModerateOrLe'])
MvmtFeatures = Variable('MvmtFeatures', ['StrongFront', 'MarkedUpper', 'OtherRapid', 'NoMajor'])
CapInScen = Variable('CapInScen', ['LessThanAve', 'Average', 'MoreThanAve'])
CldShadeConv = Variable('CldShadeConv', ['None', 'Some', 'Marked'])
IRCloudCover = Variable('IRCloudCover', ['Cloudy', 'PC', 'Clear'])
CapChange = Variable('CapChange', ['Decreasing', 'LittleChange', 'Increasing'])
QGVertMotion = Variable('QGVertMotion', ['StrongUp', 'WeakUp', 'Neutral', 'Down'])
LoLevMoistAd = Variable('LoLevMoistAd', ['StrongPos', 'WeakPos', 'Neutral', 'Negative'])
Scenario = Variable('Scenario', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'])
MountainFcst = Variable('MountainFcst', ['XNIL', 'SIG', 'SVR'])
CombVerMo = Variable('CombVerMo', ['StrongUp', 'WeakUp', 'Neutral', 'Down'])
Boundaries = Variable('Boundaries', ['None', 'Weak', 'Strong'])
MeanRH = Variable('MeanRH', ['VeryMoist', 'Average', 'Dry'])
Dewpoints = Variable('Dewpoints', ['LowEvrywhere', 'LowAtStation', 'LowSHighN', 'LowNHighS', 'LowMtsHighPl', 'HighEvrywher', 'Other'])
InsChange = Variable('InsChange', ['Decreasing', 'LittleChange', 'Increasing'])
N34StarFcst = Variable('N34StarFcst', ['XNIL', 'SIG', 'SVR'])
SynForcng = Variable('SynForcng', ['SigNegative', 'NegToPos', 'SigPositive', 'PosToNeg', 'LittleChange'])
CompPlFcst = Variable('CompPlFcst', ['IncCapDecIns', 'LittleChange', 'DecCapIncIns'])
Date = Variable('Date', ['May15_Jun14', 'Jun15_Jul1', 'Jul2_Jul15', 'Jul16_Aug10', 'Aug11_Aug20', 'Aug20_Sep15'])
WndHodograph = Variable('WndHodograph', ['DCVZFavor', 'StrongWest', 'Westerly', 'Other'])
ScenRel3_4 = Variable('ScenRel3_4', ['ACEFK', 'B', 'D', 'GJ', 'HI'])
R5Fcst = Variable('R5Fcst', ['XNIL', 'SIG', 'SVR'])
LatestCIN = Variable('LatestCIN', ['None', 'PartInhibit', 'Stifling', 'TotalInhibit'])
WindFieldMt = Variable('WindFieldMt', ['Westerly', 'LVorOther'])
RaoContMoist = Variable('RaoContMoist', ['VeryWet', 'Wet', 'Neutral', 'Dry'])
AreaMeso_ALS = Variable('AreaMeso_ALS', ['StrongUp', 'WeakUp', 'Neutral', 'Down'])
SatContMoist = Variable('SatContMoist', ['VeryWet', 'Wet', 'Neutral', 'Dry'])
MorningBound = Variable('MorningBound', ['None', 'Weak', 'Strong'])
RHRatio = Variable('RHRatio', ['MoistMDryL', 'DryMMoistL', 'Other'])
WindAloft = Variable('WindAloft', ['LV', 'SWQuad', 'NWQuad', 'AllElse'])
LowLLapse = Variable('LowLLapse', ['CloseToDryAd', 'Steep', 'ModerateOrLe', 'Stable'])
AMDewptCalPl = Variable('AMDewptCalPl', ['Instability', 'Neutral', 'Stability'])
SubjVertMo = Variable('SubjVertMo', ['StronUp', 'WeakUp', 'Neutral', 'Down'])
OutflowFrMt = Variable('OutflowFrMt', ['None', 'Weak', 'Strong'])
AreaMoDryAir = Variable('AreaMoDryAir', ['VeryWet', 'Wet', 'Neutral', 'Dry'])
MorningCIN = Variable('MorningCIN', ['None', 'PartInhibit', 'Stifling', 'TotalInhibit'])
TempDis = Variable('TempDis', ['QStationary', 'Moving', 'None', 'Other'])
InsSclInScen = Variable('InsSclInScen', ['LessUnstable', 'Average', 'MoreUnstable'])
WindFieldPln = Variable('WindFieldPln', ['LV', 'DenvCyclone', 'LongAnticyc', 'E_NE', 'SEQuad', 'WidespdDnsl'])
CurPropConv = Variable('CurPropConv', ['None', 'Slight', 'Moderate', 'Strong']) 
f_ScnRelPlFcst = Prob(ScnRelPlFcst,[Scenario],[1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0])
f_AMInsWliScen = Prob(AMInsWliScen,[ScenRelAMIns,LIfr12ZDENSd,AMDewptCalPl],[0.6,0.3,0.1,0.85,0.13,0.02,0.95,0.04,0.01,0.3,0.3,0.4,0.5,0.3,0.2,0.75,0.2,0.05,0.06,0.21,0.73,0.2,0.4,0.4,0.5,0.4,0.1,0.01,0.04,0.95,0.05,0.2,0.75,0.35,0.35,0.3,0.4,0.3,0.3,0.7,0.2,0.1,0.9,0.08,0.02,0.15,0.3,0.55,0.25,0.5,0.25,0.6,0.3,0.1,0.03,0.17,0.8,0.2,0.3,0.5,0.45,0.4,0.15,0.01,0.04,0.95,0.05,0.18,0.77,0.25,0.4,0.35,0.35,0.35,0.3,0.55,0.4,0.05,0.85,0.13,0.02,0.07,0.38,0.55,0.2,0.6,0.2,0.5,0.43,0.07,0.0,0.05,0.95,0.05,0.35,0.6,0.25,0.5,0.25,0.0,0.02,0.98,0.0,0.05,0.95,0.04,0.16,0.8,0.3,0.4,0.3,0.5,0.3,0.2,0.75,0.2,0.05,0.15,0.35,0.5,0.2,0.6,0.2,0.15,0.7,0.15,0.07,0.23,0.7,0.13,0.47,0.4,0.1,0.75,0.15,0.02,0.18,0.8,0.04,0.26,0.7,0.07,0.3,0.63,0.35,0.45,0.2,0.4,0.5,0.1,0.58,0.4,0.02,0.1,0.25,0.65,0.15,0.45,0.4,0.4,0.45,0.15,0.02,0.18,0.8,0.05,0.25,0.7,0.15,0.35,0.5,0.01,0.09,0.9,0.03,0.17,0.8,0.08,0.32,0.6,0.3,0.55,0.15,0.4,0.5,0.1,0.5,0.43,0.07,0.1,0.35,0.55,0.25,0.5,0.25,0.3,0.5,0.2,0.05,0.22,0.73,0.1,0.35,0.55,0.15,0.35,0.5,0.02,0.1,0.88,0.04,0.16,0.8,0.1,0.25,0.65])
f_SfcWndShfDis = Prob(SfcWndShfDis,[Scenario],[0.65,0.05,0.1,0.08,0.04,0.07,0.01,0.65,0.05,0.1,0.1,0.02,0.07,0.01,0.0,0.65,0.2,0.02,0.06,0.05,0.02,0.12,0.02,0.02,0.02,0.45,0.27,0.1,0.06,0.14,0.04,0.04,0.25,0.4,0.07,0.1,0.1,0.1,0.02,0.0,0.56,0.12,0.02,0.05,0.05,0.0,0.35,0.33,0.2,0.01,0.1,0.15,0.4,0.0,0.23,0.11,0.02,0.1,0.5,0.3,0.01,0.02,0.05,0.06,0.08,0.04,0.02,0.6,0.14,0.06,0.05,0.13,0.05,0.39,0.13,0.15,0.1])
f_InsInMt = Prob(InsInMt,[CldShadeOth,AMInstabMt],[0.9,0.1,0.0,0.01,0.4,0.59,0.0,0.05,0.95,0.6,0.39,0.01,0.0,0.4,0.6,0.0,0.0,1.0,0.5,0.35,0.15,0.0,0.15,0.85,0.0,0.0,1.0])
f_AMCINInScen = Prob(AMCINInScen,[ScenRelAMCIN,MorningCIN],[1.0,0.0,0.0,0.6,0.37,0.03,0.25,0.45,0.3,0.0,0.1,0.9,0.75,0.25,0.0,0.3,0.6,0.1,0.01,0.4,0.59,0.0,0.03,0.97])
f_PlainsFcst = Prob(PlainsFcst,[CapInScen,InsSclInScen,CurPropConv,ScnRelPlFcst],[0.75,0.2,0.05,0.75,0.2,0.05,0.9,0.08,0.02,0.9,0.06,0.04,0.88,0.1,0.02,0.92,0.08,0.0,0.85,0.13,0.02,1.0,0.0,0.0,0.9,0.08,0.02,0.9,0.08,0.02,0.95,0.04,0.01,0.7,0.25,0.05,0.6,0.33,0.07,0.82,0.13,0.05,0.85,0.1,0.05,0.82,0.15,0.03,0.85,0.14,0.01,0.8,0.17,0.03,0.97,0.02,0.01,0.88,0.1,0.02,0.86,0.1,0.04,0.88,0.1,0.02,0.5,0.4,0.1,0.45,0.42,0.13,0.75,0.18,0.07,0.75,0.15,0.1,0.72,0.22,0.06,0.78,0.21,0.01,0.66,0.27,0.07,0.88,0.1,0.02,0.7,0.22,0.08,0.78,0.16,0.06,0.8,0.16,0.04,0.4,0.45,0.15,0.35,0.45,0.2,0.6,0.27,0.13,0.6,0.22,0.18,0.55,0.32,0.13,0.69,0.29,0.02,0.54,0.36,0.1,0.75,0.2,0.05,0.55,0.3,0.15,0.7,0.22,0.08,0.7,0.25,0.05,0.5,0.3,0.2,0.6,0.3,0.1,0.8,0.14,0.06,0.85,0.09,0.06,0.85,0.1,0.05,0.88,0.11,0.01,0.8,0.17,0.03,0.92,0.06,0.02,0.8,0.12,0.08,0.75,0.22,0.03,0.9,0.08,0.02,0.3,0.4,0.3,0.55,0.34,0.11,0.7,0.2,0.1,0.75,0.15,0.1,0.62,0.28,0.1,0.85,0.14,0.01,0.75,0.2,0.05,0.82,0.14,0.04,0.6,0.25,0.15,0.68,0.22,0.1,0.82,0.15,0.03,0.2,0.45,0.35,0.4,0.4,0.2,0.7,0.2,0.1,0.65,0.22,0.13,0.5,0.34,0.16,0.74,0.24,0.02,0.6,0.3,0.1,0.67,0.24,0.09,0.35,0.4,0.25,0.6,0.25,0.15,0.75,0.2,0.05,0.16,0.47,0.37,0.3,0.45,0.25,0.45,0.32,0.23,0.52,0.26,0.22,0.35,0.45,0.2,0.65,0.32,0.03,0.48,0.39,0.13,0.58,0.3,0.12,0.25,0.45,0.3,0.5,0.28,0.22,0.65,0.27,0.08,0.35,0.2,0.45,0.45,0.35,0.2,0.8,0.1,0.1,0.72,0.14,0.14,0.78,0.15,0.07,0.86,0.12,0.02,0.65,0.25,0.1,0.85,0.1,0.05,0.65,0.2,0.15,0.72,0.2,0.08,0.85,0.1,0.05,0.3,0.25,0.45,0.4,0.36,0.24,0.65,0.2,0.15,0.6,0.2,0.2,0.6,0.28,0.12,0.83,0.14,0.03,0.45,0.4,0.15,0.7,0.18,0.12,0.55,0.25,0.2,0.6,0.25,0.15,0.72,0.2,0.08,0.25,0.28,0.47,0.3,0.38,0.32,0.45,0.3,0.25,0.5,0.25,0.25,0.4,0.35,0.25,0.72,0.24,0.04,0.25,0.57,0.18,0.57,0.28,0.15,0.25,0.35,0.4,0.48,0.26,0.26,0.6,0.26,0.14,0.18,0.3,0.52,0.2,0.4,0.4,0.3,0.3,0.4,0.4,0.3,0.3,0.25,0.48,0.27,0.63,0.32,0.05,0.15,0.63,0.22,0.4,0.38,0.22,0.2,0.37,0.43,0.3,0.35,0.35,0.5,0.32,0.18,0.75,0.2,0.05,0.65,0.3,0.05,0.9,0.08,0.02,0.91,0.05,0.04,0.85,0.13,0.02,0.9,0.1,0.0,0.84,0.12,0.04,0.99,0.01,0.0,0.88,0.1,0.02,0.92,0.06,0.02,0.96,0.03,0.01,0.65,0.25,0.1,0.58,0.32,0.1,0.8,0.15,0.05,0.85,0.1,0.05,0.8,0.16,0.04,0.83,0.16,0.01,0.77,0.17,0.06,0.93,0.06,0.01,0.85,0.12,0.03,0.85,0.1,0.05,0.9,0.08,0.02,0.45,0.35,0.2,0.45,0.35,0.2,0.7,0.2,0.1,0.72,0.17,0.11,0.7,0.22,0.08,0.75,0.24,0.01,0.62,0.3,0.08,0.85,0.12,0.03,0.75,0.15,0.1,0.76,0.17,0.07,0.8,0.16,0.04,0.35,0.4,0.25,0.35,0.4,0.25,0.55,0.3,0.15,0.55,0.27,0.18,0.5,0.35,0.15,0.65,0.33,0.02,0.38,0.5,0.12,0.7,0.24,0.06,0.65,0.2,0.15,0.67,0.23,0.1,0.7,0.25,0.05,0.35,0.3,0.35,0.55,0.3,0.15,0.82,0.13,0.05,0.82,0.1,0.08,0.75,0.18,0.07,0.88,0.11,0.01,0.75,0.2,0.05,0.9,0.07,0.03,0.7,0.2,0.1,0.8,0.15,0.05,0.9,0.08,0.02,0.28,0.37,0.35,0.48,0.35,0.17,0.7,0.2,0.1,0.7,0.17,0.13,0.6,0.29,0.11,0.82,0.16,0.02,0.63,0.3,0.07,0.8,0.15,0.05,0.5,0.3,0.2,0.7,0.2,0.1,0.8,0.16,0.04,0.23,0.4,0.37,0.38,0.35,0.27,0.58,0.25,0.17,0.55,0.25,0.2,0.53,0.32,0.15,0.73,0.25,0.02,0.35,0.53,0.12,0.65,0.24,0.11,0.3,0.4,0.3,0.6,0.24,0.16,0.68,0.24,0.08,0.18,0.45,0.37,0.3,0.35,0.35,0.45,0.3,0.25,0.45,0.3,0.25,0.35,0.43,0.22,0.62,0.35,0.03,0.2,0.65,0.15,0.52,0.33,0.15,0.23,0.42,0.35,0.47,0.3,0.23,0.55,0.3,0.15,0.25,0.15,0.6,0.45,0.35,0.2,0.65,0.2,0.15,0.55,0.2,0.25,0.55,0.25,0.2,0.81,0.17,0.02,0.6,0.28,0.12,0.8,0.13,0.07,0.6,0.2,0.2,0.75,0.15,0.1,0.88,0.08,0.04,0.22,0.17,0.61,0.35,0.37,0.28,0.45,0.3,0.25,0.45,0.25,0.3,0.48,0.29,0.23,0.72,0.25,0.03,0.43,0.4,0.17,0.68,0.2,0.12,0.35,0.3,0.35,0.6,0.2,0.2,0.74,0.16,0.1,0.19,0.18,0.63,0.25,0.4,0.35,0.35,0.3,0.35,0.35,0.3,0.35,0.35,0.35,0.3,0.65,0.3,0.05,0.22,0.58,0.2,0.45,0.35,0.2,0.25,0.34,0.41,0.48,0.26,0.26,0.58,0.25,0.17,0.15,0.2,0.65,0.18,0.4,0.42,0.25,0.35,0.4,0.25,0.35,0.4,0.25,0.42,0.33,0.58,0.36,0.06,0.13,0.62,0.25,0.3,0.45,0.25,0.22,0.35,0.43,0.35,0.32,0.33,0.5,0.3,0.2,0.75,0.2,0.05,0.75,0.2,0.05,0.95,0.04,0.01,0.93,0.04,0.03,0.92,0.06,0.02,0.87,0.13,0.0,0.9,0.06,0.04,0.98,0.02,0.0,0.92,0.06,0.02,0.95,0.04,0.01,0.97,0.02,0.01,0.6,0.3,0.1,0.65,0.28,0.07,0.9,0.08,0.02,0.85,0.1,0.05,0.82,0.13,0.05,0.8,0.19,0.01,0.8,0.13,0.07,0.91,0.08,0.01,0.85,0.12,0.03,0.9,0.08,0.02,0.93,0.06,0.01,0.35,0.4,0.25,0.45,0.4,0.15,0.75,0.19,0.06,0.7,0.2,0.1,0.6,0.3,0.1,0.72,0.27,0.01,0.6,0.3,0.1,0.8,0.16,0.04,0.75,0.17,0.08,0.75,0.2,0.05,0.88,0.1,0.02,0.2,0.45,0.35,0.3,0.45,0.25,0.55,0.3,0.15,0.5,0.3,0.2,0.45,0.38,0.17,0.6,0.38,0.02,0.28,0.57,0.15,0.65,0.28,0.07,0.63,0.25,0.12,0.62,0.28,0.1,0.8,0.17,0.03,0.5,0.2,0.3,0.6,0.25,0.15,0.85,0.1,0.05,0.85,0.07,0.08,0.75,0.15,0.1,0.85,0.14,0.01,0.75,0.2,0.05,0.94,0.05,0.01,0.65,0.22,0.13,0.83,0.1,0.07,0.93,0.06,0.01,0.4,0.28,0.32,0.5,0.25,0.25,0.72,0.18,0.1,0.65,0.2,0.15,0.55,0.3,0.15,0.78,0.2,0.02,0.55,0.35,0.1,0.85,0.12,0.03,0.45,0.3,0.25,0.73,0.15,0.12,0.85,0.12,0.03,0.3,0.34,0.36,0.35,0.35,0.3,0.55,0.25,0.2,0.5,0.27,0.23,0.4,0.38,0.22,0.7,0.28,0.02,0.35,0.5,0.15,0.6,0.25,0.15,0.35,0.35,0.3,0.62,0.22,0.16,0.7,0.22,0.08,0.23,0.4,0.37,0.25,0.4,0.35,0.4,0.3,0.3,0.4,0.3,0.3,0.3,0.45,0.25,0.57,0.4,0.03,0.15,0.65,0.2,0.5,0.33,0.17,0.25,0.36,0.39,0.5,0.28,0.22,0.55,0.3,0.15,0.4,0.08,0.52,0.45,0.25,0.3,0.75,0.1,0.15,0.65,0.15,0.2,0.52,0.25,0.23,0.82,0.16,0.02,0.65,0.27,0.08,0.85,0.09,0.06,0.5,0.2,0.3,0.77,0.1,0.13,0.9,0.07,0.03,0.27,0.1,0.63,0.35,0.3,0.35,0.55,0.22,0.23,0.45,0.25,0.3,0.42,0.3,0.28,0.74,0.22,0.04,0.45,0.4,0.15,0.77,0.13,0.1,0.3,0.25,0.45,0.68,0.15,0.17,0.75,0.15,0.1,0.15,0.16,0.69,0.25,0.3,0.45,0.4,0.3,0.3,0.3,0.3,0.4,0.25,0.4,0.35,0.6,0.34,0.06,0.18,0.62,0.2,0.47,0.3,0.23,0.25,0.3,0.45,0.5,0.22,0.28,0.5,0.27,0.23,0.1,0.2,0.7,0.2,0.3,0.5,0.2,0.4,0.4,0.23,0.3,0.47,0.15,0.45,0.4,0.5,0.42,0.08,0.1,0.65,0.25,0.28,0.4,0.32,0.2,0.32,0.48,0.3,0.28,0.42,0.38,0.32,0.3])
f_CombClouds = Prob(CombClouds,[VISCloudCov,IRCloudCover],[0.95,0.04,0.01,0.85,0.13,0.02,0.8,0.1,0.1,0.45,0.52,0.03,0.1,0.8,0.1,0.05,0.45,0.5,0.1,0.4,0.5,0.02,0.28,0.7,0.0,0.02,0.98])
f_LIfr12ZDENSd = Prob(LIfr12ZDENSd,[],[0.1,0.52,0.3,0.08])
f_CombMoisture = Prob(CombMoisture,[SatContMoist,RaoContMoist],[0.9,0.1,0.0,0.0,0.6,0.35,0.05,0.0,0.3,0.5,0.2,0.0,0.25,0.35,0.25,0.15,0.55,0.4,0.05,0.0,0.15,0.6,0.2,0.05,0.05,0.4,0.45,0.1,0.1,0.3,0.3,0.3,0.25,0.3,0.35,0.1,0.1,0.35,0.5,0.05,0.0,0.15,0.7,0.15,0.0,0.1,0.4,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25])
f_AMInstabMt = Prob(AMInstabMt,[],[0.333333,0.333333,0.333334])
f_CldShadeOth = Prob(CldShadeOth,[AreaMeso_ALS,AreaMoDryAir,CombClouds],[1.0,0.0,0.0,0.85,0.15,0.0,0.25,0.35,0.4,0.92,0.08,0.0,0.7,0.29,0.01,0.15,0.4,0.45,0.88,0.12,0.0,0.4,0.5,0.1,0.1,0.4,0.5,0.85,0.14,0.01,0.55,0.43,0.02,0.1,0.25,0.65,0.95,0.05,0.0,0.4,0.55,0.05,0.05,0.45,0.5,0.9,0.09,0.01,0.25,0.6,0.15,0.01,0.3,0.69,0.85,0.15,0.0,0.15,0.75,0.1,0.0,0.2,0.8,0.6,0.39,0.01,0.01,0.9,0.09,0.0,0.15,0.85,0.93,0.07,0.0,0.2,0.78,0.02,0.01,0.29,0.7,0.8,0.2,0.0,0.01,0.89,0.1,0.0,0.1,0.9,0.8,0.18,0.02,0.03,0.85,0.12,0.0,0.05,0.95,0.78,0.2,0.02,0.01,0.74,0.25,0.0,0.04,0.96,0.74,0.25,0.01,0.0,0.5,0.5,0.0,0.1,0.9,0.65,0.34,0.01,0.0,0.4,0.6,0.0,0.02,0.98,0.5,0.48,0.02,0.01,0.74,0.25,0.0,0.01,0.99,0.42,0.55,0.03,0.05,0.65,0.3,0.0,0.0,1.0])
f_N0_7muVerMo = Prob(N0_7muVerMo,[],[0.25,0.25,0.25,0.25])
f_LLIW = Prob(LLIW,[],[0.12,0.32,0.38,0.18])
f_ScenRelAMIns = Prob(ScenRelAMIns,[Scenario],[1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0])
f_VISCloudCov = Prob(VISCloudCov,[],[0.1,0.5,0.4])
f_ScenRelAMCIN = Prob(ScenRelAMCIN,[Scenario],[1.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_MidLLapse = Prob(MidLLapse,[Scenario],[0.25,0.55,0.2,0.25,0.5,0.25,0.4,0.38,0.22,0.43,0.37,0.2,0.02,0.38,0.6,0.0,0.1,0.9,0.84,0.16,0.0,0.25,0.31,0.44,0.41,0.29,0.3,0.23,0.42,0.35,0.16,0.28,0.56])
f_MvmtFeatures = Prob(MvmtFeatures,[Scenario],[0.25,0.55,0.2,0.0,0.05,0.1,0.1,0.75,0.1,0.3,0.3,0.3,0.18,0.38,0.34,0.1,0.02,0.02,0.26,0.7,0.05,0.07,0.05,0.83,0.1,0.25,0.15,0.5,0.0,0.6,0.1,0.3,0.2,0.1,0.2,0.5,0.04,0.0,0.04,0.92,0.5,0.35,0.09,0.06])
f_CapInScen = Prob(CapInScen,[CapChange,AMCINInScen],[1.0,0.0,0.0,0.75,0.25,0.0,0.3,0.35,0.35,0.98,0.02,0.0,0.03,0.94,0.03,0.0,0.02,0.98,0.35,0.35,0.3,0.0,0.25,0.75,0.0,0.0,1.0])
f_CldShadeConv = Prob(CldShadeConv,[InsInMt,WndHodograph],[1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.3,0.6,0.1,0.2,0.7,0.1,0.5,0.46,0.04,0.8,0.19,0.01,0.0,0.3,0.7,0.0,0.2,0.8,0.1,0.5,0.4,0.5,0.38,0.12])
f_IRCloudCover = Prob(IRCloudCover,[],[0.15,0.45,0.4])
f_CapChange = Prob(CapChange,[CompPlFcst],[0.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,0.0])
f_QGVertMotion = Prob(QGVertMotion,[],[0.15,0.15,0.5,0.2])
f_LoLevMoistAd = Prob(LoLevMoistAd,[],[0.12,0.28,0.3,0.3])
f_Scenario = Prob(Scenario,[Date],[0.1,0.16,0.1,0.08,0.08,0.01,0.08,0.1,0.09,0.03,0.17,0.05,0.16,0.09,0.09,0.12,0.02,0.13,0.06,0.07,0.11,0.1,0.04,0.13,0.1,0.08,0.15,0.03,0.14,0.04,0.06,0.15,0.08,0.04,0.13,0.09,0.07,0.2,0.08,0.06,0.05,0.07,0.13,0.08,0.04,0.11,0.1,0.07,0.17,0.05,0.1,0.05,0.07,0.14,0.1,0.05,0.11,0.1,0.08,0.11,0.02,0.11,0.06,0.08,0.11,0.17])
f_MountainFcst = Prob(MountainFcst,[InsInMt],[1.0,0.0,0.0,0.48,0.5,0.02,0.2,0.5,0.3])
f_CombVerMo = Prob(CombVerMo,[N0_7muVerMo,SubjVertMo,QGVertMotion],[1.0,0.0,0.0,0.0,0.9,0.1,0.0,0.0,0.7,0.2,0.1,0.0,0.2,0.5,0.2,0.1,0.9,0.1,0.0,0.0,0.7,0.3,0.0,0.0,0.15,0.7,0.15,0.0,0.1,0.35,0.45,0.1,0.7,0.2,0.1,0.0,0.15,0.7,0.15,0.0,0.2,0.6,0.2,0.0,0.1,0.2,0.6,0.1,0.2,0.5,0.2,0.1,0.1,0.35,0.45,0.1,0.1,0.2,0.6,0.1,0.1,0.1,0.2,0.6,0.9,0.1,0.0,0.0,0.7,0.3,0.0,0.0,0.15,0.7,0.15,0.0,0.1,0.35,0.45,0.1,0.7,0.3,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.7,0.3,0.0,0.0,0.2,0.7,0.1,0.15,0.7,0.15,0.0,0.0,0.7,0.3,0.0,0.0,0.3,0.7,0.0,0.0,0.15,0.5,0.35,0.1,0.35,0.45,0.1,0.0,0.2,0.7,0.1,0.0,0.15,0.5,0.35,0.0,0.1,0.2,0.7,0.7,0.2,0.1,0.0,0.15,0.7,0.15,0.0,0.2,0.6,0.2,0.0,0.1,0.2,0.6,0.1,0.15,0.7,0.15,0.0,0.0,0.7,0.3,0.0,0.0,0.3,0.7,0.0,0.0,0.15,0.5,0.35,0.2,0.6,0.2,0.0,0.0,0.3,0.7,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.7,0.3,0.1,0.2,0.6,0.1,0.0,0.15,0.5,0.35,0.0,0.0,0.7,0.3,0.0,0.0,0.3,0.7,0.2,0.5,0.2,0.1,0.1,0.35,0.45,0.1,0.1,0.2,0.6,0.1,0.1,0.1,0.2,0.6,0.1,0.35,0.45,0.1,0.0,0.2,0.7,0.1,0.0,0.15,0.5,0.35,0.0,0.1,0.2,0.7,0.1,0.2,0.6,0.1,0.0,0.15,0.5,0.35,0.0,0.0,0.7,0.3,0.0,0.0,0.3,0.7,0.1,0.1,0.2,0.6,0.0,0.1,0.2,0.7,0.0,0.0,0.3,0.7,0.0,0.0,0.0,1.0])
f_Boundaries = Prob(Boundaries,[WndHodograph,OutflowFrMt,MorningBound],[0.5,0.48,0.02,0.3,0.5,0.2,0.1,0.25,0.65,0.3,0.63,0.07,0.1,0.5,0.4,0.05,0.2,0.75,0.0,0.55,0.45,0.0,0.4,0.6,0.0,0.15,0.85,0.75,0.22,0.03,0.45,0.45,0.1,0.25,0.4,0.35,0.15,0.7,0.15,0.1,0.75,0.15,0.05,0.5,0.45,0.0,0.5,0.5,0.0,0.4,0.6,0.0,0.2,0.8,0.8,0.18,0.02,0.35,0.5,0.15,0.25,0.35,0.4,0.15,0.7,0.15,0.05,0.8,0.15,0.05,0.45,0.5,0.0,0.7,0.3,0.0,0.5,0.5,0.0,0.2,0.8,0.7,0.28,0.02,0.25,0.6,0.15,0.05,0.35,0.6,0.4,0.55,0.05,0.2,0.65,0.15,0.05,0.3,0.65,0.02,0.73,0.25,0.01,0.5,0.49,0.01,0.2,0.79])
f_MeanRH = Prob(MeanRH,[Scenario],[0.33,0.5,0.17,0.4,0.4,0.2,0.05,0.45,0.5,0.1,0.5,0.4,0.05,0.65,0.3,1.0,0.0,0.0,0.0,0.07,0.93,0.4,0.55,0.05,0.2,0.45,0.35,0.05,0.55,0.4,0.2,0.4,0.4])
f_Dewpoints = Prob(Dewpoints,[Scenario],[0.04,0.05,0.15,0.05,0.19,0.3,0.22,0.05,0.07,0.15,0.1,0.3,0.27,0.06,0.4,0.25,0.0,0.15,0.05,0.02,0.13,0.13,0.22,0.18,0.07,0.34,0.03,0.03,0.15,0.2,0.2,0.18,0.11,0.11,0.05,0.0,0.0,0.0,0.0,0.0,0.98,0.02,0.5,0.27,0.15,0.02,0.02,0.0,0.04,0.0,0.02,0.1,0.05,0.5,0.2,0.13,0.0,0.02,0.7,0.0,0.2,0.04,0.04,0.1,0.45,0.1,0.05,0.26,0.02,0.02,0.1,0.1,0.1,0.2,0.05,0.1,0.35])
f_InsChange = Prob(InsChange,[CompPlFcst,LoLevMoistAd],[0.0,0.05,0.95,0.05,0.15,0.8,0.15,0.5,0.35,0.5,0.4,0.1,0.0,0.12,0.88,0.1,0.4,0.5,0.2,0.6,0.2,0.8,0.16,0.04,0.05,0.15,0.8,0.25,0.5,0.25,0.35,0.5,0.15,0.9,0.09,0.01])
f_N34StarFcst = Prob(N34StarFcst,[ScenRel3_4,PlainsFcst],[0.94,0.05,0.01,0.06,0.89,0.05,0.01,0.05,0.94,0.98,0.02,0.0,0.04,0.94,0.02,0.0,0.03,0.97,0.92,0.06,0.02,0.01,0.89,0.1,0.0,0.01,0.99,0.92,0.06,0.02,0.03,0.92,0.05,0.01,0.04,0.95,0.99,0.01,0.0,0.09,0.9,0.01,0.03,0.12,0.85])
f_SynForcng = Prob(SynForcng,[Scenario],[0.35,0.25,0.0,0.35,0.05,0.06,0.1,0.06,0.3,0.48,0.1,0.27,0.4,0.08,0.15,0.35,0.2,0.1,0.25,0.1,0.15,0.15,0.1,0.15,0.45,0.15,0.1,0.05,0.15,0.55,0.15,0.1,0.1,0.25,0.4,0.25,0.25,0.25,0.15,0.1,0.25,0.2,0.15,0.2,0.2,0.01,0.05,0.01,0.05,0.88,0.2,0.2,0.35,0.15,0.1])
f_CompPlFcst = Prob(CompPlFcst,[AreaMeso_ALS,CldShadeOth,Boundaries,CldShadeConv],[0.4,0.35,0.25,0.4,0.35,0.25,0.45,0.3,0.25,0.35,0.35,0.3,0.35,0.35,0.3,0.4,0.35,0.25,0.3,0.3,0.4,0.3,0.3,0.4,0.3,0.35,0.35,0.1,0.35,0.55,0.25,0.3,0.45,0.4,0.3,0.3,0.05,0.35,0.6,0.1,0.35,0.55,0.25,0.4,0.35,0.01,0.25,0.74,0.05,0.6,0.35,0.15,0.35,0.5,0.05,0.3,0.65,0.15,0.35,0.5,0.35,0.3,0.35,0.03,0.25,0.72,0.05,0.3,0.65,0.2,0.4,0.4,0.01,0.2,0.79,0.04,0.27,0.69,0.13,0.35,0.52,0.6,0.25,0.15,0.65,0.25,0.1,0.7,0.22,0.08,0.5,0.25,0.25,0.55,0.25,0.2,0.65,0.25,0.1,0.35,0.25,0.4,0.4,0.25,0.35,0.5,0.25,0.25,0.4,0.3,0.3,0.45,0.3,0.25,0.55,0.3,0.15,0.3,0.35,0.35,0.35,0.35,0.3,0.45,0.35,0.2,0.15,0.4,0.45,0.2,0.4,0.4,0.35,0.35,0.3,0.2,0.5,0.3,0.25,0.5,0.25,0.4,0.45,0.15,0.15,0.45,0.4,0.2,0.5,0.3,0.3,0.5,0.2,0.1,0.35,0.55,0.12,0.43,0.45,0.2,0.45,0.35,0.6,0.35,0.05,0.65,0.3,0.05,0.7,0.27,0.03,0.55,0.3,0.15,0.6,0.3,0.1,0.65,0.3,0.05,0.45,0.3,0.25,0.5,0.3,0.2,0.55,0.35,0.1,0.45,0.4,0.15,0.5,0.4,0.1,0.6,0.3,0.1,0.4,0.4,0.2,0.45,0.4,0.15,0.55,0.3,0.15,0.3,0.4,0.3,0.35,0.4,0.25,0.45,0.35,0.2,0.25,0.45,0.3,0.3,0.45,0.25,0.55,0.33,0.12,0.2,0.4,0.4,0.25,0.5,0.25,0.5,0.3,0.2,0.15,0.4,0.45,0.2,0.45,0.35,0.4,0.35,0.25,0.7,0.27,0.03,0.75,0.23,0.02,0.85,0.14,0.01,0.6,0.35,0.05,0.65,0.3,0.05,0.78,0.18,0.04,0.5,0.35,0.15,0.55,0.35,0.1,0.7,0.24,0.06,0.65,0.3,0.05,0.7,0.26,0.04,0.8,0.17,0.03,0.6,0.3,0.1,0.65,0.3,0.05,0.75,0.2,0.05,0.48,0.32,0.2,0.55,0.3,0.15,0.65,0.28,0.07,0.6,0.35,0.05,0.65,0.32,0.03,0.75,0.23,0.02,0.55,0.33,0.12,0.6,0.35,0.05,0.7,0.25,0.05,0.45,0.35,0.2,0.5,0.4,0.1,0.6,0.3,0.1])
f_Date = Prob(Date,[],[0.254098,0.131148,0.106557,0.213115,0.07377,0.221312])
f_WndHodograph = Prob(WndHodograph,[],[0.3,0.25,0.25,0.2])
f_ScenRel3_4 = Prob(ScenRel3_4,[Scenario],[1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0])
f_R5Fcst = Prob(R5Fcst,[MountainFcst,N34StarFcst],[1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0])
f_LatestCIN = Prob(LatestCIN,[],[0.4,0.4,0.15,0.05])
f_WindFieldMt = Prob(WindFieldMt,[Scenario],[0.8,0.2,0.35,0.65,0.75,0.25,0.7,0.3,0.65,0.35,0.15,0.85,0.7,0.3,0.3,0.7,0.5,0.5,0.01,0.99,0.7,0.3])
f_RaoContMoist = Prob(RaoContMoist,[],[0.15,0.2,0.4,0.25])
f_AreaMeso_ALS = Prob(AreaMeso_ALS,[CombVerMo],[1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0])
f_SatContMoist = Prob(SatContMoist,[],[0.15,0.2,0.4,0.25])
f_MorningBound = Prob(MorningBound,[],[0.5,0.35,0.15])
f_RHRatio = Prob(RHRatio,[Scenario],[0.05,0.5,0.45,0.1,0.5,0.4,0.4,0.15,0.45,0.2,0.45,0.35,0.8,0.05,0.15,0.0,0.0,1.0,0.6,0.0,0.4,0.0,0.7,0.3,0.1,0.7,0.2,0.4,0.4,0.2,0.15,0.45,0.4])
f_WindAloft = Prob(WindAloft,[Scenario],[0.0,0.95,0.01,0.04,0.2,0.3,0.2,0.3,0.05,0.09,0.59,0.27,0.03,0.32,0.42,0.23,0.07,0.66,0.02,0.25,0.5,0.0,0.0,0.5,0.25,0.3,0.25,0.2,0.2,0.14,0.43,0.23,0.2,0.41,0.1,0.29,0.96,0.0,0.0,0.04,0.03,0.08,0.33,0.56])
f_LowLLapse = Prob(LowLLapse,[Scenario],[0.04,0.25,0.35,0.36,0.07,0.31,0.31,0.31,0.35,0.47,0.14,0.04,0.4,0.4,0.13,0.07,0.45,0.35,0.15,0.05,0.01,0.35,0.45,0.19,0.78,0.19,0.03,0.0,0.0,0.02,0.33,0.65,0.22,0.4,0.3,0.08,0.13,0.4,0.35,0.12,0.09,0.4,0.33,0.18])
f_AMDewptCalPl = Prob(AMDewptCalPl,[],[0.3,0.25,0.45])
f_SubjVertMo = Prob(SubjVertMo,[],[0.15,0.15,0.5,0.2])
f_OutflowFrMt = Prob(OutflowFrMt,[InsInMt,WndHodograph],[1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.4,0.1,0.15,0.4,0.45,0.35,0.6,0.05,0.8,0.19,0.01,0.05,0.45,0.5,0.01,0.15,0.84,0.1,0.25,0.65,0.6,0.3,0.1])
f_AreaMoDryAir = Prob(AreaMoDryAir,[AreaMeso_ALS,CombMoisture],[0.99,0.01,0.0,0.0,0.7,0.29,0.01,0.0,0.2,0.55,0.24,0.01,0.0,0.25,0.55,0.2,0.8,0.2,0.0,0.0,0.35,0.55,0.1,0.0,0.01,0.39,0.55,0.05,0.0,0.02,0.43,0.55,0.7,0.29,0.01,0.0,0.2,0.6,0.2,0.0,0.01,0.09,0.8,0.1,0.0,0.0,0.3,0.7,0.2,0.74,0.06,0.0,0.05,0.4,0.45,0.1,0.0,0.05,0.5,0.45,0.0,0.0,0.01,0.99])
f_MorningCIN = Prob(MorningCIN,[],[0.15,0.57,0.2,0.08])
f_TempDis = Prob(TempDis,[Scenario],[0.13,0.15,0.1,0.62,0.15,0.15,0.25,0.45,0.12,0.1,0.35,0.43,0.1,0.15,0.4,0.35,0.04,0.04,0.82,0.1,0.05,0.12,0.75,0.08,0.03,0.03,0.84,0.1,0.05,0.4,0.5,0.05,0.8,0.19,0.0,0.01,0.1,0.05,0.4,0.45,0.2,0.3,0.3,0.2])
f_InsSclInScen = Prob(InsSclInScen,[InsChange,AMInsWliScen],[1.0,0.0,0.0,0.6,0.4,0.0,0.25,0.35,0.4,0.9,0.1,0.0,0.15,0.7,0.15,0.0,0.1,0.9,0.4,0.35,0.25,0.0,0.4,0.6,0.0,0.0,1.0])
f_WindFieldPln = Prob(WindFieldPln,[Scenario],[0.05,0.6,0.02,0.1,0.23,0.0,0.08,0.6,0.02,0.1,0.2,0.0,0.1,0.0,0.75,0.0,0.0,0.15,0.1,0.15,0.2,0.05,0.3,0.2,0.43,0.1,0.15,0.06,0.06,0.2,0.6,0.07,0.01,0.12,0.2,0.0,0.25,0.01,0.3,0.01,0.03,0.4,0.04,0.02,0.04,0.8,0.1,0.0,0.2,0.3,0.05,0.37,0.07,0.01,0.6,0.08,0.07,0.03,0.2,0.02,0.1,0.05,0.1,0.05,0.2,0.5])
f_CurPropConv = Prob(CurPropConv,[LatestCIN,LLIW],[0.7,0.28,0.02,0.0,0.1,0.5,0.3,0.1,0.01,0.14,0.35,0.5,0.0,0.02,0.18,0.8,0.9,0.09,0.01,0.0,0.65,0.25,0.09,0.01,0.25,0.35,0.3,0.1,0.01,0.15,0.33,0.51,0.95,0.05,0.0,0.0,0.75,0.23,0.02,0.0,0.4,0.4,0.18,0.02,0.2,0.3,0.35,0.15,1.0,0.0,0.0,0.0,0.95,0.05,0.0,0.0,0.75,0.2,0.05,0.0,0.5,0.35,0.1,0.05])
Hailfinder_Belief_Net = Belief_network(
    vars=[ScnRelPlFcst,AMInsWliScen,SfcWndShfDis,InsInMt,AMCINInScen,PlainsFcst,CombClouds,LIfr12ZDENSd,CombMoisture,AMInstabMt,CldShadeOth,N0_7muVerMo,LLIW,ScenRelAMIns,VISCloudCov,ScenRelAMCIN,MidLLapse,MvmtFeatures,CapInScen,CldShadeConv,IRCloudCover,CapChange,QGVertMotion,LoLevMoistAd,Scenario,MountainFcst,CombVerMo,Boundaries,MeanRH,Dewpoints,InsChange,N34StarFcst,SynForcng,CompPlFcst,Date,WndHodograph,ScenRel3_4,R5Fcst,LatestCIN,WindFieldMt,RaoContMoist,AreaMeso_ALS,SatContMoist,MorningBound,RHRatio,WindAloft,LowLLapse,AMDewptCalPl,SubjVertMo,OutflowFrMt,AreaMoDryAir,MorningCIN,TempDis,InsSclInScen,WindFieldPln,CurPropConv],
    factors=[f_ScnRelPlFcst,f_AMInsWliScen,f_SfcWndShfDis,f_InsInMt,f_AMCINInScen,f_PlainsFcst,f_CombClouds,f_LIfr12ZDENSd,f_CombMoisture,f_AMInstabMt,f_CldShadeOth,f_N0_7muVerMo,f_LLIW,f_ScenRelAMIns,f_VISCloudCov,f_ScenRelAMCIN,f_MidLLapse,f_MvmtFeatures,f_CapInScen,f_CldShadeConv,f_IRCloudCover,f_CapChange,f_QGVertMotion,f_LoLevMoistAd,f_Scenario,f_MountainFcst,f_CombVerMo,f_Boundaries,f_MeanRH,f_Dewpoints,f_InsChange,f_N34StarFcst,f_SynForcng,f_CompPlFcst,f_Date,f_WndHodograph,f_ScenRel3_4,f_R5Fcst,f_LatestCIN,f_WindFieldMt,f_RaoContMoist,f_AreaMeso_ALS,f_SatContMoist,f_MorningBound,f_RHRatio,f_WindAloft,f_LowLLapse,f_AMDewptCalPl,f_SubjVertMo,f_OutflowFrMt,f_AreaMoDryAir,f_MorningCIN,f_TempDis,f_InsSclInScen,f_WindFieldPln,f_CurPropConv],
    positions=[])

