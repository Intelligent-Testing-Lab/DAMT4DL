import argparse
import os

from utils import config, gen_path_name
from analyse.analyse_utils import *

def cal_mutation_scores(conf):
    if conf.criterion == 'k_score':
        ms = cal_mutation_scores_k_score(conf)
    elif conf.criterion == 'd_score':
        ms = cal_mutation_scores_d_score(conf)
    return ms

def count_killed_mutants(conf):
    kille_num = 0
    for mutation in conf.mutations:
        full_path = gen_path_name.gen_full_path('results', conf, mutation)
        
        # the path of the stats file
        states_path = os.path.join(full_path, 'stats.csv')

        # load the stats file
        stats = load_stats_k_score(states_path)

        # count the killed mutants
        for stat in stats:
            if stat[3]:
                kille_num += 1
    return kille_num


def cal_mutation_scores_k_score(conf):
    # calculate the killed mutants in the current mode
    cur_killed_num = count_killed_mutants(conf=conf)
    
    # calculate the killed mutants in the training set
    conf.mode = 'train'
    train_killed_num = count_killed_mutants(conf=conf)

    return float(cur_killed_num/train_killed_num)


def get_undistinguished_mutants(conf):
    all_mutants_num = 1 # include the original model
    for mutation in conf.mutations:
        full_path = gen_path_name.gen_full_path('results', conf, mutation)
        
        # the path of the stats file
        states_path = os.path.join(full_path, 'stats.csv')

        # load the stats file
        stats = load_stats_d_score(states_path)

        

        # count the killed mutants
        undistinguished_set = set()
        original_d_vec = (0, ) * len(stats[0][1])
        undistinguished_set.add(original_d_vec)
        
        for stat in stats:
            d_vec = stat[1]
            undistinguished_set.add(d_vec)
            all_mutants_num += 1
    return undistinguished_set, all_mutants_num


def cal_mutation_scores_d_score(conf):
    # calculate the undistinguished mutants under the current mode
    undistinguished_set, all_mutants_num = get_undistinguished_mutants(conf=conf)
    
    if conf.algorithm == 'd_score_original_base':
        # if the algorithm is d_score_original_base, return the ratio of the undistinguished mutants to all the mutants
        return float(len(undistinguished_set)/all_mutants_num)
    elif conf.algorithm == 'd_score_train_training_base':
        # if the algorithm is d_score_train_training_base, return the ratio of the undistinguished mutants to the training set
        conf.mode = 'train'
        undisguished_set_train, _ = get_undistinguished_mutants( conf=conf)

def run():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Run the experiment')
    parser.add_argument('--config', type=str, help='Path to the configuration file')


    # Parse the arguments
    args = parser.parse_args()

    # Set up the experiment parameters
    conf = config.Config.from_yaml(args.config)

    print("=========Read Properties successfully: subject: %s, mode: %s, mutations: %s, criterion: %s, algorithm: %s=========" % (conf.subject_name, conf.mode, conf.mutations, conf.criterion, conf.algorithm))

    # Calculate the mutation scores
    print("Calculating mutation scores")
    ms = cal_mutation_scores(conf)
    print("Mutation scores: %f" % ms)

    print("Finished")

    
if __name__ == '__main__':
    run()