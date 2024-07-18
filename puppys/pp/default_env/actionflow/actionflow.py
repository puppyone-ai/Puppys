import os
import io
import sys
import dill
import inspect
import threading
from puppys.env.env import Env
from contextlib import redirect_stdout, redirect_stderr
from puppys.pp.default_env.actionflow.debug_actionflow import TestActionflow
from puppys.pp.actions.load_env import load_env
from puppys.pp.default_env.actionflow.puppy_ast_exec import puppy_exec
from puppys.pp.default_env.actionflow.parse import parse_code2str, replace_function_arguments


class Actionflow(Env):
    """
    Actionflow is a default essential env for agent.
    It shows the agent's action over time.
    """
    visible = False

    def __init__(
        self, 
        puppy_instance: any, 
        *args, 
        function: any, 
        printing_mode: bool = None, 
        save_actionflow: bool = True, 
        save_instance: bool = True, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.puppy_instance = puppy_instance
        self.function = function
        self.save_actionflow = save_actionflow
        self.save_instance = save_instance

        # If the output mode is buffer, redirect the output to the buffer
        if printing_mode == "buffer":
            self.output_buffer = io.StringIO()
            self.error_buffer = io.StringIO()
            self.buffer_outputs = True
        else:
            self.output_buffer = sys.__stdout__
            self.error_buffer = sys.__stderr__
            self.buffer_outputs = False

        # Set the trigger
        self.trigger = threading.Event()

        # Get the full source code
        self.source_code = inspect.getsource(self.function)

        # Get the function signature
        self.signature = inspect.signature(self.function)

        # Use get full args pec to get more specific information
        self.args_spec = inspect.getfullargspec(self.function)

        # Set up the all code for actionflow, and current code for the running action
        self.history_codes = []
        self.current_code = ""
        self.future_codes = []
        self.current_action_code = ""
        self.temp_current_code = {}
        self.errors = ""
        
        # Set the color for printing
        self.GREEN = "\033[32m"
        self.GREY = "\033[90m"
        self.RED = "\033[31m"
        self.RESET = "\033[0m"

    def puppy_exec(
        self, 
        code: str
    ) -> None:
        """
        Executes the given code with redirected stdout and stderr.
        Args:
            code (str): The code to execute.
        """

        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # Execute the code
            puppy_exec(code, self.puppy_instance.puppy_vars.global_dict, self.puppy_instance.puppy_vars.runtime_dict)

    def write_to_py_file(
        self, 
        code: list, 
        sig_str: str, 
        actionflow_root_path: str = "user_case_history", 
        actionflow_file_name: str = "temp_actionflow_code.py"
    ) -> None:
        """
        Write the code to a python file
        """

        if not os.path.exists(actionflow_root_path):
            os.makedirs(actionflow_root_path)

        file_path = os.path.join(actionflow_root_path, actionflow_file_name)
        code_with_indentation = "\n".join(["    " + line.rstrip("\n") for lines in code for line in lines.splitlines(keepends=True) if line.strip()])
        code = f"def actionflow{sig_str}:\n" + code_with_indentation

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code + "\n")
        except Exception as e:
            print(f"{self.RED}Fail writing file: {e}{self.RESET}")

    def save_puppy_instance(
        self, 
        root_path: str = "user_case_history", 
        file_name: str = "puppy_instance.pkl"
    ) -> None:
        """
        Save the puppy_instance to a pickle file
        """
        
        if not os.path.exists(root_path):
            os.makedirs(root_path)

        file_path = os.path.join(root_path, file_name)
        
        try:
            with open(file_path, "wb") as output_file:
                dill.dump(self.puppy_instance, output_file)
        except Exception as e:
            print(f"{self.RED}Fail saving instance: {e}{self.RESET}")

    def load_puppy_instance(
        self, 
        root_path: str = "user_case_history", 
        file_name: str = "puppy_instance.pkl"
    ) -> any:
        """
        Load the puppy_instance from a pickle file
        """
        
        if not os.path.exists(root_path):
            os.makedirs(root_path)

        file_path = os.path.join(root_path, file_name)

        try:
            with open(file_path, "rb") as input_file:
                loaded_instance = dill.load(input_file)
            if isinstance(loaded_instance, self.puppy_instance.__class__):
                return loaded_instance
            else:
                raise ValueError(f"The loaded instance is not an instance of {self.puppy_instance.__class__}")
        except Exception as e:
            print(f"{self.RED}Fail loading instance: {e}{self.RESET}")
            return None

    def handle_buffer_outputs(
        self, 
        combined_output: list, 
        combined_errors: list
    ) -> None:
        """
        Redirect the output and error buffer values to the combined output and error lists.
        """

        # Get and store the output and error buffer values
        output_buffer_value = self.output_buffer.getvalue()
        error_buffer_value = self.error_buffer.getvalue()
        if output_buffer_value.strip():
            combined_output.append(output_buffer_value)
        if error_buffer_value.strip():
            combined_errors.append(error_buffer_value)

        # Reset the buffer
        self.output_buffer.truncate(0)
        self.output_buffer.seek(0)
        self.error_buffer.truncate(0)
        self.error_buffer.seek(0)

    def test_run(
        self, 
        node_num: int, 
        num_of_action: int, 
        handle_exceptions: bool,
        max_length: int,
        use_command_line: bool, 
        updates: dict = None
    ) -> list:
        """
        Test run the saved actionflow in debug mode.
        """
        
        puppy_instance = self.load_puppy_instance()
        test_actionflow = TestActionflow(puppy_instance)
        results = test_actionflow.test_run(
            node_num, 
            num_of_action, 
            handle_exceptions,
            max_length,
            use_command_line,
            updates
        )

        return results

    def run(
        self, 
        **kwargs
    ) -> tuple:
        """
        Run the agent"s actionflow by "value'
        """

        # Check if the kwargs fits the arg
        required_args = [arg for arg in self.args_spec.args if arg != "self"]
        missing_args = [arg for arg in required_args if arg not in kwargs]

        # If missing an arg, then raise an error
        if missing_args:
            raise ValueError(f"Missing required arguments: {", ".join(missing_args)}")

        # Load the pre-defined envs
        load_env(self.puppy_instance, target=Env)

        # Update the runtime env
        self.puppy_instance.puppy_vars.runtime_dict.update(kwargs)

        self.future_codes = parse_code2str(self.source_code, self.puppy_instance.puppy_vars.runtime_dict)
        
        combined_output = []
        combined_errors = []

        while self.future_codes:
            self.current_code = self.future_codes.pop(0)

            try:
                self.current_code = replace_function_arguments(
                    self.current_code, 
                    self.puppy_instance.puppy_vars.runtime_dict
                )
                self.puppy_exec(self.current_code)
            except KeyboardInterrupt as e:
                print(f"{self.RED}Error: KeyboardInterrupt{self.RESET}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"{self.RED}Error: {e}{self.RESET}", file=sys.stderr)
                sys.exit(1)
            finally:
                if self.save_actionflow:
                    self.write_to_py_file(self.history_codes, str(self.signature))
                if self.save_instance:
                    self.save_puppy_instance()

            # Update the history code
            self.history_codes.append(self.current_code)
            
            if self.buffer_outputs:
                self.handle_buffer_outputs(combined_output, combined_errors)

        if self.buffer_outputs:
            output_str = "\n".join(combined_output)
            error_str = "\n".join(combined_errors)
            return output_str, error_str
        else:
            return None, None

