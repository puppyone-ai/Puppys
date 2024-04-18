from puppy.publicFunc.default.send_message_to_human import SendSendMessageToHuman
from puppy.publicFunc.default.google_search_native import GoogleSearchNative
from puppy.publicFunc.default.gpt import GPT

from puppy.thread.base import ThreadBase


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


# if __name__ == "__main__":
#     print(FunctionsDefault().get_infos())
