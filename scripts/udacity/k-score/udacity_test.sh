#!/bin/bash

# Define the list of mutations
mutations=("change_label", "delete_training_data", "unbalance_train_data", "make_output_classes_overlap",
                      "change_learning_rate", "change_epochs", "change_activation_function",
                      "remove_activation_function", "add_weights_regularisation", "change_dropout_rate",
                      "change_weights_initialisation", "remove_bias", "change_loss_function",
                      "change_optimisation_function", "remove_validation_set")

# Iterate over the list of mutations
for mutation in "${mutations[@]}"
do
  # Create a unique sbatch script for each mutation
  sbatch_script="#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/udacity/k-score/test/${mutation}_%j.out
#SBATCH --error=./Output/udacity/k-score/test/${mutation}_%j.err  # Standard error log
#SBATCH --job-name=ud_k_te_${mutation}

module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/udacity/k-score/test/${mutation}.yaml --properties ./properties/udacity/properties.py --constants ./properties/udacity/constants.py
"

  # Save the sbatch script to a temporary file
  echo "$sbatch_script" > temp_${mutation}.sh
  
  # Submit the sbatch script
  sbatch temp_${mutation}.sh
  
  # Optionally remove the temporary sbatch script
  rm temp_${mutation}.sh
done
