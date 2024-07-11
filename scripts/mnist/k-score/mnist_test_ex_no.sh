#!/bin/bash
#SBATCH --nodes=10  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/mnist/test/k-score/ex_no.out
#SBATCH --error=./Output/mnist/test/k-score/ex_no.err  # Standard error log
#SBATCH --tasks-per-node=1  # Specify the number of tasks on each node
#SBATCH --job-name=mn_te_ex_no

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/mnist/k-score/mnist_test_ex_no.yaml --properties ./properties/mnist/properties.py --constants ./properties/mnist/constants.py
