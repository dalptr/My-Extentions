import ast
import astunparse
import os


class TypeHintRemover(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        node.returns = None
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        return node

    def visit_Import(self, node):
        node.names = [n for n in node.names if n.name != 'typing']
        return node if node.names else None

    def visit_ImportFrom(self, node):
        return node if node.module != 'typing' else None


def file_to_string(filename):
    if not os.path.exists(filename):
        print("%s not found !" % filename)
        return

    with open(filename, 'r') as file:
        return file.read()


def remove_type_hints(input_file, output_file=None):
    source_code = file_to_string(input_file)
    parsed_source = ast.parse(source_code)
    transformed = TypeHintRemover().visit(parsed_source)
    if output_file is not None and os.path.exists(output_file):
        with open(output_file, 'a') as file:
            file.write(astunparse.unparse(transformed))
        print("Your code snippet after removing type hints has been saved to " + output_file)
    else:
        print(astunparse.unparse(transformed))
