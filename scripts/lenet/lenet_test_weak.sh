#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 5 gigabytes of real memory (mem)
#SBATCH --output=./Output/lenet_test_weak.txt  # This is where your output and errors are logged
#SBATCH --job-name=le_D_tw

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/lenet/k-score/lenet_test_weak.yaml --properties ./properties/lenet/properties_test.py --constants ./properties/lenet/constants_test.py
