import os
import numpy as np


root_directory = input('Enter path to directory of .edgelist files to convert to NPY format: \n')

def convert_to_npy(dirpath, file):
    G = np.loadtxt(os.path.join(dirpath, file), dtype=int)
    output_dir = os.path.join(dirpath, 'NPY')
    os.makedirs(output_dir, exist_ok=True)

    np.save(os.path.join(output_dir, os.path.splitext(file)[0] + '.npy'), G)
    

for dirpath, dirnames, files in os.walk(root_directory):
    for file in files:
        if file.endswith('.edgelist'):
            full_path = os.path.join(dirpath, file)
            convert_to_npy(dirpath, file)
            
