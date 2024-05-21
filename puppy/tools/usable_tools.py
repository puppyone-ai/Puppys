from puppy.tools.defaultTools.send_message_to_human import SendMessageToHuman
from puppy.tools.defaultTools.search_native import SearchNative
from puppy.tools.defaultTools.large_language_model import LangeLanguageModel
from puppy.thread.base import ThreadBase
from puppy.environment.base import EnvBase
from puppy.environment.func import FuncBase


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
        self.add_env(SendMessageToHuman(self.__thread_instance), LangeLanguageModel())

        # TODO: Search path to collect all the default funcs

    @property
    def thread_instance(self):
        return self.__thread_instance

    @property
    def tool_dict(self) -> dict:

        """
        This property is used to return the dict of all tools dynamically
        """

        clone_dict = self.detail_dict.copy()

        return {key: value for key, value in clone_dict.items() if isinstance(value, FuncBase)}

    def inventory_tools(self) -> None:

        """
        This method is used to inventory all the tools within the tool box
        """

        for tool in self.tool_dict.values():
            self.load_tool(tool)

    def load_tool(self, tool: FuncBase) -> None:

        """
        This method is used to load a tool into the tool box
        """

        self.usable_tools_dict.update({tool.name: tool.intro})

        self.__thread_instance.runtime_vars_dict.update({tool.name: tool.func})
        # once a tool_instance has been loaded into the list, we make a global func

    def remove_tool(self, name: str) -> None:

        """
        This method is used to remove a tool from the tool box
        """

        self.usable_tools_dict.pop(name)

        self.thread_instance.exec_environment.pop(name)


if __name__ == "__main__":
    tool_box = (UsableTools(thread_instance=ThreadBase()))
    print(tool_box.expose())
    print(tool_box.tool_dict)
