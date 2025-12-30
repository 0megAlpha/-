---
name: jupyter
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
- ipynb
- jupyter
---

# Jupyter Notebook Guide

## Programmatic Notebook Modification

When modifying Jupyter notebooks programmatically, use Python's JSON library since notebooks are JSON files:

```python
import json

# Load the notebook
with open('notebook.ipynb') as f:
    nb = json.load(f)

# Cells are in nb['cells'], each has 'source' (list of strings) and 'cell_type'
# cell_type can be 'code', 'markdown', or 'raw'
cell = nb['cells'][cell_index]
source_lines = cell['source']

# Modify source_lines as needed, then save
with open('notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```

## Creating a New Notebook

```python
import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# My Notebook\n"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["print('Hello, World!')\n"]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open('new_notebook.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)
```

## Executing Notebooks

Execute a notebook and update it in place:

```bash
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```

Execute and convert to other formats:

```bash
# Convert to HTML
jupyter nbconvert --to html notebook.ipynb

# Convert to PDF (requires pandoc and LaTeX)
jupyter nbconvert --to pdf notebook.ipynb

# Convert to Python script
jupyter nbconvert --to script notebook.ipynb

# Convert to Markdown
jupyter nbconvert --to markdown notebook.ipynb
```

## Finding Code in Notebooks

Quick search using grep:

```bash
grep -n "search_term" notebook.ipynb
```

Programmatic search through cells:

```python
import json

with open('notebook.ipynb') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'search_term' in source:
        print(f"Found in cell {i} ({cell['cell_type']})")
```

## Installing Jupyter

```bash
pip install jupyter notebook

# Or with JupyterLab
pip install jupyterlab
```

## Running Jupyter

```bash
# Start Jupyter Notebook server
jupyter notebook

# Start JupyterLab
jupyter lab

# Run in background with no browser
jupyter notebook --no-browser --port=8888 &
```

## Common Cell Operations

### Add a new cell

```python
import json

with open('notebook.ipynb') as f:
    nb = json.load(f)

new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": ["# New code cell\n"]
}

nb['cells'].append(new_cell)

with open('notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```

### Delete a cell

```python
import json

with open('notebook.ipynb') as f:
    nb = json.load(f)

del nb['cells'][cell_index]

with open('notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```

### Clear all outputs

```python
import json

with open('notebook.ipynb') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

with open('notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```
