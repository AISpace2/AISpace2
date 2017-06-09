# probFactors.py - Factor manipulation for graphical models
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from functools import reduce
#from probVariables import Variable

class Factor(object):
    nextid=0  # each factor has a unique identifier; for printing
    
    def __init__(self,variables):
        """variables is the ordered list of variables
        """
        self.variables = variables   # ordered list of variables
        # Compute the size and the offsets for the variables
        self.var_offsets = {}
        self.size = 1
        for i in range(len(variables)-1,-1,-1):
            self.var_offsets[variables[i]]=self.size
            self.size *= variables[i].size
        self.id = Factor.nextid
        Factor.nextid += 1

    def get_value(self,assignment):
        raise NotImplementedError("get_value")   # abstract method
        
    def __str__(self, variables=None):
        """returns a string representation of the factor.
        Allows for an arbitrary variable ordering.
        variables is a list of the variables in the factor 
        (can contain other variables)"""
        if variables==None:
            variables = self.variables
        else:
            variables = [v for v in variables if v in self.variables]
        res = ""
        for v in variables:
            res += str(v) + "\t"
        res += "f"+str(self.id)+"\n"
        for i in range(self.size):
            asst = self.index_to_assignment(i)
            for v in variables:
                res += str(asst[v])+"\t"
            res += str(self.get_value(asst))
            res += "\n"
        return res

    def brief(self):
        """returns a string representing a summary of the factor"""
        res = "f"+str(self.id)+"("
        for i in range(0,len(self.variables)-1):
            res += str(self.variables[i])+","
        if len(self.variables)>0:
            res += str(self.variables[len(self.variables)-1])
        res += ")"
        return res

    def assignment_to_index(self,assignment):
        """returns the index where the variable:value assignment is stored"""
        index = 0
        for var in self.variables:
            index += var.val_to_index[assignment[var]]*self.var_offsets[var]
        return index
        
    def index_to_assignment(self,index):
        """gives a dict representation of the variable assignment for index
        """
        asst = {}
        for i in range(len(self.variables)-1,-1,-1):
            asst[self.variables[i]] = self.variables[i].domain[index % self.variables[i].size]
            index = index // self.variables[i].size
        return asst

class Factor_stored(Factor):
    def __init__(self,variables,values):
        Factor.__init__(self, variables)
        self.values = values

    def get_value(self,assignment):
        return self.values[self.assignment_to_index(assignment)]

class Factor_observed(Factor):
    def __init__(self,factor,obs):
        Factor.__init__(self, [v for v in factor.variables if v not in obs])
        self.observed = obs
        self.orig_factor = factor

    def get_value(self,assignment):
        ass = assignment.copy()
        for ob in self.observed:
            ass[ob]=self.observed[ob]
        return self.orig_factor.get_value(ass)

class Factor_sum(Factor_stored):
    def __init__(self,var,factors):
        self.var_summed_out = var
        self.factors = factors
        vars = []
        for fac in factors:
            for v in fac.variables:
                if v is not var and v not in vars:
                    vars.append(v)
        Factor_stored.__init__(self,vars,None)
        self.values = [None]*self.size

    def get_value(self,assignment):
        """lazy implementation: if not saved, compute it. Return saved value"""
        index = self.assignment_to_index(assignment)
        if self.values[index]:
            return self.values[index]
        else:
            total = 0
            new_asst = assignment.copy()
            for val in self.var_summed_out.domain:
                new_asst[self.var_summed_out] = val
                prod = 1
                for fac in self.factors:
                    prod *= fac.get_value(new_asst)
                total += prod
            self.values[index] = total
            return total

def factor_times(variable,factors):
    """when factors are factors just on variable (or on no variables)"""
    prods= []
    facs = [f for f in factors if variable in f.variables]
    for val in variable.domain:
        prod = 1
        ast = {variable:val}
        for f in facs:
            prod *= f.get_value(ast)
        prods.append(prod)
    return prods
    
class Prob(Factor_stored):
    """A factor defined by a conditional probability table"""
    def __init__(self,var,pars,cpt):
        """Creates a factor from a conditional probability table, cptf. 
        The cpt values are assumed to be for the ordering par+[var]
        """
        Factor_stored.__init__(self,pars+[var],cpt)
        self.child = var
        self.parents = pars
        assert self.size==len(cpt),"Table size incorrect "+str(self)

    def cond_dist(self,par_assignment):
        """returns the distribution (a val:prob dictionary) over the child given
        assignment to the parents

        par_assignment is a variable:value dictionary that assigns values to parents
        """
        index = 0
        for var in self.parents:
            index += var.val_to_index[par_assignment[var]]*self.var_offsets[var]
        # index is the position where the disgribution starts
        return {self.child.domain[i]:self.values[index+i] for i in range(len(self.child.domain))}

    def cond_prob(self,par_assignment,child_value):
        """returns the probability child has child_value given
        assignment to the parents

        par_assignment is a variable:value dictionary that assigns values to parents
        child_value is a value to the child
        """
        index = self.child.val_to_index[child_value]
        for var in self.parents:
            index += var.val_to_index[par_assignment[var]]*self.var_offsets[var]
        return self.values[index]

class Factor_rename(Factor):
    def __init__(self,fac,renaming):
        Factor.__init__(self,list(renaming.keys()))
        self.orig_fac = fac
        self.renaming = renaming

    def get_value(self,assignment):
        return self.orig_fac.get_value({self.renaming[var]:val
                                        for (var,val) in assignment.items()
                                        if var in self.variables})

