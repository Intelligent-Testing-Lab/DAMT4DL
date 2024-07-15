#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/lenet/test/k-score/ex_no.out
#SBATCH --error=./Output/lenet/test/k-score/ex_no.err  # Standard error log
#SBATCH --ntasks=15  # Specify the number of tasks
#SBATCH --job-name=le_te_ex_no

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/lenet/k-score/lenet_test_ex_no.yaml --properties ./properties/lenet/properties.py --constants ./properties/lenet/constants.py