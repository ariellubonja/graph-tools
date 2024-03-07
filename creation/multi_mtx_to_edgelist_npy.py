# Ariel Lubonja & ChatGPT
# Merges multiple .mtx files into a single edge list.
# 6-Mar-2024

# This script expects that the input directory will contain only .mtx files to be processed,
# and that these files are named according to the convention used by 7-Zip when extracting
# archives with files of the same name (e.g., file.mtx, file_1.mtx, file_2.mtx, etc.).

# Use 7zz x <filename> to extract the files, then u to auto-rename the zipped files w/ the same name

import numpy as np
import os
import argparse
import re


def yield_edges_from_mtx(file_path):
    """
    Generator that yields edges from a .mtx file.

    Args:
        file_path (str): The path to the .mtx file.
    """
    with open(file_path, 'r') as file:
        header_passed = False
        for line in file:
            if line.startswith('%'):
                # Skip the next line after the header (which contains the matrix dimensions)
                header_passed = True
                continue
            if header_passed:
                # This is the line immediately following the header; skip it
                header_passed = False
                continue
            i, j = map(int, line.split())
            yield i, j


def get_file_order(file_name):
    """
    Extracts the numerical part from the file name for sorting. Handles filenames with or without an underscore.
    Special case: file named 'uk_2005.mtx' is treated as the earliest in the order.

    Args:
        file_name (str): The file name of the .mtx file.

    Returns:
        int: The numerical part of the file name. If no numerical part is found, returns -1 for the base file,
             and 0 for others.
    """

    match = re.search(r'(\d+)\.mtx$', file_name)
    if match:
        # If the file name ends with digits followed by ".mtx"
        return int(match.group(1))

    return 0




def main(input_dir, output_filename):
    """
    Processes all .mtx files in the given directory, converting them into a single edge list represented as a NumPy array,
    and writes this list to a specified output file. The file 'uk_2005.mtx' is processed first, followed by other
    files in numeric order.

    Args:
        input_dir (str): Directory containing .mtx files.
        output_filename (str): File path where the combined edge list will be saved.
    """
    graph_matrix = np.empty((0, 2), dtype=np.int32)
    mtx_files = [f for f in os.listdir(input_dir) if f.endswith('.mtx')]
    mtx_files.sort(key=get_file_order)

    # Ensure uk_2005.mtx (the file without an underscore) is first in the list
    mtx_files = [mtx_files[-1]] + mtx_files[:-1]

    for file_name in mtx_files:
        full_path = os.path.join(input_dir, file_name)
        edges = list(yield_edges_from_mtx(full_path))  # Collect edges into a list
        edges_array = np.array(edges, dtype=np.int32)  # Convert to NumPy array
        graph_matrix = np.append(graph_matrix, edges_array, axis=0)

    edgelist_path = f'{output_filename}.edgelist'
    npy_path = f'{output_filename}.npy'

    np.savetxt(edgelist_path, graph_matrix, fmt='%d')
    np.save(npy_path, graph_matrix)

    print(f'Processed {len(mtx_files)} .mtx files. Total edges: {len(graph_matrix)}')
    print(f'Edge list saved to: {edgelist_path}')
    print(f'NumPy array saved to: {npy_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge .mtx files into a single edge list represented as a NumPy array")
    parser.add_argument("--input_dir", type=str, help="Directory containing .mtx files")
    parser.add_argument("--output_filename", type=str, help="Output file for the combined edge list")
    args = parser.parse_args()
    main(args.input_dir, args.output_filename)
