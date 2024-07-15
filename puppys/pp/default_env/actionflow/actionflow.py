import inspect
from puppys.env.env import Env
from puppys.pp.default_env.actionflow.parse import parse_code2str, replace_function_arguments
from puppys.pp.actions.load_env import load_env
from puppys.pp.default_env.actionflow.puppy_ast_exec import puppy_exec
import threading
from contextlib import redirect_stdout, redirect_stderr
import os
import io
import sys


class Actionflow(Env):
    """
    Actionflow is a default essential env for agent
    It shows the agent's action over time
    """
    visible = False

    def __init__(self, puppy_instance, *args, function, printing_mode=None, save_actionflow=True, actionflow_root_path: str = "user_case_history", actionflow_file_name: str = "temp_actionflow_code.py", **kwargs):
        super().__init__(*args, **kwargs)

        self.puppy_instance = puppy_instance
        self.function = function
        self.save_actionflow = save_actionflow
        self.actionflow_root_path = actionflow_root_path
        self.actionflow_file_name = actionflow_file_name

        # if the output mode is buffer, redirect the output to the buffer
        if printing_mode == 'buffer':
            self.output_buffer = io.StringIO()
            self.error_buffer = io.StringIO()
            self.buffer_outputs = True
        else:
            self.output_buffer = sys.__stdout__
            self.error_buffer = sys.__stderr__
            self.buffer_outputs = False

        # set the trigger
        self.trigger = threading.Event()

        # get the full source code
        self.source_code = inspect.getsource(self.function)

        # get the function signature
        self.signature = inspect.signature(self.function)

        # or use  get full args pec to get more specific information
        self.args_spec = inspect.getfullargspec(self.function)

        # set up the all code for actionflow, and current code for the running action
        self.history_codes = []
        self.current_code = ""
        self.future_codes = []
        self.current_action_code = ""
        self.temp_current_code = {}
        self.errors = ""


    def puppy_exec(self, code):

        """
        Executes the given code with redirected stdout and stderr.
        Args:
            code (str): The code to execute.
        """
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # execute the code
            puppy_exec(code, self.puppy_instance.puppy_vars.global_dict, self.puppy_instance.puppy_vars.runtime_dict)
    
    def write_to_py_file(self, code: list, sig_str: str) -> None:
        """
        Write the code to a python file
        """

        if not os.path.exists(self.actionflow_root_path):
            os.makedirs(self.actionflow_root_path)

        file_path = os.path.join(self.actionflow_root_path, self.actionflow_file_name)
        code_with_indentation = "\n".join(["    " + line.rstrip('\n') for lines in code for line in lines.splitlines(keepends=True) if line.strip()])
        code = f"def actionflow{sig_str}:\n" + code_with_indentation

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code + '\n')
        except Exception as e:
            print(f"Unexpected Error: {e}")

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

        self.future_codes = parse_code2str(self.source_code, self.puppy_instance.puppy_vars.runtime_dict)
        
        combined_output = []
        combined_errors = []

        while self.future_codes:
            self.current_code = self.future_codes.pop(0)

            try:
                self.current_code = replace_function_arguments(self.current_code, self.puppy_instance.puppy_vars.runtime_dict)
                print("self.current_code: ", self.current_code)
                self.puppy_exec(self.current_code)
            except KeyboardInterrupt:
                if self.save_actionflow:
                    self.write_to_py_file(self.history_codes, str(self.signature))

            self.history_codes.append(self.current_code)
            
            if self.buffer_outputs:
                # get and store the output and error buffer values
                output_buffer_value = self.output_buffer.getvalue()
                error_buffer_value = self.error_buffer.getvalue()
                if output_buffer_value.strip():
                    combined_output.append(output_buffer_value)
                if error_buffer_value.strip():
                    combined_errors.append(error_buffer_value)

                # reset the buffer
                self.output_buffer.truncate(0)
                self.output_buffer.seek(0)
                self.error_buffer.truncate(0)
                self.error_buffer.seek(0)

        if self.buffer_outputs:
            output_str = "\n".join(combined_output)
            error_str = "\n".join(combined_errors)
            self.errors = error_str
            return output_str, error_str
        else:
            if self.save_actionflow:
                self.write_to_py_file(self.history_codes, str(self.signature))
            return None, None
