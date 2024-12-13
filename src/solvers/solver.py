#!/bin/python3

'''solver.py

- Author: Matt Anderson
- Course: CSC 489, Fall 2024
- Date: 08/08/24

Contains an abstract class Solver.  Create new solvers by subclassing
and changing the implementation of the solve method.  An example of
this is provided by Identity_Solver which returns the edge set of the
graph as the "matching", which is unlikely to be correct.
'''

import sys, os
from abc import ABC, abstractmethod

# Finds path to mmb_tools, better done by updating PATH in environment.
sys.path.append(os.path.join(os.path.dirname(__file__), "../mmb/"))
from mmb_tools import parse_mmi, parse_check_is_matching

class Solver(ABC):

    @abstractmethod
    def solve(self, G):
        '''Takes an instance G = (d, n, m, E) in the format parse_mmi
        produces.  Return a list contains d-edges as tuples of a maximum
        matching of G.
        '''
        pass
        
    def do_main(self):

        # Capture the instance from stdin.
        stdin_lines = []
        try:
            while True:
                stdin_lines.append(input())
        except EOFError:
            pass

        # Parse the instance
        (d, n, m, E, _) = parse_mmi(stdin_lines)
        G = (d, n, m, E)

        # Output debug info to stderr.
        print("DEBUG:", G, file=sys.stderr)
    
        # Solve the instance!
        M = self.solve(G)

        # Output the matching on stdout.
        M_lines = [str(e)[1:-1] for e in M]
        for line in M_lines:
            print(line)

        # Locally test correctness of M.
        try:
            parse_check_is_matching(G, M_lines)
            print("DEBUG: Matching is correct!", file=sys.stderr)
        except:
            print("DEBUG: Matching is incorrect.", file=sys.stderr)
    
class Identity_Solver(Solver):
    '''Solves the maximum matching problem for bipartite graphs using the
    Edmonds-Karp algorithm.

    '''

    def solve(self, G):
        '''Takes an instance G = (d, n, m, E) in the format parse_mmi
        produces.  Return a list contains d-edges as tuples of a maximum
        matching of G.

        >>>> BUG: It doesn't actually do this!  Instead it just returns
        all the edges in E, which is unlikely to be a matching. <<<<<
        '''
        (d, n, m, E) = G

        M = E.keys()  # WRONG!!!

        return M

if __name__ == "__main__":
    s = Identity_Solver()
    s.do_main()

