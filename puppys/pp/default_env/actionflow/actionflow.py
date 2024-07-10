import inspect
from puppys.env.env import Env
from puppys.pp.default_env.actionflow.parse import parse_code2str
from puppys.pp.actions.load_env import load_env
from puppys.pp.default_env.actionflow.puppy_ast_exec import puppy_exec
import threading
from contextlib import redirect_stdout, redirect_stderr
import re
import io
import sys
import ast


def replace_formatted_string(code: str, local_dict: dict) -> str:
    """
    Replace formatted string parts with their actual values from the local dictionary
    only if the line of code is in the format: self.do(...) or self.do_check(...).
    """

    class FormatStringVisitor(ast.NodeVisitor):
        def __init__(self):
            self.formatted_strings = []

        def visit_JoinedStr(self, node):
            self.formatted_strings.append(node)
            self.generic_visit(node)

    class FormatStringReplacer(ast.NodeTransformer):
        def __init__(self, local_dict):
            self.local_dict = local_dict

        def visit_JoinedStr(self, node):
            # Replace formatted parts with actual values
            new_values = []
            for value in node.values:
                if isinstance(value, ast.FormattedValue):
                    eval_value = eval(ast.unparse(value.value), {}, self.local_dict)
                    new_values.append(ast.Constant(value=str(eval_value)))
                else:
                    new_values.append(value)
            node.values = new_values
            return node

    def should_replace_line(line):
        return line.strip().startswith("self.do(") or line.strip().startswith("self.do_check(")

    # Split the code into lines
    lines = code.split("\n")

    # Process each line individually
    new_lines = []
    for line in lines:
        if should_replace_line(line):
            # Parse the line into an AST
            tree = ast.parse(line)
            
            # Find all formatted strings
            visitor = FormatStringVisitor()
            visitor.visit(tree)
            
            # Replace formatted strings with actual values
            replacer = FormatStringReplacer(local_dict)
            new_tree = replacer.visit(tree)
            
            # Convert the modified AST back to source code
            new_line = ast.unparse(new_tree).strip()
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # Recombine the lines
    new_code = "\n".join(new_lines)
    return new_code



class Actionflow(Env):
    """
    Actionflow is a default essential env for agent
    It shows the agent's action over time
    """
    visible = False

    def __init__(self, puppy_instance, *args, function, printing_mode=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.puppy_instance = puppy_instance
        self.function = function

        # if the output mode is buffer, redirect the output to the buffer
        if printing_mode == 'buffer':
            self.output_buffer = io.StringIO()
            self.error_buffer = io.StringIO()
        else:
            self.output_buffer = sys.__stdout__
            self.error_buffer = sys.__stderr__

        # set the trigger
        self.trigger = threading.Event()

        # get the full source code
        self.source_code = inspect.getsource(self.function)

        # get the function signature
        self.signature = inspect.signature(self.function)

        # or use  get full args pec to get more specific information
        self.args_spec = inspect.getfullargspec(self.function)

        # set up the all code for actionflow, and current code for the running action
        self.all_code = parse_code2str(self.source_code)
        self.current_action_code = ""
        self.errors = ""

    def puppy_exec(self, code):

        """
        Executes the given code with redirected stdout and stderr.
        Args:
            code (str): The code to execute.
        """
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # Handle Formatted Strings
            formatted_code = replace_formatted_string(code, self.puppy_instance.puppy_vars.runtime_dict)
            self.all_code = self.all_code.replace(code, formatted_code)
            # execute the code
            puppy_exec(formatted_code, self.puppy_instance.puppy_vars.global_dict, self.puppy_instance.puppy_vars.runtime_dict)

    def run(self, **kwargs):

        """
        run the agent's actionflow by 'value'
        """
        # check if the kwargs fits the arg
        required_args = [arg for arg in self.args_spec.args if arg != 'self']
        missing_args = [arg for arg in required_args if arg not in kwargs]

        # if missing an arg, then raise an error
        if missing_args:
            raise ValueError(f"Missing required arguments: {', '.join(missing_args)}")

        # load the pre-defined envs
        load_env(self.puppy_instance, target=Env)

        # update the runtime env
        self.puppy_instance.puppy_vars.runtime_dict.update(kwargs)

        return self.puppy_exec(self.all_code)
