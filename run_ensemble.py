import os
import subprocess
import argparse

def start():
    """Generate and execute ensemble.py commands for multiple parameter combinations"""
    # Dataset-specific configuration
    from dataset_config import dataset_params, default_params
    
    # Common parameters
    n_ensembles = ['9']
    # datasets = list(dataset_params.keys())
    datasets = ['bank']
    
    # Iterate through target datasets
    for dataset in datasets:
        # Get dataset-specific parameters or use defaults
        params = dataset_params.get(dataset, default_params)
        mds = params['mds']
        mls = params['mls']
        n_estimators = params['n_estimators']
        num_class = params['num_class']
        small_model = params['small_model']
        
        # Iterate through all parameter combinations for this dataset
        for md in mds:
            for ml in mls:
                for tree in n_estimators:
                    for n_ensemble in n_ensembles:
                        # Build command to execute ensemble.py with current parameters
                        cmd_parts = [
                            'python', 'ensemble.py',
                            '--small_model', small_model,
                            '--num_classes', str(num_class),
                            '--n_ensemble', n_ensemble,
                            '--md', str(md),
                            '--ml', str(ml),
                            '--tree', str(tree),
                            '--dataset', dataset,
                        ]

                        # Define log file path for command output
                        log_file = f'results/{dataset}/e_RF_md{md}_ml{ml}_tree{tree}_{dataset}_{small_model}_{n_ensemble}.log'  
                        
                        # Execute command and redirect output to log file
                        try:
                            print(f"Executing command: {' '.join(cmd_parts)} > {log_file}")
                            with open(log_file, 'w') as f:
                                subprocess.run(cmd_parts, check=True, stdout=f, stderr=subprocess.STDOUT)
                        except subprocess.CalledProcessError as e:
                            print(f"Command failed: {' '.join(cmd_parts)}\nError: {e}")

if __name__ == "__main__":
    # Entry point: start command generation and execution
    start()
