import numpy as np
import sklearn.metrics as skm
import os
import argparse
import re
import warnings
from dataset_config import dataset_params, default_params
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


def integrate_predictions():
    """Integrate prediction results and labels by loading data from files"""
    predictions = {}
    test_label_loaded = None
    
    data_name = args.dataset
    new_directory = f'results/{data_name}'
    
    # Compile regex patterns
    pattern1 = re.compile(
        fr"RF_md{args.md}_ml{args.ml}_tree{args.tree}_full_{args.small_model}_([0-{int(args.n_ensemble)}]).npy")
    pattern2 = re.compile(
        fr"{args.dataset}_md{args.md}_ml{args.ml}_tree{args.tree}.npy")
    
    # Process files in directory
    for root, _, files in os.walk(new_directory):
        for file in files:
            # Check for pattern1 matches
            if pattern1.search(file):
                file_path = os.path.join(root, file)
                loaded_data = np.load(file_path, allow_pickle=True).item()
                predictions[file_path] = loaded_data['logit']
                current_label = loaded_data['label']
                
            # Check for pattern2 matches
            elif pattern2.search(file):
                file_path = os.path.join(root, file)
                print(f'file_path: {file_path}')
                loaded_data = np.load(file_path, allow_pickle=True).item()
                predictions[file_path] = loaded_data['logit']
                current_label = loaded_data['label']
                
            # Skip non-matching files
            else:
                continue
                
            # Validate label consistency
            if test_label_loaded is None:
                test_label_loaded = current_label
            elif not np.array_equal(test_label_loaded, current_label):
                raise ValueError("Inconsistent labels detected between files.")
    
    return predictions, test_label_loaded


def ensemble_vote(predictions, is_rf=False):
    """
    Ensemble predictions from multiple models
    
    Args:
        predictions: Dictionary of {file_path: logits}
        is_rf: Whether to use RF voting criteria (True=RF, False=LM)
        
    Returns:
        np.array: Ensemble class distributions
    """
    # Filter predictions based on voting type
    P = []
    for key in predictions.keys():
        # RF voting criteria
        if is_rf:
            if f'md{args.md}_ml{args.ml}_tree{args.tree}' in key and args.small_model not in key:
                P.append(predictions[key])
                print('RF_vote:', key)
        # LM voting criteria
        else:
            if f'md{args.md}_ml{args.ml}_tree{args.tree}_full' in key and args.small_model in key:
                P.append(predictions[key])
                print('LM_vote:', key)

    if not P:
        raise ValueError("No matching predictions found for voting")
    
    num_samples = len(P[0])
    class_distribution = []
    
    # Use mean for regression, sum for classification
    aggregation_func = np.mean if int(args.num_classes) == 1 else np.sum
    
    for i in range(num_samples):
        sample_predictions = [pred[i] for pred in P]
        aggregated = aggregation_func(sample_predictions, axis=0)
        class_distribution.append(aggregated)
    
    return np.array(class_distribution)


def check_softmax(logits):
    """Check and ensure input is normalized softmax probability distribution"""
    if np.any((logits < 0) | (logits > 1)) or (not np.allclose(logits.sum(axis=-1), 1, atol=1e-5)):
        exps = np.exp(logits - np.max(logits, axis=1, keepdims=True)) 
        return exps / np.sum(exps, axis=1, keepdims=True)
    else:
        return logits
        
import json
def load_y_info(dataset_name):
    save_dir = "reg_info"
    load_path = os.path.join(save_dir, f"{dataset_name}.json")
    
    if not os.path.exists(load_path):
        print(f"Error: y_info file {load_path} does not exist!")
        return None  
    
    try:
        with open(load_path, "r", encoding="utf-8") as f:
            y_info = json.load(f) 
        print(f"y_info loaded successfully from {load_path}")
        return y_info  
    
    except json.JSONDecodeError:
        print(f"Error: {load_path} is not a valid JSON file ")
        return None
    except Exception as e:
        print(f"Failed to load y_info from {load_path}, error: {str(e)}")
        return None

def calculate_metrics(test_logit, labels):
    """
    Automatically determine task type and calculate metrics based on number of classes:
    - Regression when num_classes == 1
    - Classification when num_classes >= 2
    
    Parameters:
        test_logit: Model predictions (numeric values for regression, logits/probabilities for classification)
        labels: Ground truth labels
    
    Returns:
        metric_values: Tuple of metric values
        metric_names: Tuple of metric names
    """
    # Determine task type based on number of classes
    if int(args.num_classes) == 1:
        # Regression task handling
        if args is None:
            raise ValueError("args parameter is required for regression tasks")
            
        # Basic regression metrics
        mae = skm.mean_absolute_error(labels, test_logit)
        nrmse = np.sqrt(skm.mean_squared_error(labels, test_logit))
        r2 = skm.r2_score(labels, test_logit)
        y_info = load_y_info(args.dataset)
        std = y_info['std']
        if y_info['policy'] == 'mean_std':
            mae *= std
            rmse = nrmse * std
        else:
            rmse = nrmse  # Use unstandardized RMSE if no matching std
        
        metric_values = (mae, r2, rmse, nrmse)
        metric_names = ("MAE", "R2", "RMSE", "nRMSE")
        
    elif int(args.num_classes) >= 2:
        # Classification task handling
        # Ensure input is normalized probability distribution
        test_logit = check_softmax(test_logit)
        pred_labels = test_logit.argmax(axis=-1)
        
        # Common classification metrics
        accuracy = skm.accuracy_score(labels, pred_labels)
        avg_recall = skm.balanced_accuracy_score(labels, pred_labels)
        avg_precision = skm.precision_score(labels, pred_labels, average='macro')
        log_loss = skm.log_loss(labels, test_logit)
        
        # Binary vs multi-class handling
        if int(args.num_classes) == 2:
            f1_score = skm.f1_score(labels, pred_labels, average='binary')
            auc = skm.roc_auc_score(labels, test_logit[:, 1])
        else:
            f1_score = skm.f1_score(labels, pred_labels, average='macro')
            auc = skm.roc_auc_score(labels, test_logit, average='macro', multi_class='ovr')
        
        metric_values = (accuracy, avg_recall, avg_precision, f1_score, log_loss, auc)
        metric_names = ("Accuracy", "Avg_Recall", "Avg_Precision", "F1", "LogLoss", "AUC")
        
    else:
        raise ValueError(f"Invalid num_classes value: {args.num_classes}. Use 1 for regression or >=2 for classification")
    
    return metric_values, metric_names
    
def show_results_classical(metric_name, results_list):
    """Display results for classical models"""
    metric_arrays = {name: [] for name in metric_name}

    for result in results_list:
        for idx, name in enumerate(metric_name):
            metric_arrays[name].append(result[idx])
    
    mean_metrics = {name: np.mean(metric_arrays[name]) for name in metric_name}
    std_metrics = {name: np.std(metric_arrays[name]) for name in metric_name}

    # Printing results
    print(f'ensemble: {1} Trials')
    for name in metric_name:
        formatted_results = ', '.join(['{:.8f}'.format(e) for e in metric_arrays[name]])
        print(f'{name} Results: {formatted_results}')
        print(f'{name} MEAN = {mean_metrics[name]:.8f} ± {std_metrics[name]:.8f}')

    print('-' * 50)

if __name__ == "__main__":
    # Load predictions and labels
    predictions, test_label = integrate_predictions()

    # Generate ensemble distributions
    LM_class_distribution = ensemble_vote(predictions, is_rf=False)
    RF_class_distribution = ensemble_vote(predictions, is_rf=True)

    # Show appropriate metrics based on task type
    if int(args.num_classes) == 1:
        # Regression task evaluation
        # Evaluate LM performance
        lm_results, lm_metric_name = calculate_metrics(LM_class_distribution, test_label)
        print('LM RMSE MEAN:', lm_results[2])
        print('LM nRMSE MEAN:', lm_results[3])
        
        # Evaluate RF performance
        rf_results, rf_metric_name = calculate_metrics(RF_class_distribution, test_label)
        print('RF RMSE MEAN:', rf_results[2])
        print('RF nRMSE MEAN:', rf_results[3])
        
        # Evaluate fused model
        # Adjust fusion weight i as needed
        i = 0.001
        fused_class_distribution = LM_class_distribution + i * RF_class_distribution
        print('Fused class_distribution sample:', fused_class_distribution[0])
        fused_results, fused_metric_name = calculate_metrics(fused_class_distribution, test_label)
        print('Fused RMSE MEAN:', fused_results[2])
        print('Fused nRMSE MEAN:', fused_results[3])
        
        # Optional: Save fused results
        # np.save(f'model/classical_methods/data/draw/reg/di_beste_RF_md{args.md}_ml{args.ml}_tree{args.tree}_full_{args.knn_type}.npy', fused_class_distribution)
        
    else:
        # Classification task evaluation
        # Evaluate RF performance
        rf_results, rf_metric_name = calculate_metrics(RF_class_distribution, test_label)
        print('RF Accuracy MEAN:', rf_results[0])
        print('RF AUC MEAN:', rf_results[-1])
        
        # Evaluate fused model
        # Adjust fusion weight i as needed
        params = dataset_params.get(args.dataset, default_params)
        i = params['eta']
        #i = 0.2
        fused_class_distribution = i * LM_class_distribution + RF_class_distribution
        fused_results, fused_metric_name = calculate_metrics(fused_class_distribution, test_label)
        print(f'Fused Accuracy MEAN: {fused_results[0]}')
        print(f'Fused AUC MEAN: {fused_results[-1]}')

    # Suppress specific warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.metrics._classification", message=".*Precision is ill-defined.*")
    
