# cspConsistency.py - Arc Consistency and Domain splitting for solving a CSP
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from utilities import Displayable

class Con_solver(Displayable):
    def __init__(self, csp, **kwargs):
        """a CSP solver that uses arc consistency
        * csp is the CSP to be solved
        * kwargs is the keyword arguments for Displayable superclass
        """
        super().__init__(**kwargs)    # Or Displayable.__init__(self,**kwargs)
        self.csp = csp
        
    def make_arc_consistent(self, orig_domains=None, to_do=None):
        """Makes this CSP arc-consistent using generalized arc consistency
        orig_domains is the original domains
        to_do is a set of (variable,constraint) pairs
        returns the reduced domains
        """
        if orig_domains is None:
            orig_domains = self.csp.domains
        if to_do is None:
            to_do = {(var, const) for const in self.csp.constraints
                     for var in const.scope}
        else:
            to_do = to_do.copy()  # use a copy of to_do
        domains = orig_domains.copy()
        self.display(2,"Performing AC with domains", domains)
        while to_do:
            var, const = self.select_arc(to_do)
            self.display(3, "Processing arc (", var, ",", const, ")")
            other_vars = [ov for ov in const.scope if ov is not var]
            new_domain = {val for val in domains[var]
                          if self.any_holds(domains, const, {var: val}, other_vars)}
            if new_domain != domains[var]:
                self.display(4, "Arc: (", var, ",", const, ") is inconsistent")
                self.display(3, "Domain pruned", "dom(", var, ") =", new_domain,
                                 " due to ", const)
                domains[var] = new_domain
                add_to_do = self.new_to_do(var, const) - to_do
                to_do |= add_to_do      # set union
                self.display(3, "  adding", add_to_do if add_to_do else "nothing", "to to_do.")
            self.display(4, "Arc: (", var, ",", const, ") now consistent")
        self.display(2, "AC done. Reduced domains", domains)
        return domains

    def new_to_do(self, var, const):
        """returns new elements to be added to to_do after assigning
        variable var in constraint const.
        """
        return {(nvar, nconst) for nconst in self.csp.var_to_const[var]
                if nconst != const
                for nvar in nconst.scope
                if nvar != var}

    def select_arc(self, to_do):
        """Selects the arc to be taken from to_do .
        * to_do is a set of arcs, where an arc is a (variable,constraint) pair
        the element selected must be removed from to_do.
        """
        return to_do.pop() 

    def any_holds(self, domains, const, env, other_vars, ind=0):
        """returns True if Constraint const holds for an assignment
        that extends env with the variables in other_vars[ind:]
        env is a dictionary
        Warning: this has side effects and changes the elements of env
        """
        if ind == len(other_vars):
            return const.holds(env)
        else:
            var = other_vars[ind]
            for val in domains[var]:
                # env = dict_union(env,{var:val})  # no side effects!
                env[var] = val
                if self.any_holds(domains, const, env, other_vars, ind + 1):
                    return True
            return False

    def solve_one(self, domains=None, to_do=None):
        """return a solution to the current CSP or False if there are no solutions
        to_do is the list of arcs to check
        """
        if domains is None:
            domains = self.csp.domains
        new_domains = self.make_arc_consistent(domains, to_do)
        if any(len(new_domains[var]) == 0 for var in domains):
            return False
        elif all(len(new_domains[var]) == 1 for var in domains):
            self.display(2, "solution:", {var: select(
                new_domains[var]) for var in new_domains})
            return {var: select(new_domains[var]) for var in domains}
        else:
            var = select(x for x in self.csp.variables if len(new_domains[x]) > 1)
            if var:
                dom1, dom2 = partition_domain(new_domains[var])
                self.display(3, "...splitting", var, "into", dom1, "and", dom2)
                new_doms1 = copy_with_assign(new_domains, var, dom1)                
                new_doms2 = copy_with_assign(new_domains, var, dom2)
                to_do = self.new_to_do(var, None)
                return self.solve_one(new_doms1, to_do) or self.solve_one(new_doms2, to_do)

def partition_domain(dom):
    """partitions domain dom into two.
    """
    split = len(dom) // 2
    dom1 = set(list(dom)[:split])
    dom2 = dom - dom1
    return dom1, dom2
    
def copy_with_assign(domains, var=None, new_domain={True, False}):
    """create a copy of the domains with an assignment var=new_domain
    if var==None then it is just a copy.
    """
    newdoms = domains.copy()
    if var is not None:
        newdoms[var] = new_domain
    return newdoms

def select(iterable):
    """select an element of iterable. Returns None if there is no such element.

    This implementation just picks the first element.
    For many of the uses, which element is selected does not affect correctness, 
    but may affect efficiency.
    """
    for e in iterable:
        return e  # returns first element found

from cspExamples import test
def ac_solver(csp):
    "arc consistency (solve_one)"
    return Con_solver(csp).solve_one()
if __name__ == "__main__":
    test(ac_solver)

from searchProblem import Search_problem

class Search_with_AC_from_CSP(Search_problem,Displayable):
    """A search problem with arc consistency and domain splitting

    A node is a CSP """
    def __init__(self, csp):
        self.cons = Con_solver(csp)  #copy of the CSP
        self.domains = self.cons.make_arc_consistent()

    def is_goal(self, node):
        """node is a goal if all domains have 1 element"""
        return all(len(node[var])==1 for var in node)
    
    def start_nodes(self):
        return [self.domains]
    
    def neighbor_nodes(self,node):
        """an iterator over the neighboring nodes of node.
        This is used for depth-first search"""
        var = select(x for x in node if len(node[x])>1)
        if var:
            split = len(node[var])//2
            dom1 = set(list(node[var])[:split]) #a nonempty proper subset
            dom2 = node[var]-dom1
            self.display(2,"Splitting", var, "into", dom1, "and", dom2)
            to_do = self.cons.new_to_do(var,None)
            for dom in [dom1,dom2]:
                newdoms = copy_with_assign(node,var,dom)
                cons_doms = self.cons.make_arc_consistent(newdoms,to_do)
                if all(len(cons_doms[v])>0 for v in cons_doms):
                    # all domains are non-empty
                    yield cons_doms
                else:
                    self.display(2,"...",var,"in",dom,"has no solution")

from cspExamples import test
from searchDepthFirst import Depth_first_search

def ac_search_solver(csp):
    """arc consistency (search interface)"""
    sol = Depth_first_search(Search_with_AC_from_CSP(csp)).search()
    return {v:select(d) for (v,d) in sol.items()}
if __name__ == "__main__":
    test(ac_search_solver)

from cspExamples import csp1, csp2, crossword1, crossword2, crossword2d

## Test Solving CSPs with Arc consistency and domain splitting:
#Con_solver(csp1).solve_one()
#searcher1d = Depth_first_search(Search_with_AC_from_CSP(csp1))
#print(searcher1d.search())
#Depth_first_search.max_display_level = 2  # display search trace (0 turns off)
#searcher2c = Depth_first_search(Search_with_AC_from_CSP(csp2))
#print(searcher2c.search())
#searcher3c = Depth_first_search(Search_with_AC_from_CSP(crossword1))
#print(searcher3c.search())
#searcher4c = Depth_first_search(Search_with_AC_from_CSP(crossword2))
#print(searcher4c.search())
#searcher5c = Depth_first_search(Search_with_AC_from_CSP(crossword2d))
#print(searcher5c.search())

