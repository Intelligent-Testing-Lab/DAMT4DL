import os
import logging
import mutation.mutations as mutations

from utils import constants, gen_path_name
from mutation.mutations import *
from mutation.prepare import *

def mutate_model(config):
    # Set up the paths
    mutants_path = constants.save_paths['mutated']
    prepared_path = constants.save_paths['prepared']

    # prepare the original model code and save it 
    full_prepared_path = gen_path_name.gen_prepare_directory_path(prepared_path, config)
    save_path_prepared = os.path.join(full_prepared_path, 'prepared.py')
    prepare_model(config.original_path, save_path_prepared)
    
    # Generate the mutated models
    for mutation in config.mutations:
        full_mutants_path = os.path.join(gen_path_name.gen_mutant_directory_path(mutants_path, config, mutation), 'mutated')
        try:
            mutationClass = create_mutation(mutation)
            mutationClass.mutate(save_path_prepared, full_mutants_path)
        except LookupError as e:
            logging.info("Unable to apply the mutation for mutation %s. See technical logs for details. ", mutation)
            logging.error("Was not able to create a class for mutation %s: " + str(e), mutation)
        except Exception as e:
            logging.info("Unable to apply the mutation for mutation %s. See technical logs for details. ", mutation)
            logging.error("Unable to apply the mutation for mutation %s: " + str(e), mutation)
       


def create_mutation(mut):
    """ Script that renames the file with trained model

        Keyword arguments:
        file_path -- path to the file
        ... params needed to constuct new name

        Returns: ...
    """

    MutClass = getattr(mutations, constants.mutation_class_map[mut])

    if MutClass is None:
        logging.error("Has not found a class to create a Mutation.")
        raise LookupError("Has not found a class to create a Mutation")

    mutation = MutClass()

    return mutation    