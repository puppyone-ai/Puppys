from puppy.toolBox.default.send_message_to_human import SendSendMessageToHuman
from puppy.toolBox.default.google_search_native import GoogleSearchNative
from puppy.toolBox.default.gpt import GPT
from puppy.thread.base import ThreadBase
from puppy.environment.base import EnvBase


# TODO: Search path to collect all the default funcs

class ToolBox(EnvBase):
    def __init__(self, thread_instance=ThreadBase(), **kwargs):
        super().__init__(name='ToolBox',
                         intro="a Tool Box that full of default functions",
                         visibility=False, **kwargs)

        self.thread_instance = thread_instance

        for blueprint in [GPT, GoogleSearchNative, SendSendMessageToHuman]:
            tool = blueprint(env_instance=self)
            self.add(tool)

    def add(self, tool):

        setattr(self, tool.name, tool)

        if not isinstance(self, ThreadBase):
            tool.thread_instance = self.thread_instance
            setattr(tool.thread_instance, tool.name, tool)


if __name__ == "__main__":
    tool_box = ToolBox(thread_instance=ThreadBase())

    print(tool_box.expose)



