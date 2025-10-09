import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('--prompt_path', type=str, default='prompt.py')
parser.add_argument('--tree_rules', type=str, default='com_rand512.log')
parser.add_argument('--target_prompt_path', type=str, default='target_prompt1.txt')

args = parser.parse_args()
print(args)

# Define markers for the start and end of the CART tree rules
start_marker = "## CART tree rules"
end_marker = "## CART tree rules end"

# Read the source file
with open(args.prompt_path, "r") as src:
    source_content = src.readlines()

def extract_content(replacement_file):
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

# Update leaf node count constraint
trees = replacement_content.strip().split('--------------------------------------------------------------------------------')
class_counts = []
for tree in trees:
    classes = re.findall(r'class:', tree)  # TODO: Regression uses 'value'; Classification uses 'class'
    class_counts.append(len(classes))

max_count = max(class_counts) if class_counts else 0
for i, line in enumerate(updated_content):
    if 'The number of leaf nodes should no more than 3' in line:
        updated_content[i] = line.replace(
            'The number of leaf nodes should no more than 3',
            f'The number of leaf nodes should no more than {max_count}'
        )
        break

# Write output file
with open(args.target_prompt_path, "w") as out:
    out.writelines(updated_content)

print(f"Updated content has been written to {args.target_prompt_path}")