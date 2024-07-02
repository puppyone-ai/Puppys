import ast


def exec_ast_with_context(node: ast.Module, global_dict: dict, local_dict: dict):
    """
    Execute AST nodes with proper context handling to maintain state across different parts of the AST.
    """
    if isinstance(node, ast.Module):
        for stmt in node.body:
            exec_ast_with_context(stmt, global_dict, local_dict)

    elif isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.Expr)):
        # Execute code for imports, assignments, and expressions
        exec(compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec"), global_dict, local_dict)
        global_dict.update(local_dict)
    
    elif isinstance(node, ast.For):
        # Handle 'for' loop
        iter_obj = eval(compile(ast.Expression(node.iter), filename="<ast>", mode="eval"), global_dict, local_dict)
        for item in iter_obj:
            local_dict[node.target.id] = item
            for stmt in node.body:
                exec_ast_with_context(stmt, global_dict, local_dict)

    elif isinstance(node, ast.If):
        # Handle 'if' conditionals
        test_result = eval(compile(ast.Expression(node.test), filename="<ast>", mode="eval"), global_dict, local_dict)
        body = node.body if test_result else node.orelse
        for stmt in body:
            exec_ast_with_context(stmt, global_dict, local_dict)
    
    elif isinstance(node, ast.While):
        # Handle 'while' loop
        while eval(compile(ast.Expression(node.test), filename="<ast>", mode="eval"), global_dict, local_dict):
            for stmt in node.body:
                exec_ast_with_context(stmt, global_dict, local_dict)

    else:
        # Handle all other types by executing directly
        exec(compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec"), global_dict, local_dict)



def execute_python_code(code):
    global_dict = {}
    local_dict = {}
    parsed_ast = ast.parse(code)
    exec_ast_with_context(parsed_ast, global_dict, local_dict)


test_code = """
import random
x=5
print('[RandomNum]', [random.randint(1, x) for _ in range(10)])
def foo():
    print('[RandomNum]', [random.randint(1, 100) for _ in range(10)])
class Bar:
    def method(self):
        return random.choice([1, 2, 3])
foo()
b = Bar()
print(b.method())

# Test for 'if' statement
x = 10
if x > 5:
    result_if = 'greater'
else:
    result_if = 'not greater'
# Test for 'for' loop
result_for = []
for i in range(3):
    result_for.append(i)

# Test for 'while' loop
count = 0
result_while = []
while count < 3:
    result_while.append(count)
    count += 1

# Function in function
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function(10)
result_finf = outer_function(5)

# Functions in for
c = 5
for i in range(3):
    c = outer_function(c)
print("c: ", c)

# Class in class
class OuterClass:
    class InnerClass:
        def inner_method(self):
            return 'inner'
    def outer_method(self):
        return self.InnerClass().inner_method()
result_cinc = OuterClass().outer_method()

# Class in function
def function_with_class():
    class FunctionClass:
        def method(self):
            return 'from_class'
    instance = FunctionClass()
    return instance.method()
result_cinf = function_with_class()

# Try exception block
try:
    1 / 0
except ZeroDivisionError:
    result_try = 'exception caught'

# All combined
def combined_test():
    if x > 0:
        for i in range(2):
            try:
                if i == 0:
                    # x = 5
                    raise ValueError('test')
            except ValueError as e:
                print(e, x)
    class CombinedClass:
        def method(self):
            return 'combined'
    return CombinedClass().method()
result_comb = combined_test()

# Outputs
print(f'IF Test: {result_if}')
print(f'FOR Loop Test: {result_for}')
print(f'WHILE Loop Test: {result_while}')
print(f'Function in Function: {result_finf}')
print(f'Class in Class: {result_cinc}')
print(f'Class in Function: {result_cinf}')
print(f'Try Exception: {result_try}')
print(f'Combined Test: {result_comb}')

# Test 1: With Statement for file handling
with open('testfile.txt', 'w') as file:
    file.write('Hello World')

import threading
def thread_function(name):
    return f'Thread {name} is running'
results = []
threads = []
for index in range(3):
    x = threading.Thread(target=lambda q, arg=index: q.append(thread_function(arg)), args=(results,))
    print(x)
    threads.append(x)
    x.start()
for thread in threads:
    thread.join()

def my_decorator(func):
    def wrapper():
        return 'Decorated ' + func()
    return wrapper
@my_decorator
def say_hello():
    return 'hello'
decorated_result = say_hello()

def count_down(num):
    while num > 0:
        yield num
        num -= 1
generator_result = list(count_down(5))

# Test 6: List Comprehension
list_comprehension_result = [x * 2 for x in range(10)]

# Test 7: Dictionary Comprehension
dict_comprehension_result = {x: x * x for x in range(5)}

# Test 8: Set Comprehension
set_comprehension_result = {x for x in 'hello world' if x not in 'aeiou'}

# Printing results for verification
print(results)
print(decorated_result)
print(generator_result)
print(list_comprehension_result)
print(dict_comprehension_result)
print(set_comprehension_result)
"""

execute_python_code(test_code)


