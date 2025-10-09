import os
import time
import shlex
import subprocess
import itertools
import argparse

def start():
    datasets = ['adult']
    trees = [15]
    mds = [20]
    mls = [50]
    
    cmds = []
    for dataset in datasets:
        for tree in trees:
            for md in mds:
                for ml in mls:
                    log_file = f"{dataset}_randfull_md{md}_ml{ml}_tree{tree}.txt"
                    cmd_parts = [
                        'python', 'get_answer.py',
                        '--base_rule_path', f"data/{dataset}/prompts",
                        '--rule_path', log_file,
                        '--target_answer_path', f"data/{dataset}/answers"
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