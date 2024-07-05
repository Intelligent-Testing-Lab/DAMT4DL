import os
import logging
import mutation.mutations as mutations

from utils import constants, gen_path_name
from mutation.mutations import *
from mutation.prepare import *
from mutation.original_model import *

def mutate_model(config):    
    # Generate the mutated models
    for mutation in config.mutations:
        
        # prepare the original model code for muation and save it 
        full_path = gen_path_name.gen_full_path('results', config, mutation)
        save_path_prepared = os.path.join(full_path, 'prepared.py')
        prepare_model(config.original_path, save_path_prepared)
        print("Prepared model saved to: %s\n" % save_path_prepared)

        # prepare the origianl model for training
        sava_path_original = os.path.join(full_path, 'original.py')
        update_orginal_model(config.original_path, sava_path_original)
        print("Original model saved to: %s\n" % sava_path_original)

        print("Generate mutants for mutation %s\n\n" % mutation)
        # create the muatant 
        mutationClass = create_mutation(mutation)
        mutationClass.mutate(save_path_prepared, full_path)
        
        print("Mutation (%s) applied to the model. Mutated models saved to: %s\n" % (mutation, full_path))
       


def create_mutation(mut):
    """ Script that renames the file with trained model

        Keyword arguments:
        file_path -- path to the file
        ... params needed to constuct new name

        Returns: ...
    """

    MutClass = getattr(mutations, constants.mutation_class_map[mut])
    mutation = MutClass()
    return mutation    