# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import csv

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
    scores = []
    with open(file_path) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            if any(x.strip() for x in row):
                scores.append((float(row[1]), float(row[2])))

    return scores
