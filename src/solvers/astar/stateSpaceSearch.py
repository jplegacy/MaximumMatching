#!/bin/python3

'''stateSpaceSearch.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 09/19/24

Contains all classes required to do state space traversal. The classes include the following:
    - An abstract problem state class
    - Queue class
    - Search Class
    - Node Class
    

To use this, create a new problem class by subclassing and changing the implementation of the functions 
specified below.  

'''

from abc import ABC, abstractmethod
import sys


class ProblemState(ABC):
    """
    An interface class for problems  
    """

    @abstractmethod
    def applyOperators(self):
        """
        Returns a list of successors states.
        """
        pass
    
    @abstractmethod   
    def equals(self, state):
        """
        Tests whether the state instance equals the given state.
        """
        pass

    @abstractmethod
    def dictkey(self):
        """
        Returns a string that can be used as a dictionary key to
        represent each unique state.
        """
        pass

class Queue:
    """
    A Queue class to be used in combination with state space
    search. The enqueue method adds new elements to the end. The
    dequeue method removes elements from the front.
    """
    def __init__(self):
        self.queue = []
        
    def __str__(self):
        result = "Queue contains " + str(len(self.queue)) + " items\n"
        for item in self.queue:
            result += str(item) + "\n"
        return result

    def enqueue(self, node):
        self.queue.append(node)

    def dequeue(self):
        if not self.empty():
            return self.queue.pop(0)
        else:
            print("Error Dequeuing", file=sys.stderr)
            raise Exception

    def size(self):
        return len(self.queue)

    def empty(self):
        return len(self.queue) == 0

class Node:
    """
    A Node class to be used in combination with state space search.  A
    node contains a state, a parent node, and the depth of the node in
    the search tree.  The root node should be at depth 0.
    """
    def __init__(self, state, parent, depth):
        self.state = state
        self.parent = parent
        self.depth = depth
    def __str__(self):
        result = "\nState: " +  str(self.state)
        result += "\nDepth: " + str(self.depth)
        if self.parent != None:
            result += "\nParent: " + str(self.parent.state)
        return result

class Search:
    """
    A general search class that can be used for any problem domain.
    Given instances of an initial state and a goal state in the
    problem domain.  The problem domain should be based on the ProblemState
    class.
    """
    def __init__(self, initialState, winningFunc, verbose=False):
        self.uniqueStates = {}
        self.uniqueStates[initialState.dictkey()] = True
        self.q = Queue()
        self.q.enqueue(Node(initialState, None, 0))
        self.isWinState = winningFunc
        self.verbose = verbose
        solution = self.execute()
        if solution == None:
            print("Search failed")
        else:
            self.showPath(solution)

    def execute(self):
        while not self.q.empty():
            current = self.q.dequeue()
            if self.isWinState(current.state):
                return current
            else:
                successors = current.state.applyOperators()
                for nextState in successors:
                    if nextState.dictkey() not in self.uniqueStates.keys():
                        n = Node(nextState, current, current.depth+1)
                        self.q.enqueue(n)
                        self.uniqueStates[nextState.dictkey()] = True
                if self.verbose:
                    print("Expanded:", current)
                    print("Number of successors:", len(successors))
                    print("Queue length:", self.q.size())
                    print( "-------------------------------")
                
        return None

    def showPath(self, node):
        path = self.buildPath(node)        
        for current in path:
            print( current.state)
        print("Goal reached in", current.depth, "steps")

    def buildPath(self, node):
        """
        Beginning at the goal node, follow the parent links back
        to the start state.  Create a list of the states traveled
        through during the search from start to finish.
        """
        result = []
        while node != None:
            result.insert(0, node)
            node = node.parent
        return result

    
