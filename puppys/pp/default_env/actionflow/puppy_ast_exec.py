import ast


def handle_control_flow(
    body: list, 
    global_dict: dict, 
    local_dict: dict
) -> str:
    """
    Executes each statement within a node body, handling control flow specifically.

    Args:
        body (list): The list of statements to execute.
        global_dict (dict): The global dictionary to use for execution.
        local_dict (dict): The local dictionary to use for execution.

    Returns:
        str: The control flow type if any (break or continue).
    """

    for stmt in body:
        if isinstance(stmt, ast.Break):
            return 'break'
        elif isinstance(stmt, ast.Continue):
            return 'continue'
        elif isinstance(stmt, ast.Pass):
            continue
        else:
            control_flow_type = puppy_ast_exec(stmt, global_dict, local_dict)
            if control_flow_type in ['break', 'continue']:
                return control_flow_type
    return ""

def puppy_ast_exec(
    node: any, 
    global_dict: dict, 
    local_dict: dict
) -> str:
    """
    Execute AST nodes with proper context handling to maintain state across different parts of the AST.

    Args:
        node (any): The AST node to execute.
        global_dict (dict): The global dictionary to use for execution.
        local_dict (dict): The local dictionary to use for execution.

    Returns:
        str: The control flow type if any (break or continue).
    """

    control_flow_type = ""

    if isinstance(node, ast.Module):
        for stmt in node.body:
            puppy_ast_exec(stmt, global_dict, local_dict)

    elif isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.Expr)):
        # Execute code for imports, assignments, and expressions
        exec(compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec"), global_dict, local_dict)
        global_dict.update(local_dict)

    elif isinstance(node, ast.For):
        # Handle "for" loop
        iter_obj = eval(compile(ast.Expression(node.iter), filename="<ast>", mode="eval"), global_dict, local_dict)
        for item in iter_obj:
            if isinstance(node.target, ast.Tuple):
                for idx, target in enumerate(node.target.elts):
                    local_dict[target.id] = item[idx]
            else:
                local_dict[node.target.id] = item
            control_signal = handle_control_flow(node.body, global_dict, local_dict)
            if control_signal == 'break':
                break
            elif control_signal == 'continue':
                continue

    elif isinstance(node, ast.If):
        # Handle "if" conditionals
        test_result = eval(compile(ast.Expression(node.test), filename="<ast>", mode="eval"), global_dict, local_dict)
        body = node.body if test_result else node.orelse
        control_flow_type = handle_control_flow(body, global_dict, local_dict)

    elif isinstance(node, ast.While):
        # Handle "while" loop
        while eval(compile(ast.Expression(node.test), filename="<ast>", mode="eval"), global_dict, local_dict):
            control_signal = handle_control_flow(node.body, global_dict, local_dict)
            if control_signal == 'break':
                break
            elif control_signal == 'continue':
                continue

    else:
        # Handle all other types by executing directly
        exec(compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec"), global_dict, local_dict)

    return control_flow_type


def puppy_exec(
    code: str, 
    global_dict: dict, 
    local_dict: dict
) -> None:
    global_dict.update(local_dict)
    parsed_ast = ast.parse(code)
    puppy_ast_exec(parsed_ast, global_dict, local_dict)


if __name__ == "__main__":
    test_code = """
import random
x=5
print("[RandomNum]", [random.randint(1, x) for _ in range(10)])
    """

    puppy_exec(test_code, {},{})
