#!/bin/python3

'''informedSearch.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 09/19/24

Contains classes required to do A*. The classes include the following:
    - An abstract problem state class
    - Informed Search Class

To use this, create a new Informed Problem State class by subclassing and implementing the functions 
specified below.  
'''

from pq import *
from stateSpaceSearch import *
from abc import abstractmethod

class InformedProblemState(ProblemState):
    """
    An extended interface class for problem domains
    with an informed abstract approach.  
    """

    @abstractmethod   
    def objective(self):
        """
        Tests whether the state instance satisfies it
        """
        pass

    @abstractmethod
    def heuristic(self):
        pass

class InformedNode(Node):
    def __init__(self, state, parent, depth):
        super().__init__(state, parent, depth)

    def priority(self):        
        #TODO:CONFIGURAIZE PRIORITY TYPE

        #Different priority type
        return self.depth + self.state.heuristic()

        # return int(str(self.depth) + str(self.state.heuristic()))


class InformedSearch(Search):
    def __init__(self, initialState, verbose=False):
        self.uniqueStates = {}
        self.uniqueStates[initialState.dictkey()] = True
        self.q = PriorityQueue()
        self.q.enqueue(InformedNode(initialState, None, 0))
        self.verbose = verbose
        self.nodeChecked = 0

        self.solution = self.execute()
        
    def solution(self):
        return self.solution
    
    def execute(self):
        while not self.q.empty():
            current = self.q.dequeue()
            self.nodeChecked += 1
            if current.state.objective():
                return current
            else:
                successors = current.state.applyOperators()
                for nextState in successors:
                    if nextState.dictkey() not in self.uniqueStates.keys():
                        n = InformedNode(nextState, current, current.depth+1)
                        self.q.enqueue(n)
                        self.uniqueStates[nextState.dictkey()] = True
                if self.verbose:
                    print( "Expanded:", current)
                    print( "Number of successors:", len(successors))
                    print( "-------------------------------")


