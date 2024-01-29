#!/bin/bash

# Prompt the user to enter the path to the Ligra directory
echo "Enter the path to the Ligra repository base directory:"
read ligra_directory

# Prompt the user to enter the path to the Erdos-Renyi graph directory
echo "Enter the path to the Erdos-Renyi graph directory:"
read erdos_renyi_directory

# Define the output directory
output_directory="${erdos_renyi_directory}/Ligra-AdjGraphs"

# Compile ligra/utils if not already compiled
(cd "$ligra_directory" && make -j utils)

# Create the output directory if it doesn't exist
mkdir -p "$output_directory"

# Loop over all .edgelist files in the Erdos-Renyi graph directory
for file in "${erdos_renyi_directory}"/*.edgelist; do
    # Define the output file name by replacing the extension and adding the output directory
    output_file="${output_directory}/$(basename "${file%.edgelist}").AdjGraph"

    # Run the SNAPtoAdj utility
    "${ligra_directory}/utils/SNAPtoAdj" "$file" "$output_file"
done
