#!/bin/bash

# Define the list of mutations
mutations=("change_label" "delete_training_data" "unbalance_train_data" "make_output_classes_overlap"
           "change_batch_size" "change_learning_rate" "change_epochs" "disable_batching"
           "change_loss_function" "change_optimisation_function" "remove_validation_set")

# Iterate over the list of mutations
for mutation in "${mutations[@]}"
do
  # Create a unique sbatch script for each mutation
  sbatch_script="#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/movie/k-score/train/${mutation}_%j.out
#SBATCH --error=./Output/movie/k-score/train/${mutation}_%j.err  # Standard error log
#SBATCH --job-name=mv_k_tr_${mutation}
#SBATCH --time=4-00:00:00              # Run time (D-HH:MM:SS)

module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/movie/k-score/train/${mutation}.yaml --properties ./properties/movie/properties.py --constants ./properties/movie/constants.py
"

  # Save the sbatch script to a temporary file
  echo "$sbatch_script" > temp_${mutation}.sh
  
  # Submit the sbatch script
  sbatch temp_${mutation}.sh
  
  # Optionally remove the temporary sbatch script
  rm temp_${mutation}.sh
done
