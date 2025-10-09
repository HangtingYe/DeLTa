
tree_full_md10_ml200_1 = {
    "feature": 11,
    "threshold": -0.78,
    "operator": "<=",
    "left": {"id": "leaf_1"},
    "right": {
        "feature": 7,
        "threshold": 0.23,
        "operator": "<=",
        "left": {
            "feature": 17,
            "threshold": 1.25,
            "operator": "<=",
            "left": {"id": "leaf_2"},
            "right": {
                "feature": 3,
                "threshold": -0.64,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {"id": "leaf_4"},
            }
        },
        "right": {
            "feature": 2,
            "threshold": 0.55,
            "operator": "<=",
            "left": {
                "feature": 19,
                "threshold": 0.87,
                "operator": "<=",
                "left": {"id": "leaf_5"},
                "right": {"id": "leaf_6"},
            },
            "right": {"id": "leaf_7"},
        }
    }
}



tree_full_md10_ml200_0 = {
    "feature": 18,
    "threshold": 0.08,
    "operator": "<=",
    "left": {  # Subtree for feature_18 <= 0.08
        "feature": 17,
        "threshold": 0.28,
        "operator": "<=",
        "left": {  # Subtree for feature_17 <= 0.28
            "feature": 2,
            "threshold": 0.37,
            "operator": "<=",
            "left": {  # Subtree for feature_2 <= 0.37
                "feature": 15,
                "threshold": -0.48,
                "operator": "<=",
                "left": {"id": "leaf_1"},  # Deep low-memory/reclaimed page activity
                "right": {  # Subtree for feature_15 > -0.48
                    "feature": 7,
                    "threshold": -0.74,
                    "operator": "<=",
                    "left": {"id": "leaf_2"},  # Network I/O constraint observed
                    "right": {"id": "leaf_3"},  # Moderate I/O and memory activity
                },
            },
            "right": {  # Subtree for feature_2 > 0.37
                "feature": 17,
                "threshold": -0.15,
                "operator": "<=",
                "left": {  # Subtree for feature_17 <= -0.15
                    "feature": 8,
                    "threshold": -0.47,
                    "operator": "<=",
                    "left": {"id": "leaf_4"},  # CPU-bound workload (low cache hits)
                    "right": {"id": "leaf_5"},  # Balanced CPU and I/O activity
                },
                "right": {"id": "leaf_6"},  # High CPU activity with efficient paging
            },
        },
        "right": {  # Subtree for feature_17 > 0.28
            "feature": 2,
            "threshold": 1.24,
            "operator": "<=",
            "left": {  # Subtree for feature_2 <= 1.24
                "feature": 17,
                "threshold": 1.06,
                "operator": "<=",
                "left": {"id": "leaf_7"},  # Mixed workload with compute-moderate regions
                "right": {"id": "leaf_8"},  # Memory-constrained compute focus
            },
            "right": {  # Subtree for feature_2 > 1.24
                "feature": 17,
                "threshold": 1.75,
                "operator": "<=",
                "left": {"id": "leaf_9"},  # Transient high CPU activity spikes
                "right": {"id": "leaf_10"},  # Sustained heavy compute utilization
            },
        },
    },
    "right": {  # Subtree for feature_18 > 0.08
        "feature": 19,
        "threshold": 0.16,
        "operator": "<=",
        "left": {"id": "leaf_11"},  # Idle latency observed (resource underutilized)
        "right": {"id": "leaf_12"},  # System overload (multi-dimensional bottleneck)
    },
}



tree_full_md10_ml200_3 = {
    "feature": 18,
    "threshold": 0.08,
    "operator": "<=",
    "left": {
        "feature": 17,
        "threshold": -0.5,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -1.0,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {
                "feature": 15,
                "threshold": 0.5,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
        },
        "right": {
            "feature": 7,
            "threshold": 0.3,
            "operator": "<=",
            "left": {
                "feature": 4,
                "threshold": -0.2,
                "operator": "<=",
                "left": {"id": "leaf_4"},
                "right": {
                    "feature": 20,
                    "threshold": 1.0,
                    "operator": "<=",
                    "left": {"id": "leaf_5"},
                    "right": {"id": "leaf_6"},
                },
            },
            "right": {
                "feature": 14,
                "threshold": -0.3,
                "operator": "<=",
                "left": {"id": "leaf_7"},
                "right": {"id": "leaf_8"},
            },
        },
    },
    "right": {
        "feature": 17,
        "threshold": 1.5,
        "operator": "<=",
        "left": {
            "feature": 6,
            "threshold": 0.5,
            "operator": "<=",
            "left": {
                "feature": 2,
                "threshold": 0.6,
                "operator": "<=",
                "left": {"id": "leaf_9"},
                "right": {"id": "leaf_10"},
            },
            "right": {
                "feature": 14,
                "threshold": 1.2,
                "operator": "<=",
                "left": {"id": "leaf_11"},
                "right": {"id": "leaf_12"},
            },
        },
        "right": {
            "feature": 7,
            "threshold": 0.9,
            "operator": "<=",
            "left": {
                "feature": 5,
                "threshold": 1.0,
                "operator": "<=",
                "left": {"id": "leaf_13"},
                "right": {"id": "leaf_14"},
            },
            "right": {
                "feature": 4,
                "threshold": 0.5,
                "operator": "<=",
                "left": {"id": "leaf_15"},
                "right": {"id": "leaf_16"},
            },
        },
    },
}



tree_full_md10_ml200_2 = {
    "feature": 17,
    "threshold": 0.3,
    "operator": "<=",
    "left": {
        "feature": 2,
        "threshold": -0.5,
        "operator": "<=",
        "left": {
            "feature": 8,
            "threshold": 0.2,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {"id": "leaf_2"},
        },
        "right": {
            "feature": 10,
            "threshold": 1.0,
            "operator": "<=",
            "left": {"id": "leaf_3"},
            "right": {"id": "leaf_4"},
        },
    },
    "right": {
        "feature": 14,
        "threshold": 0.1,
        "operator": "<=",
        "left": {
            "feature": 6,
            "threshold": 0.5,
            "operator": "<=",
            "left": {
                "feature": 18,
                "threshold": -0.2,
                "operator": "<=",
                "left": {"id": "leaf_5"},
                "right": {"id": "leaf_6"},
            },
            "right": {"id": "leaf_7"},
        },
        "right": {
            "feature": 5,
            "threshold": -0.1,
            "operator": "<=",
            "left": {"id": "leaf_8"},
            "right": {
                "feature": 15,
                "threshold": 0.75,
                "operator": "<=",
                "left": {"id": "leaf_9"},
                "right": {"id": "leaf_10"},
            },
        },
    },
}



tree_full_md10_ml200_9 = {
    "feature": 18,
    "threshold": 0.08,
    "operator": "<=",
    "left": {
        "feature": 17,
        "threshold": -0.3,
        "operator": "<=",
        "left": {
            "feature": 4,
            "threshold": -0.36,
            "operator": "<=",
            "left": {
                "feature": 2,
                "threshold": -1.22,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {"id": "leaf_2"},
            },
            "right": {
                "feature": 15,
                "threshold": -0.48,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {
                    "feature": 3,
                    "threshold": -0.64,
                    "operator": "<=",
                    "left": {"id": "leaf_4"},
                    "right": {
                        "feature": 20,
                        "threshold": 1.01,
                        "operator": "<=",
                        "left": {"id": "leaf_5"},
                        "right": {"id": "leaf_6"},
                    },
                },
            },
        },
        "right": {
            "feature": 2,
            "threshold": 0.66,
            "operator": "<=",
            "left": {
                "feature": 8,
                "threshold": -0.47,
                "operator": "<=",
                "left": {
                    "feature": 15,
                    "threshold": 4.22,
                    "operator": "<=",
                    "left": {"id": "leaf_7"},
                    "right": {"id": "leaf_8"},
                },
                "right": {
                    "feature": 17,
                    "threshold": 0.01,
                    "operator": "<=",
                    "left": {"id": "leaf_9"},
                    "right": {"id": "leaf_10"},
                },
            },
            "right": {
                "feature": 0,
                "threshold": 22.85,
                "operator": "<=",
                "left": {"id": "leaf_11"},
                "right": {"id": "leaf_12"},
            },
        },
    },
    "right": {
        "feature": 17,
        "threshold": 2.29,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": 3.02,
            "operator": "<=",
            "left": {
                "feature": 17,
                "threshold": 1.76,
                "operator": "<=",
                "left": {"id": "leaf_13"},
                "right": {"id": "leaf_14"},
            },
            "right": {"id": "leaf_15"},
        },
        "right": {
            "feature": 6,
            "threshold": 1.10,
            "operator": "<=",
            "left": {"id": "leaf_16"},
            "right": {"id": "leaf_17"},
        },
    },
}



tree_full_md10_ml200_5 = {
    "feature": 18,
    "threshold": 0.08,
    "operator": "<=",
    "left": {
        "feature": 17,
        "threshold": 0.56,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -1.25,
            "operator": "<=",
            "left": {
                "feature": 19,
                "threshold": -0.64,
                "operator": "<=",
                "left": {"id": "leaf_1"},  
                "right": {"id": "leaf_2"},
            },
            "right": {
                "feature": 15,
                "threshold": 1.28,
                "operator": "<=",
                "left": {
                    "feature": 7,
                    "threshold": -0.74,
                    "operator": "<=",
                    "left": {"id": "leaf_3"},
                    "right": {
                        "feature": 13,
                        "threshold": 0.20,
                        "operator": "<=",
                        "left": {"id": "leaf_4"},
                        "right": {"id": "leaf_5"},
                    },
                },
                "right": {"id": "leaf_6"},
            },
        },
        "right": {
            "feature": 2,
            "threshold": 0.66,
            "operator": "<=",
            "left": {
                "feature": 8,
                "threshold": -0.47,
                "operator": "<=",
                "left": {"id": "leaf_7"},
                "right": {
                    "feature": 17,
                    "threshold": 0.01,
                    "operator": "<=",
                    "left": {"id": "leaf_8"},
                    "right": {"id": "leaf_9"},
                },
            },
            "right": {
                "feature": 0,
                "threshold": 22.85,
                "operator": "<=",
                "left": {"id": "leaf_10"},
                "right": {"id": "leaf_11"},
            },
        },
    },
    "right": {"id": "leaf_12"},
}



tree_full_md10_ml200_4 = {
    "feature": 18,
    "threshold": 0.08,
    "operator": "<=",
    "left": {
        "feature": 17,
        "threshold": 0.56,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -0.77,
            "operator": "<=",
            "left": {
                "feature": 3,
                "threshold": -0.36,
                "operator": "<=",
                "left": {
                    "feature": 14,
                    "threshold": -0.54,
                    "operator": "<=",
                    "left": {"id": "leaf_1"},
                    "right": {"id": "leaf_2"},
                },
                "right": {
                    "feature": 14,
                    "threshold": 0.76,
                    "operator": "<=",
                    "left": {"id": "leaf_3"},
                    "right": {"id": "leaf_4"},
                },
            },
            "right": {
                "feature": 20,
                "threshold": 1.01,
                "operator": "<=",
                "left": {
                    "feature": 7,
                    "threshold": -0.74,
                    "operator": "<=",
                    "left": {"id": "leaf_5"},
                    "right": {"id": "leaf_6"},
                },
                "right": {
                    "feature": 15,
                    "threshold": 4.81,
                    "operator": "<=",
                    "left": {"id": "leaf_7"},
                    "right": {"id": "leaf_8"},
                },
            },
        },
        "right": {
            "feature": 8,
            "threshold": -0.47,
            "operator": "<=",
            "left": {
                "feature": 16,
                "threshold": 0.44,
                "operator": "<=",
                "left": {"id": "leaf_9"},
                "right": {"id": "leaf_10"},
            },
            "right": {
                "feature": 17,
                "threshold": 0.01,
                "operator": "<=",
                "left": {
                    "feature": 2,
                    "threshold": 0.36,
                    "operator": "<=",
                    "left": {"id": "leaf_11"},
                    "right": {"id": "leaf_12"},
                },
                "right": {
                    "feature": 8,
                    "threshold": 2.64,
                    "operator": "<=",
                    "left": {"id": "leaf_13"},
                    "right": {"id": "leaf_14"},
                },
            },
        },
    },
    "right": {
        "feature": 17,
        "threshold": 2.29,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": 1.30,
            "operator": "<=",
            "left": {
                "feature": 7,
                "threshold": 0.69,
                "operator": "<=",
                "left": {
                    "feature": 14,
                    "threshold": 0.41,
                    "operator": "<=",
                    "left": {"id": "leaf_15"},
                    "right": {"id": "leaf_16"},
                },
                "right": {"id": "leaf_17"},
            },
            "right": {
                "feature": 2,
                "threshold": 1.79,
                "operator": "<=",
                "left": {"id": "leaf_18"},
                "right": {"id": "leaf_19"},
            },
        },
        "right": {
            "feature": 6,
            "threshold": 2.19,
            "operator": "<=",
            "left": {
                "feature": 16,
                "threshold": 1.48,
                "operator": "<=",
                "left": {"id": "leaf_20"},
                "right": {"id": "leaf_21"},
            },
            "right": {
                "feature": 14,
                "threshold": 1.84,
                "operator": "<=",
                "left": {"id": "leaf_22"},
                "right": {"id": "leaf_23"},
            },
        },
    },
}



tree_full_md10_ml200_7 = {
    "feature": 18,
    "threshold": 0.08,
    "operator": "<=",
    "left": {
        "feature": 17,
        "threshold": 0.56,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -0.58,
            "operator": "<=",
            "left": {
                "feature": 15,
                "threshold": -0.29,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {
                    "feature": 7,
                    "threshold": -0.74,
                    "operator": "<=",
                    "left": {"id": "leaf_2"},
                    "right": {"id": "leaf_3"},
                },
            },
            "right": {
                "feature": 4,
                "threshold": 0.13,
                "operator": "<=",
                "left": {"id": "leaf_4"},
                "right": {"id": "leaf_5"},
            },
        },
        "right": {
            "feature": 8,
            "threshold": -0.47,
            "operator": "<=",
            "left": {
                "feature": 3,
                "threshold": -0.15,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"},
            },
            "right": {
                "feature": 14,
                "threshold": -0.53,
                "operator": "<=",
                "left": {"id": "leaf_8"},
                "right": {"id": "leaf_9"},
            },
        },
    },
    "right": {
        "feature": 17,
        "threshold": 2.29,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": 1.30,
            "operator": "<=",
            "left": {
                "feature": 7,
                "threshold": 0.69,
                "operator": "<=",
                "left": {"id": "leaf_10"},
                "right": {"id": "leaf_11"},
            },
            "right": {
                "feature": 5,
                "threshold": 0.94,
                "operator": "<=",
                "left": {"id": "leaf_12"},
                "right": {"id": "leaf_13"},
            },
        },
        "right": {
            "feature": 6,
            "threshold": 2.19,
            "operator": "<=",
            "left": {
                "feature": 3,
                "threshold": 0.48,
                "operator": "<=",
                "left": {"id": "leaf_14"},
                "right": {"id": "leaf_15"},
            },
            "right": {
                "feature": 16,
                "threshold": 3.13,
                "operator": "<=",
                "left": {"id": "leaf_16"},
                "right": {"id": "leaf_17"},
            },
        },
    },
}



tree_full_md10_ml200_8 = {
    "feature": 18,
    "threshold": 0.08,
    "operator": "<=",
    "left": {
        "feature": 17,
        "threshold": -0.30,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -1.22,
            "operator": "<=",
            "left": {
                "feature": 14,
                "threshold": -0.54,
                "operator": "<=",
                "left": {"id": "leaf_1"},
                "right": {"id": "leaf_2"}
            },
            "right": {
                "feature": 15,
                "threshold": -0.48,
                "operator": "<=",
                "left": {"id": "leaf_3"},
                "right": {
                    "feature": 3,
                    "threshold": -0.64,
                    "operator": "<=",
                    "left": {"id": "leaf_4"},
                    "right": {"id": "leaf_5"}
                }
            }
        },
        "right": {
            "feature": 8,
            "threshold": -0.47,
            "operator": "<=",
            "left": {
                "feature": 15,
                "threshold": 4.22,
                "operator": "<=",
                "left": {"id": "leaf_6"},
                "right": {"id": "leaf_7"}
            },
            "right": {
                "feature": 17,
                "threshold": 0.01,
                "operator": "<=",
                "left": {"id": "leaf_8"},
                "right": {
                    "feature": 16,
                    "threshold": 0.87,
                    "operator": "<=",
                    "left": {"id": "leaf_9"},
                    "right": {"id": "leaf_10"}
                }
            }
        }
    },
    "right": {
        "feature": 17,
        "threshold": 2.29,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": 3.02,
            "operator": "<=",
            "left": {
                "feature": 1,
                "threshold": -0.19,
                "operator": "<=",
                "left": {"id": "leaf_11"},
                "right": {"id": "leaf_12"}
            },
            "right": {
                "feature": 15,
                "threshold": -0.09,
                "operator": "<=",
                "left": {"id": "leaf_13"},
                "right": {"id": "leaf_14"}
            }
        },
        "right": {
            "feature": 7,
            "threshold": 0.97,
            "operator": "<=",
            "left": {"id": "leaf_15"},
            "right": {"id": "leaf_16"},
        },
    }
}



tree_full_md10_ml200_6 = {
    "feature": 18,
    "threshold": 0.08,
    "operator": "<=",
    "left": {
        "feature": 17,
        "threshold": -0.30,
        "operator": "<=",
        "left": {
            "feature": 2,
            "threshold": -1.25,
            "operator": "<=",
            "left": {"id": "leaf_1"},
            "right": {
                "feature": 14,
                "threshold": -0.54,
                "operator": "<=",
                "left": {"id": "leaf_2"},
                "right": {"id": "leaf_3"},
            },
        },
        "right": {
            "feature": 15,
            "threshold": -0.48,
            "operator": "<=",
            "left": {
                "feature": 3,
                "threshold": -0.64,
                "operator": "<=",
                "left": {"id": "leaf_4"},
                "right": {
                    "feature": 20,
                    "threshold": 1.02,
                    "operator": "<=",
                    "left": {"id": "leaf_5"},
                    "right": {"id": "leaf_6"},
                },
            },
            "right": {
                "feature": 2,
                "threshold": 0.46,
                "operator": "<=",
                "left": {"id": "leaf_7"},
                "right": {"id": "leaf_8"},
            },
        },
    },
    "right": {
        "feature": 20,
        "threshold": 0.97,
        "operator": "<=",
        "left": {
            "feature": 17,
            "threshold": 1.12,
            "operator": "<=",
            "left": {
                "feature": 2,
                "threshold": 1.30,
                "operator": "<=",
                "left": {"id": "leaf_9"},
                "right": {
                    "feature": 18,
                    "threshold": -0.15,
                    "operator": "<=",
                    "left": {"id": "leaf_10"},
                    "right": {"id": "leaf_11"},
                },
            },
            "right": {
                "feature": 6,
                "threshold": 1.69,
                "operator": "<=",
                "left": {"id": "leaf_12"},
                "right": {"id": "leaf_13"},
            },
        },
        "right": {
            "feature": 16,
            "threshold": 1.20,
            "operator": "<=",
            "left": {
                "feature": 15,
                "threshold": 0.93,
                "operator": "<=",
                "left": {"id": "leaf_14"},
                "right": {"id": "leaf_15"},
            },
            "right": {"id": "leaf_16"},
        },
    },
}


