from puppy.environment.func import FuncBase
from contextlib import redirect_stdout
from puppy.thread.base import ThreadBase
from puppy.utils.websocket_backend import request_feedback_from_frontend
import sys
import asyncio
from concurrent.futures import Future
import multiprocessing

# notify_message_queue = multiprocessing.Queue()
# feedback_message_queue = multiprocessing.Queue()


class SendMessageToHuman(FuncBase):
    def __init__(self, thread_instance, *args, **kwargs):

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

for example:
## Ask the user about the phone number of his boss
send_message_to_human("\U0001F600: What's the phone number of your boss?")
        """
        self.func = self.send_message_to_human

        self.__thread_instance = thread_instance

    def reflex(self):
        self.func = self.send_message_to_frontend

    def send_message_to_human(self, question: str):

        question = str(question)

        # with redirect_stdout(sys.__stdout__):
        user_input = input(question + "\n" + "Your response:")

        chat_history = "\n" + "your message:" + question + "\n" + "# User's response: " + user_input + "\n"

        # TODO: create a thread to modify on going code
        self.__thread_instance.actionflow.on_going.code += chat_history

    # def send_message_to_human_multiprocessing(self, question: str):
    #
    #     question = str(question)
    #
    #     notify_message_queue.put(question)
    #
    #     while True:
    #         if not feedback_message_queue.empty():
    #             user_input = feedback_message_queue.get()
    #             chat_history = "\n" + "your message:" + question + "\n" + "# User's response: " + user_input + "\n"
    #
    #             # TODO: create a thread to modify on going code
    #             self.__thread_instance.actionflow.on_going.code += chat_history
    #
    #             break

    def send_message_to_frontend(self, question: str):

        """
        Send the question to the frontend asynchronously, and wait for the response.
        Until receive a response, keep pending
        After receive a response, add it to the on_going code
        """

        question = str(question)

        def add2history(ft: Future):

            chat_history = "\n" + "your message:" + question + "\n" + "# User's response: " + ft.result() + "\n"

            # TODO: create a thread to modify on going code
            self.__thread_instance.actionflow.on_going.code += chat_history

        # asyncio.set_event_loop(self.__thread_instance.loop)

        # loop = asyncio.get_event_loop()

        future = asyncio.run_coroutine_threadsafe(request_feedback_from_frontend(question), self.__thread_instance.loop)

        future.add_done_callback(add2history)


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    from puppy.thread.base import ThreadBase

    thread = ThreadBase()

    sender = SendMessageToHuman(thread_instance=thread)

    sender.run(text)
