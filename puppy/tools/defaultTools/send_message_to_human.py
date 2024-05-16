from puppy.environment.func import FuncBase
from contextlib import redirect_stdout
from puppy.thread.base import ThreadBase
import sys



class SendMessageToHuman(FuncBase):
    def __init__(self, thread_instance=None, *args, **kwargs):

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

        super().__init__(*args, **kwargs)

        self.name = "send_message_to_human"
        self.intro = """
        Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
        If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
        use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ question/ etc.
        You must add the "self" before each function.
        
        for example:
        ## Ask the user about the phone number of his boss
        send_message_to_human("\U0001F600: What's the phone number of your boss?")
        """
        self.func = self.send_message_to_human

        self.__thread_instance = thread_instance

    def send_message_to_human(self, question):

        with redirect_stdout(sys.__stdout__):
            user_input = input(str(question) + "\n" + "Your response:")

        chat_history = "\n" + "your message:" + str(question) + "\n" + "# User's response: " + user_input + "\n"

        # TODO: creat a thread to modify on going code
        self.thread_instance.actionflow.on_going.code += chat_history



if __name__ == "__main__":
    text = "how should I install the package of openAI"

    from puppy.thread.base import ThreadBase

    thread = ThreadBase()

    sender = SendMessageToHuman(thread_instance=thread)

    sender.run(text)
