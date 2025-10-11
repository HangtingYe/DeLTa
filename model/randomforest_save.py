from model.base import classical_methods
from copy import deepcopy
import os.path as ops
import pickle
import time
import pandas as pd
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.tree import export_text
import numpy as np
import ipdb
class RandomForestMethod(classical_methods):
    def __init__(self, args, is_regression):
        super().__init__(args, is_regression)
        assert(args.cat_policy != 'indices')
        self.selected = None
        self.selected_y = None

    def construct_model(self, model_config = None):
        if model_config is None:
            model_config = self.args.config['model']
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        print('self.is_regression:',self.is_regression)
        if self.is_regression:#todo：
            self.model = RandomForestRegressor(random_state=self.args.seed, n_estimators=self.args.n_estimators,max_depth=self.args.max_depth, max_leaf_nodes=self.args.max_leaf_nodes)  #
        else:
            self.model = RandomForestClassifier(random_state=self.args.seed, n_estimators=self.args.n_estimators,max_depth=self.args.max_depth, max_leaf_nodes=self.args.max_leaf_nodes)


    def fit(self, data, info, train=True, config=None):
        super().fit(data, info, train, config)
        # if not train, skip the training process. such as load the checkpoint and directly predict the results
        if not train:
            return
        tic = time.time()

        #todo:1.  few shot data for cls
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
            print('X_sampled:',X_sampled.shape,X_sampled)
            print('y_sampled:',y_sampled.shape,y_sampled)
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
            print('X_sampled:',X_sampled.shape,X_sampled)
            print('y_sampled:',y_sampled.shape,y_sampled)
            self.selected = X_sampled
            self.selected_y = y_sampled
            self.model.fit(X_sampled, y_sampled)

        # todo:3. full data
        elif self.args.task_type == 'full':
            self.selected = self.N['train']
            self.selected_y = self.y['train']
            self.model.fit(self.N['train'], self.y['train'])
       
        print('self.model:',self.model)

        # print tree rules
        for i, tree in enumerate(self.model.estimators_):
            print(f"Tree {i} rules:")
            tree_rules = export_text(tree)
            print(tree_rules)
            print("-" * 80) 
        print('finished print tree')



        if not self.is_regression:
            y_val_pred = self.model.predict(self.N['val'])
            self.trlog['best_res'] = accuracy_score(self.y['val'], y_val_pred)
        else:
            y_val_pred = self.model.predict(self.N['val'])
            self.trlog['best_res'] = mean_squared_error(self.y['val'], y_val_pred, squared=False)*self.y_info['std']
        time_cost = time.time() - tic
        print('train time:',time_cost)
        with open(ops.join(self.args.save_path , 'best-val-{}.pkl'.format(self.args.seed)), 'wb') as f:
            pickle.dump(self.model, f)
        return time_cost

    def predict(self, data, info, model_name):
        test_start = time.time()
        N, C, y = data
        with open(ops.join(self.args.save_path , 'best-val-{}.pkl'.format(self.args.seed)), 'rb') as f:
            self.model = pickle.load(f)
        self.data_format(False, N, C, y)
        test_label = self.y_test
                
        
        if self.is_regression:
            test_logit = self.model.predict(self.N_test)
            train_logit = self.model.predict(self.selected)
        else:
            test_logit = self.model.predict_proba(self.N_test)
            train_logit = self.model.predict_proba(self.selected)
        test_ed = time.time()
        test_cost = test_ed - test_start
        print('test_logit:',test_logit.shape,test_logit.dtype,test_logit[0:5])
        print()
        data_dict = {
                'logit': test_logit,
                'label': test_label
            }
        np.save(self.args.save_npy , data_dict)
        print(f'test_logit save to {self.args.save_npy}')

        print()
        train_data_dict = {
                'logit': train_logit,
                'label': self.selected_y
            }
        np.save(self.args.save_npy + '_train', train_data_dict)
        print(f'train_logit save to {self.args.save_npy + "_train"}')
      
        if self.is_regression:
            print( self.y_info['policy'])
            print(self.y_info['std'])
        vres, metric_name = self.metric(test_logit, test_label, self.y_info)

        test_train  = np.vstack([self.N_test, self.selected])
        print(self.N_test.shape)
        print(test_train.shape)
        return vres, metric_name, test_logit

