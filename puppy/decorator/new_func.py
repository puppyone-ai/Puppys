from puppy.env import FuncEnv


# Rapidly create a new func instance under the env instance
def new_func(func):
    func_env = FuncEnv(value=func)
    return func_env


if __name__ == "__main__":
    @new_func
    def send_message_to_human(*, what_to_say) -> None:

        """
        Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
            If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
            use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ question/ etc.
            You must add the "self" before each function.

        for example:
        ## Ask the user about the phone number of his boss
        answer = self.ok("\U0001F600: What's the phone number of your boss?")
        """

        print(what_to_say)

    send_message_to_human(what_to_say="全体起立向我看齐，我宣布个事儿，我是个傻逼！")
