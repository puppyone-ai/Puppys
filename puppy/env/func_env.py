from __future__ import annotations
from puppy.env.env import Env
import inspect


class FuncEnv(Env):

    def __init__(self, name: str, description: str, value, fixed_params: dict = None, free_params: list = None, *args,
                 **kwargs):
        super().__init__(name=name, description=description, value=value, *args, **kwargs)

        self.fixed_params = fixed_params if fixed_params is not None else {}

        self.free_params = free_params
        if self.free_params is None:
            raise ValueError("free_params cannot be None")

        # use the inspect to check the value function, making sure that all free_params are valid
        self.validate_params()

    def validate_params(self):
        # get all param list
        all_params = inspect.signature(self.value).parameters

        # check if the free param list contains invalid params
        for param in self.free_params:
            if param not in all_params:
                raise ValueError(f"Parameter '{param}' is not a valid parameter of the function {self.value.__name__}")

#TODO  fix the bug of this
    def __call__(self, *args, **kwargs):

        if args:  # check if args is empty
            raise ValueError("No positional arguments are allowed for Func_Env")


        # 确保所有传入的自由参数都在 free_params 列表中
        free_params_dict = {k: v for k, v in kwargs.items() if k in self.free_params}
        # 合并固定参数和自由参数
        combined_params = {**self.fixed_params, **free_params_dict}
        return self.value(**combined_params)


if __name__ == "__main__":

    # Method that can define a func, by its description, name, and value
    name = "ok"

    description = """
        Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
        If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
        use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ message/ etc.
        You must add the "self" before each function.

        for example:
        ## introduce yourself
        answer = ok(intro="my name is Lin")
        """


    def send_message_to_human(intro, max_num, *args, **kwargs):

        num = 0
        while num < max_num:
            print(f"hello, everyone, I am {intro}")
            num += 1

    send_message_to_human = FuncEnv(name="ok", description=description, value=send_message_to_human,
                                    fixed_params={"max_num": 3}, free_params=["intro"])

    send_message_to_human(intro="puppy", ok=3)

    exec("send_message_to_human(intro= 'puppy', ok=3)")
