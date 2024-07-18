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
import dill


class Actionflow(Env):
    """
    Actionflow is a default essential env for agent
    It shows the agent's action over time
    """
    visible = False

    def __init__(self, puppy_instance, *args, function, printing_mode=None, save_actionflow=True, save_instance=True, **kwargs):
        super().__init__(*args, **kwargs)

        self.puppy_instance = puppy_instance
        self.function = function
        self.save_actionflow = save_actionflow
        self.save_instance = save_instance

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
        
        # set the color for printing
        self.RED = "\033[31m"
        self.RESET = "\033[0m"


    def puppy_exec(self, code):

        """
        Executes the given code with redirected stdout and stderr.
        Args:
            code (str): The code to execute.
        """
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # execute the code
            puppy_exec(code, self.puppy_instance.puppy_vars.global_dict, self.puppy_instance.puppy_vars.runtime_dict)
    
    def write_to_py_file(self, code: list, sig_str: str, actionflow_root_path: str = "user_case_history", actionflow_file_name: str = "temp_actionflow_code.py"):
        """
        Write the code to a python file
        """

        if not os.path.exists(actionflow_root_path):
            os.makedirs(actionflow_root_path)

        file_path = os.path.join(actionflow_root_path, actionflow_file_name)
        code_with_indentation = "\n".join(["    " + line.rstrip('\n') for lines in code for line in lines.splitlines(keepends=True) if line.strip()])
        code = f"def actionflow{sig_str}:\n" + code_with_indentation

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code + '\n')
        except Exception as e:
            print(f"{self.RED}Fail writing file: {e}{self.RESET}")

    def save_puppy_instance(self, root_path: str = "user_case_history", file_name: str = "puppy_instance.pkl"):
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

    def load_puppy_instance(self, root_path: str = "user_case_history", file_name: str = "puppy_instance.pkl"):
        """
        Load the puppy_instance from a pickle file
        """
        
        if not os.path.exists(root_path):
            os.makedirs(root_path)

        file_path = os.path.join(root_path, file_name)

        try:
            with open(file_path, 'rb') as input_file:
                loaded_instance = dill.load(input_file)
            if isinstance(loaded_instance, self.puppy_instance.__class__):
                return loaded_instance
            else:
                raise ValueError(f"The loaded instance is not an instance of {self.puppy_instance.__class__}")
        except Exception as e:
            print(f"{self.RED}Fail loading instance: {e}{self.RESET}")
            return None

    def handle_buffer_outputs(self, combined_output: list, combined_errors: list):
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

    def test_run(self, node_num: int, num_of_action: int, handle_exceptions: bool = True, mode: str = 'inline', **kwargs):
        """
        Test run the saved actionflow in debug mode.
        
        ## Parameters:
        ### node_num (int): 
        The number of the node to start execution from. The node numbers are as follows:
        - 0: The current code.
        - 1 to len(future_codes): The corresponding index in future_codes.
        - -1: All code nodes from the current code to the last element of future_codes.
        - -2: All code nodes, including history_codes, the current code, and future_codes.

        ### num_of_action (int):
        The number of times to execute the actionflow. This allows repeated execution to test stability and success rate.

        ### handle_exceptions (bool):
        Whether to handle exceptions during execution. If True, the function will stop and return the exception when an error occurs. If False, the exception message will be captured and included in the results list, and execution will continue.

        ### mode (str):
        The mode of execution. It can be either 'inline' or 'commandline'.
        - 'inline': In this mode, the function applies monkey patching to update the attribute values of the loaded puppy_instance from the local file based on the provided kwargs. The function then runs the code node(s) num_of_action times.
        - 'commandline': In this mode, the function provides an interactive command-line interface for the developer to select which attributes to modify. The current value is displayed, and the developer can enter new values. After updating values, the developer can choose to test run or continue updating values.

        ### **kwargs: 
        Keyword arguments used for inline mode to update the attribute values of the puppy_instance.

        ## Returns:
        ### list:
        A list of results from the executions, each element representing the output and error messages (if any) for one execution. If handle_exceptions is set to False, exceptions will be included in the list as well.
        """
        results = []

        def execute_code(node_num):
            """
            Execute code from the specified node number.
            """
            if node_num == -2:
                codes_to_execute = self.history_codes + [self.current_code] + self.future_codes
            elif node_num == -1:
                codes_to_execute = [self.current_code] + self.future_codes
            else:
                if node_num == 0:
                    codes_to_execute = [self.current_code]
                elif 0 < node_num <= len(self.future_codes):
                    codes_to_execute = self.future_codes[node_num - 1:]
                else:
                    raise ValueError(f"Invalid node_num: {node_num}")

            combined_output = []
            combined_errors = []

            for code in codes_to_execute:
                try:
                    code = replace_function_arguments(code, self.puppy_instance.puppy_vars.runtime_dict)
                    self.puppy_exec(code)
                    if self.buffer_outputs:
                        self.handle_buffer_outputs(combined_output, combined_errors)
                except Exception as e:
                    if handle_exceptions:
                        raise e
                    combined_errors.append(str(e))
                    break

            if self.buffer_outputs:
                return "\n".join(combined_output), "\n".join(combined_errors)
            else:
                return None, "\n".join(combined_errors)

        if mode == 'inline':
            # Apply monkey patching
            for key, value in kwargs.items():
                if key in self.puppy_instance:
                    setattr(self.puppy_instance, key, value)
                else:
                    raise ValueError(f"Invalid key: {key}")

        elif mode == 'commandline':
            while True:
                print("\nCurrent puppy_instance attributes and values:")
                for attr, value in vars(self.puppy_instance).items():
                    print(f"{attr}: {value}")

                modify = input("\nDo you want to modify any attribute? (yes/no): ").strip().lower()
                if modify == 'yes':
                    keep_modifying = True
                    while keep_modifying:
                        attr_to_modify = input("Enter the attribute name: ").strip()
                        if hasattr(self.puppy_instance, attr_to_modify):
                            current_value = getattr(self.puppy_instance, attr_to_modify)
                            print(f"Current value of {attr_to_modify}: {current_value}")
                            new_value = input("Enter the new value: ").strip()
                            setattr(self.puppy_instance, attr_to_modify, new_value)
                            modify = input("Do you want to modify any other attribute? (yes/no): ").strip().lower()
                            if modify == 'no':
                                keep_modifying = False
                        else:
                            print(f"Attribute {attr_to_modify} does not exist.")
                elif modify == 'no':
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

        for _ in range(num_of_action):
            try:
                result = execute_code(node_num)
                results.append(result)
            except Exception as e:
                results.append(f"Exception: {e}")
                if handle_exceptions:
                    break

        return results


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
            self.errors = error_str
            return output_str, error_str
        else:
            return None, None
