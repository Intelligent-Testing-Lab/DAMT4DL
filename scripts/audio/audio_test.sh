#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 5 gigabytes of real memory (mem)
#SBATCH --output=./Output/audio_test.txt  # This is where your output and errors are logged
#SBATCH --job-name=au_D_te

module load Java/17.0.4
module load Anaconda3/2022.05

source activate deepcrime # using HPC

export PYTHONPATH=$(pwd)
python ./cmd/main.py --config ./config_file/audio/k-score/audio_test.yaml --properties ./properties/audio/properties_test.py --constants ./properties/audio/constants_test.py