import os
import subprocess

def start():
    # Dataset-specific parameters stored in a dictionary
    from dataset_config import dataset_params, default_params

    # List of datasets to process (uses keys from dataset_params)
    # datasets = list(dataset_params.keys())
    datasets = ['adult']
    for dataset in datasets:
        # Get parameters for current dataset or use defaults
        params = dataset_params.get(dataset, default_params)
        mds = params['mds']
        mls = params['mls']
        n_estimators_list = params['n_estimators']
        
        # Create output directory if it doesn't exist
        output_dir = f"results/{dataset}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate commands for all parameter combinations
        cmds = []
        for n_estimator in n_estimators_list:
            for md in mds:
                for ml in mls:
                    cmd_parts = [
                        'python', 'train_model_classical.py',
                        '--task_type', 'full',
                        '--n_estimators', str(n_estimator),
                        '--max_depth', str(md),
                        '--max_leaf_nodes', str(ml),
                        '--dataset', dataset,
                        '--dataset_path', 'example_datasets',
                        '--seed_num', '1',
                        '--model_type', 'RandomForest_save',
                        '--save_npy', f'{output_dir}/{dataset}_md{md}_ml{ml}_tree{n_estimator}'
                    ]
                    
                    log_file = f'{output_dir}/{dataset}_md{md}_ml{ml}_tree{n_estimator}.log'
                    cmds.append((cmd_parts, log_file))
        
        # Execute all generated commands
        for cmd_parts, log_file in cmds:
            try:
                print(f"Executing command: {' '.join(cmd_parts)} > {log_file}")
                with open(log_file, 'w') as f:
                    subprocess.run(cmd_parts, check=True, stdout=f, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                print(f"Command failed: {' '.join(cmd_parts)}\nError: {e}")

if __name__ == "__main__":
    start()

    
