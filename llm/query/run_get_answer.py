import time
import shlex
import subprocess
import itertools
import argparse
import os,sys
import subprocess
current_script_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(os.path.dirname(current_script_path), '..', '..'))
sys.path.append(project_root)
from dataset_config import dataset_params, default_params

def start():
    datasets = ['bank']
    cmds = []
    for dataset in datasets:
        params = dataset_params.get(dataset, default_params)
        mds = params['mds']
        mls = params['mls']
        trees = params['n_estimators']
        target_answer_path = f"../answers/{dataset}"
        if not os.path.exists(target_answer_path):
            print(f"Creating prompts directory: {target_answer_path}")
            os.makedirs(target_answer_path)
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
    
    for cmd in cmds:
        try:
            print(f"Executing command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{cmd}' failed with error: {e}")


if __name__ == "__main__":

    start()

