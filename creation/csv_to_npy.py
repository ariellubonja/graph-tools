import os
import numpy as np


root_directory = input('Enter path to directory of .csv files to convert to .npy: \n')

def convert_to_csv(dirpath, file):
    G = np.load(os.path.join(dirpath, file))

    # parent = os.path.dirname(dirpath)
    np.save(os.path.join(dirpath, os.path.splitext(file)[0] + '.npy'), G)
    

for dirpath, dirnames, files in os.walk(root_directory):
    for file in files:
        if file.endswith('.csv'):
            full_path = os.path.join(dirpath, file)
            convert_to_csv(dirpath, file)
            
