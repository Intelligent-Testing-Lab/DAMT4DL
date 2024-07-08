#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 5 gigabytes of real memory (mem)
#SBATCH --output=./Output/movie_test.txt  # This is where your output and errors are logged
#SBATCH --job-name=mv_D_te

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/movie/k-score/movie_test.yaml --properties ./properties/movie/properties_test.py --constants ./properties/movie/constants_test.py