from execution.execute_original import execute_original_model
from execution.execute_mutant import execute_mutants_MO
from utils import gen_path_name
from execution.execution_utils import *
import os



def execute_models(config):
    is_original_exucted = False
    # execute the mutants
    print("Executing mutants for each mutation operator")
    original_scores = []
    for mutation in config.mutations:
        # full path
        full_path = gen_path_name.gen_full_path('results', config, mutation)

        # mutant weights path
        mutant_weights_path = gen_path_name.gen_mutant_weights_path('results', config, mutation)

        # execute the original model, only once
        if is_original_exucted == False:
            original_scores = execute_original_model(full_path, config)
            is_original_exucted = True
        else:
            # save the scores of the original model
            scores_file_path = os.path.join(full_path, 'original_scores.csv') # save the scores of the original model
            if not(os.path.isfile(scores_file_path)):
                save_scores_csv(original_scores, scores_file_path)
           
        # execute the mutants for each mutation operator
        execute_mutants_MO(full_path, mutation, mutant_weights_path)
