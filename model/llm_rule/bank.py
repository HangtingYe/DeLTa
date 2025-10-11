
tree_full_md5_ml50_4 = {
    "feature": 3,  # feature representing 'duration'
    "threshold": 0.5,
    "operator": "<=",
    "left": {
        "feature": 5,  # feature representing 'campaign'
        "threshold": 0.8,
        "operator": "<=",
        "left": {
            "feature": 14,  # feature representing 'poutcome'
            "threshold": 0.9,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {
                "feature": 11,  # feature representing 'housing'
                "threshold": 0.0,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
        },
        "right": {
            "feature": 2,  # feature representing 'day'
            "threshold": 1.0,
            "operator": "<=",
            "left": {"id": "leaf_4"},
            "right": {"id": "leaf_5"},
        },
    },
    "right": {
        "feature": 1,  # feature representing 'balance'
        "threshold": 0.3,
        "operator": "<=",
        "left": {
            "feature": 6,  # feature representing 'previous'
            "threshold": 1.2,
            "operator": "<=",
            "left": {"id": "leaf_6"},
            "right": {"id": "leaf_7"},
        },
        "right": {
            "feature": 14,  # feature representing 'poutcome'
            "threshold": 2.0,
            "operator": "<=",
            "left": {"id": "leaf_8"},
            "right": {
                "feature": 12,  # feature representing 'loan'
                "threshold": 0.5,
                "operator": "<=",
                "left": {"id": "leaf_9"},
                "right": {"id": "leaf_10"},
            },
        },
    },
}



tree_full_md5_ml50_1 = {
    "feature": 3,
    "threshold": 0.75,
    "operator": "<=",
    "left": {
        "feature": 14,
        "threshold": 1.32,
        "operator": "<=",
        "left": {
            "feature": 11,
            "threshold": -0.12,
            "operator": "<=",
            "left": {
                "feature": 15,
                "threshold": -0.06,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {"id": "leaf_2"},
            },
            "right": {
                "feature": 5,
                "threshold": 0.68,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"},
            },
        },
        "right": {
            "feature": 0,
            "threshold": 1.84,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {
                "feature": 13,
                "threshold": 0.95,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"},
            },
        },
    },
    "right": {
        "feature": 6,
        "threshold": -0.04,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": 0.44,
            "operator": "<=",
            "left": {"id": "leaf_8"},
            "right": {"id": "leaf_9"},
        },
        "right": {
            "feature": 15,
            "threshold": -1.07,
            "operator": "<=",
            "left": {"id": "leaf_10"},
            "right": {
                "feature": 1,
                "threshold": 0.74,
                "operator": "<=",
                "left": {"id": "leaf_11"},
                "right": {"id": "leaf_12"},
            },
        },
    },
}



tree_full_md5_ml50_3 = {
    "feature": 3,
    "threshold": 0.40,
    "operator": "<=",
    "left": {  # Left branch for feature_3 <= 0.40
        "feature": 15,
        "threshold": -0.06,
        "operator": "<=",
        "left": {  # Left branch for feature_15 <= -0.06
            "feature": 11,
            "threshold": -0.12,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {  # Right branch for feature_15 > -0.06
            "feature": 13,
            "threshold": 0.95,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {  # Right branch for feature_3 > 0.40
        "feature": 14,
        "threshold": 1.32,
        "operator": "<=",
        "left": {  # Left branch for feature_14 <= 1.32
            "feature": 6,
            "threshold": -0.04,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
        "right": {  # Right branch for feature_14 > 1.32
            "feature": 5,
            "threshold": 0.73,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"},
        },
    },
}



tree_full_md5_ml50_7 = {
    "feature": 3,  # duration might be an influential feature based on previous rules
    "threshold": 0.75,
    "operator": ">",
    "left": {
        "feature": 6,  # pdays as another decision point
        "threshold": -0.04,
        "operator": "<=",
        "left": {"id": "leaf_1"},
        "right": {
            "feature": 5,  # campaign
            "threshold": 1.5,
            "operator": "<=",
            "left": {"id": "leaf_2"},
            "right": {"id": "leaf_3"},
        },
    },
    "right": {
        "feature": 14,  # poutcome feature focus
        "threshold": 1.32,
        "operator": "<=",
        "left": {
            "feature": 11,  # default
            "threshold": -0.12,
            "operator": "<=",
            "left": {"id": "leaf_4"},
            "right": {
                "feature": 8,  # contact as decision point
                "threshold": 0.55,
                "operator": "<=",
                "left": {"id": "leaf_5"},
                "right": {"id": "leaf_6"},
            },
        },
        "right": {
            "feature": 1,  # Second focus on balance or job category
            "threshold": 0.5,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {
                "feature": 12,  # Further pruning based on another feature, perhaps education
                "threshold": 0.94,
                "operator": "<=",
                "left": {"id": "leaf_8"},
                "right": {"id": "leaf_9"},
            },
        },
    },
}



tree_full_md5_ml50_0 = {
    "feature": 3,
    "threshold": 1.0,
    "operator": "<=",
    "left": {
        "feature": 6,
        "threshold": -0.04,
        "operator": "<=",
        "left": {
            "feature": 14,
            "threshold": 1.32,
            "operator": "<=",
            "left": {
                "feature": 0,
                "threshold": 1.5,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {"id": "leaf_2"},
            },
            "right": {
                "feature": 2,
                "threshold": 0.56,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"},
            },
        },
        "right": {"id": "leaf_5"},
    },
    "right": {
        "feature": 11,
        "threshold": -0.12,
        "operator": "<=",
        "left": {
            "feature": 5,
            "threshold": 1.5,
            "operator": "<=",
            "left": {"id": "leaf_6"},
            "right": {
                "feature": 15,
                "threshold": -0.06,
                "operator": "<=",
                "left": {"id": "leaf_7"},
                "right": {"id": "leaf_8"},
            },
        },
        "right": {
            "feature": 7,
            "threshold": 0.5,
            "operator": "<=",
            "left": {"id": "leaf_9"},
            "right": {"id": "leaf_10"},
        },
    },
}



tree_full_md5_ml50_6 = {
    "feature": 5,  # balance
    "threshold": 0.5,
    "operator": "<=",
    "left": {
        "feature": 3,  # duration
        "threshold": 1.0,
        "operator": "<=",
        "left": {
            "feature": 14,  # month
            "threshold": 0.5,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {
                "feature": 11,  # contact
                "threshold": -0.2,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
        },
        "right": {
            "feature": 7,  # campaign
            "threshold": 1.2,
            "operator": "<=",
            "left": {"id": "leaf_4"},
            "right": {
                "feature": 1,  # job
                "threshold": -0.1,
                "operator": "<=",
                "left": {"id": "leaf_5"},
                "right": {"id": "leaf_6"},
            },
        },
    },
    "right": {
        "feature": 2,  # day
        "threshold": 1.5,
        "operator": "<=",
        "left": {
            "feature": 6,  # pdays
            "threshold": 0.3,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"},
        },
        "right": {
            "feature": 9,  # default
            "threshold": 0.1,
            "operator": "<=",
            "left": {"id": "leaf_9"},
            "right": {
                "feature": 15,  # loan
                "threshold": 0.2,
                "operator": "<=",
                "left": {"id": "leaf_10"},
                "right": {"id": "leaf_11"},
            },
        },
    },
}



tree_full_md5_ml50_8 = {
    "feature": 3,
    "threshold": 0.81,
    "operator": "<=",
    "left": {
        "feature": 15,
        "threshold": -0.06,
        "operator": "<=",
        "left": {
            "feature": 11,
            "threshold": -0.12,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {
                "feature": 1,
                "threshold": -0.48,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
        },
        "right": {
            "feature": 11,
            "threshold": -0.12,
            "operator": ">",
            "left": {
                "feature": 14,
                "threshold": 1.32,
                "operator": "<=",
                "left": {"id": "leaf_4"},
                "right": {"id": "leaf_5"},
            },
            "right": {"id": "leaf_6"},
        },
    },
    "right": {
        "feature": 6,
        "threshold": -0.04,
        "operator": "<=",
        "left": {
            "feature": 13,
            "threshold": 0.95,
            "operator": "<=",
            "left": {
                "feature": 5,
                "threshold": 0.46,
                "operator": "<=",
                "left": {"id": "leaf_7"},
                "right": {"id": "leaf_8"},
            },
            "right": {
                "feature": 3,
                "threshold": 2.07,
                "operator": "<=",
                "left": {"id": "leaf_9"},
                "right": {"id": "leaf_10"},
            },
        },
        "right": {
            "feature": 5,
            "threshold": 0.67,
            "operator": "<=",
            "left": {
                "feature": 11,
                "threshold": -0.12,
                "operator": "<=",
                "left": {"id": "leaf_11"},
                "right": {"id": "leaf_12"},
            },
            "right": {
                "feature": 7,
                "threshold": 0.05,
                "operator": "<=",
                "left": {"id": "leaf_13"},
                "right": {"id": "leaf_14"},
            },
        },
    },
}



tree_full_md5_ml50_9 = {
    "feature": 3,
    "threshold": 0.75,
    "operator": "<=",
    "left": {
        "feature": 5,
        "threshold": -0.12,
        "operator": "<=",
        "left": {
            "feature": 0,
            "threshold": 1.84,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {
                "feature": 14,
                "threshold": 1.32,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {
                    "feature": 2,
                    "threshold": -0.04,
                    "operator": "<=",
                    "left": {"id": "leaf_3"},
                    "right": {"id": "leaf_4"},
                },
            },
        },
        "right": {
            "feature": 8,
            "threshold": 0.55,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
    },
    "right": {
        "feature": 14,
        "threshold": 1.32,
        "operator": "<=",
        "left": {
            "feature": 6,
            "threshold": -0.04,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"},
        },
        "right": {
            "feature": 2,
            "threshold": 0.56,
            "operator": "<=",
            "left": {"id": "leaf_9"},
            "right": {
                "feature": 1,
                "threshold": 0.74,
                "operator": "<=",
                "left": {"id": "leaf_10"},
                "right": {"id": "leaf_11"},
            },
        },
    },
}



tree_full_md5_ml50_2 = {
    "feature": 14,
    "threshold": 1.32,
    "operator": "<=",
    "left": {
        "feature": 3,
        "threshold": 0.75,
        "operator": "<=",
        "left": {
            "feature": 5,
            "threshold": 0.50,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 6,
            "threshold": 0.00,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 2,
        "threshold": 0.56,
        "operator": "<=",
        "left": {
            "feature": 11,
            "threshold": -0.12,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
        "right": {
            "feature": 1,
            "threshold": 0.07,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"},
        },
    },
}



tree_full_md5_ml50_5 = {
    "feature": 3,  # Assuming this is a pivotal feature based on its frequent appearance
    "threshold": 0.95,
    "operator": "<=",
    "left": {
        "feature": 14,  # Another frequent feature in rules
        "threshold": 1.32,
        "operator": "<=",
        "left": {
            "feature": 11,
            "threshold": -0.12,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 6,  # Another impactful feature
            "threshold": -0.04,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 15,
        "threshold": -0.06,
        "operator": "<=",
        "left": {
            "feature": 5,
            "threshold": 1.51,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
        "right": {
            "feature": 1,
            "threshold": 0.44,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"},
        },
    },
}


