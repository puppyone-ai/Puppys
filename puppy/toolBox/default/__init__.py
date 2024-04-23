from puppy.toolBox.default.send_message_to_human import SendSendMessageToHuman
from puppy.toolBox.default.google_search_native import GoogleSearchNative
from puppy.toolBox.default.gpt import GPT

from puppy.thread.base import ThreadBase
from puppy.environment.base import EnvBase


class FunctionsDefault:

    # TODO: Search path to collect all the default funcs
    def __init__(self, thread_instance: ThreadBase = ThreadBase()):

        self.thread_instance = thread_instance

        self.default_funcs = [SendSendMessageToHuman, GoogleSearchNative, GPT]

        self.installed_funcs = [func(self.thread_instance) for func in self.default_funcs]

        for func in self.installed_funcs:
            setattr(self.thread_instance, getattr(func, 'name'), func)

    # generate the information of the installed funcs
    def get_infos(self, description=True, example=True) -> str:
        functions_simplified = """"""

        information = ['name']
        if description:
            information.append('description')
        if example:
            information.append('example')

        for n, action in enumerate(self.installed_funcs, start=1):
            functions_simplified += f"\n\t\t{n}."
            for info in information:
                if info == 'name':
                    functions_simplified += f"{getattr(action, info)} : "
                else:
                    functions_simplified += f"{getattr(action,info)}"

        return functions_simplified




class ToolBox(EnvBase):
    def __init__(self,thread_instance=ThreadBase()):
        super().__init__(name='ToolBox',
                         intro="a Tool Box that full of default functions",
                         visibility=False)

        self.thread_instance = thread_instance

        self.gpt = GPT(thread_instance=self.thread_instance)

        self.send_message_to_human = SendSendMessageToHuman(thread_instance=self.thread_instance)

        self.google_search_native = GoogleSearchNative(thread_instance=self.thread_instance)



if __name__ == "__main__":
    tool_box=ToolBox(thread_instance=ThreadBase())

    print(tool_box.expose)



