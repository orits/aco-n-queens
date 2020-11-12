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
    chessboard: ant own play chessboard that save all legal steps that the ant still can do.
    path: history of ant path/tour.
    block: flag true if the block and can't move to the next queen's choice because empty moves.
    current_queen: ant current queen column position.
    previous_queen: ant previous queen column position.
    start_queen: ant start queen column position.
    previous_queen_value:  ant previous queen column value.
"""


class Ant:

    # Initializer / Instance Attributes
    def __init__(self, n, start_queen):
        self.chessboard = func.initialize_chessboard_graph(n)
        self.path = []
        self.block = False
        self.current_queen = start_queen
        self.previous_queen = start_queen
        self.start_queen = start_queen
        self.previous_queen_value = 0
        self.n = n

    """
    This method is filter of the last move (x,y) values and update the chessboard legal steps.
    """     
    def filter_values(self, x, y):
        func.update_chessboard_graph(x, y, self.chessboard, self.n)
        y += 1
        col = self.chessboard[:, y:y + 1]
        t_list = np.where(col)
        return list(set(t_list[0]))
