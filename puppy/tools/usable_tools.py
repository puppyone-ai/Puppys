from puppy.tools.defaultTools.send_message_to_human import SendSendMessageToHuman
from puppy.tools.defaultTools.google_search_native import GoogleSearchNative
from puppy.tools.defaultTools.gpt import GPT
from puppy.thread.base import ThreadBase
from puppy.environment.base import EnvBase


# TODO: Search path to collect all the default funcs

# the default tool box that contains all the default functions
# use to manage all tools under a thread
class UsableTools(EnvBase):
    def __init__(self, thread_instance: ThreadBase = ThreadBase(), **kwargs):

        """
        {"EnvBase": {
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

        # the all tools' detail
        self.tools_dict={}

        # deliver the tool box as a variable under the exec_environment of the thread
        self.thread_instance.exec_environment['tool_box'] = self

        # for blueprint in [GPT, GoogleSearchNative, SendSendMessageToHuman]:
        #     tool = blueprint(env_instance=self)
        #     self.add(tool)

        # TODO: Search path to collect all the default funcs
        '''
        self.add(GPT(env_instance=self))
        self.add(GoogleSearchNative(env_instance=self))
        self.add(SendSendMessageToHuman(env_instance=self, thread_instance=self.thread_instance))
        '''
    @property
    def thread_instance(self):
        return self.__thread_instance

    # to add an extra tool to the tool box
    def add(self, tool):

        setattr(self, tool.name, tool)
        setattr(self.thread_instance, tool.name, tool)

    # once a tool_instance has been loaded into the list, we make a global func
    def load_tools(self, tool_instance):
        self.tools_dict.update({tool_instance.name: tool_instance.detail})

        def make_function(inst):
            def func(*args, **kwargs):
                return inst.run(*args, **kwargs)

            return func
        self.__thread_instance.exec_environment.update({tool_instance.name: make_function(tool_instance)})

    def remove_tools(self, name):
        for tool in self.tools_dict:
            if tool.name == name:
                self.tools_dict.pop(tool.name)
                self.thread_instance.exec_environment.pop(tool.name)


if __name__ == "__main__":
    tool_box = (UsableTools(thread_instance=ThreadBase()))
    print(tool_box.expose)
