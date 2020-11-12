# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:59:41 2020

@author: Or6699
"""

import numpy as np
from Ant import Ant
import functions as func

"""
A class for defining an Ant Colony Optimizer for n-queen solving.
The c'tor receives the following arguments:
    Queens: queens list (list size of dim) 
    Nant: Colony size (number of ants)
    Niter: maximal number of iterations to be run.
    rho: evaporation constant.
    alpha: pheromones' exponential weight in the nextMove calculation.
    beta: heuristic information's (eta) exponential weight in the nextMove calculation.
    seed: random number generator's seed.
"""


class AntForNQueen(object):
    def __init__(self, dim=8, n_ant=1, n_iter=1000, rho=0.05, alpha=1, beta=1.5, seed=None):
        self.Queens = func.initialize_n_queen_node(dim)
        self.dim = dim
        self.Nant = n_ant
        self.Niter = n_iter
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.local_state = np.random.RandomState(seed)
        self.last_good_solution = []
        self.solutions_count = 2
        self.printed_solutions_count = 0

    # This method invokes the ACO search over the n-queen graph.
    # It didn't return value.
    # Importantly, 'all_ants' is a list of Ant obj.
    # Notably, every individual 'path' is a list of edges, each represented by a pair of nodes.
    # if ant will find solutions_count good solution for n-queens it return true and finish this run.
    def run(self):
        for i in range(self.Niter):
            print("iter num: ", i + 1)
            all_ants = self.construct_colony_of_ants()
          
            for t in range(self.dim):
                if t == 0:
                    self.run_one_step_all_ants(all_ants, t, True) 
                else:
                    self.run_one_step_all_ants(all_ants, t, False)
            
            finish = self.update_pheromones(all_ants)
            if finish:
                return 

    # This method deposits pheromones on the "edges" between the queens.
    # pheromones save at dictionary for only need update.
    def update_pheromones(self, all_ants):

        # evaporation all pheromones.
        for i in range(self.dim):
            d = self.Queens[i].Dist
            d.update((k, v * (1 - self.rho)) for k, v in d.items())

        # update new pheromones. (deposit)
        for i in range(self.Nant):
            self.printed_solutions_count += self.deposit_pheromones(all_ants[i])
            if self.printed_solutions_count == self.solutions_count:
                return True  # find 2 different tour, end run.
  
    # This method deposit pheromones on a tour per an ant, starting from node 'start'
    def deposit_pheromones(self, ant):
        path = ant.path

        if ant.block:
            for i in range(len(path) - 1):
                qs = path[i][1]
                xs = path[i][0]
                xd = path[i + 1][0]
                string = str(xs) + str(xd)
                
                if i != len(path) - 1:
                    if self.Queens[qs].Dist.get(string, -1) != -1:
                        self.Queens[qs].Dist[string] += 2
                    else:
                        self.Queens[qs].Dist[string] = 2
                else:  # if ant is block, last step get punishment less pheromone.
                    if self.Queens[qs].Dist.get(string, -1) != -1: 
                        self.Queens[qs].Dist[string] += 0.5
                    else:
                        self.Queens[qs].Dist[string] = 0.5
            return 0             
        else:
            # if ant finish a tour successful. 
            if str(self.last_good_solution) != str(ant.path):
                self.last_good_solution = ant.path
                print("(x,y) ", ant.path)  
                func.print_chess(ant, self.dim)
                print("")
                return 1
            
            return 0
         
    # This method generates 'Nant' of ants, for the entire colony,
    # representing a single ant that try solving n-queens problem.
    def construct_colony_of_ants(self):
        all_ants = []
        
        for i in range(self.Nant):
            all_ants.append(Ant(self.dim, 0))
            
        return all_ants
    
    # This method is the one step of ants (first queen), for the entire colony,
    # representing a one single step for ant that try solving n-queens problem.
    def run_one_step_all_ants(self, all_ants, t, first):
        
        for i in range(self.Nant):
            if all_ants[i].block:
                if first:
                    x = self.local_state.randint(0, self.dim)
                else:
                    x = self.ant_movement(all_ants[i], t)
                    if x == -1:  # ant is block.
                        continue
                    
                y = all_ants[i].current_queen
                all_ants[i].path.append((x, y))
                all_ants[i].previous_queen_value = x
                all_ants[i].previous_queen = all_ants[i].current_queen
            
    # This method is the ant movement step of ant.
    def ant_movement(self, ant, t): 
        if ant.current_queen + 1 != self.dim:
            ant.current_queen += 1    
            pos = ant.path[-1]
            x = pos[0]
            y = pos[1]
            filter_values = ant.filter_values(x, y)
            queen_s = ant.previous_queen
            
            if len(filter_values) != 0:
                if len(filter_values) == 1:
                    return filter_values[0]
                
                selected_value = self.value_probability(ant, filter_values, self.Queens[queen_s].Dist, t)
                return selected_value
            else:
                ant.block = True
                return -1

    # This method probabilistically calculates the next move (next value to choice)
    # given a neighboring ants & rules of n-queens problem.
    # information per a single ant at a specified value.
    # The random generation relies on norm_row, as a vector of probabilities, using the numpy function 'choice'
    def value_probability(self, ant, filter_values, pheromone_dist, t):
        pheromone = np.ones(len(filter_values), dtype=int)

        for v in range(len(filter_values)):
            xs = ant.previous_queen_value  # source queen value.
            xd = filter_values[v]  # destination queen value.
            pheromone[v] = pheromone_dist.get(str(xs) + str(xd), 1)

            if pheromone[v] == 0:  # if first time using this value for destination queen.
                pheromone[v] = 1

        copy_pheromone = np.copy(pheromone)
        row = copy_pheromone ** self.alpha * ((func.oblivion_rate(t + 1)) ** self.beta)
        f_value_probability = row / row.sum()
        index = self.local_state.choice(range(len(filter_values)), 1, p=f_value_probability)
        return int(filter_values[index[0]])
