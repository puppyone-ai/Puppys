import re
import ast


def replace_formatted_strings(
    line: str,
    local_vars: dict
) -> str:
    """
    Replace formatted parts of the string with actual values from local_vars.

    Args:
        line (str): The line to replace formatted strings in.
        local_vars (dict): The local variables to use for replacement.

    Returns:
        str: The line with formatted strings replaced.
    """

    pattern = re.compile(r"\{(.*?)\}")
    matches = pattern.findall(line)

    for match in matches:
        if match in local_vars:
            line = line.replace(f"{{{match}}}", str(local_vars[match]))
    return line


def replace_function_arguments(
    line: str,
    local_vars: dict
) -> str:
    """
    Replace function arguments in the line with actual values from local_vars.

    Args:
        line (str): The line to replace function arguments in.
        local_vars (dict): The local variables to use for replacement.

    Returns:
        str: The line with function arguments replaced.
    """

    # Parse the line into an AST
    tree = ast.parse(line, mode="exec")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            for idx, arg in enumerate(node.args):
                if isinstance(arg, ast.Name) and arg.id in local_vars:
                    node.args[idx] = ast.Constant(value=local_vars[arg.id], kind=None)

    # Unparse the modified AST back into a string
    new_line = ast.unparse(tree)
    return new_line


def parse_code2str(
    source_code: str,
    local_vars: dict
) -> list:
    """
    Parse the source code and extract the function body code.

    Args:
        source_code (str): The source code to parse.
        local_vars (dict): The local variables to use for replacement.

    Returns:
        list: The list of function body codes, each element is a code block instead of one line of code.
    """

    # Replace formatted strings with actual values from local_vars
    replaced_code = replace_formatted_strings(source_code, local_vars)

    # Split the source code into lines and keep the line endings
    lines = replaced_code.splitlines(keepends=True)

    # Find the first non-empty line and get its indentation
    first_non_empty_line = next(line for line in lines if line.strip())
    min_indent = len(re.match(r"^\s*", first_non_empty_line).group())

    # Remove the minimum indentation from each line
    adjusted_lines = [line[min_indent:] if len(line.strip()) > 0 else line for line in lines]

    # Recombine the adjusted lines
    adjusted_source_code = "".join(adjusted_lines)

    # Parse the adjusted source code into an AST
    tree = ast.parse(adjusted_source_code)

    function_body_code = []
    # Walk through the AST and extract the function body code
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for body_node in node.body:
                # Convert each statement to source code and append to the result
                body_code_block = ast.unparse(body_node)
                body_code_block = body_code_block + "\n" if not body_code_block.endswith("\n") else body_code_block
                function_body_code.append(body_code_block)

    return function_body_code

