# probVE.py - Variable Elimination for Graphical Models
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from probFactors import Factor, Factor_observed, Factor_sum, factor_times
from probGraphicalModels import Graphical_model, Inference_method

class VE(Inference_method):
    """The class that queries Graphical Models using variable elimination.

    gm is graphical model to query
    """
    def __init__(self,gm=None):
        self.gm = gm

    def query(self,var,obs={},elim_order=None):
        """computes P(var|obs) where
        var is a variable
        obs is a variable:value dictionary"""
        if var in obs:
            return [1 if val == obs[var] else 0 for val in var.domain]
        else:
            if elim_order == None:
                elim_order = self.gm.variables
            projFactors = [self.project_observations(fact,obs) 
                           for fact in self.gm.factors]
            for v in elim_order:   
                if v != var and v not in obs:
                    projFactors = self.eliminate_var(projFactors,v)
            unnorm = factor_times(var,projFactors)
            p_obs=sum(unnorm)
            self.display(1,"Unnormalized probs:",unnorm,"Prob obs:",p_obs)
            return {val:pr/p_obs for val,pr in zip(var.domain, unnorm)}

    def project_observations(self,factor,obs):
        """Returns the resulting factor after observing obs

        obs is a dictionary of variable:value pairs.
        """
        if any((var in obs) for var in factor.variables):
            # a variable in factor is observed
            return Factor_observed(factor,obs)
        else:
            return factor

    def eliminate_var(self,factors,var):
        """Eliminate a variable var from a list of factors. 
        Returns a new set of factors that has var summed out.
        """
        self.display(2,"eliminating ",str(var))
        contains_var = []
        not_contains_var = []
        for fac in factors:
            if var in fac.variables:
                contains_var.append(fac)
            else:
                not_contains_var.append(fac)
        if contains_var == []:
            return factors
        else:
            newFactor = Factor_sum(var,contains_var)
            self.display(2,"Multiplying:",[f.brief() for f in contains_var])
            self.display(2,"Creating factor:", newFactor.brief())
            self.display(3,"Factor in detail", newFactor)
            not_contains_var.append(newFactor)
            return not_contains_var

from probGraphicalModels import bn1, A,B,C
bn1v = VE(bn1)
## bn1v.query(A,{})
## bn1v.query(C,{})
## Inference_method.max_display_level = 3   # show more detail in displaying
## Inference_method.max_display_level = 1   # show less detail in displaying
## bn1v.query(A,{C:True})
## bn1v.query(B,{A:True,C:False})

from probGraphicalModels import bn2,Al,Fi,Le,Re,Sm,Ta
bn2v = VE(bn2)    # answers queries using variable elimination
## bn2v.query(Ta,{})
## Inference_method.max_display_level = 0   # show no detail in displaying
## bn2v.query(Le,{})
## bn2v.query(Ta,{},elim_order=[Sm,Re,Le,Al,Fi])
## bn2v.query(Ta,{Re:True})
## bn2v.query(Ta,{Re:True,Sm:False})

from probGraphicalModels import bn3, Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet
bn3v = VE(bn3)
## bn3v.query(Shoes_wet,{})
## bn3v.query(Shoes_wet,{Rained:True})
## bn3v.query(Shoes_wet,{Grass_shiny:True})
## bn3v.query(Shoes_wet,{Grass_shiny:False,Rained:True})

