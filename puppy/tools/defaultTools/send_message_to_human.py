from puppy.environment.func import FuncBase
from puppy.utils.std import recover_stdout


class SendSendMessageToHuman(FuncBase):
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
        answer = send_message_to_human("\U0001F600: What's the phone number of your boss?")
        """
        self.func = self.run

        self.__question = ""

        self.__thread_instance = thread_instance

    @property
    def question(self):
        return self.__question

    @question.setter
    def question(self, value):
        self.__question = value

    def __call__(self, question=None):
        if question:
            self.question = question
        return self.run()

    def set_question(self, question):
        self.question = question

    def run(self, question=None):

        if question is not None:
            self.question = question

        with recover_stdout():
            user_input = input(self.question + "\n" + "Your response:")
            print("\U0001F600: Sure, get it.")

        chat_history = "\n" + "your message:" + self.question + "\n" + "# User's response: " + user_input + "\n"

        self.__thread_instance.attention.code += chat_history
