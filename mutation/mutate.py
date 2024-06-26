import os

from utils import constants, gen_path_name
from mutation import prepare

def mutate_model(config):
    # Set up the paths
    mutants_path = constants.save_paths['mutated']
    prepared_path = constants.save_paths['prepared']

    # prepare the original model code and save it 
    full_prepared_path = gen_path_name.gen_prepare_directory_path(prepared_path, config)
    save_path_prepared = os.path.join(full_prepared_path, 'prepared.py')
    prepare.prepare_model(config.original_path, save_path_prepared)
    
    # Generate the mutated models
    for mutation in config.mutations:
        full_mutants_path = gen_path_name.gen_mutant_directory_path(mutants_path, config, mutation)
     