from puppy.utils.std import recover_stdout
from puppy.thread.base import ThreadBase
from puppy.environment.func import FuncBase


class SendSendMessageToHuman(FuncBase):
    def __init__(self, thread_instance: ThreadBase = ThreadBase()):
        super().__init__()

        self.thread_instance = thread_instance

        self.name = "send_message_to_human"
        self.tag = "func"
        self.intro = """
        Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
        If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
        use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ question/ etc.
        You must add the "self" before each function.
        
        for example:
        ## Ask the user about the phone number of his boss
        answer = self.send_message_to_human("\U0001F600: What's the phone number of your boss?")
        """
        self.question = ""

    def __call__(self, question=""):
        self.question = question
        return self.run(self.question)

    def set_question(self, question):
        self.question = question

    def run(self, question=""):

        self.question = question

        with recover_stdout():
            user_input = input(question + "\n" + "Your response:")
            print("\U0001F600: Sure, get it.")

        chat_history = "\n" + "# Above code have some issue about:" + self.question + "\n" + "# Instruction for the issue as: " + user_input + "\n"

        self.thread_instance.attention.code += chat_history
