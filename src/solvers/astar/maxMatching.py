#!/bin/python3

from itertools import combinations
from informedSearch import *

class MaxMatchingProblem(InformedProblemState):
    def __init__(self, G):
        (d, n, m, E) = G
        self.d = d
        self.n = n
        self.m = m
        self.E = E.copy()  
        self.vertex_set = set()  # A set of all vertices in the hypergraph

        for edge in E:
            self.vertex_set.update(edge)  # Add all vertices from each edge

    def heuristic(self):
        """
        Computes the heuristic value for the current state. This heuristic
        combines the number of unmatched vertices, the number of conflicts,
        and the number of unmatched edges.
        """
        # 1. Unmatched vertices
        unmatched_vertices = self.num_unmatched_vertices()

        # 2. Conflicts
        conflicts = self.num_of_conflicts()

        # 3. Unmatched edges (edges that are not yet part of the matching)
        unmatched_edges = self.num_unmatched_edges()

        # Weighted sum of all the factors
        alpha = 1.0
        beta = 2.0  # Conflicts are likely more costly to resolve than unmatched vertices
        gamma = 1.5  # Unmatched edges can also be a significant indicator

        return alpha * unmatched_vertices + beta * conflicts + gamma * unmatched_edges

    def num_unmatched_vertices(self):
        """
        Returns the number of vertices that are not yet matched in the current state.
        """
        matched_vertices = set()
        for edge in self.E:
            matched_vertices.update(edge)
        unmatched = len(self.vertex_set - matched_vertices)
        return unmatched

    def num_unmatched_edges(self):
        """
        Returns the number of edges that are not part of the matching.
        An edge is unmatched if it is not yet included in the matching.
        """
        unmatched_edges = 0
        for edge in self.E:
            if not self.is_matched(edge):
                unmatched_edges += 1
        return unmatched_edges

    def is_matched(self, edge):
        """
        A helper function to check if an edge is part of the matching.
        An edge is part of the matching if it doesn't conflict with any other edge.
        """
        for other_edge in self.E:
            if edge != other_edge and self.has_common_vertex(edge, other_edge):
                return False
        return True

    def has_common_vertex(self, edge1, edge2):
        """
        Checks if two edges share a common vertex.
        """
        return bool(set(edge1) & set(edge2))

    def num_of_conflicts(self):
        """
        Counts the number of conflicts (edges sharing vertices).
        """
        count = 0
        for edge1 in self.E:
            for edge2 in self.E:
                if edge1 != edge2 and self.has_common_vertex(edge1, edge2):
                    count += 1
        return count


    def has_no_conflicts(self):
        """
        Checks if there exists conflicts.
        """
        dt = [set() for _ in range(self.d)]

        for e in self.E:
            for i in range(self.d):
                # If a vertex is already used in the current dimension, it's not a valid matching
                if e[i] in dt[i]:
                    return False
                dt[i].add(e[i])
        return True
    
    def __str__(self):
        results = ""  
        for edge in self.E:
            results += '|'
            for vertex in edge:
                results += '|' + str(vertex) + '|'
            results += '|\n'
        return results

    def dictkey(self):
        """
        A method that generates a key that reflects the current state for
        isomorphism checking or uniqueness purposes.
        """
        results = ""
        for edge in self.E:
            for vertex in edge:
                results += str(vertex)
        return results

    def equals(self, state):
        return self.dictkey() == state.dictkey()

    def objective(self):
        return self.no_conflict_objective()

    def no_conflict_objective(self):
        return self.has_no_conflicts()

    def applyOperators(self):
        operations = []
        if len(self.E) > self.n:
            for subset in combinations(self.E, self.n):
                G = (self.d, self.n, self.m, list(subset))
                operations.append(MaxMatchingProblem(G))
        else:
            for i, edge_excluded in enumerate(self.E):
                edge_excluded_list = self.E[:i] + self.E[i+1:]
                G = (self.d, self.n, self.m, edge_excluded_list)
                operations.append(MaxMatchingProblem(G))
                
        return operations