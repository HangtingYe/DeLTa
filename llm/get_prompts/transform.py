import argparse
import re
import os,sys

current_script_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(os.path.dirname(current_script_path), '..', '..'))
sys.path.append(project_root)
from dataset_config import dataset_params, default_params

parser = argparse.ArgumentParser()
parser.add_argument('--prompt_path', type=str)
parser.add_argument('--tree_rules', type=str)
parser.add_argument('--target_prompt_path', type=str)

args = parser.parse_args()
print(args)

# Extract dataset name from prompt_path (assuming filename format: {dataset}.py)
dataset_name = args.prompt_path.split('.')[0]
# Get dataset parameters, use default if not found
dataset_config = dataset_params.get(dataset_name, default_params)
# Determine task type: classification (num_class > 1) or regression (num_class == 1)
is_regression = dataset_config['num_class'] == 1

# Define markers for CART tree rules
start_marker = "## CART tree rules"
end_marker = "## CART tree rules end"

# Read source prompt file
with open(args.prompt_path, "r") as src:
    source_content = src.readlines()

def extract_content(replacement_file):
    """Extract tree rule content based on task type"""
    start_flag = "Tree 0 rules:"
    end_flag = 'finished print tree'
    extracted_content = []
    capturing = False
    
    with open(replacement_file, "r") as repl:
        for line in repl:
            if start_flag in line:
                capturing = True
            if capturing:
                if end_flag in line:
                    break
                # Filter out unwanted lines
                if ("100%" not in line and 
                    'index.pkl' not in line and 
                    'leaf_ids: [' not in line):
                    extracted_content.append(line)
    
    return "".join(extracted_content)

replacement_content = extract_content(args.tree_rules)

# Ensure end marker is on a new line
for i, line in enumerate(source_content):
    if end_marker in line:
        source_content[i] = line.replace(end_marker, "\n" + end_marker)
        break

# Find marker positions
start_index = next(i for i, line in enumerate(source_content) if line.strip() == start_marker)
end_index = next(i for i, line in enumerate(source_content) if line.strip() == end_marker)

# Create updated content
updated_content = (
    source_content[:start_index + 1]  # Content before start marker
    + list(replacement_content)       # Replacement rules
    + source_content[end_index:]      # Content after end marker
)

# Extract leaf node counts based on task type and update constraint
trees = replacement_content.strip().split('--------------------------------------------------------------------------------')
node_counts = []
for tree in trees:
    if tree.strip():  # Skip empty tree entries
        if is_regression:
            # Regression tasks use 'value' to extract leaf nodes
            nodes = re.findall(r'value:', tree)
        else:
            # Classification tasks use 'class' to extract leaf nodes
            nodes = re.findall(r'class:', tree)
        node_counts.append(len(nodes))

max_count = max(node_counts) if node_counts else 0
# Update leaf node count constraint
for i, line in enumerate(updated_content):
    if 'The number of leaf nodes should no more than' in line:
        updated_content[i] = line.replace(
            re.findall(r'The number of leaf nodes should no more than \d+', line)[0],
            f'The number of leaf nodes should no more than {max_count}'
        )
        break

# Write output file
with open(args.target_prompt_path, "w") as out:
    out.writelines(updated_content)

print(f"Updated content has been written to {args.target_prompt_path}")
print(f"Task type: {'regression' if is_regression else 'classification'}, Max leaf nodes: {max_count}")
    