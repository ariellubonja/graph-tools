#!/bin/bash

# Prompt the user to enter the root directory
echo "Enter the path to the directory of .edgelist files:"
read root_directory

# Define the output directory
output_directory="${root_directory}/Ligra-AdjGraphs"

# Change to the root directory
cd "$root_directory" || exit

# Compile ligra/utils if not already compiled
make -j ligra/utils

# Create the output directory if it doesn't exist
mkdir -p "$output_directory"

# Loop over all .edgelist files in the root directory
for file in *.edgelist; do
    # Define the output file name by replacing the extension and adding the output directory
    output_file="${output_directory}/${file%.edgelist}.AdjGraph"

    # Run the SNAPtoAdj utility
    ./SNAPtoAdj "$file" "$output_file"
done
