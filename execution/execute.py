import os

from execution.execute_original import execute_original_model
from execution.execute_mutant import execute_mutants
from utils import constants, gen_path_name



def execute_models(config):
    # read the save path of the prepared model, mutants and original model
    mutants_path = constants.save_paths['mutated']
    prepared_path = constants.save_paths['prepared']
    origianl_path = constants.save_paths['original']

    # orginal model path
    full_original_path = gen_path_name.gen_original_directory_path(origianl_path, config)

    # execute the original model
    execute_original_model(full_original_path)

    
    # prepared model path
    full_prepared_path = gen_path_name.gen_prepare_directory_path(prepared_path, config)
    save_path_prepared = os.path.join(full_prepared_path, 'prepared.py')

    # mutants path
    for mutation in config.mutations:
        full_mutants_path = os.path.join(gen_path_name.gen_mutant_directory_path(mutants_path, config, mutation), 'mutated')
        mutant_stats_path = os.path.join(full_mutants_path, 'stats')

        # execute the mutants for each mutation operator
        execute_mutants(full_mutants_path)

   



