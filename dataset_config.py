"""Dataset configuration parameters for model training"""

# Dataset-specific parameters
dataset_params = {
    'adult': {
        'mds': [20],
        'mls': [50],
        'n_estimators': [15],
        'small_model': 'cart', 
        'eta':0.12,
        'num_class': 2  # Binary classification
    },
    'bank': {
        'mds': [20],
        'mls': [50],
        'n_estimators': [15],
        'small_model': 'cart', 
        'eta':0.2,
        'num_class': 2  # Binary classification
    },
    'car': {
        'mds': [10],
        'mls': [10],
        'n_estimators': [20],
        'small_model': 'cart', 
        'eta':0.044,  
        'num_class': 4  
    },
    'blood': {
        'mds': [10],
        'mls': [10],
        'n_estimators': [3],
        'small_model': 'cart', 
        'eta':0.04, 
        'num_class': 2  
    },
   
    'credit-g': {
        'mds': [15],
        'mls': [20],
        'n_estimators': [20],
        'small_model': 'cart',  
        'eta':0.1,
        'num_class': 2  
    },
    'jannis': {
        'mds': [20],
        'mls': [50],
        'n_estimators': [20],
        'small_model': 'cart', 
        'eta':0.18, 
        'num_class': 4  
    },
    'cpu_act': {
        'mds': [10],
        'mls': [200],
        'n_estimators': [3],
        'small_model': 'tabpfn',  
        'num_class': 1  # Regression
    },
    'house_16H_reg': {
        'mds': [10],
        'mls': [200],
        'n_estimators': [5],
        'small_model': 'tabpfn',  
        'num_class': 1  # Regression
    },
    'credit_reg': {
        'mds': [10],
        'mls': [200],
        'n_estimators': [3],
        'small_model': 'tabpfn',  
        'num_class': 1  # Regression
    },
    'fried': {
        'mds': [10],
        'mls': [200],
        'n_estimators': [5],
        'small_model': 'tabpfn',  
        'num_class': 1  # Regression
    },
    'Diamonds': {
        'mds': [10],
        'mls': [200],
        'n_estimators': [3],
        'small_model': 'tabpfn',  
        'num_class': 1  # Regression
    },
    'california_housing': {
        'mds': [10],
        'mls': [200],
        'n_estimators': [5],
        'small_model': 'tabpfn',  
        'num_class': 1  # Regression
    },
    
}

# Default parameters for datasets not explicitly defined
default_params = {
    'mds': [20],
    'mls': [50],
    'n_estimators': [20],
    'small_model': 'cart',  
    'num_class': 2  
}
    
