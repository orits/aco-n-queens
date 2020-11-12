# -*- coding: utf-8 -*-
"""
@author: or6699.
"""
" this funtions is for useful to Ant Colony Optimizer for n-queen solving."

import numpy as np
from QueenNode import QueenNode
import pandas as pan
    
" this function initialize the chessboard graph."
def initializeChessboardGraph(n):
    G = np.ones((n,n), dtype = bool)       
    return G  

" this function initialize the n-queen list."
def initializeNQuenNode(n) :
    G = []
    for j in range(n) :
        G.append(QueenNode(j))
    return G  

"""
this function is the meta-heuristics desirability for selecting "edge" (x, y) values. 
"""
def oblivion_rate(t) :
    return 1 - (1 / (t ** 0.25))

"""
    this function update ant ligel next moves (arc consistency).
    x , y - it the position to update at the board.
    G - is the board graph.
    n - dim of the graph.
"""
def update_chessboard_graph(x, y, G, n) :
    #row
    G[x: x + 1] = False
    
    #col
    G[: , y:y + 1] = False
    
    #deago 
    r = np.arange(n)
    m1 = r[::-1,None] == r + n-x-y-1
    m2 = r[:,None] == r+x-y
    G[m1|m2] = False
   
"""
    this function print the finely any good solution at a board n X n with numbers of rows and columns.
    x , y - it the position to update at the board.
    G - is the board graph.
    n - dim of the graph.
"""
def print_chess(ant,dim):
    table=np.empty((dim,dim),dtype=object)
    path = ant.path
    for i in range(dim):
        for j in range(dim):
            table[i][j]='.'
    for i in range(len(path)):
        table[path[i][0]][path[i][1]] = 'Q'
     
    
    pan.set_option('display.max_columns', 1000) 
    pan.set_option('display.max_rows', 1000) 
    pan.set_option('display.width', 500)
    print(pan.DataFrame(table))