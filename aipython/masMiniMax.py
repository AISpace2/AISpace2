# masMiniMax.py - Minimax search with alpha-beta pruning
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

def minimax(node):
    """returns the value of node, and a best path for the agents
    """
    if node.isLeaf():
        return node.evaluate(),None
    elif node.isMax:
        max_score = -999
        max_path = None
        for C in node.children():
            score,path = minimax(C,depth+1)
            if score > max_score:
                max_score = score
                max_path = C.name,path
        return max_score,max_path
    else:
        min_score = 999
        min_path = None
        for C in node.children():
            score,path = minimax(C,depth+1)
            if score < min_score:
                min_score = score
                min_path = C.name,path
        return min_score,min_path

def minimax_alpha_beta(node,alpha,beta,depth=0):
    """node is a Node, alpha and beta are cutoffs, depth is the depth
    returns value, path
    where path is a sequence of nodes that results in the value"""
    node.display(2,"  "*depth,"minimax_alpha_beta(",node.name,", ",alpha, ", ", beta,")")
    best=None      # only used if it will be pruned
    if node.isLeaf():
        node.display(2,"  "*depth,"returning leaf value",node.evaluate())
        return node.evaluate(),None
    elif node.isMax:
        for C in node.children():
            score,path = minimax_alpha_beta(C,alpha,beta,depth+1)
            if score >= beta:    # beta pruning
                node.display(2,"  "*depth,"pruned due to beta=",beta,"C=",C.name)
                return score, None 
            if score > alpha:
                alpha = score
                best = C.name, path
        node.display(2,"  "*depth,"returning max alpha",alpha,"best",best)
        return alpha,best
    else:
        for C in node.children():
            score,path = minimax_alpha_beta(C,alpha,beta,depth+1)
            if score <= alpha:     # alpha pruning
                node.display(2,"  "*depth,"pruned due to alpha=",alpha,"C=",C.name)
                return score, None
            if score < beta:
                beta=score
                best = C.name,path
        node.display(2,"  "*depth,"returning min beta",beta,"best=",best)
        return beta,best

from masProblem import fig10_5, Magic_sum, Node

# Node.max_display_level=2   # print detailed trace
# minimax_alpha_beta(fig10_5, -9999, 9999,0)
# minimax_alpha_beta(Magic_sum(), -9999, 9999,0)

#To see how much time alpha-beta pruning can save over minimax, uncomment the following:
## import timeit
## timeit.Timer("minimax(Magic_sum())",setup="from __main__ import minimax, Magic_sum"
##              ).timeit(number=1)
## trace=False
## timeit.Timer("minimax_alpha_beta(Magic_sum(), -9999, 9999,0)",
##              setup="from __main__ import minimax_alpha_beta, Magic_sum"
##              ).timeit(number=1)

