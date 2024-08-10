import os

def gen_full_path(path, config, mutation):
    """
    Generate the full path to save codes of orginal, prepared and mutated models and the scores of all the models for each muatation, criterion and mode
    """
    path = os.path.join(config.subject_name, mutation, config.criterion, config.mode)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def gen_original_weights_path(path, config):
    """
    Generate the path to save the original model weights
    """
    path = os.path.join(config.save_path, path, config.subject_name, 'original_weights')
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def gen_mutant_weights_path(path, config, mutation):
    """
    Generate the path to save the mutant models weights
    """
    path = os.path.join(config.save_path, path, config.subject_name, 'mutation_weights', mutation)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def gen_ms_path(path, subject_name, criterion):
    """
    Generate the path to save the mutation scores for each subject
    """
    path = os.path.join(path, subject_name, criterion)
    if not os.path.exists(path):
        os.makedirs(path)
    return path
