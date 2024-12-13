#!/bin/python3

'''assadiAlgorithm.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 10/6/24

Contains an implementation of Assadi's (1-eps) Sample and Solve probablistic algorithm.

#FIXME: Currently Functional for general graphs but not on hypergraphs, implementating in OOP can GREATLY improve performance

Refer to https://arxiv.org/abs/2307.02968 for more details on the algorithm.
'''

import math
import os
import random
import sys

from tools import getOddSubsets, set_cover

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../astar"))

from astar.maxMatching import MaxMatchingProblem
from astar.informedSearch import InformedSearch

def isFracMatching(G, fracMatching):
    """Checks to see if list is a fractional matching of G

    The following conditions must hold:
        - |fracMatching| == |E|
        - fracMatching[i] is between 0 and 1 (including)
        - For all v in V:
            - The summation of weights assigned 
            to the adjacent edges of the current 
            v are less than 1
        - For all sets S with odd elements in V:
            - The summation of weights of each edge 
            containing any vertex from S is less than 
            or equal to (|S|-1)/2

    Args:
        G (tuple): a Graph (V,E) where V is the set of vertices and E is the Edges 
        fracMatching (dict): Edges to assigned weights
    
    Returns:
        bool: whether the matching is a fractional matching
    """
    return False


def isFracOddSetCover(G, W, vertexWeights, oddSetWeights):
    """Checks to see if weights satisfy Fractional Odd Set 
    cover definition in G, if an edge doesn't satisfy it, it is also returned

    The following conditions must hold:
        - |vertexWeights| == |V|
        - |oddSetWeights| == |odd vertex sets| 
        - For all edges:
            - vertexWeights[edge[0]] 
                + vertexWeights[edge[1]]
                + summation of the oddSetWeights that contain E
                >= W

    Args:
        G (tuple): a Graph (V,E) where V is the set of vertices and E is the Edges 
        W (dicts): Edges to assigned weights
        vertexWeights (dict): vertices to real number
        oddSetWeights (dict): OddSetTuple to real number

    Returns:
        tuple: whether lists passed in satisfy the definition 
                of Fractional Odd Set cover and the tuples that didn't pass
    """

    #TODO: ENSURE ODDSETWEIGHT KEYS MATCH UP WITH EACH SUBSET

    if len(vertexWeights) != len(G.V):
        return False,[]
    
    oddSubsets = getOddSubsets(tuple(G.V))
    if len(oddSubsets) != len(oddSetWeights):
        return False, [] 

    rejected_edges = []
    for edge in G.E:
        running_foscp = vertexWeights[edge[0]] + vertexWeights[edge[1]]
        for oddSubset in oddSubsets:
            if edge[0] in oddSubset or edge[1] in oddSubset:
                running_foscp += oddSetWeights[oddSubset]

        if running_foscp < W[edge]:
            rejected_edges.append[edge]

    return len(rejected_edges) <= 0, rejected_edges


def assadiApproximateAlgorithm(G, eps):
    """ Implementation of Assadi's (1-eps) Approximation
    algorithm for weighted general matching

    Refer to https://arxiv.org/abs/2307.02968 for write up
    
    Epsilon is used to denote how well of an approximation is made.
    closer to 0 is better but performces worse asymptotically.

    Disclaimer:
        iterativeImportance is a complex hash-table storing the following information in the following structure

        iterativeImportance = {
            iterationInt : [
                {edge:[importanceVal, weightedProb]},
                totalImportanceVal
            ]
        }

    Args:
        G (tuple): a Graph (V,E) where V is the set of vertices and E is the Edges 
        W (dicts): Edges to assigned weights
        eps (int): (Epsilon) A number in the interval [0,1] 

    Returns:
        list: An approximated weight matching in G
    """
    
    if G.m < 2:
        return G.E
    
    LOGMODE = math.e

    # Rounds Up value when a float
    R = math.ceil((4/eps)*(math.log(G.m, LOGMODE)))

    iterativeImportance = {r:[{},0] for r in range(1, R+1)}
 
    totalWeight = 0

    currentImportance = iterativeImportance[1]


    # Initalize importance and data table
    for edge in G.E:
        currentImportance[0][edge] =  [1, 0]   # Importance of each edge
        currentImportance[1] += G.W[edge] * 1 # Total importance * weight of each edge
        totalWeight += G.W[edge]

    epsiProb = ((8*G.n*math.log(G.n*totalWeight))/eps)

    # Computes Probability for each edge
    for edge in G.E:
        importance = currentImportance[0][edge][0]
        totalImportance = currentImportance[1]

        weight = (importance * G.W[edge]) / totalImportance

        currentImportance[0][edge][1] = epsiProb * weight


    matchings = []
    for r in range(1, R):
        (VP, EP) = sampleSubGraph(G, iterativeImportance, r)

        GP = (2, len(VP), len(EP), EP)

        problem = MaxMatchingProblem(GP)
        matching = InformedSearch(problem).solution.state.E
        matchings.append(matching)

        vertex_set_in_matching = set()
        for edge in matching:
            vertex_set_in_matching.add(edge[0])
            vertex_set_in_matching.add(edge[1])

        vsim = list(vertex_set_in_matching)

        oddSubsetsOfVSIM = getOddSubsets(vsim)            
        
        #FIXME: MAKE WEIGHT SET HERE AND PASS IT ON, CURRENTLY JUST SETS EACH WEIGHT AS 1
        weightsOfOddSubsets = [1]*len(oddSubsetsOfVSIM)

        cover = set_cover(vsim, oddSubsetsOfVSIM)

        nextImportance = iterativeImportance[r+1]

        for edge in G.E:
            if edge not in cover:
                previousImportance = iterativeImportance[r][0][edge][1]
                nextImportance[0][edge] = [previousImportance*2, 0]
                nextImportance[1] += G.W[edge] * previousImportance*2

        totalImportance = nextImportance[1]
        for edge in G.E:
            importance = nextImportance[0][edge][0]

            weight = (importance * G.W[edge]) / totalImportance

            nextImportance[0][edge][1] = epsiProb * weight

    bestMatching = matchings[0]
    for matching in matchings[1:]:
        if len(bestMatching) > len(matching):
            bestMatching = matching

    return bestMatching

def sampleSubGraph(G, iterativeImportance, level):
    """Samples Edges based off probability. In particular, does reservoir sampling

    Args:
        G (tuple): a Graph (V,E) where V is the set of vertices and E is the Edges 
        iterativeImportance (dict): Table of information about edges per iteration
        level (int): which iteration of the edges

    Returns:
        list: list of edges in sequence based off weights
    """
    sampledEdges = []
    sampledVertices = []

    for edge in G.E:
        r = random.random()

        if r <= iterativeImportance[level][0][edge][1]:
            sampledEdges.append(edge)
            {sampledVertices.append(u) for u in edge}
            
    return (sampledVertices, sampledEdges)

