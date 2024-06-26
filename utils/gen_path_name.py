import os

def gen_mutant_directory_path(path, config, mutation):
    """
    Generate the directory path to save the mutants
    """
    path = os.path.join(path, config.subject_name, config.criterion, config.mode, mutation)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def gen_prepare_directory_path(path, config):
    """
    Generate the path to save the prepared orginal model
    """
    path = os.path.join(path, config.subject_name, config.criterion, config.mode)
    if not os.path.exists(path):
        os.makedirs(path)
    return path