#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 5 gigabytes of real memory (mem)
#SBATCH --output=./Output/mnist_train.txt  # This is where your output and errors are logged
#SBATCH --job-name=mn_D_tr

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/mnist/k-score/mnist_train.yaml --properties ./properties/mnist/properties_test.py --constants ./properties/mnist/constants_test.py