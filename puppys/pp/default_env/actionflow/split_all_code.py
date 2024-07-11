import ast

def remove_inner_newlines(code: str) -> str:
    """
    Remove inner newlines from the code while preserving its structure.
    
    Args:
        code (str): The code from which to remove inner newlines.
        
    Returns:
        str: The code with inner newlines removed.
    """
    class InnerNewlineRemover(ast.NodeTransformer):
        def visit_Str(self, node):
            # Preserve newlines in string literals
            return node

        def visit_JoinedStr(self, node):
            # Preserve newlines in f-string literals
            return node

    tree = ast.parse(code)
    remover = InnerNewlineRemover()
    new_tree = remover.visit(tree)

    # Convert the modified AST back to source code
    new_code = ast.unparse(new_tree)
    return new_code

def split_code_safely(code: str):
    """
    Split code into lines safely, preserving the structure of code blocks.

    Args:
        code (str): The code to split.

    Returns:
        List[str]: List of code lines with preserved structure.
    """
    lines = code.splitlines(keepends=True)
    node_lines = []

    class CodeVisitor(ast.NodeVisitor):
        def visit(self, node):
            if hasattr(node, 'lineno'):
                node_lines.append(node.lineno - 1)
            self.generic_visit(node)

    tree = ast.parse(code)
    visitor = CodeVisitor()
    visitor.visit(tree)

    node_lines = sorted(set(node_lines))
    return [lines[i] for i in node_lines]

def indent_code_lines(code: str, indent: str = "    ") -> str:
    """
    Indent code lines safely.

    Args:
        code (str): The code to indent.
        indent (str): The indentation string.

    Returns:
        str: The indented code.
    """
    # First remove inner newlines
    code = remove_inner_newlines(code)

    # Then split code into lines safely
    lines = split_code_safely(code)

    # Indent the lines
    indented_lines = [indent + line for line in lines if line.strip()]
    return indented_lines


if __name__ == "__main__":
    code = """
def example_function():
    a_dict = {
        "a": "a", 
        "b": "b", 
        "c": "c"
    }
    
    multi_line_string = \"\"\"This is a 
    multi-line string 
    and should not be
    altered.\"\"\"

    if True:
        print("This is a test.")
    for i in range(5):
        print(i)
    """

    indented_code = indent_code_lines(code)
    print(indented_code)
