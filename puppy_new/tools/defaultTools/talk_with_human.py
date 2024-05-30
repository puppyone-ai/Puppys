from puppy_new.environment.func import FuncBase
from contextlib import redirect_stdout
from puppy_new.pp.base import PuppyBase
import sys


class TalkWithHuman(FuncBase):
    def __init__(self, puppy_instance, *args, **kwargs):

        """
        {
            "FuncBase": {
                "name": "",
                "intro": "",
                "tag": "func",
                "__env_instance": None,
                "__func": None,
                "__visibility": True
            }
        }
        """
        self.puppy_instance= puppy_instance
        super().__init__(*args, **kwargs)

        self.name = "talk_with_human"
        self.intro = """
Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to send a message to the user or let the user know your result.
If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help.


for example:
## Ask the user about the phone number of his boss
talk_with_human(" What's the phone number of your boss?")
        """
        self.func = self.send_message_to_human

        self.__puppy_instance = puppy_instance

    def send_message_to_human(self, question):

        with redirect_stdout(sys.__stdout__):
            user_input = input(self.puppy_instance.name+": "+str(question) + "\n" + "Your response:")

        chat_history = "\n" + "# your message:" + str(question) + "\n" + "# User's response: " + user_input + "\n"

        self.__puppy_instance.actionflow.current_code += chat_history


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    from puppy_new.pp.base import PuppyBase

    thread = PuppyBase(name=" Mr.Walter")

    sender = TalkWithHuman(puppy_instance=thread)

    sender.run(text)
