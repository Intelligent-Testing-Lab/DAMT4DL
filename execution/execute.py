import os

from execution.execute_original import execute_original_model
from execution.execute_mutant import execute_mutants_MO
from utils import constants, gen_path_name



def execute_models(config):
    # read the save path of the prepared model, mutants and original model
    mutants_path = constants.save_paths['mutated']
    origianl_path = constants.save_paths['original']

    # orginal model path
    full_original_path = gen_path_name.gen_original_directory_path(origianl_path, config)

    # execute the original model
    execute_original_model(full_original_path)

    for mutation in config.mutations:
        # mutants path
        full_mutants_path = os.path.join(gen_path_name.gen_mutant_directory_path(mutants_path, config, mutation), 'mutated') 

        # execute the mutants for each mutation operator
        execute_mutants_MO(full_mutants_path, mutation, full_original_path)



