#!/bin/python3

'''CPLEXSolver.py

- Author: Jeremy Perez with assistance of ChatGPT
- Course: CSC 489, Fall 2024
- Date: 10/23/24

FIXME: Uses CPLEX which is a licensed Solving module 

Solves the maximum matching problem using integer programming. 
'''

import os
import sys
import cplex

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from solver import Solver

class CPLEXSolver(Solver):

    def solve(self, G):
        '''Takes an instance G = (d, n, m, E) in the format parse_mmi
        produces.  Return a list contains d-edges as tuples of a maximum
        matching of G.'''

        (d, n, m, E) = G
    
        # Create a new CPLEX problem instance
        problem = cplex.Cplex()
        
        problem.set_results_stream(None)
        
        problem.set_problem_type(cplex.Cplex.problem_type.LP)
        problem.objective.set_sense(problem.objective.sense.maximize)

        # Extract the edges
        edge_list = list(E.keys())
        
        # Create the decision variables
        variable_names = [f"Edge_{i}" for i in range(len(edge_list))]
        problem.variables.add(names=variable_names, types=[problem.variables.type.binary] * len(edge_list))

        # Set the objective function
        problem.objective.set_linear([(var, 1) for var in variable_names])

        # Add constraints: Ensure that each vertex (i, j) is used at most once
        for i in range(d):
            for j in range(1, n + 1):
                temp = [idx for idx, e in enumerate(edge_list) if e[i] == j]
                if temp:
                    constraint_vars = [variable_names[idx] for idx in temp]
                    problem.linear_constraints.add(
                        lin_expr=[cplex.SparsePair(ind=constraint_vars, val=[1] * len(temp))],
                        senses=["L"],
                        rhs=[1]
                    )

        # Solve the problem
        problem.solve()

        # Extract the solution
        solution = []
        edge_values = problem.solution.get_values()
        for idx, value in enumerate(edge_values):
            if value == 1:
                solution.append(edge_list[idx])

        return solution


if __name__ == "__main__":

    s = CPLEXSolver()
    s.do_main()
