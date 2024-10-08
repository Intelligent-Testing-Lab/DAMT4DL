# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

from keras.callbacks import EarlyStopping as KES
from tensorflow.keras.callbacks import EarlyStopping as TKES
import utils.properties as props
import utils.exceptions as e

def operator_change_patience(callbacks=None):

    if props.change_earlystopping_patience["patience_udp"] is not None:
        new_patience = props.change_earlystopping_patience["patience_udp"]
    else:
        new_patience = props.change_earlystopping_patience["pct"]

    if isinstance(callbacks, list):
        for cb in callbacks:
            if isinstance(cb, KES) or isinstance(cb, TKES):
                cb.patience = new_patience
    elif isinstance(callbacks, KES) or isinstance(callbacks, TKES):
        callbacks.patience = new_patience
    else:
        raise e.AddAFMutationError(str(0),
                                   "Not possible to apply the change patience mutation")

    return callbacks
