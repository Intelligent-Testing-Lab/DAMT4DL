#!/bin/bash
#SBATCH --nodes=1 # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/movie/test/exhaustive_none.out
#SBATCH --error=./Output/movie/test/exhaustive_none.err  # Standard error log
#SBATCH --ntasks=10  # Specify the number of tasks on each node
#SBATCH --job-name=d_mv_te

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC
export TF_CPP_MIN_LOG_LEVEL=0 # TODO delete

export PYTHONPATH=$(pwd)
python ./analyse/stats_analysis.py --config ./config_file/movie/d-score/movie_test.yaml