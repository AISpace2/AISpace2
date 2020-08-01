# cspProblem.py - Representations of a Constraint Satisfaction Problem
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import itertools

from aipython.utilities import Displayable, dict_union
from operator import *


class Constraint(object):
    """A Constraint consists of
    * name: the unique name of this constraint
    * scope: a tuple of variables
    * condition: a function that can applied to a tuple of values
    * string: a string for printing the constraints. All of the strings must be unique.
    for the variables
    """

    def __init__(self, scope, condition, string=None):
        self.scope = scope
        self.condition = condition
        if self.condition.__name__ == "<lambda>":
            self.condition.__name__ = "Custom"
        self.condition_name = self.condition.__name__
        if string is None:
            self.string = self.condition.__name__ + str(self.scope)
        else:
            self.string = string

    def __repr__(self):
        return repr(self.string)

    def holds(self, assignment):
        """returns the value of Constraint con evaluated in assignment.
        precondition: all variables are assigned in assignment
        """
        return self.condition(*tuple(assignment[v] for v in self.scope))


class CSP(Displayable):
    """A CSP consists of
    * domains, a dictionary that maps each variable to its domain
    * constraints, a list of constraints
    * positions, a dictionary that maps name of each node into its (x,y)-position.
    """

    def __init__(self, domains, constraints, positions={}):
        self.variables = set(domains)
        self.domains = domains
        self.constraints = sorted(constraints, key=lambda con: con.__repr__())
        self.var_to_const = {var: set() for var in self.variables}
        for con in self.constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)
        self.positions = positions

    def __str__(self):
        """string representation of CSP"""
        return str(self.domains)

    def __repr__(self):
        """more detailed string representation of CSP"""
        return "CSP(" + str(self.domains) + ", " + str([str(c) for c in self.constraints]) + ")"

    def consistent(self, assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                   for con in self.constraints
                   if all(v in assignment for v in con.scope))

    # return the combinations of variables where the constraint cons holds
    def get_combinations_for_true(self, cons):
        combinationsForTrue = []
        ordered_vars = []
        ordered_domains = []
        for var, domain in self.domains.items():
            if var in cons.scope:
                ordered_vars.append(var)
                ordered_domains.append(list(domain))
        for combination in itertools.product(*ordered_domains):
            assignment = dict(zip(ordered_vars, list(combination)))
            if cons.holds(assignment):
                combinationsForTrue.append(assignment)
        return combinationsForTrue

# Constraint Functions:

# Negate the input function
# def NOT(fn):
#     def toReturn(*args, **kwargs):
#         return not fn(*args, **kwargs)
#     toReturn.__name__ = "NOT(" + fn.__name__ + ")"
#     return toReturn

def implies(bool1, bool2):
    return (not bool1) or bool2

def ne_(val):
    """not equal value"""
    # nev = lambda x: x != val   # alternative definition
    # nev = partial(neq,val)     # another alternative definition
    def nev(x):
        return val != x
    nev.__name__ = "ne_(" + str(val) + ")"      # name of the function 
    return nev

def eq_(val):
    """equal value"""
    # eqv = lambda x: x == val   # alternative definition
    # eqv = partial(eq,val)      # another alternative definition
    def eqv(x):
        return val == x
    eqv.__name__ = "eq_(" + str(val) + ")"
    return eqv

def lt_(val):
    # ltv = lambda x: x < val   # alternative definition
    # ltv = partial(lt,val)      # another alternative definition
    def ltv(x):
        return val > x
    ltv.__name__ = "lt_(" + str(val) + ")"
    return ltv

def gt_(val):
    # gtv = lambda x: x > val   # alternative definition
    # gtv = partial(gt,val)      # another alternative definition
    def gtv(x):
        return val < x
    gtv.__name__ = "gt_(" + str(val) + ")"
    return gtv

def le_(val):
    # lev = lambda x: x < val   # alternative definition
    # lev = partial(le,val)      # another alternative definition
    def lev(x):
        return val > x
    lev.__name__ = "le_(" + str(val) + ")"
    return lev

def ge_(val):
    # gev = lambda x: x > val   # alternative definition
    # gev = partial(ge,val)      # another alternative definition
    def gev(x):
        return val < x
    gev.__name__ = "ge_(" + str(val) + ")"
    return gev

csp_empty = CSP({}, [])

csp_simple1 = CSP({'A': {1, 2, 3}, 'B': {1, 2, 3}, 'C': {1, 2, 3}},
                  [Constraint(('A', 'B'), lt, "A < B"),
                   Constraint(('B', 'C'), lt, "B < C")])

C0 = Constraint(('A','B'), lt, "A < B")
C1 = Constraint(('B',), ne_(2), "B != 2")
C2 = Constraint(('B','C'), lt, "B < C")
csp_simple2 = CSP({'A':{1,2,3,4},'B':{1,2,3,4}, 'C':{1,2,3,4}},
                [C0, C1, C2],
                positions={"A": (1, 0),
                            "B": (3, 0),
                            "C": (5, 0),
                            "A < B": (2, 1),
                            "B < C": (4, 1),
                            "B != 2": (3, 2)})

csp_simple3 = CSP({'A': {1, 2, 3, 4}, 'B': {1, 2, 3, 4}, 'C': {1, 2, 3, 4}},
                  [Constraint(('A', 'B'), eq, "A = B"),
                   Constraint(('B', 'C'), eq, "B = C"),
                   Constraint(('A', 'C'), ne, "A != C")])

csp_extended1 = CSP({'A':{1,2,3,4},'B':{1,2,3,4}, 'C':{1,2,3,4}, 
                    'D':{1,2,3,4}, 'E':{1,2,3,4}},
                    [ Constraint(('B',), ne_(3), "B != 3"),
                    Constraint(('C',), ne_(2), "C != 2"),
                    Constraint(('A','B'), ne, "A != B"),
                    Constraint(('B','C'), ne, "A != C"),
                    Constraint(('C','D'), lt, "C < D"),
                    Constraint(('A','D'), eq, "A = D"),
                    Constraint(('A','E'), gt, "A > E"),
                    Constraint(('B','E'), gt, "B > E"),
                    Constraint(('C','E'), gt, "C > E"),
                    Constraint(('D','E'), gt, "D > E"),
                    Constraint(('B','D'), ne, "B != D")])


csp_extended2 = CSP({'A': {1, 2, 3, 4},
                     'B': {1, 2, 4},
                     'C': {1, 3, 4},
                     'D': {1, 2, 3, 4},
                     'E': {1, 2, 3, 4}, },
                    [Constraint(('A', 'B'), ne, "A != B"),
                     Constraint(('A', 'D'), eq, "A = D"),
                     Constraint(('B', 'D'), ne, "B != D"),
                     Constraint(('B', 'C'), ne, "B != C"),
                     Constraint(('C', 'D'), lt, "C < D"),
                     Constraint(('E', 'A'), lt, "E < A"),
                     Constraint(('E', 'D'), lt, "E < D"),
                     Constraint(('E', 'C'), lt, "E < C"),
                     Constraint(('E', 'B'), lt, "E < B")])

csp_extended3 = CSP({'A':{1,2,3,4},'B':{1,2,3,4}, 'C':{1,2,3,4}, 
                    'D':{1,2,3,4}, 'E':{1,2,3,4}},
                    [Constraint(('A','B'), ne, "A != B"),
                    Constraint(('A','D'), lt, "A < D"),
                    Constraint(('A','E'), lambda a,e: (a-e)%2 == 1, "A-E is odd"), # A-E is odd
                    Constraint(('B','E'), lt, "B < E"),
                    Constraint(('D','C'), lt, "D < C"),
                    Constraint(('C','E'), ne, "C != E"),
                    Constraint(('D','E'), ne, "D != E")])


def meet_at(p1, p2):
    """returns a function that is true when the words meet at the postions p1, p2
    """
    def meets(w1, w2):
        return w1[p1] == w2[p2]
    meets.__name__ = "meet_at(" + str(p1) + ',' + str(p2) + ')'
    return meets


csp_crossword1 = CSP({'one_across': {'ant', 'big', 'bus', 'car', 'has'},
                      'one_down': {'book', 'buys', 'hold', 'lane', 'year'},
                      'two_down': {'ginger', 'search', 'symbol', 'syntax'},
                      'three_across': {'book', 'buys', 'hold', 'land', 'year'},
                      'four_across': {'ant', 'big', 'bus', 'car', 'has'}},
                     [Constraint(('one_across', 'one_down'), meet_at(0, 0)),
                      Constraint(('one_across', 'two_down'), meet_at(2, 0)),
                      Constraint(('three_across', 'two_down'), meet_at(2, 2)),
                      Constraint(('three_across', 'one_down'), meet_at(0, 2)),
                      Constraint(('four_across', 'two_down'), meet_at(0, 4))])

words1 = {"add", "age", "aid", "aim", "air", "are", "arm", "art",
          "bad", "bat", "bee", "boa", "dim", "ear", "eel", "eft", "lee", "oaf"}

csp_crossword2 = CSP({'1_down': words1, '2_down': words1, '3_down': words1,
                      '1_across': words1, '4_across': words1, '5_across': words1},
                     [Constraint(('1_down', '1_across'), meet_at(0, 0)),  # 1_down[0]=1_across[0]
                      # 1_down[1]=4_across[0]
                      Constraint(('1_down', '4_across'), meet_at(1, 0)),
                      Constraint(('1_down', '5_across'), meet_at(2, 0)),
                      Constraint(('2_down', '1_across'), meet_at(0, 1)),
                      Constraint(('2_down', '4_across'), meet_at(1, 1)),
                      Constraint(('2_down', '5_across'), meet_at(2, 1)),
                      Constraint(('3_down', '1_across'), meet_at(0, 2)),
                      Constraint(('3_down', '4_across'), meet_at(1, 2)),
                      Constraint(('3_down', '5_across'), meet_at(2, 2))
                      ])

words2 = {"add", "ado", "age", "ago", "aid", "ail", "aim", "air",
          "and", "any", "ape", "apt", "arc", "are", "ark", "arm", "art", "ash",
          "ask", "auk", "awe", "awl", "aye", "bad", "bag", "ban", "bat", "bee",
          "boa", "dim", "ear", "eel", "eft", "far", "fat", "fit", "lee", "oaf",
          "rat", "tar", "tie"}

csp_crossword3 = CSP({'A1': words2, 'A2': words2, 'A3': words2,
                      'D1': words2, 'D2': words2, 'D3': words2},
                     [Constraint(('A2', 'D2'), meet_at(1, 1)),
                      Constraint(('A2', 'D1'), meet_at(0, 1)),
                      Constraint(('A1', 'D2'), meet_at(1, 0)),
                      Constraint(('A2', 'D3'), meet_at(2, 1)),
                      Constraint(('A1', 'D1'), meet_at(0, 0)),
                      Constraint(('A3', 'D2'), meet_at(1, 2)),
                      Constraint(('A1', 'D3'), meet_at(2, 0)),
                      Constraint(('A3', 'D1'), meet_at(0, 2)),
                      Constraint(('A3', 'D3'), meet_at(2, 2))
                      ])


def is_word(*letters, words=words1):
    """is true if the letters concatenated form a word in words"""
    return "".join(letters) in words


letters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
           "z"}

csp_crossword2d = CSP({'p00': letters, 'p01': letters, 'p02': letters,
                       'p10': letters, 'p11': letters, 'p12': letters,
                       'p20': letters, 'p21': letters, 'p22': letters},
                      [Constraint(('p00', 'p01', 'p02'), is_word),
                       Constraint(('p10', 'p11', 'p12'), is_word),
                       Constraint(('p20', 'p21', 'p22'), is_word),
                       Constraint(('p00', 'p10', 'p20'), is_word),
                       Constraint(('p01', 'p11', 'p21'), is_word),
                       Constraint(('p02', 'p12', 'p22'), is_word)])


def Queens(a, b):
    return a != b


csp_five_queens = CSP(
    domains={'A': [1, 2, 3, 4, 5], 'B': [1, 2, 3, 4, 5], 'C': [
        1, 2, 3, 4, 5], 'D': [1, 2, 3, 4, 5], 'E': [1, 2, 3, 4, 5]},
    constraints=[Constraint(('C', 'D'), Queens), Constraint(('A', 'D'), Queens), Constraint(('B', 'D'), Queens), Constraint(('B', 'C'), Queens), Constraint(
        ('A', 'C'), Queens), Constraint(('A', 'B'), Queens), Constraint(('D', 'E'), Queens), Constraint(('C', 'E'), Queens), Constraint(('B', 'E'), Queens), Constraint(('A', 'E'), Queens)],
    positions={
        "B": (213, 179),
        "Queens('A', 'E')": (550, 99),
        "Queens('A', 'B')": (285, 112),
        "C": (288, 406),
        "Queens('B', 'C')": (195, 304),
        "D": (587, 404),
        "E": (618, 172),
        "Queens('D', 'E')": (672, 313),
        "Queens('C', 'E')": (520, 314),
        "Queens('A', 'C')": (333, 227),
        "Queens('B', 'D')": (365, 312),
        "Queens('A', 'D')": (536, 229),
        "Queens('B', 'E')": (425, 163),
        "A": (437, 56),
        "Queens('C', 'D')": (446, 457)})

csp_eight_queens = CSP(
    domains={'N0': [1, 2, 3, 4, 5, 6, 7, 8], 'N1': [1, 2, 3, 4, 5, 6, 7, 8], 'N2': [1, 2, 3, 4, 5, 6, 7, 8], 'N3': [1, 2, 3, 4, 5, 6, 7, 8], 'N4': [
        1, 2, 3, 4, 5, 6, 7, 8], 'N5': [1, 2, 3, 4, 5, 6, 7, 8], 'N6': [1, 2, 3, 4, 5, 6, 7, 8], 'N7': [1, 2, 3, 4, 5, 6, 7, 8]},
    constraints=[Constraint(('N0', 'N1'), Queens), Constraint(('N0', 'N2'), Queens), Constraint(('N0', 'N3'), Queens), Constraint(('N0', 'N4'), Queens), Constraint(('N0', 'N5'), Queens), Constraint(('N0', 'N6'), Queens), Constraint(('N0', 'N7'), Queens), Constraint(('N1', 'N2'), Queens), Constraint(('N1', 'N3'), Queens), Constraint(('N1', 'N4'), Queens), Constraint(('N1', 'N5'), Queens), Constraint(('N1', 'N6'), Queens), Constraint(('N1', 'N7'), Queens), Constraint(('N2', 'N3'), Queens), Constraint(
        ('N2', 'N4'), Queens), Constraint(('N2', 'N5'), Queens), Constraint(('N2', 'N6'), Queens), Constraint(('N2', 'N7'), Queens), Constraint(('N3', 'N4'), Queens), Constraint(('N3', 'N5'), Queens), Constraint(('N3', 'N6'), Queens), Constraint(('N3', 'N7'), Queens), Constraint(('N4', 'N5'), Queens), Constraint(('N4', 'N6'), Queens), Constraint(('N4', 'N7'), Queens), Constraint(('N5', 'N6'), Queens), Constraint(('N5', 'N7'), Queens), Constraint(('N6', 'N7'), Queens)],
    positions={'N0': (7334.118, 5064.5146), 'N1': (7194.1904, 5117.885), 'N2': (7105.7144, 5235.2134), 'N3': (7200.921, 5347.732), 'N4': (7339.404, 5391.4854), 'N5': (7504.816, 5342.923), 'N6': (7568.2856, 5236.1753), 'N7': (7493.7554, 5108.7524)})

# def test(CSP_solver, csp=csp_simple2, solutions=[{'A': 1, 'B': 3, 'C': 4}, {'A': 2, 'B': 3, 'C': 4}]):
#     """CSP_solver is a solver that finds a solution to a CSP.
#     CSP_solver takes a csp and returns a solution.
#     csp has to be a CSP, where solutions is the list of all solutions.
#     This tests whether the solution returned by CSP_solver is a solution.
#     """
#     print("Testing csp with", CSP_solver.__doc__)
#     sol0 = CSP_solver(csp)
#     print("Solution found:", sol0)
#     assert sol0 in solutions, "Solution not found for " + str(csp)
#     print("Passed unit test")