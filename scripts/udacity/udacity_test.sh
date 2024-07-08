#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 5 gigabytes of real memory (mem)
#SBATCH --output=./Output/udacity_test.txt  # This is where your output and errors are logged
#SBATCH --job-name=ud_D_te

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/udacity/k-score/udacity_test.yaml --properties ./properties/udacity/properties_test.py --constants ./properties/udacity/constants_test.py