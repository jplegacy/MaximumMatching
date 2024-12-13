#!/bin/python3

'''approximateMWMSolver.py

#FIXME: NOT WORKING WITH HYPERGRAPHS

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 09/30/24

'''

import os
import sys
from assadiAlgorithm import assadiApproximateAlgorithm
from tools import Graph

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from solver import Solver

class Approximate_Solver(Solver):

    def solve(self, G):
        '''Takes an instance G = (d, n, m, E) in the format parse_mmi
        produces.  Return a list contains d-edges as tuples of a maximum
        matching of G.
        '''
        (d, n, m, E) = G

        weights = {e:1 for e in E}

        GP = Graph([range(1,n+1)], list(E.keys()), weights)

        epsilon = 0.9

        matching = assadiApproximateAlgorithm(GP, epsilon)    

        return matching
    
if __name__ == "__main__": 
    s = Approximate_Solver()
    s.do_main()

