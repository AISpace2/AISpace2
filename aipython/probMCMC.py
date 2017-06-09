# probMCMC.py - Markov Chain Monte Carlo (Gibbs sampling)
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import random
from probGraphicalModels import Inference_method

from probStochSim import sample_one, Sampling_inference_method

class Gibbs_sampling(Sampling_inference_method):
    """The class that queries Graphical Models using Gibbs Sampling.

    bn is a graphical model (e.g., a belief network) to query
    """
    def __init__(self,bn=None):
        self.bn = bn
        self.label = "Gibbs Sampling"

    def query(self, qvar, obs={}, number_samples=1000, burn_in=100, sample_order=None):
        """computes P(qvar|obs) where
        qvar is a variable.
        obs is a variable:value dictionary.
        sample_order is a list of non-observed variables in order.
        """
        counts = {val:0 for val in qvar.domain}
        if sample_order is not None:
            variables = sample_order
        else:
            variables = [v for v in self.bn.variables if v not in obs]
        var_to_factors = {v:set() for v in self.bn.variables}
        for fac in self.bn.factors:
            for var in fac.variables:
                var_to_factors[var].add(fac)
        sample = {var:random.choice(var.domain) for var in variables}
        self.display(2,"Sample:",sample)
        sample.update(obs)
        for i in range(burn_in + number_samples):
            if sample_order == None:
                random.shuffle(variables)
            for var in variables:
                # get probability distribution of var given its neighbours
                vardist = {val:1 for val in var.domain}
                for val in var.domain: 
                    sample[var] = val
                    for fac in var_to_factors[var]:  # Markov blanket
                        vardist[val] *= fac.get_value(sample)
                sample[var] = sample_one(vardist)
            if i >= burn_in:
                counts[sample[qvar]] +=1
        tot = sum(counts.values())
        return counts, {c:v/tot for (c,v) in counts.items()}

from probGraphicalModels import bn1, A,B,C
bn1g = Gibbs_sampling(bn1)
## Inference_method.max_display_level = 2   # detailed tracing for all inference methods
bn1g.query(A,{})
## bn1g.query(C,{})
## bn1g.query(A,{C:True})
## bn1g.query(B,{A:True,C:False})

from probGraphicalModels import bn2,Al,Fi,Le,Re,Sm,Ta
bn2g = Gibbs_sampling(bn2)
## bn2g.query(Ta,{Re:True},number_samples=100000)

