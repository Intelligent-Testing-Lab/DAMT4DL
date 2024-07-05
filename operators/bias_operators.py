# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import random
import copy

import utils.constants as const
import utils.properties as props
import utils.exceptions as e
import mutation.mutation_utils as mu

def operator_add_bias(model):

    if not model:
        print("raise,log we have probllems")

    current_index = props.add_bias["current_index"]

    tmp = model.get_config()

    print("Adding bias to layer"+str(current_index))
    if 'use_bias' in tmp['layers'][current_index]['config'] and not tmp['layers'][current_index]['config']['use_bias']:
        tmp['layers'][current_index]['config']['use_bias'] = True
    else:
        raise e.AddAFMutationError(str(current_index), "Not possible to apply the add bias mutation to layer ")

    model = mu.model_from_config(model, tmp)

    return model


def operator_remove_bias(model):

    if not model:
        print("raise,log we have probllems")

    current_index = props.remove_bias["current_index"]

    tmp = model.get_config()

    print("Removing bias from layer " + str(current_index))
    if 'use_bias' in tmp['layers'][current_index]['config'] and tmp['layers'][current_index]['config']['use_bias']:
        tmp['layers'][current_index]['config']['use_bias'] = False
    else:
        raise e.AddAFMutationError(str(current_index), "Not possible to apply the add bias mutation to layer ")

    model = mu.model_from_config(model, tmp)

    return model