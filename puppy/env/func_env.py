from __future__ import annotations
from puppy.env.env import Env


class FuncEnv(Env):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.name:
            self.name = self.value.__name__

        if not self.description:
            self.description = self.value.__doc__

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)


if __name__ == "__main__":

    # Method that can wrap a func into an env:

    description = """
        Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
            If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
            use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ question/ etc.
            You must add the "self" before each function.

        for example:
        ## Ask the user about the phone number of his boss
        answer = self.ok("\U0001F600: What's the phone number of your boss?")
        """

    def send_message_to_human():
        print("全体起立向我看齐，我宣布个事儿，我是个傻逼！")

    send_message_to_human = FuncEnv(value=send_message_to_human, description=description)
    send_message_to_human()
