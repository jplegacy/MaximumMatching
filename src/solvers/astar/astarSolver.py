#!/bin/python3

'''astarSolver.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 09/30/24

'''

from itertools import combinations
import os
import sys

from informedSearch import InformedSearch
from maxMatching import MaxMatchingProblem


sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from solver import Solver

class Astar_Solver(Solver):
    def solve(self, G):
        '''Takes an instance G = (d, n, m, E) in the format parse_mmi
        produces.  Return a list contains d-edges as tuples of a maximum
        matching of G.
        '''
        (d, n, m, E) = G

        edges = list(E.keys())
        G = (d, n, m, list(edges))
        problem = MaxMatchingProblem(G)
        
        return InformedSearch(problem).solution.state.E
    
if __name__ == "__main__":
    
    s = Astar_Solver()
    s.do_main()