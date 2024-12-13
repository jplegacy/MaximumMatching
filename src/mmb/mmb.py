#!/bin/python3

import csv
import time, os, glob, sys, shlex, subprocess, argparse
from subprocess import PIPE, TimeoutExpired
from mmb_tools import parse_mmi, parse_check_is_matching
from sam_visualizer import print_graph
import ast  # Safe parsing for solver output

# ================== Main ====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSC-489 Benchmarker for Maximum Matching Solvers.")

    # Arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Show debugging output and all stdout/stderr.")
    parser.add_argument("-t", "--timeout", type=int, default=None, help="Time limit on each test in seconds.")
    parser.add_argument("mmb_file_name", type=str, help="Path to .mmb file with tests.")
    parser.add_argument("exec_cmd", type=str, help="Executable command to test, put in quotes if arguments are included.")
    parser.add_argument("-pg", "--print_graphs", action="store_true",
                        help="save png representations of each mmi file and edges picked by solver")
    parser.add_argument("--output", type=str, default="benchmark_results.csv", 
                        help="Name of the output CSV file for storing results.")


    args = parser.parse_args()
    timeout, mmb_file_name, exec_cmd, verbose, output_file= (
        args.timeout, args.mmb_file_name, args.exec_cmd, args.verbose, args.output
    )

    do_print = args.print_graphs

    # Validate timeout value
    if timeout is not None and timeout < 0:
        print("Error: timeout must be a positive integer.")
        exit(3)

    # Read the .mmb file and extract test cases
    try:
        with open(mmb_file_name) as f:
            tests = f.readlines()
    except:
        print(f"Error: Unable to locate {mmb_file_name}.", file=sys.stderr)
        exit(2)

    mmb_file_dir = os.path.dirname(mmb_file_name)

    # Initialize CSV file with headers if it doesn't exist
    csv_file_path = os.path.join(mmb_file_dir, output_file)
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Test Number', 'Test Path', 'd', 'n', 'm', 'Max Matching', 
                'Elapsed Time (s)', 'Solver', 'Success'
            ])

    i = 0  # Test counter

    # Loop through each test case in the .mmb file
    for test in tests:
        if len(test) > 0 and test[0] == "#" or len(test.strip()) == 0:
            continue  # Skip comments and empty lines

        # Handle wildcard paths in the test case
        test_paths = glob.glob(os.path.join(mmb_file_dir, test.strip())) if "*" in test else [os.path.join(mmb_file_dir, test.strip())]

        for test_path in test_paths:
            i += 1
            if verbose:
                print(f"Running Test {i}: {test_path}")

            try:
                with open(test_path) as f:
                    lines = f.readlines()
                # Parse d, n, m, E, and the expected result from the .mmi file
                (d, n, m, E, result) = parse_mmi(lines)
                # Get the max matching from the last line of the .mmi file
                max_matching = lines[-1].strip()
            except Exception as e:
                print(f"Error parsing {test_path}: {e}")
                continue

            # Prepare input for the solver
            in_str = f"{d}\n{n}\n{m}\n" + "\n".join([str(key)[1:-1] for key in E])

            # Start the timer
            start_time = time.time()

            try:
                # Run the solver command
                if sys.platform == 'win32':
                    p = subprocess.Popen([sys.executable] + shlex.split(exec_cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
                else:
                    p = subprocess.Popen(shlex.split(exec_cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)

                stdout_data, stderr_data = p.communicate(in_str, timeout=timeout)
            except TimeoutExpired:
                print(f"Test {i}: Timed out.")
                p.kill()
                elapsed_time = timeout  # Log max timeout value
                success = False
                # Log the timeout in CSV
                with open(csv_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    solver_name = os.path.basename(exec_cmd).replace('.py', '')
                    writer.writerow([
                        i, test_path, d, n, m, max_matching, 
                        f"{elapsed_time:.7f}", solver_name, "Timed Out"
                    ])
                continue  # Skip to next test case
            except Exception as e:
                print(f"Test {i}: Error running command: {e}")
                continue

            # Stop the timer
            end_time = time.time()
            elapsed_time = end_time - start_time

            # # Debug: Print raw output to inspect what the solver returned
            # print(f"Test {i} Raw STDOUT:\n{stdout_data}")
               
            try:
                # Convert the solver output lines into tuples of integers
                parsed_output = [
                    tuple(map(int, line.split(',')))  # Convert each line to a tuple of integers
                    for line in stdout_data.strip().split("\n") if line.strip()
                ]
                # Debug print to ensure the parsed output is correct
                

                # Format the tuples as strings dynamically based on the size of each tuple
                string_output = [", ".join(map(str, edge)) for edge in parsed_output]
                

                # Validate the matching using the formatted string output
                exec_cmd_result = parse_check_is_matching((d, n, m, E), string_output)
                success = result is None or result == exec_cmd_result
            except Exception as e:
                print(f"Test {i}: Error checking result: {e}")
                success = False

            if do_print:
                in_name = test.split("/")[-1][:-4]
                print_graph((d, n, m, E), in_name.split(".")[0], stdout_data.strip().split("\n"))

            if success:
                print(f"Test {i}: Success! {elapsed_time:.7f} seconds")
            else:
                print(f"Test {i}: Failed.")

            # Write results to the CSV file
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                solver_name = os.path.basename(exec_cmd).replace('.py', '')
                writer.writerow([
                    i, test_path, d, n, m, max_matching, 
                    f"{elapsed_time:.7f}", solver_name, success
                ])

            if verbose:
                print(f"Test {i} STDOUT:\n{stdout_data}")
                print(f"Test {i} STDERR:\n{stderr_data}")
