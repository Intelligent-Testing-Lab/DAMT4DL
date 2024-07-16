#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/udacity/test/exhaustive_none_%j.out
#SBATCH --error=./Output/udacity/test/exhaustive_none_%j.err  # Standard error log
#SBATCH --ntasks=15  # Specify a number of tasks for the array
#SBATCH --job-name=ud_te_ex_no

module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/udacity/k-score/udacity_test_ex_no.yaml --properties ./properties/udacity/properties.py --constants ./properties/udacity/constants.py