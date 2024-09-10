#!/bin/bash

# Define the mutations array without commas
mutations=(
    "change_epochs"
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
#SBATCH --ntasks=15

module load Anaconda3/2019.07

source activate zzc_test1 # using HPC

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
