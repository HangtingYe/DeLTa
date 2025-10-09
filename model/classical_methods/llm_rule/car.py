
tree_full_md20_ml20_0 = {
    "feature": 3,
    "threshold": -0.70,
    "operator": "<=",
    "left": {"id": "leaf_1"},  # Class 0.0 (majority prediction for feature_3 <= -0.70)
    "right": {
        "feature": 5,
        "threshold": -0.53,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 0.84,
            "operator": "<=",
            "left": {"id": "leaf_2"},  # Class 1.0 (common prediction for feature_5 <= -0.53 & feature_1 <= 0.84)
            "right": {"id": "leaf_3"},  # Class 0.0 (common for feature_1 > 0.84)
        },
        "right": {
            "feature": 0,
            "threshold": -0.81,
            "operator": "<=",
            "left": {
                "feature": 2,
                "threshold": -0.87,
                "operator": "<=",
                "left": {"id": "leaf_4"},  # Class 1.0 (for feature_0 <= -0.81 & feature_2 <= -0.87)
                "right": {"id": "leaf_5"},  # Class 1.0 (for feature_0 <= -0.81 & feature_2 > -0.87)
            },
            "right": {
                "feature": 4,
                "threshold": 0.66,
                "operator": "<=",
                "left": {"id": "leaf_6"},  # Class 2.0 (for feature_0 > -0.81 & feature_4 <= 0.66)
                "right": {"id": "leaf_7"},  # Class 0.0 (for feature_0 > -0.81 & feature_4 > 0.66)
            },
        },
    },
}



tree_full_md20_ml20_9 = {
    "feature": 3,  # Choosing feature_3 as it appears frequently and often at the top of the existing trees
    "threshold": -0.7,
    "operator": "<=",
    "left": {"id": "leaf_1"},  # This path predominantly leads to class 0.0
    "right": {
        "feature": 5,  # feature_5 is also a crucial feature in the existing rules
        "threshold": -0.53,
        "operator": "<=",
        "left": {
            "feature": 1,  # feature_1 (threshold -0.92 or 0.84) is also significant in various paths
            "threshold": 0.84,
            "operator": "<=",
            "left": {"id": "leaf_2"},  # This path often leads to class 1.0 or 3.0
            "right": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_3"},  # Path for class 1.0
                "right": {"id": "leaf_4"},  # Occasionally leads to class 0.0 or another
            },
        },
        "right": {
            "feature": 4,  # feature_4 is used for splitting to distinguish further
            "threshold": 0.66,
            "operator": "<=",
            "left": {
                "feature": 2,  # optional deeper splits can be considered
                "threshold": -0.87,
                "operator": "<=",
                "left": {"id": "leaf_5"},  # Further distinguished paths
                "right": {"id": "leaf_6"},
            },
            "right": {"id": "leaf_7"},  # This path often dominates the class 0.0 outcomes
        },
    },
}



tree_full_md20_ml20_1 = {
    "feature": 3,
    "threshold": -0.7,
    "operator": "<=",
    "left": {"id": "leaf_1"},  
    "right": {
        "feature": 5,
        "threshold": -0.53,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 0.84,
            "operator": "<=",
            "left": {"id": "leaf_2"},
            "right": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {
                    "feature": 4,
                    "threshold": 0.66,
                    "operator": "<=",
                    "left": {"id": "leaf_4"},
                    "right": {"id": "leaf_5"},
                },
            },
        },
        "right": {
            "feature": 1,
            "threshold": 0.84,
            "operator": "<=",
            "left": {
                "feature": 4,
                "threshold": 0.66,
                "operator": "<=",
                "left": {
                    "feature": 2,
                    "threshold": -0.87,
                    "operator": "<=",
                    "left": {"id": "leaf_6"},
                    "right": {"id": "leaf_7"},
                },
                "right": {"id": "leaf_8"},
            },
            "right": {"id": "leaf_9"},
        },
    },
}



tree_full_md20_ml20_6 = {
    "feature": 3,
    "threshold": -0.70,
    "operator": "<=",
    "left": {"id": "leaf_1"},
    "right": {
        "feature": 5,
        "threshold": -0.53,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 0.84,
            "operator": "<=",
            "left": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
            "right": {
                "feature": 0,
                "threshold": 0.59,
                "operator": "<=",
                "left": {"id": "leaf_4"},
                "right": {"id": "leaf_5"},
            },
        },
        "right": {
            "feature": 4,
            "threshold": 0.66,
            "operator": "<=",
            "left": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"},
            },
            "right": {"id": "leaf_8"},
        },
    },
}



tree_full_md20_ml20_7 = {
    "feature": 3,  # feature_3 appears frequently in comparisons
    "threshold": -0.70,
    "operator": "<=",
    "left": {"id": "leaf_1"},  # Majority outcome when feature_3 is less than or equal to -0.70
    "right": {
        "feature": 5,  # feature_5 is also critical in determining branches
        "threshold": -0.53,
        "operator": "<=",
        "left": {
            "feature": 0,  # feature_0 is used often in branches
            "threshold": -0.81,
            "operator": "<=",
            "left": {"id": "leaf_2"},  # Outcome for this branch
            "right": {
                "feature": 1,
                "threshold": 0.84,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"},
            },
        },
        "right": {
            "feature": 4,  # feature_4 appears regularly, hence used here
            "threshold": 0.66,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
    },
}



tree_full_md20_ml20_2 = {
    "feature": 3,
    "threshold": -0.7,
    "operator": "<=",
    "left": {"id": "leaf_1"},  
    "right": {
        "feature": 1,
        "threshold": 0.84,
        "operator": "<=",
        "left": {
            "feature": 5,
            "threshold": -0.53,
            "operator": "<=",
            "left": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"}
            },
            "right": {
                "feature": 5,
                "threshold": 0.66,
                "operator": "<=",
                "left": {"id": "leaf_4"},
                "right": {"id": "leaf_5"}
            }
        },
        "right": {
            "feature": 4,
            "threshold": 0.66,
            "operator": "<=",
            "left": {
                "feature": 2,
                "threshold": 0.03,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"}
            },
            "right": {"id": "leaf_8"}
        }
    }
}



tree_full_md20_ml20_8 = {
    "feature": 3,
    "threshold": -0.70,
    "operator": "<=",
    "left": {"id": "leaf_1"},  # Captures class 0.0 consistently based on the provided rules
    "right": {
        "feature": 1,
        "threshold": 0.84,
        "operator": "<=",
        "left": {
            "feature": 5,
            "threshold": -0.53,
            "operator": "<=",
            "left": {"id": "leaf_2"},  # Captures class 1.0 patterns
            "right": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_3"},  # Mix of class 1.0 and class 2.0
                "right": {
                    "feature": 4,
                    "threshold": 0.66,
                    "operator": "<=",
                    "left": {"id": "leaf_4"},  # Captures class 3.0 and some class 2.0
                    "right": {"id": "leaf_5"}  # Captures Classes 1.0 distinctly
                }
            }
        },
        "right": {"id": "leaf_6"}  # Class 0.0 for feature_1 > 0.84
    }
}



tree_full_md20_ml20_4 = {
    "feature": 3,
    "threshold": -0.70,
    "operator": "<=",
    "left": {"id": "leaf_1"},
    "right": {
        "feature": 1,
        "threshold": 0.84,
        "operator": "<=",
        "left": {
            "feature": 5,
            "threshold": -0.53,
            "operator": "<=",
            "left": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
            "right": {
                "feature": 4,
                "threshold": 0.66,
                "operator": "<=",
                "left": {
                    "feature": 0,
                    "threshold": 0.59,
                    "operator": "<=",
                    "left": {"id": "leaf_4"},
                    "right": {"id": "leaf_5"},
                },
                "right": {"id": "leaf_6"},
            },
        },
        "right": {
            "feature": 5,
            "threshold": 0.66,
            "operator": "<=",
            "left": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_7"},
                "right": {
                    "feature": 2,
                    "threshold": 0.03,
                    "operator": "<=",
                    "left": {"id": "leaf_8"},
                    "right": {"id": "leaf_9"},
                },
            },
            "right": {
                "feature": 4,
                "threshold": -0.56,
                "operator": "<=",
                "left": {"id": "leaf_10"},
                "right": {"id": "leaf_11"},
            },
        },
    },
}



tree_full_md20_ml20_3 = {
    "feature": 3,
    "threshold": -0.70,
    "operator": "<=",
    "left": {"id": "leaf_1"},
    "right": {
        "feature": 5,
        "threshold": -0.53,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 0.84,
            "operator": "<=",
            "left": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
            "right": {
                "feature": 0,
                "threshold": -0.81,
                "operator": "<=",
                "left": {"id": "leaf_4"},
                "right": {"id": "leaf_5"},
            },
        },
        "right": {
            "feature": 0,
            "threshold": 0.59,
            "operator": "<=",
            "left": {
                "feature": 4,
                "threshold": 0.66,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"},
            },
            "right": {"id": "leaf_8"},
        },
    },
}



tree_full_md20_ml20_5 = {
    "feature": 5,
    "threshold": -0.53,
    "operator": "<=",
    "left": {
        "feature": 3,
        "threshold": -0.70,
        "operator": "<=",
        "left": {"id": "leaf_1"},
        "right": {
            "feature": 1,
            "threshold": 0.84,
            "operator": "<=",
            "left": {"id": "leaf_2"},
            "right": {
                "feature": 0,
                "threshold": 0.59,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"},
            },
        },
    },
    "right": {
        "feature": 4,
        "threshold": 0.66,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -0.87,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {
                "feature": 1,
                "threshold": -0.92,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"},
            },
        },
        "right": {
            "feature": 0,
            "threshold": -0.81,
            "operator": "<=",
            "left": {"id": "leaf_8"},
            "right": {"id": "leaf_9"},
        },
    },
}


