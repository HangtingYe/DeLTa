
tree_full_md10_ml10_0 = {
    "feature": 0,
    "threshold": 0.10,
    "operator": "<=",
    "left": {
        "feature": 1,
        "threshold": 0.50,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -0.50,
            "operator": "<=",
            "left": {"id": "leaf_1"},  
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 3,
            "threshold": 0.50,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 0,
        "threshold": 0.40,
        "operator": "<=",
        "left": {"id": "leaf_5"}, 
        "right": {"id": "leaf_6"},
    },
}



tree_full_md10_ml10_1 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 3,
        "threshold": 0.58,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 0.09,
            "operator": "<=",
            "left": {
                "feature": 2,
                "threshold": -0.43,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {"id": "leaf_2"}
            },
            "right": {"id": "leaf_3"}
        },
        "right": {
            "feature": 1,
            "threshold": 4.90,
            "operator": "<=",
            "left": {"id": "leaf_4"},
            "right": {"id": "leaf_5"}
        }
    },
    "right": {
        "feature": 0,
        "threshold": 0.44,
        "operator": "<=",
        "left": {
            "feature": 3,
            "threshold": 1.08,
            "operator": "<=",
            "left": {
                "feature": 2,
                "threshold": 0.26,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"}
            },
            "right": {"id": "leaf_8"}
        },
        "right": {"id": "leaf_9"}
    }
}



tree_full_md10_ml10_2 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 1,
        "threshold": 4.90,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -0.43,
            "operator": "<=",
            "left": {"id": "leaf_1"},  # Region mostly class 0
            "right": {
                "feature": 3,
                "threshold": 0.58,
                "operator": "<=",
                "left": {"id": "leaf_2"},  # Region potentially class 1
                "right": {"id": "leaf_3"},  # Region mostly class 0
            },
        },
        "right": {"id": "leaf_4"},  # Region mostly class 1 (feature_1 > 4.90)
    },
    "right": {
        "feature": 3,
        "threshold": 1.08,
        "operator": "<=",
        "left": {"id": "leaf_5"},  # Region mostly class 0
        "right": {
            "feature": 2,
            "threshold": 1.12,
            "operator": "<=",
            "left": {"id": "leaf_6"},  # Region potentially class 0
            "right": {"id": "leaf_7"},  # Region potentially class 1
        },
    },
}



tree_full_md10_ml10_3 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 2,
        "threshold": -0.60,
        "operator": "<=",
        "left": {"id": "leaf_1"},  
        "right": {
            "feature": 1,
            "threshold": 4.90,
            "operator": "<=",
            "left": {
                "feature": 3,
                "threshold": 0.58,
                "operator": "<=",
                "left": {
                    "feature": 1,
                    "threshold": 0.30,
                    "operator": "<=",
                    "left": {"id": "leaf_2"},  
                    "right": {"id": "leaf_3"},
                },
                "right": {"id": "leaf_4"},
            },
            "right": {"id": "leaf_5"},
        },
    },
    "right": {"id": "leaf_6"},
}



tree_full_md10_ml10_4 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 2,
        "threshold": 0.26,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 0.86,
            "operator": "<=",
            "left": {"id": "leaf_1"},  # Combined regions for class 1.0
            "right": {"id": "leaf_2"},  # Specific regions leading to class 0.0
        },
        "right": {
            "feature": 1,
            "threshold": 4.90,
            "operator": "<=",
            "left": {
                "feature": 3,
                "threshold": 0.58,
                "operator": "<=",
                "left": {"id": "leaf_3"},  # Regions that primarily led to class 0.0
                "right": {"id": "leaf_4"},  # Regions leading to class 1.0
            },
            "right": {"id": "leaf_5"},  # High feature_1 values leading to class 1.0
        },
    },
    "right": {"id": "leaf_6"},  # General class 0.0 for feature_0 > 0.14
}



tree_full_md10_ml10_5 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 2,
        "threshold": -0.60,
        "operator": "<=",
        "left": {"id": "leaf_1"},  # Mainly where class 0.0 was occurring
        "right": {
            "feature": 1,
            "threshold": 4.90,
            "operator": "<=",
            "left": {
                "feature": 1,
                "threshold": 0.30,
                "operator": "<=",
                "left": {"id": "leaf_2"},  # Consolidating an early decision for class 0.0
                "right": {
                    "feature": 2,
                    "threshold": 1.90,
                    "operator": "<=",
                    "left": {
                        "feature": 3,
                        "threshold": 0.58,
                        "operator": "<=",
                        "left": {"id": "leaf_3"},  # Mixed class evaluations
                        "right": {"id": "leaf_4"},
                    },
                    "right": {"id": "leaf_5"},  # Where class 1.0 was often predicted
                },
            },
            "right": {"id": "leaf_6"},  # Mostly class 1.0
        },
    },
    "right": {"id": "leaf_7"},  # Mainly where class 0.0 was occurring
}



tree_full_md10_ml10_6 = {
    "feature": 0,  # Starting with feature_0 as it is consistently used as the root condition
    "threshold": 0.25,
    "operator": "<=",
    "left": {
        "feature": 3,  # feature_3 is also frequently seen as a pivotal feature
        "threshold": 0.5,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 1.0,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {"id": "leaf_3"}
    },
    "right": {
        "feature": 2,
        "threshold": 0.5,
        "operator": "<=",
        "left": {"id": "leaf_4"},
        "right": {"id": "leaf_5"}
    }
}



tree_full_md10_ml10_7 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 1,
        "threshold": 0.86,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -0.43,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 2,
            "threshold": 1.90,
            "operator": "<=",
            "left": {
                "feature": 3,
                "threshold": 0.58,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"},
            },
            "right": {"id": "leaf_5"},
        },
    },
    "right": {
        "feature": 3,
        "threshold": 1.08,
        "operator": "<=",
        "left": {"id": "leaf_6"},
        "right": {"id": "leaf_7"},
    },
}



tree_full_md10_ml10_8 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 1,
        "threshold": 1.0,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": 0.26,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 1,
            "threshold": 4.9,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        }
    },
    "right": {"id": "leaf_5"}
}



tree_full_md10_ml10_9 = {
    "feature": 0,
    "threshold": 0.14,
    "operator": "<=",
    "left": {
        "feature": 2,
        "threshold": -0.60,
        "operator": "<=",
        "left": {"id": "leaf_1"},  # Predominantly class 0
        "right": {
            "feature": 1,
            "threshold": 0.86,
            "operator": "<=",
            "left": {
                "feature": 3,
                "threshold": 0.58,
                "operator": "<=",
                "left": {"id": "leaf_2"},  # Mixed with emphasis on class 1
                "right": {"id": "leaf_3"},  # Predominantly class 0
            },
            "right": {"id": "leaf_4"},  # Predominantly class 1
        }
    },
    "right": {
        "feature": 0,
        "threshold": 0.44,
        "operator": "<=",
        "left": {
            "feature": 3,
            "threshold": 1.08,
            "operator": "<=",
            "left": {
                "feature": 1,
                "threshold": 1.47,
                "operator": "<=",
                "left": {"id": "leaf_5"},  # Mixed with emphasis on class 0
                "right": {"id": "leaf_6"},  # Predominantly class 1
            },
            "right": {"id": "leaf_7"},  # Predominantly class 0
        },
        "right": {"id": "leaf_8"},  # Predominantly class 0
    }
}


