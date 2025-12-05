import os,sys
import subprocess
# Get project root path and add to system path for module import
current_script_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(os.path.dirname(current_script_path), '..', '..'))
sys.path.append(project_root)
from dataset_config import dataset_params, default_params

def start():
    """Generate and execute transform.py commands to create prompt files for datasets"""
    # Configuration parameters
    datasets=['bank']
    shot_range = ['full']
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Iterate through target datasets
    for dataset in datasets:
        # Create prompts directory if it doesn't exist
        prompts_dir = os.path.abspath(os.path.join(current_dir, '..', 'prompts', dataset))
        if not os.path.exists(prompts_dir):
            print(f"Creating prompts directory: {prompts_dir}")
            os.makedirs(prompts_dir)
        
        # Get dataset-specific parameters or use defaults
        params = dataset_params.get(dataset, default_params)
        mds = params['mds']
        mls = params['mls']
        trees = params['n_estimators']
        
        # Iterate through all (tree/md/ml) parameter combinations
        for tree in trees:
            for md in mds:
                for ml in mls:
                    #base_dir = f".../results/{dataset}"
                    base_dir = os.path.abspath(os.path.join(current_dir, '..', '..','results', dataset))
                    tree_rules = []
                    target_paths = []
                    
                    # Iterate through shot range (full) to build file paths
                    for i in shot_range:
                        # Define log/target file paths for current parameters
                        log_file = f"{dataset}_md{md}_ml{ml}_tree{tree}.log"
                        target_file = f"{dataset}_rand{i}_md{md}_ml{ml}_tree{tree}.txt"
                        
                        tree_rules.append(os.path.join(base_dir, log_file))
                        target_paths.append(os.path.join(prompts_dir, target_file))
                    
                    # Build and execute transform.py commands for each shot range
                    for i in range(len(shot_range)):
                        cmd = [
                            'python', 'transform.py',
                            '--prompt_path', f'{dataset}.py',
                            # '--prompt_path', 'v.py',  # Alternative prompt path
                            '--tree_rules', tree_rules[i],
                            '--target_prompt_path', target_paths[i]
                        ]
                        
                        try:
                            print(f"Executing command: {' '.join(cmd)}")
                            subprocess.run(cmd, check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"Command failed: {' '.join(cmd)} with error: {e}")

if __name__ == "__main__":
    # Entry point: start command generation and execution
    start()
