import yaml
import os


          
def gen_single_mutation_config(original_path, task, mode, criterion):
    # Read the original file
    with open(original_path, 'r') as file:
        data = yaml.safe_load(file)

    # Get the base data without mutations
    base_data = {key: value for key, value in data.items() if key != 'mutations'}

    # Iterate through each mutation and create a new YAML file
    for mutation in data['mutations']:
        # Add the current mutation to the base data
        mutation_data = base_data.copy()
        mutation_data['mutations'] = [mutation]

        # Create the new filename
        new_filepath = f'./config_file/{task}/{criterion}/{mode}'
        if os.path.exists(new_filepath) == False:
            os.makedirs(new_filepath)

        new_filename = f"{mutation}.yaml"

        # Save the new YAML file
        with open(os.path.join(new_filepath, new_filename), 'w') as new_file:
            yaml.dump(mutation_data, new_file)

        print(f"Created {new_filename}")



tasks = ['audio', 'lenet', 'mnist', 'movie', 'udacity']
modes = ['test', 'train', 'test_weak']
criterions = ['k-score', 'd-score']

for task in tasks:
    for mode in modes:
        if mode == 'test_weak' and task == 'movie':
            continue
        for criterion in criterions:
            original_path = f'./config_file/{task}/{criterion}/{task}_{mode}.yaml'
            gen_single_mutation_config(original_path, task, mode, criterion)