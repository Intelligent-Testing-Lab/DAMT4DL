import os

from execution.execute_original import execute_original_model
from execution.execute_mutant import execute_mutants_MO
from utils import gen_path_name



def execute_models(config):
    is_original_exucted = False
    # execute the mutants
    print("Executing mutants for each mutation operator")
    for mutation in config.mutations:
        # full path
        full_path = gen_path_name.gen_full_path('results', config, mutation)

        # mutant weights path
        mutant_weights_path = gen_path_name.gen_mutant_weights_path('results', config, mutation)

        # execute the original model, only once
        if not is_original_exucted:
            execute_original_model(full_path, config)
            s_original_exucted = True

        # execute the mutants for each mutation operator
        execute_mutants_MO(full_path, mutation, mutant_weights_path)



