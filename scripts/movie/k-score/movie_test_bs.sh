#!/bin/bash
#SBATCH --nodes=10  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/movie/test/binaryS.out
#SBATCH --error=./Output/movie/test/binaryS.err  # Standard error log
#SBATCH --tasks-per-node=1  # Specify the number of tasks on each node

#SBATCH --job-name=mv_te_bs

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/movie/k-score/movie_test_bs.yaml --properties ./properties/movie/properties.py --constants ./properties/movie/constants.py