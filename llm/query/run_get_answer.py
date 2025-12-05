import time
import shlex
import subprocess
import itertools
import argparse
import os,sys
import subprocess

# Get project root path and add to system path for module import
current_script_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(os.path.dirname(current_script_path), '..', '..'))
sys.path.append(project_root)
from dataset_config import dataset_params, default_params

def start():
    """
    Generate and execute commands to run get_answer.py for multiple dataset parameters
    
    Iterates over datasets, mds, mls, and tree numbers from config,
    creates output directories, builds commands, and executes them sequentially.
    """
    # Define target datasets to process
    datasets = ['bank']
    cmds = []
    
    # Generate commands for each parameter combination
    for dataset in datasets:
        # Get dataset-specific parameters (fallback to default if not found)
        params = dataset_params.get(dataset, default_params)
        mds = params['mds']
        mls = params['mls']
        trees = params['n_estimators']
        
        # Create output directory for answers if not exists
        target_answer_path = f"../answers/{dataset}"
        if not os.path.exists(target_answer_path):
            print(f"Creating prompts directory: {target_answer_path}")
            os.makedirs(target_answer_path)
        
        # Build command for each (tree, md, ml) combination
        for tree in trees:
            for md in mds:
                for ml in mls:
                    log_file = f"{dataset}_randfull_md{md}_ml{ml}_tree{tree}.txt"
                    cmd_parts = [
                        'python', 'get_answer.py',
                        '--base_rule_path', f"../prompts/{dataset}",
                        '--rule_path', log_file,
                        '--target_answer_path', target_answer_path
                        ]
                    cmds.append(cmd_parts)
    
    # Execute generated commands sequentially
    for cmd in cmds:
        try:
            print(f"Executing command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{cmd}' failed with error: {e}")


if __name__ == "__main__":
    # Entry point: start command generation and execution
    start()
