import os
import numpy as np


root_directory = input('Enter path to directory of .npy files to convert to CSV: \n')

def convert_to_csv(dirpath, file):
    G = np.load(os.path.join(dirpath, file))

    # parent = os.path.dirname(dirpath)
    np.savetxt(os.path.join(dirpath, os.path.splitext(file)[0] + '.csv'), G, fmt='%d')
    

for dirpath, dirnames, files in os.walk(root_directory):
    for file in files:
        if file.endswith('.npy'):
            full_path = os.path.join(dirpath, file)
            convert_to_csv(dirpath, file)
            
