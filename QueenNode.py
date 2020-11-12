# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 17:52:48 2020

@author: Or6699
"""
"""
A class for defining an queen at n-queen solving problem.
The c'tor receive queen_column: every node have a queen name like queen 0 mean queen the place at column 0 at the board.
and set Dist: dictionary the saving all the pheromones that deposit at all "edges" values between this queen ant next
queen at the board.   
"""


class QueenNode:

    # Initializer / Instance Attributes
    def __init__(self, queen_column):
        self.queen_column = queen_column
        self.Dist = {}
