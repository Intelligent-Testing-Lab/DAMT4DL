import os

def gen_mutant_path_name(mutants_path, subject_name, mutation):
    """
    Generate the path to save the mutant for each subject and mutation operator
    """
    if not os.path.exists(mutants_path):
        os.makedirs(mutants_path)
    return os.path.join(mutants_path, subject_name + "_" + mutation + "_mutated")

def gen_prepare_path_name(path, subject_name):
    """
    Generate the path to save the prepared orginal model for each subject
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path, subject_name + "_prepared")