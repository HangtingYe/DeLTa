import os
import subprocess
import argparse

def start():
    # Dataset-specific configuration
    from dataset_config import dataset_params, default_params
    
    # Common parameters
    n_ensembles = ['9']
    datasets = list(dataset_params.keys())
    
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
                        cmd_parts = [
                            'python', 'ensemble.py',
                            '--small_model', small_model,
                            '--num_classes', str(num_class),
                            '--directory', f'model/classical_methods/data/{dataset}/RF',
                            '--n_ensemble', n_ensemble,
                            '--md', str(md),
                            '--ml', str(ml),
                            '--tree', str(tree),
                            '--dataset', dataset,
                        ]

                        log_file = f'model/classical_methods/data/{dataset}/e_RF_md{md}_ml{ml}_tree{tree}_{dataset}_{small_model}_{n_ensemble}.log'  
                        
                        # Execute command
                        try:
                            print(f"Executing command: {' '.join(cmd_parts)} > {log_file}")
                            with open(log_file, 'w') as f:
                                subprocess.run(cmd_parts, check=True, stdout=f, stderr=subprocess.STDOUT)
                        except subprocess.CalledProcessError as e:
                            print(f"Command failed: {' '.join(cmd_parts)}\nError: {e}")

if __name__ == "__main__":
    start()
    