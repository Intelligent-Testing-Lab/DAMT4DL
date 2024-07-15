#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/udacity/test/bs.out
#SBATCH --error=./Output/udacity/test/bs.err  # Standard error log
#SBATCH --ntasks=15  # Specify a number of tasks for the array
#SBATCH --job-name=ud_te_bs

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/udacity/k-score/udacity_test_bs.yaml --properties ./properties/udacity/properties.py --constants ./properties/udacity/constants.py