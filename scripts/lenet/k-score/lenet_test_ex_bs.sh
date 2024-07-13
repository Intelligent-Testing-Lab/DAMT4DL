#!/bin/bash
#SBATCH --nodes=10  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/lenet/test/k-score/bs.out
#SBATCH --error=./Output/lenet/test/k-score/bs.err  # Standard error log
#SBATCH --tasks-per-node=1  # Specify the number of tasks on each node
#SBATCH --job-name=le_te_bs

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/lenet/k-score/lenet_test_bs.yaml --properties ./properties/lenet/properties.py --constants ./properties/lenet/constants.py