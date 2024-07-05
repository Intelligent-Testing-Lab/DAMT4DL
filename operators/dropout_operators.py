# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import utils.properties as props
import utils.exceptions as e
import mutation.mutation_utils as mu

def operator_change_dropout_rate(model):

    if not model:
        print("raise,log we have probllems")

    # functions = copy.copy(const.activation_functions)
    # functions.remove("linear")
    # new_act_func = random.choice(functions)

    current_index = props.change_dropout_rate["current_index"]

    tmp = model.get_config()

    print("Changing dropout for layer " + str(current_index))
    if tmp['layers'][current_index]['class_name'] == 'Dropout':
        tmp['layers'][current_index]['config']['rate'] == props.change_dropout_rate['rate']
    else:
        raise e.AddAFMutationError(str(current_index), "Not possible to apply change dropout mutation to layer ")

    model = mu.model_from_config(model, tmp)

    return model