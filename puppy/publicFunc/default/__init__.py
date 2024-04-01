from .send_message_to_human import Send_message_to_human
from .googleSearchnative import Google_search_native
from .gpt import GPT
from .all_llm import MLLM


class ActionDefault:

    def __init__(self, code_thread_instance):
        self.codeThreadInstance = code_thread_instance
        self.send_message_to_human = Send_message_to_human(self.codeThreadInstance)
        self.google_search_native = Google_search_native(self.codeThreadInstance)
        self.gpt = GPT(self.codeThreadInstance)
        self.mllm = MLLM(self.codeThreadInstance)

        # self.send_message_to_human = Send_message_to_human(code_thread_instance)
        # self.google_search_native = Google_search_native(code_thread_instance)
        # self.mllm = MLLM(code_thread_instance)
        # self.gpt = GPT(code_thread_instance)


    # def get_descriptions(self):
    #     functionsSimplified="""
    #     """
    #     functionsSimplified+="1."+ Send_message_to_human(self.codeThreadInstance).get_name() +':'+ Send_message_to_human(self.codeThreadInstance).get_description() + "\n"
    #     functionsSimplified+="2."+ Google_search_native(self.codeThreadInstance).get_name() +':'+ Google_search_native(self.codeThreadInstance).get_description() + "\n"
    #     functionsSimplified+="3."+ MLLM(self.codeThreadInstance).get_name() +':'+ MLLM(self.codeThreadInstance).get_description() + "\n"
    #     return functionsSimplified

    # def get_examples(self):
    #     functionsExample="""
    #     """
    #     functionsExample+= Send_message_to_human(self.codeThreadInstance).get_example() + "\n"
    #     functionsExample+= Google_search_native(self.codeThreadInstance).get_example() + "\n"
    #     functionsExample += MLLM(self.codeThreadInstance).get_example() + "\n"
    #     return functionsExample

    def get_description_and_example(self):
        
        functionsDescriptionAndExample="""
        """
        functionsDescriptionAndExample+= "1."+ Send_message_to_human(self.codeThreadInstance).get_name()+':' + Send_message_to_human(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample+= Send_message_to_human(self.codeThreadInstance).get_example() + "\n"

        functionsDescriptionAndExample+= "2." + Google_search_native(self.codeThreadInstance).get_name() + ':' + Google_search_native(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample+= Google_search_native(self.codeThreadInstance).get_example() + "\n"

        functionsDescriptionAndExample += "3." + GPT(self.codeThreadInstance).get_name() + ':' + GPT(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample += GPT(self.codeThreadInstance).get_example() + "\n"

        functionsDescriptionAndExample += "4." + MLLM(self.codeThreadInstance).get_name() + ':' + MLLM(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample += MLLM(self.codeThreadInstance).get_example() + "\n"
        
        return functionsDescriptionAndExample

    def get_info(self, example=True, description=True):
        functions_simplified = """
        """
        actions = [self.send_message_to_human, self.google_search_native, self.mllm, self.gpt]

        information = ['name']
        if description:
            information.append('description')
        if example:
            information.append('example')

        for n, action in enumerate(actions, start=1):
            functions_simplified += f"{n}."
            for info in information:
                functions_simplified += f"{getattr(action,info)}"

        return functions_simplified