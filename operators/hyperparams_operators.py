# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

from tensorflow.keras import backend as K

import utils.properties as props
import keras


# Define a dictionary to map string names to optimizer classes
optimizer_map = {
    'Adam': keras.optimizers.Adam(),
    'SGD': keras.optimizers.SGD(),
    'RMSprop': keras.optimizers.RMSprop(),
    # Add more optimizers as needed
}

def operator_change_learning_rate(optimiser):
    """Unparse the ast tree, save code to py file.

        Keyword arguments:
        tree -- ast tree
        save_path -- the py file where to save the code

        Returns: int (0 - success, -1 otherwise)
    """
    if isinstance(optimiser, str):
        if optimiser in optimizer_map:
            optimiser = optimizer_map[optimiser]
        else:
            raise ValueError(f"Unsupported optimizer: {optimiser}")


    if props.change_learning_rate["learning_rate_udp"]:
        new_lr = props.change_learning_rate["learning_rate_udp"]
    else:
        new_lr = props.change_learning_rate["pct"]

    with K.name_scope(optimiser.__class__.__name__):
        optimiser.learning_rate = K.variable(new_lr, name='learning_rate')

    return optimiser
