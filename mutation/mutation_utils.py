# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import ast
import keras
import shutil
import tensorflow as tf
import utils.constants as const
import utils.properties as props

from io import StringIO

from utils.unparse import Unparser

from keras import Sequential as KS
from tensorflow.keras import Sequential as TKS
from keras.models import Model as KM
from tensorflow.keras import Model as TKM

from keras.engine.sequential import Sequential as KES
from keras.engine.training import Model as KEM
from tensorflow.python.keras.engine.sequential import Sequential as TKES
from tensorflow.python.keras.engine.training import Model as TKEM

def unparse_tree(tree, save_path):
    """Unparse the ast tree, save code to py file.

        Keyword arguments:
        tree -- ast tree
        save_path -- the py file where to save the code

        Returns: int (0 - success, -1 otherwise)
    """

    buf = StringIO()
    try:
        Unparser(tree, buf)
        buf.seek(0)

        with open(save_path, 'w') as fd:
            buf.seek(0)
            shutil.copyfileobj(buf, fd)
            fd.close()
    except Exception as e:
        print("Unable to unparse the tree: " + str(e))
        raise


def is_import(elem):
    """Check if the given element is an import of library

        Keyword arguments:
        elem -- part of ast node

        Returns: boolean
    """

    is_imp = False
    if isinstance(elem, ast.Import):
        is_imp = True
    return is_imp


def generate_import_nodes():
    """Generate an import node based on the mutation_type

        Keyword arguments:
        types -- list of types of mutations to be done on a model in question

        Returns: list of ast import nodes
    """

    import_nodes = []
    for imp in const.operator_lib:
        # import_nodes.append(ast.Import(names=[ast.alias(name=const.mutation_imports[type], asname=None)]))
        import_nodes.append(
            ast.ImportFrom(module=const.operator_mod, names=[
                ast.alias(name=imp, asname=None),
            ], level=0))

    import_nodes.append(
        ast.ImportFrom(module="mutation", names=[
            ast.alias(name="mutation_utils", asname=None),
        ], level=0))

    import_nodes.append(
        ast.ImportFrom(module="utils", names=[
            ast.alias(name="properties", asname=None),
        ], level=0))

    import_nodes.append(
        ast.ImportFrom(module="keras", names=[
            ast.alias(name="optimizers", asname=None),
        ], level=0))

    return import_nodes



def check_for_annotation(elem, annotation_list):
    """Check if the given element corresponds to an annotation

        Keyword arguments:
        elem -- part of ast node
        annot_type -- type of the annotation: x_train, y_train

        Returns: boolean
    """
    if (is_annotated_node(elem)):
        target = elem.target.id
        annotation = elem.annotation.s

        if annotation in annotation_list:
            annotation_list.update({annotation: target})

def is_annotated_node(elem):
    """Check if the given node is an annotation

        Keyword arguments:
        elem -- part of ast node
        annot_type -- type of the annotation: x_train, y_train

        Returns: boolean
    """
    result = False

    if isinstance(elem, ast.AnnAssign):
        result = True

    return result


def is_specific_call(elem, call_type):
    """Check if the given element corresponds to a specific method call

        Keyword arguments:
        elem -- part of ast node
        call_type -- type of the call: fit, evaluate, add

        Returns: boolean
    """

    is_scall = False

    if (isinstance(elem, ast.Assign)
        and isinstance(elem.value, ast.Call) \
        and isinstance(elem.value.func, ast.Attribute) \
        and elem.value.func.attr == call_type) \
            or (isinstance(elem, ast.Expr)
                and isinstance(elem.value, ast.Call)
                and hasattr(elem.value.func, 'attr')
                and elem.value.func.attr == call_type):
        is_scall = True

    return is_scall


def save_original_model_params(model):
    dropout_layers = {}

    for attr, value in model.__dict__.items():
        if attr == "optimizer":
            lr = model.__dict__.get('optimizer').__dict__.get('learning_rate')
            lr_value = tf.keras.backend.get_value(lr)
            props.model_properties["learning_rate"] = lr_value

    if model.layers:
        props.model_properties["layers_num"] = len(model.layers)

        for ind, layer in enumerate(model.layers):
            if isinstance(layer, keras.layers.core.Dropout):
                dropout_layers[ind] = [layer.name, layer.rate]

        props.model_properties["dropout_layers"] = dropout_layers

    else:
        print("model has no layers")

def save_original_fit_params(x = None, epochs = None, batch_size = None):
    # if x.any():
    if x is not None:
        try:
            props.model_properties["x_train_len"] = len(x)
        except:
            props.disable_batching["applicable"] = False
            props.change_batch_size["applicable"] = False
    else:
        props.disable_batching["applicable"] = False
        props.change_batch_size["applicable"] = False

    props.model_properties["epochs"] = epochs
    props.model_properties["batch_size"] = batch_size

def is_training_call(elem):
    """Check if the given node corresponds to the call to fit/fit_generator

        Keyword arguments:
        elem - ast node

        Returns: boolean
    """

    is_call = False

    if (isinstance(elem, ast.Assign)
        and isinstance(elem.value, ast.Call) \
        and isinstance(elem.value.func, ast.Attribute) \
        # and elem.value.func.attr == 'fit') \
        and elem.value.func.attr in ('fit', 'fit_generator')) \
            or (isinstance(elem, ast.Expr)
                and isinstance(elem.value, ast.Call)
                and hasattr(elem.value.func, 'attr')
                # and elem.value.func.attr == 'fit'):
                and elem.value.func.attr in ('fit', 'fit_generator')):
        is_call = True

    return is_call


####################################################   ####################################################################
###################################### Mutation Functions ##############################################################

def model_from_config(model, tmp):
    if isinstance(model, KES):
        model = KS.from_config(tmp)
    elif isinstance(model, KEM):
        model = KM.from_config(tmp)
    elif isinstance(model, TKES):
        model = TKS.from_config(tmp)
    elif isinstance(model, TKEM):
        model = TKM.from_config(tmp)
    else:
        print("raise,log we have probllems")

    return model