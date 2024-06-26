import os

from utils import constants, gen_path_name
from mutation import prepare

def mutate_model(config):
    # Get the configuration parameters
    mutations = config['data']['mutations']
    subject_name = config['data']['subject_name']
    original_path = config['data']['original_path']
    mutants_path = constants.save_paths['mutated']
    prepared_path = constants.save_paths['prepared']


    # prepare the original model code and save it 
    save_path_prepared = gen_path_name.gen_prepare_path_name(prepared_path, subject_name)
    prepare.prepare_model(original_path, save_path_prepared)
    
    # Generate the mutated models
    for mutation in mutations:
        save_path_mutated = gen_path_name.gen_mutant_path_name(mutants_path, subject_name, mutation)
     