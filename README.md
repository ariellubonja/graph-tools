# Graph Tools

A toolkit for generating, converting, and analyzing synthetic graphs, with a focus on large-scale random graph generation and format conversion utilities.

## Overview

This repository provides tools for creating synthetic graphs (primarily Erdős-Rényi and Stochastic Block Model graphs) and converting between various graph formats. It's designed to handle very large graphs efficiently using both igraph and NetworkX/NetworKit libraries.

## Features

- **Graph Generation**
  - Erdős-Rényi random graphs with configurable edge counts
  - Stochastic Block Model (SBM) graphs for community detection research
  - Support for graphs with billions of edges using NetworKit

- **Format Conversion**
  - EdgeList ↔ NumPy (.npy) format conversion
  - NumPy ↔ CSV format conversion
  - Matrix Market (.mtx) to EdgeList conversion
  - Ligra AdjGraph format generation

- **Analysis Tools**
  - Average degree calculation
  - Graph statistics and properties

- **Utilities**
  - Fake label generation for semi-supervised learning experiments
  - Batch processing of multiple graph files

## Repository Structure

```
graph-tools/
├── creation/                    # Graph generation and conversion scripts
│   ├── erdos_renyi.ipynb       # Erdős-Rényi graph generation
│   ├── stochastic_block_model.ipynb # SBM graph generation
│   ├── npy_from_edgelist.py    # EdgeList to NumPy conversion
│   ├── npy_to_csv.py           # NumPy to CSV conversion
│   ├── csv_to_npy.py           # CSV to NumPy conversion
│   ├── multi_mtx_to_edgelist_npy.py # MTX files merger
│   ├── fake_labels.py          # Generate synthetic node labels
│   └── ligra_adjgraph.sh       # Convert to Ligra format
├── analysis/                   # Analysis tools
│   └── find_avg_degree.ipynb   # Calculate average degree
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

### Prerequisites

```bash
# Core dependencies
pip install numpy networkx igraph-python

# For large graph generation (optional)
pip install networkit

# For Jupyter notebooks
pip install jupyter
```

### Optional: Ligra Framework
For Ligra format conversion, you'll need to compile the [Ligra framework](https://github.com/jshun/ligra).

## Usage

### Generating Erdős-Rényi Graphs

The main graph generation is done through the Jupyter notebook `creation/erdos_renyi.ipynb`:

```python
import math
import igraph as ig
import networkit as nk  # For very large graphs

# Configure parameters
desired_average_degree = 10
n_desired_edges = [2**i for i in range(13, 31)]  # From 8K to 1B+ edges

# Generate graphs with different edge counts
for edge_count in n_desired_edges:
    num_nodes = int(math.ceil(2 * edge_count / desired_average_degree))
    edge_prob = desired_average_degree / (num_nodes - 1)
    
    # For smaller graphs (< 100M edges)
    graph = ig.Graph.Erdos_Renyi(n=num_nodes, p=edge_prob)
    
    # For very large graphs (> 100M edges), use NetworKit
    graph = nk.generators.ErdosRenyiGenerator(num_nodes, edge_prob).generate()
```

### Format Conversion

**EdgeList to NumPy:**
```bash
python creation/npy_from_edgelist.py
# Enter path when prompted
```

**NumPy to CSV:**
```bash
python creation/npy_to_csv.py
# Enter path when prompted
```

**Multiple MTX files to single EdgeList:**
```bash
python creation/multi_mtx_to_edgelist_npy.py --input_dir /path/to/mtx/files --output_filename merged_graph
```

### Generating Synthetic Labels

For semi-supervised learning experiments:

```bash
python creation/fake_labels.py
# Creates sparse labels with 10% labeled nodes, 90% unlabeled (-1)
```

### Converting to Ligra Format

```bash
bash creation/ligra_adjgraph.sh
# Follow prompts to specify Ligra directory and graph directory
```

### Analysis

Calculate average degree of generated graphs:

```python
# In Jupyter: analysis/find_avg_degree.ipynb
import networkx as nx

def calculate_average_degree(edgelist_file):
    G = nx.read_edgelist(edgelist_file)
    degrees = [degree for node, degree in G.degree()]
    return sum(degrees) / len(degrees) if degrees else 0
```

## Graph Formats Supported

- **EdgeList** (`.edgelist`): Space-separated source-target pairs
- **NumPy** (`.npy`): Binary NumPy array format
- **CSV** (`.csv`): Comma-separated values
- **Matrix Market** (`.mtx`): Sparse matrix format
- **Ligra AdjGraph**: Compressed sparse row format for Ligra framework

## Performance Notes

- **igraph**: Suitable for graphs up to ~100M edges
- **NetworKit**: Recommended for graphs with 100M+ edges
- **NetworkX**: Functional but slower for large graphs

The repository includes both options, with NetworKit being used for the largest graph generation tasks.

## Generated Graph Statistics

The toolkit generates Erdős-Rényi graphs with:
- **Node counts**: From ~1.6K to ~214M nodes
- **Edge counts**: From ~8K to ~1B edges  
- **Average degree**: Configurable (default: 10)
- **Format**: Multiple output formats supported

## Example Applications

- **Graph neural network training**: Use generated graphs with synthetic labels
- **Scalability testing**: Test algorithms on graphs of varying sizes
- **Community detection**: Use SBM graphs with known community structure
- **Graph algorithm benchmarking**: Standard format conversion for different frameworks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

Copyright (c) 2024 Ariel Lubonja

## Acknowledgments

- Built using igraph, NetworkX, and NetworKit libraries
- Compatible with Ligra graph processing framework
- Designed for large-scale graph analysis research
