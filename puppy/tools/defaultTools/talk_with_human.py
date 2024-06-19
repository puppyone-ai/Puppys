from contextlib import redirect_stdout
from puppy.pp.main import Puppy
import sys


def talk_with_human(puppy, question):

    """
    Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to send a message to the user or let the user know your result.
    If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help.

    for example:
    ## Ask the user about the phone number of his boss
    talk_with_human(" What's the phone number of your boss?")
    """

    with redirect_stdout(sys.__stdout__):
        user_input = input(f"{puppy.name}" + ": " + str(question) + "\n" + "Your response:")

    chat_history = "\n" + "# your message:" + str(question) + "\n" + "# User's response: " + user_input + "\n"

    puppy.current_code += chat_history


if __name__ == "__main__":

    text = "how should I install the package of openAI"

    talk_with_human(Puppy(value=None), text)
