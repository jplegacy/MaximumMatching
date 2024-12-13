'''mmb_tools.py

Module with helpful tools for testing or writing a Maximum Matching
Solver that work with mmb.py

- Author: Matt Anderson
- Course: CSC 489, Fall 2024
- Date: 08/08/24
'''

def str_is_int(s):
    '''Returns True iff s is a representation of an integer.'''
    try:
        i = int(s)
        return True
    except:
        return False

def parse_mmi(lines):
    '''Parses a list of lines from an .mmi file.  If the file is properly
    formated (see src/README.md), it returns a tuple (d, n, m, E,
    result) containing, respectively, the dimension, vertex size, edge size, edges,
    and, if available, the maximum matching size contained in the file.

    This function also attempts to validate the file's format. It
    raises an exception on many common formating errors, but probably
    isn't exhaustive.
    '''
    
    if len(lines) < 3:
        raise Exception("Insufficient lines to parse.")

    # Parse first three lines.
    for (i, c) in [(0, "d"), (1, "n"), (2, "m")]:
        if not str_is_int(lines[i].strip()):
            raise TypeError(f"Line {i}: Expected {c} is int, got: {lines[i].strip()}")

    d = int(lines[0])
    n = int(lines[1])
    m = int(lines[2])

    
    if len(lines) < m + 3:
        raise Exception(f"Line {len(lines)}: Expected {m} {d}-edges, got {len(lines) - 3}")

    # Parse edges.
    E = {}
    for i in range(m):
        line = lines[3 + i]
        toks = line.strip().split(",")
        e = []
        if len(toks) != d:
            raise Exception(f"Line {3 + i}: Expected {d}-edge, got {line.strip()}")
        for j in range(d):
            if not str_is_int(toks[j]):
                raise TypeError(f"Line {3 + i}: Expected int, got {toks[j]}")
            e.append(int(toks[j]))

        e = tuple(e)
        if e in E:
            raise Exception(f"Line {3 + i}: Duplicate edge detected, {line.strip()}")
        E[e] = True

    # Parse optional result.
    result = None
    if len(lines) == m + 3 + 1:
        if lines[m + 3].strip() != "":
            if not str_is_int(lines[m + 3].strip()):
                raise TypeError(f"Line {m+3}: Expected int, got: {lines[m+3].strip()}")
            result = int(lines[m + 3])

    if len(lines) > m + 4:
        raise Exception(f"Line {m+4}: Unexpected lines, {lines[m+4].strip()}")
                     
    return (d, n, m, E, result)

def parse_check_is_matching(G, lines):
    '''Takes the parameters (d, n, m, E) as returned by parse_mmi()
    specifying a maximum matching instance graph G, and a list of
    lines containing strings.  If the lines express d-edges given in
    the same format as .mmi files (see src/README.md), this function
    tests where they are a matching of G and returns the number of
    edges in the matching.

    If the lines are ill-formed or the edges don't form a matching an
    exception is raised.
    '''

    (d, n, m, E) = G
    M = {}
    
    for i in range(len(lines)):
        line = lines[i].strip()
        toks = line.strip().split(",")
        e = []
        if len(toks) != d:
            raise Exception(f"Solution Line {i}: Expected {d}-edge, got {line}")
        for j in range(d):
            if not str_is_int(toks[j]):
                raise TypeError(f"Solution Line {i}: Expected int, got {toks[j]}")
            e.append(int(toks[j]))
        e = tuple(e)
        
        # Verify e is in the graph.
        if e not in E:
            raise Exception(f"Solution Line {i}: Received edge not present in graph {str(e)}")

        # Verify e hasn't been used already.
        if e in M:
            raise Exception(f"Solution Line {i}: Received duplicate edge {str(e)}")

        # Verify e is coordinate-wise vertex disjoint to ensure M stays a matching of G.
        for e2 in M:
            for j in range(d):
                if e[j] == e2[j]:
                    raise Exception(f"Solution Line {i}: Edge {str(e)} conflicts with prior edge {str(e2)}")

        # Add e to the matching M. 
        M[e] = True
        
    return len(M)
