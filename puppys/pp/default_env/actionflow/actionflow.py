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
    It inherits from the Env class as an invisible env.

    Init Args:
        puppy_instance (any): The puppy instance that runs all the actions.
        *args: The arguments.
        function (any): The function to run.
        printing_mode (str): The printing mode, can either be `buffer` or `terminal`. The default is `terminal`.
        save_actionflow (bool): Whether to save the actionflow. The default is True.
        save_instance (bool): Whether to save the instance. The default is True.
        **kwargs: The keyword arguments.
    """
    visible = False

    def __init__(
        self, 
        puppy_instance: any, 
        *args, 
        function: any, 
        printing_mode: str = None, 
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

        # Set up the code storages for actionflow
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
        Write the code to a python file. Exceptions will be raised if the file cannot be written.

        Args:
            code (list): The code to write.
            sig_str (str): The signature string.
            actionflow_root_path (str): The root path to save the actionflow file. The default is "user_case_history".
            actionflow_file_name (str): The actionflow file name. The default is "temp_actionflow.
        """

        if not os.path.exists(actionflow_root_path):
            os.makedirs(actionflow_root_path)

        file_path = os.path.join(actionflow_root_path, actionflow_file_name)

        # Adjust the indentation of the code
        code_with_indentation = ["    " + line.rstrip("\n") for lines in code for line in lines.splitlines(keepends=True) if line.strip()]
        indent_keywords = ["def", "if", "else", "elif", "for", "while", "try", "except", "finally", "with", "class"]
        for i, line in enumerate(code_with_indentation):
            if i > 0:
                leading_spaces = len(line) - len(line.lstrip())
                prev_lead_spaces = len(code_with_indentation[i-1]) - len(code_with_indentation[i-1].lstrip())
                if leading_spaces > prev_lead_spaces:
                    if not any(code_with_indentation[i-1].lstrip().startswith(kw) for kw in indent_keywords):
                        # Calculate the number of spaces to remove
                        excess_spaces = leading_spaces - prev_lead_spaces
                        # Remove the extra spaces
                        code_with_indentation[i] = line[excess_spaces:]
                    elif leading_spaces - prev_lead_spaces > 4:
                        code_with_indentation[i] = line[leading_spaces - prev_lead_spaces - 4:]

        code_with_indentation = "\n".join(code_with_indentation)
        code = f"def actionflow{sig_str}:\n" + code_with_indentation

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code + "\n")
            print(f"{self.GREEN}Successfully write the code to `{file_path}`!{self.RESET}")
        except Exception as e:
            print(f"{self.RED}Fail writing file: {e}{self.RESET}")

    def save_puppy_instance(
        self, 
        root_path: str = "user_case_history", 
        file_name: str = "puppy_instance.pkl"
    ) -> None:
        """
        Save the puppy_instance to a pickle file. Exceptions will be raised if the instance cannot be saved.

        Args:
            root_path (str): The root path to save the instance file. The default is "user_case_history".
            file_name (str): The instance file name. The default is "puppy_instance.pkl".
        """

        if not os.path.exists(root_path):
            os.makedirs(root_path)

        file_path = os.path.join(root_path, file_name)

        try:
            with open(file_path, "wb") as output_file:
                dill.dump(self.puppy_instance, output_file)
            print(f"{self.GREEN}Successfully save the instance to `{file_path}`!{self.RESET}")
        except Exception:
            try:
                serializable_instance = self._filter_non_serializable(self.puppy_instance)
                with open(file_path, "wb") as output_file:
                    dill.dump(serializable_instance, output_file)
                print(f"{self.GREEN}Successfully save the instance to `{file_path}`!{self.RESET}")
            except Exception as e:
                print(f"{self.RED}Fail saving instance: {e}{self.RESET}")

    def _filter_non_serializable(self, obj):
        serializable_obj = {}
        for key, value in obj.__dict__.items():
            try:
                dill.dumps(value)
                serializable_obj[key] = value
            except dill.PicklingError:
                continue
            except TypeError:
                continue
        return serializable_obj

    def load_puppy_instance(
        self, 
        root_path: str = "user_case_history", 
        file_name: str = "puppy_instance.pkl"
    ) -> any:
        """
        Load the puppy_instance from a pickle file. Exceptions will be raised if the instance cannot be loaded.

        Args:
            root_path (str): The root path to load the instance file. The default is "user_case_history".
            file_name (str): The instance file name. The default is "puppy_instance.pkl".
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

        Args:
            combined_output (list): The combined output list.
            combined_errors (list): The combined error list.
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

        Args:
            node_num (int): The node number to run. If -1, then run all the nodes. 
            num_of_action (int): The number of actions to run. 
            handle_exceptions (bool): Whether to handle exceptions. 
            max_length (int): The maximum length of the code to show. 
            use_command_line (bool): Whether to use the command line. 
            updates (dict): The updates to the runtime dict. The default is None for `use_command_line` is True. This argument is required if the `use_command_line` is False.

        Returns:
            list: The results of the test run. The first element contains the full output while the rest contains the difference to the first element to save the result length.
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

    def check_required_args(
        self, 
        kwargs
    ) -> None:
        """
        Check if the required arguments are present in kwargs.

        Args:
            kwargs (dict): The keyword arguments.

        Raises:
            ValueError: If any required argument is missing.
        """

        required_args = [arg for arg in self.args_spec.args if arg != "self"]
        missing_args = [arg for arg in required_args if arg not in kwargs]

        if missing_args:
            raise ValueError(f"Missing required arguments: {', '.join(missing_args)}")

    def load_and_update_env(
        self, 
        kwargs
    ) -> None:
        """
        Load the pre-defined environments and update the runtime environment.

        Args:
            kwargs (dict): The keyword arguments.
        """

        load_env(self.puppy_instance, target=Env)
        self.puppy_instance.puppy_vars.runtime_dict.update(kwargs)
        self.future_codes = parse_code2str(self.source_code, self.puppy_instance.puppy_vars.runtime_dict)

    def execute_current_code(
        self, 
    ) -> None:
        """
        Execute the current code and handle exceptions.
        """

        try:
            self.current_code = replace_function_arguments(
                self.current_code,
                self.puppy_instance.puppy_vars.runtime_dict
            )
            self.puppy_exec(self.current_code)
        except KeyboardInterrupt:
            print(f"{self.RED}Error: KeyboardInterrupt{self.RESET}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            import traceback
            tb = traceback.TracebackException.from_exception(e)
            concise_traceback = "".join(tb.format_exception_only())
            print(f"{self.RED}Error: {concise_traceback}{self.RESET}", file=sys.stderr)
            sys.exit(1)
        finally:
            if self.save_actionflow:
                code_to_write = self.history_codes + [self.current_code]
                self.write_to_py_file(code_to_write, str(self.signature))
            if self.save_instance:
                self.save_puppy_instance()

            self.history_codes.append(self.current_code)

    def run(
        self, 
        **kwargs
    ) -> tuple:
        """
        Run the agent's actionflow by 'value'.

        Args:
            **kwargs: The keyword arguments.

        Returns:
            tuple: The combined output and error strings. Empty if the buffer_outputs is False, as the results are shown immediately in the terminal after each code execution.
        """

        self.check_required_args(kwargs)
        self.load_and_update_env(kwargs)

        combined_output = []
        combined_errors = []

        while self.future_codes:
            self.current_code = self.future_codes.pop(0)
            self.execute_current_code()
            if self.buffer_outputs:
                self.handle_buffer_outputs(combined_output, combined_errors)

        if self.buffer_outputs:
            output_str = "\n".join(combined_output)
            error_str = "\n".join(combined_errors)
            return output_str, error_str
        else:
            return None, None

