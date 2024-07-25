import csv
import numpy as np
import ast
import sys

# Increase the CSV field size limit
csv.field_size_limit(sys.maxsize)



def load_scores_from_csv(file_path):
    """
    Load scores from csv file for k_score
    """
    scores = []
    with open(file_path) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            if any(x.strip() for x in row):
                scores.append((float(row[1]), float(row[2])))

    return scores

def load_scores_from_npy_d_scores(file_path):
    """ load scores from npy file for d_score
    """
    row_array = np.load(file_path)
    
    return row_array.tolist()

def get_accuracy_list_from_scores(scores):
    """
    Get accuracy list from scores
    """
    scores_len = len(scores)
    accuracy_list = list(range(0, scores_len))
    for i in range (0, scores_len):
        accuracy_list[i] = scores[i][1]

    return accuracy_list

def get_accuracy_list_from_scores_d_score(scores, test_case_id, runs_num):
    """
    Get accuracy list from scores for d_score
    """
    accuracy_list = list(range(0, runs_num))
    for i in range (0, runs_num):
        accuracy_list[i] = scores[i][test_case_id][1]

    return accuracy_list

def save_stats_k_score(states_path, mutant_name, p_value, effect_size, is_sts):
    """
    Save the states to csv file for k_score
    """
    with open(states_path, 'a') as f1:
        writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
        writer.writerow([mutant_name, str(p_value), str(effect_size), 1 if is_sts else 0])

def load_stats_k_score(states_path):
    """
    Load the states from csv file for k_score
    """
    states = []
    with open(states_path) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            mutant_name = row[0]
            p_value = float(row[1])
            effect_size = float(row[2])
            is_sts = False if row[3] == '0' else True
            states.append([mutant_name, p_value, effect_size, is_sts])

    return states


def save_stats_d_score(states_path, mutant_name, d_vector):
    """
    Save the states to csv file for d_score
    """
    with open(states_path, 'a') as f1:
        writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
        writer.writerow([mutant_name, d_vector])

def load_stats_d_score(states_path):
    """
    Load the states from csv file for d_score
    """
    states = []
    with open(states_path) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            mutant_name = row[0]
            d_vector = ast.literal_eval(row[1])
            states.append([mutant_name, tuple(d_vector)])

    return states