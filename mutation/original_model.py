import ast
import os

from mutation.mutation_utils import *

def update_orginal_model(model_path, save_path):
    """
    update the original model for training
    """
    modify_original_model(model_path, save_path)


# This function is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International
def modify_original_model(model_path, save_path):

    with open(model_path, "r") as source:
        tree = ast.parse(source.read())

    # params = {}
    keywords = []
    imports_inserted = False
    for node in ast.walk(tree):
        if hasattr(node, 'body') and isinstance(node.body, list):
            for ind, x in enumerate(node.body):
                if not imports_inserted:
                    if is_import(x):
                        import_nodes = []
                        import_nodes.append(
                            ast.ImportFrom(module="mutation", names=[
                                ast.alias(name="mutation_utils", asname=None),
                            ], level=0))
                        for i, n in enumerate(import_nodes):
                            node.body.insert(ind + i + 1, n)

                        imports_inserted = True

                if is_specific_call(x, 'compile'):
                    model_name = x.value.func.value.id
                    lr_save_node = ast.Expr(value=ast.Call(
                                func=ast.Attribute(value=ast.Name(id='mutation_utils', ctx=ast.Load()), attr='save_original_model_params',
                                                   ctx=ast.Load()), args=[ast.Name(id=model_name, ctx=ast.Load()), ],
                                keywords=[]))
                    node.body.insert(ind + 1, lr_save_node)

                if is_specific_call(x, 'fit'):

                    if hasattr(x.value, 'args') and len(x.value.args) > 0:
                        if isinstance(x.value.args[0], ast.List):
                            x_train = ast.Name(id=x.value.args[0].elts[0].id, ctx=ast.Load())
                        else:
                            x_train = ast.Name(id=x.value.args[0].id, ctx=ast.Load())

                        keywords.append(
                            ast.keyword(arg="x", value=x_train))

                    # else:
                    #     print("we have a problem here")

                    if hasattr(x.value, 'keywords') and len(x.value.keywords) > 0:
                        for k in x.value.keywords:
                            if k.arg in ("batch_size", "epochs", "x"):
                                keywords.append(k)
                    # else:
                    #     print("we have a problem here")

                    param_save_node = ast.Expr(value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='mutation_utils', ctx=ast.Load()), attr='save_original_fit_params',
                                           ctx=ast.Load()), args=[], keywords=keywords))

                    node.body.insert(ind, param_save_node)
                    break
    # fix the missing locations in ast tree
    ast.fix_missing_locations(tree)

    # unparse the ast tree, write the resulting code into py file
    unparse_tree(tree, save_path)