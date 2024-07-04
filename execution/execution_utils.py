# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import csv
import utils.properties as props

def save_scores_csv(scores, file_path, mutation_params = None):
    """ Script that renames the file with trained model

        Keyword arguments:
        file_path -- path to the file
        ... params needed to constuct new name

        Returns: ...
    """
    row_list = []

    for ind, score in enumerate(scores):
        row_list.append([ind+1, score[0], score[1]])

    with open(file_path, "w+", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)

def load_scores_from_csv(file_path):
    """
    Load scores from csv file
    """
    scores = []
    with open(file_path) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            if any(x.strip() for x in row):
                scores.append((float(row[1]), float(row[2])))

    return scores

def get_accuracy_list_from_scores(scores):
    """
    Get accuracy list from scores
    """
    scores_len = len(scores)
    accuracy_list = list(range(0, scores_len))
    for i in range (0, scores_len):
        accuracy_list[i] = scores[i][1]

    return accuracy_list

def update_mutation_properties(mutation, param, new_value):
    """ Script that renames the file with trained model

        Keyword arguments:
        file_path -- path to the file
        ... params needed to constuct new name

        Returns: ...
    """
    params = getattr(props, mutation)

    keys = [key for key, value in params.items() if param in key.lower()]

    for key in keys:
        params[key] = new_value

def save_sates_csv(lower_bound, upper_bound, middle_bound, p_value, effect_size, is_sts, file_path):
    """
    Save states to csv file
    """
    with open(file_path, 'a') as f1:
        writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
        writer.writerow([lower_bound, upper_bound, middle_bound ,str(p_value), str(effect_size), str(is_sts)])