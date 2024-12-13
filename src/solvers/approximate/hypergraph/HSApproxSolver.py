#!/bin/python3

'''HSApproxSolver.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 11/16/24

Implements Hurkens and Schrijver (k+eps)/2 +  approximation algorithm for k-Set Packing problems

Refer to https://doi.org/10.1137/0402008 for more information
'''

from itertools import combinations
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from solver import Solver

class HS_Solver(Solver):

    def solve(self, G):
        '''Takes an instance G = (d, n, m, E) in the format parse_mmi
        produces.  Return a list contains d-edges as tuples of a maximum
        matching of G.
        '''
        (d, n, m, E) = G

        S = 1

        edges = E.keys()
                
        incrementedEdges = []
        if all(0 in edge for edge in edges):
            for edge in edges:
                incrementedEdge = []
                for v in edge:
                    incrementedEdge.append(v+1)
                    
                incrementedEdges.append(incrementedEdge)
                    
            edges = incrementedEdges

        partMapping = {}
        counter = 0
        for i in range(n+1):
            for j in range(d+1):
                counter += 1
                partMapping[(i,j)] = counter

        translatedEdges = {}
        reverseTranslation = {}
        
        for edge in edges:
            mapping = set()
            for currentColumn, v in enumerate(edge):
                mapping.add(partMapping[(v, currentColumn)])

            translatedEdges[edge] = mapping
            reverseTranslation[tuple(sorted(mapping))] = edge

        packings = HS(list(translatedEdges.values()), S)
        
        matching = set()
        for packing in packings:
            matching.add(reverseTranslation[tuple(sorted(packing))])

        return matching

def is_pairwise_disjoint(a, b):    
    running = set()
    for s in a:
        running = running.union(*a)

    for s in b:
        overlap = running.intersection(s)
        if len(overlap) != 0:
            return False
        
        running = running.union(*b)

    return True

def is_disjoint(a):
    running = set()
    
    for s in a:
        overlap = running.intersection(s)
        if len(overlap) != 0:
            return False
        
        running = running.union(a)
        
    return True
    
        
def replacement(sets, packing, p):
    for largerPSet in combinations(sets, p+1):
        if len(packing) == 0 and p == 1:
            return set(largerPSet)
        
        if not is_disjoint(largerPSet):
            continue

        for pSet in combinations(packing, p):
            pSetWithdrawn = packing - set(pSet)
                        
            lPS = set(largerPSet)
            if is_pairwise_disjoint(pSetWithdrawn, lPS):
                return pSetWithdrawn.union(lPS.copy())
            
    return packing

def HS(sets, s):
    packing = set()
    sets = [tuple(s) for s in sets]
        
    p = 0
    while p <= s:
        expandedPacking = replacement(sets, packing, p)
        
        if len(expandedPacking) == len(packing):
            p += 1
        else:
            packing = expandedPacking
            p = 0
    
    return packing
            
    
if __name__ == "__main__": 
    s = HS_Solver()
    s.do_main()

