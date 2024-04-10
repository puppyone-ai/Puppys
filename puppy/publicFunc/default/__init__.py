from puppy.publicFunc.default.send_message_to_human import SendSendMessageToHuman
from puppy.publicFunc.default.google_search_native import GoogleSearchNative
from puppy.publicFunc.default.gpt import GPT
# from puppy.publicFunc.default.all_llm import MLLM
from puppy.thread.mainThread.base import Thread


class ActionDefault:

    #TODO: Use path to coollect all the default actions, and optimise connection logic during thread init.

    def __init__(self, **kwargs):

        if 'code_thread_instance' in kwargs:
            code_thread_instance = kwargs['code_thread_instance']
        else:
            code_thread_instance = Thread()

        self.send_message_to_human = SendSendMessageToHuman(code_thread_instance)
        self.google_search_native = GoogleSearchNative(code_thread_instance)
        # self.mllm = MLLM(code_thread_instance)
        self.gpt = GPT(code_thread_instance)

    def get_info(self, description=True, example=True):
        functions_simplified = """
        """
        actions = [self.send_message_to_human, self.google_search_native, self.gpt]

        information = ['name']
        if description:
            information.append('description')
        if example:
            information.append('example')

        for n, action in enumerate(actions, start=1):
            functions_simplified += f"\n\t\t{n}."
            for info in information:
                if info == 'name':
                    functions_simplified += f"{getattr(action, info)} : "
                else:
                    functions_simplified += f"{getattr(action,info)}"

        return functions_simplified


# if __name__ == "__main__":
#     print(ActionDefault().get_info())
