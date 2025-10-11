
tree_full_md10_ml10_9 = {
    "feature": 0,  # Based on the presence of feature_0 in each tree rule
    "threshold": 0.14,
    "operator": "<=",
    "left": {  # When feature_0 <= 0.14
        "feature": 1,  # Focusing on feature_1 as critical discriminator in rules.
        "threshold": 1.0,
        "operator": "<=",
        "left": {  # When feature_1 <= 1.0
            "feature": 3,  # Considering additional interactions with feature_3
            "threshold": 0.5,
            "operator": "<=",
            "left": {"id": "leaf_1"},  # Similar to original left class 1 regions
            "right": {"id": "leaf_2"},  # Original class 0 locations
        },
        "right": {  # When feature_1 > 1.0
            "id": "leaf_3"
        }
    },
    "right": {  # When feature_0 > 0.14
        "feature": 2,  # Use feature_2 to help discriminate further
        "threshold": 0.5,
        "operator": "<=",
        "left": {"id": "leaf_4"},  # Maintain division in line with leaf node class 0
        "right": {"id": "leaf_5"}  # Original class 1 distinction
    }
}



tree_full_md10_ml10_2 = {
    "feature": 0,  # Recency
    "threshold": 0.20,
    "operator": "<=",
    "left": {  # sub-tree for feature_0 (Recency) <= 0.20
        "feature": 1,  # Frequency
        "threshold": 0.80,
        "operator": "<=",
        "left": {
            "feature": 2,  # Monetary
            "threshold": 0.30,
            "operator": "<=",
            "left": {"id": "leaf_1"},  # Represents a region in feature space
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 3,  # Time
            "threshold": 0.60,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {  # sub-tree for feature_0 (Recency) > 0.20
        "feature": 3,  # Time
        "threshold": 0.50,
        "operator": "<=",
        "left": {
            "feature": 1,  # Frequency
            "threshold": -0.50,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
        "right": {"id": "leaf_7"}  
    },
}



tree_full_md10_ml10_5 = {
    "feature": 0,  # Assuming 'feature_0' here which relates to 'Recency'
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 1,  # Assuming 'feature_1' here which relates to 'Frequency'
        "threshold": 4.9,
        "operator": "<=",
        "left": {
            "feature": 2,  # Assuming 'feature_2' here which relates to 'Monetary'
            "threshold": 0.26,
            "operator": "<=",
            "left": {"id": "leaf_1"}, 
            "right": {
                "feature": 3,  # Assuming 'feature_3' here which relates to 'Time'
                "threshold": 1.08,
                "operator": "<=",
                "left": {"id": "leaf_2"}, 
                "right": {"id": "leaf_3"},
            },
        },
        "right": {
            "feature": 3,  # Using 'feature_3' (Time) again to segregate another pattern
            "threshold": 0.75,
            "operator": "<=",
            "left": {"id": "leaf_4"},
            "right": {"id": "leaf_5"},
        },
    },
    "right": {
        "feature": 2,  # Assumes 'feature_2' (Monetary) is critical on the other branch as well
        "threshold": -0.6,
        "operator": "<=",
        "left": {"id": "leaf_6"},
        "right": {"id": "leaf_7"},
    },
}



tree_full_md10_ml10_3 = {
    "feature": 0,  # Recency
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 2,  # Monetary
        "threshold": -0.60,
        "operator": "<=",
        "left": {"id": "leaf_1"},  # direct decision based on CART analysis
        "right": {
            "feature": 1,  # Frequency
            "threshold": 0.86,
            "operator": "<=",
            "left": {
                "feature": 3,  # Time
                "threshold": 0.58,
                "operator": "<=",
                "left": {"id": "leaf_2"},  # merged favorable decision points
                "right": {"id": "leaf_1"},  # preference towards majority decision in CART
            },
            "right": {
                "feature": 1,  # Frequency
                "threshold": 4.90,
                "operator": "<=",
                "left": {
                    "feature": 2,  # Monetary
                    "threshold": 1.90,
                    "operator": "<=",
                    "left": {"id": "leaf_3"},  # distinguishing between close groupings
                    "right": {"id": "leaf_2"},  # upper-bound driven decisions
                },
                "right": {"id": "leaf_2"},  # high specificity decisions
            },
        },
    },
    "right": {
        "feature": 0,  # Recency
        "threshold": 0.04,
        "operator": "<=",
        "left": {
            "feature": 3,  # Time
            "threshold": -1.03,
            "operator": "<=",
            "left": {"id": "leaf_4"},  # unique distinctions at other extreme
            "right": {
                "feature": 3,  # Time
                "threshold": 0.75,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_4"},
            },
        },
        "right": {"id": "leaf_1"},  # Default fallback
    },
}



tree_full_md10_ml10_4 = {
    "feature": 0,  # Recency
    "threshold": 0.10,
    "operator": "<=",
    "left": {
        "feature": 1,  # Frequency
        "threshold": 0.50,
        "operator": "<=",
        "left": {
            "feature": 3,  # Time
            "threshold": 0.00,
            "operator": "<=",
            "left": {"id": "leaf_1"},  # A region primarily for class 0
            "right": {"id": "leaf_2"},  # A region where class distinction is needed from below
        },
        "right": {
            "feature": 2,  # Monetary
            "threshold": 1.00,
            "operator": "<=",
            "left": {"id": "leaf_3"},  # A region primarily for class 1
            "right": {"id": "leaf_4"},  # Another region for class 1
        }
    },
    "right": {"id": "leaf_5"}  # Region where Recency is greater
}



tree_full_md10_ml10_6 = {
    "feature": 0,  # Recency
    "threshold": 0.1,  # A refined threshold choice
    "operator": "<=",
    "left": {
        "feature": 1,  # Frequency
        "threshold": 0.5,
        "operator": "<=",
        "left": {
            "feature": 2,  # Monetary
            "threshold": 0.0,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 3,  # Time
            "threshold": 0.6,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 2,  # Monetary
        "threshold": 1.0,
        "operator": "<=",
        "left": {
            "feature": 3,  # Time
            "threshold": 0.2,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
        "right": {"id": "leaf_7"},
    },
}



tree_full_md10_ml10_7 = {
    "feature": 0,  # Recency
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 1,  # Frequency
        "threshold": 0.86,
        "operator": "<=",
        "left": {
            "feature": 2,  # Monetary
            "threshold": 0.26,
            "operator": "<=",
            "left": {"id": "leaf_1"},  # Region assuming a lower monetary engagement
            "right": {"id": "leaf_2"},  # Region assuming a higher monetary engagement
        },
        "right": {
            "feature": 3,  # Time
            "threshold": 0.58,
            "operator": "<=",
            "left": {"id": "leaf_3"},  # Region assuming low recency and moderate frequency
            "right": {"id": "leaf_4"},  # Region assuming low recency but high frequency
        },
    },
    "right": {
        "feature": 3,  # Time
        "threshold": 1.08,
        "operator": "<=",
        "left": {"id": "leaf_5"},  # Region assuming high Recency
        "right": {"id": "leaf_6"},  # Region assuming high Recency and Time
    },
}



tree_full_md10_ml10_8 = {
    "feature": 0,  # Corresponding to "Recency"
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 2,  # Corresponding to "Monetary"
        "threshold": -0.43,
        "operator": "<=",
        "left": {"id": "leaf_1"},
        "right": {
            "feature": 1,  # Corresponding to "Frequency"
            "threshold": 4.90,
            "operator": "<=",
            "left": {
                "feature": 3,  # Corresponding to "Time"
                "threshold": 0.58,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 3,  # Corresponding to "Time"
        "threshold": 1.08,
        "operator": "<=",
        "left": {"id": "leaf_5"},
        "right": {
            "feature": 2,  # Corresponding to "Monetary"
            "threshold": 0.26,
            "operator": "<=",
            "left": {"id": "leaf_6"},
            "right": {"id": "leaf_7"},
        },
    },
}



tree_full_md10_ml10_0 = {
    "feature": 0,  # Corresponding to "Recency"
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 1,  # Corresponding to "Frequency"
        "threshold": 1.0,
        "operator": "<=",
        "left": {"id": "leaf_1"},  # Region favoring class 1.0
        "right": {
            "feature": 2,  # Corresponding to "Monetary"
            "threshold": 0.26,
            "operator": "<=",
            "left": {"id": "leaf_2"},  # Region favoring class 0.0
            "right": {"id": "leaf_3"},  # Region favoring class 1.0
        },
    },
    "right": {
        "feature": 3,  # Corresponding to "Time"
        "threshold": 1.08,
        "operator": "<=",
        "left": {"id": "leaf_4"},  # Region favoring class 0.0
        "right": {"id": "leaf_5"},  # Region favoring class 1.0
    },
}



tree_full_md10_ml10_1 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 1,
        "threshold": 1.0,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -0.6,
            "operator": "<=",
            "left": {"id": "leaf_1"},  # Region likely class 0
            "right": {
                "feature": 3,
                "threshold": 0.58,
                "operator": "<=",
                "left": {
                    "feature": 1,
                    "threshold": 0.09,
                    "operator": "<=",
                    "left": {"id": "leaf_2"},  # Region likely class 0
                    "right": {"id": "leaf_3"}  # Region likely class 1
                },
                "right": {"id": "leaf_4"}  # Region likely class 0
            },
        },
        "right": {"id": "leaf_5"},  # Region likely class 1
    },
    "right": {
        "feature": 3,
        "threshold": 1.08,
        "operator": "<=",
        "left": {"id": "leaf_6"},  # Region likely class 0
        "right": {"id": "leaf_7"}  # Region likely class 1
    },
}


