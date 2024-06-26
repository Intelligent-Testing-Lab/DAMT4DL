import argparse

from utils import config
from execution import execute
from mutation import mutate



def run():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Run the experiment')
    parser.add_argument('--config', type=str, help='Path to the configuration file')

    # Parse the arguments
    args = parser.parse_args()

    # Set up the experiment parameters
    conf = config.Config.from_yaml(args.config)

    # Generate mutation models TODO
    mutate.mutate_model(conf)

    # Train the models and save results TODO
    execute.execute_models(conf)


if __name__ == '__main__':
    run()

