import importlib
import os
import utils.constants as const
import multiprocessing
import concurrent.futures
import time


from utils import gen_path_name
from execution.execution_utils import *

def execute_original_model(path, config):    
    print("Executing original model")

    # results save path
    if config.criterion == 'k_score':
        scores_file_path = os.path.join(path, 'original_scores.csv') # save the scores of the original model
    elif config.criterion == 'd_score':
        scores_file_path = os.path.join(path, 'original_scores.npy')

    # load the original model 
    transformed_path = os.path.join(path, 'original.py').replace(os.path.sep, ".").replace(".py", "")

    # train the original model and save the results
    if not(os.path.isfile(scores_file_path)):
        original_weights_path = gen_path_name.gen_original_weights_path('results', config)
        
        manager = multiprocessing.Manager()

        if config.criterion == 'k_score':
            scores = [[0,0]] * const.runs_number_default
            scores = manager.list(scores)  # Use a managed list to share data between processes
        elif config.criterion == 'd_score':
            scores = [[]] * const.runs_number_default # d-score has 3 values: single test case index, scores[0], scores[1]
            scores = manager.list(scores)  # Use a managed list to share data between processes 
        
        # Execute the original model asynchronously across multiple processes 
        with concurrent.futures.ProcessPoolExecutor(max_workers=config.workers_num) as executor:
            futures = [executor.submit(train_model, transformed_path, scores, original_weights_path, i) for i in range(const.runs_number_default)]
            concurrent.futures.wait(futures)

        # Save the scores after all futures complete
        if config.criterion == 'k_score':
            save_scores_csv(list(scores), scores_file_path)
        elif config.criterion == 'd_score':
            save_scores_npy_d_score(list(scores), scores_file_path)
        print(f"The scores of the original model have been saved to the file: {scores_file_path}")
    else:
        # TODO depreacted
        print("Loading the scores from the file")
        if config.criterion == 'k_score':
            scores = load_scores_from_csv(scores_file_path)
            print("The scores of the original model: %s" % scores)
        elif config.criterion == 'd_score':
            scores = load_scores_from_csv_d_score(scores_file_path, const.runs_number_default)   
            print("The length of scores of the original model: %s" % len(scores))

    print("Execution of original model completed\n\n")
    return scores

def train_model(transformed_path, scores, original_weights_path, i):
    """
    train the mutant and save the results
    """
    start_time = time.time()
    try:
        weight_file_path = os.path.join(original_weights_path, 'model_weights_%d.h5' % i)
        m1 = importlib.import_module(transformed_path) # load the model
        score = m1.main(weight_file_path)
        scores[i] = score
    except Exception as e:
        print("Error in training the original model: %s" % e)
    print("Time taken for the original model name(%d): %s\n" % (i, time.time() - start_time))