# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

###
# udp = user_defined_params
# pct = percentage
# lbl = label
###
# Training Data Mutations
###
model_name = ""
model_type = "regression"
statistical_test = "GLM"
MS = "DC_MS"

model_properties = {
    "epochs": 50,
    "batch_size": 64,
    "learning_rate": 0.0001,
    "x_train_len": 9792,
    "layers_num": 12,
    "dropout_layers": {6}
}

# Mutation Change label
change_label = {
    "name": 'change_label',
    "change_label_udp": False,
    "change_label_pct": -1,
    "change_label_label": None,
    "runs_number": 20,
    "annotation_params": ["y_train"],
    "bs_lower_bound": 0,
    "bs_upper_bound": 100,
    "precision": 5,
    "search_type": 'exhaustive',
    "bs_rounding_type": 'float'
}
# change_label_udp = False
# change_label_pct = -1
# change_label_label = None

# Mutation Delete Training Data
delete_training_data = {
    "name": 'delete_td',
    "delete_train_data_udp": False,
    "delete_train_data_pct": -1,
    "runs_number": 20,
    "annotation_params": ["x_train", "y_train"],
    "bs_lower_bound": 0,
    "bs_upper_bound": 99,
    "precision": 5,
    "search_type": 'exhaustive',
    "bs_rounding_type": 'float'
}
# delete_train_data_udp = False
# delete_train_data_pct = -1

# Unbalance Training Data
unbalance_train_data = {
    "name": 'unbalance_td',
    "unbalance_train_data_udp": False,
    "unbalance_train_data_pct": -1,
    "runs_number": 20,
    "annotation_params": ["x_train", "y_train"],
    "bs_lower_bound": 0,
    "bs_upper_bound": 100,
    "precision": 5,
    "search_type": 'exhaustive',
    "bs_rounding_type": 'float'
}

make_output_classes_overlap = {
    "name": 'output_classes_overlap',
    "make_output_classes_overlap_udp": False,
    "make_output_classes_overlap_pct": -1,
    "runs_number": 20,
    "annotation_params": ["x_train", "y_train"],
    "bs_lower_bound": 0,
    "bs_upper_bound": 100,
    "precision": 5,
    "search_type": 'exhaustive',
    "bs_rounding_type": 'float'
}

# Add Noise to Training Data
add_noise = {
    "name": 'add_noise',
    "add_noise_udp": False,
    "add_noise_pct": -1,
    "runs_number": 20,
    "annotation_params": ["x_train"],
    "bs_lower_bound": 0,
    "bs_upper_bound": 100,
    "search_type": 'binary',
     "precision": 5,
     "bs_rounding_type": 'float'
}

change_epochs = {
    "name": 'change_epochs',
    "change_epochs_size": False,
    "pct": 50,
    "bs_lower_bound": 50,
    "bs_upper_bound": 1,
    "bs_rounding_type": 'int',
    "annotation_params": [],
    "search_type": 'exhaustive',
    "precision": 5,
    "runs_number": 20,
}

change_batch_size = {
    "name": 'change_batch_size',
    "runs_number": 20,
    "change_batch_size_udp": False,
    "batch_size": -1,
    "annotation_params": [],
    "search_type": 'exhaustive',
    "applicable": True
}

change_learning_rate = {
    "name": 'change_learning_rate',
    "learning_rate_udp": False,
    "pct": -1,
    "bs_lower_bound": 0.0001,
    "bs_upper_bound": 0.00001,
    "annotation_params": [],
    "search_type": 'exhaustive',
    "runs_number": 20,
    "precision": 0.00001,
    "bs_rounding_type": 'float5'
}

disable_batching = {
    "name": 'disable_batching',
    "train_size": 9792,
    "annotation_params": [],
    "search_type": None,
    "runs_number": 20,
    "applicable": True
}

change_activation_function = {
    "name": 'change_activation_function',
    "activation_function_udp": False,
    "layer_udp": 4,
    "runs_number": 20,
    "annotation_params": [],
    "layer_mutation": True,
    "current_index": 0,
    "mutation_target": None,
    "search_type": 'exhaustive'
}

remove_activation_function = {
    "name": 'remove_activation_function',
    "layer_udp": None,
    "runs_number": 20,
    "annotation_params": [],
    "layer_mutation": True,
    "current_index": 0,
    "mutation_target": None,
    "search_type": None
}

add_activation_function = {
    "name": 'add_activation_function',
    "activation_function_udp": None,
    "layer_udp": None,
    "runs_number": 20,
    "annotation_params": [],
    "layer_mutation": True,
    "current_index": 0,
    "mutation_target": None,
    "search_type": 'exhaustive'
}

change_weights_initialisation = {
    "name": 'change_weights_initialisation',
    "weights_initialisation_udp": None,
    "layer_udp": 3,
    "annotation_params": [],
    "runs_number": 20,
    "current_index": 0,
    "layer_mutation": True,
    "search_type": 'exhaustive'
}

change_optimisation_function = {
    "optimisation_function_udp": False,
    "annotation_params": [],
    "mutation_target": None,
    "runs_number": 20,
    "layer_mutation": False,
    "search_type": 'exhaustive',
    "name": 'change_optimisation_function',
}

remove_validation_set = {
    "name": 'remove_validation_set',
    "runs_number": 20,
    "annotation_params": [],
    "search_type": None
}

change_gradient_clip = {
    "change_gradient_clip_udp": False,
    "clipnorm": -1,
    "bs_lower_bound": 0,
    "bs_upper_bound": 0,
    "clipvalue": 0.5,
    # "bs_lower_bound1": 0,
    # "bs_upper_bound1": 0,
    "annotation_params": [],
    "search_type": None
}

add_bias = {
    "name": 'add_bias',
    "layer_udp": None,
    "runs_number": 20,
    "annotation_params": [],
    "layer_mutation": True,
    "current_index": 0,
    "mutation_target": None,
    "search_type": None
}

remove_bias = {
    "name": 'remove_bias',
    "layer_udp": None,
    "runs_number": 20,
    "annotation_params": [],
    "layer_mutation": True,
    "current_index": 0,
    "mutation_target": None,
    "search_type": None
}

change_loss_function = {
    "name": 'change_loss_function',
    "loss_function_udp": None,
    "runs_number": 20,
    "annotation_params": [],
    "mutation_target": None,
    "search_type": 'exhaustive',
    "layer_mutation": False
}

change_dropout_rate = {
    "name": 'change_dropout_rate',
    "layer_udp": 6,
    "runs_number": 20,
    "dropout_rate_udp": False,
    "annotation_params": [],
    "rate": 0,
    "current_index": 0,
    "layer_mutation": True,
    "search_type": 'exhaustive'
}

add_weights_regularisation = {
    "name": 'add_weights_regularisation',
    "weights_regularisation_udp": None,
    "layer_udp": 3,
    "runs_number": 20,
    "annotation_params": [],
    "layer_mutation": True,
    "current_index": 0,
    "mutation_target": None,
    "search_type": 'exhaustive'
}

change_weights_regularisation = {
    "name": 'change_weights_regularisation',
    "weights_regularisation_udp": None,
    "layer_udp": None,
    "runs_number": 20,
    "annotation_params": [],
    "layer_mutation": True,
    "current_index": 0,
    "mutation_target": None,
    "search_type": None
}

remove_weights_regularisation = {
    "name": 'remove_weights_regularisation',
    "layer_udp": None,
    "runs_number": 20,
    "annotation_params": [],
    "layer_mutation": True,
    "current_index": 0,
    "search_type": 'exhaustive'
}

change_earlystopping_patience = {
    "name": "change_patience",
    "runs_number": 20,
    "patience_udp": None,
    "annotation_params": [],
    "layer_mutation": False,
    "bs_lower_bound": 10,
    "bs_upper_bound": 1,
    "pct": 1,
    "search_type": 'binary'
}