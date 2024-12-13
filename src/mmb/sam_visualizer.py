import igraph as ig
from mmb_tools import parse_mmi
import argparse

'''sam_visualizer.py
Module for visualizing graphs for CSC-489, Fall 2024

To use this module stand-alone, call sam_visualizer.py from fall-2024
There is only one argument: graph_file_path, a path to a valid .mmi file or .mmb file
If given a .mmi file, it will generate a .png of the .mmi with the same name
If given a .mmb file, it will generate a .png for each .mmi file within the .mmb. 
    Each .png generated will have the same name as the .mmb file with an appeneded number to differentiate them

'''

##Visualizer
## @author: Sam Appleton
## @version: 2024-10-17
# Module for visualizing graph instances for the CSC-489
# **requires igraph and pycairo modules to run**
# Can be called as a stand-alone program from command line or imported into other projects.

def __get_graph(path):
    # Given a string with the path to a .mmi file, return the parsed graph from the file. 
    # If the path is invalid, throws an error
    toReturn = ""
    try:
        f = open(path, "r")
        lines = f.readlines()
        f.close()
        toReturn = parse_mmi(lines)
    except:
        print("Error: .mmi instance not found: " + path)
        exit()
    return toReturn

def print_graph_path(path, name, matching=[]):
    ''' 
    create a visualization of a graph with the given path, output name, and a matching if desired
    path : string with the file path to a singuler .mmi file
    name : desired name of the output file. will have '.png' appended automatically, so don't include it 
    matching : a list of edges to be used to highlight edges in the final visualization. can be empty
    '''
    #get tuple representing graph
    graph = __get_graph(path)

    print_graph(graph, name, matching)

def print_graph(in_graph, name, matching=[]):
    '''
    create a visualization of a graph with the given tuple, output name, and a matching if desired
    in_graph : a tuple of the form (d, n, m, E) to represent a d-partite graph. 
    name : desired name of the output file. will have a '.png' appended automatically, so don't include it
    matching : a list of edges to be used to highlight edges in the final visualization. can be empty
    '''

    output_name = name + ".png"

    #create a graph object with all nodes in the d-partite graph
    my_graph = ig.Graph(n=(in_graph[1]*in_graph[0]))

    #get list of edges
    edges = []
    for edge in in_graph[3]:
        edges.append(edge)

    #get list of edges used in the maximum matching
    mm = list(matching).copy()

    #convert tuple edges to edges for graph object
    colors = ["red", "orange", "green", "blue", "purple", "pink"]
    colors_to_use = []
    edge_in_matching = []
    increm = 0
    for edge in edges:
        increm = increm + 1
        for i in range(0, len(edge)-1):
            #add edge(s) to graph object based on edge tuple
            source_node = (edge[i]-1)+(in_graph[1]*i)
            target_node = (edge[i+1]-1)+(in_graph[1]*(i+1))
            my_graph.add_edge(source_node, target_node)

            #keep track of which edges were added to the graph object so they can be colored correctly
            colors_to_use.append(colors[increm % len(colors)])

            #keep track of which edges were added to the graph object so they can highlighted correctly
            if str(edge)[1:-1] in mm: ##edge is a tuple, but mm is string. need to remove the parentheses to compare
                edge_in_matching.append("1")
            else:
                edge_in_matching.append("0")

    #create coordinate system for the graph
    layout = my_graph.layout(layout='grid')
    k = 0
    for i in range(0, in_graph[0]): ##for each row (d)
        for j in range(0, in_graph[1]): ##for each vertex in that row (n)
            layout[k] = (i, j)
            k = k + 1

    #calculate the correct names for each vertex
    labels = []
    for i in range(0, in_graph[0]*in_graph[1]):
        labels.append((i % in_graph[1])+1)

    #visualize the graph
    ig.plot(my_graph, 
            target = output_name, 
            layout = layout, 
            bbox = (1000,1000), # maybe determine on size of d and n?
            vertex_color = "lightblue",
            vertex_label = labels,
            edge_width = [2 if edge_in_matching[i] == '0' else 6 for i in range(0, len(my_graph.es()))], #if edge is in maximum matching, then make it bold
            edge_color = colors_to_use,
            )
    print("Done! Printed " + output_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualizer for MMI files.")

    parser.add_argument("graph_file_name", type=str, help="path to a .mmi file or a .mmb file containing .mmi files")

    args = parser.parse_args()
    graph_path = args.graph_file_name

    try:
        f = open(graph_path, "r")
        f.close()
    except:
        print("Error: .mmi instance not found: " + graph_path)
        exit()

    if graph_path[-4:] == ".mmi": # singular instance
        output_name = graph_path.split("/")[-1][:-4]
        print_graph_path(graph_path, output_name) 
    elif graph_path[-4:] == ".mmb": # handling 0+ graphs
        f = open(graph_path, "r")
        lines = f.readlines()
        f.close()
        
        trimmed_lines = []
        for line in lines:
            toAdd = line.replace("\n", "")
            if toAdd[-3:] == "mmi":
                trimmed_lines.append("src/benchmarks/" + toAdd)
            else:
                print("Non-fatal Error: unrecognized file in .mmb: " + line)

        increm = 1

        for line in trimmed_lines:
            output_name = graph_path.split("/")[-1][:-4] + str(increm)
            print_graph_path(line, output_name)
            increm = increm + 1

    else:
        print("Error: unrecognized file type: " + graph_path[-4:])
        exit()

    print("Done printing!")