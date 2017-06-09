# probStochSim.py - Probabilistic inference using stochastic simulation
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import random
from probGraphicalModels import Inference_method

def sample_one(dist):
    """returns the index of a single sample from normalized distribution dist."""
    rand = random.random()*sum(dist.values())
    cum = 0     # cumulative weights
    for v in dist:
        cum += dist[v]
        if cum > rand:
            return v

def sample_multiple(dist, num_samples):
    """returns a list of num_samples values selected using distribution dist.
    dist is a value:weight dictionary that does not need to be normalized
    """
    total = sum(dist.values())
    rands = sorted(random.random()*total for i in range(num_samples))
    result = []
    dist_items = list(dist.items())
    cum = dist_items[0][1]    # cumulative sum
    index = 0
    for r in rands:
        while r>cum:
            index += 1
            cum += dist_items[index][1]
        result.append(dist_items[index][0])
    return result

def test_sampling(dist, num_samples):
    """Given a distribution, dist, draw num_samples samples
    and return the resulting counts
    """
    result = {v:0 for v in dist}
    for v in sample_multiple(dist, num_samples):
        result[v] += 1
    return result

# try the following queries a number of times each:
# test_sampling({1:1,2:2,3:3,4:4}, 100)
# test_sampling({1:1,2:2,3:3,4:4}, 100000)

class Sampling_inference_method(Inference_method):
    """The abstract class of sampling-based belief network inference methods"""
    def query(self,qvar,obs={},number_samples=1000,sample_order=None):
        raise NotImplementedError("Sampling_inference_method query")  # abstract

def select_sample_ordering(bn):
    """creates a sample ordering of factors such that the parents of a node
    are before the node.
    raises StopIteration if there is no such ordering. This would occur in next(.).
    """
    sample_order=[]
    defined = set()  # set of variables whose probability is defined
    factors_to_sample = bn.factors.copy()
    while factors_to_sample:
        fac = next(f for f in factors_to_sample
                   if all(par in defined for par in f.parents))
        factors_to_sample.remove(fac)
        sample_order.append(fac)
        defined.add(fac.child)
    return sample_order

class Rejection_sampling(Sampling_inference_method):
    """The class that queries Graphical Models using Rejection Sampling.

    bn is a belief network to query
    """
    def __init__(self,bn=None):
        self.bn = bn
        self.label = "Rejection Sampling"

    def query(self,qvar,obs={},number_samples=1000,sample_order=None):
        """computes P(qvar|obs) where
        qvar is a variable.
        obs is a variable:value dictionary.
        sample_order is a list of factors where factors defining the parents
          come before the factors for the child.
        """
        if sample_order is None:
            sample_order = select_sample_ordering(self.bn)
        self.display(2,*[f.child for f in sample_order],sep="\t")
        counts = {val:0 for val in qvar.domain}
        for i in range(number_samples):
            rejected = False
            sample = {}
            for fac in sample_order:
                nvar = fac.child     #next variable
                val = sample_one(fac.cond_dist(sample))
                self.display(2,val,end="\t")
                if nvar in obs and obs[nvar] != val:
                    rejected = True
                    self.display(2,"Rejected")
                    break
                sample[nvar] = val
            if not rejected:
                counts[sample[qvar]] += 1
                self.display(2,"Accepted")
        tot = sum(counts.values())
        return counts, {c:divide(v,tot) for (c,v) in counts.items()}

def divide(num,denom):
    """returns num/denom without divide-by-zero errors.
    defines 0/0 to be 1."""
    if denom == 0:
        return 1.0
    else:
        return num/denom

class Likelihood_weighting(Sampling_inference_method):
    """The class that queries Graphical Models using Likelihood weighting.

    bn is a belief network to query
    """
    def __init__(self,bn=None):
        self.bn = bn
        self.label = "Likelihood weighting"

    def query(self,qvar,obs={},number_samples=1000,sample_order=None):
        """computes P(qvar|obs) where
        qvar is a variable.
        obs is a variable:value dictionary.
        sample_order is a list of factors where factors defining the parents
          come before the factors for the child.
        """
        if sample_order is None:
            sample_order = select_sample_ordering(self.bn)
        self.display(2,*[f.child for f in sample_order
                            if f.child not in obs],sep="\t")
        counts = [0 for val in qvar.domain]
        for i in range(number_samples):
            sample = {}
            weight = 1.0
            for fac in sample_order:
                nvar = fac.child  # next variable sampled
                if nvar in obs:
                    sample[nvar] = obs[nvar]
                    weight *= fac.get_value(sample)
                else:
                    val = sample_one(fac.cond_dist(sample))
                    self.display(2,val,end="\t")
                    sample[nvar] = val
            counts[sample[qvar]] += weight
            self.display(2,weight)
        tot = sum(counts)
        return counts, {c:v/tot for (c,v) in counts.items()}

class Particle_filtering(Sampling_inference_method):
    """The class that queries Graphical Models using Particle Filtering.

    bn is a belief network to query
    """
    def __init__(self,bn=None):
        self.bn = bn
        self.label = "Particle Filtering"

    def query(self, qvar, obs={}, number_samples=1000, sample_order=None):
        """computes P(qvar|obs) where
        qvar is a variable.
        obs is a variable:value dictionary.
        sample_order is a list of factors where factors defining the parents
          come before the factors for the child.
        """
        if sample_order is None:
            sample_order = select_sample_ordering(self.bn)
        self.display(2,*[f.child for f in sample_order
                            if f.child not in obs],sep="\t")
        particles = [{} for i in range(number_samples)]
        for fac in sample_order:
            nvar = fac.child  # the variable sampled
            if nvar in obs:
                weights = {part:fac.cond_prob(part,obs[nvar]) for part in particles}
                particles = [p.copy for p in resample(particles, weights, number_samples)]
            else:
                for part in particles:
                    part[nvar] = sample_one(fac.cond_dist(part))
                self.display(2,part[nvar],end="\t")
        counts = [0 for val in qvar.domain]
        for part in particles:
            counts[part[qvar]] += 1
        self.display(2,weight)
        return counts

def resample(particles, weights, num_samples):
    """returns num_samples copies of particles resampled according to weights.
    particles is a list of particles
    weights is a list of positive numbers, of same length as particles
    num_samples is n integer
    """
    total = sum(weights)
    rands = sorted(random.random()*total for i in range(num_samples))
    result = []
    cum = weights[0]     # cumulative sum
    index = 0
    for r in rands:
        while r>cum:
            index += 1
            cum += weights[index]
        result.append(particles[index])
    return result

from probGraphicalModels import bn1, A,B,C
bn1r = Rejection_sampling(bn1)
bn1L = Likelihood_weighting(bn1)
## Inference_method.max_display_level = 2   # detailed tracing for all inference methods
## bn1r.query(A,{})
## bn1r.query(C,{})
## bn1r.query(A,{C:True})
## bn1r.query(B,{A:True,C:False})

from probGraphicalModels import bn2,Al,Fi,Le,Re,Sm,Ta
bn2r = Rejection_sampling(bn2)    # answers queries using rejection sampling
bn2L = Likelihood_weighting(bn2)    # answers queries using rejection sampling
bn2p = Particle_filtering(bn2)    # answers queries using particle filtering
## bn2r.query(Ta,{})
## bn2r.query(Ta,{})
## bn2r.query(Ta,{Re:True})
## Inference_method.max_display_level = 0 # no detailed tracing for all inference methods
## bn2r.query(Ta,{Re:True},number_samples=100000)
## bn2r.query(Ta,{Re:True,Sm:False})
## bn2r.query(Ta,{Re:True,Sm:False},number_samples=100)

## bn2L.query(Ta,{Re:True,Sm:False},number_samples=100)
## bn2L.query(Ta,{Re:True,Sm:False},number_samples=100)


from probGraphicalModels import bn3,Season, Sprinkler
from probGraphicalModels import Rained, Grass_wet, Grass_shiny, Shoes_wet
bn3r = Rejection_sampling(bn3)    # answers queries using rejection sampling
bn3L = Likelihood_weighting(bn3)    # answers queries using rejection sampling
bn3p = Particle_filtering(bn3)    # answers queries using particle filtering
#bn3r.query(Shoes_wet,{Grass_shiny:True,Rained:True})
#bn3L.query(Shoes_wet,{Grass_shiny:True,Rained:True})
#bn3p.query(Shoes_wet,{Grass_shiny:True,Rained:True})

import matplotlib.pyplot as plt

def plot_stats(method, what, qvar, obs, number_samples=100, number_runs=1000):
    """Plots a cumulative distribution of the prediction of the model.
    method is a Sampling_inference_method (that implements appropriate query(.))
    what is either "prob_ev" or the value of qvar to plot
    qvar is the query variable
    obs is the variable:value dictionary representing the observations
    number_samples is the number of samples for each run
    number_iterations is the number of runs that are plotted
    """
    plt.ion()
    plt.xlabel("value")
    plt.ylabel("Cumulative Number")
    Inference_method.max_display_level, prev_max_display_level = 0, Inference_method.max_display_level
    answers = [method.query(qvar,obs,number_samples=number_samples)
               for i in range(number_runs)]
    if what == "prob_ev":
        values = [sum(ans)/number_samples for ans in answers]
        label = method.label+"(prob of evidence)"
    else:
        values = [divide(ans[qvar.val_to_index[what]],sum(ans)) for ans in answers]
        label = method.label+" ("+str(qvar)+"="+str(what)+")"
    values.sort()
    plt.plot(values,range(number_runs),label=label)
    plt.legend(loc="upper left")
    plt.draw()
    Inference_method.max_display_level = prev_max_display_level   # restore display level


# plot_stats(bn2r,False,Ta,{Re:True,Sm:False},number_samples=1000, number_runs=1000)
# plot_stats(bn2L,False,Ta,{Re:True,Sm:False},number_samples=1000, number_runs=1000)
# plot_stats(bn2r,False,Ta,{Re:True,Sm:False},number_samples=100, number_runs=1000)
# plot_stats(bn2L,False,Ta,{Re:True,Sm:False},number_samples=100, number_runs=1000)
# plot_stats(bn3r,True,Shoes_wet,{Grass_shiny:True,Rained:True},number_samples=1000)
# plot_stats(bn3L,True,Shoes_wet,{Grass_shiny:True,Rained:True},number_samples=1000)
# plot_stats(bn2r,"prob_ev",Ta,{Re:True,Sm:False},number_samples=1000, number_runs=1000)
# plot_stats(bn2L,"prob_ev",Ta,{Re:True,Sm:False},number_samples=1000, number_runs=1000)

