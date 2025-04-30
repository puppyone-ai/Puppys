import os
import copy
import json
import dill
import pickle
from puppys.pp.default_env.actionflow.puppy_ast_exec import puppy_exec
from puppys.pp.default_env.actionflow.parse import replace_function_arguments


class TestActionflow():
    """
    TestActionflow test a specific actionflow in debug mode.

    Init Args:
        puppy_instance (any): The instance of the puppy to test.
    """

    def __init__(
        self, 
        puppy_instance: any
    ):
        self.puppy_instance = puppy_instance

        # Set the color for printing
        self.GREEN = "\033[32m"
        self.GREY = "\033[90m"
        self.RED = "\033[31m"
        self.RESET = "\033[0m" 
    
    def test_run(
        self, 
        node_num: int, 
        num_of_action: int, 
        handle_exceptions: bool = True,
        max_length: int = 1000,
        use_command_line: bool = False,
        updates: dict = None
    ) -> list:
        """
        Test run the saved actionflow in debug mode.

        Args:

        node_num (int): 
            The number of the node to start execution from. The node numbers are as follows:
            - 0: The current code.
            - 1: From the current code to all the future codes.
            - -1: From the history codes to the current code.
            - 2: All code nodes, including history_codes, the current code, and future_codes.
            - -2: The last node of the history codes, the current code, and the first node of the future codes.

        num_of_action (int):
            The number of times to execute the actionflow. This allows repeated execution to test stability and success rate.

        handle_exceptions (bool):
            Whether to handle exceptions during execution. If True, the function will stop and return the exception when an error occurs. If False, the exception message will be captured and included in the results list, and execution will continue.

        use_command_line (bool):
            The mode of execution. It can be either inline or command-line.
            - False: The function applies monkey patching to update the attribute values of the loaded puppy_instance from the local file based on the provided kwargs. The function then runs the code node(s) num_of_action times.
            - True: The function provides an interactive command-line interface for the developer to select which attributes to modify. The current value is displayed, and the developer can enter new values. After updating values, the developer can choose to test run or continue updating values.

        updates (dict): 
            Dictionary used for inline mode to update the attribute values of the puppy_instance.

        Returns:
            A list of results from the executions, each element representing the output and error messages (if any) for one execution. If handle_exceptions is set to False, exceptions will be included in the list as well.
        """

        results = []

        # Update attributes
        if not use_command_line:
            self.inline_mode(updates)
            results = self.execute_code_multiple_times(
                num_of_action,
                node_num,
                results,
                handle_exceptions,
                max_length
            )
        else:
            results = self.command_line_mode(
                num_of_action,
                node_num,
                results,
                handle_exceptions,
                max_length
            )

        return results

    def inline_mode(
        self, 
        updates: dict
    ) -> None:
        """
        The inline mode for updating the attribute values of the puppy_instance.

        Args:
            updates (dict): The dictionary used to update the attribute values of the puppy_instance.
        """

        for key, value in updates.items():
            if self._has_nested_attr(self.puppy_instance, key):
                self._set_nested_attr(self.puppy_instance, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")

    def command_line_mode(
        self,
        num_of_action: int,
        node_num: int,
        results: list,
        handle_exceptions: bool,
        max_length: int
    ) -> list:
        """
        The command line mode for updating the attribute values of the puppy_instance.

        Args:
            num_of_action (int): The number of times to execute the actionflow.
            node_num (int): The number of the node to start execution from.
            results (list): The list of results from the executions.
            handle_exceptions (bool): Whether to handle exceptions during execution.
            max_length (int): The maximum length of the output to display.

        Returns:
            A list of results from the executions.
        """

        print(self.RED + "*** Command Line Mode for Test Run ***" + self.RESET)
        while True:
            print("Current puppy_instance attributes and values:")
            for attr, value in vars(self.puppy_instance).items():
                print(f"{self.GREEN}{attr}:{self.RESET} \n{self._advanced_print(value)}")

            execute = self._input_value("Execute codes (y) or change attributes (n)?: ", str).lower()
            if execute == "y":
                results = self.execute_code_multiple_times(num_of_action, node_num, results, handle_exceptions, max_length)
                print("Results: \n", results, "\n\n")
                is_exit = self._input_value("Exit test run? (y/n): ", str).lower()
                if is_exit == "y":
                    return results
            elif execute == "n":
                keep_modifying = True
                while keep_modifying:
                    attr_to_modify = input("Enter the attribute name to change: ").strip()
                    if self._has_nested_attr(self.puppy_instance, attr_to_modify):
                        current_value = self._get_nested_attr(self.puppy_instance, attr_to_modify)
                        print(f"Current value of {attr_to_modify}: {current_value}")

                        if isinstance(current_value, list):
                            self._modify_list(attr_to_modify, current_value)
                        else:
                            new_value = self._input_value("Enter the new value: ", type(current_value))
                            self._set_nested_attr(self.puppy_instance, attr_to_modify, new_value)
                            print(f"Updated value of {attr_to_modify}: {self._advanced_print(self._get_nested_attr(self.puppy_instance, attr_to_modify))}")

                        inner_modify = input("Do you want to modify any other attribute? (y/n): ").strip().lower()
                        if inner_modify == "n":
                            keep_modifying = False
                    else:
                        print(f"Attribute {attr_to_modify} does not exist.")
            else:
                print("Invalid input. Please enter `y` or `n`.")

    def execute_code_multiple_times(
        self,
        num_of_action: int,
        node_num: int,
        results: list,
        handle_exceptions: bool,
        max_length: int
    ) -> list:
        """
        Execute the code multiple times and append the results to the results list.
        The first element of the results list contains all the values, while the rest of the elements only contain the differences.

        Args:
            num_of_action (int): The number of times to execute the actionflow.
            node_num (int): The number of the node to start execution from.
            results (list): The list of results from the executions.
            handle_exceptions (bool): Whether to handle exceptions during execution.
            max_length (int): The maximum length of the output to display.

        Returns:
            A list of results from the executions.
        """

        # Execute the code
        for _ in range(num_of_action):
            try:
                result = self.execute_code(node_num)
                if isinstance(result, dict):
                    results.append(result)
                else:
                    raise ValueError(f"{result}")
            except Exception as e:
                if handle_exceptions:
                    raise e
                results.append({"Exception": e})

        # Find the differences between the results
        results = self._find_differences(results, max_length)

        # Save the updated puppy_instance
        self.save_updated_puppy_instance()
        self.save_instance_to_json(self.puppy_instance)

        return results

    def execute_code(
        self, 
        node_num: int
    ) -> dict:
        """
        Execute code from the specified node number.

        Args:
            node_num (int): The number of the node to start execution from.

        Returns:
            A dictionary containing the runtime values of the puppy_instance after executing the code.
        """

        codes_to_execute = self._set_code_node(node_num)

        for code in codes_to_execute:
            code = replace_function_arguments(code, self.puppy_instance.puppy_vars.runtime_dict)
            puppy_exec(code, self.puppy_instance.puppy_vars.global_dict, self.puppy_instance.puppy_vars.runtime_dict)

        # Create a deep copy of the runtime_dict
        picklable_dict, non_picklable_dict = self._separate_runtime_dict(self.puppy_instance.puppy_vars.runtime_dict)
        runtime_dict = copy.deepcopy(picklable_dict)
        runtime_dict.update(non_picklable_dict)

        return runtime_dict

    def save_updated_puppy_instance(
        self, 
        root_path: str = "user_case_history", 
        file_name: str = "puppy_instance_updated.pkl"
    ) -> None:
        """
        Save the updated puppy_instance to a pickle file. Exceptions will be raised if the file cannot be saved.

        Args:
            root_path (str): The root path to save the file. Defaults to "user_case_history".
            file_name (str): The name of the file. Defaults to "puppy_instance_updated.pkl".
        """

        if not os.path.exists(root_path):
            os.makedirs(root_path)

        file_path = os.path.join(root_path, file_name)

        try:
            with open(file_path, "wb") as output_file:
                dill.dump(self.puppy_instance, output_file)
            print(f"{self.GREEN}Updated Puppy instance saved to `{file_path}` successfully!{self.RESET}")
        except Exception:
            try:
                serializable_instance = self._filter_non_serializable(self.puppy_instance)
                with open(file_path, "wb") as output_file:
                    dill.dump(serializable_instance, output_file)
                print(f"{self.GREEN}Successfully save the instance to `{file_path}`!{self.RESET}")
            except Exception as e:
                print(f"{self.RED}Fail saving instance: {e}{self.RESET}")

    def save_instance_to_json(
        self, 
        instance: dict, 
        root_path: str = "user_case_history", 
        file_name: str = "puppy_instance_values.json"
    ) -> None:
        """
        Save all key-value pairs of an instance to a JSON file. Exceptions will be raised if the file cannot be saved.

        Args:
            instance (dict): The instance to save.
            root_path (str): The root path to save the file. Defaults to "user_case_history".
            file_name (str): The name of the file. Defaults to "puppy_instance_values
        """

        if not os.path.exists(root_path):
            os.makedirs(root_path)

        file_path = os.path.join(root_path, file_name)
        
        # Parse the instance into a dictionary
        instance_dict = {}
        for attr, value in vars(instance).items():
            value_string = self._parse_inner_json(value)
            instance_dict[attr] = value_string

        # Save the instance to a JSON file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(instance_dict, f, ensure_ascii=False, indent=4)
            print(f"{self.GREEN}Attribute values saved to `{file_path}` successfully!{self.RESET}")
        except Exception as e:
            print(f"{self.RED}Fail saving instance: {e}{self.RESET}")

    def _filter_non_serializable(
        self, 
        obj: any
    ) -> dict:
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

    def _parse_inner_json(
        self, 
        obj: any, 
        indent: int = 0
    ) -> dict:
        """
        Parse inner json function that parse the object into inner json objects.

        Args:
            obj: The object to parse.
            indent: The current indentation level (used for nested structures).
        
        Returns:
            The inner json object.
        """

        value_to_print = {}

        obj_type = type(obj).__name__

        if obj_type == "Actionflow":
            value_to_print = self._parse_inner_json(obj.__dict__, indent + 1)
        elif obj_type == "FuncEnv":
            value_to_print = self._parse_inner_json(obj.__dict__, indent + 1)
        elif obj_type == "PuppyVars":
            value_to_print = self._parse_inner_json(obj.__dict__["runtime_dict"], indent + 1)
        elif obj_type == "dict":
            for key, value in obj.items():
                value_to_print[key] = self._parse_inner_json(value, indent + 1)
        elif isinstance(obj, (list, tuple, set)):
            value_to_print = [self._parse_inner_json(item, indent + 1) for item in obj]
        else:
            obj_string = str(obj) if obj else "None"
            value_to_print = obj_string
        
        return value_to_print

    def _advanced_print(
        self, 
        obj: any, 
        indent: int = 0
    ) -> str:
        """
        Advanced print function that prints both standard Python objects and self-defined types.

        Args:
            obj: The object to print.
            indent: The current indentation level (used for nested structures).

        Returns:
            The formatted string to print.
        """
        
        spacing = " " * (indent * 4)
        
        value_to_print = ""
        
        obj_type = type(obj).__name__
        if obj_type == "Actionflow":
            value_to_print += self._advanced_print(obj.__dict__, indent + 1)
        elif obj_type == "FuncEnv":
            value_to_print += self._advanced_print(obj.__dict__, indent + 1)
        elif obj_type == "PuppyVars":
            value_to_print += self._advanced_print(obj.__dict__["runtime_dict"], indent + 1)
        elif obj_type == "dict":
            for key, value in obj.items():
                value_to_print += f"{self.GREEN}{spacing}{key}{self.RESET}: {self.GREY}{value}{self.RESET}\n"
        else:
            obj_string = str(obj) if obj else "None"
            value_to_print += f"{self.GREY}{spacing}{obj_string}{self.RESET}"
        
        return value_to_print

    def _set_code_node(
        self, 
        node_num: int
    ) -> list:
        """
        Set the code node to test run. Exceptions will be raised if the node number is invalid.

        Args:

        node_num (int): 
            The number of the node to start execution from. The node numbers are as follows:
            - 0: The current code.
            - 1: From the current code to all the future codes.
            - -1: From the history codes to the current code.
            - 2: All code nodes, including history_codes, the current code, and future_codes.
            - -2: The last node of the history codes, the current code, and the first node of the future codes.

        Returns:
            A list of codes to execute.
        """

        match node_num:
            case 0:
                codes_to_execute = [self.puppy_instance.actionflow.current_code]
            case 1:
                codes_to_execute = [self.puppy_instance.actionflow.current_code] + self.puppy_instance.actionflow.future_codes
            case -1:
                codes_to_execute = self.puppy_instance.actionflow.history_codes + [self.puppy_instance.actionflow.current_code]
            case 2:
                codes_to_execute = self.puppy_instance.actionflow.history_codes + [self.puppy_instance.actionflow.current_code] + self.puppy_instance.actionflow.future_codes
            case -2:
                codes_to_execute = [self.puppy_instance.actionflow.history_codes[-1]] + [self.puppy_instance.actionflow.current_code] + [self.puppy_instance.actionflow.future_codes[0]]
            case _:
                raise ValueError("Invalid node number. Please choose from 0, 1, -1, 2, or -2.")
        return codes_to_execute

    def _separate_runtime_dict(
        self, 
        runtime: dict
    ) -> tuple:
        """
        Separate a dictionary into two dictionaries: one with picklable values and the other with non-picklable summary in string format.

        Args:
            runtime (dict): The input dictionary.

        Returns:
            tuple: A tuple containing two dictionaries: (picklable_dict: picklable key-values, non_picklable_dict: non-picklable key-values in a summarized formatted string).
        """
        
        picklable_dict = {}
        non_picklable_dict = {}

        for key, value in runtime.items():
            try:
                pickle.dumps(value)
                picklable_dict[key] = value
            except (pickle.PicklingError, TypeError):
                # Use string representation for non-picklable values
                non_picklable_dict[key] = f"{type(value).__name__}: {repr(value)}"

        return picklable_dict, non_picklable_dict

    def _find_differences(
        self, 
        dict_list: list,
        max_length: int
    ) -> list:
        """
        Find the differences between dictionaries in a list.

        Args:
            dict_list (list): A list of dictionaries to compare.
            max_length (int): The maximum length of the output to display.

        Returns:
            A list of dictionaries representing the differences, the first element contains all the values while the rest elements only contain the difference.
        """

        if not dict_list:
            return [{}]

        first_dict = dict_list[0]
        differences = [first_dict]

        for d in dict_list[1:]:
            total_length = 0

            diff = {}
            for key, value in d.items():
                value_str = str(value)
                if total_length + len(value_str) > max_length:
                    diff["..."] = "Output truncated due to length limits"
                    break
                if (key in first_dict and first_dict[key] != value) or (key not in first_dict):
                    diff[key] = value
                total_length += len(value_str)

            differences.append(diff)

        return differences

    def _convert_value(
        self, 
        value: str, 
        target_type: type
    ) -> any:
        """
        Convert the input value to the target type if possible.

        Args:
            value (str): The input value.
            target_type (type): The target type to convert to.

        Returns:
            The converted value with the target type.
        """

        if target_type == int:
            return int(value)
        elif target_type == float:
            return float(value)
        elif target_type == bool:
            return value.lower() in ["true", "1", "yes"]
        elif target_type == list:
            return value.strip("[]").split(",")
        elif target_type == dict:
            import ast
            return ast.literal_eval(value)
        else:
            return value

    def _input_value(
        self, 
        prompt: str, 
        target_type: type
    ) -> any:
        """
        Keep asking for input until the input value is of the target type.

        Args:
            prompt (str): The prompt to display.
            target_type (type): The target type to convert to.

        Returns:
            The converted value with the target type.
        """

        while True:
            try:
                value = input(prompt).strip()
                return self._convert_value(value, target_type)
            except ValueError:
                print(f"Invalid input. Expected type: {target_type.__name__}.")

    def _modify_list(
        self, 
        attr_to_modify: str, 
        current_list: list
    ) -> None:
        """
        Modify the list attribute of the puppy_instance by each element.

        Args:
            attr_to_modify (str): The attribute to modify.
            current_list (list): The current list to modify.
        """

        if current_list:
            print(f"Current list elements of {attr_to_modify}:")
            for index, element in enumerate(current_list):
                print(f"{index}: {element}")

            index_to_modify = self._input_value("Enter the index to modify: ", int)
            if 0 <= index_to_modify < len(current_list):
                element_type = type(current_list[index_to_modify])
                new_value = self._input_value(f"Enter the new value for index {index_to_modify}: ", element_type)
                current_list[index_to_modify] = new_value
                print(f"Updated list: {current_list}")
            else:
                print("Invalid index.")
        else:
            num_of_elements = self._input_value("Current list is empty, enter the number of elements to add: ", int)
            for i in range(num_of_elements):
                new_element = self._input_value(f"New element {i} (Only string type is supported): ", str)
                current_list.append(new_element)
            print(f"Updated list: {current_list}")

    def _has_nested_attr(
        self, 
        obj: any, 
        attr_path: str
    ) -> bool:
        """
        Check if the object has a nested attribute.

        Args:
            obj (any): The object to check.
            attr_path (str): The path to the attribute, separated by dots.

        Returns:
            bool: True if the nested attribute exists, False otherwise.
        """

        attrs = attr_path.split(".")
        for attr in attrs:
            if not hasattr(obj, attr):
                return False
            obj = getattr(obj, attr)
        return True

    def _get_nested_attr(
        self, 
        obj: any, 
        attr_path: str
    ) -> any:
        """
        Get the value of a nested attribute.

        Args:
            obj (any): The object from which to get the attribute.
            attr_path (str): The path to the attribute, separated by dots.

        Returns:
            The value of the nested attribute.
        """

        attrs = attr_path.split(".")
        for attr in attrs:
            obj = getattr(obj, attr)
        return obj

    def _set_nested_attr(
        self, 
        obj: any, 
        attr_path: str, 
        value: any
    ) -> None:
        """
        Set the value of a nested attribute.

        Args:
            obj (any): The object on which to set the attribute.
            attr_path (str): The path to the attribute, separated by dots.
            value (any): The value to set.
        """

        attrs = attr_path.split(".")
        for attr in attrs[:-1]:
            obj = getattr(obj, attr)
        setattr(obj, attrs[-1], value)

 