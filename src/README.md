# Application for Benchmarking Maximum Matching Solvers

- Author: Matt Anderson
- Course: CSC 489, Fall 2024
- Date: 08/08/24

## Organization


- `mmb/mmb.py` - Main application file.
- `mmb/mmb_tools.py` - Module with useful functions for benchmarking and checking solutions for maximum matching.
- `benchmarks/*.mmb` - Benchmarking Test Files.
- `benchmarks/tests/*.mmi` - Maximum Matching Instance Files.
- `solvers/solver.py` - An abstract class for writing a maximum matching solver. Includes an example `Identity_Solver` that **doesn't correctly solve the maximum matching problem!**

## Usage of the Benchmarker

Running `mmb.py -h` for usage produces:

```
usage: mmb.py [-h] [-v] [-t TIMEOUT] [-pg] mmb_file_name exec_cmd

CSC-489 Benchmarker for the Maximum Matching Problem.

positional arguments:
  mmb_file_name         path to .mmb file with tests
  exec_cmd              executable command to test, put in quote if arguments are included

options:
  -h, --help            show this help message and exit
  -v, --verbose         show debugging output and all stdout / stderr output created by exec_cmd
  -t TIMEOUT, --timeout TIMEOUT
                        positive integer time limit on each test in seconds
  -pg, --print_graphs   generate a .png for each graph in .mmb file. requires igraph and pycairo 
```

For an example usage, from `src/mmb/` run 
```
./mmb.py ../benchmarks/benchmark1.mmb  ../solvers/solver.py
```
this will run the default (incorrect) solver `Identity_Solver` on `benchmark1.mmb`.


## Maxmimum Matching Benchmarking File Format (.mmb)

Contains any number of lines which are paths to .mmi files to be
tested.  Any lines that begin with a # are ignored. Paths can be
absolute or relative. If they are relative, they need to be defined
relative to the location of this .mmb file.  Can include wildcards *.

## Maximum Matching Instance File Format (.mmi)

Considers d-partite maximum matching instances G = <V^d, E> with n =
|V| and m = |E|.  The .mmi file format capture all information
necessary to specify such instances.  It can optionally include the size of the
maximum matching of G, if known.

- First three lines:
  - d, an integer >= 2 specifying the number of dimensions
  - n, the number of vertices in V.
  - m, the number of edges in E.
- Next m lines:
  - d-tuples of the numbers {1..n} comma separated indicating the edges of G.
- Optional last line:
  - If present this indicates the known maximum matching size of G.

A parser for .mmi files can be found in `mmb/mmb_tools.py`.

## Executable Command

Specifies an executable command to run.  The command must be given in
quotes if it contains more than one token.  The command should be
written to run properly from the current working directory.

The executable is expected to read the maximum matching instance from
standard input as (3 + m) lines as described aboved in the .mmi
format. Then, it should calculate and output a maximum matching to
standard output as k lines of d-tuples.  It should halt with exit code
0.  No other output to standard output should be produced.  

An example Python program that conforms to this input / output format 
is given in `solvers/solver.py`.  That said, the benchmarker should 
work with any executable, from any programming language, that conforms 
to this input / output format.

This benchmarking application will run the executable command on each 
instance provided in the benchmarking test file, checking correctness 
and recording running time.  If a non-negative timeout is specified, 
the test will run for up to that many seconds before halting with an
error.

## Output of this Program

On success this application outputs a number of lines equal to the
number of tests in this benchmark.  For each test it reports the
test's sequence number, the .mmi file name for the test and the walk
clock runtime of the test.  If the test errors, times out, or fails to
output a valid maximum matching for the instance an error message is
displayed.  The output information is semi-colon separated for easy
import into an analysis program.

The verbose option `-v` can be set to display the entire standard
output and standard error produced when the executable runs the test.
If you want to use print debugging with this application to debug your
maximum matching program you are advised to only output debug
information to standard error, e.g., as in `print("error",
file=sys.stderr)` in Python.




# For Kurtik only:
## personal command for benchmark from src directory:
```
python3 mmb/mmb.py benchmarks/benchmark1.mmb "python3 solvers/bipartite/kurtik_solver.py"
```

## enter my environment
```
source .venv/bin/activate
```
```
pip install networkx
```
```
cd src
```
```
python3 solvers/Random_Graph_networkx2.py
```