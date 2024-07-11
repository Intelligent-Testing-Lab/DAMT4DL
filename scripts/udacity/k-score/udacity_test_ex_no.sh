#!/bin/bash
#SBATCH --nodes=10  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/udacity/test/exhaustive_none.out
#SBATCH --error=./Output/udacity/test/exhaustive_none.err  # Standard error log
#SBATCH --tasks-per-node=1  # Specify the number of tasks on each node
#SBATCH --job-name=ud_te_ex_no

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/udacity/k-score/udacity_test_ex_no.yaml --properties ./properties/udacity/properties.py --constants ./properties/udacity/constants.py