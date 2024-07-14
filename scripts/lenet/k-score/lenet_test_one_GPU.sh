#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/lenet/test/k-score/one_GPU.out
#SBATCH --error=./Output/lenet/test/k-score/one_GPU.err  # Standard error log
#SBATCH --tasks-per-node=1  # Specify the number of tasks on each node
#SBATCH --job-name=le_te_1

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

source activate deepcrime

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/lenet/k-score/lenet_test_one.yaml --properties ./properties/lenet/properties.py --constants ./properties/lenet/constants.py