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

bn2 = Belief_network([Al, Fi, Le, Re, Sm, Ta], [
                     f_ta, f_fi, f_sm, f_al, f_lv, f_re])

Season = Variable("Season", ["summer", "winter"])
Sprinkler = Variable("Sprinkler", ["on", "off"])
Rained = Variable("Rained", boolean)
Grass_wet = Variable("Grass wet", boolean)
Grass_shiny = Variable("Grass shiny", boolean)
Shoes_wet = Variable("Shoes wet", boolean)

f_season = Prob(Season, [], [0.5, 0.5])
f_sprinkler = Prob(Sprinkler, [Season], [0.9, 0.1, 0.05, 0.95])
f_rained = Prob(Rained, [Season], [0.7, 0.3, 0.2, 0.8])
f_wet = Prob(Grass_wet, [Sprinkler, Rained], [
             1, 0, 0.1, 0.9, 0.2, 0.8, 0.02, 0.98])
f_shiny = Prob(Grass_shiny, [Grass_wet], [0.95, 0.05, 0.3, 0.7])
f_shoes = Prob(Shoes_wet, [Grass_wet], [0.92, 0.08, 0.35, 0.65])

bn3 = Belief_network([Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet], [
                     f_season, f_sprinkler, f_rained, f_wet, f_shiny, f_shoes])

# An example with domain length > 2

C100 = Variable("C100", ["c103", "c110", "c121"])
M200 = Variable("M200", ["m200", "m221"])
C200 = Variable("C200", ["c210", "c221"])
C300 = Variable("C300", ["c310", "c313", "c314", "c320"])

f_c100 = Prob(C100, [], [0.2, 0.4, 0.4])
f_m200 = Prob(M200, [], [0.5, 0.5])
f_c200 = Prob(C200, [C100], [0.5, 0.5, 0.8, 0.2, 0.2, 0.8])
f_c300 = Prob(C300, [C200, M200], [0.25, 0.25, 0.25, 0.25, 0.30,
                                   0.30, 0.10, 0.30, 0.20, 0.20, 0.40, 0.20, 0.10, 0.10, 0.70, 0.10])

bn4 = Belief_network([C100, M200, C200, C300], [
                     f_c100, f_m200, f_c200, f_c300])

Fire = Variable('Fire', ['T', 'F'])
Report = Variable('Report', ['T', 'F'])
Smoke = Variable('Smoke', ['T', 'F'])
Tampering = Variable('Tampering', ['T', 'F'])
Leaving = Variable('Leaving', ['T', 'F'])
Alarm = Variable('Alarm', ['T', 'F'])
f_fire = Prob(Fire,[],[0.01,0.99])
f_report = Prob(Report,[Leaving],[0.75,0.25,0.01,0.99])
f_smoke = Prob(Smoke,[Fire],[0.9,0.1,0.01,0.99])
f_tampering = Prob(Tampering,[],[0.02,0.98])
f_leaving = Prob(Leaving,[Alarm],[0.88,0.12,0.0,1.0])
f_alarm = Prob(Alarm,[Tampering,Fire],[0.5,0.5,0.85,0.15,0.99,0.01,0.0,1.0])

Fire_Alarm_Belief_Network = Belief_network(
                                           vars=[Fire, Report, Smoke, Tampering, Leaving, Alarm],
                                           factors=[f_fire, f_report, f_smoke, f_tampering, f_leaving, f_alarm],
                                           positions=[])
Fever = Variable('Fever', ['T', 'F'])
Sore_throat = Variable('Sore_throat', ['T', 'F'])
Bronchitis = Variable('Bronchitis', ['T', 'F'])
Wheezing = Variable('Wheezing', ['T', 'F'])
Influenza = Variable('Influenza', ['T', 'F'])
Coughing = Variable('Coughing', ['T', 'F'])
Smokes = Variable('Smokes', ['T', 'F'])
f_fever = Prob(Fever,[Influenza],[0.9,0.1,0.05,0.95])
f_sore_throat = Prob(Sore_throat,[Influenza],[0.3,0.7,0.001,0.999])
f_bronchitis = Prob(Bronchitis,[Influenza,Smokes],[0.99,0.01,0.9,0.1,0.7,0.3,1.0E-4,0.9999])
f_wheezing = Prob(Wheezing,[Bronchitis],[0.6,0.4,0.001,0.999])
f_influenza = Prob(Influenza,[],[0.05,0.95])
f_coughing = Prob(Coughing,[Bronchitis],[0.8,0.2,0.07,0.93])
f_smokes = Prob(Smokes,[],[0.2,0.8])

Simple_Diagnostic_Example = Belief_network(
                                           vars=[Fever, Sore_throat, Bronchitis, Wheezing, Influenza, Coughing, Smokes],
                                           factors=[f_fever, f_sore_throat, f_bronchitis, f_wheezing, f_influenza, f_coughing, f_smokes],
                                           positions=[])
F = Variable('F', ['T', 'F'])
A = Variable('A', ['T', 'F'])
D = Variable('D', ['T', 'F'])
C = Variable('C', ['T', 'F'])
E = Variable('E', ['T', 'F'])
B = Variable('B', ['T', 'F'])
G = Variable('G', ['T', 'F'])
f_f = Prob(F,[C],[0.45,0.55,0.85,0.15])
f_a = Prob(A,[B],[0.88,0.12,0.38,0.62])
f_d = Prob(D,[E],[0.04,0.96,0.84,0.16])
f_c = Prob(C,[B,D],[0.93,0.07,0.33,0.67,0.53,0.47,0.83,0.17])
f_e = Prob(E,[],[0.91,0.09])
f_b = Prob(B,[],[0.7,0.3])
f_g = Prob(G,[F],[0.26,0.74,0.96,0.04])

Simple_graph = Belief_network(
                              vars=[F, A, D, C, E, B, G],
                              factors=[f_f, f_a, f_d, f_c, f_e, f_b, f_g],
                              positions=[])
F = Variable('F', ['T', 'F'])
A = Variable('A', ['T', 'F'])
D = Variable('D', ['T', 'F'])
H = Variable('H', ['T', 'F'])
C = Variable('C', ['T', 'F'])
I = Variable('I', ['T', 'F'])
J = Variable('J', ['T', 'F'])
E = Variable('E', ['T', 'F'])
B = Variable('B', ['T', 'F'])
G = Variable('G', ['T', 'F'])
f_f = Prob(F,[E,G],[0.9,0.1,0.2,0.8,0.4,0.6,0.7,0.3])
f_a = Prob(A,[B],[0.7,0.3,0.4,0.6])
f_d = Prob(D,[B,E],[0.3,0.7,0.5,0.5,0.2,0.8,0.9,0.1])
f_h = Prob(H,[G,J],[0.8,0.2,0.3,0.7,0.5,0.5,0.1,0.9])
f_c = Prob(C,[],[0.5,0.5])
f_i = Prob(I,[H],[0.8,0.2,0.1,0.9])
f_j = Prob(J,[],[0.3,0.7])
f_e = Prob(E,[C],[0.7,0.3,0.2,0.8])
f_b = Prob(B,[C],[0.9,0.1,0.4,0.6])
f_g = Prob(G,[],[0.2,0.8])

Conditional_Independence_Quiz = Belief_network(
                                               vars=[F, A, D, H, C, I, J, E, B, G],
                                               factors=[f_f, f_a, f_d, f_h, f_c, f_i, f_j, f_e, f_b, f_g],
                                               positions=[])
Spark_timing = Variable('Spark_timing', ['good', 'bad', 'very_bad'])
Headlights = Variable('Headlights', ['bright', 'dim', 'off'])
Starter_motor_ok = Variable('Starter_motor_ok', ['T', 'F'])
Fuel_system_ok = Variable('Fuel_system_ok', ['T', 'F'])
Air_filter_clean = Variable('Air_filter_clean', ['T', 'F'])
Battery_voltage = Variable('Battery_voltage', ['strong', 'weak', 'dead'])
Starter_system_ok = Variable('Starter_system_ok', ['T', 'F'])
Car_starts = Variable('Car_starts', ['T', 'F'])
Distributer_ok = Variable('Distributer_ok', ['T', 'F'])
Spark_adequate = Variable('Spark_adequate', ['T', 'F'])
Car_cranks = Variable('Car_cranks', ['T', 'F'])
Charging_system_ok = Variable('Charging_system_ok', ['T', 'F'])
Air_system_ok = Variable('Air_system_ok', ['T', 'F'])
Spark_plugs = Variable('Spark_plugs', ['okay', 'too_wide', 'fouled'])
Alternator_ok = Variable('Alternator_ok', ['T', 'F'])
Voltage_at_plug = Variable('Voltage_at_plug', ['strong', 'weak', 'dead'])
Spark_quality = Variable('Spark_quality', ['good', 'bad', 'very_bad'])
Main_fuse_ok = Variable('Main_fuse_ok', ['T', 'F'])
Battery_age = Variable('Battery_age', ['new', 'old', 'very_old'])
f_spark_timing = Prob(Spark_timing,[Distributer_ok],[0.97,0.02,0.01,0.2,0.3,0.5])
f_headlights = Prob(Headlights,[Voltage_at_plug],[0.98,0.015,0.005,0.05,0.9,0.05,0.0,0.0,1.0])
f_starter_motor_ok = Prob(Starter_motor_ok,[],[0.992,0.008])
f_fuel_system_ok = Prob(Fuel_system_ok,[],[0.9,0.1])
f_air_filter_clean = Prob(Air_filter_clean,[],[0.9,0.1])
f_battery_voltage = Prob(Battery_voltage,[Charging_system_ok,Battery_age],[0.999,8.0E-4,2.0E-4,0.99,0.008,0.002,0.6,0.3,0.1,0.8,0.15,0.05,0.05,0.3,0.65,0.002,0.1,0.898])
f_starter_system_ok = Prob(Starter_system_ok,[Battery_voltage,Main_fuse_ok,Starter_motor_ok],[0.998,0.002,0.0,1.0,0.0,1.0,0.0,1.0,0.72,0.28,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_car_starts = Prob(Car_starts,[Car_cranks,Fuel_system_ok,Air_system_ok,Spark_adequate],[1.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_distributer_ok = Prob(Distributer_ok,[],[0.99,0.01])
f_spark_adequate = Prob(Spark_adequate,[Spark_timing,Spark_quality],[0.99,0.01,0.5,0.5,0.1,0.9,0.5,0.5,0.05,0.95,0.01,0.99,0.1,0.9,0.01,0.99,0.0,1.0])
f_car_cranks = Prob(Car_cranks,[Starter_system_ok],[0.98,0.02,0.0,1.0])
f_charging_system_ok = Prob(Charging_system_ok,[Alternator_ok],[0.995,0.005,0.0,1.0])
f_air_system_ok = Prob(Air_system_ok,[Air_filter_clean],[0.9,0.1,0.3,0.7])
f_spark_plugs = Prob(Spark_plugs,[],[0.99,0.003,0.007])
f_alternator_ok = Prob(Alternator_ok,[],[0.9997,3.0E-4])
f_voltage_at_plug = Prob(Voltage_at_plug,[Battery_voltage,Main_fuse_ok,Distributer_ok],[0.98,0.015,0.005,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.1,0.8,0.1,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0])
f_spark_quality = Prob(Spark_quality,[Voltage_at_plug,Spark_plugs],[1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0,0.2,0.8,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0])
f_main_fuse_ok = Prob(Main_fuse_ok,[],[0.999,0.001])
f_battery_age = Prob(Battery_age,[],[0.4,0.4,0.2])

Car_Starting_Problem = Belief_network(
                                      vars=[Spark_timing, Headlights, Starter_motor_ok, Fuel_system_ok, Air_filter_clean, Battery_voltage, Starter_system_ok, Car_starts, Distributer_ok, Spark_adequate, Car_cranks, Charging_system_ok, Air_system_ok, Spark_plugs, Alternator_ok, Voltage_at_plug, Spark_quality, Main_fuse_ok, Battery_age],
                                      factors=[f_spark_timing, f_headlights, f_starter_motor_ok, f_fuel_system_ok, f_air_filter_clean, f_battery_voltage, f_starter_system_ok, f_car_starts, f_distributer_ok, f_spark_adequate, f_car_cranks, f_charging_system_ok, f_air_system_ok, f_spark_plugs, f_alternator_ok, f_voltage_at_plug, f_spark_quality, f_main_fuse_ok, f_battery_age],
                                      positions=[])
W3 = Variable('W3', ['live', 'dead'])
W1 = Variable('W1', ['live', 'dead'])
Cb1_st = Variable('Cb1_st', ['on', 'off'])
L1_lit = Variable('L1_lit', ['T', 'F'])
S3_st = Variable('S3_st', ['ok', 'upside_down', 'short', 'intermittent', 'broken'])
S2_st = Variable('S2_st', ['ok', 'upside_down', 'short', 'intermittent', 'broken'])
Cb2_st = Variable('Cb2_st', ['on', 'off'])
Outside_power = Variable('Outside_power', ['on', 'off'])
W2 = Variable('W2', ['live', 'dead'])
S1_pos = Variable('S1_pos', ['up', 'down'])
W4 = Variable('W4', ['live', 'dead'])
S1_st = Variable('S1_st', ['ok', 'upside_down', 'short', 'intermittent', 'broken'])
P2 = Variable('P2', ['T', 'F'])
P1 = Variable('P1', ['T', 'F'])
W0 = Variable('W0', ['live', 'dead'])
W6 = Variable('W6', ['live', 'dead'])
S3_pos = Variable('S3_pos', ['up', 'down'])
S2_pos = Variable('S2_pos', ['up', 'down'])
L1_st = Variable('L1_st', ['ok', 'intermittent', 'broken'])
L2_lit = Variable('L2_lit', ['T', 'F'])
L2_st = Variable('L2_st', ['ok', 'intermittent', 'broken'])
f_w3 = Prob(W3,[Outside_power,Cb1_st],[1.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_w1 = Prob(W1,[W3,S1_st,S1_pos],[1.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,0.6,0.4,0.4,0.6,0.4,0.6,0.01,0.99,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_cb1_st = Prob(Cb1_st,[],[0.999,0.001])
f_l1_lit = Prob(L1_lit,[W0,L1_st],[1.0,0.0,0.7,0.3,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_s3_st = Prob(S3_st,[],[0.9,0.01,0.04,0.03,0.02])
f_s2_st = Prob(S2_st,[],[0.9,0.01,0.04,0.03,0.02])
f_cb2_st = Prob(Cb2_st,[],[0.999,0.001])
f_outside_power = Prob(Outside_power,[],[0.98,0.02])
f_w2 = Prob(W2,[W3,S1_st,S1_pos],[0.0,1.0,1.0,0.0,1.0,0.0,0.0,1.0,0.4,0.6,0.4,0.6,0.2,0.8,0.2,0.8,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_s1_pos = Prob(S1_pos,[],[0.5,0.5])
f_w4 = Prob(W4,[W3,S3_pos,S3_st],[1.0,0.0,0.0,1.0,0.4,0.6,0.2,0.8,0.0,1.0,0.0,1.0,1.0,0.0,0.4,0.6,0.2,0.8,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_s1_st = Prob(S1_st,[],[0.9,0.01,0.04,0.03,0.02])
f_p2 = Prob(P2,[W6],[1.0,0.0,0.0,1.0])
f_p1 = Prob(P1,[W3],[1.0,0.0,0.0,1.0])
f_w0 = Prob(W0,[W1,W2,S2_st,S2_pos],[1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,0.8,0.2,0.8,0.2,0.4,0.6,0.4,0.6,0.0,1.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,0.4,0.6,0.4,0.6,0.2,0.8,0.2,0.8,0.0,1.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,0.0,0.0,1.0,0.4,0.6,0.4,0.6,0.2,0.8,0.2,0.8,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_w6 = Prob(W6,[Outside_power,Cb2_st],[1.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_s3_pos = Prob(S3_pos,[],[0.8,0.2])
f_s2_pos = Prob(S2_pos,[],[0.5,0.5])
f_l1_st = Prob(L1_st,[],[0.9,0.07,0.03])
f_l2_lit = Prob(L2_lit,[W4,L2_st],[1.0,0.0,0.6,0.4,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])
f_l2_st = Prob(L2_st,[],[0.9,0.03,0.07])

Electrical_Diagnosis_Problem = Belief_network(
                                              vars=[W3, W1, Cb1_st, L1_lit, S3_st, S2_st, Cb2_st, Outside_power, W2, S1_pos, W4, S1_st, P2, P1, W0, W6, S3_pos, S2_pos, L1_st, L2_lit, L2_st],
                                              factors=[f_w3, f_w1, f_cb1_st, f_l1_lit, f_s3_st, f_s2_st, f_cb2_st, f_outside_power, f_w2, f_s1_pos, f_w4, f_s1_st, f_p2, f_p1, f_w0, f_w6, f_s3_pos, f_s2_pos, f_l1_st, f_l2_lit, f_l2_st],
                                              positions=[])
Disconnect = Variable('Disconnect', ['TRUE', 'FALSE'])
Expco2 = Variable('Expco2', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
Hr = Variable('Hr', ['LOW', 'NORMAL', 'HIGH'])
Kinkedtube = Variable('Kinkedtube', ['TRUE', 'FALSE'])
Pulmembolus = Variable('Pulmembolus', ['TRUE', 'FALSE'])
Shunt = Variable('Shunt', ['NORMAL', 'HIGH'])
Artco2 = Variable('Artco2', ['LOW', 'NORMAL', 'HIGH'])
Anaphylaxis = Variable('Anaphylaxis', ['TRUE', 'FALSE'])
Intubation = Variable('Intubation', ['NORMAL', 'ESOPHAGEAL', 'ONESIDED'])
Bp = Variable('Bp', ['LOW', 'NORMAL', 'HIGH'])
Pap = Variable('Pap', ['LOW', 'NORMAL', 'HIGH'])
Lvedvolume = Variable('Lvedvolume', ['LOW', 'NORMAL', 'HIGH'])
Catechol = Variable('Catechol', ['NORMAL', 'HIGH'])
Errlowoutput = Variable('Errlowoutput', ['TRUE', 'FALSE'])
Hrbp = Variable('Hrbp', ['LOW', 'NORMAL', 'HIGH'])
Fio2 = Variable('Fio2', ['LOW', 'NORMAL'])
Tpr = Variable('Tpr', ['LOW', 'NORMAL', 'HIGH'])
Sao2 = Variable('Sao2', ['LOW', 'NORMAL', 'HIGH'])
Ventmach = Variable('Ventmach', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
Ventlung = Variable('Ventlung', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
Hypovolemia = Variable('Hypovolemia', ['TRUE', 'FALSE'])
Errcauter = Variable('Errcauter', ['TRUE', 'FALSE'])
Ventalv = Variable('Ventalv', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
Hrekg = Variable('Hrekg', ['LOW', 'NORMAL', 'HIGH'])
Hrsat = Variable('Hrsat', ['LOW', 'NORMAL', 'HIGH'])
Venttube = Variable('Venttube', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
Pvsat = Variable('Pvsat', ['LOW', 'NORMAL', 'HIGH'])
Insuffanesth = Variable('Insuffanesth', ['TRUE', 'FALSE'])
History = Variable('History', ['TRUE', 'FALSE'])
Strokevolume = Variable('Strokevolume', ['LOW', 'NORMAL', 'HIGH'])
Minvol = Variable('Minvol', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
Cvp = Variable('Cvp', ['LOW', 'NORMAL', 'HIGH'])
Pcwp = Variable('Pcwp', ['LOW', 'NORMAL', 'HIGH'])
Press = Variable('Press', ['ZERO', 'LOW', 'NORMAL', 'HIGH'])
Lvfailure = Variable('Lvfailure', ['TRUE', 'FALSE'])
Co = Variable('Co', ['LOW', 'NORMAL', 'HIGH'])
Minvolset = Variable('Minvolset', ['LOW', 'NORMAL', 'HIGH'])
f_disconnect = Prob(Disconnect,[],[0.1,0.9])
f_expco2 = Prob(Expco2,[Ventlung,Artco2],[0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97])
f_hr = Prob(Hr,[Catechol],[0.05,0.9,0.05,0.01,0.09,0.9])
f_kinkedtube = Prob(Kinkedtube,[],[0.04,0.96])
f_pulmembolus = Prob(Pulmembolus,[],[0.01,0.99])
f_shunt = Prob(Shunt,[Pulmembolus,Intubation],[0.1,0.9,0.01,0.99,0.95,0.05,0.1,0.9,0.95,0.05,0.05,0.95])
f_artco2 = Prob(Artco2,[Ventalv],[0.01,0.01,0.98,0.01,0.01,0.98,0.04,0.92,0.04,0.9,0.09,0.01])
f_anaphylaxis = Prob(Anaphylaxis,[],[0.01,0.99])
f_intubation = Prob(Intubation,[],[0.92,0.03,0.05])
f_bp = Prob(Bp,[Tpr,Co],[0.98,0.01,0.01,0.98,0.01,0.01,0.3,0.6,0.1,0.98,0.01,0.01,0.1,0.85,0.05,0.05,0.4,0.55,0.9,0.09,0.01,0.05,0.2,0.75,0.01,0.09,0.9])
f_pap = Prob(Pap,[Pulmembolus],[0.01,0.19,0.8,0.05,0.9,0.05])
f_lvedvolume = Prob(Lvedvolume,[Hypovolemia,Lvfailure],[0.95,0.04,0.01,0.98,0.01,0.01,0.01,0.09,0.9,0.05,0.9,0.05])
f_catechol = Prob(Catechol,[Insuffanesth,Tpr,Sao2,Artco2],[0.01,0.99,0.01,0.99,0.7,0.3,0.01,0.99,0.05,0.95,0.7,0.3,0.01,0.99,0.05,0.95,0.7,0.3,0.01,0.99,0.01,0.99,0.7,0.3,0.01,0.99,0.05,0.95,0.7,0.3,0.01,0.99,0.05,0.95,0.7,0.3,0.01,0.99,0.01,0.99,0.1,0.9,0.01,0.99,0.01,0.99,0.1,0.9,0.01,0.99,0.01,0.99,0.1,0.9,0.01,0.99,0.05,0.95,0.95,0.05,0.01,0.99,0.05,0.95,0.95,0.05,0.05,0.95,0.05,0.95,0.95,0.05,0.01,0.99,0.05,0.95,0.99,0.01,0.01,0.99,0.05,0.95,0.99,0.01,0.05,0.95,0.05,0.95,0.99,0.01,0.01,0.99,0.01,0.99,0.3,0.7,0.01,0.99,0.01,0.99,0.3,0.7,0.01,0.99,0.01,0.99,0.3,0.7])
f_errlowoutput = Prob(Errlowoutput,[],[0.05,0.95])
f_hrbp = Prob(Hrbp,[Errlowoutput,Hr],[0.98,0.01,0.01,0.4,0.59,0.01,0.3,0.4,0.3,0.98,0.01,0.01,0.01,0.98,0.01,0.01,0.01,0.98])
f_fio2 = Prob(Fio2,[],[0.05,0.95])
f_tpr = Prob(Tpr,[Anaphylaxis],[0.98,0.01,0.01,0.3,0.4,0.3])
f_sao2 = Prob(Sao2,[Pvsat,Shunt],[0.98,0.01,0.01,0.01,0.98,0.01,0.01,0.01,0.98,0.98,0.01,0.01,0.98,0.01,0.01,0.69,0.3,0.01])
f_ventmach = Prob(Ventmach,[Minvolset],[0.05,0.93,0.01,0.01,0.05,0.01,0.93,0.01,0.05,0.01,0.01,0.93])
f_ventlung = Prob(Ventlung,[Kinkedtube,Intubation,Venttube],[0.97,0.01,0.01,0.01,0.95,0.03,0.01,0.01,0.4,0.58,0.01,0.01,0.3,0.68,0.01,0.01,0.97,0.01,0.01,0.01,0.95,0.03,0.01,0.01,0.5,0.48,0.01,0.01,0.3,0.68,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97])
f_hypovolemia = Prob(Hypovolemia,[],[0.2,0.8])
f_errcauter = Prob(Errcauter,[],[0.1,0.9])
f_ventalv = Prob(Ventalv,[Intubation,Ventlung],[0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.03,0.95,0.01,0.01,0.01,0.94,0.04,0.01,0.01,0.88,0.1,0.01])
f_hrekg = Prob(Hrekg,[Errcauter,Hr],[0.33333334,0.33333333,0.33333333,0.33333334,0.33333333,0.33333333,0.33333334,0.33333333,0.33333333,0.98,0.01,0.01,0.01,0.98,0.01,0.01,0.01,0.98])
f_hrsat = Prob(Hrsat,[Errcauter,Hr],[0.33333334,0.33333333,0.33333333,0.33333334,0.33333333,0.33333333,0.33333334,0.33333333,0.33333333,0.98,0.01,0.01,0.01,0.98,0.01,0.01,0.01,0.98])
f_venttube = Prob(Venttube,[Disconnect,Ventmach],[0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97])
f_pvsat = Prob(Pvsat,[Fio2,Ventalv],[1.0,0.0,0.0,0.99,0.01,0.0,0.95,0.04,0.01,0.95,0.04,0.01,1.0,0.0,0.0,0.95,0.04,0.01,0.01,0.95,0.04,0.01,0.01,0.98])
f_insuffanesth = Prob(Insuffanesth,[],[0.1,0.9])
f_history = Prob(History,[Lvfailure],[0.9,0.1,0.01,0.99])
f_strokevolume = Prob(Strokevolume,[Hypovolemia,Lvfailure],[0.98,0.01,0.01,0.95,0.04,0.01,0.5,0.49,0.01,0.05,0.9,0.05])
f_minvol = Prob(Minvol,[Intubation,Ventlung],[0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.6,0.38,0.01,0.01,0.5,0.48,0.01,0.01,0.5,0.48,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97])
f_cvp = Prob(Cvp,[Lvedvolume],[0.95,0.04,0.01,0.04,0.95,0.01,0.01,0.29,0.7])
f_pcwp = Prob(Pcwp,[Lvedvolume],[0.95,0.04,0.01,0.04,0.95,0.01,0.01,0.04,0.95])
f_press = Prob(Press,[Kinkedtube,Intubation,Venttube],[0.97,0.01,0.01,0.01,0.01,0.3,0.49,0.2,0.01,0.01,0.08,0.9,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.01,0.29,0.3,0.4,0.01,0.01,0.08,0.9,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.4,0.58,0.01,0.01,0.2,0.75,0.04,0.01,0.2,0.7,0.09,0.01,0.97,0.01,0.01,0.01,0.1,0.84,0.05,0.01,0.05,0.25,0.25,0.45,0.01,0.15,0.25,0.59,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.97,0.01,0.01,0.01,0.01,0.9,0.08,0.01,0.01,0.01,0.38,0.6,0.01,0.01,0.01,0.97])
f_lvfailure = Prob(Lvfailure,[],[0.05,0.95])
f_co = Prob(Co,[Strokevolume,Hr],[0.98,0.01,0.01,0.95,0.04,0.01,0.3,0.69,0.01,0.95,0.04,0.01,0.04,0.95,0.01,0.01,0.3,0.69,0.8,0.19,0.01,0.01,0.04,0.95,0.01,0.01,0.98])
f_minvolset = Prob(Minvolset,[],[0.05,0.9,0.05])

Diagnosis_Problem = Belief_network(
                                   vars=[Disconnect, Expco2, Hr, Kinkedtube, Pulmembolus, Shunt, Artco2, Anaphylaxis, Intubation, Bp, Pap, Lvedvolume, Catechol, Errlowoutput, Hrbp, Fio2, Tpr, Sao2, Ventmach, Ventlung, Hypovolemia, Errcauter, Ventalv, Hrekg, Hrsat, Venttube, Pvsat, Insuffanesth, History, Strokevolume, Minvol, Cvp, Pcwp, Press, Lvfailure, Co, Minvolset],
                                   factors=[f_disconnect, f_expco2, f_hr, f_kinkedtube, f_pulmembolus, f_shunt, f_artco2, f_anaphylaxis, f_intubation, f_bp, f_pap, f_lvedvolume, f_catechol, f_errlowoutput, f_hrbp, f_fio2, f_tpr, f_sao2, f_ventmach, f_ventlung, f_hypovolemia, f_errcauter, f_ventalv, f_hrekg, f_hrsat, f_venttube, f_pvsat, f_insuffanesth, f_history, f_strokevolume, f_minvol, f_cvp, f_pcwp, f_press, f_lvfailure, f_co, f_minvolset],
                                   positions=[])
Satcontmoist = Variable('Satcontmoist', ['VeryWet', 'Wet', 'Neutral', 'Dry'])
Boundaries = Variable('Boundaries', ['None', 'Weak', 'Strong'])
Amdewptcalpl = Variable('Amdewptcalpl', ['Instability', 'Neutral', 'Stability'])
Midllapse = Variable('Midllapse', ['CloseToDryAd', 'Steep', 'ModerateOrLe'])
Inssclinscen = Variable('Inssclinscen', ['LessUnstable', 'Average', 'MoreUnstable'])
Insinmt = Variable('Insinmt', ['None', 'Weak', 'Strong'])
N34starfcst = Variable('N34starfcst', ['XNIL', 'SIG', 'SVR'])
Amcininscen = Variable('Amcininscen', ['LessThanAve', 'Average', 'MoreThanAve'])
Windfieldmt = Variable('Windfieldmt', ['Westerly', 'LVorOther'])
Combmoisture = Variable('Combmoisture', ['VeryWet', 'Wet', 'Neutral', 'Dry'])
Aminswliscen = Variable('Aminswliscen', ['LessUnstable', 'Average', 'MoreUnstable'])
Sfcwndshfdis = Variable('Sfcwndshfdis', ['DenvCyclone', 'E_W_N', 'E_W_S', 'MovingFtorOt', 'DryLine', 'None', 'Other'])
Capinscen = Variable('Capinscen', ['LessThanAve', 'Average', 'MoreThanAve'])
Scenrel3_4 = Variable('Scenrel3_4', ['ACEFK', 'B', 'D', 'GJ', 'HI'])
Scnrelplfcst = Variable('Scnrelplfcst', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'])
Windfieldpln = Variable('Windfieldpln', ['LV', 'DenvCyclone', 'LongAnticyc', 'E_NE', 'SEQuad', 'WidespdDnsl'])
Aminstabmt = Variable('Aminstabmt', ['None', 'Weak', 'Strong'])
Wndhodograph = Variable('Wndhodograph', ['DCVZFavor', 'StrongWest', 'Westerly', 'Other'])
Scenario = Variable('Scenario', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'])
Curpropconv = Variable('Curpropconv', ['None', 'Slight', 'Moderate', 'Strong'])
Capchange = Variable('Capchange', ['Decreasing', 'LittleChange', 'Increasing'])
Morningcin = Variable('Morningcin', ['None', 'PartInhibit', 'Stifling', 'TotalInhibit'])
R5fcst = Variable('R5fcst', ['XNIL', 'SIG', 'SVR'])
Inschange = Variable('Inschange', ['Decreasing', 'LittleChange', 'Increasing'])
Windaloft = Variable('Windaloft', ['LV', 'SWQuad', 'NWQuad', 'AllElse'])
Lolevmoistad = Variable('Lolevmoistad', ['StrongPos', 'WeakPos', 'Neutral', 'Negative'])
Date = Variable('Date', ['May15_Jun14', 'Jun15_Jul1', 'Jul2_Jul15', 'Jul16_Aug10', 'Aug11_Aug20', 'Aug20_Sep15'])
Outflowfrmt = Variable('Outflowfrmt', ['None', 'Weak', 'Strong'])
Scenrelamins = Variable('Scenrelamins', ['ABI', 'CDEJ', 'F', 'G', 'H', 'K'])
Combvermo = Variable('Combvermo', ['StrongUp', 'WeakUp', 'Neutral', 'Down'])
Cldshadeconv = Variable('Cldshadeconv', ['None', 'Some', 'Marked'])
Latestcin = Variable('Latestcin', ['None', 'PartInhibit', 'Stifling', 'TotalInhibit'])
Lliw = Variable('Lliw', ['Unfavorable', 'Weak', 'Moderate', 'Strong'])
Synforcng = Variable('Synforcng', ['SigNegative', 'NegToPos', 'SigPositive', 'PosToNeg', 'LittleChange'])
Cldshadeoth = Variable('Cldshadeoth', ['Cloudy', 'PC', 'Clear'])
Raocontmoist = Variable('Raocontmoist', ['VeryWet', 'Wet', 'Neutral', 'Dry'])
Morningbound = Variable('Morningbound', ['None', 'Weak', 'Strong'])
Viscloudcov = Variable('Viscloudcov', ['Cloudy', 'PC', 'Clear'])
Mvmtfeatures = Variable('Mvmtfeatures', ['StrongFront', 'MarkedUpper', 'OtherRapid', 'NoMajor'])
Meanrh = Variable('Meanrh', ['VeryMoist', 'Average', 'Dry'])
Lifr12zdensd = Variable('Lifr12zdensd', ['LIGt0', 'N1GtLIGt_4', 'N5GtLIGt_8', 'LILt_8'])
Mountainfcst = Variable('Mountainfcst', ['XNIL', 'SIG', 'SVR'])
Ircloudcover = Variable('Ircloudcover', ['Cloudy', 'PC', 'Clear'])
Tempdis = Variable('Tempdis', ['QStationary', 'Moving', 'None', 'Other'])
Areameso_als = Variable('Areameso_als', ['StrongUp', 'WeakUp', 'Neutral', 'Down'])
Combclouds = Variable('Combclouds', ['Cloudy', 'PC', 'Clear'])
Areamodryair = Variable('Areamodryair', ['VeryWet', 'Wet', 'Neutral', 'Dry'])
Compplfcst = Variable('Compplfcst', ['IncCapDecIns', 'LittleChange', 'DecCapIncIns'])
Subjvertmo = Variable('Subjvertmo', ['StronUp', 'WeakUp', 'Neutral', 'Down'])
Qgvertmotion = Variable('Qgvertmotion', ['StrongUp', 'WeakUp', 'Neutral', 'Down'])
Plainsfcst = Variable('Plainsfcst', ['XNIL', 'SIG', 'SVR'])
Rhratio = Variable('Rhratio', ['MoistMDryL', 'DryMMoistL', 'Other'])
N0_7muvermo = Variable('N0_7muvermo', ['StrongUp', 'WeakUp', 'Neutral', 'Down'])
Dewpoints = Variable('Dewpoints', ['LowEvrywhere', 'LowAtStation', 'LowSHighN', 'LowNHighS', 'LowMtsHighPl', 'HighEvrywher', 'Other'])
Lowllapse = Variable('Lowllapse', ['CloseToDryAd', 'Steep', 'ModerateOrLe', 'Stable'])
Scenrelamcin = Variable('Scenrelamcin', ['AB', 'CThruK'])
f_satcontmoist = Prob(Satcontmoist,[],[0.15,0.2,0.4,0.25])
f_boundaries = Prob(Boundaries,[Wndhodograph,Outflowfrmt,Morningbound],[0.5,0.48,0.02,0.3,0.5,0.2,0.1,0.25,0.65,0.3,0.63,0.07,0.1,0.5,0.4,0.05,0.2,0.75,0.0,0.55,0.45,0.0,0.4,0.6,0.0,0.15,0.85,0.75,0.22,0.03,0.45,0.45,0.1,0.25,0.4,0.35,0.15,0.7,0.15,0.1,0.75,0.15,0.05,0.5,0.45,0.0,0.5,0.5,0.0,0.4,0.6,0.0,0.2,0.8,0.8,0.18,0.02,0.35,0.5,0.15,0.25,0.35,0.4,0.15,0.7,0.15,0.05,0.8,0.15,0.05,0.45,0.5,0.0,0.7,0.3,0.0,0.5,0.5,0.0,0.2,0.8,0.7,0.28,0.02,0.25,0.6,0.15,0.05,0.35,0.6,0.4,0.55,0.05,0.2,0.65,0.15,0.05,0.3,0.65,0.02,0.73,0.25,0.01,0.5,0.49,0.01,0.2,0.79])
f_amdewptcalpl = Prob(Amdewptcalpl,[],[0.3,0.25,0.45])
f_midllapse = Prob(Midllapse,[Scenario],[0.25,0.55,0.2,0.25,0.5,0.25,0.4,0.38,0.22,0.43,0.37,0.2,0.02,0.38,0.6,0.0,0.1,0.9,0.84,0.16,0.0,0.25,0.31,0.44,0.41,0.29,0.3,0.23,0.42,0.35,0.16,0.28,0.56])
f_inssclinscen = Prob(Inssclinscen,[Inschange,Aminswliscen],[1.0,0.0,0.0,0.6,0.4,0.0,0.25,0.35,0.4,0.9,0.1,0.0,0.15,0.7,0.15,0.0,0.1,0.9,0.4,0.35,0.25,0.0,0.4,0.6,0.0,0.0,1.0])
f_insinmt = Prob(Insinmt,[Cldshadeoth,Aminstabmt],[0.9,0.1,0.0,0.01,0.4,0.59,0.0,0.05,0.95,0.6,0.39,0.01,0.0,0.4,0.6,0.0,0.0,1.0,0.5,0.35,0.15,0.0,0.15,0.85,0.0,0.0,1.0])
f_n34starfcst = Prob(N34starfcst,[Scenrel3_4,Plainsfcst],[0.94,0.05,0.01,0.06,0.89,0.05,0.01,0.05,0.94,0.98,0.02,0.0,0.04,0.94,0.02,0.0,0.03,0.97,0.92,0.06,0.02,0.01,0.89,0.1,0.0,0.01,0.99,0.92,0.06,0.02,0.03,0.92,0.05,0.01,0.04,0.95,0.99,0.01,0.0,0.09,0.9,0.01,0.03,0.12,0.85])
f_amcininscen = Prob(Amcininscen,[Scenrelamcin,Morningcin],[1.0,0.0,0.0,0.6,0.37,0.03,0.25,0.45,0.3,0.0,0.1,0.9,0.75,0.25,0.0,0.3,0.6,0.1,0.01,0.4,0.59,0.0,0.03,0.97])
f_windfieldmt = Prob(Windfieldmt,[Scenario],[0.8,0.2,0.35,0.65,0.75,0.25,0.7,0.3,0.65,0.35,0.15,0.85,0.7,0.3,0.3,0.7,0.5,0.5,0.01,0.99,0.7,0.3])
f_combmoisture = Prob(Combmoisture,[Satcontmoist,Raocontmoist],[0.9,0.1,0.0,0.0,0.6,0.35,0.05,0.0,0.3,0.5,0.2,0.0,0.25,0.35,0.25,0.15,0.55,0.4,0.05,0.0,0.15,0.6,0.2,0.05,0.05,0.4,0.45,0.1,0.1,0.3,0.3,0.3,0.25,0.3,0.35,0.1,0.1,0.35,0.5,0.05,0.0,0.15,0.7,0.15,0.0,0.1,0.4,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25])
f_aminswliscen = Prob(Aminswliscen,[Scenrelamins,Lifr12zdensd,Amdewptcalpl],[0.6,0.3,0.1,0.85,0.13,0.02,0.95,0.04,0.01,0.3,0.3,0.4,0.5,0.3,0.2,0.75,0.2,0.05,0.06,0.21,0.73,0.2,0.4,0.4,0.5,0.4,0.1,0.01,0.04,0.95,0.05,0.2,0.75,0.35,0.35,0.3,0.4,0.3,0.3,0.7,0.2,0.1,0.9,0.08,0.02,0.15,0.3,0.55,0.25,0.5,0.25,0.6,0.3,0.1,0.03,0.17,0.8,0.2,0.3,0.5,0.45,0.4,0.15,0.01,0.04,0.95,0.05,0.18,0.77,0.25,0.4,0.35,0.35,0.35,0.3,0.55,0.4,0.05,0.85,0.13,0.02,0.07,0.38,0.55,0.2,0.6,0.2,0.5,0.43,0.07,0.0,0.05,0.95,0.05,0.35,0.6,0.25,0.5,0.25,0.0,0.02,0.98,0.0,0.05,0.95,0.04,0.16,0.8,0.3,0.4,0.3,0.5,0.3,0.2,0.75,0.2,0.05,0.15,0.35,0.5,0.2,0.6,0.2,0.15,0.7,0.15,0.07,0.23,0.7,0.13,0.47,0.4,0.1,0.75,0.15,0.02,0.18,0.8,0.04,0.26,0.7,0.07,0.3,0.63,0.35,0.45,0.2,0.4,0.5,0.1,0.58,0.4,0.02,0.1,0.25,0.65,0.15,0.45,0.4,0.4,0.45,0.15,0.02,0.18,0.8,0.05,0.25,0.7,0.15,0.35,0.5,0.01,0.09,0.9,0.03,0.17,0.8,0.08,0.32,0.6,0.3,0.55,0.15,0.4,0.5,0.1,0.5,0.43,0.07,0.1,0.35,0.55,0.25,0.5,0.25,0.3,0.5,0.2,0.05,0.22,0.73,0.1,0.35,0.55,0.15,0.35,0.5,0.02,0.1,0.88,0.04,0.16,0.8,0.1,0.25,0.65])
f_sfcwndshfdis = Prob(Sfcwndshfdis,[Scenario],[0.65,0.05,0.1,0.08,0.04,0.07,0.01,0.65,0.05,0.1,0.1,0.02,0.07,0.01,0.0,0.65,0.2,0.02,0.06,0.05,0.02,0.12,0.02,0.02,0.02,0.45,0.27,0.1,0.06,0.14,0.04,0.04,0.25,0.4,0.07,0.1,0.1,0.1,0.02,0.0,0.56,0.12,0.02,0.05,0.05,0.0,0.35,0.33,0.2,0.01,0.1,0.15,0.4,0.0,0.23,0.11,0.02,0.1,0.5,0.3,0.01,0.02,0.05,0.06,0.08,0.04,0.02,0.6,0.14,0.06,0.05,0.13,0.05,0.39,0.13,0.15,0.1])
f_capinscen = Prob(Capinscen,[Capchange,Amcininscen],[1.0,0.0,0.0,0.75,0.25,0.0,0.3,0.35,0.35,0.98,0.02,0.0,0.03,0.94,0.03,0.0,0.02,0.98,0.35,0.35,0.3,0.0,0.25,0.75,0.0,0.0,1.0])
f_scenrel3_4 = Prob(Scenrel3_4,[Scenario],[1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0])
f_scnrelplfcst = Prob(Scnrelplfcst,[Scenario],[1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0])
f_windfieldpln = Prob(Windfieldpln,[Scenario],[0.05,0.6,0.02,0.1,0.23,0.0,0.08,0.6,0.02,0.1,0.2,0.0,0.1,0.0,0.75,0.0,0.0,0.15,0.1,0.15,0.2,0.05,0.3,0.2,0.43,0.1,0.15,0.06,0.06,0.2,0.6,0.07,0.01,0.12,0.2,0.0,0.25,0.01,0.3,0.01,0.03,0.4,0.04,0.02,0.04,0.8,0.1,0.0,0.2,0.3,0.05,0.37,0.07,0.01,0.6,0.08,0.07,0.03,0.2,0.02,0.1,0.05,0.1,0.05,0.2,0.5])
f_aminstabmt = Prob(Aminstabmt,[],[0.333333,0.333333,0.333334])
f_wndhodograph = Prob(Wndhodograph,[],[0.3,0.25,0.25,0.2])
f_scenario = Prob(Scenario,[Date],[0.1,0.16,0.1,0.08,0.08,0.01,0.08,0.1,0.09,0.03,0.17,0.05,0.16,0.09,0.09,0.12,0.02,0.13,0.06,0.07,0.11,0.1,0.04,0.13,0.1,0.08,0.15,0.03,0.14,0.04,0.06,0.15,0.08,0.04,0.13,0.09,0.07,0.2,0.08,0.06,0.05,0.07,0.13,0.08,0.04,0.11,0.1,0.07,0.17,0.05,0.1,0.05,0.07,0.14,0.1,0.05,0.11,0.1,0.08,0.11,0.02,0.11,0.06,0.08,0.11,0.17])
f_curpropconv = Prob(Curpropconv,[Latestcin,Lliw],[0.7,0.28,0.02,0.0,0.1,0.5,0.3,0.1,0.01,0.14,0.35,0.5,0.0,0.02,0.18,0.8,0.9,0.09,0.01,0.0,0.65,0.25,0.09,0.01,0.25,0.35,0.3,0.1,0.01,0.15,0.33,0.51,0.95,0.05,0.0,0.0,0.75,0.23,0.02,0.0,0.4,0.4,0.18,0.02,0.2,0.3,0.35,0.15,1.0,0.0,0.0,0.0,0.95,0.05,0.0,0.0,0.75,0.2,0.05,0.0,0.5,0.35,0.1,0.05])
f_capchange = Prob(Capchange,[Compplfcst],[0.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,0.0])
f_morningcin = Prob(Morningcin,[],[0.15,0.57,0.2,0.08])
f_r5fcst = Prob(R5fcst,[Mountainfcst,N34starfcst],[1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0])
f_inschange = Prob(Inschange,[Compplfcst,Lolevmoistad],[0.0,0.05,0.95,0.05,0.15,0.8,0.15,0.5,0.35,0.5,0.4,0.1,0.0,0.12,0.88,0.1,0.4,0.5,0.2,0.6,0.2,0.8,0.16,0.04,0.05,0.15,0.8,0.25,0.5,0.25,0.35,0.5,0.15,0.9,0.09,0.01])
f_windaloft = Prob(Windaloft,[Scenario],[0.0,0.95,0.01,0.04,0.2,0.3,0.2,0.3,0.05,0.09,0.59,0.27,0.03,0.32,0.42,0.23,0.07,0.66,0.02,0.25,0.5,0.0,0.0,0.5,0.25,0.3,0.25,0.2,0.2,0.14,0.43,0.23,0.2,0.41,0.1,0.29,0.96,0.0,0.0,0.04,0.03,0.08,0.33,0.56])
f_lolevmoistad = Prob(Lolevmoistad,[],[0.12,0.28,0.3,0.3])
f_date = Prob(Date,[],[0.254098,0.131148,0.106557,0.213115,0.07377,0.221312])
f_outflowfrmt = Prob(Outflowfrmt,[Insinmt,Wndhodograph],[1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.4,0.1,0.15,0.4,0.45,0.35,0.6,0.05,0.8,0.19,0.01,0.05,0.45,0.5,0.01,0.15,0.84,0.1,0.25,0.65,0.6,0.3,0.1])
f_scenrelamins = Prob(Scenrelamins,[Scenario],[1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0])
f_combvermo = Prob(Combvermo,[N0_7muvermo,Subjvertmo,Qgvertmotion],[1.0,0.0,0.0,0.0,0.9,0.1,0.0,0.0,0.7,0.2,0.1,0.0,0.2,0.5,0.2,0.1,0.9,0.1,0.0,0.0,0.7,0.3,0.0,0.0,0.15,0.7,0.15,0.0,0.1,0.35,0.45,0.1,0.7,0.2,0.1,0.0,0.15,0.7,0.15,0.0,0.2,0.6,0.2,0.0,0.1,0.2,0.6,0.1,0.2,0.5,0.2,0.1,0.1,0.35,0.45,0.1,0.1,0.2,0.6,0.1,0.1,0.1,0.2,0.6,0.9,0.1,0.0,0.0,0.7,0.3,0.0,0.0,0.15,0.7,0.15,0.0,0.1,0.35,0.45,0.1,0.7,0.3,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.7,0.3,0.0,0.0,0.2,0.7,0.1,0.15,0.7,0.15,0.0,0.0,0.7,0.3,0.0,0.0,0.3,0.7,0.0,0.0,0.15,0.5,0.35,0.1,0.35,0.45,0.1,0.0,0.2,0.7,0.1,0.0,0.15,0.5,0.35,0.0,0.1,0.2,0.7,0.7,0.2,0.1,0.0,0.15,0.7,0.15,0.0,0.2,0.6,0.2,0.0,0.1,0.2,0.6,0.1,0.15,0.7,0.15,0.0,0.0,0.7,0.3,0.0,0.0,0.3,0.7,0.0,0.0,0.15,0.5,0.35,0.2,0.6,0.2,0.0,0.0,0.3,0.7,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.7,0.3,0.1,0.2,0.6,0.1,0.0,0.15,0.5,0.35,0.0,0.0,0.7,0.3,0.0,0.0,0.3,0.7,0.2,0.5,0.2,0.1,0.1,0.35,0.45,0.1,0.1,0.2,0.6,0.1,0.1,0.1,0.2,0.6,0.1,0.35,0.45,0.1,0.0,0.2,0.7,0.1,0.0,0.15,0.5,0.35,0.0,0.1,0.2,0.7,0.1,0.2,0.6,0.1,0.0,0.15,0.5,0.35,0.0,0.0,0.7,0.3,0.0,0.0,0.3,0.7,0.1,0.1,0.2,0.6,0.0,0.1,0.2,0.7,0.0,0.0,0.3,0.7,0.0,0.0,0.0,1.0])
f_cldshadeconv = Prob(Cldshadeconv,[Insinmt,Wndhodograph],[1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.3,0.6,0.1,0.2,0.7,0.1,0.5,0.46,0.04,0.8,0.19,0.01,0.0,0.3,0.7,0.0,0.2,0.8,0.1,0.5,0.4,0.5,0.38,0.12])
f_latestcin = Prob(Latestcin,[],[0.4,0.4,0.15,0.05])
f_lliw = Prob(Lliw,[],[0.12,0.32,0.38,0.18])
f_synforcng = Prob(Synforcng,[Scenario],[0.35,0.25,0.0,0.35,0.05,0.06,0.1,0.06,0.3,0.48,0.1,0.27,0.4,0.08,0.15,0.35,0.2,0.1,0.25,0.1,0.15,0.15,0.1,0.15,0.45,0.15,0.1,0.05,0.15,0.55,0.15,0.1,0.1,0.25,0.4,0.25,0.25,0.25,0.15,0.1,0.25,0.2,0.15,0.2,0.2,0.01,0.05,0.01,0.05,0.88,0.2,0.2,0.35,0.15,0.1])
f_cldshadeoth = Prob(Cldshadeoth,[Areameso_als,Areamodryair,Combclouds],[1.0,0.0,0.0,0.85,0.15,0.0,0.25,0.35,0.4,0.92,0.08,0.0,0.7,0.29,0.01,0.15,0.4,0.45,0.88,0.12,0.0,0.4,0.5,0.1,0.1,0.4,0.5,0.85,0.14,0.01,0.55,0.43,0.02,0.1,0.25,0.65,0.95,0.05,0.0,0.4,0.55,0.05,0.05,0.45,0.5,0.9,0.09,0.01,0.25,0.6,0.15,0.01,0.3,0.69,0.85,0.15,0.0,0.15,0.75,0.1,0.0,0.2,0.8,0.6,0.39,0.01,0.01,0.9,0.09,0.0,0.15,0.85,0.93,0.07,0.0,0.2,0.78,0.02,0.01,0.29,0.7,0.8,0.2,0.0,0.01,0.89,0.1,0.0,0.1,0.9,0.8,0.18,0.02,0.03,0.85,0.12,0.0,0.05,0.95,0.78,0.2,0.02,0.01,0.74,0.25,0.0,0.04,0.96,0.74,0.25,0.01,0.0,0.5,0.5,0.0,0.1,0.9,0.65,0.34,0.01,0.0,0.4,0.6,0.0,0.02,0.98,0.5,0.48,0.02,0.01,0.74,0.25,0.0,0.01,0.99,0.42,0.55,0.03,0.05,0.65,0.3,0.0,0.0,1.0])
f_raocontmoist = Prob(Raocontmoist,[],[0.15,0.2,0.4,0.25])
f_morningbound = Prob(Morningbound,[],[0.5,0.35,0.15])
f_viscloudcov = Prob(Viscloudcov,[],[0.1,0.5,0.4])
f_mvmtfeatures = Prob(Mvmtfeatures,[Scenario],[0.25,0.55,0.2,0.0,0.05,0.1,0.1,0.75,0.1,0.3,0.3,0.3,0.18,0.38,0.34,0.1,0.02,0.02,0.26,0.7,0.05,0.07,0.05,0.83,0.1,0.25,0.15,0.5,0.0,0.6,0.1,0.3,0.2,0.1,0.2,0.5,0.04,0.0,0.04,0.92,0.5,0.35,0.09,0.06])
f_meanrh = Prob(Meanrh,[Scenario],[0.33,0.5,0.17,0.4,0.4,0.2,0.05,0.45,0.5,0.1,0.5,0.4,0.05,0.65,0.3,1.0,0.0,0.0,0.0,0.07,0.93,0.4,0.55,0.05,0.2,0.45,0.35,0.05,0.55,0.4,0.2,0.4,0.4])
f_lifr12zdensd = Prob(Lifr12zdensd,[],[0.1,0.52,0.3,0.08])
f_mountainfcst = Prob(Mountainfcst,[Insinmt],[1.0,0.0,0.0,0.48,0.5,0.02,0.2,0.5,0.3])
f_ircloudcover = Prob(Ircloudcover,[],[0.15,0.45,0.4])
f_tempdis = Prob(Tempdis,[Scenario],[0.13,0.15,0.1,0.62,0.15,0.15,0.25,0.45,0.12,0.1,0.35,0.43,0.1,0.15,0.4,0.35,0.04,0.04,0.82,0.1,0.05,0.12,0.75,0.08,0.03,0.03,0.84,0.1,0.05,0.4,0.5,0.05,0.8,0.19,0.0,0.01,0.1,0.05,0.4,0.45,0.2,0.3,0.3,0.2])
f_areameso_als = Prob(Areameso_als,[Combvermo],[1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0])
f_combclouds = Prob(Combclouds,[Viscloudcov,Ircloudcover],[0.95,0.04,0.01,0.85,0.13,0.02,0.8,0.1,0.1,0.45,0.52,0.03,0.1,0.8,0.1,0.05,0.45,0.5,0.1,0.4,0.5,0.02,0.28,0.7,0.0,0.02,0.98])
f_areamodryair = Prob(Areamodryair,[Areameso_als,Combmoisture],[0.99,0.01,0.0,0.0,0.7,0.29,0.01,0.0,0.2,0.55,0.24,0.01,0.0,0.25,0.55,0.2,0.8,0.2,0.0,0.0,0.35,0.55,0.1,0.0,0.01,0.39,0.55,0.05,0.0,0.02,0.43,0.55,0.7,0.29,0.01,0.0,0.2,0.6,0.2,0.0,0.01,0.09,0.8,0.1,0.0,0.0,0.3,0.7,0.2,0.74,0.06,0.0,0.05,0.4,0.45,0.1,0.0,0.05,0.5,0.45,0.0,0.0,0.01,0.99])
f_compplfcst = Prob(Compplfcst,[Areameso_als,Cldshadeoth,Boundaries,Cldshadeconv],[0.4,0.35,0.25,0.4,0.35,0.25,0.45,0.3,0.25,0.35,0.35,0.3,0.35,0.35,0.3,0.4,0.35,0.25,0.3,0.3,0.4,0.3,0.3,0.4,0.3,0.35,0.35,0.1,0.35,0.55,0.25,0.3,0.45,0.4,0.3,0.3,0.05,0.35,0.6,0.1,0.35,0.55,0.25,0.4,0.35,0.01,0.25,0.74,0.05,0.6,0.35,0.15,0.35,0.5,0.05,0.3,0.65,0.15,0.35,0.5,0.35,0.3,0.35,0.03,0.25,0.72,0.05,0.3,0.65,0.2,0.4,0.4,0.01,0.2,0.79,0.04,0.27,0.69,0.13,0.35,0.52,0.6,0.25,0.15,0.65,0.25,0.1,0.7,0.22,0.08,0.5,0.25,0.25,0.55,0.25,0.2,0.65,0.25,0.1,0.35,0.25,0.4,0.4,0.25,0.35,0.5,0.25,0.25,0.4,0.3,0.3,0.45,0.3,0.25,0.55,0.3,0.15,0.3,0.35,0.35,0.35,0.35,0.3,0.45,0.35,0.2,0.15,0.4,0.45,0.2,0.4,0.4,0.35,0.35,0.3,0.2,0.5,0.3,0.25,0.5,0.25,0.4,0.45,0.15,0.15,0.45,0.4,0.2,0.5,0.3,0.3,0.5,0.2,0.1,0.35,0.55,0.12,0.43,0.45,0.2,0.45,0.35,0.6,0.35,0.05,0.65,0.3,0.05,0.7,0.27,0.03,0.55,0.3,0.15,0.6,0.3,0.1,0.65,0.3,0.05,0.45,0.3,0.25,0.5,0.3,0.2,0.55,0.35,0.1,0.45,0.4,0.15,0.5,0.4,0.1,0.6,0.3,0.1,0.4,0.4,0.2,0.45,0.4,0.15,0.55,0.3,0.15,0.3,0.4,0.3,0.35,0.4,0.25,0.45,0.35,0.2,0.25,0.45,0.3,0.3,0.45,0.25,0.55,0.33,0.12,0.2,0.4,0.4,0.25,0.5,0.25,0.5,0.3,0.2,0.15,0.4,0.45,0.2,0.45,0.35,0.4,0.35,0.25,0.7,0.27,0.03,0.75,0.23,0.02,0.85,0.14,0.01,0.6,0.35,0.05,0.65,0.3,0.05,0.78,0.18,0.04,0.5,0.35,0.15,0.55,0.35,0.1,0.7,0.24,0.06,0.65,0.3,0.05,0.7,0.26,0.04,0.8,0.17,0.03,0.6,0.3,0.1,0.65,0.3,0.05,0.75,0.2,0.05,0.48,0.32,0.2,0.55,0.3,0.15,0.65,0.28,0.07,0.6,0.35,0.05,0.65,0.32,0.03,0.75,0.23,0.02,0.55,0.33,0.12,0.6,0.35,0.05,0.7,0.25,0.05,0.45,0.35,0.2,0.5,0.4,0.1,0.6,0.3,0.1])
f_subjvertmo = Prob(Subjvertmo,[],[0.15,0.15,0.5,0.2])
f_qgvertmotion = Prob(Qgvertmotion,[],[0.15,0.15,0.5,0.2])
f_plainsfcst = Prob(Plainsfcst,[Capinscen,Inssclinscen,Curpropconv,Scnrelplfcst],[0.75,0.2,0.05,0.75,0.2,0.05,0.9,0.08,0.02,0.9,0.06,0.04,0.88,0.1,0.02,0.92,0.08,0.0,0.85,0.13,0.02,1.0,0.0,0.0,0.9,0.08,0.02,0.9,0.08,0.02,0.95,0.04,0.01,0.7,0.25,0.05,0.6,0.33,0.07,0.82,0.13,0.05,0.85,0.1,0.05,0.82,0.15,0.03,0.85,0.14,0.01,0.8,0.17,0.03,0.97,0.02,0.01,0.88,0.1,0.02,0.86,0.1,0.04,0.88,0.1,0.02,0.5,0.4,0.1,0.45,0.42,0.13,0.75,0.18,0.07,0.75,0.15,0.1,0.72,0.22,0.06,0.78,0.21,0.01,0.66,0.27,0.07,0.88,0.1,0.02,0.7,0.22,0.08,0.78,0.16,0.06,0.8,0.16,0.04,0.4,0.45,0.15,0.35,0.45,0.2,0.6,0.27,0.13,0.6,0.22,0.18,0.55,0.32,0.13,0.69,0.29,0.02,0.54,0.36,0.1,0.75,0.2,0.05,0.55,0.3,0.15,0.7,0.22,0.08,0.7,0.25,0.05,0.5,0.3,0.2,0.6,0.3,0.1,0.8,0.14,0.06,0.85,0.09,0.06,0.85,0.1,0.05,0.88,0.11,0.01,0.8,0.17,0.03,0.92,0.06,0.02,0.8,0.12,0.08,0.75,0.22,0.03,0.9,0.08,0.02,0.3,0.4,0.3,0.55,0.34,0.11,0.7,0.2,0.1,0.75,0.15,0.1,0.62,0.28,0.1,0.85,0.14,0.01,0.75,0.2,0.05,0.82,0.14,0.04,0.6,0.25,0.15,0.68,0.22,0.1,0.82,0.15,0.03,0.2,0.45,0.35,0.4,0.4,0.2,0.7,0.2,0.1,0.65,0.22,0.13,0.5,0.34,0.16,0.74,0.24,0.02,0.6,0.3,0.1,0.67,0.24,0.09,0.35,0.4,0.25,0.6,0.25,0.15,0.75,0.2,0.05,0.16,0.47,0.37,0.3,0.45,0.25,0.45,0.32,0.23,0.52,0.26,0.22,0.35,0.45,0.2,0.65,0.32,0.03,0.48,0.39,0.13,0.58,0.3,0.12,0.25,0.45,0.3,0.5,0.28,0.22,0.65,0.27,0.08,0.35,0.2,0.45,0.45,0.35,0.2,0.8,0.1,0.1,0.72,0.14,0.14,0.78,0.15,0.07,0.86,0.12,0.02,0.65,0.25,0.1,0.85,0.1,0.05,0.65,0.2,0.15,0.72,0.2,0.08,0.85,0.1,0.05,0.3,0.25,0.45,0.4,0.36,0.24,0.65,0.2,0.15,0.6,0.2,0.2,0.6,0.28,0.12,0.83,0.14,0.03,0.45,0.4,0.15,0.7,0.18,0.12,0.55,0.25,0.2,0.6,0.25,0.15,0.72,0.2,0.08,0.25,0.28,0.47,0.3,0.38,0.32,0.45,0.3,0.25,0.5,0.25,0.25,0.4,0.35,0.25,0.72,0.24,0.04,0.25,0.57,0.18,0.57,0.28,0.15,0.25,0.35,0.4,0.48,0.26,0.26,0.6,0.26,0.14,0.18,0.3,0.52,0.2,0.4,0.4,0.3,0.3,0.4,0.4,0.3,0.3,0.25,0.48,0.27,0.63,0.32,0.05,0.15,0.63,0.22,0.4,0.38,0.22,0.2,0.37,0.43,0.3,0.35,0.35,0.5,0.32,0.18,0.75,0.2,0.05,0.65,0.3,0.05,0.9,0.08,0.02,0.91,0.05,0.04,0.85,0.13,0.02,0.9,0.1,0.0,0.84,0.12,0.04,0.99,0.01,0.0,0.88,0.1,0.02,0.92,0.06,0.02,0.96,0.03,0.01,0.65,0.25,0.1,0.58,0.32,0.1,0.8,0.15,0.05,0.85,0.1,0.05,0.8,0.16,0.04,0.83,0.16,0.01,0.77,0.17,0.06,0.93,0.06,0.01,0.85,0.12,0.03,0.85,0.1,0.05,0.9,0.08,0.02,0.45,0.35,0.2,0.45,0.35,0.2,0.7,0.2,0.1,0.72,0.17,0.11,0.7,0.22,0.08,0.75,0.24,0.01,0.62,0.3,0.08,0.85,0.12,0.03,0.75,0.15,0.1,0.76,0.17,0.07,0.8,0.16,0.04,0.35,0.4,0.25,0.35,0.4,0.25,0.55,0.3,0.15,0.55,0.27,0.18,0.5,0.35,0.15,0.65,0.33,0.02,0.38,0.5,0.12,0.7,0.24,0.06,0.65,0.2,0.15,0.67,0.23,0.1,0.7,0.25,0.05,0.35,0.3,0.35,0.55,0.3,0.15,0.82,0.13,0.05,0.82,0.1,0.08,0.75,0.18,0.07,0.88,0.11,0.01,0.75,0.2,0.05,0.9,0.07,0.03,0.7,0.2,0.1,0.8,0.15,0.05,0.9,0.08,0.02,0.28,0.37,0.35,0.48,0.35,0.17,0.7,0.2,0.1,0.7,0.17,0.13,0.6,0.29,0.11,0.82,0.16,0.02,0.63,0.3,0.07,0.8,0.15,0.05,0.5,0.3,0.2,0.7,0.2,0.1,0.8,0.16,0.04,0.23,0.4,0.37,0.38,0.35,0.27,0.58,0.25,0.17,0.55,0.25,0.2,0.53,0.32,0.15,0.73,0.25,0.02,0.35,0.53,0.12,0.65,0.24,0.11,0.3,0.4,0.3,0.6,0.24,0.16,0.68,0.24,0.08,0.18,0.45,0.37,0.3,0.35,0.35,0.45,0.3,0.25,0.45,0.3,0.25,0.35,0.43,0.22,0.62,0.35,0.03,0.2,0.65,0.15,0.52,0.33,0.15,0.23,0.42,0.35,0.47,0.3,0.23,0.55,0.3,0.15,0.25,0.15,0.6,0.45,0.35,0.2,0.65,0.2,0.15,0.55,0.2,0.25,0.55,0.25,0.2,0.81,0.17,0.02,0.6,0.28,0.12,0.8,0.13,0.07,0.6,0.2,0.2,0.75,0.15,0.1,0.88,0.08,0.04,0.22,0.17,0.61,0.35,0.37,0.28,0.45,0.3,0.25,0.45,0.25,0.3,0.48,0.29,0.23,0.72,0.25,0.03,0.43,0.4,0.17,0.68,0.2,0.12,0.35,0.3,0.35,0.6,0.2,0.2,0.74,0.16,0.1,0.19,0.18,0.63,0.25,0.4,0.35,0.35,0.3,0.35,0.35,0.3,0.35,0.35,0.35,0.3,0.65,0.3,0.05,0.22,0.58,0.2,0.45,0.35,0.2,0.25,0.34,0.41,0.48,0.26,0.26,0.58,0.25,0.17,0.15,0.2,0.65,0.18,0.4,0.42,0.25,0.35,0.4,0.25,0.35,0.4,0.25,0.42,0.33,0.58,0.36,0.06,0.13,0.62,0.25,0.3,0.45,0.25,0.22,0.35,0.43,0.35,0.32,0.33,0.5,0.3,0.2,0.75,0.2,0.05,0.75,0.2,0.05,0.95,0.04,0.01,0.93,0.04,0.03,0.92,0.06,0.02,0.87,0.13,0.0,0.9,0.06,0.04,0.98,0.02,0.0,0.92,0.06,0.02,0.95,0.04,0.01,0.97,0.02,0.01,0.6,0.3,0.1,0.65,0.28,0.07,0.9,0.08,0.02,0.85,0.1,0.05,0.82,0.13,0.05,0.8,0.19,0.01,0.8,0.13,0.07,0.91,0.08,0.01,0.85,0.12,0.03,0.9,0.08,0.02,0.93,0.06,0.01,0.35,0.4,0.25,0.45,0.4,0.15,0.75,0.19,0.06,0.7,0.2,0.1,0.6,0.3,0.1,0.72,0.27,0.01,0.6,0.3,0.1,0.8,0.16,0.04,0.75,0.17,0.08,0.75,0.2,0.05,0.88,0.1,0.02,0.2,0.45,0.35,0.3,0.45,0.25,0.55,0.3,0.15,0.5,0.3,0.2,0.45,0.38,0.17,0.6,0.38,0.02,0.28,0.57,0.15,0.65,0.28,0.07,0.63,0.25,0.12,0.62,0.28,0.1,0.8,0.17,0.03,0.5,0.2,0.3,0.6,0.25,0.15,0.85,0.1,0.05,0.85,0.07,0.08,0.75,0.15,0.1,0.85,0.14,0.01,0.75,0.2,0.05,0.94,0.05,0.01,0.65,0.22,0.13,0.83,0.1,0.07,0.93,0.06,0.01,0.4,0.28,0.32,0.5,0.25,0.25,0.72,0.18,0.1,0.65,0.2,0.15,0.55,0.3,0.15,0.78,0.2,0.02,0.55,0.35,0.1,0.85,0.12,0.03,0.45,0.3,0.25,0.73,0.15,0.12,0.85,0.12,0.03,0.3,0.34,0.36,0.35,0.35,0.3,0.55,0.25,0.2,0.5,0.27,0.23,0.4,0.38,0.22,0.7,0.28,0.02,0.35,0.5,0.15,0.6,0.25,0.15,0.35,0.35,0.3,0.62,0.22,0.16,0.7,0.22,0.08,0.23,0.4,0.37,0.25,0.4,0.35,0.4,0.3,0.3,0.4,0.3,0.3,0.3,0.45,0.25,0.57,0.4,0.03,0.15,0.65,0.2,0.5,0.33,0.17,0.25,0.36,0.39,0.5,0.28,0.22,0.55,0.3,0.15,0.4,0.08,0.52,0.45,0.25,0.3,0.75,0.1,0.15,0.65,0.15,0.2,0.52,0.25,0.23,0.82,0.16,0.02,0.65,0.27,0.08,0.85,0.09,0.06,0.5,0.2,0.3,0.77,0.1,0.13,0.9,0.07,0.03,0.27,0.1,0.63,0.35,0.3,0.35,0.55,0.22,0.23,0.45,0.25,0.3,0.42,0.3,0.28,0.74,0.22,0.04,0.45,0.4,0.15,0.77,0.13,0.1,0.3,0.25,0.45,0.68,0.15,0.17,0.75,0.15,0.1,0.15,0.16,0.69,0.25,0.3,0.45,0.4,0.3,0.3,0.3,0.3,0.4,0.25,0.4,0.35,0.6,0.34,0.06,0.18,0.62,0.2,0.47,0.3,0.23,0.25,0.3,0.45,0.5,0.22,0.28,0.5,0.27,0.23,0.1,0.2,0.7,0.2,0.3,0.5,0.2,0.4,0.4,0.23,0.3,0.47,0.15,0.45,0.4,0.5,0.42,0.08,0.1,0.65,0.25,0.28,0.4,0.32,0.2,0.32,0.48,0.3,0.28,0.42,0.38,0.32,0.3])
f_rhratio = Prob(Rhratio,[Scenario],[0.05,0.5,0.45,0.1,0.5,0.4,0.4,0.15,0.45,0.2,0.45,0.35,0.8,0.05,0.15,0.0,0.0,1.0,0.6,0.0,0.4,0.0,0.7,0.3,0.1,0.7,0.2,0.4,0.4,0.2,0.15,0.45,0.4])
f_n0_7muvermo = Prob(N0_7muvermo,[],[0.25,0.25,0.25,0.25])
f_dewpoints = Prob(Dewpoints,[Scenario],[0.04,0.05,0.15,0.05,0.19,0.3,0.22,0.05,0.07,0.15,0.1,0.3,0.27,0.06,0.4,0.25,0.0,0.15,0.05,0.02,0.13,0.13,0.22,0.18,0.07,0.34,0.03,0.03,0.15,0.2,0.2,0.18,0.11,0.11,0.05,0.0,0.0,0.0,0.0,0.0,0.98,0.02,0.5,0.27,0.15,0.02,0.02,0.0,0.04,0.0,0.02,0.1,0.05,0.5,0.2,0.13,0.0,0.02,0.7,0.0,0.2,0.04,0.04,0.1,0.45,0.1,0.05,0.26,0.02,0.02,0.1,0.1,0.1,0.2,0.05,0.1,0.35])
f_lowllapse = Prob(Lowllapse,[Scenario],[0.04,0.25,0.35,0.36,0.07,0.31,0.31,0.31,0.35,0.47,0.14,0.04,0.4,0.4,0.13,0.07,0.45,0.35,0.15,0.05,0.01,0.35,0.45,0.19,0.78,0.19,0.03,0.0,0.0,0.02,0.33,0.65,0.22,0.4,0.3,0.08,0.13,0.4,0.35,0.12,0.09,0.4,0.33,0.18])
f_scenrelamcin = Prob(Scenrelamcin,[Scenario],[1.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0])

Hailfinder_Belief_Net = Belief_network(
                                       vars=[Satcontmoist, Boundaries, Amdewptcalpl, Midllapse, Inssclinscen, Insinmt, N34starfcst, Amcininscen, Windfieldmt, Combmoisture, Aminswliscen, Sfcwndshfdis, Capinscen, Scenrel3_4, Scnrelplfcst, Windfieldpln, Aminstabmt, Wndhodograph, Scenario, Curpropconv, Capchange, Morningcin, R5fcst, Inschange, Windaloft, Lolevmoistad, Date, Outflowfrmt, Scenrelamins, Combvermo, Cldshadeconv, Latestcin, Lliw, Synforcng, Cldshadeoth, Raocontmoist, Morningbound, Viscloudcov, Mvmtfeatures, Meanrh, Lifr12zdensd, Mountainfcst, Ircloudcover, Tempdis, Areameso_als, Combclouds, Areamodryair, Compplfcst, Subjvertmo, Qgvertmotion, Plainsfcst, Rhratio, N0_7muvermo, Dewpoints, Lowllapse, Scenrelamcin],
                                       factors=[f_satcontmoist, f_boundaries, f_amdewptcalpl, f_midllapse, f_inssclinscen, f_insinmt, f_n34starfcst, f_amcininscen, f_windfieldmt, f_combmoisture, f_aminswliscen, f_sfcwndshfdis, f_capinscen, f_scenrel3_4, f_scnrelplfcst, f_windfieldpln, f_aminstabmt, f_wndhodograph, f_scenario, f_curpropconv, f_capchange, f_morningcin, f_r5fcst, f_inschange, f_windaloft, f_lolevmoistad, f_date, f_outflowfrmt, f_scenrelamins, f_combvermo, f_cldshadeconv, f_latestcin, f_lliw, f_synforcng, f_cldshadeoth, f_raocontmoist, f_morningbound, f_viscloudcov, f_mvmtfeatures, f_meanrh, f_lifr12zdensd, f_mountainfcst, f_ircloudcover, f_tempdis, f_areameso_als, f_combclouds, f_areamodryair, f_compplfcst, f_subjvertmo, f_qgvertmotion, f_plainsfcst, f_rhratio, f_n0_7muvermo, f_dewpoints, f_lowllapse, f_scenrelamcin],
                                       positions=[])

