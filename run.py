import os
import subprocess
import argparse

def start():
    # Dataset-specific configuration
    from dataset_config import dataset_params, default_params
    
    # Common parameters
    shot_range = ['full']
    n_answers = 10
    model_type = 'DeLTa'
    datasets = list(dataset_params.keys())
    
    for dataset in datasets:
        # Get dataset-specific parameters or use defaults
        params = dataset_params.get(dataset, default_params)
        mds = params['mds']
        mls = params['mls']
        n_estimators = params['n_estimators']
        # Directly assign knn from parameters instead of looping
        small_model = params['small_model']
        
        # Build base classify rule path
        base_classify_rule = f'model.classical_methods.llm_rule.{dataset}.'
        
        # Iterate through all parameter combinations 
        for tree in n_estimators:
            for md in mds:
                for ml in mls:
                    # Generate classification rules inside the loop to use current md and ml values
                    classify_rules = []
                    for i in range(len(shot_range)):
                        current_rules = []
                        for j in range(n_answers):
                            rule = f'tree_{shot_range[i]}_md{md}_ml{ml}_{j}'
                            current_rules.append(rule)
                        classify_rules.append(current_rules)
                    
                    # Generate commands for each shot range and answer
                    cmds = []
                    for i in range(len(shot_range)):
                        for j in range(n_answers):
                            cmd_parts = [
                                'python', 'train_model_classical.py',
                                '--task_type', 'full',
                                '--small_model', small_model,
                                '--classify_rule', f'{base_classify_rule}{classify_rules[i][j]}',
                                '--dataset', dataset,
                                '--dataset_path', 'example_datasets',
                                '--seed_num', '1',
                                '--model_type', model_type,
                                '--gpu', '0',
                                '--cat_policy', 'ordinal',
                                '--save_npy',
                                f'model/classical_methods/data/{dataset}/RF_md{md}_ml{ml}_tree{tree}_full_{small_model}_{j}'
                            ]
                            
                            log_file = f"model/classical_methods/data/{dataset}/RF_md{md}_ml{ml}_tree{tree}_{dataset}_shotfull_{j}_{small_model}.log"
                            cmds.append((cmd_parts, log_file))
                    
                    # Execute all commands for current parameter combination
                    for cmd_parts, log_file in cmds:
                        try:
                            print(f"Executing command: {' '.join(cmd_parts)} > {log_file}")
                            with open(log_file, 'w') as f:
                                subprocess.run(cmd_parts, check=True, stdout=f, stderr=subprocess.STDOUT)
                        except subprocess.CalledProcessError as e:
                            print(f"Command failed: {' '.join(cmd_parts)}\nError: {e}")

if __name__ == "__main__":
    start()
    