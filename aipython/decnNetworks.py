# decnNetworks.py - Representations for Decision Networks
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from probGraphicalModels import Graphical_model
from probFactors import Factor_stored
from probVariables import Variable
from probFactors import Prob

class Utility(Factor_stored):
    """A factor defined by a utility"""
    def __init__(self,vars,table):
        """Creates a factor on vars from the table.
        The table is ordered according to vars.
        """
        Factor_stored.__init__(self,vars,table)
        assert self.size==len(table),"Table size incorrect "+str(self)

class DecisionVariable(Variable):
    def __init__(self,name,domain,parents):
        Variable.__init__(self,name,domain)
        self.parents = parents
        self.all_vars = set(parents) | {self}

class DecisionNetwork(Graphical_model):
    def __init__(self,vars=None,factors=None):
        """vars is a list of variables
        factors is a list of factors (instances of Prob and Utility)
        """
        Graphical_model.__init__(self,vars,factors)

from probFactors import factor_times, Factor_stored
from probVE import VE

class VE_DN(VE):
    """Variable Elimination for Decision Networks"""
    def __init__(self,dn=None):
        """dn is a decision network"""
        VE.__init__(self,dn)
        self.dn = dn
        
    def optimize(self,elim_order=None,obs={}):
        if elim_order == None:
                elim_order = self.gm.variables
        policy = []
        proj_factors = [self.project_observations(fact,obs) 
                           for fact in self.dn.factors]
        for v in elim_order:
            if isinstance(v,DecisionVariable):
                to_max = [fac for fac in proj_factors
                          if v in fac.variables and set(fac.variables) <= v.all_vars]
                assert len(to_max)==1, "illegal variable order "+str(elim_order)+" at "+str(v)
                newFac = Factor_max(v, to_max[0])
                policy.append(newFac.decision_fun)
                proj_factors = [fac for fac in proj_factors if fac is not to_max[0]]+[newFac]
                self.display(2,"maximizing",v,"resulting factor",newFac.brief() )
                self.display(3,newFac)
            else:
                proj_factors = self.eliminate_var(proj_factors, v)
        assert len(proj_factors)==1,"Should there be only one element of proj_factors?"
        value = proj_factors[0].get_value({})
        return value,policy

class Factor_max(Factor_stored):
    """A factor obtained by maximizing a variable in a factor.
    Also builds a decision_function. This is based on Factor_sum.
    """

    def __init__(self, dvar, factor):
        """dvar is a decision variable. 
        factor is a factor that contains dvar and only parents of dvar
        """
        self.dvar = dvar
        self.factor = factor
        vars = [v for v in factor.variables if v is not dvar]
        Factor_stored.__init__(self,vars,None)
        self.values = [None]*self.size
        self.decision_fun = Factor_stored(vars,[None]*self.size)

    def get_value(self,assignment):
        """lazy implementation: if saved, return save value else compute it"""
        index = self.assignment_to_index(assignment)
        if self.values[index]:
            return self.values[index]
        else:
            max_val = float("-inf")  # -infinity
            new_asst = assignment.copy()
            for elt in self.dvar.domain:
                new_asst[self.dvar] = elt
                fac_val = self.factor.get_value(new_asst)
                if fac_val>max_val:
                    max_val = fac_val
                    best_elt = elt
            self.values[index] = max_val
            self.decision_fun.values[index] = best_elt
            return max_val
           
boolean = [False, True]
Al = Variable("Alarm", boolean)
Fi = Variable("Fire", boolean)
Le = Variable("Leaving", boolean)
Re = Variable("Report", boolean)
Sm = Variable("Smoke", boolean)
Ta = Variable("Tamper", boolean)
SS = Variable("See Sm", boolean)
CS = DecisionVariable("Ch Sm", boolean,{Re})
Call = DecisionVariable("Call", boolean,{SS,CS,Re})

f_ta = Prob(Ta,[],[0.98,0.02])
f_fi = Prob(Fi,[],[0.99,0.01])
f_sm = Prob(Sm,[Fi],[0.99,0.01,0.1,0.9])
f_al = Prob(Al,[Fi,Ta],[0.9999, 0.0001, 0.15, 0.85, 0.01, 0.99, 0.5, 0.5])
f_lv = Prob(Le,[Al],[0.999, 0.001, 0.12, 0.88])
f_re = Prob(Re,[Le],[0.99, 0.01, 0.25, 0.75])
f_ss = Prob(SS,[CS,Sm],[1,0,1,0,1,0,0,1])

ut = Utility([CS,Fi,Call],[0,-200,-5000,-200,-20,-220,-5020,-220])

dnf = DecisionNetwork([Ta,Fi,Al,Le,Sm,Call,SS,CS,Re],[f_ta,f_fi,f_sm,f_al,f_lv,f_re,f_ss,ut])
# v,p = VE_DN(dnf).optimize()
# for df in p: print(df,"\n")

grades = ["A","B","C","F"]
Wa = Variable("Watched", boolean)
CC1 = Variable("Caught1", boolean)
CC2 = Variable("Caught2", boolean)
Pun = Variable("Punish",["None","Suspension","Recorded"])
Gr1 = Variable("Grade_1",grades)
Gr2 = Variable("Grade_2",grades)
GrF = Variable("Fin_Gr",grades)
Ch1 = DecisionVariable("Cheat_1", boolean,set())
Ch2 = DecisionVariable("Cheat_2", boolean,{Ch1,CC1})

p_wa = Prob(Wa,[],[0.7, 0.3])
p_cc1 = Prob(CC1,[Wa,Ch1],[1.0, 0.0, 0.9, 0.1, 1.0, 0.0, 0.5, 0.5])
p_cc2 = Prob(CC2,[Wa,Ch2],[1.0, 0.0, 0.9, 0.1, 1.0, 0.0, 0.5, 0.5])
p_pun = Prob(Pun,[CC1,CC2],[1.0, 0.0, 0.0, 0.5, 0.4, 0.1, 0.6, 0.2, 0.2, 0.2, 0.5, 0.3])
p_gr1 = Prob(Gr1,[Ch1], [0.2, 0.3, 0.3, 0.2, 0.5, 0.3, 0.2, 0.0])
p_gr2 = Prob(Gr2,[Ch2], [0.2, 0.3, 0.3, 0.2, 0.5, 0.25, 0.25, 0.0])
p_fg = Prob(GrF,[Gr1,Gr2],
        [1.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.25, 0.5, 0.25, 0.0, 0.25,
        0.25, 0.25, 0.25, 0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.5,
        0.5, 0.0, 0.0, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.0, 0.0, 0.5, 0.5,
        0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.25, 0.75, 0.25, 0.5, 0.25, 0.0,
        0.0, 0.25, 0.5, 0.25, 0.0, 0.0, 0.25, 0.75, 0.0, 0.0, 0.0, 1.0])
utc = Utility([Pun,GrF],[100,90,70,50,40,20,10,0,70,60,40,20])

dnc = DecisionNetwork([Pun,CC2,Wa,GrF,Gr2,Gr1,Ch2,CC1,Ch1],
                      [p_wa, p_cc1, p_cc2, p_pun, p_gr1, p_gr2,p_fg,utc])

# VE_DN.max_display_level = 3  # if you want to show lots of detail
# v,p = VE_DN(dnc).optimize(); print(v)
# for df in p: print(df,"\n") # print decision functions

