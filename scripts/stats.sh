#!bin/bash

source ./scripts/tasks_properities.sh


# Get the mutations based on the task
get_mutations() {
    local task=$1
    local mutations=()
    if [ $task == "mnist" ]; then
        mutations=("${mnist_mutations[@]}")
    elif [ $task == "movie" ]; then
        mutations=("${movie_mutations[@]}")
    elif [ $task == "audio" ]; then
        mutations=("${audio_mutations[@]}")
    elif [ $task == "udacity" ]; then
        mutations=("${udacity_mutations[@]}")
    elif [ $task == "lenet" ]; then
        mutations=("${lenet_mutations[@]}")
    fi
    echo "${mutations[@]}"
}

# do the stats analysis
stats_analysis() {
    local task=$1
    local criterion=$2
    local mode=$3
    local mutation=$4
    local model_type=$5
    local statistical_test=$6

    # Create a unique sbatch script for each mutation
    sbatch_script="#!/bin/bash
#SBATCH --nodes=1  # Specify a number of nodes
#SBATCH --mem=30G  # Request 30 gigabytes of real memory (mem)
#SBATCH --output=./Output/${task}/${criterion}/${mode}/stats/${mutation}_%j.out
#SBATCH --error=./Output/${task}/${criterion}/${mode}/stats/${mutation}_%j.err
#SBATCH --job-name=S${task:0:2}_${criterion:0:1}_${mode:0:2}_${mutation}
#SBATCH --time=4-00:00:00  # Run time (D-HH:MM:SS)
#SBATCH --ntasks=1

module load Anaconda3/2022.05

source activate deepcrime

export PYTHONPATH=$(pwd)
python ./analyse/stats_analysis.py --config ./config_file/${task}/${criterion}/${mode}/${mutation}.yaml --model_type $model_type --statistical_test $statistical_test
"
    # Save the sbatch script to a temporary file
    echo "$sbatch_script" > temp_${mutation}.sh
    
    # Submit the sbatch script
    sbatch temp_${mutation}.sh
    
    # Optionally remove the temporary sbatch script
    rm temp_${mutation}.sh
}



# Constants Definitions
tasks=("mnist" "movie" "audio" "udacity"  "lenet") # The tasks to be analysed
criterions=("k-score" "d-score") # The criterions to be analysed
modes=("test" "train" "test_weak") # The modes to be analysed

for task in "${tasks[@]}"
do
    for criterion in "${criterions[@]}"
    do
        for mode in "${modes[@]}"
        do
            if [ "$task" == "movie" ] && [ "$mode" == "test_weak" ]; then
                continue
            fi  
            # Capture the returned mutations into an array
            IFS=' ' read -r -a mutations <<< "$(get_mutations "$task")"

            # Get the model type and statistical test for the task
            model_type=$(eval echo "\$${task}_model_type")
            statistical_test=$(eval echo "\$${task}_statistical_test")


            for mutation in "${mutations[@]}"
            do
                stats_analysis "$task" "$criterion" "$mode" "$mutation" "$model_type" "$statistical_test"
            done
        done
    done
done
