import importlib
import os
import sys
import utils.constants as const

from utils import gen_path_name
from execution.execution_utils import *

def execute_original_model(path, config):    
    print("Executing original model")
    # results save path
    scores_file_path = os.path.join(path, 'original_scores.csv') # save the scores of the original model

    # load the original model 
    transformed_path = os.path.join(path, 'original.py').replace(os.path.sep, ".").replace(".py", "")
    m1 = importlib.import_module(transformed_path)

    # train the original model and save the results
    scores = []
    if not(os.path.isfile(scores_file_path)):
        for i in range(const.runs_number_default):
            origian_weights_path = gen_path_name.gen_original_weights_path('results', config)
            weight_file_path = os.path.join(origian_weights_path, 'model_weights_%d.h5' % i)
            score = m1.main(weight_file_path)
            scores.append(score)

        save_scores_csv(scores, scores_file_path)
        print("The scores of the original model have been saved to the file: %s" % scores_file_path)
    else:
        print("Loading the scores from the file")
        scores = load_scores_from_csv(scores_file_path)
        print("The scores of the original model: %s" % scores)

    print("Execution of original model completed\n\n")
    return scores
