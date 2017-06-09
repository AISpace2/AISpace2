# logicTopDown.py - Top-down Proof Procedure for Definite Clauses
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from logicProblem import yes

def prove(kb, ans_body, indent=""):
    """returns True if kb |- ans_body
    """
    kb.display(2,indent,'yes <-',' & '.join(ans_body))
    if ans_body:
        selected = ans_body[0]   # select first atom from ans_body
        if selected in kb.askables:
            return (yes(input("Is "+selected+" true? "))
                    and  prove(kb,ans_body[1:],indent+"    "))
        else:
            return any(prove(kb,cl.body+ans_body[1:],indent+"    ")
                       for cl in kb.clauses_for_atom(selected))
    else:
        return True    # empty body is true

from logicProblem import triv_KB
def test():
    a1 = prove(triv_KB,['i_am'])
    assert a1, "triv_KB proving i_am gave "+str(a1)
    a2 = prove(triv_KB,['i_smell'])
    assert not a2, "triv_KB proving i_smell gave "+str(a2it)
    print("Passed unit tests")
if __name__ == "__main__":
    test()   
# try
from logicProblem import elect
# elect.max_display_level=3  # give detailed trace
# prove(elect,['live_w6'])
# prove(elect,['lit_l1'])

