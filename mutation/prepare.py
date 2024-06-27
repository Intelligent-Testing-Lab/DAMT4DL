import ast

from mutation.mutation_utils import *

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



    