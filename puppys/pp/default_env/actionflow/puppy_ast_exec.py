import ast


def puppy_ast_exec(node: ast.Module, global_dict: dict, local_dict: dict):
    """
    Execute AST nodes with proper context handling to maintain state across different parts of the AST.
    """
    if isinstance(node, ast.Module):
        for stmt in node.body:
            puppy_ast_exec(stmt, global_dict, local_dict)

    elif isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.Expr)):
        # Execute code for imports, assignments, and expressions
        exec(compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec"), global_dict, local_dict)
        global_dict.update(local_dict)

    elif isinstance(node, ast.For):
        # Handle 'for' loop
        iter_obj = eval(compile(ast.Expression(node.iter), filename="<ast>", mode="eval"), global_dict, local_dict)
        for item in iter_obj:
            if isinstance(node.target, ast.Tuple):
                for idx, target in enumerate(node.target.elts):
                    local_dict[target.id] = item[idx]
            else:
                local_dict[node.target.id] = item
            for stmt in node.body:
                puppy_ast_exec(stmt, global_dict, local_dict)

    elif isinstance(node, ast.If):
        # Handle 'if' conditionals
        test_result = eval(compile(ast.Expression(node.test), filename="<ast>", mode="eval"), global_dict, local_dict)
        body = node.body if test_result else node.orelse
        for stmt in body:
            puppy_ast_exec(stmt, global_dict, local_dict)

    elif isinstance(node, ast.While):
        # Handle 'while' loop
        while eval(compile(ast.Expression(node.test), filename="<ast>", mode="eval"), global_dict, local_dict):
            for stmt in node.body:
                puppy_ast_exec(stmt, global_dict, local_dict)

    else:
        # Handle all other types by executing directly
        exec(compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec"), global_dict, local_dict)


def puppy_exec(code, global_dict: dict, local_dict: dict):
    global_dict.update(local_dict)
    parsed_ast = ast.parse(code)
    puppy_ast_exec(parsed_ast, global_dict, local_dict)


if __name__ == "__main__":
    test_code = """
    import random
    x=5
    print('[RandomNum]', [random.randint(1, x) for _ in range(10)])
    """

    puppy_exec(test_code, {},{})