# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 15:00:45 2020

@author: Or6699
"""

import sys
from ACO import AntForNQueen


if __name__ == "__main__":
    
    orig_stdout = sys.stdout
    f = open('out.txt', 'w')
    
    sys.stdout = f            # output write to the file directly.
          
    n_iter = 100              # number of legal iteration to find a solution.
    n_ant = 200               # number of ants every iteration.
    n_queens = 64             # number of queens to search.
    
    ant_colony = AntForNQueen(n_queens, n_ant, n_iter, rho=0.05, alpha=1, beta=1.5)
    ant_colony.run()
    
    sys.stdout = orig_stdout
    f.close()
