#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 5 gigabytes of real memory (mem)
#SBATCH --output=./Output/movie/mutation_scores/d_score_origianl_%j.out  # Standard output and error log
#SBATCH --error=./Output/movie/mutation_scores/d_score_original_%j.err  # Standard error log
#SBATCH --job-name=d_mv_ms_o

module load Anaconda3/2022.05

source activate deepcrime # using HPC

python ./analyse/mutation_scores.py --config ./config_file/movie/mutation_scores/movie_d_score_original.yaml