from model.base import classical_methods
from copy import deepcopy
import os.path as ops
import pickle
from model.lib.data import (
    Dataset,
)
from model.utils import (
    get_device,replace_subtree,find_sibling_leaf,build_leaf_index_dict,find_valid_parent_knn,calculate_leaf_grad,assign_leaf,predict_group
)
import copy
import os,json
from tabpfn import TabPFNClassifier,TabPFNRegressor
import multiprocessing
from multiprocessing import Pool
from collections import defaultdict
import pandas as pd
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
import numpy as np
import time
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np

import importlib
import numpy as np
import random
import pickle
import sklearn
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
import copy


class DeLTa(classical_methods):
    """
    DeLTa class for decision tree-based regression/classification with leaf-level gradient fitting
    Inherits from classical_methods, supports few-shot/full data training and leaf-wise model refinement
    """
    def __init__(self, args, is_regression):
        self.args = args
        print(args.config)
        self.is_regression = is_regression
        self.D = None
        self.args.device = get_device()
        self.trlog = {}
        self.leaf_grad_dict = {}
        self.model_leaf = {}
        self.model_list = {}
        self.one_model_list={}
        self.n_class = None
        self.train_logit =None
        self.leaf_index_dict2={}
        assert(args.cat_policy == 'ordinal')

    def fit(self, data, info, train=True, config=None):
        """
        Train decision tree model with few-shot/full data sampling (classification/regression)
        Saves regression info (mean/std) to JSON file and records validation metrics
        
        Args:
            data: Tuple of (N, C, y) containing numerical/categorical features and labels
            info: Dataset metadata
            train: Whether to perform model training (False = skip training)
            config: Optional model configuration override
        Returns:
            time_cost: Training time in seconds
        """
        N, C, y = data
        self.D = Dataset(N, C, y, info)
        self.N, self.C, self.y = self.D.N, self.D.C, self.D.y
        self.is_binclass, self.is_multiclass, self.is_regression = self.D.is_binclass, self.D.is_multiclass, self.D.is_regression
        self.n_num_features, self.n_cat_features = self.D.n_num_features, self.D.n_cat_features

        
        model_config = None
        if config is not None:
            self.reset_stats_withconfig(config)
            model_config = config['model']
        
        if model_config is None:
            model_config = self.args.config['model']
        self.data_format(is_train = True)

        # Save regression metadata (mean/std) to JSON if not exists
        save_dir = "reg_info"
        save_path = os.path.join(save_dir, f"{self.args.dataset}.json")
        if not os.path.exists(save_path):
            os.makedirs(save_dir, exist_ok=True)        
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(self.y_info, f, indent=4)  
            print(f"y_info saved to {save_path}") 
    
        X_train = self.N['train']
        X_val =self.N['val']

        if not train:
            return
        fit_config = deepcopy(self.args.config['fit'])
        fit_config.pop('n_bins')
        fit_config['eval_set'] = (X_val, self.y['val'])
        tic = time.time()
        self.n_class = len(np.unique(self.y['train']))
 
        # Classification task: stratified few-shot sampling
        if self.args.task_type == 'cls':
    
            X_train = self.N['train']  
            y_train = self.y['train']  
            
            def stratified_sample(X, y, num_shot, seed):
                """Stratified sampling for few-shot classification (preserves class distribution)"""
                saved_random_state = np.random.get_state()
                np.random.seed(seed)
                selected_indices = []
                
                unique_labels = np.unique(y)
                num_classes = len(unique_labels)
                
                base_shot = num_shot // num_classes
                last_shot = num_shot - (base_shot * (num_classes - 1))
                shots_per_class = [base_shot] * (num_classes - 1) + [last_shot]
                
                for label, class_shot in zip(unique_labels, shots_per_class):
                    class_indices = np.where(y == label)[0]
                    replace = True
                    selected = np.random.choice(class_indices, size=class_shot, replace=replace)
                    selected_indices.extend(selected.tolist())
                
                
                print('selected_indices:',selected_indices)
                np.random.set_state(saved_random_state)
                return X[selected_indices], y[selected_indices]
            
            # Perform stratified sampling for few-shot training
            X_sampled, y_sampled = stratified_sample(
                X_train, 
                y_train,
                num_shot=self.args.shot,
                seed=self.args.few_shot_random_seed  
            )
            self.selected = X_sampled
            self.selected_y = y_sampled

        # Regression task: random few-shot sampling
        elif self.args.task_type == 'reg':
            def regression_sample(X, y, num_shot, seed):
                """Random sampling for few-shot regression"""
                saved_random_state = np.random.get_state()
                np.random.seed(seed)
                all_indices = np.arange(len(y))
                selected_indices = np.random.choice(all_indices, size=num_shot, replace=True)

                np.random.set_state(saved_random_state)
                print('regression_sample selected_indices:', selected_indices)
                return X[selected_indices], y[selected_indices]
            # Perform random sampling for few-shot regression
            X_sampled, y_sampled = regression_sample(self.N['train'], self.y['train'], num_shot=self.args.shot, seed=self.args.few_shot_random_seed)
            self.selected = X_sampled
            self.selected_y = y_sampled
        # Full data training (no sampling)
        elif self.args.task_type == 'full':
            self.selected = X_train
            self.selected_y = self.y['train']

        

        #fit
        import importlib
        print('*'*20)
        try:
            # Import decision tree rule function from specified module
            module_name, function_name = self.args.classify_rule.rsplit('.', 1)
            module = importlib.import_module(module_name)
            tree = getattr(module, function_name)
            print('tree:', function_name)
        except (ImportError, AttributeError) as e:
            print(f"Error importing classify_rule function: {e}")

        self.tree = tree
        print('tree:',tree)
        print('*'*20)

        # Map training samples to leaf nodes using decision tree rules
        self.leaf_index_dict = build_leaf_index_dict(self.tree, self.selected)
    
        # Extract md/ml/tree parameters from save path
        pattern = r'md(\d+)_ml(\d+)_tree(\d+)'
        import re
        data_names_x = self.args.dataset
        match = re.search(pattern, self.args.save_npy)
        if match:
            md = int(match.group(1))
            ml = int(match.group(2))
            tree = int(match.group(3))
        else:
            print("no matching...")
        # Load pre-trained RF train logits (full/few-shot)
        if self.args.task_type == 'full':
            file = f'results/{data_names_x}/{data_names_x}_md{md}_ml{ml}_tree{tree}_train.npy'
        else:
            file = f'results/{data_names_x}/RF_tree/seed{self.args.few_shot_random_seed}/RFshot{self.args.shot}_seed{self.args.few_shot_random_seed}_md{md}_ml{ml}_tree{tree}_train.npy'
        train_data = np.load(file, allow_pickle=True).item()
        train_data = np.load(file, allow_pickle=True).item()
        print('read RF train_logit',file)
        print('*'*20)

        train_y = train_data['label']
        assert np.array_equal(train_y,self.selected_y) ##
        self.train_logit = train_data['logit']

        self.if_parallel = True
        self.if_direct = False
        # Train leaf-level gradient models
        self.model_leaf = calculate_leaf_grad(self.args, self.model_leaf, self.leaf_index_dict,self.is_regression, self.selected, self.selected_y, self.train_logit, self.one_model_list, self.n_class)
        time_cost = time.time() - tic
        return time_cost


    
    def predict(self, data, info, model_name):
        """
        Predict on test data with leaf-level models, handle missing leaf IDs (sibling/parent fallback)
        Loads pre-trained RF logits, calculates leaf gradients, and saves test predictions to NPY
        
        Args:
            data: Tuple of (N, C, y) test data
            info: Dataset metadata
            model_name: Name of model for logging
        Returns:
            vres: Calculated metrics
            metric_name: Names of metrics
            test_logit: Test predictions (logits)
        """

        # Test inference function (group samples by leaf ID)
        
        # Prepare test data and run prediction
        N, C, y = data
        self.data_format(False, N, C, y)
        test_data = self.N_test
        test_label = self.y_test
        print('*'*20)
        print('TEST')
        test_logit = predict_group(
            X=test_data,  
            leaf_index_dict=self.leaf_index_dict,  
            tree=self.tree,  
            model_leaf=self.model_leaf,  
            one_model_list=self.one_model_list, 
            selected=self.selected,  
            selected_y=self.selected_y,
            args=self.args,  
            train_logit=self.train_logit, 
            n_class=self.n_class,  
            is_regression=self.is_regression  
        )
        # Save test predictions (logits + labels) to NPY file
        parts = self.args.classify_rule.split('.')
        name = parts[-2] + '.' + parts[-1]
        data_dict = {
            'logit': test_logit,
            'label': test_label
        }
        np.save(self.args.save_npy, data_dict)
        print('test_logit saved! ',self.args.save_npy)
        # Calculate evaluation metrics
        #vres, metric_name = self.metric(test_logit, test_label, self.y_info)
        return 
