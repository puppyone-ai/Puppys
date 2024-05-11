from puppy.tools.defaultTools.send_message_to_human import SendMessageToHuman
from puppy.tools.defaultTools.search_native import SearchNative
from puppy.tools.defaultTools.chat_llm import ChatLLM
from puppy.thread.base import ThreadBase
from puppy.environment.base import EnvBase


# TODO: Search path to collect all the default funcs

# the default tool box that contains all the default functions
# use to manage all tools under a thread
class UsableTools(EnvBase):
    def __init__(self, thread_instance: ThreadBase = ThreadBase(), **kwargs):

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

        # the all tools' detail
        self.usable_tools_dict = {}

        # the default tools
        self.default_tools = [ChatLLM, SearchNative, SendMessageToHuman]

        # TODO: Search path to collect all the default funcs

    @property
    def thread_instance(self):
        return self.__thread_instance

    @property
    def usable_tools(self):
        import json
        return json.dumps(self.usable_tools_dict, indent=4)

    # once a tool_instance has been loaded into the list, we make a global func
    def load_tool(self, tool):

        self.usable_tools_dict.update({tool.name: tool.intro})

        self.__thread_instance.exec_environment.update({tool.name: tool.func})

    def remove_tool(self, name):

        self.usable_tools_dict.pop(name)

        self.thread_instance.exec_environment.pop(name)


if __name__ == "__main__":
    tool_box = (UsableTools(thread_instance=ThreadBase()))
    print(tool_box.expose)
