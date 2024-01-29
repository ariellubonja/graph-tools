import os
import numpy as np


root_directory = input('Enter absolute path to directory of .NPY files to create fake node labels for: \n')

def create_fake_labels(dirpath, file):
    G = np.load(os.path.join(dirpath, file))

    max_node = np.max(G[:, :2]) # If weighed, will have 3 cols.
    n_nodes = max_node + 1

    # Create fake labels for Graph Encoder Embedding
    # Create some “ground truth” e.g. max 50 
    labels = np.random.randint(low=0, high=50, size=(n_nodes,1))
    # Generate n_nodes bernoulli with p=0.9:
    bern = np.random.binomial(1, 0.1, size=(n_nodes,1))
    # Remove 90% of them by assigning -1 (Semi-Supervised)
    sparse_labels = labels * bern
    # Subtract 1 from sparse labels bcs. GEE wants unlabeled = -1
    sparse_labels -= 1
    # Make sure to assign 1 value to be maxvalue i.e. 49 (50-1) in Y - GEE uses max(Y) to set embedding size
    sparse_labels[0]=49

    # Save
    base_dir = os.path.dirname(dirpath)  # Move one level up from NPY directory
    output_dir = os.path.join(base_dir, 'Ys')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.splitext(file)[0] + '.npy'
    np.save(os.path.join(output_dir, output_file), sparse_labels)

    

for dirpath, dirnames, files in os.walk(root_directory):
    for file in files:
        if file.endswith('.npy'):
            create_fake_labels(dirpath, file)
            