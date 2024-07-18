import argparse
import os

from utils import config, gen_path_name
from analyse.analyse_utils import *
from analyse.stats import *


def analyze_stats(conf):
     for mutation in conf.mutations:
        print("\n\nAnalyzing the results for mutation operator: %s" % mutation)

        # full path
        full_path = gen_path_name.gen_full_path('results', conf, mutation)

        # save the states to csv file
        states_path = os.path.join(full_path, 'stats.csv')
        
        if not os.path.exists(states_path):
            # analyze satistics based on the criterion
            if conf.criterion == 'k_score':
                analyze_results_k_scores(full_path, states_path)
            elif conf.criterion == 'd_score':
                analyze_results_d_scores(full_path, states_path)
        else:
            print("The stats file already exists: %s for mutation operator: %s" % (states_path, mutation))
            

def analyze_results_k_scores(full_path, states_path):
    print("Analyzing the results for k_score")

    original_scores_path = os.path.join(full_path, 'original_scores.csv') # save the scores of the original model

    # load the original scores
    original_scores = load_scores_from_csv(original_scores_path)
    original_accuracy_list = get_accuracy_list_from_scores(original_scores)

    # statistic analysis for each mutant
    for _, _, filenames in os.walk(full_path):
        for filename in filenames:
            if filename.endswith('.csv') and filename != 'original_scores.csv':
                print("mutant name: %s" % filename)

                # load mutant scores from csv file
                mutant_scores_path = os.path.join(full_path, filename)
                mutant_scores = load_scores_from_csv(mutant_scores_path)
                mutant_accuracy_list = get_accuracy_list_from_scores(mutant_scores)

                # statistic anaylyse for the performance
                is_sts, p_value, effect_size = is_diff_sts(original_accuracy_list, mutant_accuracy_list)

                # save the stats
                save_stats_k_score(states_path, filename.replace(".csv", ""), p_value, effect_size, is_sts)


def handle_d_score(scores):
    """
    Handle the d_score

    Returns:
    d_scores: dictionary of the d_score
    Key: run number
    Value: [[score1, score2], [score1, score2], ...] # for each test case
    """
    d_scores = {}
    for mutant_id, test_case_id, score1, score2 in scores:
        if int(mutant_id-1) not in d_scores:
            d_scores[int(mutant_id-1)] = []
        d_scores[int(mutant_id-1)].append([score1, score2])

    return d_scores
  

def is_diff_sts_d_score(original_scores, mutant_scores):
    d_vec = []
    runs_num = len(original_scores)
    test_cases_num = len(original_scores[0])

    for test_case_id in range(test_cases_num):
        original_accuracy_list = get_accuracy_list_from_scores_d_score(original_scores, test_case_id, runs_num)
        mutant_accuracy_list = get_accuracy_list_from_scores_d_score(mutant_scores, test_case_id, runs_num)
        is_sts, _, _ = is_diff_sts(original_accuracy_list, mutant_accuracy_list)
        d_vec.append(1 if is_sts else 0)
    return d_vec


def analyze_results_d_scores(full_path, states_path):
    print("Analyzing the results for d_score")
    original_scores_path = os.path.join(full_path, 'original_scores.npy') # save the scores of the original model
    print("original_scores_path: %s" % original_scores_path)
    
    # load the original scores
    original_scores = load_scores_from_npy_d_scores(original_scores_path)
    original_d_scores = handle_d_score(original_scores)


    # statistic analysis for each mutant
    for _, _, filenames in os.walk(full_path):
        for filename in filenames:
            if filename.endswith('.npy') and filename != 'original_scores.npy':
                print("mutant name: %s" % filename)

                # load mutant scores from npy file
                mutant_scores_path = os.path.join(full_path, filename)
                mutant_scores = load_scores_from_npy_d_scores(mutant_scores_path)
                mutant_d_scores = handle_d_score(mutant_scores)

                # statistic anaylyse for the performance
                d_vector = is_diff_sts_d_score(original_d_scores, mutant_d_scores)

                # save the stats
                save_stats_d_score(states_path, filename.replace(".npy", ""), d_vector)

                
                        
def run():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Run the experiment')
    parser.add_argument('--config', type=str, help='Path to the configuration file')


    # Parse the arguments
    args = parser.parse_args()

    # Set up the experiment parameters
    conf = config.Config.from_yaml(args.config)

    print("=========Read Properties successfully: subject: %s, mode: %s, mutations: %s, criterion: %s, workers_num: %s=========\n\n" % (conf.subject_name, conf.mode, conf.mutations, conf.criterion, conf.workers_num))


    # Statistical analysis of the results
    print("===========Statistical Analyzing the results===========\n\n")
    analyze_stats(conf)

    print("===========Statistical Analysis completed===========\n\n")

if __name__ == '__main__':
    run()