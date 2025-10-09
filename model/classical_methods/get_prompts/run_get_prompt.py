import os
import subprocess

def start():
    # Configuration parameters
    datasets = ['cpu_act', 'credit_reg', 'Diamonds']
    datasets=['fried','california_housing','house_16H_reg']
    trees = [5]
    mds = [10]
    mls = [200]

    for dataset in datasets:
        # Create prompts directory if it doesn't exist
        prompts_dir = f"../data/{dataset}/prompts"
        if not os.path.exists(prompts_dir):
            print(f"Creating prompts directory: {prompts_dir}")
            os.makedirs(prompts_dir)
        
        for tree in trees:
            for md in mds:
                for ml in mls:
                    base_dir = f"../data/{dataset}"
                    tree_rules = []
                    target_paths = []
                    
                    for i in ange:
                        # Define file paths
                        log_file = f"{dataset}_md{md}_ml{ml}_tree{tree}.log"
                        target_file = f"{dataset}_rand{i}_md{md}_ml{ml}_tree{tree}.txt"
                        
                        tree_rules.append(os.path.join(base_dir, log_file))
                        target_paths.append(os.path.join(prompts_dir, target_file))
                    
                    # Build and execute commands
                    for i in range(len(ange)):
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
    start()