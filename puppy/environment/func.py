from puppy.environment.base import EnvBase


# the decorator that wraps a function

def new_func(func):
    class FuncBase(EnvBase):
        def __init__(self, env_instance=None):

            super().__init__()

            self.func = func

            self.EnvInstance = env_instance

            self.name = func.__name__

            self.tag = ["func"]

            self.intro = func.__doc__

            self.detail = {"name": self.name, "intro": self.intro}

            self.visibility = True

        def __call__(self, *args, **kwargs):

            return self.run(*args, **kwargs)

        def run(self, *args, **kwargs):

            return self.func(self.EnvInstance, *args, **kwargs)

    def wrapper(env_instance):

        return FuncBase(func, env_instance)

    return wrapper


@new_func
def send_message_to_human():
    """
    Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
        If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
        use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ question/ etc.
        You must add the "self" before each function.

    for example:
    ## Ask the user about the phone number of his boss
    answer = send_message_to_human("\U0001F600: What's the phone number of your boss?")
    """
    print("全体起立向我看齐，看我看我，我是个傻逼！")
    # print(env.expose())


EnvVars = EnvBase(name="building", visibility=True)

EnvVars.ok = send_message_to_human(EnvVars)  # 实例化FuncBase

print(EnvVars.detail)  # 调用FuncBase实例，进而调用原始函数





"""
class SendSendMessageToHuman:
    def __init__(self, thread_instance):
        self.thread_instance = thread_instance

        self.name = "send_message_to_human"
        self.tag = "func"
        self.description = '''Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
        If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
        use emoji to make the conversation more interesting. For example, happy/ sad/ sorry/ angry/ question/ etc.
        You must add the "self" before each function.
        '''
        self.example = f'''
        ## Ask the user about the phone number of his boss
        answer = self.send_message_to_human("\U0001F600: What's the phone number of your boss?")
        '''
        # self.function_before_action = []
        # self.function_after_action = []
        # self.allowed_thread = ["main_thread"]
        self.question = ""

    def __call__(self, question=""):
        self.question = question
        return self.run(self.question)

    def set_question(self, question):
        self.question = question

    def run(self, question=""):
        self.question = question

        user_input = input(question + "\n" + "Your response:")
        print("\U0001F600: Sure, get it.")

        chat_history = "\n" + "your message:" + self.question + "\n" + "# User's response: " + user_input + "\n"

        self.thread_instance.doing_action.code += chat_history
"""
