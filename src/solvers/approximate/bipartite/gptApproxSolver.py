#!/bin/python3

'''gptSolver.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 09/30/24

'''

import os
import sys
from gptHelpers import BipartiteGraph, sample_and_solve

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from solver import Solver

class Approximate_Solver(Solver):

    def solve(self, G):
        '''Takes an instance G = (d, n, m, E) in the format parse_mmi
        produces.  Return a list contains d-edges as tuples of a maximum
        matching of G.
        '''
        
        (d, n, m, E) = G

        l,r = range(1,n+1), range(1,n+1)
        bipartite_graph = BipartiteGraph(l, r, E.keys())
        epsilon = 0.5  # You can choose any value between 0 and 1

        matching = sample_and_solve(bipartite_graph, epsilon)
       
        return matching

if __name__ == "__main__": 
    s = Approximate_Solver()
    s.do_main()

