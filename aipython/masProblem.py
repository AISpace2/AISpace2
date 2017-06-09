# masProblem.py - A Multiagent Problem
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from utilities import Displayable

class Node(Displayable):
    """A node in a search tree. It has a
    name a string
    isMax is True if it is a maximizing node, otherwise it is minimizing node
    children is the list of children
    value is what it evaluates to if it is a leaf.
    """
    def __init__(self, name, isMax, value, children):
        self.name = name
        self.isMax = isMax
        self.value = value
        self.allchildren = children
        
    def isLeaf(self):
        """returns true of this is a leaf node"""
        return self.allchildren is None
    
    def children(self):
        """returns the list of all children."""
        return self.allchildren
    
    def evaluate(self):
        """returns the evaluation for this node if it is a leaf"""
        return self.value

fig10_5 = Node("a",True,None, [
            Node("b",False,None, [
                Node("d",True,None, [
                    Node("h",False,None, [
                        Node("h1",True,7,None),
                        Node("h2",True,9,None)]),
                    Node("i",False,None, [
                        Node("i1",True,6,None),
                        Node("i2",True,888,None)])]),
                Node("e",True,None, [
                    Node("j",False,None, [
                        Node("j1",True,11,None),
                        Node("j2",True,12,None)]),
                    Node("k",False,None, [
                        Node("k1",True,888,None),
                        Node("k2",True,888,None)])])]),
            Node("c",False,None, [
                Node("f",True,None, [
                    Node("l",False,None, [
                        Node("l1",True,5,None),
                        Node("l2",True,888,None)]),
                    Node("m",False,None, [
                        Node("m1",True,4,None),
                        Node("m2",True,888,None)])]),
                Node("g",True,None, [
                    Node("n",False,None, [
                        Node("n1",True,888,None),
                        Node("n2",True,888,None)]),
                    Node("o",False,None, [
                        Node("o1",True,888,None),
                        Node("o2",True,888,None)])])])])
                        

class Magic_sum(Node):
    def __init__(self, xmove=True, last_move=None,
                 available=[1,2,3,4,5,6,7,8,9], x=[], o=[]):
        """This is a node in the search for the magic-sum game.
        xmove is True if the next move belongs to X.
        last_move is the number selected in the last move
        available is the list of numbers that are available to be chosen
        x is the list of numbers already chosen by x
        o is the list of numbers already chosen by o
        """
        self.isMax = self.xmove = xmove
        self.last_move = last_move
        self.available = available
        self.x = x
        self.o = o
        self.allchildren = None   #computed on demand
        lm = str(last_move)
        self.name = "start" if not last_move else "o="+lm if xmove else "x="+lm

    def children(self):
        if self.allchildren is None:
            if self.xmove:
                self.allchildren = [
                    Magic_sum(xmove = not self.xmove,
                              last_move = sel,
                              available = [e for e in self.available if e is not sel],
                              x = self.x+[sel],
                              o = self.o)
                            for sel in self.available]
            else:
                self.allchildren = [
                    Magic_sum(xmove = not self.xmove,
                              last_move = sel,
                              available = [e for e in self.available if e is not sel],
                              x = self.x,
                              o = self.o+[sel])
                            for sel in self.available]
        return self.allchildren

    def isLeaf(self):
        """A leaf has no numbers available or is a win for one of the players.
        We only need to check for a win for o if it is currently x's turn,
        and only check for a win for x if it is o's turn (otherwise it would
        have been a win earlier).
        """
        return (self.available == [] or
                (sum_to_15(self.last_move,self.o)
                 if self.xmove
                 else sum_to_15(self.last_move,self.x)))

    def evaluate(self):
        if self.xmove and sum_to_15(self.last_move,self.o):
            return -1
        elif not self.xmove and sum_to_15(self.last_move,self.x):
            return 1
        else:
            return 0
            
def sum_to_15(last,selected):
    """is true if last, toegether with two other elements of selected sum to 15.
    """
    return any(last+a+b == 15
               for a in selected if a != last
               for b in selected if b != last and b != a)

