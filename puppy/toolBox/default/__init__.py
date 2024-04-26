from puppy.toolBox.default.send_message_to_human import SendSendMessageToHuman
from puppy.toolBox.default.google_search_native import GoogleSearchNative
from puppy.toolBox.default.gpt import GPT
from puppy.thread.base import ThreadBase
from puppy.environment.base import EnvBase


# TODO: Search path to collect all the default funcs

class ToolBox(EnvBase):
    def __init__(self, thread_instance=ThreadBase(), **kwargs):

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

        super().__init__(name='tool_box',
                         intro="a Tool Box that full of default functions",
                         visibile=False, **kwargs)

        self.__thread_instance = thread_instance

        # deliver the tool box as a variable under the exec_environment of the thread
        self.thread_instance.exec_environment['tool_box'] = self

        # for blueprint in [GPT, GoogleSearchNative, SendSendMessageToHuman]:
        #     tool = blueprint(env_instance=self)
        #     self.add(tool)

        # TODO: Search path to collect all the default funcs
        self.add(GPT(env_instance=self))
        self.add(GoogleSearchNative(env_instance=self))
        self.add(SendSendMessageToHuman(env_instance=self, thread_instance=self.thread_instance))


    @property
    def thread_instance(self):
        return self.__thread_instance

    def add(self, tool):

        setattr(self, tool.name, tool)
        setattr(self.thread_instance, tool.name, tool)


if __name__ == "__main__":
    tool_box = ToolBox(thread_instance=ThreadBase())

    print(tool_box.expose)



