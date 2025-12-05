from model.base import classical_methods
from copy import deepcopy
import os.path as ops
import pickle
from model.lib.data import (
    Dataset,
)
from model.utils import (
    get_device
)
from sklearn.neural_network import MLPRegressor,MLPClassifier 
import copy
import os,json
from sklearn.linear_model import LogisticRegression
from tabpfn import TabPFNClassifier,TabPFNRegressor
import multiprocessing
from multiprocessing import Pool
from collections import defaultdict
import ipdb
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
import numpy as np
import time
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np

class DeLTa(classical_methods):
    def __init__(self, args, is_regression):
        self.args = args
        print(args.config)
        self.is_regression = is_regression
        self.D = None
        self.args.device = get_device()
        self.trlog = {}
        self.leaf_grad_dict = {}#
        self.model_leaf = {}#
        self.model_list = {}#
        self.one_model_list={}#
        self.n_class = None
        self.train_logit =None
        self.leaf_index_dict2={}
        assert(args.cat_policy == 'ordinal')

    def fit(self, data, info, train=True, config=None):
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

        save_dir = "reg_info"
        save_path = os.path.join(save_dir, f"{self.args.dataset}.json")
        if not os.path.exists(save_path):
            os.makedirs(save_dir, exist_ok=True)        
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(self.y_info, f, indent=4)  
            print(f"y_info saved to {save_path}") 
    
        X_train = self.N['train']
        X_val =self.N['val']
        self.model = DecisionTreeRegressor(max_depth=3, max_leaf_nodes=10) if self.is_regression else DecisionTreeClassifier(max_depth=3, max_leaf_nodes=10)
        if not train:
            return
        fit_config = deepcopy(self.args.config['fit'])
        fit_config.pop('n_bins')
        fit_config['eval_set'] = (X_val, self.y['val'])
        tic = time.time()
        self.n_class = len(np.unique(self.y['train']))
 
        if self.args.task_type == 'cls':
    
            X_train = self.N['train']  
            y_train = self.y['train']  
            
            def stratified_sample(X, y, num_shot, seed):
                
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
            
            X_sampled, y_sampled = stratified_sample(
                X_train, 
                y_train,
                num_shot=self.args.shot,
                seed=self.args.few_shot_random_seed  
            )
            self.selected = X_sampled
            self.selected_y = y_sampled
            self.model.fit(X_sampled, y_sampled)

        # todo:2.  low regime for reg
        elif self.args.task_type == 'reg':
            def regression_sample(X, y, num_shot, seed):
                saved_random_state = np.random.get_state()
                np.random.seed(seed)
                all_indices = np.arange(len(y))
                selected_indices = np.random.choice(all_indices, size=num_shot, replace=True)

                np.random.set_state(saved_random_state)
                print('regression_sample selected_indices:', selected_indices)
                return X[selected_indices], y[selected_indices]
            X_sampled, y_sampled = regression_sample(self.N['train'], self.y['train'], num_shot=self.args.shot, seed=self.args.few_shot_random_seed)
            self.selected = X_sampled
            self.selected_y = y_sampled
            self.model.fit(X_sampled, y_sampled)
        # full data
        elif self.args.task_type == 'full':
            self.selected = X_train
            self.selected_y = self.y['train']
            self.model.fit(X_train, self.y['train'])


        if not self.is_regression:
            y_pred_val = self.model.predict(X_val)
            self.trlog['best_res'] = accuracy_score(self.y['val'], y_pred_val) 
        else:
            y_pred_val = self.model.predict(X_val)
            self.trlog['best_res'] = mean_squared_error(self.y['val'], y_pred_val, squared=False)*self.y_info['std']
        time_cost = time.time() - tic
        
        return time_cost

    def assign_leaf(self, tree, sample):
        if "id" in tree:                
            return tree["id"]
        
        feature = tree["feature"]
        threshold = tree["threshold"]
        operator = tree["operator"]
        
        if operator == "<=":
            if sample[feature] <= threshold:
                return self.assign_leaf(tree["left"], sample)
            else:
                return self.assign_leaf(tree["right"], sample)
        elif operator == ">":
            if sample[feature] > threshold:
                return self.assign_leaf(tree["right"], sample)
            else:
                return self.assign_leaf(tree["left"], sample)
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def build_leaf_index_dict(self, tree, train_data):
        leaf_index_dict = defaultdict(list)
        
        for idx, sample in enumerate(train_data):
            leaf_id = self.assign_leaf(tree, sample.astype(float)) 
            leaf_index_dict[leaf_id].append(idx)        
        return dict(leaf_index_dict)

    def calculate_leaf_grad(self):
        print('fitting negative gradient')
        leaf_grad_dict = {}
        if not self.is_regression:
            num_classes = len(np.unique(self.y['train']))
            for leaf_id, indices in self.leaf_index_dict.items():
                if leaf_id in self.model_leaf.keys():
                    continue
                # true labels
                leaf_targets = self.selected_y[indices]  # y
                one_hot_encoding = np.zeros((leaf_targets.shape[0], num_classes), dtype=float)
                one_hot_encoding[np.arange(leaf_targets.shape[0]), leaf_targets] = 1
                
                # construct negative gradient labels
                logit = self.train_logit[indices]
                if (leaf_id in self.one_model_list ):  # mlp output has 2 columns
                    print(leaf_id, 'in', 'one_model_list')
                    cla = self.one_model_list[leaf_id]  # array([1])
                    a_ = np.zeros((logit.shape[0], self.n_class), dtype=float)
                    np.put_along_axis(a_, cla.reshape(1, -1), logit, axis=1)
                    logit = a_
                
                def check_softmax(logits):
                    if np.any((logits < 0) | (logits > 1)) or (not np.allclose(logits.sum(axis=-1), 1, atol=1e-5)):
                        exps = np.exp(logits - np.max(logits, axis=1, keepdims=True))
                        return exps / np.sum(exps, axis=1, keepdims=True)
                    else:
                        return logits
                
                softmax_result = check_softmax(logit)
                leaf_targets2 = one_hot_encoding - softmax_result
                set_ = self.selected[indices].astype(float)
                y_ = leaf_targets2

                # train regression model
                if self.args.small_model == 'cart':
                    model = DecisionTreeRegressor(max_depth=5, max_leaf_nodes=20, random_state=42)
                elif self.args.small_model == 'tabpfn':  # 
                    if set_.shape[0] > 1 and leaf_id not in self.one_model_list.keys():
                        model = TabPFNRegressor(device='cuda', ignore_pretraining_limits=True, random_state=self.args.seed) 
                    else:
                        model = DecisionTreeRegressor(max_depth=5, max_leaf_nodes=20, random_state=42)
                from sklearn.multioutput import MultiOutputRegressor

                if set_.shape[0] > 5000:
                    selected_rows = np.random.choice(set_.shape[0], 5000, replace=False) 
                    set_, y_ = set_[selected_rows], y_[selected_rows]

                model = MultiOutputRegressor(model)
                model.fit(set_, y_)
                self.model_leaf[leaf_id] = model
        else:
            leaf_grad_dict = {}
            rf = 0.001
            for leaf_id, indices in self.leaf_index_dict.items():
                if leaf_id in self.model_leaf.keys():
                    continue
                print('leaf_id :', leaf_id)
                # true labels
                leaf_label = self.selected_y[indices]  

                # construct negative gradient labels
                logit = self.train_logit[indices]
                leaf_targets2 = leaf_label - rf * logit  # regression negative gradient
                set_ = self.selected[indices].astype(float)
                y_ = leaf_targets2

                # train regression model
                if self.args.small_model == 'cart':
                    model = DecisionTreeRegressor(max_depth=5, max_leaf_nodes=20, random_state=42)
                elif self.args.small_model == 'tabpfn':  
                    if len(set_) == 1 or np.unique(y_).shape[0] == 1:
                        model = DecisionTreeRegressor(max_depth=5, max_leaf_nodes=20, random_state=42)
                    else:
                        model = TabPFNRegressor(device='cuda', ignore_pretraining_limits=True, random_state=self.args.seed)

                if set_.shape[0] > 5000:
                    selected_rows = np.random.choice(set_.shape[0], 5000, replace=False)
                    set_, y_ = set_[selected_rows], y_[selected_rows]

                model.fit(set_, y_)
                self.model_leaf[leaf_id] = model

        return leaf_grad_dict

    def find_parent_node(self, tree, leaf_id):
        """
        Find the parent node of a given leaf node.
        """
        if "id" in tree:
            return None  

        if "left" in tree:
            if "id" in tree["left"] and tree["left"]["id"] == leaf_id:
                return tree
            parent_left = self.find_parent_node(tree["left"], leaf_id)
            if parent_left:
                return parent_left

        if "right" in tree:
            if "id" in tree["right"] and tree["right"]["id"] == leaf_id:
                return tree
            parent_right = self.find_parent_node(tree["right"], leaf_id)
            if parent_right:
                return parent_right

        return None

    def find_sibling_leaf(self, tree, leaf_id):
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
        left_result = self.find_sibling_leaf(tree["left"], leaf_id)
        if left_result is not None:
            return left_result
        right_result = self.find_sibling_leaf(tree["right"], leaf_id)
        if right_result is not None:
            return right_result

        return None


    def replace_subtree(self, tree, subtree, new_subtree):
        if 'id' in tree:
            return tree
        if tree == subtree:
            return new_subtree
        if 'left' in tree:
            tree['left'] = self.replace_subtree(tree['left'], subtree, new_subtree)
        if 'right' in tree:
            tree['right'] = self.replace_subtree(tree['right'], subtree, new_subtree)
        return tree
    def find_valid_parent(self, tree, leaf_id, real_leaf_id):
        parent_leaf = self.find_parent_node(tree, leaf_id)  # Find parent node
        new_tree = {"id": "leaf_x"}
        replace_subtree = self.replace_subtree(tree, parent_leaf, new_tree)
        parent_leaf_index_dict = self.build_leaf_index_dict(replace_subtree, self.selected)
        
        if "leaf_x" in parent_leaf_index_dict:
            self.leaf_index_dict[real_leaf_id] = parent_leaf_index_dict["leaf_x"]
            return parent_leaf_index_dict["leaf_x"]
        else:
            leaf_id = 'leaf_x'
            return self.find_valid_parent(replace_subtree, leaf_id, real_leaf_id)

    def find_valid_parent_knn(self, tree, leaf_id, real_leaf_id):
        parent_leaf = self.find_parent_node(tree, leaf_id)  
        new_tree = {"id": "leaf_x"}
        replace_subtree = self.replace_subtree(tree, parent_leaf, new_tree)
        parent_leaf_index_dict = self.build_leaf_index_dict(replace_subtree, self.selected)

        if "leaf_x" in parent_leaf_index_dict:
            self.leaf_index_dict[real_leaf_id] = parent_leaf_index_dict["leaf_x"]
            #print(f'self.leaf_index_dict after  {real_leaf_id}:', self.leaf_index_dict.keys())
            return self.selected[self.leaf_index_dict[real_leaf_id]], self.selected_y[self.leaf_index_dict[real_leaf_id]]
        else:
            leaf_id = 'leaf_x'
            return self.find_valid_parent_knn(replace_subtree, leaf_id, real_leaf_id)
    
    def predict(self, data, info, model_name):
        import importlib
        print('*'*20)
        try:

            module_name, function_name = self.args.classify_rule.rsplit('.', 1)
            module = importlib.import_module(module_name)
            tree = getattr(module, function_name)
            print('tree:', function_name)
            # print(classify_rule)
        except (ImportError, AttributeError) as e:
            print(f"Error importing classify_rule function: {e}")

        self.tree = tree
        print('tree:',tree)
        print('*'*20)

        # construct train set leaf nodes
        self.leaf_index_dict = self.build_leaf_index_dict(self.tree, self.selected)
        #print('selected:', len(self.selected))

    
        # print(self.args.save_npy)
        pattern = r'md(\d+)_ml(\d+)_tree(\d+)'
        import re
        data_names_x = self.args.dataset
        match = re.search(pattern, self.args.save_npy)
        if match:
            md = int(match.group(1))
            ml = int(match.group(2))
            tree = int(match.group(3))
            #print(f"md: {md}, ml: {ml}, tree: {tree}")
        else:
            print("no matching...")
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
        self.leaf_grad_dict = self.calculate_leaf_grad() 

        # test inference

        def predict_group(X):
            leaf_groups = defaultdict(list)
            for idx, sample in enumerate(X):
                leaf_id = self.assign_leaf(self.tree, sample.astype(float))
                if leaf_id in self.leaf_index_dict.keys():
                    a = np.array([idx, sample], dtype=object)
                    leaf_groups[leaf_id].append(a)
                else:
                    print('leaf_index_dict missing leaf_id:', leaf_id)
                    sibling_leaf_id = self.find_sibling_leaf(self.tree, leaf_id)
                    if sibling_leaf_id in self.leaf_index_dict:
                        print(f"{leaf_id} replaced by {sibling_leaf_id}")
                        self.leaf_index_dict[leaf_id] = self.leaf_index_dict[sibling_leaf_id]
                        self.model_leaf[leaf_id] = self.model_leaf[sibling_leaf_id]
                        if sibling_leaf_id in self.one_model_list:
                            self.one_model_list[leaf_id] = self.one_model_list[sibling_leaf_id]
                        leaf_groups[leaf_id].append(np.array([idx, sample], dtype=object))
                    else:
                        print("No sibling, finding parent")
                        leaf_node_samples, leaf_node_labels = self.find_valid_parent_knn(copy.deepcopy(self.tree), leaf_id, leaf_id)
                        self.leaf_grad_dict = self.calculate_leaf_grad()
                        leaf_groups[leaf_id].append(np.array([idx, sample], dtype=object))
            
            ID = np.array([])
            PRED = np.array([])
            for leaf_id, samples in leaf_groups.items():
                indices = [sample[0] for sample in samples]
                self.leaf_index_dict2[leaf_id] = indices
            
            for leaf_id in leaf_groups.keys():
                model = self.model_leaf[leaf_id]
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
                    if not self.is_regression:
                        PRED = np.vstack((PRED, pred))
                    else:
                        PRED = np.concatenate((PRED, pred))
            
            sorted_indices = np.argsort(ID, axis=0)
            id_sorted = ID[sorted_indices]
            pred_sorted = PRED[sorted_indices[:, 0]]
            
            return pred_sorted

        N, C, y = data
        self.data_format(False, N, C, y)
        test_data = self.N_test
        test_label = self.y_test
        print('*'*20)
        print('TEST')
        test_logit = predict_group(test_data)

        parts = self.args.classify_rule.split('.')
        name = parts[-2] + '.' + parts[-1]
        data_dict = {
            'logit': test_logit,
            'label': test_label
        }
        np.save(self.args.save_npy, data_dict)
        print('test_logit saved! ',self.args.save_npy)
        vres, metric_name = self.metric(test_logit, test_label, self.y_info)
        return vres, metric_name, test_logit
   
