#!/bin/bash

# Define the mutations array without commas
mutations=(
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

# Iterate over the list of mutations
for mutation in "${mutations[@]}"
do
  # Create a unique sbatch script for each mutation
  sbatch_script="#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/mnist/k-score/test/${mutation}_%j.out
#SBATCH --error=./Output/mnist/k-score/test/${mutation}_%j.err  # Standard error log
#SBATCH --job-name=mn_k_te_${mutation}
#SBATCH --time=4-00:00:00              # Run time (D-HH:MM:SS)

module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/mnist/k-score/test/${mutation}.yaml --properties ./properties/mnist/properties.py --constants ./properties/mnist/constants.py
"

  # Save the sbatch script to a temporary file
  echo "$sbatch_script" > temp_${mutation}.sh
  
  # Submit the sbatch script
  sbatch temp_${mutation}.sh
  
  # Optionally remove the temporary sbatch script
  rm temp_${mutation}.sh
done
