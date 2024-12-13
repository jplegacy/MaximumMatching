#!/bin/python3

'''primeSolver.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 09/29/24

'''
import os
import sys

import sympy

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from solver import Solver


class Prime_Solver(Solver):
    """
    Currently, does not actually use any number-theoretical properties, 
    but does assign elements to prime numbers for when it is ready.

    Column-Row Vertices:
    The notion of Column-Row Vertices is treating 
    every traversal down an edge as a seperate vertex. Any permutation is fine. 
    
     Normal       Column-Row
    Vertices       Vertices
    
    1--1--1        1--2--3
    2--2--2 -----> 4--5--6
    3--3--3        7--8--9

    """

    def solve(self, G):
        '''Takes an instance G = (d, n, m, E) in the format parse_mmi
        produces.  Return a list contains d-edges as tuples of a maximum
        matching of G.
        '''
        (d, n, m, E) = G

        edges = []
        prime_mapping = {}
        prime_translation = {}
        prime_count = 0

        # Prime assignment to every sub-vertex
        for i in range(n):
            for j in range(d):
                prime_count += 1
                p = sympy.prime(prime_count)
                prime_mapping[(i,j)] = p

        for edge in E:
            mapping = []
            for current_column, v in enumerate(edge):
                mapping.append(prime_mapping[(v-1,current_column)])
            prime_translation[edge] = mapping
            edges.append(edge)

        conflicts = self.conflict_summation(edges, prime_translation)
        is_done = self.do_conflict_remain(conflicts)        
        
        results = self.recursive_traversal(edges, prime_mapping, prime_translation, is_done)
        
        return results

    def recursive_traversal(self, edges, crv_location, crv_edge_mapping, is_previous_min):
        """ 
        
        Args:
            edges (List): List of tuples representing edges
            crv_location (Dict): 2D Array Coordinates to identifier
            crv_edge_mapping (Dict): Edges mapped to their prime renamed edge
            is_previous_min (bool): If previous minimum was 1

        Returns:
            List: Returns Maximum Matching
        """
        heurstics = self.heuristic(edges, crv_edge_mapping)
        remove_edge_mins = self.minimum_valued_edges(heurstics)

        # Case: Already a Matching
        if is_previous_min == 1 and heurstics[remove_edge_mins[0]] == 1:
            return edges

        # Case: Single Conflict 
        if len(remove_edge_mins) == 1 and heurstics[remove_edge_mins[0]] == 1:
            clone = edges.copy()
            clone.remove(remove_edge_mins[0])
            return clone

        # Case: Multiple Conflicts
        max_remaining_edges = None

        for edge in remove_edge_mins:
            edge_list_removed = edges.copy()
            edge_list_removed.remove(edge)
            
            remaining_edges = self.recursive_traversal(edge_list_removed, crv_location, crv_edge_mapping, heurstics[edge])

            if max_remaining_edges == None or len(remaining_edges) > len(max_remaining_edges):
                max_remaining_edges = remaining_edges
            
        return max_remaining_edges           

    def conflict_summation(self, edges, crv_edge_mapping):
        """Coutns the number of times each column_row_vertex is found in an edge 

        Args:
            edges (list): List of tuples representing edges
            crv_edge_mapping (dict): Edges mapped to their prime renamed edge

        Returns:
            dict: Tuple, representing edge, to dictionary of every column_row_vertex, and the number of times they were found 
        """
        conflicts = {}
        for edge in edges:
            for crv in crv_edge_mapping[edge]:
                if conflicts.get(crv) == None:
                    conflicts[crv] = 0
                conflicts[crv] += 1

        return conflicts

    def do_conflict_remain(self, conflicts_dictionary):
        """Checks dictionary to see if any vertex is counted more than once

        Args:
            conflicts_dictionary (dict): column_row_vertices mapped to number of times counted

        Returns:
            bool: True if all elements were counted once, False otherwise
        """
        for crv in conflicts_dictionary:
            if conflicts_dictionary[crv] > 1:
                return False

        return True

    def once_removed_conflicts(self, edges, crv_edge_mapping):
        """Counts the number of times each column_row_vertex is shown in a list where a single edge is removed. 
        
        ASYMPTOTICALLY_SLOW: This is done to every edge!

        Args:
            edges (list): List of tuples representing edges
            crv_edge_mapping (dict): Edges mapped to their prime renamed edge

        Returns:
            dict: Tuple to a dictionary of every column_row_vertex, and the number of times they were found 
        """
        
        conflicts_once_removed = {}
        for i, edge_excluded in enumerate(edges):
            conflicts_once_removed[edge_excluded] = {}
            for edge in edges[:i]+edges[i+1:]:
                for crv in crv_edge_mapping[edge]:
                    if conflicts_once_removed[edge_excluded].get(crv) == None:
                        conflicts_once_removed[edge_excluded][crv] = 0
                    conflicts_once_removed[edge_excluded][crv] += 1

        return conflicts_once_removed


    def heuristic(self, edges, crv_edge_mapping):
        """Calculates 'Conflict-Product-Once-Removed' heuristic for every edge passed in 

        Conflict-Product-Once-Removed iterates through all the edges, per iteration removes the current edge out the list,
        and calculate the number of times each column_row_vertex is shown. From here, the product of all these values is kept as the
        heuristic for the current edge removed.

        Args:
            edges (list): Tuples representing edges
            crv_edge_mapping (dict): Edge to edge with column_row_vertices

        Returns:
            dict: Edges with their corresponding heuristic
        """
        conflicts_once_removed = self.once_removed_conflicts(edges, crv_edge_mapping)

        edge_heuristics = {}
        for edge in conflicts_once_removed:
            if not edge_heuristics.get(edge):
                edge_heuristics[edge] = 1 # Multiplictive Identity
            
            for prime in conflicts_once_removed[edge]:
                edge_heuristics[edge] *= conflicts_once_removed[edge][prime]
                
        return edge_heuristics


    def minimum_valued_edges(self, heuristic_dict):
        """Finds all edges with the minimum heuristic 

        Args:
            heuristic_dict (dict): Edges assigned to some heurstic value.

        Returns:
            list: Set of keys with the minimum value
        """
        min_value = min(heuristic_dict.values())
        ideal_edges = [edge for edge, value in heuristic_dict.items() if value == min_value]
        return ideal_edges

if __name__ == "__main__":
    
    s = Prime_Solver()
    s.do_main()