import argparse
import os

from utils import config, gen_path_name
from analyse.analyse_utils import *

def count_mutants_MO_k_score(stats):
    """
    count the number of killed mutants and all mutants for single mutant operators under k_score
    """
    killed_num = 0
    all_num = 0
    # count the killed mutants
    for stat in stats:
        if stat[3]:
            killed_num += 1
        all_num += 1
    return killed_num, all_num


def cal_mutation_scores_task_k_score(task, mutations, mode):
    """
    calculate the mutation scores for a task using k_score
    """

    results = {}
    conf = config.Config(
        subject_name=task,
        criterion='k_score',
        mode=mode
    )
    killed_num_overall = 0
    all_num_overall = 0
    for mutation in mutations:
        print("Calculating scores for %s mutation operator" % mutation)
        
        # the path of the stats file
        full_path = gen_path_name.gen_full_path('results', conf, mutation)
        states_path = os.path.join(full_path, 'stats.csv')

        # load the stats file
        stats = load_stats_k_score(states_path)

        # count the killed mutants for single mutant operator
        killed_num, all_num = count_mutants_MO_k_score(stats)
        
        results[mutation] = float(killed_num / all_num)

        killed_num_overall += killed_num
        all_num_overall += all_num
    
    # calculate the overall mutation score
    results["Overall"] = float(killed_num_overall / all_num_overall)

    return results

def get_unidstinguished_mutants_MO_d_score(stats):
    """
    Get undistinguished mutants and the number of all mutants for each single mutant operator under d_score
    """

    undistinguished_set = set()
    original_d_vec = (0, ) * len(stats[0][1]) # the d_vector of the original model
    undistinguished_set.add(original_d_vec)

    all_num = 0
    for stat in stats:
        d_vec = stat[1]
        undistinguished_set.add(d_vec)
        all_num += 1
    
    return undistinguished_set, all_num


def cal_mutation_scores_task_d_score(task, mutations, mode):
    """
    calculate the mutation scores for a task using d_score using the given algorithm
    """
    results = {}

    conf = config.Config(
        subject_name=task,
        criterion='d_score',
        mode=mode,
    )

    undistinguished_set_overall = set()
    all_num_overall = 0 

    for mutation in mutations:
        print("Calculating scores for %s mutation operator" % mutation)
        # the path of the stats file
        full_path = gen_path_name.gen_full_path('results', conf, mutation)
        states_path = os.path.join(full_path, 'stats.csv')

        # load the stats file
        stats = load_stats_d_score(states_path)

        # calculate the undistinguished mutants for single mutant operator
        undistinguished_set, all_num = get_unidstinguished_mutants_MO_d_score(stats)

        results[mutation] = float(len(undistinguished_set) / (all_num+1)) # add 1 to the denominator because the original model is also included

        # update the overall undistinguished mutants and all mutants
        undistinguished_set_overall = undistinguished_set_overall.union(undistinguished_set)
        all_num_overall += all_num
    
    # calculate the overall mutation score
    results["Overall"] = float(len(undistinguished_set_overall) / (all_num_overall + 1)) # add 1 to the denominator because the original model is also included

    return results

def save_mutation_scores(results, save_results_path, criterion, mutations, task):
    """
    Save the mutation scores to a csv file
    """
    ms_path = os.path.join(save_results_path, 'mutation_scores_%s.csv' % criterion)
    with open(ms_path, 'w') as f1:
        writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
        
        # write the header
        header = ['Mutation', 'Test', 'Train']
        if task != 'movie':
            header.append('Test_weak')
        writer.writerow(header)

        # write the mutation scores
        for mutation in mutations:
            values = [mutation, results['test'][mutation], results['train'][mutation]]
            if task != 'movie':
                values.append(results['test_weak'][mutation])
            writer.writerow(values)

        # write the overall mutation scores
        overall = ['Overall', results['test']['Overall'], results['train']['Overall']]
        if task != 'movie':
            overall.append(results['test_weak']['Overall'])
        writer.writerow(overall)



def run():
    # # Constants definition
    tasks = ['audio', 'lenet', 'mnist', 'movie', 'udacity']

    # Mutation operators for each task
    mnist_mutations = [
        "change_epochs",
        "change_label",
        "delete_training_data",
        "unbalance_train_data",
        "add_noise",
        "make_output_classes_overlap",
        "change_batch_size",
        "change_learning_rate",
        "remove_activation_function",
        "add_weights_regularisation",
        "change_dropout_rate",
        "change_weights_initialisation",
        "remove_bias",
        "change_loss_function",
        "change_optimisation_function",
        "remove_validation_set"
    ]

    movie_mutations = [
        "change_label",
        "delete_training_data",
        "unbalance_train_data",
        "make_output_classes_overlap",
        "change_batch_size",
        "change_learning_rate",
        "change_epochs",
        "disable_batching",
        "change_loss_function",
        "change_optimisation_function",
        "remove_validation_set"
    ]

    audio_mutations = [
        "change_label",
        "delete_training_data",
        "unbalance_train_data",
        "make_output_classes_overlap",
        "change_learning_rate",
        "change_epochs",
        "change_activation_function",
        "remove_activation_function",
        "add_activation_function",
        "add_weights_regularisation",
        "change_weights_initialisation",
        "remove_bias",
        "change_loss_function",
        "change_optimisation_function",
        "remove_validation_set",
        "change_earlystopping_patience"
    ]

    udacity_mutations = [
        "change_label",
        "delete_training_data",
        "unbalance_train_data", 
        "make_output_classes_overlap",
        "change_learning_rate",
        "change_epochs",
        "change_activation_function",
        "remove_activation_function",
        "add_weights_regularisation",
        "change_dropout_rate",
        "change_weights_initialisation",
        "remove_bias",
        "change_loss_function",
        "change_optimisation_function",
        "remove_validation_set"
    ]

    lenet_mutations = [
        "remove_validation_set",
        "change_optimisation_function",
        "change_loss_function",
        "remove_activation_function",
        "remove_bias",
        "add_weights_regularisation",
        "add_activation_function",
        "change_activation_function",
        "change_weights_initialisation",
        "change_epochs",
        "change_batch_size",
        "change_learning_rate",
        "delete_training_data",
        "add_noise",
        "unbalance_train_data",
        "make_output_classes_overlap",
        "change_label"
    ]
    

    for task in tasks:
        results = {}
        if task == 'audio':
            mutations = audio_mutations
        elif task == 'lenet':
            mutations = lenet_mutations
        elif task == 'mnist':
            mutations = mnist_mutations
        elif task == 'movie':
            mutations = movie_mutations
        elif task == 'udacity':
            mutations = udacity_mutations
        
        results['k_score'] = {}
        results['d_score'] = {}
        for mode in ['test', 'train', 'test_weak']:
            if task == 'movie' and mode == 'test_weak':
                continue
            # k-score
            print("\n\nCalculating k-scores for %s task using %s mode\n\n" % (task, mode))
            results['k_score'][mode] = cal_mutation_scores_task_k_score(task, mutations, mode)

            # d-score
            print("\n\nCalculating d-scores for %s task using %s mode\n\n" % (task, mode))
            results['d_score'][mode] = cal_mutation_scores_task_d_score(task, mutations, mode)
        
        # save results
        for criterion in ['k_score', 'd_score']:
            save_results_path = gen_path_name.gen_ms_path('results/analysis', task, criterion)
            save_mutation_scores(results[criterion], save_results_path, criterion, mutations, task)
 
if __name__ == '__main__':
    run()