from execution.execute_original import execute_original_model
from execution.execute_mutant import execute_mutants

def execute_models(config):
    # TODO use config to get the path
    original_path = ""
    mutant_path = ""

    execute_original_model(original_path)
    execute_mutants(mutant_path)



