

'''linearApproximateMWM.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 10/6/24

Contains an impartial/incomplete implementation of Duan and Pettie's (1-eps) Linear-Time 
Approximation Algorithm approximately solving the Maximum Weight Matching Problem.

#FIXME: Currently not functional

Refer to https://dl.acm.org/doi/10.1145/2529989 for more details on the algorithm.
'''

import math
from tools import Graph


def theta(epsilon):
    """Ensures LTA is solved within (1-eps)

    Args:
        epsilon (float): float value in the interval (0,1]

    Returns:
        float: ideal epsilon
    """

    #FIXME: CORRECTLY CALCULATE THIS!
    
    return 1/4 # Never greater than 1/4

def isEligible(M, edge, yz, wi, di):
    """Follows (ii) and (iii) conditions of Eligibility defined for the Scaling Algorithm 

    Args:
        M (set): a set of edges which are a Matching
        edge (tuple): d-tuple
        yz (float): dual value corresponding to edge 
        wi (float): truncated weight corresponding to the edge
        di (float): scale value corresponding to the weight scale

    Returns:
        bool: whether the edge satifies Eligibility property 
    """

    if edge not in M and yz == (wi- di):
        return True

    if edge in M and (yz - wi) / di  > 0:
        return True
    
    return False

def getEligibleGraph(G, M, OM, yz, w, d, level):
    edgeEligible = []
    for edge in G.E:
        if isEligible(M, edge, yz[edge], w[level][edge], d[level][edge]):
            edgeEligible.append(edge)

    # Condition (iii) of eligibility
    for oddSubset in OM:
        for edge in G.E:
            for vertex in edge:
                if vertex in oddSubset:
                    edgeEligible.append(edge)

    return Graph(G.V, edgeEligible, G.W)

def getFreeVertices(G, matching):
    return {v for v in G.V if v not in {u for edge in matching for u in edge}}

def LTA(G, eps):
    """
    Implementation of Duan and Pettie's (1-eps) Linear-Time Approximation Algorithm
    approximately solving the Maximum Weight Matching Problems.

    Please refer to https://dl.acm.org/doi/10.1145/2529989 for more details on the algorithm below

    Args:
        G (Graph): Where V, E, M is defined
        eps (float): float value in the interval (0,1]

    Returns:
        list: Maximal Weight Matching
    """

    M = set()                   # Matching Set
    OM = set()                  # Blossoms

    eps_p = theta(eps)

    d = {0: theta(eps) * G.N}   # Delta Values
    w = {0:{d[0] * math.floor(G.w(edge)/d[0]) for edge in G.E}} # Truncated Weights

    y = {edge: (G.N/2) - (d[0]/2) for edge in G.V}
    yz = {edge: 2*((G.N/2) - (d[0]/2)) for edge in G.V}

    G_elig = getEligibleGraph(G, M, OM, yz, w, d, scale)

    L = math.log(G.N)
    for scale in range(L+1):
        d[scale] = d[0] / (2 ** scale)
        
        freeVertices = getFreeVertices(G_elig, M)
        augmentedPaths = findAugmentingPaths(G_elig, freeVertices)

        for path in augmentedPaths:
            for edge in path:
                M.add(edge)

        
        continue
    
    return False


def findAugmentingPaths():
    return

def dualAdjust():
    return 

if __name__ == "__main__": 
    G = Graph(
        [0,1], 
        [(0,1),(0,0),(1,1)],
        {(0,1):1,(0,0):1,(1,1):1}
        )
