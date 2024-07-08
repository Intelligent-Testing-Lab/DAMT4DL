import argparse
import importlib
import os
import shutil
import time

from utils import config
import utils.properties as props
import utils.constants as const
from execution import execute
from mutation import gen_mutants



def run():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Run the experiment')
    parser.add_argument('--config', type=str, help='Path to the configuration file')
    parser.add_argument('--properties', type=str, help='Path to the properties file')
    parser.add_argument('--constants', type=str, help='Path to the constants file')

    # Parse the arguments
    args = parser.parse_args()

    # Set up the experiment parameters
    conf = config.Config.from_yaml(args.config)

    # Set up the properties and constants
    shutil.copy(args.properties, os.path.join('utils', 'properties.py'))
    shutil.copy(args.constants, os.path.join('utils', 'constants.py'))
    importlib.reload(props)
    importlib.reload(const)

    print("=========Read Properties successfully: subject: %s, mode: %s, mutations: %s, criterion: %s =========\n\n" % (conf.subject_name, conf.mode, conf.mutations, conf.criterion))

    # record the experiment running time
    start_time = time.time()
    print("===========Experiment started===========\n\n")

    # Generate mutation models
    print("========Generating mutants========\n\n")
    gen_mutants.mutate_model(conf)
    print("Mutated models generated\n\n")

    # Train the models and save results
    print("===========Training the origianl and mutated models===========\n\n")
    execute.execute_models(conf)
    print("===========Training completed and results saved===========\n\n")

    print("===========Experiment completed: %s seconds===========\n\n" % (time.time() - start_time))


if __name__ == '__main__':
    run()

