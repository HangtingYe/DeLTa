
tree_full_md15_ml20_7 = {
    "feature": 1,
    "threshold": 1.11,
    "operator": "<=",
    "left": {
        "feature": 8,
        "threshold": 1.19,
        "operator": "<=",
        "left": {
            "feature": 17,
            "threshold": -0.77,
            "operator": "<=",
            "left": {
                "feature": 10,
                "threshold": -0.59,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {"id": "leaf_2"}
            },
            "right": {
                "feature": 0,
                "threshold": -0.75,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"}
            }
        },
        "right": {
            "feature": 16,
            "threshold": -1.08,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"}
        }
    },
    "right": {
        "feature": 9,
        "threshold": 0.43,
        "operator": "<=",
        "left": {
            "feature": 11,
            "threshold": 0.71,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"}
        },
        "right": {
            "feature": 7,
            "threshold": 0.77,
            "operator": "<=",
            "left": {"id": "leaf_9"},
            "right": {"id": "leaf_10"}
        }
    }
}



tree_full_md15_ml20_4 = {
    "feature": 7,
    "threshold": -0.02,
    "operator": "<=",
    "left": {
        "feature": 11,
        "threshold": 0.71,
        "operator": "<=",
        "left": {
            "feature": 0,
            "threshold": -0.01,
            "operator": "<=",
            "left": {"id": "leaf_1"},  # Capturing lower values leading towards class 1.0
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 9,
            "threshold": 0.43,
            "operator": ">",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 5,
        "threshold": 0.20,
        "operator": "<=",
        "left": {
            "feature": 14,
            "threshold": -0.73,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {
                "feature": 1,
                "threshold": 1.54,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"},
            },
        },
        "right": {
            "feature": 10,
            "threshold": 0.32,
            "operator": ">",
            "left": {"id": "leaf_8"},
            "right": {
                "feature": 8,
                "threshold": 1.19,
                "operator": "<=",
                "left": {"id": "leaf_9"},
                "right": {"id": "leaf_10"},
            },
        },
    },
}



tree_full_md15_ml20_9 = {
    "feature": 0,
    "threshold": 0.65,
    "operator": "<=",
    "left": {
        "feature": 8,
        "threshold": -1.71,
        "operator": "<=",
        "left": {"id": "leaf_1"},  # Region where feature 0 <= 0.65 and feature 8 <= -1.71
        "right": {
            "feature": 1,
            "threshold": 1.54,
            "operator": "<=",
            "left": {"id": "leaf_2"},  # Region where feature 0 <= 0.65, feature 8 > -1.71, and feature 1 <= 1.54
            "right": {"id": "leaf_3"}   # Region where feature 0 <= 0.65, feature 8 > -1.71, and feature 1 > 1.54
        },
    },
    "right": {
        "feature": 7,
        "threshold": 0.77,
        "operator": "<=",
        "left": {
            "feature": 11,
            "threshold": 0.71,
            "operator": "<=",
            "left": {"id": "leaf_4"},  # Region where feature 0 > 0.65, feature 7 <= 0.77, and feature 11 <= 0.71
            "right": {"id": "leaf_5"}  # Region where feature 0 > 0.65, feature 7 <= 0.77, and feature 11 > 0.71
        },
        "right": {"id": "leaf_6"}   # Region where feature 0 > 0.65 and feature 7 > 0.77
    }
}



tree_full_md15_ml20_5 = {
    "feature": 1,
    "threshold": 0.91,
    "operator": "<=",
    "left": {
        "feature": 7,
        "threshold": -0.02,
        "operator": "<=",
        "left": {
            "feature": 8,
            "threshold": 1.19,
            "operator": "<=",
            "left": {
                "feature": 11,
                "threshold": 0.71,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {"id": "leaf_2"},
            },
            "right": {"id": "leaf_3"},
        },
        "right": {
            "feature": 3,
            "threshold": 0.61,
            "operator": "<=",
            "left": {"id": "leaf_4"},
            "right": {"id": "leaf_5"},
        },
    },
    "right": {
        "feature": 0,
        "threshold": 0.65,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -0.39,
            "operator": "<=",
            "left": {"id": "leaf_6"},
            "right": {"id": "leaf_7"},
        },
        "right": {
            "feature": 10,
            "threshold": 0.32,
            "operator": "<=",
            "left": {"id": "leaf_8"},
            "right": {"id": "leaf_9"},
        },
    },
}



tree_full_md15_ml20_2 = {
    "feature": 0,
    "threshold": 0,
    "operator": "<=",
    "left": {
        "feature": 7,
        "threshold": -0.02,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 1.86,
            "operator": "<=",
            "left": {
                "feature": 17,
                "threshold": -0.77,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {"id": "leaf_2"},
            },
            "right": {
                "feature": 2,
                "threshold": -1.27,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"},
            },
        },
        "right": {
            "feature": 11,
            "threshold": 0.71,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
    },
    "right": {
        "feature": 8,
        "threshold": 1.19,
        "operator": "<=",
        "left": {
            "feature": 16,
            "threshold": -1.08,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"},
        },
        "right": {"id": "leaf_9"},
    },
}



tree_full_md15_ml20_6 = {
    "feature": 7,
    "threshold": 0.15,
    "operator": "<=",
    "left": {
        "feature": 1,
        "threshold": 1.20,
        "operator": "<=",
        "left": {
            "feature": 10,
            "threshold": 0.50,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 4,
            "threshold": -0.03,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 0,
        "threshold": -0.50,
        "operator": "<=",
        "left": {
            "feature": 17,
            "threshold": 0.20,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
        "right": {
            "feature": 2,
            "threshold": -0.39,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"},
        },
    },
}



tree_full_md15_ml20_1 = {
    "feature": 8,
    "threshold": 0.22,
    "operator": "<=",
    "left": {
        "feature": 7,
        "threshold": -0.02,
        "operator": "<=",
        "left": {
            "feature": 1,
            "threshold": 1.11,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 3,
            "threshold": 0.61,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 0,
        "threshold": 0.65,
        "operator": "<=",
        "left": {
            "feature": 10,
            "threshold": 0.32,
            "operator": "<=",
            "left": {"id": "leaf_5"},
            "right": {"id": "leaf_6"},
        },
        "right": {
            "feature": 9,
            "threshold": 0.83,
            "operator": "<=",
            "left": {"id": "leaf_7"},
            "right": {"id": "leaf_8"},
        },
    },
}



tree_full_md15_ml20_0 = {
    "feature": 7,
    "threshold": 0.77,
    "operator": "<=",
    "left": {
        "feature": 1,
        "threshold": 0.22,
        "operator": "<=",
        "left": {
            "feature": 8,
            "threshold": 1.19,
            "operator": "<=",
            "left": {"id": "leaf_1"},  
            "right": {
                "feature": 16,
                "threshold": -1.08,
                "operator": "<=",
                "left": {"id": "leaf_2"},  
                "right": {"id": "leaf_3"},
            },
        },
        "right": {
            "feature": 0,
            "threshold": 0.65,
            "operator": "<=",
            "left": {"id": "leaf_4"},
            "right": {"id": "leaf_5"},
         },
    },
    "right": {
        "feature": 2,
        "threshold": 0.49,
        "operator": "<=",
        "left": {
            "feature": 11,
            "threshold": 1.45,
            "operator": "<=",
            "left": {"id": "leaf_6"},
            "right": {"id": "leaf_7"},
        },
        "right": {
            "feature": 4,
            "threshold": -0.07,
            "operator": "<=",
            "left": {"id": "leaf_8"},
            "right": {"id": "leaf_9"},
        },
    },
}



tree_full_md15_ml20_3 = {
    "feature": 1,
    "threshold": 0.22,
    "operator": "<=",
    "left": {
        "feature": 0,
        "threshold": -0.75,
        "operator": "<=",
        "left": {"id": "leaf_1"},
        "right": {
            "feature": 7,
            "threshold": -0.02,
            "operator": "<=",
            "left": {"id": "leaf_2"},
            "right": {
                "feature": 9,
                "threshold": 0.83,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"},
            }
        },
    },
    "right": {
        "feature": 8,
        "threshold": 1.19,
        "operator": "<=",
        "left": {
            "feature": 10,
            "threshold": -0.59,
            "operator": "<=",
            "left": {
                "feature": 11,
                "threshold": 1.45,
                "operator": "<=",
                "left": {"id": "leaf_5"},
                "right": {"id": "leaf_6"},
            },
            "right": {
                "feature": 6,
                "threshold": 1.00,
                "operator": "<=",
                "left": {"id": "leaf_7"},
                "right": {"id": "leaf_8"},
            },
        },
        "right": {
            "feature": 16,
            "threshold": -1.08,
            "operator": "<=",
            "left": {"id": "leaf_9"},
            "right": {"id": "leaf_10"},
        },
    },
}



tree_full_md15_ml20_8 = {
    "feature": 8,
    "threshold": -0.74,
    "operator": "<=",
    "left": {
        "feature": 1,
        "threshold": 0.22,
        "operator": "<=",
        "left": {
            "feature": 4,
            "threshold": 0.0,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {
                "feature": 7,
                "threshold": -0.02,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            }
        },
        "right": {
            "feature": 10,
            "threshold": 1.24,
            "operator": "<=",
            "left": {"id": "leaf_4"},
            "right": {"id": "leaf_5"},
        }
    },
    "right": {
        "feature": 0,
        "threshold": -0.01,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": 0.49,
            "operator": "<=",
            "left": {"id": "leaf_6"},
            "right": {
                "feature": 16,
                "threshold": 0.82,
                "operator": "<=",
                "left": {"id": "leaf_7"},
                "right": {"id": "leaf_8"},
            }
        },
        "right": {
            "feature": 6,
            "threshold": 1.00,
            "operator": "<=",
            "left": {
                "feature": 14,
                "threshold": -0.73,
                "operator": "<=",
                "left": {"id": "leaf_9"},
                "right": {"id": "leaf_10"}
            },
            "right": {"id": "leaf_11"}
        }
    }
}


