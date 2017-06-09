# probVariables.py - Probabilistic Variables
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

class Variable(object):
    """A random variable.
    name (string) - name of the variable
    domain (list) - a list of the values for the variable.
    Variables are ordered according to their name.
    """

    def __init__(self,name,domain):
        self.name = name
        self.size = len(domain)
        self.domain = domain
        self.val_to_index = {} # map from domain to index
        for i,val in enumerate(domain):
            self.val_to_index[val]=i

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Variable('"+self.name+"')"

