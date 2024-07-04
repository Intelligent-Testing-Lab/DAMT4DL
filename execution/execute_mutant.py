import importlib
import csv
import os
import utils.properties as props
import utils.constants as const

from execution.execution_utils import *
from analyse.stats import *

def execute_mutants_MO(mutation_path, mutation, full_original_path):
    """
    execute the mutants for each mutation operator
    """
    print("Executing mutants")
    
    # read the muation operator parameters
    mutation_params = {}
    try:
        mutation_params = getattr(props, mutation)
    except AttributeError:
        print("No attributes found")

    # # read the model parameters
    # model_params = getattr(props, "model_properties") # TODO what is model_properties?

    # TODO what is udp?
    # udp = [value for key, value in mutation_params.items() if "udp" in key.lower() and "layer" not in key.lower()]
    # if len(udp) > 0:
    #     udp = udp[0]
    # else:
    #     udp = None
    # layer_udp = mutation_params.get("layer_udp", None)

    # read the search type
    search_type = mutation_params.get("search_type")

    # execute the mutants
    for dirpath, _, filenames in os.walk(mutation_path):
        for filename in filenames:
            if filename.endswith('.py'):
                # read the path of the mutant
                mutant_path = os.path.join(dirpath, filename)

                # based on the search type, execute the mutant
                if search_type == const.Binary:
                    print("calling binary search")
                    execute_binary_search(mutant_path, mutation, mutation_params, mutation_path, full_original_path)
                elif search_type == const.Exhaustive:
                    print("calling exhaustive search")
                    execute_exhaustive_search(mutant_path, mutation, mutation_params, mutation_path, full_original_path)
                else:
                    # TODO handle when search type is None
                    pass

                
                # # TODO handle the layer_muatation - about udp
                # if mutation_params.get("layer_mutation", False):
                #     # TODO do not understand
                #     if layer_udp:
                #         if isinstance(layer_udp, list):
                #             inds = layer_udp
                #         else:
                #             inds = [layer_udp]
                #     else:
                #         inds = range(model_params["layers_num"])

                #     for ind in inds:
                #         mutation_params["mutation_target"] = None
                #         mutation_params["current_index"] = ind
                #         mutation_ind = "_" + str(ind)
                    
                #     execute_based_on_search(udp, search_type, mutation, mutant, mutation_params, ind, mutation_ind)
                # else:
                #     execute_based_on_search(udp, search_type, mutation, mutant, mutation_params)



def execute_binary_search(mutant_path, mutation, mutation_params, mutation_path, full_original_path):
    """
    execute the binary search for a mutant

    Args:
    mutant_path -- the path of the mutant
    mutation -- the mutation operator name
    mutation_params -- the parameters of the mutation operator
    full_original_path -- the path of the original model
    """
    print("Running Binary Search for" + str(mutation))

    # read the mutation parameters
    lower_bound = mutation_params["bs_lower_bound"]
    upper_bound = mutation_params["bs_upper_bound"]

    # get the performance of the orginal model
    origianl_scores_file_path = os.path.join(full_original_path, 'scores.csv') # save the scores of the original model
    original_scores = load_scores_from_csv(origianl_scores_file_path)
    original_accuracy = get_accuracy_list_from_scores(original_scores)

    # execute the upper bound of the mutant
    update_mutation_properties(mutation, "pct", upper_bound) # update the parameyters using upper bound
    mutant_scores = execute_mutant(mutant_path, mutation_path, mutation_params)
    mutant_accuracy = get_accuracy_list_from_scores(mutant_scores)

    # satistic anaylyse for the performance 
    is_sts, p_value, effect_size = is_diff_sts(original_accuracy, mutant_accuracy)

    # save the results of the upper bound of the mutant
    states_path = os.path.join(mutation_path, 'states')
    save_sates_csv(str(lower_bound),str(upper_bound), '', p_value, effect_size, is_sts, states_path)

    # execute the lower bound of the mutant
    if is_sts:
        print("Binary Search: Upper Bound is Killable")
        search_for_bs_conf(mutant_path, mutation, mutation_params, lower_bound, upper_bound, original_accuracy, mutant_accuracy, states_path, mutation_path)
    else:
        print("Binary Search: Upper Bound is Not Killable")

# This function is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International
def execute_exhaustive_search(mutant, mutation, my_params, mutation_path, full_original_path, mutation_ind = ''):

    print("Running Exhaustive Search for" + str(mutant))
    # get the performance of the orginal model
    origianl_scores_file_path = os.path.join(full_original_path, 'scores.csv') # save the scores of the original model
    original_scores = load_scores_from_csv(origianl_scores_file_path)
    original_accuracy_list = get_accuracy_list_from_scores(original_scores)

    # get the path of the states
    states_path = os.path.join(mutation_path, 'states')


    name = my_params['name']
    if name == 'change_optimisation_function':
        for optimiser in const.keras_optimisers:
            print("Changing into optimiser:" + str(optimiser))
            update_mutation_properties(mutation, "optimisation_function_udp", optimiser)
            mutation_accuracy_list = get_accuracy_list_from_scores(execute_mutant(mutant, my_params))
            is_sts, p_value, effect_size = is_diff_sts(original_accuracy_list, mutation_accuracy_list)

            if len(mutation_accuracy_list) > 0:
                with open(states_path, 'a') as f1:
                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                    writer.writerow([str(optimiser), str(p_value), str(effect_size), str(is_sts)])
    elif name == 'change_activation_function' or name == 'add_activation_function':
        for activation in const.activation_functions:
            print("Changing into activation:" + str(activation))
            update_mutation_properties(mutation, "activation_function_udp", activation)
            mutation_accuracy_list = get_accuracy_list_from_scores(execute_mutant(mutant, my_params, mutation_ind))
            is_sts, p_value, effect_size = is_diff_sts(original_accuracy_list, mutation_accuracy_list)

            if len(mutation_accuracy_list) > 0:
                with open(states_path, 'a') as f1:
                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                    writer.writerow([str(activation), str(p_value), str(effect_size), str(is_sts)])
    elif name == 'change_loss_function':
        for loss in const.keras_losses:
            print("Changing into loss:" + str(loss))
            update_mutation_properties(mutation, "loss_function_udp", loss)
            mutation_accuracy_list = get_accuracy_list_from_scores(execute_mutant(mutant, my_params))
            is_sts, p_value, effect_size = is_diff_sts(original_accuracy_list, mutation_accuracy_list)

            if len(mutation_accuracy_list) > 0:
                with open(states_path, 'a') as f1:
                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                    writer.writerow([str(loss), str(p_value), str(effect_size), str(is_sts)])
    elif name == 'change_dropout_rate':
        for dropout in const.dropout_values:
            print("Changing into dropout rate:" + str(dropout))
            update_mutation_properties(mutation, "rate", dropout)
            mutation_accuracy_list = get_accuracy_list_from_scores(execute_mutant(mutant, my_params, mutation_ind))
            is_sts, p_value, effect_size = is_diff_sts(original_accuracy_list, mutation_accuracy_list)

            if len(mutation_accuracy_list) > 0:
                with open(states_path, 'a') as f1:
                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                    writer.writerow([str(dropout), str(p_value), str(effect_size), str(is_sts)])
    elif name == 'change_batch_size':
        for batch_size in const.batch_sizes:
            print("Changing into batch size:" + str(batch_size))
            update_mutation_properties(mutation, "batch_size", batch_size)
            mutation_accuracy_list = get_accuracy_list_from_scores(execute_mutant(mutant, my_params))
            is_sts, p_value, effect_size = is_diff_sts(original_accuracy_list, mutation_accuracy_list)

            if len(mutation_accuracy_list) > 0:
                with open(states_path, 'a') as f1:
                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                    writer.writerow([str(batch_size), str(p_value), str(effect_size), str(is_sts)])
    elif name == 'change_weights_initialisation':
        for initialiser in const.keras_initialisers:
            print("Changing into initialisation:" + str(initialiser))
            update_mutation_properties(mutation, "weights_initialisation_udp", initialiser)
            mutation_accuracy_list = get_accuracy_list_from_scores(execute_mutant(mutant, my_params, mutation_ind))
            is_sts, p_value, effect_size = is_diff_sts(original_accuracy_list, mutation_accuracy_list)

            if len(mutation_accuracy_list) > 0:
                with open(states_path, 'a') as f1:
                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                    writer.writerow([str(initialiser), str(p_value), str(effect_size), str(is_sts)])
    elif name == 'add_weights_regularisation':
        for regularisation in const.keras_regularisers:
            print("Changing into regularisation:" + str(regularisation))
            update_mutation_properties(mutation, "weights_regularisation_udp", regularisation)
            mutation_accuracy_list = get_accuracy_list_from_scores(execute_mutant(mutant, my_params, mutation_ind))
            is_sts, p_value, effect_size = is_diff_sts(original_accuracy_list, mutation_accuracy_list)

            if len(mutation_accuracy_list) > 0:
                with open(states_path, 'a') as f1:
                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                    writer.writerow([str(regularisation), str(p_value), str(effect_size), str(is_sts)])
    
def execute_mutant(mutant_path, mutation_path, mutation_params):
    """
    execute for a mutant based on the given parameters
    Args:
    mutant_path -- the path of the mutant
    mutation_path -- the path of the mutation operator
    mutation_params -- the parameters of the mutation operator
    """
    # results save path
    scores_file_path = os.path.join(mutation_path, 'scores.csv') # save the scores of the original model

    scores = [] # save the scores of the mutant
    params_list = concat_params_for_file_name(mutation_params) # concat the parameters for the file name

    # load the mutant
    m1 = importlib.import_module(mutant_path)

    # TODO: need to check
    # data = read_properties()
    #     if data['mode'] in ('train', 'weak'):
    #         importlib.reload(m1) # reload the module to get the new properties

    # train the mutant and save the results
    if not(os.path.isfile(scores_file_path)):
        for i in range(mutation_params["runs_number"]):
            weight_file_path = os.path.join(mutation_path, 'weights', 'model_weights_%s_%d.h5' % (params_list, i))
            score = m1.main(weight_file_path)
            scores.append(score)
        # save the scores
        save_scores_csv(scores, scores_file_path)
    else:
        print("reading scores from file")
        scores = load_scores_from_csv(scores_file_path)
    return scores


# This function is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International
def concat_params_for_file_name(params):
    """ Script that renames the file with trained model

        Keyword arguments:
        file_path -- path to the file
        ... params needed to construct new name

        Returns: ...
    """
    list_params = ""
    for k, v in params.items():
        if any(abbrv in k for abbrv in const.mutation_params_abbrvs):
            list_params += str(v) + "_"

    if list_params:
        list_params = "_" + list_params[:-1]

    return list_params
    
    
    

# This function is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International
def search_for_bs_conf(mutant_path, mutation, my_params, lower_bound, upper_bound, lower_accuracy_list, upper_accuracy_list, states_path, mutation_path):
    """
    search for the binary search confidence: until the size of the range becomes smaller than or equal to a predefined precision 𝜖,
    """

    # calculate the middle bound
    if my_params['bs_rounding_type'] == 'int':
        middle_bound = round((upper_bound + lower_bound) / 2)
    elif my_params['bs_rounding_type'] == 'float3':
        middle_bound = round((upper_bound + lower_bound) / 2, 3)
    elif my_params['bs_rounding_type'] == 'float4':
        middle_bound = round((upper_bound + lower_bound) / 2, 4)
    elif my_params['bs_rounding_type'] == 'float5':
        middle_bound = round((upper_bound + lower_bound) / 2, 5)
    else:
        middle_bound = round((upper_bound + lower_bound) / 2, 2)

    print("middle_bound is:" + str(middle_bound))

    # execute the middle bound
    update_mutation_properties(mutation, "pct", middle_bound)
    middle_scores = execute_mutant(mutant_path, mutation_path, my_params)
    middle_accuracy_list = get_accuracy_list_from_scores(middle_scores)

    # statistic analysis for the performance
    is_sts, p_value, effect_size = is_diff_sts(lower_accuracy_list, middle_accuracy_list)

    # save the results of the middle bound of the mutant
    save_sates_csv(str(lower_bound), str(upper_bound), str(middle_bound), p_value, effect_size, is_sts, states_path)

    # update the bounds based on the performance
    if is_sts:
        upper_bound = middle_bound
        upper_accuracy_list = middle_accuracy_list
    else:
        lower_bound = middle_bound
        lower_accuracy_list = middle_accuracy_list

    # check if the size of the range is smaller than or equal to a predefined precision 𝜖
    if abs(upper_bound - lower_bound) <= my_params['precision']:
        if is_sts:
            perfect = middle_bound
            conf_nk = lower_bound
        else:
            perfect = upper_bound
            conf_nk = middle_bound
        
        # save the perfect and conf_nk configuration
        # perfect configuration is the one that is killable
        # conf_nk is the one that is not killable
        with open(states_path, 'a') as f1:
            writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
            writer.writerow([str(perfect), str(conf_nk)])

        print("Binary Search Configuration is:" + str(perfect))
        return perfect, conf_nk
    else:
        print("Changing interval to: [" + str(lower_bound) + ", " + str(upper_bound) + "]")
        return search_for_bs_conf(mutant_path, mutation, my_params, lower_bound, upper_bound,
                                  lower_accuracy_list, upper_accuracy_list, states_path, mutation_path)