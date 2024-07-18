#!/bin/bash
#SBATCH --nodes=1 # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/movie/test/d-score/stats_analysis_test_%j.out  # Standard output log
#SBATCH --error=./Output/movie/test/d-score/stats_analysis_test_%j.err  # Standard error log
#SBATCH --job-name=d_mv_stats_te

module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./analyse/stats_analysis.py --config ./config_file/movie/d-score/movie_test.yaml