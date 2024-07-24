#!bin/bash

# Muatations for each task
mnist_mutations=(
    "change_epochs"
    "change_label"
    "delete_training_data"
    "unbalance_train_data"
    "add_noise"
    "make_output_classes_overlap"
    "change_batch_size"
    "change_learning_rate"
    "remove_activation_function"
    "add_weights_regularisation"
    "change_dropout_rate"
    "change_weights_initialisation"
    "remove_bias"
    "change_loss_function"
    "change_optimisation_function"
    "remove_validation_set"
)

movie_mutations=("change_label" "delete_training_data" "unbalance_train_data" "make_output_classes_overlap"
           "change_batch_size" "change_learning_rate" "change_epochs" "disable_batching"
           "change_loss_function" "change_optimisation_function" "remove_validation_set")

audio_mutations=(
    "change_label"
    "delete_training_data"
    "unbalance_train_data"
    "make_output_classes_overlap"
    "change_learning_rate"
    "change_epochs"
    "change_activation_function"
    "remove_activation_function"
    "add_activation_function"
    "add_weights_regularisation"
    "change_weights_initialisation"
    "remove_bias"
    "change_loss_function"
    "change_optimisation_function"
    "remove_validation_set"
    "change_earlystopping_patience"
)

udacity_mutations=(
    "change_label"
    "delete_training_data"
    "unbalance_train_data"
    "make_output_classes_overlap"
    "change_learning_rate"
    "change_epochs"
    "change_activation_function"
    "remove_activation_function"
    "add_weights_regularisation"
    "change_dropout_rate"
    "change_weights_initialisation"
    "remove_bias"
    "change_loss_function"
    "change_optimisation_function"
    "remove_validation_set"
)

lenet_mutations=(
    "remove_validation_set"
    "change_optimisation_function"
    "change_loss_function"
    "remove_activation_function"
    "remove_bias"
    "add_weights_regularisation"
    "add_activation_function"
    "change_activation_function"
    "change_weights_initialisation"
    "change_epochs"
    "change_batch_size"
    "change_learning_rate"
    "delete_training_data"
    "add_noise"
    "unbalance_train_data"
    "make_output_classes_overlap"
    "change_label"
)
