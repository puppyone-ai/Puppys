from __future__ import annotations
from puppy.environment.base import EnvBase
from puppy.pp.base import PuppyBase


class FuncBase(EnvBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self):
        return self.__dict__['name'] if self.__dict__['name'] else self.value.__name__

    @name.setter
    def name(self, value):
        self.__dict__['name'] = value

    @property
    def description(self):
        return self.__dict__["description"] if self.__dict__["description"] else self.value.__doc__

    @description.setter
    def description(self, value: str):
        self.__dict__['description'] = value

    def run(self, *args, **kwargs):
        return self.value(*args, **kwargs)


# (decorator) Rapidly create a new func instance under the env instance
def new_func(puppy: PuppyBase = None):
    def decorator(func):
        func_env = FuncBase(value=func)
        if puppy:
            setattr(puppy, func.__name__, func_env)
        return func  # 返回原始函数或包装后的函数

    if puppy:
        return decorator(puppy)

    return decorator


if __name__ == "__main__":

    """
    Three method that can create a new env in an env:
    """

    # method_1: use @new_func decorator
    @new_func()
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

    send_message_to_human.run()

    # method_2 use FuncBase
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

    func_send_message = FuncBase(value=send_message_to_human, name="send_message_to_human", description=description)
    send_message_to_human.run()
