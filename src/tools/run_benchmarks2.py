"""
run_benchmarks2.py

This script iterates through a list of specified 
The results are output to a specified CSV file.

Purpose:
- To automate the process of running benchmarks on different solver scripts and collecting the results.

Credits:
- Developed by Jeremy
- Original Code from Kurtik
- Assisted by ChatGPT
"""
import os
import subprocess

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.path.join(current_dir, "..")  # Go up to src directory
benchmark_script = os.path.join(current_dir, "mmb/mmb.py")
benchmark_file = os.path.join(current_dir, "benchmarks/publishTest.mmb")
output_file = os.path.join(current_dir, "analysis/data/publishData.csv")

# D partite list
solver_files = [
    "src/solvers/approximate/hypergraph/HSApproxSolver.py",
    "src/solvers/astar/astarSolver.py",  
    "src/solvers/brute/bruteForceV2Solver.py",  
    "src/solvers/dfs/DFSSolver.py",  
    "src/solvers/dfs/primeSolver.py",  
    "src/solvers/integer/CPLEXSolver.py",  
    "src/solvers/integer/IPSolver.py",  
    "src/solvers/java/HopcroftKarp/HopcroftKarp.py",  
    "src/solvers/java/ThreadingHopcroftKarp/ThreadingHopcroftKarp.py",  
]

# Bipartite list
# solver_files = [
#     "src/solvers/bipartite/huyenEdmondsKarpSolver.py",
#     "src/solvers/bipartite/kurtikHopcroftKarpSolver.py",
#     "src/solvers/bipartite/kurtikSolver.py",
#     "src/solvers/bipartite/vinhEdmondsKarpSolver.py",
#     "src/solvers/bipartite/vinhHopcroftKarpSolver.py",
#     "src/solvers/java/HopcroftKarp/HopcroftKarp.py",  
#     "src/solvers/java/ThreadingHopcroftKarp/ThreadingHopcroftKarp.py",  
#     "src/solvers/approximate/general/approximateMWMSolver.py",  
#     "src/solvers/approximate/bipartite/gptApproxSolver.py",  
# ]


timeout_per_test = 2  # Timeout in seconds

# ---------------------------------Configuration above--------------------------------------------------------------

# Iterate over the given list of solver Python files
for solver_path in solver_files:
    # Check if the solver file exists and is a Python script
    if os.path.isfile(solver_path) and solver_path.endswith(".py"):
        
        # Construct the full benchmark command as a list of arguments
        command = [
            "python3", benchmark_script, benchmark_file,
            f"python3 {solver_path}", "--output", output_file,
            "--timeout", str(timeout_per_test)
        ]

        print(f"Running: {' '.join(command)}")  # Debug print

        try:
            # Execute the command
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(result.stdout)  # Print the command output
        except subprocess.CalledProcessError as e:
            print(f"Error running {solver_path}: {e.stderr}")
