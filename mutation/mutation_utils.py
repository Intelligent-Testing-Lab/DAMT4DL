# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import ast
import shutil

from io import StringIO
from utils import constants
from utils.unparse import Unparser

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


def generate_import_nodes():
    """
    Generate import nodes for the prepared model
    """
   
    import_nodes = []

    # add the import nodes for the operators
    # for imp in constants.operator_lib:
    #     import_nodes.append(
    #         ast.ImportFrom(module=constants.operator_mod, names=[
    #             ast.alias(name=imp, asname=None),
    #         ], level=0)) 

    # TODO based on the tasks to update the import nodes
    # import_nodes.append(
    #     ast.ImportFrom(module="utils", names=[
    #         ast.alias(name="properties", asname=None),
    #     ], level=0))

    # import_nodes.append(
    #     ast.ImportFrom(module="keras", names=[
    #         ast.alias(name="optimizers", asname=None),
    #     ], level=0))

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