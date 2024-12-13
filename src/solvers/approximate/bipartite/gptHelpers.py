#!/bin/python3

'''gpt.py
- Author: Jeremy Perez using chatGPT
- Course: CSC 489, Fall 2024
- Date: 09/30/24

ChatGPT's implementation of Sepehr Assadi's Approximation algorithm

'''
import random

class BipartiteGraph:
    def __init__(self, left, right, edges):
        self.L = left  # Left set of vertices
        self.R = right  # Right set of vertices
        self.E = edges  # Edges between left and right sets

def maximum_matching(bipartite_graph):
    # Create an adjacency list for the bipartite graph
    adj = {u: [] for u in bipartite_graph.L}
    for u, v in bipartite_graph.E:
        adj[u].append(v)

    # To keep track of which vertices are matched
    match_left = {u: None for u in bipartite_graph.L}
    match_right = {v: None for v in bipartite_graph.R}

    def bpm(u, visited):
        for v in adj[u]:
            if visited[v]:
                continue
            visited[v] = True
            # If v is not matched or previously matched vertex has an alternate path
            if match_right[v] is None or bpm(match_right[v], visited):
                match_left[u] = v
                match_right[v] = u
                return True
        return False

    # Find maximum matching
    for u in bipartite_graph.L:
        visited = {v: False for v in bipartite_graph.R}
        bpm(u, visited)

    # Extract the matching pairs
    matching = [(u, match_left[u]) for u in bipartite_graph.L if match_left[u] is not None]
    return matching

def minimum_vertex_cover(bipartite_graph, matching):
    # Create adjacency list for the bipartite graph
    adj = {u: [] for u in bipartite_graph.L}
    for u, v in bipartite_graph.E:
        adj[u].append(v)

    # Create a set of matched vertices
    matched_left = {u for u, v in matching}
    matched_right = {v for u, v in matching}

    # Step 1: Find unmatched vertices in left set
    unmatched_left = set(bipartite_graph.L) - matched_left

    # Step 2: Use DFS to find vertices reachable from unmatched vertices in left
    reachable = set()
    
    def dfs(u):
        reachable.add(u)
        for v in adj[u]:
            if v not in matched_right and v not in reachable:
                reachable.add(v)
                for neighbor in adj[v]:
                    if neighbor not in matched_left:
                        dfs(neighbor)

    # Start DFS from unmatched left vertices
    for u in unmatched_left:
        dfs(u)

    # Step 3: Build the vertex cover
    cover = set()
    
    # Vertices in left set that are reachable
    for u in bipartite_graph.L:
        if u in reachable:
            continue
        cover.add(u)
    
    # Vertices in right set that are not reachable
    for v in bipartite_graph.R:
        if v not in reachable:
            cover.add(v)
    
    return cover

def sample_and_solve(bipartite_graph, epsilon):
    n = len(bipartite_graph.L) + len(bipartite_graph.R)
    R = int(4 / epsilon * (n ** 0.5))  # Approximate number of iterations

    q = {e: 1 for e in bipartite_graph.E}  # Importance of each edge

    best_matching = []
    
    for r in range(R):
        # Sample edges
        total_importance = sum(q[e] for e in bipartite_graph.E)
        sampled_edges = []
        
        for e in bipartite_graph.E:
            p = (2 * n / epsilon) * (q[e] / total_importance)
            if random.random() < p:
                sampled_edges.append(e)

        sampled_graph = BipartiteGraph(bipartite_graph.L, bipartite_graph.R, sampled_edges)
        matching = maximum_matching(sampled_graph)
        vertex_cover = minimum_vertex_cover(sampled_graph, matching)

        # Update importance
        for e in bipartite_graph.E:
            if e not in vertex_cover:
                q[e] *= 2  # Double the importance for uncovered edges

        best_matching = matching  # Store the best matching found so far

    return best_matching

# Example usage
if __name__ == "__main__":
    left = ['A', 'B', 'C','D','E']
    right = ['1', '2', '3','4','5']
    edges = [('A', '1'), ('A', '2'), ('B', '2'),('B', '5'), ('C', '3'),('D', '5'),('E','4')]
    
    bipartite_graph = BipartiteGraph(left, right, edges)
    epsilon = 0.1  # You can choose any value between 0 and 1

    matching = sample_and_solve(bipartite_graph, epsilon)
    print("Approximate Maximum Matching:", matching)
