from puppy.tools.defaultTools.talk_with_human import TalkWithHuman
from puppy.tools.defaultTools.search import Search
from puppy.tools.defaultTools.large_language_model import LLM
from puppy.pp.base import PuppyBase
from puppy.environment.base import EnvBase


# TODO: Search path to collect all the default funcs

# the default tool box that contains all the default functions
# use to manage all tools under a pp
class UsableTools(EnvBase):
    def __init__(self, thread_instance: PuppyBase = PuppyBase(), **kwargs):

        """
        {
            "EnvBase": {
                "name": "",
                "description": "",
                "tag": "env",
                "__visibility": False
            }
        }
        """

        super().__init__(name='tool_box',
                         description="a Tool Box that full of default functions",
                         visibile=False, **kwargs)

        self.__thread_instance = thread_instance

        # default tool list
        self.sub_env_list = [TalkWithHuman(self.__thread_instance), LLM()]


        # TODO: Search path to collect all the default funcs

    @property
    def thread_instance(self):
        return self.__thread_instance

    # once a tool_instance has been loaded into the list, we make a global func
    def load_tool(self):

        for tool in self.sub_env_list:
            self.__thread_instance.runtime_vars_dict.update({tool.name: tool.func})

    def remove_tool(self, name):

        self.sub_env_list.pop(name)

        self.thread_instance.exec_environment.pop(name)


if __name__ == "__main__":
    tool_box = (UsableTools(thread_instance=PuppyBase()))
    print(tool_box.explore)
