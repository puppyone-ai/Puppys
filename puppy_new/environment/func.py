from __future__ import annotations
from puppy.environment.base import EnvBase


class FuncBase(EnvBase):

    def __init__(self,
                 env_instance: EnvBase = None,
                 func=None,
                 *args, **kwargs):

        """
        {
            "EnvBase": {
                "name": "",
                "intro": "",
                "tag": "env",
                "__visibility": False
            }
        }
        """

        super().__init__(*args, **kwargs)

        self.tag = "func"

        self.env_instance = env_instance

        self.func = func

        self.visible = True

        self.__name = None
        self.__intro = None

    @property
    def name(self):
        # return getattr(self, '__name', self.func.__name__)

        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def intro(self):
        # return getattr(self, '__intro', self.func.__doc__)

        return self.__intro

    @intro.setter
    def intro(self, value):
        self.__intro = value

    @property
    def func(self):
        return self.__func

    @func.setter
    def func(self, value):
        self.__func = value

    @property
    def env_instance(self):
        return self.__env_instance

    @env_instance.setter
    def env_instance(self, value):
        self.__env_instance = value

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)


# (decorator) Rapidly create a new func instance under the env instance
def new_func(env_instance=None):

    def wrapper(func):
        return FuncBase(env_instance=env_instance, func=func, name=func.__name__, intro=func.__doc__)

    return wrapper


if __name__ == "__main__":

    EnvVars = EnvBase(name="building", visibility=True)

    @new_func(env_instance=EnvVars)
    def send_message_to_human():

        """
        Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
            If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
            use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ question/ etc.
            You must add the "self" before each function.

        for example:
        ## Ask the user about the phone number of his boss
        answer = self.ok("\U0001F600: What's the phone number of your boss?")
        """

        print("全体起立向我看齐，我宣布个事儿，我是个傻逼！")


    EnvVars.send_message = send_message_to_human

    EnvVars.send_message.run()
