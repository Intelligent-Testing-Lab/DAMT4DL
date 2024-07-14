#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/mnist/test/k-score/bs.out
#SBATCH --error=./Output/mnist/test/k-score/bs.err  # Standard error log
#SBATCH --ntasks=10  # Specify a number of tasks for your job
#SBATCH --job-name=mn_te_bs

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/mnist/k-score/mnist_test_bs.yaml --properties ./properties/mnist/properties.py --constants ./properties/mnist/constants.py
