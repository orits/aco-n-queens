# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:13:44 2020

@author: Or6699
"""
import functions as func
import numpy as np

"""
A class for defining an Ant at n-queen solving problem.
The c'tor receives the following arguments:
    chessboard: ant own play chessboard that save all legil steps that the ant still can do.
    path: history of ant path/tour.
    block: flag true if the block and can't move to the next queen's choice because emputy moves.
    current_queen: ant current queen column position.
    previous_queen: ant previous queen column position.
    strat_queen: ant strat queen column position.
    previous_queen_value:  ant previous queen column value.
    n = 0
"""

class Ant:
    
    # Class Attribute
    chessboard = 0
    path = 0
    block = False
    current_queen = 0
    previous_queen = 0
    strat_queen = 0
    previous_queen_value = 0
    n = 0

    # Initializer / Instance Attributes
    def __init__(self, n, strat_queen):
      self.chessboard = func.initializeChessboardGraph(n)
      self.path = []
      self.current_queen = strat_queen
      self.previous_queen = strat_queen
      self.strat_queen = strat_queen
      self.n = n
     
    
    """
    This method is filter of the last move (x,y) values and update the chessboard legil steps.
    """     
    def filterValues(self, x, y):
        func.update_chessboard_graph(x, y, self.chessboard, self.n)
        y += 1
        col = self.chessboard[:,y:y + 1]
        l = np.where(col)
        return list(set(l[0]))
    