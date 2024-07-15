#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/audio/test/k-score/bs.out
#SBATCH --error=./Output/audio/test/k-score/bs.err  # Standard error log
#SBATCH --ntasks=15  # Specify a number of tasks for the array
#SBATCH --job-name=au_te_bs

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/audio/k-score/audio_test_bs.yaml --properties ./properties/audio/properties.py --constants ./properties/audio/constants.py