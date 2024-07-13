#!/bin/bash
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/mnist/test/k-score/ex_no.out
#SBATCH --error=./Output/mnist/test/k-score/ex_no.err  # Standard error log
#SBATCH --tasks-per-node=1  # Specify the number of tasks on each node
#SBATCH --job-name=mn_te_ex_no

#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1

module load CUDA/10.1.243  # Load the available CUDA module
module load cuDNN/7.6.2.24-CUDA-10.1.243  # Load the compatible cuDNN module
module load Anaconda3/2022.05

# Set up environment variables
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.1/lib64
export PATH=$PATH:/usr/local/cuda-10.1/bin
export TF_CPP_MIN_LOG_LEVEL=0 # TODO delete


source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/mnist/k-score/mnist_test_ex_no.yaml --properties ./properties/mnist/properties.py --constants ./properties/mnist/constants.py
