#!/bin/bash

# Define the list of mutations
mutations=(
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

# Iterate over the list of mutations
for mutation in "${mutations[@]}"
do
  # Create a unique sbatch script for each mutation
  sbatch_script="#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/lenet/k-score/test_weak/${mutation}_%j.out
#SBATCH --error=./Output/lenet/k-score/test_weak/${mutation}_%j.err  # Standard error log
#SBATCH --job-name=le_k_tw_${mutation}
#SBATCH --time=4-00:00:00              # Run time (D-HH:MM:SS)
#SBATCH --ntasks=15

module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/lenet/k-score/test_weak/${mutation}.yaml --properties ./properties/lenet/properties.py --constants ./properties/lenet/constants.py
"

  # Save the sbatch script to a temporary file
  echo "$sbatch_script" > temp_${mutation}.sh
  
  # Submit the sbatch script
  sbatch temp_${mutation}.sh
  
  # Optionally remove the temporary sbatch script
  rm temp_${mutation}.sh
done
