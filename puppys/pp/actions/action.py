import os
import re
import traceback
from puppys.llm.open_ai import open_ai_chat


class Action:
    """
    The base class for all actions using the Large Language Models.

    Init Args:
        puppy_instance (any): The puppy instance.
        action_name (str): The name of the action.
        model (str): The model to use for the Large Language Model.
        show_prompt (bool): Whether to show the prompt.
        show_response (bool): Whether to show the response.
        retries (int): The number of retries for the action.
    """
    def __init__(
        self, 
        puppy_instance: any, 
        action_name: str, 
        model: str, 
        show_prompt: bool, 
        show_response: bool, 
        retries: int
    ):
        self._puppy_instance = puppy_instance
        self.action_name = action_name
        self.model = model
        self.show_prompt = show_prompt
        self.show_response = show_response
        self.retries = retries

        # Set the printing color
        self.GREEN= "\033[32m"
        self.RED = "\033[31m"
        self.GREY = "\033[90m"
        self.RESET = "\033[0m"

    def replace_action_code(
        self, 
        new_code: str
    ) -> None:
        """
        Replace the action code in the all code.

        Args:
            new_code (str): The new code to replace. It can be a single line or multiple lines.
        """
        print("replace_action_code!!!")

        new_lines = new_code.split("\n")

        # For the cases that replace the code multiple times due to the retry mechanism
        if self.action_name in self._puppy_instance.actionflow.temp_current_code and \
            self._puppy_instance.actionflow.temp_current_code[self.action_name][1] in self._puppy_instance.actionflow.current_code:
            leading_whitespaces = self._puppy_instance.actionflow.temp_current_code[self.action_name][0]
            code_to_replace = self._puppy_instance.actionflow.temp_current_code[self.action_name][1]
            new_code_to_add = "\n".join([leading_whitespaces + line for line in new_lines]) + "\n"
            print("if Current: ", code_to_replace)
            print("if Replaced: ", new_code_to_add)
            self._puppy_instance.actionflow.current_code = self._puppy_instance.actionflow.current_code.replace(code_to_replace, new_code_to_add, 1)
            self._puppy_instance.actionflow.temp_current_code[self.action_name] = (leading_whitespaces, new_code_to_add)
            if self.retries == 0:
                self._puppy_instance.actionflow.temp_current_code = {}

        # For the cases that replace the code the first time
        else:
            # Replace the line containing action_name
            current_code_lines = self._puppy_instance.actionflow.current_code.splitlines(keepends=True)
            print("current_code_lines: ", current_code_lines)
            self.action_name = self.action_name.strip().replace("\n", "\\n")
            for current_line in current_code_lines:
                if self.action_name in current_line:
                    leading_whitespaces = re.match(r"\s*", current_line).group()
                    new_code_to_add = "\n".join([leading_whitespaces + line for line in new_lines]) + "\n"
                    print("Current: ", current_line)
                    print("Replaced: ", new_code_to_add)
                    self._puppy_instance.actionflow.current_code = self._puppy_instance.actionflow.current_code.replace(current_line, new_code_to_add, 1)
                    self._puppy_instance.actionflow.temp_current_code[self.action_name] = (leading_whitespaces, new_code_to_add)
                    # Only replace one action at a time
                    break

    def get_concise_traceback(
        self, 
        exc: Exception, 
        num_of_lines: int = 10
    ) -> str:
        """
        Get the concise traceback if the error occurs.

        Args:
            exc (Exception): The exception that occurs.
            num_of_lines (int): The number of lines to show in the traceback. Count from the end of the traceback. The default is 10.

        Returns:
            str: The concise traceback.
        """

        tb = traceback.TracebackException.from_exception(exc)
        concise_traceback = "".join(tb.format_exception_only())
        detailed_traceback = "".join(tb.format())
        traceback_lines = detailed_traceback.split("\n")
        relevant_lines = traceback_lines[-num_of_lines:]

        if relevant_lines:
            concise_traceback += "\n".join(relevant_lines)

        return concise_traceback

    def highlighting(
        self, 
        action_type: str, 
        prompt: list, 
        prompt_action: str = ""
    ) -> None:
        """
        Highlight the action name and prompt.

        Args:
            action_type (str): The type of the action. Showing at the start of the action.
            prompt (list): The raw prompts to show.
            prompt_action (str): The action to show in the prompt. The default is "".
        """
        
        # Print the action name
        print(self.GREEN + f"[{action_type}]" + self.action_name + self.RESET)

        # If show_prompt is true, show the prompt
        if self.show_prompt is True:
            print(self.GREY + f"\t*******{prompt_action} prompt********" + self.RESET)
            for chunk in prompt:
                print(self.GREY + chunk["content"] + self.RESET)

    def clean_llm_code(
        self, 
        new_code: str, 
        add_code: bool
    ) -> str:
        """
        Clean the LLM code and add it to the current code if needed.

        Args:
            new_code (str): The new code to clean.
            add_code (bool): Whether to add the new code to the current code in the actionflow.

        Returns:
            str: The cleaned code.
        """

        # Clean the code
        new_code = new_code.replace("```python\n", "").replace("\n```", "")

        # Add the ran code into the current code
        if add_code:
            self._puppy_instance.actionflow.current_action_code += new_code + "\n"

        return new_code

    def run_without_errors(
        self, 
        new_code: str
    ) -> str:
        """
        Run the Agent's code without any errors.

        Args:
            new_code (str): The new code to run.

        Returns:
            str: The new code.
        """

        self._puppy_instance.actionflow.puppy_exec(new_code)
        # Reset the error
        self._puppy_instance.actionflow.errors = ""
        return new_code

    def run_with_errors(
        self, 
        error_message: Exception
    ) -> str:
        """
        Run the Agent's code with errors caught by Exceptions.

        Args:
            error_message (Exception): The error message.

        Returns:
            str: The error details.
        """

        # Store the error message
        error_details = self.get_concise_traceback(error_message)
        print(self.RED + "Error:\n", error_message, error_details, self.RESET)
        self._puppy_instance.actionflow.errors += error_details

        return error_details

    def get_puppy_instance(
        self
    ):
        """
        Return the updated puppy_instance.
        """

        return self._puppy_instance

