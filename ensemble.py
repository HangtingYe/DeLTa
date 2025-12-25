import numpy as np
import sklearn.metrics as skm
import os
import argparse
import re
import warnings
from dataset_config import dataset_params, default_params
from model.utils import integrate_predictions,ensemble_vote,calculate_metrics,show_results
# Configure argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--num_classes', type=str, default='1')
parser.add_argument('--small_model', type=str)
parser.add_argument('--n_ensemble', type=str)
parser.add_argument('--md', type=str)
parser.add_argument('--ml', type=str)
parser.add_argument('--tree', type=str)
parser.add_argument('--dataset', type=str)
args = parser.parse_args()
print(args)


if __name__ == "__main__":
    # Load predictions and labels
    predictions, test_label = integrate_predictions(args)

    # Generate ensemble distributions
    LM_class_distribution = ensemble_vote(args,predictions, is_rf=False)
    RF_class_distribution = ensemble_vote(args,predictions, is_rf=True)

    # Show appropriate metrics based on task type
    if int(args.num_classes) == 1:
        # Regression task evaluation
        # Evaluate RF performance
        rf_results, rf_metric_name = calculate_metrics(args,RF_class_distribution, test_label)
        print('RF RMSE MEAN:', rf_results[2])
        print('RF nRMSE MEAN:', rf_results[3])
        
        # Evaluate fused model
        # Adjust fusion weight i as needed
        i = 0.001
        fused_class_distribution = LM_class_distribution + i * RF_class_distribution
        print('Fused class_distribution sample:', fused_class_distribution[0])
        fused_results, fused_metric_name = calculate_metrics(args,fused_class_distribution, test_label)
        print('Fused RMSE MEAN:', fused_results[2])
        print('Fused nRMSE MEAN:', fused_results[3])
        
        
    else:
        # Classification task evaluation
        # Evaluate RF performance
        rf_results, rf_metric_name = calculate_metrics(args,RF_class_distribution, test_label)
        print('RF Accuracy MEAN:', rf_results[0])
        print('RF AUC MEAN:', rf_results[-1])
        
        # Evaluate fused model
        # Adjust fusion weight i as needed
        params = dataset_params.get(args.dataset, default_params)
        i = params['eta']
        #i = 0.2
        fused_class_distribution = i * LM_class_distribution + RF_class_distribution
        fused_results, fused_metric_name = calculate_metrics(args,fused_class_distribution, test_label)
        print(f'Fused Accuracy MEAN: {fused_results[0]}')
        print(f'Fused AUC MEAN: {fused_results[-1]}')

    # Suppress specific warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.metrics._classification", message=".*Precision is ill-defined.*")
    
