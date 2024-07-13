#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/udacity/test/exhaustive_none_GPU.out
#SBATCH --error=./Output/udacity/test/exhaustive_none_GPU.err  # Standard error log
#SBATCH --tasks-per-node=1  # Specify the number of tasks on each node
#SBATCH --job-name=ud_te_ex_no

#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1

module load CUDA/10.1.243  # Load the available CUDA module
module load cuDNN/7.6.2.24-CUDA-10.1.243  # Load the compatible cuDNN module

# Set up environment variables
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.1/lib64
export PATH=$PATH:/usr/local/cuda-10.1/bin

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/udacity/k-score/udacity_test_ex_no.yaml --properties ./properties/udacity/properties.py --constants ./properties/udacity/constants.py