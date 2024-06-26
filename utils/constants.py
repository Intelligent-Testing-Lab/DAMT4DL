###
# the results of the experiment are saved in the following paths
###
save_paths = {
    "trained": "results/trained_models", # the path to save the trained models
    "mutated": "results/mutated_models", # the path to save the mutated programs
    "prepared": "results/prepared_models" # the path to save the prepared original program
}

###
# the name of python file 
###
file_name = {
    "prepared": "prepared.py",
    "mutated": "muated%d.py",
}

###
# Operators lib
###
operator_mod = "operators"
operator_lib = ["activation_function_operators",
                "training_data_operators",
                "bias_operators",
                "weights_operators",
                "optimiser_operators",
                "dropout_operators,"
                "hyperparams_operators",
                "training_process_operators",
                "loss_operators"]