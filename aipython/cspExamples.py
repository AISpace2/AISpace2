# cspExamples.py - Example CSPs
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from aipython.cspProblem import CSP, Constraint        
from operator import lt,ne,eq,gt

def ne_(val):
    """not equal value"""
    # nev = lambda x: x != val   # alternative definition
    # nev = partial(neq,val)     # another alternative definition
    def nev(x):
        return val != x
    nev.__name__ = str(val)+"!="      # name of the function 
    return nev

def is_(val):
    """is a value"""
    # isv = lambda x: x == val   # alternative definition
    # isv = partial(eq,val)      # another alternative definition
    def isv(x):
        return val == x
    isv.__name__ = str(val)+"=="
    return isv

csp0 = CSP({'A':{1,2,3},'B':{1,2,3}, 'C':{1,2,3}},
           [ Constraint(('A','B'),lt),
             Constraint(('B','C'),lt)])

csp1 = CSP({'A':{1,2,3,4},'B':{1,2,3,4}, 'C':{1,2,3,4}},
           [ Constraint(('A','B'),lt),
             Constraint(('B',),ne_(2)),
             Constraint(('B','C'),lt)])

csp2 = CSP({'A':{1,2,3,4},'B':{1,2,3,4}, 'C':{1,2,3,4}, 
            'D':{1,2,3,4}, 'E':{1,2,3,4}},
           [ Constraint(('B',),ne_(3)),
            Constraint(('C',),ne_(2)),
            Constraint(('A','B'),ne),
            Constraint(('B','C'),ne),
            Constraint(('C','D'),lt),
            Constraint(('A','D'),eq),
            Constraint(('A','E'),gt),
            Constraint(('B','E'),gt),
            Constraint(('C','E'),gt),
            Constraint(('D','E'),gt),
            Constraint(('B','D'),ne)])

def meet_at(p1,p2):
    """returns a function that is true when the words meet at the postions p1, p2
    """
    def meets(w1,w2):
        return w1[p1] == w2[p2]
    meets.__name__ = "meet_at("+str(p1)+','+str(p2)+')'
    return meets

crossword1 = CSP({'one_across':{'ant', 'big', 'bus', 'car', 'has'},
                  'one_down':{'book', 'buys', 'hold', 'lane', 'year'},
                  'two_down':{'ginger', 'search', 'symbol', 'syntax'},
                  'three_across':{'book', 'buys', 'hold', 'land', 'year'},
                  'four_across':{'ant', 'big', 'bus', 'car', 'has'}},
                  [Constraint(('one_across','one_down'),meet_at(0,0)),
                   Constraint(('one_across','two_down'),meet_at(2,0)),
                   Constraint(('three_across','two_down'),meet_at(2,2)),
                   Constraint(('three_across','one_down'),meet_at(0,2)),
                   Constraint(('four_across','two_down'),meet_at(0,4))])

words1 = {"add", "age", "aid", "aim", "air", "are", "arm", "art",
    "bad", "bat", "bee", "boa", "dim", "ear", "eel", "eft", "lee", "oaf"}
    
words2 = {"add", "ado", "age", "ago", "aid", "ail", "aim", "air",
    "and", "any", "ape", "apt", "arc", "are", "ark", "arm", "art", "ash",
    "ask", "auk", "awe", "awl", "aye", "bad", "bag", "ban", "bat", "bee",
    "boa", "dim", "ear", "eel", "eft", "far", "fat", "fit", "lee", "oaf",
    "rat", "tar", "tie"}
    
crossword2 = CSP({'1_down':words1, '2_down':words1, '3_down':words1,
                  '1_across':words1, '4_across':words1, '5_across':words1},
                  [Constraint(('1_down','1_across'),meet_at(0,0)), # 1_down[0]=1_across[0]
                   Constraint(('1_down','4_across'),meet_at(1,0)), # 1_down[1]=4_across[0]
                   Constraint(('1_down','5_across'),meet_at(2,0)),
                   Constraint(('2_down','1_across'),meet_at(0,1)),
                   Constraint(('2_down','4_across'),meet_at(1,1)),
                   Constraint(('2_down','5_across'),meet_at(2,1)),
                   Constraint(('3_down','1_across'),meet_at(0,2)),
                   Constraint(('3_down','4_across'),meet_at(1,2)),
                   Constraint(('3_down','5_across'),meet_at(2,2))
                   ])

def is_word(*letters, words=words1):
    """is true if the letters concatenated form a word in words"""
    return "".join(letters) in words

letters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
  "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
  "z"} 
crossword2d = CSP({"p00":letters, "p01":letters, "p02":letters,
                  "p10":letters, "p11":letters, "p12":letters,
                  "p20":letters, "p21":letters, "p22":letters},
                  [Constraint(("p00","p01","p02"), is_word),
                   Constraint(("p10","p11","p12"), is_word),
                   Constraint(("p20","p21","p22"), is_word),
                   Constraint(("p00","p10","p20"), is_word),
                   Constraint(("p01","p11","p21"), is_word),
                   Constraint(("p02","p12","p22"), is_word)])
                   
def test(CSP_solver, csp=csp1,
             solutions=[{'A': 1, 'B': 3, 'C': 4}, {'A': 2, 'B': 3, 'C': 4}]):
    """CSP_solver is a solver that finds a solution to a CSP.
    CSP_solver takes a csp and returns a solution. 
    csp has to be a CSP, where solutions is the list of all solutions.
    This tests whether the solution returned by CSP_solver is a solution.
    """
    print("Testing csp with",CSP_solver.__doc__)
    sol0 = CSP_solver(csp)
    print("Solution found:",sol0)
    assert sol0 in solutions, "Solution not found for "+str(csp)
    print("Passed unit test")

