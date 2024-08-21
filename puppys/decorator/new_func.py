# If you are a VS Code users:
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from puppys.env import FuncEnv
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from puppys.pp.actions.explore import explore


# Rapidly create a new func instance with decorator
def new_func(
    fixed_params: dict = None, 
    free_params: list = None, 
    name: str = None, 
    description: str = None
) -> any:
    """
    Create a new func instance with decorator.

    Args:
        fixed_params: dict, the fixed parameters of the function
        free_params: list, the free parameters of the function
        name: str, the name of the function
        description: str, the description of the function

    Returns:
        decorator: function, the decorator function
    """

    def decorator(func):
        # Check the parameters
        local_fixed_params = fixed_params if fixed_params else {}
        local_free_params = free_params if free_params else []

        # Use the name, or use the function's initial name and description
        func_name = name if name else func.__name__
        func_description = description if description else func.__doc__

        # Create func_env with the parameters
        func_env = FuncEnv(
            name=func_name, 
            description=func_description, 
            value=func,
            fixed_params=local_fixed_params, 
            free_params=local_free_params
        )

        return func_env

    return decorator


if __name__ == "__main__":
    @new_func(free_params=["what_to_say"])
    def say(what_to_say) -> None:
        """
        Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
            If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
            use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ message/ etc.
            You must add the "self" before each function.

        For example:
        ## Ask the user about the phone number of his boss
        answer = self.OK(what_to_say="\U0001F600: What's the phone number of your boss?")
        """

        print(what_to_say)

    def puppy_actionflow(self):
        pass

    puppy = Puppy(name="Puppy", value=puppy_actionflow)

    puppy.tool = say

    print(explore(puppy, target=FuncEnv, output_content_mode="attribute", attributes=["name","description","value"]))

    puppy.tool(what_to_say="Hi all, My name is Puppy!")
