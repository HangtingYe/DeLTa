import os
import shutil
import time
import errno
import pprint
import torch
import numpy as np
import random
import json
import os.path as osp
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text
from tabpfn import TabPFNClassifier,TabPFNRegressor
import copy


THIS_PATH = os.path.dirname(__file__)
############## DeLTa ########################
def assign_leaf(tree, sample):
    """Recursively assign sample to leaf node based on decision tree rules"""
    if "id" in tree:                
        return tree["id"]
    
    feature = tree["feature"]
    threshold = tree["threshold"]
    operator = tree["operator"]
    
    if operator == "<=":
        if sample[feature] <= threshold:
            return assign_leaf(tree["left"], sample)
        else:
            return assign_leaf(tree["right"], sample)
    elif operator == ">":
        if sample[feature] > threshold:
            return assign_leaf(tree["right"], sample)
        else:
            return assign_leaf(tree["left"], sample)
    else:
        raise ValueError(f"Unsupported operator: {operator}")
from collections import defaultdict
def build_leaf_index_dict(tree, train_data):
    """Build dictionary mapping leaf IDs to sample indices in training data"""
    leaf_index_dict = defaultdict(list)
    
    for idx, sample in enumerate(train_data):
        leaf_id = assign_leaf(tree, sample.astype(float)) 
        leaf_index_dict[leaf_id].append(idx)        
    return dict(leaf_index_dict)

def replace_subtree(tree, subtree, new_subtree):
    """Recursively replace subtree with new subtree in decision tree"""
    if 'id' in tree:
        return tree
    if tree == subtree:
        return new_subtree
    if 'left' in tree:
        tree['left'] = replace_subtree(tree['left'], subtree, new_subtree)
    if 'right' in tree:
        tree['right'] = replace_subtree(tree['right'], subtree, new_subtree)
    return tree
def find_sibling_leaf(tree, leaf_id):
    """Find sibling leaf node for a given leaf ID (same parent)"""
    if "id" in tree:
        return None
    if "id" in tree["left"] and tree["left"]["id"] == leaf_id:
        if "id" in tree["right"]:
            return tree["right"]["id"]
        else:
            return None
    if "id" in tree["right"] and tree["right"]["id"] == leaf_id:
        if "id" in tree["left"]:
            return tree["left"]["id"]
        else:
            return None
    left_result = find_sibling_leaf(tree["left"], leaf_id)
    if left_result is not None:
        return left_result
    right_result = find_sibling_leaf(tree["right"], leaf_id)
    if right_result is not None:
        return right_result

    return None
def find_parent_node(tree, leaf_id):
    """
    Find the parent node of a given leaf node.
    """
    if "id" in tree:
        return None  

    if "left" in tree:
        if "id" in tree["left"] and tree["left"]["id"] == leaf_id:
            return tree
        parent_left = find_parent_node(tree["left"], leaf_id)
        if parent_left:
            return parent_left

    if "right" in tree:
        if "id" in tree["right"] and tree["right"]["id"] == leaf_id:
            return tree
        parent_right = find_parent_node(tree["right"], leaf_id)
        if parent_right:
            return parent_right

    return None
def find_valid_parent_knn(tree, leaf_id, real_leaf_id, leaf_index_dict, selected):
    """Find valid parent node for missing leaf ID (returns samples/labels for KNN)"""
    parent_leaf = find_parent_node(tree, leaf_id)  
    new_tree = {"id": "leaf_x"}
    replaced_subtree = replace_subtree(tree, parent_leaf, new_tree)
    parent_leaf_index_dict = build_leaf_index_dict(replaced_subtree, selected)

    if "leaf_x" in parent_leaf_index_dict:
        leaf_index_dict[real_leaf_id] = parent_leaf_index_dict["leaf_x"]
        return leaf_index_dict
    else:
        leaf_id = 'leaf_x'
        return find_valid_parent_knn(replaced_subtree, leaf_id, real_leaf_id, leaf_index_dict, selected)

def calculate_leaf_grad(args, model_leaf, leaf_index_dict,is_regression, selected, selected_y, train_logit, one_model_list, n_class):
    """Train leaf-level regression models to fit negative gradients (classification/regression)"""
    print('fitting negative gradient')
    if not is_regression:
        num_classes = len(np.unique(selected_y))
        for leaf_id, indices in leaf_index_dict.items():
            if leaf_id in model_leaf.keys():
                continue
            # true labels
            leaf_targets = selected_y[indices]  # y
            one_hot_encoding = np.zeros((leaf_targets.shape[0], num_classes), dtype=float)
            one_hot_encoding[np.arange(leaf_targets.shape[0]), leaf_targets] = 1
            
            # construct negative gradient labels
            logit = train_logit[indices]
            if (leaf_id in one_model_list):  # mlp output has 2 columns
                print(leaf_id, 'in', 'one_model_list')
                cla = one_model_list[leaf_id]  # array([1])
                a_ = np.zeros((logit.shape[0], n_class), dtype=float)
                np.put_along_axis(a_, cla.reshape(1, -1), logit, axis=1)
                logit = a_
            
            def check_softmax(logits):
                """Ensure logits are normalized to valid probability distribution"""
                if np.any((logits < 0) | (logits > 1)) or (not np.allclose(logits.sum(axis=-1), 1, atol=1e-5)):
                    exps = np.exp(logits - np.max(logits, axis=1, keepdims=True))
                    return exps / np.sum(exps, axis=1, keepdims=True)
                else:
                    return logits
            
            softmax_result = check_softmax(logit)
            leaf_targets2 = one_hot_encoding - softmax_result
            set_ = selected[indices].astype(float)
            y_ = leaf_targets2

            # train regression model
            if args.small_model == 'cart':
                model = DecisionTreeRegressor(max_depth=5, max_leaf_nodes=20, random_state=42)
            elif args.small_model == 'tabpfn': 
                if set_.shape[0] > 1 and leaf_id not in one_model_list.keys():
                    model = TabPFNRegressor(device='cuda', ignore_pretraining_limits=True, random_state=args.seed) 
                else:
                    model = DecisionTreeRegressor(max_depth=5, max_leaf_nodes=20, random_state=42)
            from sklearn.multioutput import MultiOutputRegressor

            if set_.shape[0] > 5000:
                selected_rows = np.random.choice(set_.shape[0], 5000, replace=False) 
                set_, y_ = set_[selected_rows], y_[selected_rows]

            model = MultiOutputRegressor(model)
            model.fit(set_, y_)
            model_leaf[leaf_id] = model
    else:
        rf = 0.001
        for leaf_id, indices in leaf_index_dict.items():
            if leaf_id in model_leaf.keys():
                continue
            print('leaf_id :', leaf_id)
            # true labels
            leaf_label = selected_y[indices]  

            # construct negative gradient labels
            logit = train_logit[indices]
            leaf_targets2 = leaf_label - rf * logit  # regression negative gradient
            set_ = selected[indices].astype(float)
            y_ = leaf_targets2

            # train regression model
            if args.small_model == 'cart':
                model = DecisionTreeRegressor(max_depth=5, max_leaf_nodes=20, random_state=42)
            elif args.small_model == 'tabpfn':  
                if len(set_) == 1 or np.unique(y_).shape[0] == 1:
                    model = DecisionTreeRegressor(max_depth=5, max_leaf_nodes=20, random_state=42)
                else:
                    model = TabPFNRegressor(device='cuda', ignore_pretraining_limits=True, random_state=args.seed)

            if set_.shape[0] > 5000:
                selected_rows = np.random.choice(set_.shape[0], 5000, replace=False)
                set_, y_ = set_[selected_rows], y_[selected_rows]

            model.fit(set_, y_)
            model_leaf[leaf_id] = model

    return model_leaf

def predict_group(X, leaf_index_dict, tree, model_leaf, one_model_list, selected, selected_y, args, train_logit, n_class, is_regression):
    """Group test samples by leaf ID, predict with leaf-level models (handle missing leaves)"""
    leaf_groups = defaultdict(list)
    for idx, sample in enumerate(X):
        leaf_id = assign_leaf(tree, sample.astype(float))
        if leaf_id in leaf_index_dict.keys():
            a = np.array([idx, sample], dtype=object)
            leaf_groups[leaf_id].append(a)
        else:
            print('leaf_index_dict missing leaf_id:', leaf_id)
            # Fallback 1: use sibling leaf ID if available
            sibling_leaf_id = find_sibling_leaf(tree, leaf_id)
            if sibling_leaf_id in leaf_index_dict:
                print(f"{leaf_id} replaced by {sibling_leaf_id}")
                leaf_index_dict[leaf_id] = leaf_index_dict[sibling_leaf_id]
                model_leaf[leaf_id] = model_leaf[sibling_leaf_id]
                if sibling_leaf_id in one_model_list:
                    one_model_list[leaf_id] = one_model_list[sibling_leaf_id]
                leaf_groups[leaf_id].append(np.array([idx, sample], dtype=object))
            else:
                # Fallback 2: find parent node for missing leaf
                print("No sibling, finding parent")
                leaf_index_dict = find_valid_parent_knn(copy.deepcopy(tree), leaf_id, leaf_id, leaf_index_dict, selected)
                model_leaf = calculate_leaf_grad(args, model_leaf, leaf_index_dict,is_regression, selected, selected_y, train_logit, one_model_list, n_class)
                leaf_groups[leaf_id].append(np.array([idx, sample], dtype=object))
    
    # Collect predictions and sort by sample index
    ID = np.array([])
    PRED = np.array([])
   
    for leaf_id in leaf_groups.keys():
        model = model_leaf[leaf_id]
        group = np.array(leaf_groups[leaf_id])
        group_id = group[:, 0].reshape(-1, 1)
        if ID.size == 0:
            ID = group_id
        else:
            ID = np.vstack((ID, group_id))
        
        group_feature = np.array([sample[1] for sample in group])
        pred = model.predict(group_feature)
        
        if PRED.size == 0:
            PRED = pred
        else:
            if not is_regression:
                PRED = np.vstack((PRED, pred))
            else:
                PRED = np.concatenate((PRED, pred))
    
    # Sort predictions by original sample index
    sorted_indices = np.argsort(ID, axis=0)
    id_sorted = ID[sorted_indices]
    pred_sorted = PRED[sorted_indices[:, 0]]
    
    return pred_sorted  
################################################
############## ensemble ########################
import re
def integrate_predictions(args):
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
def ensemble_vote(args,predictions, is_rf=False):
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
def calculate_metrics(args,test_logit, labels):
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
def show_results(args,metric_name, results_list):
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
######################################


def mkdir(path):
    """
    Create a directory if it does not exist.

    :path: str, path to the directory
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def set_gpu(x):
    """
    Set environment variable CUDA_VISIBLE_DEVICES
    
    :x: str, GPU id
    """
    os.environ['CUDA_VISIBLE_DEVICES'] = x
    print('using gpu:', x)


def ensure_path(path, remove=True):
    """
    Ensure a path exists.

    path: str, path to the directory
    remove: bool, whether to remove the directory if it exists
    """
    if os.path.exists(path):
        if remove:
            if input('{} exists, remove? ([y]/n)'.format(path)) != 'n':
                shutil.rmtree(path)
                os.mkdir(path)
    else:
        os.mkdir(path)


#  --- criteria helper ---
class Averager():
    """
    A simple averager.

    """
    def __init__(self):
        self.n = 0
        self.v = 0

    def add(self, x):
        """
        
        :x: float, value to be added
        """
        self.v = (self.v * self.n + x) / (self.n + 1)
        self.n += 1

    def item(self):
        return self.v

class Timer():

    def __init__(self):
        self.o = time.time()

    def measure(self, p=1):
        """
        Measure the time since the last call to measure.

        :p: int, period of printing the time
        """

        x = (time.time() - self.o) / p
        x = int(x)
        if x >= 3600:
            return '{:.1f}h'.format(x / 3600)
        if x >= 60:
            return '{}m'.format(round(x / 60))
        return '{}s'.format(x)

_utils_pp = pprint.PrettyPrinter()
def pprint(x):
    _utils_pp.pprint(x)

#  ---- import from lib.util -----------
def set_seeds(base_seed: int, one_cuda_seed: bool = False) -> None:
    """
    Set random seeds for reproducibility.

    :base_seed: int, base seed
    :one_cuda_seed: bool, whether to set one seed for all GPUs
    """
    assert 0 <= base_seed < 2 ** 32 - 10000
    random.seed(base_seed)
    np.random.seed(base_seed + 1)
    print('np.random.seed(base_seed + 1):',base_seed + 1)
    torch.manual_seed(base_seed + 2)
    cuda_seed = base_seed + 3
    if one_cuda_seed:
        torch.cuda.manual_seed_all(cuda_seed)
    elif torch.cuda.is_available():
        # the following check should never succeed since torch.manual_seed also calls
        # torch.cuda.manual_seed_all() inside; but let's keep it just in case
        if not torch.cuda.is_initialized():
            torch.cuda.init()
        # Source: https://github.com/pytorch/pytorch/blob/2f68878a055d7f1064dded1afac05bb2cb11548f/torch/cuda/random.py#L109
        for i in range(torch.cuda.device_count()):
            default_generator = torch.cuda.default_generators[i]
            default_generator.manual_seed(cuda_seed + i)

def get_device() -> torch.device:
    return torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

import sklearn.metrics as skm
def rmse(y, prediction, y_info):
    """
    
    :y: np.ndarray, ground truth
    :prediction: np.ndarray, prediction
    :y_info: dict, information about the target variable
    :return: float, root mean squared error
    """
    rmse = skm.mean_squared_error(y, prediction) ** 0.5  # type: ignore[code]
    if y_info['policy'] == 'mean_std':
        rmse *= y_info['std']
    return rmse
    
def load_config(args, config=None, config_name=None):
    """
    Load the config file.

    :args: argparse.Namespace, arguments
    :config: dict, config file
    :config_name: str, name of the config file
    :return: argparse.Namespace, arguments
    """
    if config is None:
        config_path = os.path.join(os.path.abspath(os.path.join(THIS_PATH, '..')), 
                                   'configs', args.dataset, 
                                   '{}.json'.format(args.model_type if args.config_name is None else args.config_name))
        with open(config_path, 'r') as fp:
            config = json.load(fp)

    # set additional parameters
    args.config = config 

    # save the config files
    with open(os.path.join(args.save_path, 
                           '{}.json'.format('config' if config_name is None else config_name)), 'w') as fp:
        args_dict = vars(args)
        if 'device' in args_dict:
            del args_dict['device']
        json.dump(args_dict, fp, sort_keys=True, indent=4)

    return args

# parameter search
def sample_parameters(trial, space, base_config):
    """
    Sample hyper-parameters.

    :trial: optuna.trial.Trial, trial
    :space: dict, search space
    :base_config: dict, base configuration
    :return: dict, sampled hyper-parameters
    """
    def get_distribution(distribution_name):
        return getattr(trial, f'suggest_{distribution_name}')

    result = {}
    for label, subspace in space.items():
        if isinstance(subspace, dict):
            result[label] = sample_parameters(trial, subspace, base_config)
        else:
            assert isinstance(subspace, list)
            distribution, *args = subspace

            if distribution.startswith('?'):
                default_value = args[0]
                result[label] = (
                    get_distribution(distribution.lstrip('?'))(label, *args[1:])
                    if trial.suggest_categorical(f'optional_{label}', [False, True])
                    else default_value
                )

            elif distribution == '$mlp_d_layers':
                min_n_layers, max_n_layers, d_min, d_max = args
                n_layers = trial.suggest_int('n_layers', min_n_layers, max_n_layers)
                suggest_dim = lambda name: trial.suggest_int(name, d_min, d_max)  # noqa
                d_first = [suggest_dim('d_first')] if n_layers else []
                d_middle = (
                    [suggest_dim('d_middle')] * (n_layers - 2) if n_layers > 2 else []
                )
                d_last = [suggest_dim('d_last')] if n_layers > 1 else []
                result[label] = d_first + d_middle + d_last

            elif distribution == '$d_token':
                assert len(args) == 2
                try:
                    n_heads = base_config['model']['n_heads']
                except KeyError:
                    n_heads = base_config['model']['n_latent_heads']

                for x in args:
                    assert x % n_heads == 0
                result[label] = trial.suggest_int('d_token', *args, n_heads)  # type: ignore[code]

            elif distribution in ['$d_ffn_factor', '$d_hidden_factor']:
                if base_config['model']['activation'].endswith('glu'):
                    args = (args[0] * 2 / 3, args[1] * 2 / 3)
                result[label] = trial.suggest_uniform('d_ffn_factor', *args)

            else:
                result[label] = get_distribution(distribution)(label, *args)
    return result

def merge_sampled_parameters(config, sampled_parameters):
    """
    Merge the sampled hyper-parameters.

    :config: dict, configuration
    :sampled_parameters: dict, sampled hyper-parameters
    """
    for k, v in sampled_parameters.items():
        if isinstance(v, dict):
            merge_sampled_parameters(config.setdefault(k, {}), v)
        else:
            # If there are parameters in the default config, the value of the parameter will be overwritten.
            config[k] = v

def get_classical_args():
    """
    Get the arguments for classical models.

    :return: argparse.Namespace, arguments
    """

    import argparse
    import warnings
    warnings.filterwarnings("ignore")
    with open('configs/classical_configs.json','r') as file:
        default_args = json.load(file)
    parser = argparse.ArgumentParser()
    #todo:cartl2l:
    parser.add_argument('--task_type', type=str, default='cls', choices=['cls', 'reg', 'full'])
    parser.add_argument('--shot', type=int, default=2)
    parser.add_argument('--few_shot_random_seed', type=int, default=42)#42 1024 0 1 32
    #parser.add_argument('--knn', type=bool, default=False)
    parser.add_argument('--small_model', type=str, default='noknn',choices=['noknn', 'knn','cart','catboost','logistics','tabpfn','mlp'])
    parser.add_argument('--classify_rule', type=str, default='my_module.my_classify_rule',
                        help='Import path of the classify_rule function')
    parser.add_argument('--tree_index', type=str, default=2)

    # todo:cartl2l_test:
    parser.add_argument('--data_regime', type=str, default='few_shot', choices=['few_shot', 'low_regime', 'full'])
    parser.add_argument('--save_npy', type=str)
    parser.add_argument('--multi', type=int, default=1)
    #parser.add_argument('--tree', type=str, default='my_module.my_classify_rule')

    #todo:randomforest；
    parser.add_argument('--n_estimators', type=int, default=3)
    parser.add_argument('--max_depth', type=int, default=3)
    parser.add_argument('--max_leaf_nodes', type=int, default=10)



    # basic parameters
    parser.add_argument('--dataset', type=str, default=default_args['dataset'])
    parser.add_argument('--model_type', type=str, 
                        default=default_args['model_type'], 
                        choices=['RandomForest_save','DeLTa','DeLTa1'])#todo

    # optimization parameters 
    parser.add_argument('--normalization', type=str, default=default_args['normalization'], choices=['none', 'standard', 'minmax', 'quantile', 'maxabs', 'power', 'robust'])
    parser.add_argument('--num_nan_policy', type=str, default=default_args['num_nan_policy'], choices=['mean', 'median'])
    parser.add_argument('--cat_nan_policy', type=str, default=default_args['cat_nan_policy'], choices=['new', 'most_frequent'])
    parser.add_argument('--cat_policy', type=str, default=default_args['cat_policy'], choices=['indices', 'ordinal', 'ohe', 'binary', 'hash', 'loo', 'target', 'catboost'])
    parser.add_argument('--num_policy',type=str, default=default_args['num_policy'],choices=['none','Q_PLE','T_PLE','Q_Unary','T_Unary','Q_bins','T_bins','Q_Johnson','T_Johnson'])
    parser.add_argument('--n_bins', type=int, default=default_args['n_bins'])
    parser.add_argument('--cat_min_frequency', type=float, default=default_args['cat_min_frequency'])

    # other choices
    parser.add_argument('--n_trials', type=int, default=default_args['n_trials'])    
    parser.add_argument('--seed_num', type=int, default=default_args['seed_num'])
    parser.add_argument('--gpu', default=default_args['gpu'])
    parser.add_argument('--tune', action='store_true', default=default_args['tune'])  
    parser.add_argument('--retune', action='store_true', default=default_args['retune'])  
    parser.add_argument('--dataset_path', type=str, default=default_args['dataset_path'])  
    parser.add_argument('--model_path', type=str, default=default_args['model_path'])
    parser.add_argument('--evaluate_option', type=str, default=default_args['evaluate_option']) 
    args = parser.parse_args()
    
    set_gpu(args.gpu)
    save_path1 = '-'.join([args.dataset, args.model_type])
    
    save_path2 = 'Norm-{}'.format(args.normalization)
    save_path2 += '-Nan-{}-{}'.format(args.num_nan_policy, args.cat_nan_policy)
    save_path2 += '-Cat-{}'.format(args.cat_policy)

    if args.cat_min_frequency > 0.0:
        save_path2 += '-CatFreq-{}'.format(args.cat_min_frequency)
    if args.tune:
        save_path1 += '-Tune'

    save_path = osp.join(save_path1, save_path2)
    args.save_path = osp.join(args.model_path, save_path)
    mkdir(args.save_path)    
    
    # load config parameters
    args.seed = 0
    
    config_default_path = os.path.join('configs','default',args.model_type+'.json')
    config_opt_path = os.path.join('configs','opt_space',args.model_type+'.json')
    with open(config_default_path,'r') as file:
        default_para = json.load(file)  
    
    with open(config_opt_path,'r') as file:
        opt_space = json.load(file)

    args.config = default_para[args.model_type]
    set_seeds(args.seed)
    if torch.cuda.is_available():     
        torch.backends.cudnn.benchmark = True
    pprint(vars(args))
    
    args.config['fit']['n_bins'] = args.n_bins
    return args,default_para,opt_space   

def get_deep_args():  
    """
    Get the arguments for deep learning models.

    :return: argparse.Namespace, arguments
    """
    import argparse 
    import warnings
    warnings.filterwarnings("ignore")

    parser = argparse.ArgumentParser()
    # basic parameters
    with open('configs/deep_configs.json','r') as file:
        default_args = json.load(file)
    parser.add_argument('--dataset', type=str, default=default_args['dataset'])
    parser.add_argument('--model_type', type=str, 
                        default=default_args['model_type'],
                        choices=['mlp', 'resnet', 'ftt', 'node', 'autoint',
                                 'tabpfn', 'tangos', 'saint', 'tabcaps', 'tabnet',
                                 'snn', 'ptarl', 'danets', 'dcn2', 'tabtransformer',
                                 'dnnr', 'switchtab', 'grownet', 'tabr', 'modernNCA',
                                 'hyperfast', 'bishop', 'realmlp', 'protogate', 'mlp_plr',
                                 'excelformer', 'grande','amformer','tabptm','trompt'
                                 ])
    #cartl2l
    parser.add_argument('--task_type', type=str, default='cls', choices=['cls', 'reg', 'full'])
    parser.add_argument('--shot', type=int, default=2)
    parser.add_argument('--small_model', type=str, default='noknn',choices=['noknn', 'knn','cart','catboost','logistics','tabpfn','mlp'])
    parser.add_argument('--classify_rule', type=str, default='my_module.my_classify_rule',
                        help='Import path of the classify_rule function')
    parser.add_argument('--tree_index', type=str, default=2)
    parser.add_argument('--data_regime', type=str, default='few_shot', choices=['few_shot', 'low_regime', 'full'])
    parser.add_argument('--save_npy', type=str)
    parser.add_argument('--multi', type=int, default=1)
    parser.add_argument('--few_shot_random_seed', type=int, default=42)#42 1024 0 1 32
    # optimization parameters
    parser.add_argument('--max_epoch', type=int, default=default_args['max_epoch'])
    parser.add_argument('--batch_size', type=int, default=default_args['batch_size'])  
    parser.add_argument('--normalization', type=str, default=default_args['normalization'], choices=['none', 'standard', 'minmax', 'quantile', 'maxabs', 'power', 'robust'])
    parser.add_argument('--num_nan_policy', type=str, default=default_args['num_nan_policy'], choices=['mean', 'median'])
    parser.add_argument('--cat_nan_policy', type=str, default=default_args['cat_nan_policy'], choices=['new', 'most_frequent'])
    parser.add_argument('--cat_policy', type=str, default=default_args['cat_policy'], choices=['indices', 'ordinal', 'ohe', 'binary', 'hash', 'loo', 'target', 'catboost','tabr_ohe'])
    parser.add_argument('--num_policy',type=str, default=default_args['num_policy'],choices=['none','Q_PLE','T_PLE','Q_Unary','T_Unary','Q_bins','T_bins','Q_Johnson','T_Johnson'])
    parser.add_argument('--n_bins', type=int, default=default_args['n_bins'])  
    parser.add_argument('--cat_min_frequency', type=float, default=default_args['cat_min_frequency'])

    # other choices
    parser.add_argument('--n_trials', type=int, default=default_args['n_trials'])    
    parser.add_argument('--seed_num', type=int, default=default_args['seed_num'])
    parser.add_argument('--workers', type=int, default=default_args['workers'])
    parser.add_argument('--gpu', default=default_args['gpu'])
    parser.add_argument('--tune', action='store_true', default=default_args['tune'])  
    parser.add_argument('--retune', action='store_true', default=default_args['retune'])  
    parser.add_argument('--evaluate_option', type=str, default=default_args['evaluate_option'])   
    parser.add_argument('--dataset_path', type=str, default=default_args['dataset_path'])  
    parser.add_argument('--model_path', type=str, default=default_args['model_path'])
    args = parser.parse_args()
    
    set_gpu(args.gpu)
    save_path1 = '-'.join([args.dataset, args.model_type])
    save_path2 = 'Epoch{}BZ{}'.format(args.max_epoch, args.batch_size)
    save_path2 += '-Norm-{}'.format(args.normalization)
    save_path2 += '-Nan-{}-{}'.format(args.num_nan_policy, args.cat_nan_policy)
    save_path2 += '-Cat-{}'.format(args.cat_policy)

    if args.cat_min_frequency > 0.0:
        save_path2 += '-CatFreq-{}'.format(args.cat_min_frequency)
    if args.tune:
        save_path1 += '-Tune'

    save_path = osp.join(save_path1, save_path2)
    args.save_path = osp.join(args.model_path, save_path)
    mkdir(args.save_path)    
    
    # load config parameters
    config_default_path = os.path.join('configs','default',args.model_type+'.json')
    config_opt_path = os.path.join('configs','opt_space',args.model_type+'.json')
    with open(config_default_path,'r') as file:
        default_para = json.load(file)  
    
    with open(config_opt_path,'r') as file:
        opt_space = json.load(file)
    args.config = default_para[args.model_type]
    
    args.seed = 0
    set_seeds(args.seed)
    if torch.cuda.is_available():     
        torch.backends.cudnn.benchmark = True
    pprint(vars(args))
    
    args.config['training']['n_bins'] = args.n_bins
    return args,default_para,opt_space   

def show_results_classical(args,info,metric_name,results_list,time_list):
    """
    Show the results for classical models.

    :args: argparse.Namespace, arguments
    :info: dict, information about the dataset
    :metric_name: list, names of the metrics
    :results_list: list, list of results
    :time_list: list, list of time
    """
    metric_arrays = {name: [] for name in metric_name}  


    for result in results_list:
        for idx, name in enumerate(metric_name):
            metric_arrays[name].append(result[idx])

    metric_arrays['Time'] = time_list
    metric_name = metric_name + ('Time', )

    mean_metrics = {name: np.mean(metric_arrays[name]) for name in metric_name}
    std_metrics = {name: np.std(metric_arrays[name]) for name in metric_name}
    

    # Printing results
    print(f'{args.model_type}: {args.seed_num} Trials')
    for name in metric_name:
        if info['task_type'] == 'regression' and name != 'Time':
            formatted_results = ', '.join(['{:.8e}'.format(e) for e in metric_arrays[name]])
            print(f'{name} Results: {formatted_results}')
            print(f'{name} MEAN = {mean_metrics[name]:.8e} ± {std_metrics[name]:.8e}')
        else:
            formatted_results = ', '.join(['{:.8f}'.format(e) for e in metric_arrays[name]])
            print(f'{name} Results: {formatted_results}')
            print(f'{name} MEAN = {mean_metrics[name]:.8f} ± {std_metrics[name]:.8f}')

    print('-' * 20, 'GPU info', '-' * 20)
    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
        print(f"{num_gpus} GPU Available.")
        for i in range(num_gpus):
            gpu_info = torch.cuda.get_device_properties(i)
            print(f"GPU {i}: {gpu_info.name}")
            print(f"  Total Memory:          {gpu_info.total_memory / 1024**2} MB")
            print(f"  Multi Processor Count: {gpu_info.multi_processor_count}")
            print(f"  Compute Capability:    {gpu_info.major}.{gpu_info.minor}")
    else:
        print("CUDA is unavailable.")
    print('-' * 50)



def show_results(args,info,metric_name,loss_list,results_list,time_list):
    """
    Show the results for deep learning models.

    :args: argparse.Namespace, arguments
    :info: dict, information about the dataset
    :metric_name: list, names of the metrics
    :loss_list: list, list of loss
    :results_list: list, list of results
    :time_list: list, list of time
    """
    metric_arrays = {name: [] for name in metric_name}  


    for result in results_list:
        for idx, name in enumerate(metric_name):
            metric_arrays[name].append(result[idx])

    metric_arrays['Time'] = time_list
    metric_name = metric_name + ('Time', )

    mean_metrics = {name: np.mean(metric_arrays[name]) for name in metric_name}
    std_metrics = {name: np.std(metric_arrays[name]) for name in metric_name}
    mean_loss = np.mean(np.array(loss_list))

    # Printing results
    print(f'{args.model_type}: {args.seed_num} Trials')
    for name in metric_name:
        if info['task_type'] == 'regression' and name != 'Time':
            formatted_results = ', '.join(['{:.8e}'.format(e) for e in metric_arrays[name]])
            print(f'{name} Results: {formatted_results}')
            print(f'{name} MEAN = {mean_metrics[name]:.8e} ± {std_metrics[name]:.8e}')
        else:
            formatted_results = ', '.join(['{:.8f}'.format(e) for e in metric_arrays[name]])
            print(f'{name} Results: {formatted_results}')
            print(f'{name} MEAN = {mean_metrics[name]:.8f} ± {std_metrics[name]:.8f}')

    print(f'Mean Loss: {mean_loss:.8e}')
    
    print('-' * 20, 'GPU info', '-' * 20)
    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
        print(f"{num_gpus} GPU Available.")
        for i in range(num_gpus):
            gpu_info = torch.cuda.get_device_properties(i)
            print(f"GPU {i}: {gpu_info.name}")
            print(f"  Total Memory:          {gpu_info.total_memory / 1024**2} MB")
            print(f"  Multi Processor Count: {gpu_info.multi_processor_count}")
            print(f"  Compute Capability:    {gpu_info.major}.{gpu_info.minor}")
    else:
        print("CUDA is unavailable.")
    print('-' * 50)

def tune_hyper_parameters(args,opt_space,train_val_data,info):
    """
    Tune hyper-parameters.

    :args: argparse.Namespace, arguments
    :opt_space: dict, search space
    :train_val_data: tuple, training and validation data
    :info: dict, information about the dataset
    :return: argparse.Namespace, arguments
    """
    import optuna
    import optuna.samplers
    import optuna.trial
    def objective(trial):
        config = {}
        try:
            opt_space[args.model_type]['training']['n_bins'] = [
                    "int",
                    2, 
                    256
            ]
        except:
            opt_space[args.model_type]['fit']['n_bins'] = [
                    "int",
                    2, 
                    256
            ]
        merge_sampled_parameters(
            config, sample_parameters(trial, opt_space[args.model_type], config)
        )    
        if args.model_type == 'xgboost' and torch.cuda.is_available():
            config['model']['tree_method'] = 'gpu_hist' 
            config['model']['gpu_id'] = args.gpu
            config['fit']["verbose"] = False
        elif args.model_type == 'catboost' and torch.cuda.is_available():
            config['fit']["logging_level"] = "Silent"
        
        elif args.model_type == 'RandomForest':
            config['model']['max_depth'] = 12
            
        if args.model_type in ['resnet']:
            config['model']['activation'] = 'relu'
            config['model']['normalization'] = 'batchnorm'    

        if args.model_type in ['ftt']:
            config['model'].setdefault('prenormalization', False)
            config['model'].setdefault('initialization', 'xavier')
            config['model'].setdefault('activation', 'reglu')
            config['model'].setdefault('n_heads', 8)
            config['model'].setdefault('d_token', 64)
            config['model'].setdefault('token_bias', True)
            config['model'].setdefault('kv_compression', None)
            config['model'].setdefault('kv_compression_sharing', None)    

        if args.model_type in ['excelformer']:
            config['model'].setdefault('prenormalization', False)
            config['model'].setdefault('kv_compression', None)
            config['model'].setdefault('kv_compression_sharing', None)  
            config['model'].setdefault('token_bias', True)
            config['model'].setdefault('init_scale', 0.01)
            config['model'].setdefault('n_heads', 8)

        if args.model_type in ["node"]:
            config["model"].setdefault("choice_function", "sparsemax")
            config["model"].setdefault("bin_function", "sparsemoid")

        if args.model_type in ['tabr']:
            config['model']["num_embeddings"].setdefault('type', 'PLREmbeddings')
            config['model']["num_embeddings"].setdefault('lite', True)
            config['model'].setdefault('d_multiplier', 2.0)
            config['model'].setdefault('mixer_normalization', 'auto')
            config['model'].setdefault('dropout1', 0.0)
            config['model'].setdefault('normalization', "LayerNorm")
            config['model'].setdefault('activation', "ReLU")
        
        if args.model_type in ['mlp_plr']:
            config['model']["num_embeddings"].setdefault('type', 'PLREmbeddings')
            config['model']["num_embeddings"].setdefault('lite', True)
            
        if args.model_type in ['ptarl']:
            config['model']['n_clusters'] = 20
            config['model']["regularize"]="True"
            config['general']["diversity"]="True"
            config['general']["ot_weight"]=0.25
            config['general']["diversity_weight"]=0.25
            config['general']["r_weight"]=0.25

        if args.model_type in ['modernNCA']:
            config['model']["num_embeddings"].setdefault('type', 'PLREmbeddings')
            config['model']["num_embeddings"].setdefault('lite', True)
            
        if args.model_type in ['danets']:
            config['general']['k'] = 5
            config['general']['virtual_batch_size'] = 256
        
        if args.model_type in ['dcn2']:
            config['model']['stacked'] = False

        if args.model_type in ['grownet']:
            config["ensemble_model"]["lr"] = 1.0
            config['model']["sparse"] = False
            config["training"]['lr_scaler'] = 3

        if args.model_type in ['autoint']:
            config['model'].setdefault('prenormalization', False)
            config['model'].setdefault('initialization', 'xavier')
            config['model'].setdefault('activation', 'relu')
            config['model'].setdefault('n_heads', 8)
            config['model'].setdefault('d_token', 64)
            config['model'].setdefault('kv_compression', None)
            config['model'].setdefault('kv_compression_sharing', None)

        if args.model_type in ['protogate']:
            config['training'].setdefault('lam', 1e-3)
            config['training'].setdefault('pred_coef', 1)
            config['training'].setdefault('sorting_tau', 16)
            config['training'].setdefault('feature_selection', True)
            config['model'].setdefault('a',1)
            config['model'].setdefault('sigma',0.5)
        
        if args.model_type in ['grande']:
            config['model'].setdefault('from_logits', True)
            config['model'].setdefault('use_class_weights', True)
            config['model'].setdefault('bootstrap', False)

        if args.model_type in ['amformer']:
            config['model'].setdefault('heads', 8)
            config['model'].setdefault('groups', [54,54,54,54])
            config['model'].setdefault('sum_num_per_group', [32,16,8,4])
            config['model'].setdefault("prod_num_per_group", [6,6,6,6])
            config['model'].setdefault("cluster", True)
            config['model'].setdefault("target_mode", "mix")
            config['model'].setdefault("token_descent", False)

        if config.get('config_type') == 'trv4':
            if config['model']['activation'].endswith('glu'):
                # This adjustment is needed to keep the number of parameters roughly in the
                # same range as for non-glu activations
                config['model']['d_ffn_factor'] *= 2 / 3

        trial_configs.append(config)
        # method.fit(train_val_data, info, train=True, config=config)  
        # run with this config
        try:
            method.fit(train_val_data, info, train=True, config=config)    
            return method.trlog['best_res']
        except Exception as e:
            print(e)
            return 1e9 if info['task_type'] == 'regression' else 0.0
    
    if osp.exists(osp.join(args.save_path, '{}-tuned.json'.format(args.model_type))) and args.retune == False:
        with open(osp.join(args.save_path, '{}-tuned.json'.format(args.model_type)), 'rb') as fp:
            args.config = json.load(fp)
    else:
        # get data property
        if info['task_type'] == 'regression':
            direction = 'minimize'
            for key in opt_space[args.model_type]['model'].keys():
                if 'dropout' in key and '?' not in opt_space[args.model_type]['model'][key][0]:
                    opt_space[args.model_type]['model'][key][0] = '?'+ opt_space[args.model_type]['model'][key][0]
                    opt_space[args.model_type]['model'][key].insert(1, 0.0)
        else:
            direction = 'maximize'  
        
        method = get_method(args.model_type)(args, info['task_type'] == 'regression')      

        trial_configs = []
        study = optuna.create_study(
                direction=direction,
                sampler=optuna.samplers.TPESampler(seed=0),
            )        
        study.optimize(
            objective,
            **{'n_trials': args.n_trials},
            show_progress_bar=True,
        ) 
        # get best configs
        best_trial_id = study.best_trial.number
        # update config files        
        print('Best Hyper-Parameters')
        print(trial_configs[best_trial_id])
        args.config = trial_configs[best_trial_id]
        with open(osp.join(args.save_path, '{}-tuned.json'.format(args.model_type)), 'w') as fp:
            json.dump(args.config, fp, sort_keys=True, indent=4)
    return args

def get_method(model):
    """
    Get the method class.

    :model: str, model name
    :return: class, method class
    """
    if model == 'RandomForest_save':
        from model.randomforest_save import RandomForestMethod
        return RandomForestMethod
    elif model == 'DeLTa':
        from model.DeLTa import DeLTa
        return DeLTa
    elif model == 'DeLTa1':
        from model.DeLTa1 import DeLTa
        return DeLTa
    else:
        raise NotImplementedError("Model \"" + model + "\" not yet implemented")
