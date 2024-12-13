import random as r
import os

'''dgt2testgenerator.py
Module for create .mmi files for d > 2 with a known maximum matching size

Call from the folder you want to hold all of the files you generate.
'''


def make_graph(d, n, m, matching_size, name):
    nodes = []
    for i in range(0, d):
        nodes.append(list(range(1, n + 1)))

    #get edges
    edges = []
    #get all edges in the matching
    for i in range(0, matching_size):
        to_add = []
        for j in range(0, d):
            random_index = r.randint(0, len(nodes[j]) - 1)
            to_add.append(nodes[j].pop(random_index))
        edges.append(to_add)
        # after each interation of this for loop, edges will 
        # contain a new edge that is part of a max matching and
        # nodes will contain only nodes not yet visited in the 
        # edgeset

    max_matching = edges.copy()
    # choose a column at random where no added edges will 
    # conflict with edges that already exist
    exclude_index = r.randint(0, len(nodes) - 1)

    # get nodes that added edges can use 
    okay = []
    for i in range(1, n + 1):
        if nodes[exclude_index].count(i) == 0:
            okay.append(i)

    
    for i in range(matching_size, m):
        new_edge = []
        for j in range(0, d):
            if j != exclude_index:
                new_edge.append(range(1, n + 1)[r.randint(0, n - 1)])
            else:
                new_edge.append(okay[r.randint(0, len(okay) - 1)])
        if edges.count(new_edge) == 0:
            edges.append(new_edge)
        else:
            #Just generate a new edge
            i = i - 1

        if len(edges) == m:
            #Be prepared to stop making edges early to prevent infinite loop
            break

    f = open(name, "w")
    f.write(str(d) + "\n")
    f.write(str(n) + "\n")
    f.write(str(m) + "\n")
    for edge in edges:
        to_add = ""
        for node in edge:
            to_add = to_add + str(node) + ", "
        f.write(to_add[:-2] + "\n")
    f.write(str(matching_size))
    f.close

if __name__ == "__main__":
    d = int(input("Enter d for testing suite: "))
    n = int(input("Enter n for testing suite: "))
    m = int(input("Enter m for testing suite: "))
    matching = int(input("Enter maximum matching size for suite: "))
    amount = int(input("Enter how many .mmi files you'd like: "))

    errored = False
    if d <= 0:
        print("Error: Invalid d. Must be greater than 0, got " + str(d))
        errored = True
    if n <= 0:
        print("Error: Invalid n. Must be greater than 0, got " + str(n))
        errored = True
    if m > n**d:
        print("Error: Invalid m. Must be within bounds of n^d, got " + str(m))
        errored = True
    if m < 0:
        print("Error: Inavlid m. Must be non-negative, got " + str(m))
        errored = True
    if matching > m:
        print("Error: Invalid maximum matching size, must be greater than edgeset size, got " + str(matching))
        errored = True
    if matching < 1:
        print("Error: Inavlid maximum matching size, must be at least 1, got " + str(matching))
        errored = True
    
    if errored:
        print("Aborting")
        quit()

    for i in range(0, amount):
        output_name = "d" + str(d) + "n" + str(n) + "m" + str(m) + "M" + str(matching) + "test" + str(i) + ".mmi"
        make_graph(d, n, m, matching, output_name)
    
    print("Done creating tests. ")

    
    