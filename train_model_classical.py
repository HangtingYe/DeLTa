from tqdm import tqdm
from model.utils import (
    get_classical_args,tune_hyper_parameters,
    show_results_classical,get_method,set_seeds
)
from model.lib.data import (
    get_dataset
)
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import time
import re

if __name__ == '__main__':
    results_list, time_list = [], []
    args,default_para,opt_space = get_classical_args()
    args.dataset_path = 'DeLTa-main/example_datasets'
    train_val_data,test_data,info = get_dataset(args.dataset,args.dataset_path)
    if args.tune:
        args = tune_hyper_parameters(args,opt_space,train_val_data,info)
    
    ## Training Stage over different random seeds
    for seed in tqdm(range(args.seed_num)):
        args.seed = seed    # update seed  
        set_seeds(args.seed)
        method = get_method(args.model_type)(args, info['task_type'] == 'regression')
        start_train = time.time()
        time_cost = method.fit(train_val_data, info,train=True)   
        end_train = time.time()
        train_time = end_train - start_train

        start_test = time.time()
        vres, metric_name, predict_logits = method.predict(test_data, info, model_name=args.evaluate_option)
        end_test = time.time()
        test_time = end_test - start_test

        results_list.append(vres)
        time_list.append(time_cost)
    show_results_classical(args,info, metric_name,results_list,time_list)
