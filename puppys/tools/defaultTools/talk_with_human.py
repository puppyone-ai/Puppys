from contextlib import redirect_stdout
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from puppys.pp.actions.explore import explore
import sys


def talk_with_human(puppy, message):

    """
    Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to send a message to the user or let the user know your result.
    If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help.

    for example:
    ## Ask the user about the phone number of his boss
    question="What's the phone number of your boss?"
    talk_with_human(message=question) # the message is essential
    """

    BLUE = "\033[34m"
    RESET = "\033[0m"

    with redirect_stdout(sys.__stdout__):
        user_input = input(f"{BLUE}{puppy.name}: {message}\nYour response: {RESET}")

    chat_history = "\n" + "# your message:" + str(message) + "\n" + "# User's response: " + user_input + "\n"

    puppy.actionflow.current_action_code += chat_history


if __name__ == "__main__":

    # define an agent
    puppy=Puppy(name="Puppy")

    # define the tool in the agent
    puppy.tools_talk_with_human = FuncEnv(name="talk_with_human",
                            description=talk_with_human.__doc__,
                            value=talk_with_human,
                            fixed_params={"puppy": puppy}, free_params=["message"])

    # run the tool
    puppy.tools_talk_with_human(message="hello world")

    print(explore(puppy, target=FuncEnv))

    for key, e in explore(puppy, target=FuncEnv).items():
        print(e)