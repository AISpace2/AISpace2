# probDBN.py - Dynamic belief networks
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from probVariables import Variable
from probGraphicalModels import Graphical_model
from probFactors import Prob, Factor_rename
from probVE import VE
from utilities import Displayable

class DBN_variable(Variable):
    """A random variable that incorporates 

    A variable can have both a name and an index. The index defaults to 1.
    Equality is true if they are both the name and the index are the same."""
    def __init__(self,name,domain=[False,True],index=1):
        Variable.__init__(self,name,domain)
        self.index = index
        self.previous = None

    def __lt__(self,other):
        if self.name != other.name:
            return self.name<other.name
        else:
            return self.index<other.index

    def __gt__(self,other):
        return other<self

    def __str__(self):
#        if self.index==1:
#            return self.name
#        else:
            return self.name+"_"+str(self.index)

    __repr__ = __str__

def variable_pair(name,domain=[False,True]):
    """returns a variable and its predecessor. This is used to define 2-stage DBNs

    If the name is X, it returns the pair of variables X0,X"""
    var = DBN_variable(name,domain)
    var0 = DBN_variable(name,domain,index=0)
    var.previous = var0
    return var0, var

class DBN(Displayable):
    """The class of stationary Dynamic Bayesian networks.

    * vars1 is a list of current variables (each must have
    previous variable).
    * transition_factors is a list of factors for P(X|parents) where X
    is a current variable and parents is a list of current or previous variables.
    * init_factors is a list of factors for P(X|parents) where X is a
    current variable and parents can only include current variables
    The graph of transition factors + init factors must be acyclic.
    
    """
    def __init__(self,vars1, transition_factors=None, init_factors=None):
        self.vars1 = vars1
        self.vars0 = [v.previous for v in vars1]
        self.transition_factors = transition_factors
        self.init_factors = init_factors
        self.var_index = {}       # var_index[v] is the index of variable v
        for i,v in enumerate(vars1):
            self.var_index[v]=i

A0,A1 = variable_pair("A")
B0,B1 = variable_pair("B")
C0,C1 = variable_pair("C")

# dynamics
pc = Prob(C1,[B1,C0],[0.03,0.97,0.38,0.62,0.23,0.77,0.78,0.22])
pb = Prob(B1,[A0,A1],[0.5,0.5,0.77,0.23,0.4,0.6,0.83,0.17])
pa = Prob(A1,[A0,B0],[0.1,0.9,0.65,0.35,0.3,0.7,0.8,0.2])

# initial distribution
pa0 = Prob(A1,[],[0.9,0.1])
pb0 = Prob(B1,[A1],[0.3,0.7,0.8,0.2])
pc0 = Prob(C1,[],[0.2,0.8])

dbn1 = DBN([A1,B1,C1],[pa,pb,pc],[pa0,pb0,pc0])

from probHMM import closeMic, farMic, midMic, sm, mmc, sc, mcm, mcc

Pos_0,Pos_1 = variable_pair("Position",domain=[0,1,2,3])
Mic1_0,Mic1_1 = variable_pair("Mic1")
Mic2_0,Mic2_1 = variable_pair("Mic2")
Mic3_0,Mic3_1 = variable_pair("Mic3")

# conditional probabilities - see hmm for the values of sm,mmc, etc
ppos = Prob(Pos_1, [Pos_0], 
            [sm, mmc, mmc, mmc,  #was in middle
             mcm, sc, mcc, mcc,  #was in corner 1
             mcm, mcc, sc, mcc,  #was in corner 2
             mcm, mcc, mcc, sc]) #was in corner 3
pm1 = Prob(Mic1_1, [Pos_1], [1-midMic, midMic, 1-closeMic, closeMic, 
                            1-farMic, farMic, 1-farMic, farMic])
pm2 = Prob(Mic2_1, [Pos_1], [1-midMic, midMic, 1-farMic, farMic, 
                            1-closeMic, closeMic, 1-farMic, farMic])
pm3 = Prob(Mic3_1, [Pos_1], [1-midMic, midMic, 1-farMic, farMic, 
                            1-farMic, farMic, 1-closeMic, closeMic])
ipos = Prob(Pos_1,[], [0.25, 0.25, 0.25, 0.25])
dbn_an =DBN([Pos_1,Mic1_1,Mic2_1,Mic3_1], 
            [ppos, pm1, pm2, pm3],
            [ipos, pm1, pm2, pm3])
            
class DBN_VE_filter(VE):
    def __init__(self,dbn):
        self.dbn = dbn
        self.current_factors = dbn.init_factors
        self.current_obs = {}

    def observe(self, obs):
        """updates the current observations with obs.
        obs is a variable:value dictionary where variable is a current
        variable.
        """
        assert all(self.current_obs[var]==obs[var] for var in obs 
                   if var in self.current_obs),"inconsistent current observations"
        self.current_obs.update(obs)

    def query(self,var):
        """returns the posterior probability of current variable var"""
        return VE(Graphical_model(self.dbn.vars1,self.current_factors)).query(var,self.current_obs)

    def advance(self):
        """advance to the next time"""
        prev_factors = [self.make_previous(fac) for fac in self.current_factors]
        prev_obs = {var.previous:val for var,val in self.current_obs.items()}
        two_stage_factors = prev_factors + self.dbn.transition_factors
        self.current_factors = self.elim_vars(two_stage_factors,self.dbn.vars0,prev_obs)
        self.current_obs = {}

    def make_previous(self,fac):
         """Creates new factor from fac where the current variables in fac
         are renamed to previous variables.
         """
         return Factor_rename(fac, {var.previous:var for var in fac.variables})

    def elim_vars(self,factors, vars, obs):
        for var in vars:
            if var in obs:
                factors = [self.project_observations(fac,obs) for fac in factors]
            else:
                factors = self.eliminate_var(factors, var)
        return factors

df = DBN_VE_filter(dbn1)
#df.observe({B1:True}); df.advance(); df.observe({C1:False})
#df.query(B1)
#df.advance()
#df.query(B1)
dfa = DBN_VE_filter(dbn_an)
# dfa.observe({Mic1_1:0, Mic2_1:1, Mic3_1:1})
# dfa.advance()
# dfa.observe({Mic1_1:1, Mic2_1:0, Mic3_1:1})
# dfa.query(Pos_1)

