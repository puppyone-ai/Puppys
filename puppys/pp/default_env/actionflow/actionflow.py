import inspect
from puppys.env.env import Env
from puppys.pp.default_env.actionflow.parse import parse_code2str
from puppys.pp.actions.load_env import load_env
from puppys.pp.default_env.actionflow.puppy_ast_exec import puppy_exec
import threading
from contextlib import redirect_stdout, redirect_stderr
import io
import sys

# a default essential env for agent
class Actionflow(Env):
    visible = False

    def __init__(self, puppy_instance, *args, function, printing_mode=None,  **kwargs):
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
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # execute the code
            puppy_exec(code, self.puppy_instance.puppy_vars.global_dict, self.puppy_instance.puppy_vars.runtime_dict)

    def run(self, **kwargs):

        #check if the kwargs fits the arg
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
