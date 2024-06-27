import argparse
import importlib
import os
import shutil

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

    # Generate mutation models
    gen_mutants.mutate_model(conf)

    # Train the models and save results TODO
    execute.execute_models(conf)


if __name__ == '__main__':
    run()

