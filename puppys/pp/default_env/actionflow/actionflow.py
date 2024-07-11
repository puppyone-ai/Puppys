import inspect
from puppys.env.env import Env
from puppys.pp.default_env.actionflow.parse import parse_code2str
from puppys.pp.actions.load_env import load_env
from puppys.pp.default_env.actionflow.puppy_ast_exec import puppy_exec
import threading
from contextlib import redirect_stdout, redirect_stderr
import io
import sys


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
        self.all_code = ""
        self.current_action_code = ""
        self.errors = ""
        self.current_code = ""


    def puppy_exec(self, code):

        """
        Executes the given code with redirected stdout and stderr.
        Args:
            code (str): The code to execute.
        """
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # execute the code
            puppy_exec(code, self.puppy_instance.puppy_vars.global_dict, self.puppy_instance.puppy_vars.runtime_dict)

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
        
        self.all_code = parse_code2str(self.source_code, self.puppy_instance.puppy_vars.runtime_dict)
        print("self.all_code: ", self.all_code)

        # return self.puppy_exec(self.all_code)
        
        combined_output = []
        combined_errors = []
        
        for current_code in self.all_code:
            self.current_code = current_code
            self.puppy_exec(current_code)
            
            if self.buffer_outputs:
                combined_output.append(self.output_buffer.getvalue())
                combined_errors.append(self.error_buffer.getvalue())
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
            return None, None
