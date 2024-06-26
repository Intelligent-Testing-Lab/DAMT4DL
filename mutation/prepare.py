import ast
import shutil

from io import StringIO
from utils import constants
from utils.unparse import Unparser

def prepare_model(original_path, save_path):
    """
    Convert the original model code to human-readable format and save it as prepared model
    """

    # read the original model code
    tree = None
    with open(original_path, "r") as source:
        tree = ast.parse(source.read())
    

    # convert the original model code to human-readable format
    imports_inserted = False
    for node in ast.walk(tree):
        if hasattr(node, 'body') and isinstance(node.body, list):
            for ind, x in enumerate(node.body):
                if not imports_inserted:
                    if is_import(x):
                        import_nodes = generate_import_nodes()
                        for i, n in enumerate(import_nodes):
                            node.body.insert(ind + i + 1, n)

                        imports_inserted = True
    # fix the missing locations in ast tree
    ast.fix_missing_locations(tree)

    # unparse the tree and save the prepared model code
    unparse_tree(tree, save_path)


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



    